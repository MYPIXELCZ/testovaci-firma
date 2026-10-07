import { after } from "next/server";
import { notifyOwner, sendWithdrawalReceipt } from "@/lib/email";
import { listOrders } from "@/lib/orders";
import { allow, dayWindow, hourWindow } from "@/lib/ratelimit";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  if (!body) return Response.json({ error: "Neplatný požadavek." }, { status: 400 });
  if (body.website) return Response.json({ error: "Neplatný požadavek." }, { status: 400 }); // honeypot

  const email = String(body.email ?? "").trim().toLowerCase();
  const name = String(body.name ?? "").trim().slice(0, 120);
  const vs = String(body.vs ?? "").trim().replace(/\s/g, "").slice(0, 20);
  if (!EMAIL_RE.test(email) || email.length > 200) return Response.json({ error: "Zkontrolujte prosím e-mail." }, { status: 400 });
  if (!name || !vs) return Response.json({ error: "Vyplňte prosím jméno a číslo objednávky." }, { status: 400 });

  const ip = req.headers.get("x-real-ip") ?? req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";
  if (!(await allow("wd-ip", ip, 5, hourWindow())) || !(await allow("wd-email", email, 3, dayWindow()))) {
    return Response.json({ error: "Odstoupení se nepodařilo odeslat. Napište nám prosím na e-mail printopia@mypixel.cz." }, { status: 429 });
  }

  const sentAt = new Date();
  const order = (await listOrders()).find((o) => o.vs === vs) ?? null;
  const matched = !!order && order.email === email;
  after(async () => {
    await sendWithdrawalReceipt({ name, email, vs, sentAt }).catch((e) => console.error("[odstoupeni] potvrzení zákazníkovi selhalo", vs, e));
    await notifyOwner("Odstoupení od smlouvy", [
      `Odstoupení od smlouvy přes formulář: ${name}, ${email}, objednávka ${vs}, ${sentAt.toISOString()}.`,
      order
        ? `Objednávka nalezena (${order.status === "paid" ? "zaplacená" : "nezaplacená"}, ${order.amount} Kč), e-mail ${matched ? "souhlasí" : "NESOUHLASÍ s objednávkou"}.`
        : "Objednávka s tímto číslem nenalezena (ověřit ručně).",
      order?.status === "paid" ? `Vrátit ${order.amount} Kč z Fio na účet, ze kterého přišla platba, nejpozději do 14 dnů od ${sentAt.toISOString().slice(0, 10)}.` : "Nic k vrácení, pokud nebyla platba přijata.",
    ]).catch((e) => console.error("[odstoupeni] upozornění pro firmu selhalo", vs, e));
  });
  return Response.json({ ok: true });
}
