// E2E test testovací stránky: build musí proběhnout předem (npm run test:e2e).
import { spawn } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const PORT = 3200;
const BASE = `http://localhost:${PORT}`;
const store = mkdtempSync(path.join(tmpdir(), "printopia-"));
const app = spawn("npx", ["next", "start", "-p", String(PORT)], {
  env: { ...process.env, LOCAL_STORE_DIR: store, BLOB_READ_WRITE_TOKEN: "", VERCEL: "" },
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
const post = (body) => fetch(`${BASE}/api/lead`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

try {
  for (let i = 0; i < 60; i++) {
    if (await fetch(BASE).then(() => true, () => false)) break;
    await new Promise((r) => setTimeout(r, 500));
  }
  const home = await (await fetch(`${BASE}/?utm_source=sklik`)).text();
  check(home.includes("Přijímačky z matiky po tématech"), "úvodní stránka");
  check(home.includes('class="fr"'), "zlomky nad sebou v ukázce");
  check(home.includes("/koupit?src=sklik"), "zdroj návštěvy se předává do Koupit");
  const pdf = await fetch(`${BASE}/ukazka-zlomky.pdf`);
  check(pdf.ok && pdf.headers.get("content-type")?.includes("pdf"), "ukázka PDF ke stažení");
  const buy = await (await fetch(`${BASE}/koupit?src=sklik`)).text();
  check(buy.includes("Sadu spouštíme") && buy.includes("279"), "stránka Koupit (spuštění + sleva)");
  check((await fetch(`${BASE}/ochrana-osobnich-udaju`)).ok, "ochrana osobních údajů");
  const zl = await (await fetch(`${BASE}/zlomky-prijimacky`)).text();
  check(zl.includes("Zlomky na přijímačky") && zl.includes("240 stran"), "stránka Zlomky s příklady a řešením");
  check((await (await fetch(`${BASE}/sitemap.xml`)).text()).includes("/zlomky-prijimacky"), "sitemap obsahuje Zlomky");
  check((await fetch(`${BASE}/og.png`)).ok, "náhled pro sdílení");
  check((await fetch(`${BASE}/neexistuje`)).status === 404, "404");

  check((await post({ email: "spatny", consent: true, source: "ukazka" })).status === 400, "odmítne neplatný e-mail");
  check((await post({ email: "a@b.cz", consent: false, source: "ukazka" })).status === 400, "odmítne bez souhlasu");
  const r1 = await post({ email: "Rodic@Example.cz", consent: true, source: "ukazka", src: "sklik" });
  const j1 = await r1.json();
  check(r1.ok && j1.download === "/ukazka-zlomky.pdf", "lead z ukázky vrátí odkaz na PDF");
  const r2 = await post({ email: "rodic@example.cz", consent: true, source: "koupit", src: "sklik" });
  check(r2.ok, "lead z Koupit");
  const hp = await post({ email: "bot@example.cz", consent: true, source: "ukazka", website: "x" });
  check(hp.ok, "honeypot odpoví ok");
  const files = readdirSync(path.join(store, "leads"));
  check(files.length === 1, "jeden e-mail = jeden záznam (bot se neuložil)");
  const lead = JSON.parse(readFileSync(path.join(store, "leads", files[0]), "utf8"));
  check(lead.email === "rodic@example.cz" && lead.sources.join() === "ukazka,koupit" && lead.src === "sklik", "záznam má zdroje i původ");
  check(logs.includes('"ev":"visit"') && logs.includes('"ev":"buy_click"') && logs.includes('"ev":"lead"'), "události v logu pro měření testu");
} finally {
  process.kill(-app.pid);
}
console.log(failed ? `\n${failed} kontrol selhalo` : "\nVšechny kontroly prošly");
process.exit(failed ? 1 : 0);
