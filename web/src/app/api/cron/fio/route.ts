import { SALES_OPEN, UNPAID_RETENTION_DAYS } from "@/lib/config";
import { sendDelivery } from "@/lib/email";
import { incomingPayments } from "@/lib/fio";
import { getSecret } from "@/lib/secrets";
import { deleteOrder, getOrder, listPending, markPaid } from "@/lib/orders";

export const maxDuration = 60;

/** Vercel Cron (vercel.json): spáruje příchozí platby z Fio s nezaplacenými objednávkami. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }

  if (!SALES_OPEN) {
    // Před spuštěním hlásí připravenost do logu (bez obsahu tajemství). Testovací objednávky se párují i tak.
    const [fio, resend] = await Promise.all([getSecret("FIO_TOKEN"), getSecret("RESEND_API_KEY")]);
    console.log(`[cron] prodej vypnutý; fio=${Boolean(fio)} resend=${Boolean(resend)}`);
  }

  const pending = await listPending();
  const result = { pending: pending.length, paid: [] as string[], underpaid: [] as string[], expired: 0 };

  if (pending.length > 0) {
    const payments = await incomingPayments();
    for (const p of pending) {
      // Platba musí přijít v den objednávky nebo později (Fio datum: "2026-09-30+0200").
      const created = p.uploadedAt.toISOString().slice(0, 10);
      const payment = payments.find((x) => x.vs === p.vs && x.currency === "CZK" && x.date.slice(0, 10) >= created);
      if (!payment) continue;
      const order = await getOrder(p.id);
      if (!order || order.status !== "pending") continue;
      if (payment.amount < order.amount) {
        result.underpaid.push(order.vs); // řeší se ručně, viz log
        continue;
      }
      const paid = await markPaid(order, payment.id);
      result.paid.push(paid.vs);
      try {
        await sendDelivery(paid);
      } catch (e) {
        console.error("[cron] doručovací e-mail selhal", paid.vs, e);
      }
    }
  }

  const cutoff = Date.now() - UNPAID_RETENTION_DAYS * 86_400_000;
  for (const p of pending) {
    if (p.uploadedAt.getTime() < cutoff && !result.paid.includes(p.vs)) {
      await deleteOrder(p);
      result.expired++;
    }
  }

  if (result.paid.length || result.underpaid.length || result.expired) console.log("[cron]", JSON.stringify(result));
  return Response.json(result);
}
