// Generuje náhledové obrázky pro sdílení článků (1200×630) do web/public/og/{slug}.png.
// Spuštění: node marketing/og/render.mjs
import { mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../../", import.meta.url);
const require = createRequire(new URL("web/package.json", root));
const { chromium } = require("playwright-core");
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

// Seznam článků čteme přímo z web/src/content/articles.ts (href + title).
const src = readFileSync(new URL("web/src/content/articles.ts", root), "utf8");
const articles = [...src.matchAll(/href: "\/([^"]+)",\s*title: "([^"]+)"/g)].map((m) => ({ slug: m[1], title: m[2] }));

const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`web/public/fonts/${f}`, root)).toString("base64")}`;
const logo = `data:image/svg+xml;base64,${readFileSync(new URL("brand/logo.svg", root)).toString("base64")}`;

const html = (title) => `<!doctype html><html lang="cs"><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
body{margin:0;width:1200px;height:630px;background:#FAF7F2;color:#2B2A28;font-family:I;display:flex;flex-direction:column;justify-content:space-between;padding:70px 90px;box-sizing:border-box;border-left:18px solid #7C8B6F}
.eyebrow{font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#9A5238;font-weight:600}
h1{font-family:F;font-weight:500;font-size:72px;line-height:1.08;margin:18px 0 0;letter-spacing:-1px;max-width:980px}
.dot{color:#B5694A}.foot{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#56654A;font-weight:600}
.foot img{width:250px}
</style></head><body><div><div class="eyebrow">Plánování svatby</div><h1>${title}<span class="dot">.</span></h1></div>
<div class="foot"><img src="${logo}"><span>anoberu.cz</span></div></body></html>`;

const out = new URL("web/public/og/", root);
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROMIUM });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
for (const a of articles) {
  await page.setContent(html(a.title), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: new URL(`${a.slug}.png`, out).pathname });
  console.log(`web/public/og/${a.slug}.png`);
}
await browser.close();
