import { FEEDBACK, type FeedbackKey } from "@/lib/metrics";
import { storage } from "@/lib/storage";

// Souhrn testu poptávky (plan/prijimacky.md, oddíl 4). Chráněno klíčem STATS_KEY, bez osobních údajů.
// Odpovídá i na otázku „proč nekupují“: trychtýř po krocích, zařízení, zdroje, důvody z ankety a automatické závěry.
const STEPS = ["view", "t10", "t30", "scroll50", "scroll100", "cta_sample", "cta_buy", "topic_link", "solution_open",
  "form_start", "form_submit", "pdf_download", "feedback"] as const;
type Funnel = Record<(typeof STEPS)[number], number>;
const empty = (): Funnel => Object.fromEntries(STEPS.map((s) => [s, 0])) as Funnel;
const pct = (a: number, b: number) => (b ? Math.round((a / b) * 1000) / 10 : null);

export async function GET(req: Request) {
  const key = process.env.STATS_KEY;
  if (!key || req.headers.get("x-stats-key") !== key) return new Response("Unauthorized", { status: 401 });

  // 1) Serverové události (návštěvy, klik na Koupit, leady)
  const counts: Record<string, Record<string, number>> = {};
  for (const item of await storage.list("events/")) {
    const [, , ev, src] = item.pathname.split("/");
    if (src === "selftest") continue;
    counts[ev] ??= {};
    counts[ev][src] = (counts[ev][src] ?? 0) + 1;
  }
  const roles: Record<string, number> = {};
  for (const item of await storage.list("leads/")) {
    const lead = JSON.parse((await storage.read(item.pathname)) ?? "{}");
    if (lead.src !== "selftest") roles[lead.role ?? "?"] = (roles[lead.role ?? "?"] ?? 0) + 1;
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
  const h = byPage.home ?? empty();
  const findings: string[] = [];
  if (h.view < 30) findings.push(`Málo dat: ${h.view} návštěv úvodní stránky, závěry až od 30.`);
  else {
    if (pct(h.t10, h.view)! < 40) findings.push("Většina odejde do 10 s: stránka neodpovídá tomu, co hledali (zkontrolovat hledané dotazy ve Skliku).");
    if (pct(h.scroll50, h.view)! < 30) findings.push("Málokdo dočte do poloviny: slabý začátek stránky (nadpis, úvod).");
    if (pct(h.cta_buy, h.view)! < 2 && pct(h.cta_sample, h.view)! < 5) findings.push("Skoro nikdo neklikne na Koupit ani na ukázku: nabídka nezaujala.");
    if (h.form_start > 0 && pct(h.form_submit, h.form_start)! < 50) findings.push("Lidé začnou vyplňovat formulář a nedokončí ho: formulář odrazuje (souhlasy, role).");
    const top = Object.entries(feedback).sort((a, b) => b[1] - a[1])[0];
    if (top) findings.push(`Nejčastější důvod z ankety: ${top[0]} (${top[1]}×).`);
  }

  const sum = (o?: Record<string, number>) => Object.values(o ?? {}).reduce((a, b) => a + b, 0);
  return Response.json({
    days: [...days].sort(),
    server: { visits: counts.visit ?? {}, buyClicks: counts.buy_click ?? {}, leads: sum(counts.lead), leadsByRole: roles },
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
  });
}
