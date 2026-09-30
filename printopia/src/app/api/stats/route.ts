import { storage } from "@/lib/storage";

// Souhrn testu poptávky (plan/prijimacky.md, oddíl 4). Chráněno klíčem STATS_KEY, bez osobních údajů.
export async function GET(req: Request) {
  const key = process.env.STATS_KEY;
  if (!key || req.headers.get("x-stats-key") !== key) return new Response("Unauthorized", { status: 401 });

  const counts: Record<string, Record<string, number>> = {};
  const days = new Set<string>();
  for (const item of await storage.list("events/")) {
    const [, day, ev, src] = item.pathname.split("/");
    if (src === "selftest") continue;
    days.add(day);
    counts[ev] ??= {};
    counts[ev][src] = (counts[ev][src] ?? 0) + 1;
  }
  const roles: Record<string, number> = {};
  const leadSources: Record<string, number> = {};
  for (const item of await storage.list("leads/")) {
    const lead = JSON.parse((await storage.read(item.pathname)) ?? "{}");
    if (lead.src === "selftest") continue;
    roles[lead.role ?? "?"] = (roles[lead.role ?? "?"] ?? 0) + 1;
    for (const s of lead.sources ?? []) leadSources[s] = (leadSources[s] ?? 0) + 1;
  }
  const sum = (o?: Record<string, number>) => Object.values(o ?? {}).reduce((a, b) => a + b, 0);
  const visits = sum(counts.visit);
  return Response.json({
    days: [...days].sort(),
    events: counts,
    totals: { visits, buyClicks: sum(counts.buy_click), leads: sum(counts.lead) },
    buyClickRate: visits ? sum(counts.buy_click) / visits : null,
    leadsByRole: roles,
    leadsBySource: leadSources,
  });
}
