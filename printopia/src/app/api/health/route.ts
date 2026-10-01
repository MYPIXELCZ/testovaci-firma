import { SALES_OPEN } from "@/lib/config";
import { incomingPayments } from "@/lib/fio";

export const maxDuration = 30;

/** Diagnostika (chráněno STATS_KEY): vidí Fio API platby? Je zapnutý prodej a e-maily? Bez osobních údajů a bez tajemství. */
export async function GET(req: Request) {
  const key = process.env.STATS_KEY;
  if (!key || req.headers.get("x-stats-key") !== key) return Response.json({ ok: true });
  let fio: Record<string, unknown>;
  try {
    const p = await incomingPayments(7);
    fio = { ok: true, payments: p.length, last: p.slice(-5).map((x) => ({ vs: x.vs, amount: x.amount, date: x.date.slice(0, 10) })) };
  } catch (e) {
    fio = { ok: false, error: e instanceof Error ? e.message : String(e) };
  }
  return Response.json({ ok: true, salesOpen: SALES_OPEN, fio, resend: Boolean(process.env.RESEND_API_KEY), cron: Boolean(process.env.CRON_SECRET) });
}
