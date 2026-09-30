// Náhled pro sdílení (1200×630) → public/og.png. Spuštění: node scripts/render-og.mjs (z adresáře printopia)
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../", import.meta.url);
const require = createRequire(new URL("../web/package.json", root));
const { chromium } = require("playwright-core");
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`public/fonts/${f}`, root)).toString("base64")}`;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
body{margin:0;width:1200px;height:630px;background:#fbfaf6;color:#1c2230;font-family:I;display:flex;flex-direction:column;justify-content:space-between;padding:72px 90px;box-sizing:border-box;border-top:18px solid #2952cc}
.e{font-size:26px;letter-spacing:.12em;text-transform:uppercase;color:#2952cc;font-weight:600}
h1{font-family:F;font-weight:500;font-size:84px;line-height:1.05;margin:18px 0 0;letter-spacing:-1px}
.f{display:flex;justify-content:space-between;align-items:center;font-size:30px;color:#5f6675}
.l{font-family:F;font-weight:600;font-size:40px;color:#1c2230}.l span{color:#f5b82e}
</style></head><body><div><div class="e">Přijímačky na SŠ · matematika</div><h1>Přijímačky z matiky po tématech</h1></div>
<div class="f"><span>Úlohy k tisku s postupem · ukázka zdarma</span><span class="l">Printopia<span>.</span></span></div></body></html>`;

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.setContent(html, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: new URL("public/og.png", root).pathname });
await browser.close();
console.log("public/og.png");
