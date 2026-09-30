// Generuje svatební checklist k tisku (A4 PDF) z obsahu plánovače.
// Spuštění: node marketing/checklist-pdf/render.mjs  → web/public/ke-stazeni/svatebni-checklist-anoberu.pdf
import { mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../../", import.meta.url);
const require = createRequire(new URL("web/package.json", root));
const { chromium } = require("playwright-core");
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

const planner = JSON.parse(readFileSync(new URL("web/src/content/planner.json", root), "utf8"));
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`web/public/fonts/${f}`, root)).toString("base64")}`;
const logo = `data:image/svg+xml;base64,${readFileSync(new URL("brand/logo.svg", root)).toString("base64")}`;

const phases = [...new Set(planner.tasks.map((t) => t.phase))];
const heading = (p) => (["Den D", "Po svatbě", "Poslední týden"].includes(p) ? p : `${p} před svatbou`);

const html = `<!doctype html><html lang="cs"><head><meta charset="utf-8"><style>
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@page{size:A4;margin:16mm 16mm 18mm}
body{font-family:I;color:#2B2A28;font-size:10.5pt;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.5pt solid #7C8B6F;padding-bottom:8pt;margin-bottom:12pt}
header img{width:44mm}
h1{font-family:F;font-weight:500;font-size:26pt;margin:0 0 2pt;line-height:1.1}
.sub{color:#6B665E;font-size:10pt}
.cols{columns:2;column-gap:10mm}
.phase{break-inside:avoid;margin-bottom:9pt}
h2{font-family:F;font-weight:600;font-size:12pt;color:#56654A;margin:0 0 3pt}
li{list-style:none;display:flex;gap:6pt;padding:2.2pt 0;border-bottom:.5pt solid #E6E0D6;line-height:1.3}
ul{margin:0;padding:0}
.box{flex:none;width:8pt;height:8pt;border:1pt solid #56654A;border-radius:1.5pt;margin-top:2pt}
.cta{break-inside:avoid;margin-top:10pt;background:#EEF1EA;border-radius:6pt;padding:9pt 11pt;font-size:10pt}
.cta b{font-family:F;font-size:12pt;font-weight:600}
.note{color:#6B665E;font-size:8.5pt;margin-top:6pt}
.extra{break-before:avoid;margin-top:14pt}
.extra h2{font-size:13pt;margin-bottom:6pt}
table{width:100%;border-collapse:collapse;margin-bottom:14pt}
td{border-bottom:.6pt solid #CFC8BC;height:17pt;font-size:9.5pt;color:#6B665E;vertical-align:bottom;padding:0 6pt 2pt 0}
td:first-child{width:32%}
.lines div{border-bottom:.6pt solid #CFC8BC;height:19pt}
</style></head><body>
<header><div><h1>Svatební checklist</h1><div class="sub">${planner.tasks.length} úkolů od zásnub po svatební cestu</div></div><img src="${logo}"></header>
<div class="cols">
${phases.map((p) => `<div class="phase"><h2>${heading(p)}</h2><ul>${planner.tasks.filter((t) => t.phase === p).map((t) => `<li><span class="box"></span><span>${t.task}</span></li>`).join("")}</ul></div>`).join("")}
<div class="cta"><b>Termíny si hlídat nemusíte.</b><br>V plánovači Ano, beru zadáte datum svatby a u každého úkolu se dopočítá konkrétní termín. K tomu rozpočet, hosté, zasedací pořádek a harmonogram dne D. <b style="font-size:10pt">anoberu.cz</b></div>
<p class="note">Termíny jsou orientační. Doklady, lhůty a poplatky pro sňatek vždy ověřte na své matrice. © Ano, beru · MYPIXEL s.r.o.</p>
</div>
<div class="extra"><h2>Důležité kontakty</h2><table>
${["Matrika / oddávající", "Místo obřadu a hostiny", "Fotograf", "Kameraman", "Kapela / DJ", "Floristka", "Kadeřnice a vizážistka", "Svědek", "Svědkyně", "Doprava"].map((k) => `<tr><td>${k}</td><td></td></tr>`).join("")}
</table><h2>Poznámky</h2><div class="lines">${"<div></div>".repeat(5)}</div></div>
</body></html>`;

const out = new URL("web/public/ke-stazeni/", root);
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROMIUM });
const page = await browser.newPage();
await page.setContent(html, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: new URL("svatebni-checklist-anoberu.pdf", out).pathname, format: "A4", printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log("web/public/ke-stazeni/svatebni-checklist-anoberu.pdf");
