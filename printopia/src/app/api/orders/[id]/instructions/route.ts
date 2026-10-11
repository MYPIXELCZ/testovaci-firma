import { after } from "next/server";
import { sendPaymentInstructions } from "@/lib/email";
import { getOrder, markInstructionsSent } from "@/lib/orders";
import { allow, hourWindow } from "@/lib/ratelimit";

/** Kupující zvolil bankovní převod: pošleme e-mail s platebními údaji a poučením (jednou). */
export async function POST(req: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  const ip = req.headers.get("x-real-ip") ?? req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";
  if (!(await allow("instr-ip", ip, 20, hourWindow()))) return Response.json({ error: "Zkuste to prosím později." }, { status: 429 });
  const order = await getOrder(id);
  if (!order || order.status !== "pending") return Response.json({ error: "Objednávka nenalezena." }, { status: 404 });
  if (order.instructionsAt) return Response.json({ ok: true, already: true });
  await markInstructionsSent(order);
  after(() => sendPaymentInstructions(order).catch((e) => console.error("[orders] e-mail s platbou selhal", order.vs, e)));
  return Response.json({ ok: true });
}
