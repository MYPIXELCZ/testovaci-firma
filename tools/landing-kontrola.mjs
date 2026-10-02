// Kontrola přistávacího webu proti normě (pojistky z FAILS.md 2026-10-02 13:50 a 13:53).
//   node tools/landing-kontrola.mjs <URL> [složka na screenshoty]
// Měří na PC (1440×900) a mobilu (390×844):
//  - hero: jeden h1 nad ohybem, podnadpis, primární CTA nad ohybem, CTA opakované aspoň 3×, čitelný velký náhled produktu,
//  - typografie: písmo těla ≥ 16 px, délka řádku, max. 2 rodiny písma, žádná výchozí „AI“ písma, žádný gradientní text, žádné emoji v rozhraní,
//  - rozvržení: nejvýš N mřížek stejných karet, žádný obrázek použitý dvakrát, ostré (ne zvětšené) obrázky, alt u obrázků, max. 1 stockový snímek,
//  - přístupnost: kontrast textu ≥ 4,5:1 (velký 3:1), tap targety ≥ 44 px na mobilu,
//  - výkon: LCP, CLS, chyby v konzoli a 4xx/5xx,
//  - struktura: ceny, záruka, FAQ, jak to funguje, důkazy/ukázka, patička, h-hierarchie, metadata (title, description, og, lang),
//  - texty: zakázané fráze typické pro text psaný AI.
// Prahy jsou výchozí a přepíše je oddíl „## Automaticky ověřitelné prahy“ v plan/postupy/pristavaci-web.md (řádky `klíč: hodnota`).
// ERR = web se nesmí spustit, VAROVÁNÍ = posoudit v nezávislé revizi vzhledu. Kód 1 při jakékoli ERR.
// Pozor: nejde o náhradu nezávislé revize očima (`plan/design-<projekt>.md`, „## Revize vzhledu“), ta měří estetiku, tento skript jen měřitelné znaky.
import { mkdirSync, readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(new URL("../web/package.json", import.meta.url));
const { chromium } = require("playwright-core");
const [url, out = "/tmp/landing-kontrola"] = process.argv.slice(2);
if (!url) throw new Error("Použití: node tools/landing-kontrola.mjs <URL> [složka]");
mkdirSync(out, { recursive: true });

const T = {
  "kontrast-text-min": 4.5, "kontrast-velky-text-min": 3, "pismo-telo-min-px": 16, "delka-radku-max-znaku": 80,
  "tap-target-min-px": 44, "lcp-max-s": 2.5, "cls-max": 0.1, "cta-opakovani-min": 3, "max-mrizek-stejnych-karet": 1,
  "pocet-rodin-pisem-max": 2, "pocet-velikosti-pisma-max": 8, "cta-vyska-min-px": 48, "h1-slov-min": 4, "ai-znaky-celkem-max": 6,
  "font-family-varovani": "Inter, Roboto, Arial, Montserrat, Open Sans, Lato, Poppins, DM Sans, Fraunces, system-ui", "nahled-produktu-min-px-pc": 420, "nahled-produktu-min-px-mobil": 280, "h1-slov-max": 12, "pomer-h1-k-telu-pc-min": 2.5, "css-promenne-min": 6,
  "max-stockovych-fotek": 1, "title-min": 25, "title-max": 65, "description-min": 70, "description-max": 165,
  "pisma-zakazana": "Space Grotesk, Poppins",
  "pisma-podezrela": "Inter, Roboto, Arial, Montserrat, Open Sans, system-ui",
  "text-zakazane-fraze": "posuňte na vyšší úroveň; na vyšší úroveň; bez kompromisů; revoluční; v dnešním rychlém světě; bezproblémově; odemkněte; plný potenciál; řešení na míru; nejmodernější technologie; ať už jste; ať už hledáte; objevte sílu; vše, co potřebujete; snadno a rychle; hravě",
};
const norma = "plan/postupy/pristavaci-web.md";
const normaPath = new URL(`../${norma}`, import.meta.url);
if (existsSync(normaPath)) {
  const txt = readFileSync(normaPath, "utf-8");
  const sec = txt.split("## Automaticky ověřitelné prahy")[1];
  if (sec) for (const line of sec.split("\n")) {
    const m = line.match(/^\s*[-*]?\s*`?([\w-]+)`?\s*:\s*(.+?)\s*$/);
    if (m && m[1] in T) T[m[1]] = typeof T[m[1]] === "number" ? Number(m[2].replace(",", ".")) || T[m[1]] : m[2];
  }
}

const results = [];
const err = (id, msg) => results.push(["ERR", id, msg]);
const warn = (id, msg) => results.push(["VAROVÁNÍ", id, msg]);

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const [name, w, h, mobile] of [["pc", 1440, 900, false], ["mobil", 390, 844, true]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const consoleErrors = [], bad = [];
  page.on("console", (m) => m.type() === "error" && consoleErrors.push(m.text()));
  page.on("response", (r) => r.status() >= 400 && bad.push(`${r.status()} ${r.url()}`));
  await page.addInitScript(() => {
    window.__lcp = 0; window.__cls = 0;
    new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: "largest-contentful-paint", buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: "layout-shift", buffered: true });
  });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: `${out}/${name}-nad-ohybem.png` });
  await page.screenshot({ path: `${out}/${name}-cela.png`, fullPage: true });
  const r = await page.evaluate((cfg) => {
    const { T, mobile } = cfg;
    const out = { err: [], warn: [] };
    const E = (id, m) => out.err.push([id, m]);
    const W = (id, m) => out.warn.push([id, m]);
    const vis = (el) => { const s = getComputedStyle(el), b = el.getBoundingClientRect(); return s.display !== "none" && s.visibility !== "hidden" && b.width > 0 && b.height > 0; };
    const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] ?? 1 }; };
    const bgOf = (el) => { // první neprůhledné pozadí směrem nahoru; null = obrázek/gradient (nelze změřit)
      let blend = { r: 255, g: 255, b: 255 };
      const stack = [];
      for (let e = el; e; e = e.parentElement) {
        const s = getComputedStyle(e);
        if (s.backgroundImage && s.backgroundImage !== "none") return null;
        const c = parse(s.backgroundColor);
        if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; }
      }
      for (const c of stack.reverse()) blend = { r: c.r * c.a + blend.r * (1 - c.a), g: c.g * c.a + blend.g * (1 - c.a), b: c.b * c.a + blend.b * (1 - c.a) };
      return blend;
    };
    const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const fold = innerHeight;

    // hero
    const h1s = [...document.querySelectorAll("h1")].filter(vis);
    if (h1s.length !== 1) E("hero-h1", `na stránce je ${h1s.length} viditelných h1 (má být 1)`);
    const h1 = h1s[0];
    if (h1) {
      const words = h1.innerText.trim().split(/\s+/).length;
      if (h1.getBoundingClientRect().top > fold * 0.75) E("hero-h1", "h1 není v horní části první obrazovky");
      if (words > T["h1-slov-max"] || words < T["h1-slov-min"]) W("hero-h1", `h1 má ${words} slov (${T["h1-slov-min"]} až ${T["h1-slov-max"]})`);
      const sub = [...document.querySelectorAll("p, h2")].find((e) => vis(e) && h1.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING && e.getBoundingClientRect().top < fold);
      if (!sub) E("hero-podnadpis", "pod h1 chybí podnadpis nad ohybem");
    }
    const ctas = [...document.querySelectorAll("a, button")].filter((e) => vis(e) && !e.closest("nav") && /^(button|a)$/i.test(e.tagName) && e.innerText.trim().length > 1);
    const ctaFold = ctas.filter((e) => e.getBoundingClientRect().top < fold - 20 && e.getBoundingClientRect().height >= 36 && /(koupit|objednat|stáhnout|začít|vyzkoušet|chci|získat|poslat|nezávazn|ukázk|naplánovat|rezervovat|vstupenk|zjistit|poptat|napsat|kontakt|přidat|zaregistr|prohlédnout)/i.test(e.innerText));
    if (!ctaFold.length) E("hero-cta", "nad ohybem není viditelné tlačítko s výzvou k akci (koupit, objednat, stáhnout…)");
    else {
      const main = ctaFold[0], href = main.getAttribute("href");
      const same = ctas.filter((e) => e.getAttribute("href") === href && e.getAttribute("href")).length;
      if (same < T["cta-opakovani-min"]) E("cta-opakovani", `primární CTA „${main.innerText.trim()}“ (${href}) je na stránce ${same}× (min. ${T["cta-opakovani-min"]}×: hero, střed, konec)`);
      const bg = bgOf(main), fg = parse(getComputedStyle(main).color);
      if (bg && fg) { const cr = ratio(fg, bg); if (cr < T["kontrast-text-min"]) E("cta-kontrast", `kontrast CTA ${cr.toFixed(2)}:1 (min. ${T["kontrast-text-min"]})`); }
    }
    const bgVisual = [...document.querySelectorAll("div, section, header")].some((e) => { const b = e.getBoundingClientRect(); return vis(e) && b.top < fold && b.width * Math.min(b.height, fold) > innerWidth * fold * 0.3 && /url\(/.test(getComputedStyle(e).backgroundImage); });
    const visuals = [...document.querySelectorAll("img, svg, picture, canvas, video")].filter((e) => vis(e) && e.getBoundingClientRect().top < fold).concat(bgVisual ? [document.body] : []);
    const minW = mobile ? T["nahled-produktu-min-px-mobil"] : T["nahled-produktu-min-px-pc"];
    const prodImgs = [...document.querySelectorAll("img")].filter((e) => vis(e) && /(náhled|ukázk|produkt|sada|plánovač|list|tabulk|web|stránk|screenshot)/i.test(`${e.alt} ${e.src}`));
    if (!prodImgs.length) E("nahled-produktu", "na stránce není obrázek s náhledem produktu (alt/název souboru: náhled, ukázka, produkt…)");
    else if (!prodImgs.some((e) => e.getBoundingClientRect().width >= minW)) E("nahled-produktu", `náhled produktu je užší než ${minW} px (nečitelný drobný mockup)`);
    if (!visuals.length) W("hero-vizual", "nad ohybem není žádný vizuál");

    // typografie
    const sizes = [...document.querySelectorAll("p, li")].filter((e) => vis(e) && e.innerText.trim().length > 60).map((e) => parseFloat(getComputedStyle(e).fontSize)).sort((a, b) => a - b);
    const medianSize = sizes.length ? sizes[Math.floor(sizes.length / 2)] : 0;
    if (medianSize && medianSize < T["pismo-telo-min-px"]) E("pismo-telo", `mediánové písmo odstavců ${medianSize}px (min. ${T["pismo-telo-min-px"]} px)`);
    const textEls = [...document.querySelectorAll("h1,h2,h3,h4,p,li,a,button,span,label,summary,dt,dd")].filter((e) => vis(e) && !e.closest("[aria-hidden=true]") && parse(getComputedStyle(e).color)?.a > 0.3 && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));
    const fams = new Set(), banned = T["pisma-zakazana"].split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);
    const bannedUsed = new Set();
    for (const e of textEls) {
      const fam = getComputedStyle(e).fontFamily.split(",")[0].replace(/["']/g, "").trim();
      fams.add(fam);
      if (banned.includes(fam.toLowerCase())) bannedUsed.add(fam);
    }
    const famList = [...fams].filter((f) => !/^(__|ui-|-apple|BlinkMac|Segoe)/.test(f) || true);
    // next/font generuje jména jako „__Inter_abc“ → vyčistit
    const clean = [...new Set(famList.map((f) => f.replace(/^__/, "").replace(/_[a-z0-9]{6,}$/i, "").replace(/_/g, " ")))];
    if (clean.length > T["pocet-rodin-pisem-max"]) W("pisma-pocet", `${clean.length} rodin písma (${clean.join(", ")}), max. ${T["pocet-rodin-pisem-max"]}`);
    const sizesUsed = new Set(textEls.map((e) => Math.round(parseFloat(getComputedStyle(e).fontSize))));
    if (sizesUsed.size > T["pocet-velikosti-pisma-max"]) W("pisma-velikosti", `${sizesUsed.size} různých velikostí písma (${[...sizesUsed].sort((a, b) => a - b).join(", ")}), max. ${T["pocet-velikosti-pisma-max"]}: chybí typografická škála`);
    const suspicious = (T["font-family-varovani"] + "," + T["pisma-podezrela"]).split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);
    for (const f of clean) {
      if (banned.includes(f.toLowerCase())) E("pisma-vychozi", `výchozí „AI“ písmo ${f}: zvolit písmo odvozené z identity produktu`);
      else if (suspicious.includes(f.toLowerCase())) W("pisma-vychozi", `velmi rozšířené výchozí písmo ${f}: posoudit v revizi, zda má web vlastní typografickou identitu`);
    }
    const lines = [...document.querySelectorAll("p")].filter((p) => vis(p) && p.innerText.trim().length > 120).map((p) => {
      const st = getComputedStyle(p), lh = parseFloat(st.lineHeight) || parseFloat(st.fontSize) * 1.4;
      const n = Math.max(1, Math.round(p.getBoundingClientRect().height / lh));
      return n >= 2 ? p.innerText.trim().length / n : 0;
    });
    if (lines.length && Math.max(...lines) > T["delka-radku-max-znaku"] * 1.1) W("delka-radku", `řádek odstavce až ~${Math.round(Math.max(...lines))} znaků (max. ${T["delka-radku-max-znaku"]})`);
    for (const e of document.querySelectorAll("*")) {
      const s = getComputedStyle(e);
      if ((s.webkitBackgroundClip === "text" || s.backgroundClip === "text") && /gradient/.test(s.backgroundImage)) { E("gradient-text", `gradientní text: ${e.tagName} „${e.innerText.slice(0, 30)}“`); break; }
    }
    const emoji = (document.body.innerText.match(/\p{Emoji_Presentation}|\p{Extended_Pictographic}\uFE0F/gu) || []);
    if (emoji.length) E("emoji", `emoji v rozhraní: ${[...new Set(emoji)].join(" ")} (nahradit vlastní ikonou nebo grafikou)`);

    // měřítko kvality zoo-hero (plan/postupy/mericko-kvality-zoo-hero.md): hierarchie, pohyb, systém
    if (h1 && medianSize && parseFloat(getComputedStyle(h1).fontSize) / medianSize < T["pomer-h1-k-telu-pc-min"] * (mobile ? 0.7 : 1)) W("hierarchie", `h1 je jen ${(parseFloat(getComputedStyle(h1).fontSize) / medianSize).toFixed(1)}× větší než text těla (zoo-hero ≈ 8×, min. ${T["pomer-h1-k-telu-pc-min"]}×)`);
    if (!mobile) {
      let animated = document.getAnimations().length > 0, reduced = false, tokens = 0, transitions = 0;
      for (const e of document.querySelectorAll("a, button")) { if (parseFloat(getComputedStyle(e).transitionDuration) > 0) transitions++; }
      for (const sh of document.styleSheets) { try { for (const rule of sh.cssRules) {
        if (rule.media && /prefers-reduced-motion/.test(rule.media.mediaText)) reduced = true;
        if (rule.selectorText === ":root") tokens += [...rule.style].filter((x) => x.startsWith("--")).length;
      } } catch {} }
      for (const e of document.querySelectorAll("*")) { if (getComputedStyle(e).animationName !== "none") { animated = true; break; } }
      if (animated && !reduced) E("pohyb-reduced-motion", "stránka má animace, ale žádné pravidlo @media (prefers-reduced-motion)");
      if (tokens < T["css-promenne-min"]) W("barevny-system", `jen ${tokens} CSS proměnných v :root (min. ${T["css-promenne-min"]}): barvy a mezery mají být systém, ne roztroušené hodnoty`);
      if (!transitions) W("mikrodetaily", "žádné plynulé přechody u tlačítek a odkazů (hover, fokus)");
    }

    // rozvržení
    const grids = [];
    for (const e of document.querySelectorAll("section, div, ul, ol")) {
      const kids = [...e.children].filter(vis);
      if (kids.length < 3 || kids.length > 8) continue;
      const bs = kids.map((k) => k.getBoundingClientRect());
      const rowTop = bs[0].top, sameRow = bs.filter((b) => Math.abs(b.top - rowTop) < 4);
      const similar = sameRow.length >= 3 && sameRow.every((b) => Math.abs(b.width - sameRow[0].width) < 3);
      const rich = kids.every((k) => k.querySelector("h2,h3,h4,strong") && k.innerText.trim().length > 20 && getComputedStyle(k).display !== "inline");
      if (similar && rich && !grids.some((g) => g.contains(e) || e.contains(g))) grids.push(e);
    }
    if (!mobile && grids.length > T["max-mrizek-stejnych-karet"]) E("mrizka-karet", `${grids.length} mřížek 3+ stejných karet (max. ${T["max-mrizek-stejnych-karet"]}): typický vzhled generovaný AI, použít různé rozvržení sekcí`);
    const shadows = {};
    for (const e of document.querySelectorAll("*")) { const s = getComputedStyle(e); if (s.boxShadow !== "none" && vis(e)) { const k = `${s.boxShadow}|${s.borderRadius}`; shadows[k] = (shadows[k] || 0) + 1; } }
    const topShadow = Math.max(0, ...Object.values(shadows));
    if (topShadow >= 8) W("stejne-stiny", `${topShadow}× stejný stín a zaoblení (jednotné „karty“ všude)`);
    const imgs = [...document.querySelectorAll("img")].filter(vis);
    const seen = {}; for (const i of imgs) { const raw = i.currentSrc || i.src, u = raw.match(/[?&]url=([^&]+)/), k = u ? decodeURIComponent(u[1]) : raw.split("?")[0]; seen[k] = (seen[k] || 0) + 1; }
    for (const [k, n] of Object.entries(seen)) if (n > 1) E("obrazek-dvakrat", `stejný obrázek ${n}× na stránce: ${k.slice(-60)}`);
    for (const i of imgs) {
      if (!i.hasAttribute("alt")) E("alt", `obrázek bez alt: ${(i.currentSrc || i.src).slice(-60)}`);
      const rw = i.getBoundingClientRect().width;
      if (i.naturalWidth && i.naturalWidth < rw * 0.95) W("obrazek-ostrost", `obrázek ${i.naturalWidth}px natažený na ${Math.round(rw)}px: ${(i.currentSrc || i.src).slice(-50)}`);
    }
    const stock = imgs.filter((i) => /unsplash|pexels|pixabay|shutterstock|istock/i.test(i.currentSrc + i.src + i.alt)).length + (/Foto:.*Unsplash/i.test(document.body.innerText) ? 0 : 0);
    const credits = (document.body.innerText.match(/Unsplash|Pexels|Pixabay/gi) || []).length;
    if (Math.max(stock, credits) > T["max-stockovych-fotek"]) E("stockove-fotky", `${Math.max(stock, credits)} stockových fotek (max. ${T["max-stockovych-fotek"]}): použít vlastní grafiku a skutečný produkt`);

    // znaky AI vzhledu (plan/postupy/pristavaci-web.md „Znaky webů navržených AI“): jen počítá a hlásí, rozhoduje revize K9
    const tells = [];
    const allEls = [...document.querySelectorAll("body *")].filter(vis);
    if (h1) {
      const prev = [...document.querySelectorAll("body *")].filter((e) => vis(e) && e !== h1 && !h1.contains(e) && (h1.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING) && e.getBoundingClientRect().bottom <= h1.getBoundingClientRect().top + 2 && e.getBoundingClientRect().bottom > h1.getBoundingClientRect().top - 90 && (e.innerText || "").trim().length > 3 && (e.innerText || "").trim().length < 60 && !e.querySelector("*") && getComputedStyle(e).textTransform === "uppercase");
      if (prev.length) tells.push("štítek VELKÝMI nad h1 (eyebrow)");
      if ([...h1.querySelectorAll("*")].some((e) => getComputedStyle(e).fontStyle === "italic" && /serif|fraunces|playfair|georgia|times/i.test(getComputedStyle(e).fontFamily) && !/sans/i.test(getComputedStyle(e).fontFamily.split(",").pop()))) tells.push("kurzivní patkový akcent v h1");
    }
    if (allEls.some((e) => /blur\(/.test(getComputedStyle(e).backdropFilter || getComputedStyle(e).webkitBackdropFilter || ""))) tells.push("glassmorphism (backdrop-filter blur)");
    if (allEls.some((e) => { const m = getComputedStyle(e).boxShadow.match(/(\d+)px\s+(\d+)px\s+(\d+)px/g); return m && m.some((x) => +x.split(/px\s+/)[2].replace("px", "") >= 24 && /rgba?\((?!0, 0, 0)/.test(getComputedStyle(e).boxShadow)); })) tells.push("barevná záře (glow) ve stínu");
    const uppers = allEls.filter((e) => getComputedStyle(e).textTransform === "uppercase" && (e.innerText || "").trim().length > 2 && !e.querySelector("*")).length;
    if (uppers > 2) tells.push(`${uppers} prvků psaných VELKÝMI`);
    const numbered = allEls.filter((e) => /^\s*0?[1-9]\s*$/.test(e.childNodes.length === 1 && e.firstChild.nodeType === 3 ? e.textContent : "x")).length;
    if (numbered >= 3 && numbered <= 8) tells.push(`očíslované kroky 1-2-3 (${numbered}×)`);
    const cta0 = ctaFold[0], cbg = cta0 && parse(getComputedStyle(cta0).backgroundColor);
    if (cbg && cbg.a > 0.5) { const mx = Math.max(cbg.r, cbg.g, cbg.b), mn = Math.min(cbg.r, cbg.g, cbg.b), d = mx - mn; if (d > 0) { let hh = mx === cbg.r ? ((cbg.g - cbg.b) / d) % 6 : mx === cbg.g ? (cbg.b - cbg.r) / d + 2 : (cbg.r - cbg.g) / d + 4; hh = (hh * 60 + 360) % 360; const sat = d / (255 - Math.abs(mx + mn - 255)) * 100; if (hh >= 240 && hh <= 295 && sat >= 35) tells.push(`fialové/indigo CTA (hue ${Math.round(hh)}°)`); } }
    const cream = parse(getComputedStyle(document.body).backgroundColor);
    if (cream && cream.a > 0 && cream.r > 235 && cream.g > 225 && cream.b > 200 && cream.r - cream.b > 6 && cream.r - cream.b < 40) tells.push("krémové pozadí");
    if (grids.length) tells.push(`${grids.length}× mřížka stejných karet`);
    if (tells.length) {
      const msg = `${tells.length} znaků AI vzhledu: ${tells.join("; ")} (jednotlivě jen varování, posoudit v revizi K9)`;
      if (tells.length > T["ai-znaky-celkem-max"]) E("znaky-ai", msg); else if (!mobile) W("znaky-ai", msg);
    }
    // focus a výška CTA
    if (!mobile) {
      let focusRule = false;
      for (const sh of document.styleSheets) { try { for (const rule of sh.cssRules) if (/:focus-visible/.test(rule.cssText)) focusRule = true; } catch {} }
      if (!focusRule) W("focus-viditelny", "žádné pravidlo :focus-visible (klávesnicová přístupnost)");
    }
    if (ctaFold.length && ctaFold[0].getBoundingClientRect().height < T["cta-vyska-min-px"]) W("cta-vyska", `primární CTA vysoké ${Math.round(ctaFold[0].getBoundingClientRect().height)} px (min. ${T["cta-vyska-min-px"]})`);

    // přístupnost
    const lowc = new Set();
    for (const e of textEls.slice(0, 400)) {
      const fg = parse(getComputedStyle(e).color), bg = bgOf(e); if (!fg || !bg) continue;
      const size = parseFloat(getComputedStyle(e).fontSize), bold = parseInt(getComputedStyle(e).fontWeight) >= 700;
      const need = size >= 24 || (size >= 18.66 && bold) ? T["kontrast-velky-text-min"] : T["kontrast-text-min"];
      const cr = ratio(fg, bg); if (cr < need) lowc.add(`${(e.innerText || "").trim().slice(0, 25)} (${cr.toFixed(2)}:1)`);
    }
    if (lowc.size) E("kontrast", `nízký kontrast: ${[...lowc].slice(0, 5).join("; ")}${lowc.size > 5 ? ` … (+${lowc.size - 5})` : ""}`);
    if (mobile) {
      const small = [...document.querySelectorAll("button, a.btn, a[class*=btn], a[class*=button], input, select")].filter((e) => vis(e) && Math.min(e.getBoundingClientRect().height, 99) < T["tap-target-min-px"]);
      if (small.length) E("tap-target", `${small.length} ovládacích prvků nižších než ${T["tap-target-min-px"]} px (např. „${(small[0].innerText || small[0].value || "").trim().slice(0, 20)}“)`);
      window.scrollTo(200, 0); if (window.scrollX > 0) E("preteka", "stránka se dá posunout do strany (vodorovný posuvník)"); window.scrollTo(0, 0);
    }

    // struktura (jen jednou, na PC)
    if (!mobile) {
      const txt = document.body.innerText.toLowerCase();
      const need = [
        ["cena", /\d[\d\s ]*\s?kč/, "cena v Kč"], ["zaruka", /záruk|vrácení peněz|vrátíme|garanc/, "záruka nebo vrácení peněz"],
        ["faq", /časté otázky|často kladené|otázky a odpovědi|faq|otázky/, "FAQ / otázky"], ["jak-funguje", /jak (to )?funguje|jak to probíhá|postup|jak (to )?bude/, "jak to funguje"],
      ];
      for (const [id, re, label] of need) if (!re.test(txt)) E(`struktura-${id}`, `chybí ${label}`);
      if (!/(recenz|reference|hodnocen|zkušenost|spokojen|ukázk|vzorov|náhled|ověřen|zdarma)/.test(txt)) W("struktura-duvod-k-duvere", "chybí důkaz důvěry (reference, recenze, ukázka zdarma, čísla). Vymyšlené reference nepoužívat");
      if (!document.querySelector("footer")) E("struktura-paticka", "chybí <footer>");
      const hs = [...document.querySelectorAll("h1,h2,h3,h4")].filter(vis).map((h) => +h.tagName[1]);
      for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i - 1] > 1) { E("h-hierarchie", `přeskočená úroveň nadpisu (h${hs[i - 1]} → h${hs[i]})`); break; }
      const bad = T["text-zakazane-fraze"].split(T["text-zakazane-fraze"].includes(";") ? ";" : ",").map((x) => x.trim().toLowerCase()).filter(Boolean).filter((f) => txt.includes(f));
      if (bad.length) E("fraze-ai", `fráze typické pro text od AI: ${bad.join("; ")}`);
      const dash = (document.body.innerText.match(/ — /g) || []).length;
      if (dash > 2) W("fraze-ai", `${dash}× dlouhá pomlčka „ — “ (česky pomlčka „ – “ s mezerami, nadužití je znak AI textu)`);
      const meta = (n) => document.querySelector(`meta[name="${n}"], meta[property="${n}"]`)?.content ?? "";
      const title = document.title, desc = meta("description");
      if (title.length < T["title-min"] || title.length > T["title-max"]) W("meta-title", `title má ${title.length} znaků (${T["title-min"]}–${T["title-max"]})`);
      if (desc.length < T["description-min"] || desc.length > T["description-max"]) W("meta-description", `description má ${desc.length} znaků (${T["description-min"]}–${T["description-max"]})`);
      if (!meta("og:title") || !meta("og:image")) E("meta-og", "chybí og:title nebo og:image");
      if (!document.documentElement.lang.startsWith("cs")) E("meta-lang", "html lang není cs");
      if (!document.querySelector('meta[name="viewport"]')) E("meta-viewport", "chybí meta viewport");
    }
    return out;
  }, { T, mobile });
  const lcp = await page.evaluate(() => window.__lcp / 1000), cls = await page.evaluate(() => window.__cls);
  if (lcp > T["lcp-max-s"]) err(`${name}:lcp`, `LCP ${lcp.toFixed(2)} s (max. ${T["lcp-max-s"]} s)`);
  if (cls > T["cls-max"]) err(`${name}:cls`, `CLS ${cls.toFixed(3)} (max. ${T["cls-max"]})`);
  if (consoleErrors.length) err(`${name}:konzole`, consoleErrors.slice(0, 3).join(" | "));
  if (bad.length) err(`${name}:http`, bad.slice(0, 3).join(" | "));
  for (const [id, m] of r.err) err(`${name}:${id}`, m);
  for (const [id, m] of r.warn) warn(`${name}:${id}`, m);
  await page.close();
}
await browser.close();

const errs = results.filter((x) => x[0] === "ERR");
for (const [lvl, id, msg] of results) console.log(`${lvl.padEnd(9)} ${id.padEnd(28)} ${msg}`);
console.log(`\nlanding-kontrola: ${errs.length ? `${errs.length} ERR` : "OK"} (${results.length - errs.length} varování), screenshoty ${out}`);
process.exit(errs.length ? 1 : 0);
