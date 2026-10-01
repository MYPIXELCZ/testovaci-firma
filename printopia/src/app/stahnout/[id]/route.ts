import { readFile } from "node:fs/promises";
import path from "node:path";
import { FILES } from "@/content/sada";
import { getOrder } from "@/lib/orders";

/** Pracovní listy leží v private/sada/ (ne v public/) a stáhnout je jde jen se zaplacenou objednávkou. */
export async function GET(req: Request, ctx: RouteContext<"/stahnout/[id]">) {
  const { id } = await ctx.params;
  const order = await getOrder(id);
  if (!order) return new Response("Objednávka nenalezena.", { status: 404 });
  if (order.status !== "paid") return Response.redirect(new URL(`/objednavka/${id}`, req.url), 303);

  const f = FILES.find((x) => x.slug === new URL(req.url).searchParams.get("soubor"));
  if (!f) return Response.redirect(new URL(`/objednavka/${id}`, req.url), 303);
  const file = await readFile(path.join(process.cwd(), "private", "sada", f.file));
  return new Response(file, {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": `attachment; filename="${f.file}"`,
      "Cache-Control": "private, no-store",
    },
  });
}
