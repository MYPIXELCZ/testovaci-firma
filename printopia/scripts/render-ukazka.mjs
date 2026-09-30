// Generuje ukázku „Zlomky“ (A4 PDF) ze src/content/ukazka.json → public/ukazka-zlomky.pdf
// Spuštění: python3 content/ukazka.py && node scripts/render-ukazka.mjs (z adresáře printopia)
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../", import.meta.url);
const require = createRequire(new URL("../web/package.json", root));
const { chromium } = require("playwright-core");
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

const data = JSON.parse(readFileSync(new URL("src/content/ukazka.json", root), "utf8"));
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`public/fonts/${f}`, root)).toString("base64")}`;
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
// Zlomky „a/b“ sázíme nad sebou; „/“ mezi závorkami (složený zlomek) necháváme jako lomítko.
const math = (s) => esc(s).replace(/(\d+)\/(\d+)/g, '<span class="fr"><span>$1</span><span>$2</span></span>');

const tasks = data.tasks
  .map((t, i) => `<div class="task"><div class="tag">${esc(t.topic)}</div><p class="q"><b>${i + 1}.</b> ${math(t.text)}</p><div class="space"></div></div>`)
  .join("");
const solutions = data.tasks
  .map((t, i) => `<div class="sol"><p class="q"><b>${i + 1}.</b> ${math(t.text)}</p><ol>${t.steps.map((s) => `<li>${math(s)}</li>`).join("")}</ol><p class="a">Výsledek: ${math(t.answer)}</p></div>`)
  .join("");

const html = `<!doctype html><html lang="cs"><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@page{size:A4;margin:16mm 17mm 16mm}
body{font-family:I;color:#1c2230;font-size:11pt;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.5pt solid #2952cc;padding-bottom:7pt;margin-bottom:12pt}
.logo{font-family:F;font-weight:600;font-size:16pt}.logo span{color:#f5b82e}
h1{font-family:F;font-weight:500;font-size:24pt;margin:0 0 3pt;line-height:1.1}
h2{font-family:F;font-weight:500;font-size:18pt;margin:0 0 10pt}
.sub{color:#5f6675;font-size:9.5pt}
.intro{background:#eaf0ff;border-radius:6pt;padding:8pt 11pt;font-size:9.5pt;margin-bottom:12pt}
.task{break-inside:avoid;border-bottom:.6pt solid #e4e2da;padding:6pt 0 0}
.tag{display:inline-block;background:#fdf3dc;border-radius:3pt;padding:0 5pt;font-size:8pt;font-weight:600}
.q{margin:3pt 0 0}
.space{height:28mm;background-image:linear-gradient(#eef0f4 .5pt,transparent .5pt);background-size:100% 7mm;margin:4pt 0 6pt}
.sol{break-inside:avoid;border-bottom:.6pt solid #e4e2da;padding:6pt 0}
.sol ol{margin:4pt 0 0;padding-left:16pt;color:#3a4150}
.a{font-weight:600;color:#1f3f9e;margin:4pt 0 0}
.break{break-before:page}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1.05;margin:0 1.5pt}
.fr span:first-child{border-bottom:.7pt solid currentColor;padding:0 1.5pt}
.sol li,.q{line-height:1.9}
.foot{margin-top:12pt;color:#5f6675;font-size:8.5pt}
</style></head><body>
<header><div><h1>Přijímačky z matiky: ${esc(data.title)}</h1><div class="sub">Ukázka zdarma · ${data.tasks.length} úloh s postupem řešení · printopia.cz</div></div><div class="logo">Printopia<span>.</span></div></header>
<div class="intro">Počítejte bez kalkulačky, jako u zkoušky. Postupy řešení najdete na konci. Když úloha nevyjde, projděte postup krok za krokem a najděte místo, kde se výpočet rozešel.</div>
${tasks}
<div class="break"></div>
<h2>Postupy řešení</h2>
${solutions}
<p class="foot">Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky, nejde o oficiální materiál CERMAT. Kompletní sada podle témat: printopia.cz · MYPIXEL s.r.o., IČO 17617421</p>
</body></html>`;

const browser = await chromium.launch({ executablePath: CHROMIUM });
const page = await browser.newPage();
await page.setContent(html, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
const out = new URL("public/ukazka-zlomky.pdf", root).pathname;
await page.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log(out);
