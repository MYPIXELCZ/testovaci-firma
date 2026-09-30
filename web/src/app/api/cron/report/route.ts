import { sendMonthlyReport } from "@/lib/email";
import { listOrders } from "@/lib/orders";

export const maxDuration = 60;

const csvCell = (v: string | number) => `"${String(v).replaceAll('"', '""')}"`;

/** Vercel Cron 1. dne v měsíci: přehled zaplacených objednávek za minulý měsíc pro účetní. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }
  const url = new URL(req.url);
  const now = new Date();
  const prev = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - 1, 1));
  const month = url.searchParams.get("month") ?? prev.toISOString().slice(0, 7); // RRRR-MM

  const paid = (await listOrders())
    .filter((o) => o.status === "paid" && o.paidAt?.startsWith(month) && !o.test)
    .sort((a, b) => a.paidAt!.localeCompare(b.paidAt!));

  const header = ["Doklad (VS)", "Datum úhrady", "Kupující", "E-mail", "Částka Kč", "Pohyb Fio"];
  const rows = paid.map((o) => [o.vs, o.paidAt!.slice(0, 10), o.name, o.email, o.amount, o.paymentId ?? ""]);
  const csv = [header, ...rows].map((r) => r.map(csvCell).join(";")).join("\r\n");
  const total = paid.reduce((s, o) => s + o.amount, 0);

  await sendMonthlyReport(month, csv, paid.length, total);
  console.log(`[report] ${month}: ${paid.length} objednávek, ${total} Kč`);
  return Response.json({ month, count: paid.length, total });
}
