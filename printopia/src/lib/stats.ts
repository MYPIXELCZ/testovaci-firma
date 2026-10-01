import "server-only";
import { FEEDBACK, type FeedbackKey } from "@/lib/metrics";
import { listOrders } from "@/lib/orders";
import { storage } from "@/lib/storage";

// Souhrn testu poptávky (plan/prijimacky.md, oddíl 4). Chráněno klíčem STATS_KEY, bez osobních údajů.
// Odpovídá i na otázku „proč nekupují“: trychtýř po krocích, zařízení, zdroje, důvody z ankety a automatické závěry.
const STEPS = ["view", "t10", "t30", "scroll50", "scroll100", "cta_sample", "cta_buy", "topic_link", "solution_open",
  "form_start", "form_submit", "pdf_download", "feedback"] as const;
type Funnel = Record<(typeof STEPS)[number], number>;
const empty = (): Funnel => Object.fromEntries(STEPS.map((s) => [s, 0])) as Funnel;
const pct = (a: number, b: number) => (b ? Math.round((a / b) * 1000) / 10 : null);

export async function computeStats() {
  // 1) Serverové události (návštěvy, klik na Koupit, leady)
  const counts: Record<string, Record<string, number>> = {};
  const visitsByDay: Record<string, number> = {};
  for (const item of await storage.list("events/")) {
    const [, day, ev, src] = item.pathname.split("/");
    if (ev === "visit" && src !== "selftest") visitsByDay[day] = (visitsByDay[day] ?? 0) + 1;
    if (src === "selftest") continue;
    counts[ev] ??= {};
    counts[ev][src] = (counts[ev][src] ?? 0) + 1;
  }
  // Návštěvy ze Skliku podle klíčového slova a reklamy (utm_term, utm_content)
  const byTerm: Record<string, number> = {};
  const byAd: Record<string, number> = {};
  for (const item of (await storage.list("events/")).filter((i) => i.pathname.split("/")[2] === "visit" && i.pathname.split("/")[3] === "sklik")) {
    const x = JSON.parse((await storage.read(item.pathname)) ?? "{}");
    if (x.term) byTerm[x.term] = (byTerm[x.term] ?? 0) + 1;
    if (x.content) byAd[x.content] = (byAd[x.content] ?? 0) + 1;
  }
  const roles: Record<string, number> = {};
  for (const item of await storage.list("leads/")) {
    const lead = JSON.parse((await storage.read(item.pathname)) ?? "{}");
    if (lead.src !== "selftest") roles[lead.role ?? "?"] = (roles[lead.role ?? "?"] ?? 0) + 1;
  }

  // Objednávky a platby podle zdroje (bez osobních údajů, testovací se nepočítají)
  const orders = { created: {} as Record<string, number>, paid: {} as Record<string, number>, revenue: 0 };
  for (const o of (await listOrders()).filter((x) => !x.test)) {
    const k = o.src || "direct";
    orders.created[k] = (orders.created[k] ?? 0) + 1;
    if (o.status === "paid") {
      orders.paid[k] = (orders.paid[k] ?? 0) + 1;
      orders.revenue += o.amount;
    }
  }

  // 2) Trychtýř z anonymních událostí: počítáme návštěvy (pv), které daný krok udělaly aspoň jednou
  const visits = new Map<string, { page: string; src: string; device: string; steps: Set<string> }>();
  const feedback: Record<string, number> = {};
  const feedbackTexts: string[] = [];
  const days = new Set<string>();
  for (const item of await storage.list("beacons/")) {
    const [, day, page, src, device, pv, file] = item.pathname.split("/");
    if (src === "selftest") continue;
    const [ev, choice] = file.replace(/\.json$/, "").split("~");
    days.add(day);
    const v = visits.get(pv) ?? { page, src, device, steps: new Set<string>() };
    v.steps.add(ev);
    visits.set(pv, v);
    if (ev === "feedback" && choice) {
      feedback[FEEDBACK[choice as FeedbackKey] ?? choice] = (feedback[FEEDBACK[choice as FeedbackKey] ?? choice] ?? 0) + 1;
      const text = JSON.parse((await storage.read(item.pathname)) ?? "{}").text;
      if (text && feedbackTexts.length < 50) feedbackTexts.push(text);
    }
  }
  const byPage: Record<string, Funnel> = {};
  const bySrc: Record<string, Funnel> = {};
  const byDevice: Record<string, Funnel> = {};
  for (const v of visits.values()) {
    for (const [map, k] of [[byPage, v.page], [bySrc, `${v.page}:${v.src}`], [byDevice, `${v.page}:${v.device}`]] as const) {
      map[k] ??= empty();
      for (const s of v.steps) if (s in map[k]) map[k][s as keyof Funnel]++;
    }
  }

  // 3) Automatické závěry pro úvodní stránku (kde lidé odpadají)
  const sum = (o?: Record<string, number>) => Object.values(o ?? {}).reduce((a, b) => a + b, 0);
  const h = byPage.home ?? empty();
  const findings: string[] = [];
  if (h.view < 30) findings.push(`Málo dat: ${h.view} návštěv úvodní stránky, závěry až od 30.`);
  else {
    if (pct(h.t10, h.view)! < 40) findings.push("Většina odejde do 10 s: stránka neodpovídá tomu, co hledali (zkontrolovat hledané dotazy ve Skliku).");
    if (pct(h.scroll50, h.view)! < 30) findings.push("Málokdo dočte do poloviny: slabý začátek stránky (nadpis, úvod).");
    if (pct(h.cta_buy, h.view)! < 2 && pct(h.cta_sample, h.view)! < 5) findings.push("Skoro nikdo neklikne na Koupit ani na ukázku: nabídka nezaujala.");
    if (h.form_start > 0 && pct(h.form_submit, h.form_start)! < 50) findings.push("Lidé začnou vyplňovat formulář a nedokončí ho: formulář odrazuje (souhlasy, role).");
    const [created, paid] = [sum(orders.created), sum(orders.paid)];
    if (created > 0 && pct(paid, created)! < 60) findings.push(`Objednají, ale nezaplatí (${paid} z ${created}): zkontrolovat QR platbu a e-mail s platebními údaji.`);
    const k = byPage.koupit;
    if (k && k.view >= 10 && pct(k.form_submit, k.view)! < 20) findings.push("Na stránce objednávky skoro nikdo neodešle formulář: cena nebo formulář odrazují.");
    const top = Object.entries(feedback).sort((a, b) => b[1] - a[1])[0];
    if (top) findings.push(`Nejčastější důvod z ankety: ${top[0]} (${top[1]}×).`);
  }

  return {
    days: [...days].sort(),
    server: { visits: counts.visit ?? {}, visitsByDay, buyClicks: counts.buy_click ?? {}, leads: sum(counts.lead), leadsByRole: roles },
    orders,
    sklik: { byKeyword: byTerm, byAd },
    funnel: { byPage, bySrc, byDevice },
    rates: {
      homeToBuyClick: pct(h.cta_buy, h.view),
      homeToSample: pct(h.cta_sample, h.view),
      homeToLead: pct(h.form_submit, h.view),
      formCompletion: pct(h.form_submit, h.form_start),
    },
    feedback,
    feedbackTexts,
    findings,
  };
}
