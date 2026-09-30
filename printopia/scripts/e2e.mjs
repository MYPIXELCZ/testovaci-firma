// E2E test testovací stránky: build musí proběhnout předem (npm run test:e2e).
import { spawn } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const PORT = 3200;
const BASE = `http://localhost:${PORT}`;
const store = mkdtempSync(path.join(tmpdir(), "printopia-"));
const app = spawn("npx", ["next", "start", "-p", String(PORT)], {
  env: { ...process.env, LOCAL_STORE_DIR: store, BLOB_READ_WRITE_TOKEN: "", VERCEL: "", STATS_KEY: "tajne" },
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
  const home = await (await get("/?utm_source=sklik")).text();
  check(home.includes("Přijímačky z matiky po tématech"), "úvodní stránka");
  check(home.includes('class="fr"'), "zlomky nad sebou v ukázce");
  check(home.includes("/koupit?src=sklik"), "zdroj návštěvy se předává do Koupit");
  const pdf = await fetch(`${BASE}/ukazka-zlomky.pdf`);
  check(pdf.ok && pdf.headers.get("content-type")?.includes("pdf"), "ukázka PDF ke stažení");
  const buy = await (await get("/koupit?src=sklik")).text();
  check(buy.includes("Sadu spouštíme") && buy.includes("279"), "stránka Koupit (spuštění + sleva)");
  check((await fetch(`${BASE}/ochrana-osobnich-udaju`)).ok, "ochrana osobních údajů");
  const zl = await (await fetch(`${BASE}/zlomky-prijimacky`)).text();
  check(zl.includes("Zlomky na přijímačky") && zl.includes("240 stran"), "stránka Zlomky s příklady a řešením");
  const sm = await (await fetch(`${BASE}/sitemap.xml`)).text();
  check(["/zlomky-prijimacky", "/procenta-prijimacky", "/rovnice-prijimacky", "/slovni-ulohy-prijimacky"].every((u) => sm.includes(u)), "sitemap obsahuje všechna témata");
  const pr = await (await fetch(`${BASE}/procenta-prijimacky`)).text();
  check(pr.includes("Procenta na přijímačky") && pr.includes("21 218 Kč"), "stránka Procenta");
  const ro = await (await fetch(`${BASE}/rovnice-prijimacky`)).text();
  check(ro.includes("Rovnice na přijímačky") && ro.includes("v 9:30, 27 km od Brna"), "stránka Rovnice");
  const sl = await (await fetch(`${BASE}/slovni-ulohy-prijimacky`)).text();
  check(sl.includes("Slovní úlohy na přijímačky") && sl.includes("21 slepic"), "stránka Slovní úlohy");
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
  check(r1.ok && j1.download === "/ukazka-zlomky.pdf", "lead z ukázky vrátí odkaz na PDF");
  const r2 = await post({ email: "rodic@example.cz", consent: true, role: "rodic", source: "koupit", src: "sklik" });
  check(r2.ok, "lead z Koupit");
  const hp = await post({ email: "bot@example.cz", consent: true, source: "ukazka", website: "x" });
  check(hp.ok, "honeypot odpoví ok");
  const files = readdirSync(path.join(store, "leads"));
  check(files.length === 1, "jeden e-mail = jeden záznam (bot se neuložil)");
  const lead = JSON.parse(readFileSync(path.join(store, "leads", files[0]), "utf8"));
  check(lead.email === "rodic@example.cz" && lead.sources.join() === "ukazka,koupit" && lead.src === "sklik" && lead.role === "rodic", "záznam má zdroje, roli i původ");
  check(logs.includes('"ev":"visit"') && logs.includes('"ev":"buy_click"') && logs.includes('"ev":"lead"'), "události v logu pro měření testu");
  await fetch(`${BASE}/`, { headers: { "User-Agent": "Googlebot/2.1" } });
  await new Promise((r) => setTimeout(r, 500));
  check((await fetch(`${BASE}/api/stats`)).status === 401, "souhrn testu je chráněný");
  const st = await (await fetch(`${BASE}/api/stats`, { headers: { "x-stats-key": "tajne" } })).json();
  check(st.events.visit?.sklik === 1 && st.events.buy_click?.sklik === 1 && st.totals.leads === 1, "souhrn: návštěva, klik na Koupit a lead ze Skliku (robot a opakovaný lead nezapočten)");
  check(st.leadsByRole.rodic === 1 && st.buyClickRate === 1 / st.totals.visits, "souhrn: role a míra kliků na Koupit");
} finally {
  process.kill(-app.pid);
}
console.log(failed ? `\n${failed} kontrol selhalo` : "\nVšechny kontroly prošly");
process.exit(failed ? 1 : 0);
