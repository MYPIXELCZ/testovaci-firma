import { notifyOwner, sendDelivery } from "@/lib/email";
import { getOrder, markPaid, paymentSeen } from "@/lib/orders";
import { verifyWebhook } from "@/lib/stripe";

/** Stripe webhook: po zaplacení (checkout.session.completed, async_payment_succeeded) označí objednávku a pošle sadu. */
export async function POST(req: Request) {
  const raw = await req.text();
  if (!verifyWebhook(raw, req.headers.get("stripe-signature"))) return new Response("Neplatný podpis", { status: 400 });
  const event = JSON.parse(raw);
  if (!["checkout.session.completed", "checkout.session.async_payment_succeeded"].includes(event.type)) return Response.json({ ok: true, ignored: event.type });
  const s = event.data?.object ?? {};
  if (s.payment_status !== "paid") return Response.json({ ok: true, waiting: s.payment_status });

  const order = await getOrder(String(s.client_reference_id ?? ""));
  const payId = `stripe_${s.id}`;
  if (!order || order.status !== "pending" || (await paymentSeen(payId))) return Response.json({ ok: true, skipped: true });
  if (s.currency !== "czk" || s.amount_total !== order.amount * 100) {
    await notifyOwner(`Platba kartou nesedí k objednávce ${order.vs}`, [
      `Stripe ${s.id}: ${s.amount_total} ${s.currency}, objednávka ${order.amount} Kč (${order.name}, ${order.email}).`,
      "Objednávka zůstává nezaplacená. Zkontrolujte platbu ve Stripe a domluvte se se zákazníkem.",
    ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
    return Response.json({ ok: true, mismatch: true });
  }
  const paid = await markPaid(order, payId);
  await sendDelivery(paid).catch((e) => console.error("[stripe] doručovací e-mail selhal", paid.vs, e));
  await notifyOwner(`Zaplaceno kartou ${paid.amount} Kč${paid.test ? " (test)" : ""}`, [
    `Objednávka ${paid.vs}: ${paid.name}, ${paid.email}`,
    `Stripe platba ${s.id}. Výplata ze Stripe přijde na bankovní účet podle nastavení Stripe.`,
  ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
  return Response.json({ ok: true, paid: paid.vs });
}
