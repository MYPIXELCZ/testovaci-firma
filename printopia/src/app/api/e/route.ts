import { isBot } from "@/lib/track";
import { EVENTS, FEEDBACK, PAGES, type Event, type FeedbackKey, type Page } from "@/lib/metrics";
import { storage } from "@/lib/storage";

// Příjem anonymních událostí z Beacon.tsx. Klíč v úložišti nese vše potřebné pro souhrn,
// aby se při vyhodnocení nemusel číst každý soubor: beacons/{den}/{page}/{src}/{zařízení}/{pv}/{ev}~{volba}~{náhoda}
const UUID = /^[0-9a-f-]{36}$/;
const clean = (v: unknown, n = 40) => String(v ?? "").slice(0, n).replace(/[^\w.-]/g, "");

function device(ua: string) {
  if (/ipad|tablet/i.test(ua)) return "tablet";
  return /mobi|android|iphone/i.test(ua) ? "mobil" : "pocitac";
}

export async function POST(req: Request) {
  const ua = req.headers.get("user-agent");
  if (isBot(ua)) return new Response(null, { status: 204 });
  const b = (await req.json().catch(() => null)) as Record<string, unknown> | null;
  if (!b || !UUID.test(String(b.pv)) || !PAGES.includes(b.page as Page) || !EVENTS.includes(b.ev as Event))
    return new Response(null, { status: 400 });
  const choice = b.ev === "feedback" ? String(b.choice ?? "") : "";
  if (b.ev === "feedback" && !(choice in FEEDBACK)) return new Response(null, { status: 400 });

  const day = new Date().toISOString().slice(0, 10);
  const page = b.page === "tema" && b.topic ? `tema-${clean(b.topic)}` : String(b.page);
  const key = `beacons/${day}/${page}/${clean(b.src) || "direct"}/${device(ua!)}/${b.pv}/${b.ev}~${choice as FeedbackKey | ""}~${Math.random().toString(36).slice(2, 8)}.json`;
  const body = b.ev === "feedback" ? { text: String(b.text ?? "").slice(0, 200) } : b.ev === "view" ? { ref: clean(b.ref, 80) } : {};
  await storage.write(key, JSON.stringify(body), { overwrite: false });
  return new Response(null, { status: 204 });
}
