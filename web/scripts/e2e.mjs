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
let fioCalls = 0;
const mock = http.createServer((req, res) => {
  if (req.url.startsWith("/fio/periods/test-token/")) {
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
  check(emails.length === 1 && emails[0].subject.includes(vs), "e-mail s platebními údaji odešel");
  check(emails[0]?.to === "nevesta@example.cz", "e-mail normalizovaný na malá písmena");
  check(emails[0]?.html.includes(`/objednavka/${id}`), "e-mail odkazuje na stránku objednávky");

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

  // 5) Správná platba
  payments.length = 0;
  payments.push({ vs, amount: 349, date: today });
  r = await (await cron()).json();
  check(r.paid.includes(vs), "platba 349 Kč se spárovala");
  r = await (await cron()).json();
  check(r.pending === 0 && r.paid.length === 0, "druhý běh cronu už nic nedělá");
  check(emails.length === 2 && emails[1].subject.includes("plánovač"), "doručovací e-mail odešel");
  check(emails[1]?.html.includes(`/stahnout/${id}`) && emails[1]?.html.includes(`Doklad o zaplacení č. ${vs}`), "e-mail obsahuje odkaz ke stažení a doklad");

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
  check(fioCalls >= 4, `Fio API voláno (${fioCalls}×)`);
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
