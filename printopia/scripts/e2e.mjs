// E2E test testovací stránky: build musí proběhnout předem (npm run test:e2e).
import { spawn, spawnSync } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";

const PORT = 3200;
const BASE = `http://localhost:${PORT}`;
const store = mkdtempSync(path.join(tmpdir(), "printopia-"));

// Falešné Fio API a Resend pro nákup
const MOCK = 3209;
const payments = [];
const emails = [];
const mock = http.createServer((req, res) => {
  if (req.url.startsWith("/fio/periods/")) {
    const transaction = payments.map((p, i) => ({
      column22: { value: p.id }, column0: { value: p.date }, column1: { value: p.amount },
      column14: { value: "CZK" }, column5: p.vs ? { value: p.vs } : null,
    }));
    res.setHeader("Content-Type", "application/json");
    return res.end(JSON.stringify({ accountStatement: { transactionList: { transaction } } }));
  }
  if (req.url === "/emails" && req.method === "POST") {
    let body = "";
    req.on("data", (c) => (body += c));
    return req.on("end", () => { emails.push(JSON.parse(body)); res.end("{}"); });
  }
  res.statusCode = 404;
  res.end();
});
await new Promise((r) => mock.listen(MOCK, r));

const app = spawn("npx", ["next", "start", "-p", String(PORT)], {
  env: {
    ...process.env, LOCAL_STORE_DIR: store, BLOB_READ_WRITE_TOKEN: "", VERCEL: "", STATS_KEY: "tajne",
    SALES_OPEN: "1", FIO_TOKEN: "test", FIO_API_BASE: `http://localhost:${MOCK}/fio`, RESEND_API_KEY: "test",
    RESEND_API_URL: `http://localhost:${MOCK}/emails`, CRON_SECRET: "cron-tajne", SITE_URL: `http://localhost:${PORT}`,
  },
  stdio: ["ignore", "pipe", "pipe"],
  detached: true,
});
let logs = "";
app.stdout.on("data", (d) => (logs += d));
app.stderr.on("data", (d) => (logs += d));

let failed = 0;
const check = (ok, name) => {
  console.log(`${ok ? "✓" : "✗"} ${name}`);
  if (!ok) failed++;
};
const UA = { "User-Agent": "Mozilla/5.0 (e2e) Safari" };
const get = (p) => fetch(`${BASE}${p}`, { headers: UA });
const post = (body) => fetch(`${BASE}/api/lead`, { method: "POST", headers: { "Content-Type": "application/json", ...UA }, body: JSON.stringify(body) });

try {
  for (let i = 0; i < 60; i++) {
    if (await fetch(BASE).then(() => true, () => false)) break;
    await new Promise((r) => setTimeout(r, 500));
  }
  const home = await (await get("/?utm_source=sklik&utm_term=123456&utm_content=ad789")).text();
  check(home.includes("Procvičte s dítětem přesně to"), "úvodní stránka");
  const flat = home.replaceAll("<!-- -->", "");
  check(["nahled-postup.webp", "Koupit sadu za 349", "8 úloh zdarma", "vrátíme peníze", "Kolik stojí příprava", "Časté otázky", "Printopia provozuje", "IČO", "dní do přijímaček"].every((t) => flat.includes(t)),
    "prodejní stránka má povinné prvky (náhled, cena v CTA, ukázka, záruka, srovnání, FAQ, provozovatel v patičce, odpočet)");
  check(flat.includes('name="google-site-verification"'), "ověření Search Console je v hlavičce");
  check(home.includes('class="fr"'), "zlomky nad sebou v ukázce");
  check(home.includes("/koupit?src=sklik"), "zdroj návštěvy se předává do Koupit");
  const pdf = await fetch(`${BASE}/ukazka-zlomky.pdf`);
  check(pdf.ok && pdf.headers.get("content-type")?.includes("pdf"), "ukázka PDF ke stažení");
  const buy = (await (await get("/koupit?src=sklik")).text()).replaceAll("<!-- -->", "");
  check(buy.includes("Objednat s povinností platby") && buy.includes("349 Kč") && buy.includes("obchodními podmínkami"), "stránka Koupit je objednávka");
  check((await fetch(`${BASE}/ochrana-osobnich-udaju`)).ok, "ochrana osobních údajů");
  const zl = await (await fetch(`${BASE}/zlomky-prijimacky`)).text();
  check(zl.includes("Zlomky na přijímačky") && zl.includes("240 stran"), "stránka Zlomky s příklady a řešením");
  const sm = await (await fetch(`${BASE}/sitemap.xml`)).text();
  check(["/jak-se-pripravit-na-prijimacky", "/zlomky-prijimacky", "/procenta-prijimacky", "/rovnice-prijimacky", "/slovni-ulohy-prijimacky"].every((u) => sm.includes(u)), "sitemap obsahuje všechna témata");
  const pr = await (await fetch(`${BASE}/procenta-prijimacky`)).text();
  check(pr.includes("Procenta na přijímačky") && pr.includes("21 218 Kč"), "stránka Procenta");
  const ro = await (await fetch(`${BASE}/rovnice-prijimacky`)).text();
  check(ro.includes("Rovnice na přijímačky") && ro.includes("v 9:30, 27 km od Brna"), "stránka Rovnice");
  const sl = await (await fetch(`${BASE}/slovni-ulohy-prijimacky`)).text();
  check(sl.includes("Slovní úlohy na přijímačky") && sl.includes("21 slepic"), "stránka Slovní úlohy");
  check((await (await fetch(`${BASE}/jak-se-pripravit-na-prijimacky`)).text()).includes("plán do dubna"), "stránka Jak se připravit");
  check((await fetch(`${BASE}/neexistujici-prijimacky`)).status === 404, "neznámé téma = 404");
  check((await fetch(`${BASE}/og.png`)).ok, "náhled pro sdílení");
  check((await fetch(`${BASE}/neexistuje`)).status === 404, "404");

  check((await post({ email: "spatny", consent: true, role: "rodic", source: "ukazka" })).status === 400, "odmítne neplatný e-mail");
  check((await post({ email: "a@b.cz", consent: false, role: "rodic", source: "ukazka" })).status === 400, "odmítne bez souhlasu");
  check((await post({ email: "a@b.cz", consent: true, source: "ukazka" })).status === 400, "odmítne bez role");
  check((await post({ email: "a@b.cz", consent: true, source: "ukazka", role: "dite" })).status === 400, "odmítne neznámou roli");
  check(home.includes("je mi aspoň 15 let") && !home.includes("rodičům</a>"), "formulář se ptá na roli, žádná výzva dětem ke koupi");
  const r1 = await post({ email: "Rodic@Example.cz", consent: true, role: "rodic", source: "ukazka", src: "sklik" });
  const j1 = await r1.json();
  check(r1.ok && j1.ok === true && !("download" in j1), "tipy e-mailem: jen přihlášení, stažení ukázky je zvlášť");
  check(home.includes('href="/ukazka-zlomky.pdf"') && (await fetch(`${BASE}/ukazka-zlomky.pdf`)).ok, "ukázka PDF se stáhne bez e-mailu");
  const r2 = await post({ email: "rodic@example.cz", consent: true, role: "rodic", source: "ukazka", src: "sklik" });
  check(r2.ok && (await post({ email: "a@b.cz", consent: true, role: "rodic", source: "koupit" })).status === 400, "opakované přihlášení; neznámý zdroj se odmítne");
  const hp = await post({ email: "bot@example.cz", consent: true, source: "ukazka", website: "x" });
  check(hp.ok, "honeypot odpoví ok");
  const files = readdirSync(path.join(store, "leads"));
  check(files.length === 1, "jeden e-mail = jeden záznam (bot se neuložil)");
  const lead = JSON.parse(readFileSync(path.join(store, "leads", files[0]), "utf8"));
  check(lead.email === "rodic@example.cz" && lead.sources.join() === "ukazka" && lead.src === "sklik" && lead.role === "rodic", "záznam má zdroje, roli i původ");
  check(logs.includes('"ev":"visit"') && logs.includes('"ev":"buy_click"') && logs.includes('"ev":"lead"'), "události v logu pro měření testu");
  await fetch(`${BASE}/`, { headers: { "User-Agent": "Googlebot/2.1" } });
  await new Promise((r) => setTimeout(r, 500));
  check((await fetch(`${BASE}/api/stats`)).status === 401, "souhrn testu je chráněný");
  // Anonymní trychtýř: dvě návštěvy (mobil a počítač), jedna dojde až k formuláři, anketa s důvodem
  const beacon = (pv, ev, extra = {}, ua = UA["User-Agent"]) => fetch(`${BASE}/api/e`, {
    method: "POST", headers: { "Content-Type": "application/json", "User-Agent": ua },
    body: JSON.stringify({ pv, ev, page: "home", src: "sklik", topic: "", ...extra }) });
  const pv1 = "11111111-1111-4111-8111-111111111111", pv2 = "22222222-2222-4222-8222-222222222222";
  for (const ev of ["view", "t10", "scroll50", "cta_buy", "form_start", "form_submit"]) await beacon(pv1, ev);
  for (const ev of ["view", "form_start"]) await beacon(pv2, ev, {}, "Mozilla/5.0 (iPhone; Mobile)");
  await beacon(pv2, "feedback", { choice: "drahe", text: "moc drahé" }, "Mozilla/5.0 (iPhone; Mobile)");
  check((await beacon("x", "view")).status === 400, "událost s neplatným ID odmítnuta");
  check((await beacon(pv1, "feedback", { choice: "nesmysl" })).status === 400, "neznámá odpověď ankety odmítnuta");
  check((await beacon(pv1, "view", {}, "Googlebot/2.1")).status === 204, "robot se tiše ignoruje");
  const st = await (await fetch(`${BASE}/api/stats`, { headers: { "x-stats-key": "tajne" } })).json();
  check(st.sklik.byKeyword["123456"] === 1 && st.sklik.byAd["ad789"] === 1, "souhrn: návštěvy ze Skliku podle klíčového slova a reklamy (utm_term, utm_content)");
  check(st.server.visits.sklik === 1 && st.server.buyClicks.sklik === 1 && st.server.leads === 1, "souhrn: serverové návštěvy, klik na Koupit a lead ze Skliku (robot a opakovaný lead nezapočten)");
  check(st.server.leadsByRole.rodic === 1, "souhrn: role kupujícího");
  const h = st.funnel.byPage.home;
  check(h.view === 2 && h.form_start === 2 && h.form_submit === 1 && h.cta_buy === 1, "trychtýř: kroky se počítají za návštěvy");
  check(st.rates.formCompletion === 50 && st.funnel.byDevice["home:mobil"].view === 1, "trychtýř: dokončení formuláře a rozdělení podle zařízení");
  check(st.feedback["Je to na mě drahé"] === 1 && st.feedbackTexts[0] === "moc drahé", "anketa: důvod i text");
  check(st.findings[0].startsWith("Málo dat"), "závěry: při málo datech to řekne");
  const home2 = await (await get("/")).text();
  check(home2.includes("zatím drží od objednání") && home2.includes('data-track="cta_buy"'), "úvodní stránka má anketu a měřená tlačítka");
  // Nákup: objednávka → QR → platba (falešné Fio) → cron → e-mail → stažení → doklad
  const cron = (auth = "Bearer cron-tajne") => fetch(`${BASE}/api/cron/fio`, { headers: { authorization: auth } });
  const today = new Date().toISOString().slice(0, 10) + "+0200";
  const order = async (body) => fetch(`${BASE}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json", ...UA }, body: JSON.stringify(body) });
  check((await order({ email: "rodic@example.cz", name: "Jana Nová", terms: false })).status === 400, "objednávka bez souhlasu s podmínkami neprojde");
  const created = await (await order({ email: "Rodic@Example.cz", name: "Jana Nová", terms: true, src: "sklik" })).json();
  const oid = created.id;
  const opage = await (await get(`/objednavka/${oid}`)).text();
  const vs = /Variabilní symbol<\/td><td>(\d+)</.exec(opage)?.[1] ?? "";
  check(/^8\d{9}$/.test(vs) && opage.includes("<svg") && opage.includes("2202343801/2010"), `stránka objednávky: QR, účet a VS 8xxxxxxxxx (${vs})`);
  await new Promise((r) => setTimeout(r, 400));
  check(emails.some((e) => e.to === "rodic@example.cz" && e.subject.includes(vs)), "e-mail s platebními údaji odešel");
  check((await fetch(`${BASE}/stahnout/${oid}?soubor=zlomky`, { redirect: "manual" })).status === 303, "stažení před zaplacením přesměruje");
  check((await cron("Bearer spatne")).status === 401, "cron bez tajemství vrací 401");
  payments.push({ id: 5001, vs: "2610011234", amount: 349, date: today }); // platba anoberu: printopia ji nehlásí
  payments.push({ id: 5002, vs, amount: 100, date: today });
  let cr = await (await cron()).json();
  check(cr.underpaid.includes(vs) && cr.paid.length === 0 && cr.orphans === 0, "nedoplatek se nespáruje, cizí platba se nehlásí");
  payments.length = 0;
  payments.push({ id: 5003, vs, amount: 349, date: today }, { id: 5004, vs: "8" + vs.slice(1, 7) + "999", amount: 349, date: today });
  cr = await (await cron()).json();
  check(cr.paid.includes(vs) && cr.orphans === 1, "platba se spárovala, platba s naším VS bez objednávky se nahlásila");
  await new Promise((r) => setTimeout(r, 400));
  const delivery = emails.find((e) => e.to === "rodic@example.cz" && e.subject.includes("sada"));
  check(Boolean(delivery?.html.includes(`/objednavka/${oid}`) && delivery?.html.includes(`Doklad o zaplacení č. ${vs}`)), "doručovací e-mail s odkazem a dokladem");
  check(emails.filter((e) => e.to === "printopia@mypixel.cz" && e.subject.includes("Zaplaceno")).length === 1, "firma dostala upozornění na platbu");
  const paidPage = (await (await get(`/objednavka/${oid}`)).text()).replaceAll("<!-- -->", "");
  check(paidPage.includes("Zaplaceno") && paidPage.includes(`/stahnout/${oid}?soubor=zlomky`), "po zaplacení stránka nabízí listy ke stažení");
  const manifest = JSON.parse(readFileSync(new URL("../src/content/sada-soubory.json", import.meta.url), "utf8"));
  check(manifest.length >= 3 && manifest[0].slug === "uvodni-test" && manifest.at(-1).slug === "plan", `sada má úvodní test, listy a plán (${manifest.length} souborů)`);
  let allPdf = true;
  for (const f of manifest) {
    const r = await fetch(`${BASE}/stahnout/${oid}?soubor=${f.slug}`);
    const buf = Buffer.from(await r.arrayBuffer());
    if (!r.ok || buf.subarray(0, 4).toString() !== "%PDF" || buf.length < 8000) { allPdf = false; console.log("  vadný soubor:", f.slug); }
  }
  check(allPdf, "všechny soubory sady se stáhnou jako PDF");
  const dl = await fetch(`${BASE}/stahnout/${oid}?soubor=zlomky`);
  check(dl.ok && dl.headers.get("content-type") === "application/pdf" && (await dl.arrayBuffer()).byteLength > 10000, "pracovní list se stáhne jako PDF");
  check((await fetch(`${BASE}/stahnout/${oid}?soubor=../../etc/passwd`, { redirect: "manual" })).status === 303, "neznámý soubor se nestáhne");
  check((await (await get(`/doklad/${oid}`)).text()).replaceAll("<!-- -->", "").includes(`Doklad o zaplacení č. ${vs}`), "doklad o zaplacení");
  check((await fetch(`${BASE}/ukazka-zlomky.pdf`)).ok && !(await fetch(`${BASE}/sada/01-zlomky.pdf`)).ok, "placené listy nejsou veřejně v public/");
  const st2 = await (await fetch(`${BASE}/api/stats`, { headers: { "x-stats-key": "tajne" } })).json();
  check(st2.orders.created.sklik === 1 && st2.orders.paid.sklik === 1 && st2.orders.revenue === 349, "souhrn: objednávky a tržby podle zdroje");
  check((await (await get("/obchodni-podminky")).text()).includes("printopia.cz"), "obchodní podmínky");
  // Přehled pro majitele: jen na chráněné adrese *.vercel.app, na veřejné doméně 404
  const asHost = (host) => new Promise((resolve) => http.get({ host: "localhost", port: PORT, path: "/prehled", headers: { host, ...UA } }, (res) => {
    let t = ""; res.on("data", (c) => (t += c)); res.on("end", () => resolve({ status: res.statusCode, text: t }));
  }));
  const [pub, internal] = [await asHost("printopia.cz"), await asHost("printopia-x-mypixelcz.vercel.app")];
  check(pub.status === 404 && internal.status === 200 && internal.text.replaceAll("<!-- -->", "").includes("Přehled Printopie"), "přehled /prehled je jen na *.vercel.app");
  const sm2 = await (await fetch(`${BASE}/sitemap.xml`)).text();
  const temata = readdirSync(new URL("../src/content/temata/", import.meta.url)).filter((f) => f.endsWith(".json"));
  check(temata.length >= 11 && temata.every((f) => sm2.includes(`/${f.replace(".json", "")}`)), `všechny tematické stránky (${temata.length}) jsou v sitemapě`);
  const tp = (await (await get("/uhly-a-trojuhelniky-prijimacky")).text()).replaceAll("<!-- -->", "");
  check(tp.includes("Úhly a trojúhelníky na přijímačky") && tp.includes("Zobrazit postup a výsledek") && tp.includes("Kompletní sada"), "tematická stránka z obsahu sady");

  // Vizuální a textová kontrola (FAILS.md 2026-10-01 02:02 a 02:05): šířka 1340 + 80 px, mobil, překryvy, z-index, texty.
  const pages = `/,/koupit,/obchodni-podminky,/objednavka/${oid},/zlomky-prijimacky,/procenta-prijimacky,/telesa-objem-povrch-prijimacky,/konstrukcni-ulohy-prijimacky,/jak-se-pripravit-na-prijimacky,/ochrana-osobnich-udaju`;
  const viz = spawnSync("node", ["../tools/vizualni-kontrola.mjs", BASE, pages, process.env.VIZ_DIR ?? path.join(store, "viz")], { encoding: "utf8" });
  console.log(viz.stdout.trim());
  check(viz.status === 0, "vizuální a textová kontrola stránek");
} finally {
  process.kill(-app.pid);
  mock.close();
}
console.log(failed ? `\n${failed} kontrol selhalo` : "\nVšechny kontroly prošly");
process.exit(failed ? 1 : 0);
