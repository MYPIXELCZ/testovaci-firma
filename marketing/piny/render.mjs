// Generuje piny na Pinterest (1000×1500) z obsahu plánovače. Spuštění: node marketing/piny/render.mjs
// Potřebuje playwright-core z web/node_modules a Chromium (CHROMIUM_PATH).
import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";

const root = new URL("../../", import.meta.url);
const require = createRequire(new URL("web/package.json", root));
const { chromium } = require("playwright-core");
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

const planner = JSON.parse(readFileSync(new URL("web/src/content/planner.json", root), "utf8"));
const font = (f) => `data:font/woff2;base64,${readFileSync(new URL(`web/public/fonts/${f}`, root)).toString("base64")}`;
const img = (f) => `data:image/png;base64,${readFileSync(new URL(`web/public/img/${f}`, root)).toString("base64")}`;
const logo = `data:image/svg+xml;base64,${readFileSync(new URL("brand/logo.svg", root)).toString("base64")}`;

const css = `
@font-face{font-family:F;src:url(${font("fraunces-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:F;src:url(${font("fraunces-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
@font-face{font-family:I;src:url(${font("inter-latin-wght-normal.woff2")});font-weight:100 900}
@font-face{font-family:I;src:url(${font("inter-latin-ext-wght-normal.woff2")});font-weight:100 900;unicode-range:U+0100-02BA,U+1E00-1EFF}
*{box-sizing:border-box}body{margin:0;width:1000px;height:1500px;background:#FAF7F2;color:#2B2A28;font-family:I;display:flex;flex-direction:column;padding:80px 80px 70px}
.eyebrow{font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#9A5238;font-weight:600;margin-bottom:24px}
h1{font-family:F;font-weight:500;font-size:84px;line-height:1.04;margin:0 0 40px;letter-spacing:-1px}
.dot{color:#B5694A}.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.row{display:flex;gap:28px;align-items:baseline;border-bottom:2px solid #E6E0D6;padding:18px 0;font-size:31px}
.row b{font-family:F;font-weight:600;color:#56654A;min-width:200px;font-size:32px}
.bar{height:22px;background:#7C8B6F;border-radius:11px}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:40px;font-size:30px;color:#56654A;font-weight:600}
.foot img{width:260px}
.shot{background:#fff;border-radius:22px;padding:14px;box-shadow:0 30px 70px -30px rgba(0,0,0,.35);transform:rotate(1.2deg)}
.shot img{width:100%;border-radius:12px;display:block}
.cta{display:inline-block;background:#56654A;color:#fff;border-radius:999px;padding:22px 40px;font-size:32px;font-weight:600;margin-top:36px}
`;

const page = (body) => `<!doctype html><html lang="cs"><head><meta charset="utf-8"><style>${css}</style></head><body>${body}
<div class="foot"><img src="${logo}"><span>anoberu.cz</span></div></body></html>`;

const phases = [...new Set(planner.tasks.map((t) => t.phase))].filter((p) => !["Den D", "Po svatbě"].includes(p));
const firstTask = (p) => planner.tasks.find((t) => t.phase === p).task.replace(/ \(.*\)$/, "");

const pins = {
  "checklist.png": page(`<div class="eyebrow">Svatební checklist</div><h1>Co zařídit a kdy<span class="dot">.</span></h1>
    <div class="main">${phases.map((p) => `<div class="row"><b>${p}</b><span>${firstTask(p)}</span></div>`).join("")}
    <p style="font-size:30px;color:#6B665E;margin-top:32px">Celý seznam ${planner.tasks.length} úkolů najdete na webu.</p></div>`),

  "rozpocet.png": page(`<div class="eyebrow">Svatební rozpočet</div><h1>Jak ho rozdělit<span class="dot">.</span></h1>
    <div class="main">${planner.categories.filter((c) => c.share >= 0.03).map((c) => `<div class="row" style="align-items:center">
      <b style="min-width:360px;font-size:30px">${c.name}</b><div class="bar" style="width:${c.share * 700}px"></div>
      <span style="font-weight:600">${Math.round(c.share * 100)} %</span></div>`).join("")}
    <p style="font-size:28px;color:#6B665E;margin-top:28px">Orientační rozdělení podle běžné praxe českých svateb.</p></div>`),

  "harmonogram.png": page(`<div class="eyebrow">Den D</div><h1>Harmonogram svatebního dne<span class="dot">.</span></h1>
    <div class="main">${planner.dayPlan.slice(0, 13).map((d) => `<div class="row" style="padding:13px 0;font-size:28px"><b style="min-width:120px">${d.time}</b><span>${d.what.replace(/ \(.*\)$/, "")}</span></div>`).join("")}</div>`),

  "oznameni.png": page(`<div class="eyebrow">Svatební oznámení</div><h1>Vzory textů, které stačí přepsat<span class="dot">.</span></h1>
    <div class="main">
      <div style="background:#fff;border-radius:18px;padding:48px 52px;box-shadow:0 20px 50px -25px rgba(0,0,0,.3);font-family:F;font-size:40px;line-height:1.35;text-align:center">
        S radostí oznamujeme, že si<br><b style="font-weight:600">12. června 2027</b><br>řekneme své ano.<br><span style="font-size:30px;color:#6B665E;font-family:I">Tereza a Jakub</span></div>
      <p style="font-size:30px;color:#6B665E;margin-top:36px">+ 4 další vzory a co v oznámení nesmí chybět</p></div>`),

  "svedek.png": page(`<div class="eyebrow">Pro svědky</div><h1>Co čeká svědka na svatbě<span class="dot">.</span></h1>
    <div class="main">${["Prsteny a doklady u sebe", "Hlídat harmonogram a čas", "Kontakt pro dodavatele", "Obálky s doplatky", "Nouzová taška", "Skupinové focení", "Proslov a přípitek"].map((t) => `<div class="row"><b style="min-width:60px;color:#B5694A">✓</b><span>${t}</span></div>`).join("")}</div>`),

  "podekovani.png": page(`<div class="eyebrow">Po svatbě</div><h1>Poděkování za svatební dar<span class="dot">.</span></h1>
    <div class="main">
      <div style="background:#fff;border-radius:18px;padding:48px 52px;box-shadow:0 20px 50px -25px rgba(0,0,0,.3);font-family:F;font-size:38px;line-height:1.38">
        Milá teto Marie,<br>sada hrnků od Tebe už má doma čestné místo. Děkujeme, že jsi s námi slavila až do rána.<br><span style="font-size:30px;color:#6B665E;font-family:I">Tereza a Jakub</span></div>
      <p style="font-size:30px;color:#6B665E;margin-top:36px">+ 4 další vzory a kdy poděkování poslat</p></div>`),

  "planovac.png": page(`<div class="eyebrow">Pro Excel a Google Tabulky</div><h1>Naplánujte si svatbu v klidu<span class="dot">.</span></h1>
    <div class="main"><div class="shot"><img src="${img("prehled.png")}"></div>
    <div><span class="cta">Svatební plánovač za 349 Kč</span></div></div>`),
};

const browser = await chromium.launch({ executablePath: CHROMIUM });
const p = await browser.newPage({ viewport: { width: 1000, height: 1500 } });
for (const [name, html] of Object.entries(pins)) {
  await p.setContent(html, { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: new URL(name, import.meta.url).pathname });
  console.log("marketing/piny/" + name);
}
await browser.close();
writeFileSync(new URL("README.md", import.meta.url), `# Piny na Pinterest\n\nGeneruje \`node marketing/piny/render.mjs\` z \`web/src/content/planner.json\`. Formát 1000×1500 (2:3).\n\n| Pin | Odkaz |\n|---|---|\n| checklist.png | https://anoberu.cz/svatebni-checklist |\n| rozpocet.png | https://anoberu.cz/svatebni-rozpocet |\n| harmonogram.png | https://anoberu.cz/harmonogram-svatebniho-dne |\n| oznameni.png | https://anoberu.cz/text-svatebniho-oznameni |\n| svedek.png | https://anoberu.cz/svedek-na-svatbe |\n| podekovani.png | https://anoberu.cz/podekovani-za-svatebni-dar |\n| planovac.png | https://anoberu.cz/ |\n`);
