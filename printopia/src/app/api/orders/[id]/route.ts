import { getOrder } from "@/lib/orders";

export async function GET(_req: Request, ctx: RouteContext<"/api/orders/[id]">) {
  const { id } = await ctx.params;
  const order = await getOrder(id);
  if (!order) return Response.json({ error: "Objednávka nenalezena." }, { status: 404 });
  return Response.json({ status: order.status }, { headers: { "Cache-Control": "no-store" } });
}
