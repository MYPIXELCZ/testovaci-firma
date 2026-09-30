// End-to-end test nákupu: objednávka -> QR -> platba (falešné Fio) -> cron -> doručení -> stažení.
// Spouštění: npm run build && node scripts/e2e.mjs
// Potřebuje Chromium (CHROMIUM_PATH, výchozí /opt/pw-browsers/...). Nic neposílá ven.
import { spawn } from "node:child_process";
import { readFileSync, rmSync } from "node:fs";
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
const mock = http.createServer((req, res) => {
  if (req.url.startsWith("/fio/periods/")) {
    fioCalls++;
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
  check(rep.count === 1 && rep.total === 349, `měsíční přehled: 1 objednávka za 349 Kč (${rep.count}, ${rep.total})`);
  check(csv.includes(vs) && csv.includes("Tereza Nováková"), "CSV pro účetní obsahuje doklad a kupujícího");
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
  check((await fetch(`${base}/objednavka/neexistuje`)).status === 404, "neexistující objednávka vrací 404");
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

  // 11) Nastavení: uložení tokenu Fio přes stránku (lokálně povoleno, na produkci jen *.vercel.app)
  await page.goto(`${base}/nastaveni`);
  await page.locator('form').first().locator('input[name="token"]').fill("kratky");
  await page.locator('form').first().locator('button').click();
  await page.waitForSelector("text=nevypadá jako token");
  check(true, "nastavení odmítne nesmyslný token");
  await page.locator('form').first().locator('input[name="token"]').fill("AbCdEf1234567890GhIjKl1234567890");
  await page.locator('form').first().locator('button').click();
  await page.waitForSelector("text=Token funguje a je uložený");
  check(readFileSync(`${STORE}secrets/FIO_TOKEN`, "utf8") === "AbCdEf1234567890GhIjKl1234567890", "token Fio uložen do úložiště");
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
