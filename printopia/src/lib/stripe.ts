import "server-only";
import { createHmac, timingSafeEqual } from "node:crypto";
import { PRODUCT, SITE_URL } from "./config";
import type { Order } from "./orders";

const API = process.env.STRIPE_API_URL ?? "https://api.stripe.com";

/** Stripe v korunách přijímá platby od 15 Kč. Testovací objednávky (1 Kč, jen chráněná adresa týmu) se kartou účtují 15 Kč, skutečné beze změny. */
export const stripeAmountCzk = (order: Pick<Order, "amount" | "test">) => (order.test ? Math.max(order.amount, 15) : order.amount);

/** Stripe Checkout (hostovaná platební stránka: karta, Apple Pay, Google Pay). Částka je vždy z objednávky, ne z prohlížeče. */
export async function createCheckoutSession(order: Order): Promise<{ id: string; url: string }> {
  const params = new URLSearchParams({
    mode: "payment",
    locale: "cs",
    "line_items[0][quantity]": "1",
    "line_items[0][price_data][currency]": "czk",
    "line_items[0][price_data][unit_amount]": String(stripeAmountCzk(order) * 100),
    "line_items[0][price_data][product_data][name]": PRODUCT.name,
    client_reference_id: order.id,
    customer_email: order.email,
    "metadata[vs]": order.vs,
    "metadata[order_id]": order.id,
    "payment_intent_data[metadata][vs]": order.vs,
    "payment_intent_data[metadata][order_id]": order.id,
    success_url: `${SITE_URL}/objednavka/${order.id}?karta=ok`,
    cancel_url: `${SITE_URL}/objednavka/${order.id}`,
  });
  const res = await fetch(`${API}/v1/checkout/sessions`, {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`, "Content-Type": "application/x-www-form-urlencoded" },
    body: params,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.url) throw new Error(`Stripe odpověděl ${res.status}: ${data?.error?.message ?? "bez adresy platby"}`);
  return { id: data.id, url: data.url };
}

/** Ověří podpis webhooku (hlavička Stripe-Signature: t=…,v1=…, HMAC SHA-256 z „t.tělo“, tolerance 5 minut). */
export function verifyWebhook(raw: string, header: string | null): boolean {
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!secret || !header) return false;
  const parts = Object.fromEntries(header.split(",").map((kv) => kv.split("=") as [string, string]));
  const t = parts.t;
  if (!t || Math.abs(Date.now() / 1000 - Number(t)) > 300) return false;
  const expected = createHmac("sha256", secret).update(`${t}.${raw}`).digest();
  return header.split(",").filter((kv) => kv.startsWith("v1=")).some((kv) => {
    const got = Buffer.from(kv.slice(3), "hex");
    return got.length === expected.length && timingSafeEqual(got, expected);
  });
}
