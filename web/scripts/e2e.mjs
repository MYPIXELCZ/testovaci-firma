// End-to-end test nákupu: objednávka -> QR -> platba (falešné Fio) -> cron -> doručení -> stažení.
// Spouštění: npm run build && node scripts/e2e.mjs
// Potřebuje Chromium (CHROMIUM_PATH, výchozí /opt/pw-browsers/...). Nic neposílá ven.
import { spawn } from "node:child_process";
import { readFileSync, rmSync, writeFileSync } from "node:fs";
import http from "node:http";
import { chromium } from "playwright-core";

const APP = 3100;
const MOCK = 3200;
const SECRET = "e2e-secret";
const STORE = new URL("../.localstore-e2e/", import.meta.url).pathname;
const CHROMIUM = process.env.CHROMIUM_PATH ?? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

let failures = 0;
const check = (ok, label) => {
  console.log(`${ok ? "✓" : "✗"} ${label}`);
  if (!ok) failures++;
};

// Falešné Fio API + Resend
const payments = [];
const emails = [];
const toCustomer = () => emails.filter((e) => e.to === "nevesta@example.cz");
const toOwner = () => emails.filter((e) => e.to === "anoberu@mypixel.cz");
let fioCalls = 0;
let fioDown = false;
const mock = http.createServer((req, res) => {
  if (req.url.startsWith("/fio/periods/")) {
    fioCalls++;
    if (fioDown) { res.statusCode = 401; return res.end("{}"); }
    const transaction = payments.map((p, i) => ({
      column22: { value: 1000 + i }, column0: { value: p.date }, column1: { value: p.amount },
      column14: { value: "CZK" }, column5: p.vs ? { value: p.vs } : null,
    }));
    res.setHeader("Content-Type", "application/json");
    return res.end(JSON.stringify({ accountStatement: { transactionList: { transaction } } }));
  }
  if (req.url === "/emails" && req.method === "POST") {
    let body = "";
    req.on("data", (c) => (body += c));
    return req.on("end", () => {
      emails.push(JSON.parse(body));
      res.end(JSON.stringify({ id: "mock" }));
    });
  }
  res.statusCode = 404;
  res.end();
});
await new Promise((r) => mock.listen(MOCK, r));

rmSync(STORE, { recursive: true, force: true });
const app = spawn("npx", ["next", "start", "-p", String(APP)], {
  cwd: new URL("..", import.meta.url).pathname,
  env: {
    ...process.env,
    LOCAL_STORE_DIR: STORE,
    FIO_TOKEN: "test-token",
    FIO_API_BASE: `http://localhost:${MOCK}/fio`,
    RESEND_API_KEY: "test",
    RESEND_API_URL: `http://localhost:${MOCK}/emails`,
    CRON_SECRET: SECRET,
    SALES_OPEN: "1",
    SITE_URL: `http://localhost:${APP}`,
    STATS_KEY: "tajne",
  },
  stdio: ["ignore", "pipe", "pipe"],
  detached: true, // vlastní skupina procesů, aby šel ukončit i next-server pod npx
});
let appLog = "";
app.stdout.on("data", (d) => (appLog += d));
app.stderr.on("data", (d) => (appLog += d));
const base = `http://localhost:${APP}`;
for (let i = 0; i < 60; i++) {
  if (await fetch(base).then((r) => r.ok, () => false)) break;
  await new Promise((r) => setTimeout(r, 500));
}

const cron = (auth = `Bearer ${SECRET}`) => fetch(`${base}/api/cron/fio`, { headers: { authorization: auth } });
const today = new Date().toISOString().slice(0, 10) + "+0200";
const browser = await chromium.launch({ executablePath: CHROMIUM });

try {
  // 1) Objednávka přes formulář
  const page = await browser.newPage();
  await page.goto(`${base}/objednat`);
  await page.fill("#email", "Nevesta@Example.cz");
  await page.fill("#name", "Tereza Nováková");
  await page.check('input[name="terms"]');
  await page.click('button[type="submit"]');
  await page.waitForURL(/\/objednavka\//);
  const orderUrl = page.url();
  const id = orderUrl.split("/").pop();
  check((await page.locator(".qr svg").count()) === 1, "stránka objednávky ukazuje QR kód");
  const vs = (await page.locator(".pay-table tr:nth-child(3) td:last-child").textContent()).trim();
  check(/^\d{10}$/.test(vs), `VS má 10 číslic (${vs})`);
  check((await page.locator(".pay-table").textContent()).includes("2202343801/2010"), "číslo účtu Fio na stránce");

  await new Promise((r) => setTimeout(r, 500));
  check(toCustomer().length === 1 && toCustomer()[0].subject.includes(vs), "e-mail s platebními údaji odešel (na e-mail malými písmeny)");
  check(toCustomer()[0]?.html.includes(`/objednavka/${id}`), "e-mail odkazuje na stránku objednávky");

  // 2) Stažení před zaplacením nesmí projít
  const early = await fetch(`${base}/stahnout/${id}`, { redirect: "manual" });
  check(early.status === 303, "stažení před zaplacením přesměruje na objednávku");

  // 3) Cron: autorizace a prázdný běh
  check((await cron("Bearer spatne")).status === 401, "cron bez správného tajemství vrací 401");
  let r = await (await cron()).json();
  check(r.pending === 1 && r.paid.length === 0, "cron bez platby nic nezaplatí");

  // 4) Nedoplatek se nespáruje
  payments.push({ vs, amount: 100, date: today });
  await new Promise((r) => setTimeout(r, 100));
  r = await (await cron()).json();
  check(r.underpaid.includes(vs) && r.paid.length === 0, "nedoplatek se nespáruje");
  check(toOwner().some((e) => e.subject.includes("Nedoplatek")), "firma dostala upozornění na nedoplatek");
  await cron();
  check(toOwner().filter((e) => e.subject.includes("Nedoplatek")).length === 1, "nedoplatek se hlásí jen jednou");

  // 5) Správná platba
  payments.length = 0;
  payments.push({ vs, amount: 349, date: today });
  r = await (await cron()).json();
  check(r.paid.includes(vs), "platba 349 Kč se spárovala");
  r = await (await cron()).json();
  check(r.pending === 0 && r.paid.length === 0, "druhý běh cronu už nic nedělá");
  const delivery = toCustomer()[1];
  check(toCustomer().length === 2 && delivery.subject.includes("plánovač"), "doručovací e-mail odešel");
  check(delivery?.html.includes(`/stahnout/${id}`) && delivery?.html.includes(`Doklad o zaplacení č. ${vs}`), "e-mail obsahuje odkaz ke stažení a doklad");
  check(toOwner().some((e) => e.subject.includes("Zaplaceno 349")), "firma dostala upozornění na zaplacení");

  // 6) Stránka se po zaplacení sama překreslí (poll 15 s)
  await page.waitForSelector("text=Zaplaceno, děkujeme!", { timeout: 25_000 });
  check(true, "stránka objednávky se sama přepnula na zaplaceno");

  // 7) Stažení vrací přesně prodejní soubor
  const dl = await fetch(`${base}/stahnout/${id}`);
  const got = Buffer.from(await dl.arrayBuffer());
  const want = readFileSync(new URL("../private/svatebni-planovac-anoberu.xlsx", import.meta.url));
  check(dl.ok && got.equals(want), "stažený soubor je prodejní plánovač");
  check(dl.headers.get("content-disposition")?.includes("attachment"), "soubor se stahuje jako příloha");

  // 8) Doklad
  await page.goto(`${base}/doklad/${id}`);
  const receipt = await page.textContent("main");
  check(receipt.includes(`č. ${vs}`) && receipt.includes("Tereza Nováková") && receipt.includes("17617421"), "doklad má číslo, kupujícího a IČO");

  // 9) Stará platba nesmí odemknout novou objednávku se stejným VS (VS se nerecyklují)
  const second = await fetch(`${base}/api/orders`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "druha@example.cz", name: "Druhá", terms: true }),
  }).then((x) => x.json());
  const secondPage = await fetch(`${base}/objednavka/${second.id}`).then((x) => x.text());
  check(!secondPage.includes(`>${vs}<`), "nová objednávka dostala jiný VS");
  r = await (await cron()).json();
  check(r.pending === 1 && r.paid.length === 0, "stará platba neodemkla novou objednávku");

  // 9a) Objednávka, jejíž ID obsahuje „_“ (u base64url běžné), se musí spárovat
  const uid = "Ab_cD_eF_gH_iJ_kL_mN_o"; // 22 znaků jako skutečné ID
  const uvs = vs.slice(0, 6) + "4242";
  const uorder = { id: uid, vs: uvs, email: "podtrzitko@example.cz", name: "Podtržítko", amount: 349, status: "pending",
    createdAt: new Date().toISOString(), consents: { terms: new Date().toISOString(), marketing: false } };
  writeFileSync(`${STORE}orders/${uid}.json`, JSON.stringify(uorder));
  writeFileSync(`${STORE}pending/${uvs}_${uid}`, uid);
  payments.push({ vs: uvs, amount: 349, date: today });
  r = await (await cron()).json();
  check(r.paid.includes(uvs), "objednávka s podtržítky v ID se spárovala");

  // 9b) Platba s „naším“ VS bez objednávky se nahlásí jednou
  payments.push({ vs: vs.slice(0, 6) + "9999", amount: 349, date: today });
  await cron();
  await cron();
  check(toOwner().filter((e) => e.subject.includes("Platba bez objednávky")).length === 1, "platba bez objednávky nahlášena firmě jednou");

  // 9c) Měsíční přehled pro účetní
  const month = new Date().toISOString().slice(0, 7);
  const rep = await (await fetch(`${base}/api/cron/report?month=${month}`, { headers: { authorization: `Bearer ${SECRET}` } })).json();
  const report = toOwner().find((e) => e.subject.includes("Přehled prodejů"));
  const csv = report ? Buffer.from(report.attachments[0].content, "base64").toString("utf8") : "";
  check(rep.count === 2 && rep.total === 698, `měsíční přehled: 2 objednávky za 698 Kč (${rep.count}, ${rep.total})`);
  check(csv.includes(vs) && csv.includes("Tereza Nováková") && csv.includes(uvs), "CSV pro účetní obsahuje doklady a kupující");
  check((await fetch(`${base}/api/cron/report`)).status === 401, "přehled bez tajemství vrací 401");

  // 10) Validace a honeypot
  const bad = await fetch(`${base}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "neplatny", name: "X", terms: true }) });
  check(bad.status === 400, "neplatný e-mail odmítnut");
  const noTerms = await fetch(`${base}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "a@example.cz", name: "X", terms: false }) });
  check(noTerms.status === 400, "bez souhlasu s VOP odmítnuto");
  const bot = await fetch(`${base}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "a@example.cz", name: "X", terms: true, website: "spam" }) });
  check(bot.status === 400, "honeypot zastaví bota");
  const nf = await fetch(`${base}/objednavka/neexistuje`);
  check(nf.status === 404 && (await nf.text()).includes("Tahle stránka tu není"), "neexistující objednávka vrací českou 404");
  const spam = async (email) => (await fetch(`${base}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json", "x-real-ip": "203.0.113.9" },
    body: JSON.stringify({ email, name: "Bot", terms: true }) })).status;
  const burst = [];
  for (let i = 0; i < 6; i++) burst.push(await spam(`bot${i}@example.cz`));
  check(burst.slice(0, 5).every((x) => x === 200) && burst[5] === 429, `6. objednávka z jedné IP za hodinu odmítnuta (${burst.join(",")})`);
  const same = [];
  for (let i = 0; i < 4; i++) same.push((await fetch(`${base}/api/orders`, { method: "POST", headers: { "Content-Type": "application/json", "x-real-ip": `198.51.100.${i}` },
    body: JSON.stringify({ email: "stejny@example.cz", name: "X", terms: true }) })).status);
  check(same.slice(0, 3).every((x) => x === 200) && same[3] === 429, `4. objednávka na stejný e-mail za den odmítnuta (${same.join(",")})`);
  check(fioCalls >= 4, `Fio API voláno (${fioCalls}×)`);

  // 10b) Výpadek Fio API se nahlásí firmě jednou denně
  fioDown = true;
  const down = await cron();
  await cron();
  fioDown = false;
  check(down.status === 502, "cron při chybě Fio vrací 502");
  check(toOwner().filter((e) => e.subject.includes("Párování plateb nefunguje")).length === 1, "výpadek Fio nahlášen firmě jednou");

  // 11) Nastavení: uložení tokenu Fio přes stránku (lokálně povoleno, na produkci jen *.vercel.app)
  await page.goto(`${base}/nastaveni`);
  const settings = await page.textContent("main");
  check(settings.includes("2 × 698") && settings.includes("stejny@example.cz"), "nastavení ukazuje přehled prodejů a poslední objednávky");
  await page.locator('form').first().locator('input[name="token"]').fill("kratky");
  await page.locator('form').first().locator('button').click();
  await page.waitForSelector("text=nevypadá jako token");
  check(true, "nastavení odmítne nesmyslný token");
  await page.locator('form').first().locator('input[name="token"]').fill("AbCdEf1234567890GhIjKl1234567890");
  await page.locator('form').first().locator('button').click();
  await page.waitForSelector("text=Token funguje a je uložený");
  check(readFileSync(`${STORE}secrets/FIO_TOKEN`, "utf8") === "AbCdEf1234567890GhIjKl1234567890", "token Fio uložen do úložiště");

  // Metriky (pojistka z FAILS.md): anonymní trychtýř, anketa, souhrn se závěry
  const BASE_URL = `http://localhost:${APP}`;
  const ua = { "User-Agent": "Mozilla/5.0 (e2e) Safari" };
  const beacon = (body, h = ua) => fetch(`${BASE_URL}/api/e`, { method: "POST", headers: { "Content-Type": "application/json", ...h }, body: JSON.stringify(body) });
  const pvA = "33333333-3333-4333-8333-333333333333";
  for (const ev of ["view", "t10", "scroll50", "cta_buy"]) await beacon({ pv: pvA, ev, page: "home", topic: "", src: "sklik" });
  const pvB = "44444444-4444-4444-8444-444444444444";
  for (const ev of ["view", "form_start", "form_submit"]) await beacon({ pv: pvB, ev, page: "objednat", topic: "", src: "" });
  await beacon({ pv: pvA, ev: "feedback", page: "home", topic: "", src: "sklik", choice: "zdarma", text: "mám šablonu" });
  check((await beacon({ pv: "x", ev: "view", page: "home" })).status === 400, "metriky: neplatná událost odmítnuta");
  check((await beacon({ pv: pvA, ev: "view", page: "home" }, { "User-Agent": "Googlebot/2.1" })).status === 204, "metriky: robot se tiše ignoruje");
  check((await fetch(`${BASE_URL}/api/stats`)).status === 401, "metriky: souhrn je chráněný");
  const st = await (await fetch(`${BASE_URL}/api/stats`, { headers: { "x-stats-key": "tajne" } })).json();
  check(st.funnel.byType.home.view === 1 && st.funnel.byType.home.cta_buy === 1 && st.funnel.byType.objednat.form_submit === 1, "metriky: trychtýř úvod → objednávka");
  check(st.orders.created >= 1 && st.orders.paid >= 1 && st.feedback["Stačí mi šablona zdarma"] === 1, "metriky: objednávky a důvody z ankety v souhrnu");
  const homeHtml = await (await fetch(BASE_URL, { headers: ua })).text();
  check(homeHtml.includes("co vás zatím drží od objednání") && homeHtml.includes('data-track="cta_buy"'), "metriky: anketa a měřená tlačítka na úvodu");
} catch (e) {
  failures++;
  console.error(e);
  console.error(appLog.slice(-3000));
} finally {
  await browser.close();
  process.kill(-app.pid, "SIGTERM");
  mock.close();
  rmSync(STORE, { recursive: true, force: true });
}

console.log(failures ? `\n${failures} kontrol selhalo` : "\nVšechny kontroly prošly");
process.exit(failures ? 1 : 0);
