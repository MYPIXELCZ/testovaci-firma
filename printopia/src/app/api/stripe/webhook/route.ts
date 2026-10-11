import { notifyOwner, sendDelivery } from "@/lib/email";
import { getOrder, markPaid, paymentSeen } from "@/lib/orders";
import { storage } from "@/lib/storage";
import { stripeAmountCzk, verifyWebhook } from "@/lib/stripe";

const kc = (haler: number | undefined, cur?: string) => `${((haler ?? 0) / 100).toLocaleString("cs-CZ")} ${(cur ?? "czk").toUpperCase() === "CZK" ? "Kč" : (cur ?? "").toUpperCase()}`;

/** Zapíše značku události (nejdřív zjistí, jestli už nebyla zpracována). Vrací true, když jde o první doručení. */
async function firstTime(kind: string, id: string) {
  const path = `stripe-events/${kind}/${id}`;
  if (await storage.exists(path)) return false;
  await storage.write(path, new Date().toISOString(), { overwrite: true });
  return true;
}

/** Objednávka podle PaymentIntentu platby (značku zakládá webhook po zaplacení). */
async function orderByIntent(pi: unknown) {
  const id = pi ? await storage.read(`stripe-pi/${pi}`).catch(() => null) : null;
  return id ? getOrder(String(id)) : null;
}

/**
 * Stripe webhook. Po zaplacení (checkout.session.completed, async_payment_succeeded) označí objednávku a pošle sadu.
 * Další události jen měří nebo upozorní firmu: checkout.session.expired a payment_intent.payment_failed (odpadání u platby),
 * charge.refunded (vrácení peněz) a charge.dispute.created (reklamace u banky, na odpověď bývá jen pár dní).
 */
export async function POST(req: Request) {
  const raw = await req.text();
  if (!verifyWebhook(raw, req.headers.get("stripe-signature"))) return new Response("Neplatný podpis", { status: 400 });
  const event = JSON.parse(raw);
  const s = event.data?.object ?? {};

  if (event.type === "checkout.session.expired" || event.type === "payment_intent.payment_failed") {
    await firstTime(event.type === "checkout.session.expired" ? "expired" : "failed", String(event.id));
    return Response.json({ ok: true, counted: event.type });
  }
  if (event.type === "charge.refunded") {
    if (!(await firstTime("refunded", String(event.id)))) return Response.json({ ok: true, skipped: true });
    const order = await orderByIntent(s.payment_intent);
    await notifyOwner(`Vrácení platby kartou${order ? ` (objednávka ${order.vs})` : ""}`, [
      `Stripe vrátil ${kc(s.amount_refunded, s.currency)} z platby ${kc(s.amount, s.currency)} (${s.id}).`,
      order ? `Objednávka ${order.vs}: ${order.name}, ${order.email}. Při odstoupení od smlouvy má kupující sadu dál nepoužívat.` : "Objednávku se nepodařilo spárovat, zkontrolujte platbu ve Stripe.",
    ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
    return Response.json({ ok: true, refunded: true });
  }
  if (event.type === "charge.dispute.created") {
    if (!(await firstTime("disputes", String(event.id)))) return Response.json({ ok: true, skipped: true });
    const order = await orderByIntent(s.payment_intent);
    const due = s.evidence_details?.due_by ? new Date(s.evidence_details.due_by * 1000).toLocaleString("cs-CZ", { timeZone: "Europe/Prague" }) : "neuvedeno";
    await notifyOwner(`POZOR: reklamace platby kartou u banky${order ? ` (objednávka ${order.vs})` : ""}`, [
      `Zákazník nebo banka zpochybnili platbu ${kc(s.amount, s.currency)} (důvod: ${s.reason ?? "neuveden"}, spor ${s.id}).`,
      `Termín na odpověď ve Stripe (Disputes): ${due}. Po termínu spor propadne a Stripe si strhne poplatek.`,
      order ? `Objednávka ${order.vs}: ${order.name}, ${order.email}.` : "Objednávku se nepodařilo spárovat.",
    ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
    return Response.json({ ok: true, dispute: true });
  }

  if (!["checkout.session.completed", "checkout.session.async_payment_succeeded"].includes(event.type)) return Response.json({ ok: true, ignored: event.type });
  if (s.payment_status !== "paid") return Response.json({ ok: true, waiting: s.payment_status });

  const order = await getOrder(String(s.client_reference_id ?? ""));
  const payId = `stripe_${s.id}`;
  if (!order || order.status !== "pending" || (await paymentSeen(payId))) return Response.json({ ok: true, skipped: true });
  if (s.currency !== "czk" || s.amount_total !== stripeAmountCzk(order) * 100) {
    await notifyOwner(`Platba kartou nesedí k objednávce ${order.vs}`, [
      `Stripe ${s.id}: ${s.amount_total} ${s.currency}, objednávka ${order.amount} Kč (${order.name}, ${order.email}).`,
      "Objednávka zůstává nezaplacená. Zkontrolujte platbu ve Stripe a domluvte se se zákazníkem.",
    ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
    return Response.json({ ok: true, mismatch: true });
  }
  const paid = await markPaid(order, payId);
  if (s.payment_intent) await storage.write(`stripe-pi/${s.payment_intent}`, order.id, { overwrite: true }).catch((e) => console.error("[stripe] značka platby selhala", e));
  await sendDelivery(paid).catch((e) => console.error("[stripe] doručovací e-mail selhal", paid.vs, e));
  await notifyOwner(`Zaplaceno kartou ${paid.amount} Kč${paid.test ? " (test)" : ""}`, [
    `Objednávka ${paid.vs}: ${paid.name}, ${paid.email}`,
    `Stripe platba ${s.id}. Výplata ze Stripe přijde na bankovní účet podle nastavení Stripe.`,
  ]).catch((e) => console.error("[stripe] upozornění selhalo", e));
  return Response.json({ ok: true, paid: paid.vs });
}
