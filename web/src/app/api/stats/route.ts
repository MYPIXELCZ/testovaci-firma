import { FEEDBACK, type FeedbackKey } from "@/lib/metrics";
import { listOrders } from "@/lib/orders";
import { storage } from "@/lib/storage";

// Souhrn pro vyhodnocení (pojistka z FAILS.md): kde lidé odpadají a proč. Chráněno STATS_KEY, bez osobních údajů.
const STEPS = ["view", "t10", "t30", "scroll50", "scroll100", "cta_buy", "cta_checklist", "form_start", "form_submit", "feedback"] as const;
type Funnel = Record<(typeof STEPS)[number], number>;
const empty = (): Funnel => Object.fromEntries(STEPS.map((s) => [s, 0])) as Funnel;
const pct = (a: number, b: number) => (b ? Math.round((a / b) * 1000) / 10 : null);

export async function GET(req: Request) {
  const key = process.env.STATS_KEY;
  if (!key || req.headers.get("x-stats-key") !== key) return new Response("Unauthorized", { status: 401 });

  const visits = new Map<string, { page: string; src: string; device: string; steps: Set<string> }>();
  const feedback: Record<string, number> = {};
  const feedbackTexts: string[] = [];
  for (const item of await storage.list("beacons/")) {
    const [, , page, src, device, pv, file] = item.pathname.split("/");
    if (src === "selftest") continue;
    const [ev, choice] = file.replace(/\.json$/, "").split("~");
    const v = visits.get(pv) ?? { page, src, device, steps: new Set<string>() };
    v.steps.add(ev);
    visits.set(pv, v);
    if (ev === "feedback" && choice) {
      const label = FEEDBACK[choice as FeedbackKey] ?? choice;
      feedback[label] = (feedback[label] ?? 0) + 1;
      const text = JSON.parse((await storage.read(item.pathname)) ?? "{}").text;
      if (text && feedbackTexts.length < 50) feedbackTexts.push(text);
    }
  }
  // Stránky sloučíme podle typu (články dohromady) i zvlášť.
  const byPage: Record<string, Funnel> = {};
  const byType: Record<string, Funnel> = {};
  const byDevice: Record<string, Funnel> = {};
  const bySrc: Record<string, Funnel> = {};
  for (const v of visits.values()) {
    const type = v.page.split("-")[0];
    for (const [map, k] of [[byPage, v.page], [byType, type], [byDevice, `${type}:${v.device}`], [bySrc, `${type}:${v.src}`]] as const) {
      map[k] ??= empty();
      for (const s of v.steps) if (s in map[k]) map[k][s as keyof Funnel]++;
    }
  }

  const orders = (await listOrders()).filter((o) => !o.test);
  const paid = orders.filter((o) => o.status === "paid").length;
  const entry = { view: (byType.home?.view ?? 0) + (byType.clanek?.view ?? 0), buy: (byType.home?.cta_buy ?? 0) + (byType.clanek?.cta_buy ?? 0) };
  const o = byType.objednat ?? empty();

  const findings: string[] = [];
  if (entry.view < 30) findings.push(`Málo dat: ${entry.view} návštěv úvodu a článků, závěry až od 30.`);
  else {
    if (pct(entry.buy, entry.view)! < 1) findings.push("Z úvodu a článků skoro nikdo neklikne na Koupit: nabídka nezaujala nebo ji nevidí.");
    if (o.view >= 5 && pct(o.form_submit, o.view)! < 30) findings.push("Na stránce objednávky většina skončí: formulář nebo cena odrazuje.");
    if (orders.length >= 3 && pct(paid, orders.length)! < 50) findings.push("Objednávky se neplatí: QR platba nebo důvěra (zkontrolovat stránku s platbou a e-mail).");
    const top = Object.entries(feedback).sort((a, b) => b[1] - a[1])[0];
    if (top) findings.push(`Nejčastější důvod z ankety: ${top[0]} (${top[1]}×).`);
  }
  return Response.json({
    funnel: { byType, byPage, byDevice, bySrc },
    orders: { created: orders.length, paid },
    rates: { entryToBuyClick: pct(entry.buy, entry.view), orderFormCompletion: pct(o.form_submit, o.view), orderToPaid: pct(paid, orders.length) },
    feedback,
    feedbackTexts,
    findings,
  });
}
