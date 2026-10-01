import { computeStats } from "@/lib/stats";

// Souhrn testu poptávky (plan/prijimacky.md, oddíl 4). Chráněno klíčem STATS_KEY, bez osobních údajů.
export async function GET(req: Request) {
  const key = process.env.STATS_KEY;
  if (!key || req.headers.get("x-stats-key") !== key) return new Response("Unauthorized", { status: 401 });
  return Response.json(await computeStats());
}
