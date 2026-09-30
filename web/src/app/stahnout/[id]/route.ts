import { readFile } from "node:fs/promises";
import path from "node:path";
import { PRODUCT } from "@/lib/config";
import { getOrder } from "@/lib/orders";

export async function GET(req: Request, ctx: RouteContext<"/stahnout/[id]">) {
  const { id } = await ctx.params;
  const order = await getOrder(id);
  if (!order) return new Response("Objednávka nenalezena.", { status: 404 });
  if (order.status !== "paid") return Response.redirect(new URL(`/objednavka/${id}`, req.url), 303);

  const file = await readFile(path.join(process.cwd(), "private", PRODUCT.file));
  return new Response(file, {
    headers: {
      "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "Content-Disposition": `attachment; filename="${PRODUCT.file}"`,
      "Cache-Control": "private, no-store",
    },
  });
}
