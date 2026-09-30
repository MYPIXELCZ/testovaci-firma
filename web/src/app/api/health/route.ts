import { INDEXING, SALES_OPEN } from "@/lib/config";
import { storage } from "@/lib/storage";

/** Stav provozu. Podrobnosti jen na *.vercel.app (chráněné Vercel Authentication), veřejně jen ok/nok. */
export async function GET(req: Request) {
  let store = "ok";
  try {
    await storage.list("pending/");
  } catch (e) {
    store = e instanceof Error ? e.message : String(e);
  }
  const internal = (req.headers.get("host") ?? "").endsWith(".vercel.app");
  const body = internal
    ? {
        storage: store,
        fioToken: Boolean(process.env.FIO_TOKEN),
        resendKey: Boolean(process.env.RESEND_API_KEY),
        cronSecret: Boolean(process.env.CRON_SECRET),
        salesOpen: SALES_OPEN,
        indexing: INDEXING,
      }
    : { ok: store === "ok" };
  return Response.json(body, { headers: { "Cache-Control": "no-store" } });
}
