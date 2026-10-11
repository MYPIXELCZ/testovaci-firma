import { isInternalHost, stripeEnabled, stripeTestMode } from "@/lib/config";
import { getOrder } from "@/lib/orders";
import { allow, hourWindow } from "@/lib/ratelimit";
import { createCheckoutSession } from "@/lib/stripe";

export async function POST(req: Request) {
  if (!stripeEnabled() || (stripeTestMode() && !isInternalHost(req.headers.get("host")))) return Response.json({ error: "Platba kartou zatím není dostupná." }, { status: 404 });
  const body = await req.json().catch(() => null);
  const id = String(body?.id ?? "");
  const ip = req.headers.get("x-real-ip") ?? req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";
  if (!(await allow("stripe-ip", ip, 20, hourWindow()))) return Response.json({ error: "Zkuste to prosím později." }, { status: 429 });
  const order = id ? await getOrder(id) : null;
  if (!order || order.status !== "pending") return Response.json({ error: "Objednávka nenalezena nebo už je zaplacená." }, { status: 404 });
  try {
    const session = await createCheckoutSession(order);
    return Response.json({ url: session.url });
  } catch (e) {
    console.error("[stripe] vytvoření platby selhalo", order.vs, e);
    return Response.json({ error: "Platbu kartou se nepodařilo otevřít. Zaplaťte prosím převodem." }, { status: 502 });
  }
}
