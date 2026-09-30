import { after } from "next/server";
import { sendPaymentInstructions } from "@/lib/email";
import { SALES_OPEN, TEST_PRICE, isInternalHost } from "@/lib/config";
import { createOrder } from "@/lib/orders";
import { allow, dayWindow, hourWindow } from "@/lib/ratelimit";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function POST(req: Request) {
  const test = isInternalHost(req.headers.get("host"));
  if (!SALES_OPEN && !test) return Response.json({ error: "Prodej jsme ještě nespustili." }, { status: 403 });
  const body = await req.json().catch(() => null);
  if (!body) return Response.json({ error: "Neplatný požadavek." }, { status: 400 });

  const email = String(body.email ?? "").trim().toLowerCase();
  const name = String(body.name ?? "").trim().slice(0, 120);
  if (body.website) return Response.json({ error: "Neplatný požadavek." }, { status: 400 }); // honeypot
  if (!EMAIL_RE.test(email) || email.length > 200) return Response.json({ error: "Zkontrolujte prosím e-mail." }, { status: 400 });
  if (!name) return Response.json({ error: "Vyplňte prosím jméno." }, { status: 400 });
  if (body.terms !== true) return Response.json({ error: "Bez souhlasu s obchodními podmínkami to nepůjde." }, { status: 400 });

  // Ochrana proti spamu: max 5 objednávek za hodinu z jedné IP a 3 denně na jeden e-mail.
  const ip = req.headers.get("x-real-ip") ?? req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";
  if (!(await allow("ip", ip, 5, hourWindow())) || !(await allow("email", email, 3, dayWindow()))) {
    return Response.json({ error: "Objednávek je teď nějak moc. Zkuste to prosím později, nebo nám napište." }, { status: 429 });
  }

  const order = await createOrder({
    email,
    name,
    marketing: body.marketing === true,
    ...(test ? { test: true, amount: TEST_PRICE } : {}),
  });
  after(() => sendPaymentInstructions(order).catch((e) => console.error("[orders] e-mail s platbou selhal", order.vs, e)));
  return Response.json({ id: order.id });
}
