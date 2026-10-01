// Obrázek sady pro Zboží.cz (1200×1200) → public/zbozi-sada.png. Spuštění: node scripts/render-zbozi.mjs (z adresáře printopia)
// Bez textu „Ukázka zdarma“ a bez vodoznaků (pravidla Zboží.cz). Stránky bere ze skutečných PDF sady (private/sada).
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRequire } from "node:module";

const root = new URL("../", import.meta.url);
const require = createRequire(new URL("../web/package.json", root));
const { chromium } = require("playwright-core");
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`public/fonts/${f}`, root)).toString("base64")}`;

const tmp = mkdtempSync(join(tmpdir(), "zbozi-"));
const pages = [["00-uvodni-test.pdf", 0], ["05-procenta.pdf", 1], ["01-zlomky.pdf", 1]];
execFileSync("python3", ["-c", `
import pymupdf, sys
for i, (name, page) in enumerate(${JSON.stringify(pages)}):
    doc = pymupdf.open("${new URL("private/sada/", root).pathname}" + name)
    doc[page].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6)).save("${tmp}/p" + str(i) + ".png")
`]);
const img = (i) => `data:image/png;base64,${readFileSync(join(tmp, `p${i}.png`)).toString("base64")}`;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
body{margin:0;width:1200px;height:1200px;background:#fbfaf6;color:#1c2230;font-family:I;position:relative;overflow:hidden;box-sizing:border-box;border-top:20px solid #2952cc}
.p{position:absolute;width:470px;background:#fff;box-shadow:0 14px 40px rgba(28,34,48,.22);border:1px solid #e4e2da}
.p img{display:block;width:100%}
.a{left:90px;top:330px;transform:rotate(-7deg)}.b{left:700px;top:350px;transform:rotate(6deg)}.c{left:395px;top:290px;z-index:2}
h1{font-family:F;font-weight:500;font-size:74px;line-height:1.05;margin:0;letter-spacing:-1px;position:absolute;left:80px;top:70px;width:1040px}
.s{position:absolute;left:80px;bottom:70px;right:80px;display:flex;justify-content:space-between;align-items:center;font-size:34px;color:#1c2230;font-weight:600}
.l{font-family:F;font-weight:600;font-size:40px}.l span{color:#f5b82e}
</style></head><body>
<h1>Přijímačky z matematiky<br>po tématech</h1>
<div class="p a"><img src="${img(1)}"></div><div class="p b"><img src="${img(2)}"></div><div class="p c"><img src="${img(0)}"></div>
<div class="s"><span>14 PDF k tisku · 12 témat · postup u každé úlohy</span><span class="l">Printopia<span>.</span></span></div>
</body></html>`;

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await browser.newPage({ viewport: { width: 1200, height: 1200 } });
await page.setContent(html, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: new URL("public/zbozi-sada.png", root).pathname });
await browser.close();
console.log("public/zbozi-sada.png");
