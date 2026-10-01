// Pracovní listy sady (A4 PDF) ze src/content/sada/*.json → private/sada/*.pdf + src/content/sada-soubory.json.
// Spuštění (z adresáře printopia): for f in content/sada/[0-9]*.py; do python3 "$f"; done && node scripts/render-sada.mjs
// Řešení jsou vždy na samostatných stranách na konci listu, aby je žák neviděl předem.
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../", import.meta.url);
const require = createRequire(new URL("../web/package.json", root));
const { chromium } = require("playwright-core");
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const LEVELS = { 1: "Základ", 2: "Jako u zkoušky", 3: "Náročnější" };
const KIND = { open: "", choice: "Vyberte jednu možnost.", yesno: "Rozhodněte o každém tvrzení, zda je pravdivé (ANO), či nikoli (NE).", construct: "Rýsujte tužkou a pravítkem." };

const dir = new URL("src/content/sada/", root);
const topics = readdirSync(dir).filter((f) => f.endsWith(".json")).sort().map((f) => JSON.parse(readFileSync(new URL(f, dir), "utf8")));
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`public/fonts/${f}`, root)).toString("base64")}`;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
// Zlomky „a/b“ sázíme nad sebou (i se záporným čitatelem); „/“ mezi závorkami necháváme jako lomítko.
// Proměnné jen a–d, n, x, y, aby se jednotky jako km/h nebo m/s nesázely jako zlomek.
// Česká typografie: číslo + jednotka, tisíce a jednopísmenné předložky se na konci řádku nerozdělí (nezlomitelná mezera).
const nbsp = (s) => s.replace(/(\d) (?=[\p{L}%‰°\d])/gu, "$1\u00a0").replace(/(^|[\s(>])([kKsSvVzZoOuUaAiI]) (?=\S)/g, "$1$2\u00a0");
const math = (s) => nbsp(esc(s)).replace(/(?<![\p{L}\d,])(−?(?:\d+(?:,\d+)?|[a-dnxy]))\/(\d+(?:,\d+)?|[a-dnxy])(?![\p{L}\d(])/gu, '<span class="fr"><span>$1</span><span>$2</span></span>');

const CSS = `
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@page{size:A4;margin:15mm 16mm 17mm}
body{font-family:I;color:#1c2230;font-size:10.5pt;margin:0}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.5pt solid #2952cc;padding-bottom:6pt;margin-bottom:10pt}
.logo{font-family:F;font-weight:600;font-size:15pt}.logo span{color:#f5b82e}
h1{font-family:F;font-weight:500;font-size:22pt;margin:0 0 2pt;line-height:1.1}
h2{font-family:F;font-weight:500;font-size:15pt;margin:14pt 0 6pt;break-after:avoid}
.sub{color:#5f6675;font-size:9pt}
.intro{background:#eaf0ff;border-radius:6pt;padding:7pt 10pt;font-size:9.5pt;margin-bottom:8pt}
.tips{margin:0;padding-left:14pt;font-size:9.5pt}.tips li{margin-bottom:2pt}
.example{border:1pt solid #2952cc;border-radius:6pt;padding:7pt 10pt;margin-top:8pt;break-inside:avoid}
.example .lbl{font-weight:700;color:#2952cc;font-size:8.5pt;text-transform:uppercase;letter-spacing:.08em}
.example ol{margin:3pt 0 0;padding-left:15pt}
.level{display:flex;align-items:center;gap:6pt;margin:12pt 0 0;font-family:F;font-size:13pt;break-after:avoid}
.level i{display:inline-block;width:7pt;height:7pt;border-radius:50%;background:#f5b82e}
.task{break-inside:avoid;border-bottom:.6pt solid #e4e2da;padding:5pt 0 0}
.q{margin:2pt 0 0}.hint{color:#5f6675;font-size:8.5pt}
.opts{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt;margin:5pt 0 2pt;font-size:10pt}
.opts.long{grid-template-columns:1fr}
.yn{border-collapse:collapse;margin:5pt 0 2pt;font-size:10pt}.yn td{padding:2pt 8pt 2pt 0}.yn .box{color:#5f6675;white-space:nowrap}
.fig{margin:4pt 0}.fig svg{max-width:62mm;max-height:42mm}
.space{background-image:linear-gradient(#eef0f4 .5pt,transparent .5pt);background-size:100% 7mm;margin:4pt 0 5pt}
.sol{break-inside:avoid;border-bottom:.6pt solid #e4e2da;padding:5pt 0}
.sol ol{margin:3pt 0 0;padding-left:15pt;color:#3a4150}
.a{font-weight:600;color:#1f3f9e;margin:3pt 0 0}
.break{break-before:page}
.stop{border:1.5pt dashed #f5b82e;background:#fdf3dc;border-radius:6pt;padding:6pt 10pt;font-weight:600;margin-bottom:8pt;text-align:center}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1.05;margin:0 1.5pt}
.fr span:first-child{border-bottom:.7pt solid currentColor;padding:0 1.5pt}
.sol li,.q,.example li,.opts{line-height:1.85}
.lic{margin-top:10pt;color:#5f6675;font-size:8pt}
table.eval,table.plan{width:100%;border-collapse:collapse;font-size:9.5pt;margin:6pt 0}
.eval th,.eval td,.plan th,.plan td{border-bottom:.6pt solid #e4e2da;padding:4pt 6pt 4pt 0;text-align:left;vertical-align:top}
.plan td{break-inside:avoid}.plan .date{width:28mm;border-bottom:.6pt solid #c9ccd4}.box{white-space:nowrap;color:#5f6675}`;

const options = (t) => {
  if (t.kind === "choice") {
    const long = t.options.some((o) => o.length > 14);
    return `<div class="opts${long ? " long" : ""}">${t.options.map((o, i) => `<span><b>${"ABCDE"[i]})</b> ${math(o)}</span>`).join("")}</div>`;
  }
  if (t.kind === "yesno") return `<table class="yn">${t.options.map((o, i) => `<tr><td>${i + 1}. ${math(o)}</td><td class="box">☐ ANO ☐ NE</td></tr>`).join("")}</table>`;
  return "";
};

function topicHtml(d) {
  let n = 0;
  let lastLevel = 0;
  const tasks = d.tasks.map((t) => {
    n++;
    const head = t.level !== lastLevel ? `<div class="level"><i></i>${LEVELS[t.level]}</div>` : "";
    lastLevel = t.level;
    return `${head}<div class="task"><p class="q"><b>${n}.</b> ${math(t.text)}${KIND[t.kind] ? ` <span class="hint">${KIND[t.kind]}</span>` : ""}</p>${t.figure ? `<div class="fig">${t.figure}</div>` : ""}${options(t)}<div class="space" style="height:${t.space * 7}mm"></div></div>`;
  }).join("");
  const sols = d.tasks.map((t, i) => `<div class="sol"><p class="q"><b>${i + 1}.</b> ${math(t.text)}</p><ol>${t.steps.map((s) => `<li>${math(s)}</li>`).join("")}</ol><p class="a">Výsledek: ${math(t.answer)}</p></div>`).join("");
  const ex = d.example;
  return `<header><div><h1>${esc(d.title)}</h1><div class="sub">Téma ${d.num} · ${d.tasks.length} úloh od základu po náročnější · postupy řešení na konci</div></div><div class="logo">Printopia<span>.</span></div></header>
<div class="intro">${math(d.intro)}</div>
<b>Na co si dát pozor</b><ul class="tips">${d.tips.map((x) => `<li>${math(x)}</li>`).join("")}</ul>
<div class="example"><div class="lbl">Řešený příklad</div><p class="q">${math(ex.text)}</p><ol>${ex.steps.map((s) => `<li>${math(s)}</li>`).join("")}</ol><p class="a">Výsledek: ${math(ex.answer)}</p></div>
${tasks}
<div class="break"></div><div class="stop">Řešení · nahlédněte až po výpočtu</div><h2 style="margin-top:0">Postupy řešení: ${esc(d.title)}</h2>${sols}
<p class="lic">© MYPIXEL s.r.o., printopia.cz. Jen pro potřebu kupující domácnosti, tisk povolen. Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky, nejde o oficiální materiál CERMAT.</p>`;
}

const doc = (title, body) => `<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>${esc(title)}</title><style>${CSS}</style></head><body>${body}</body></html>`;
const footer = (title) => `<div style="font-family:Arial;font-size:7pt;color:#8b93a6;width:100%;padding:0 16mm;display:flex;justify-content:space-between"><span>Printopia · ${esc(title)}</span><span><span class="pageNumber"></span>/<span class="totalPages"></span></span></div>`;

const outDir = new URL("private/sada/", root);
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROMIUM });
const page = await browser.newPage();
const files = [];
async function pdf(file, title, body) {
  await page.setContent(doc(title, body), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: new URL(file, outDir).pathname, format: "A4", printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: "<span></span>", footerTemplate: footer(title) });
}
// Úvodní test: 2 úlohy z každého tématu, vyhodnocení podle témat (rodič pozná, čím začít).
{
  const items = topics.flatMap((d) => d.diagnostic.map((t) => ({ ...t, topic: d })));
  const qs = items.map((t, i) => `<div class="task"><p class="q"><b>${i + 1}.</b> ${math(t.text)}${KIND[t.kind] ? ` <span class="hint">${KIND[t.kind]}</span>` : ""}</p>${t.figure ? `<div class="fig">${t.figure}</div>` : ""}${options(t)}<div class="space" style="height:21mm"></div></div>`).join("");
  const sols = items.map((t, i) => `<div class="sol"><p class="q"><b>${i + 1}.</b> ${math(t.text)} <span class="hint">téma ${t.topic.num}</span></p><ol>${t.steps.map((x) => `<li>${math(x)}</li>`).join("")}</ol><p class="a">Výsledek: ${math(t.answer)}</p></div>`).join("");
  const rows = topics.map((d) => {
    const nums = items.map((t, i) => (t.topic === d ? i + 1 : 0)).filter(Boolean);
    return `<tr><td>${d.num}. ${esc(d.title)}</td><td>${nums.join(" a ")}</td><td class="box">☐ ☐</td><td class="box">☐ nejdřív</td></tr>`;
  }).join("");
  const body = `<header><div><h1>Úvodní test</h1><div class="sub">${items.length} úloh, 2 z každého tématu · asi ${Math.round(items.length * 3.5 / 10) * 10} minut, klidně na dvakrát · vyhodnocení a postupy na konci</div></div><div class="logo">Printopia<span>.</span></div></header>
<div class="intro">Počítejte bez kalkulačky a bez nápovědy, jako u zkoušky. Úlohu, kterou nevíte, přeskočte, nehádejte. Test neslouží ke známkování: ukáže, která témata procvičit nejdřív.</div>
${qs}
<div class="break"></div><div class="stop">Vyhodnocení a řešení · až po dopočítání testu</div>
<h2 style="margin-top:0">Vyhodnocení podle témat</h2>
<p>U každé správně vyřešené úlohy zaškrtněte políčko. Téma, kde není správně aspoň jedna úloha ze dvou, zařaďte do plánu jako první. Témata s oběma úlohami správně stačí na konci zopakovat.</p>
<table class="eval"><tr><th>Téma</th><th>Úlohy</th><th>Správně</th><th>Procvičit</th></tr>${rows}</table>
<h2>Postupy řešení</h2>${sols}
<p class="lic">© MYPIXEL s.r.o., printopia.cz. Jen pro potřebu kupující domácnosti, tisk povolen. Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky, nejde o oficiální materiál CERMAT.</p>`;
  await pdf("00-uvodni-test.pdf", "Úvodní test", body);
  files.push({ slug: "uvodni-test", file: "00-uvodni-test.pdf", title: "Úvodní test", desc: `${items.length} úloh, ukáže, čím začít` });
  console.log("00-uvodni-test.pdf", items.length);
}

for (const d of topics) {
  const file = `${String(d.num).padStart(2, "0")}-${d.slug}.pdf`;
  await pdf(file, d.title, topicHtml(d));
  files.push({ slug: d.slug, file, title: `${d.num}. ${d.title}`, desc: `${d.tasks.length} úloh s postupy` });
  console.log(file, d.tasks.length);
}
// Plán procvičování: jedno téma týdně, opakování a oficiální testy na konci. Data si rodina vyplní sama.
{
  const weeks = [["Úvodní test", "Vyhodnoťte a podle něj seřaďte témata: slabá dopředu."]];
  topics.forEach((d, i) => {
    weeks.push([`Téma: ${d.title}`, "Řešený příklad, pak úlohy Základ a Jako u zkoušky. Náročnější podle chuti."]);
    if ((i + 1) % 4 === 0) weeks.push(["Opakování", "Ke každému z posledních čtyř témat znovu 3 úlohy, které nešly."]);
  });
  weeks.push(["Oficiální test CERMAT", "Jeden test z minulých let na čas (70 minut), zdarma na prijimacky.cermat.cz. Chyby dohledejte v tématech."]);
  weeks.push(["Oficiální test CERMAT", "Další test na čas. Co nejde, zopakujte podle listu tématu."]);
  weeks.push(["Poslední týden", "Jen lehké opakování a odpočinek. Pomůcky: tužka, pravítko, kružítko, bez kalkulačky."]);
  const rows = weeks.map(([what, how], i) => `<tr><td>${i + 1}.</td><td class="date"></td><td><b>${esc(what)}</b><br><span class="hint">${esc(how)}</span></td><td class="box">☐</td></tr>`).join("");
  const body = `<header><div><h1>Plán procvičování</h1><div class="sub">${weeks.length} týdnů do zkoušky · jedno téma týdně · data si doplňte sami</div></div><div class="logo">Printopia<span>.</span></div></header>
<div class="intro">Nejlépe 3× týdně 30 až 40 minut. Když do zkoušky zbývá méně týdnů, berte dvě témata týdně a vynechte úlohy Náročnější u témat, která jdou. Když se úloha nedaří, vraťte se k řešenému příkladu na začátku listu.</div>
<table class="plan"><tr><th>Týden</th><th>Od – do</th><th>Co dělat</th><th>Hotovo</th></tr>${rows}</table>
<p class="lic">© MYPIXEL s.r.o., printopia.cz. Jen pro potřebu kupující domácnosti, tisk povolen.</p>`;
  await pdf("99-plan-procvicovani.pdf", "Plán procvičování", body);
  files.push({ slug: "plan", file: "99-plan-procvicovani.pdf", title: "Plán procvičování", desc: `${weeks.length} týdnů, jedno téma týdně` });
  console.log("99-plan-procvicovani.pdf", weeks.length);
}
await browser.close();
writeFileSync(new URL("src/content/sada-soubory.json", root), JSON.stringify(files, null, 1) + "\n");
console.log(`${files.length} listů → private/sada/`);
