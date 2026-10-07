// Vizuální a textová kontrola webu (pojistky z FAILS.md 2026-10-01 02:02 a 02:05).
//   node tools/vizualni-kontrola.mjs <základní URL> <cesta1,cesta2,...> [složka na screenshoty]
// Na PC (1500 px), notebooku (1280), mobilu (390 a 360) ověří:
//  - nic nepřetéká do strany (žádný vodorovný posuvník),
//  - na PC je obsah široký max. 1340 px s 80px okraji,
//  - plovoucí prvky (absolute/fixed) nepřekrývají text ani tlačítka (měří se řádky textu, ne celé bloky),
//  - každý position:fixed prvek má nastavený z-index,
// texty (jednou na stránku):
//  - úvod (první sekce) neobsahuje provozovatele, IČO ani právní údaje (patří do patičky),
//  - žádná věta se na stránce neopakuje (vata),
//  - česká typografie: „uvozovky“, pomlčka – mezi slovy, výpustka …,
// a uloží screenshoty celé stránky pro kontrolu očima. Česky a obsahově je čte ještě člověk/Claude
// podle pravidla v CLAUDE.md. Při chybě skončí kódem 1.
import { mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const require = createRequire(new URL("../web/package.json", import.meta.url));
const { chromium } = require("playwright-core");
const [base, paths = "/", out = "/tmp/vizualni-kontrola"] = process.argv.slice(2);
const VIEWPORTS = [["pc", 1500, 900], ["notebook", 1280, 800], ["mobil", 390, 844], ["mobil-maly", 360, 740]];
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const problems = [];
for (const p of paths.split(",")) {
  for (const [name, w, h] of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(base + p, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    // Projet stránku dolů, aby se načetly líně načítané obrázky, pak zpět nahoru.
    await page.evaluate(async () => {
      document.documentElement.style.scrollBehavior = "auto"; // plynulé scrollování by screenshot zachytilo v pohybu
      for (let y = 0; y < document.documentElement.scrollHeight; y += window.innerHeight / 2) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); }
      window.scrollTo(0, 0);
      await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
      await new Promise((r) => setTimeout(r, 300));
    });
    const found = await page.evaluate((isPc) => {
      const out = [];
      const doc = document.documentElement;
      if (doc.scrollWidth > window.innerWidth + 1) out.push(`přetéká do strany: ${doc.scrollWidth} > ${window.innerWidth} px`);
      if (isPc) {
        for (const el of document.querySelectorAll(".wrap")) {
          const cs = getComputedStyle(el);
          const inner = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
          if (parseFloat(cs.paddingLeft) !== 80 || inner > 1340.5) { out.push(`.wrap: obsah ${Math.round(inner)} px, okraj ${cs.paddingLeft} (má být ≤ 1340 px a 80 px)`); break; }
        }
      }
      const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && cs.opacity !== "0"; };
      const floating = [...document.querySelectorAll("body *")].filter((el) => ["absolute", "fixed"].includes(getComputedStyle(el).position) && vis(el) && !el.closest(".hp"));
      for (const el of floating) {
        if (getComputedStyle(el).position === "fixed" && getComputedStyle(el).zIndex === "auto") out.push(`fixed bez z-indexu: ${el.className || el.tagName}`);
      }
      const texts = [...document.querySelectorAll("h1,h2,h3,p,li,label,dt,dd,td,summary,a.btn,button,input")].filter(vis);
      // U textových bloků se měří jednotlivé řádky (Range), aby prázdné místo vedle textu nebylo falešný překryv.
      const rectsOf = (t) => {
        if (t.matches("a.btn,button,input")) return [t.getBoundingClientRect()];
        const r = document.createRange();
        r.selectNodeContents(t);
        return [...r.getClientRects()].filter((x) => x.width > 1 && x.height > 1);
      };
      for (const f of floating) {
        const fr = f.getBoundingClientRect();
        for (const t of texts) {
          if (f.contains(t) || t.contains(f)) continue;
          const hit = rectsOf(t).some((tr) => {
            const ix = Math.min(fr.right, tr.right) - Math.max(fr.left, tr.left);
            const iy = Math.min(fr.bottom, tr.bottom) - Math.max(fr.top, tr.top);
            return ix > 2 && iy > 2;
          });
          if (hit) { out.push(`překryv: ${f.className || f.tagName} přes „${(t.innerText || t.value || t.tagName).trim().slice(0, 40)}“`); break; }
        }
      }
      if (isPc) {
        const main = document.querySelector("main") ?? document.body;
        const first = main.querySelector("section");
        const legal = /IČO|IČ:|s\.r\.o\.|provozuje|Provozuje|spisová značka|obchodním rejstříku/;
        const legalPage = /ochrana-osobnich-udaju|obchodni-podminky|odstoupeni-od-smlouvy|doklad/.test(location.pathname);
        if (first && !legalPage && legal.test(first.innerText)) out.push(`text: úvod obsahuje provozovatele/právní údaje („${first.innerText.match(legal)[0]}“), patří do patičky`);
        const text = main.innerText;
        const sentences = text.split(/(?<=[.!?])\s+|\n+/).map((x) => x.trim()).filter((x) => x.length > 40);
        const seen = new Set();
        for (const x of sentences) { if (seen.has(x)) out.push(`text: věta se opakuje: „${x.slice(0, 60)}“`); seen.add(x); }
        const typo = [[/"[^"\n]{1,80}"/, "rovné uvozovky místo „…“"], [/\S \- \S/, "spojovník místo pomlčky –"], [/\.\.\./, "tři tečky místo …"]];
        for (const [rx, msg] of typo) { const m = text.match(rx); if (m) out.push(`text: ${msg}: „${m[0].slice(0, 40)}“`); }
      }
      return [...new Set(out)];
    }, name === "pc");
    for (const f of found) problems.push(`${p} [${name} ${w}px] ${f}`);
    await page.screenshot({ path: path.join(out, `${p.replace(/\W+/g, "_") || "home"}-${name}.png`), fullPage: true });
    await page.close();
  }
}
await browser.close();
if (problems.length) {
  console.log("Vizuální kontrola: PROBLÉMY\n- " + problems.join("\n- "));
  process.exit(1);
}
console.log(`Vizuální kontrola: OK (${paths.split(",").length} stránek × ${VIEWPORTS.length} šířek), screenshoty v ${out}`);
