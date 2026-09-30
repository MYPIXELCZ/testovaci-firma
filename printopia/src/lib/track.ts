import "server-only";
import { storage } from "@/lib/storage";

// Události testu poptávky ukládáme do úložiště: logy Vercelu drží data jen krátce, test běží 14 dní.
// Bez osobních údajů (žádná IP, žádný user-agent), roboty nepočítáme.
const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|curl|wget|python|node-fetch|headless|lighthouse|seznam/i;
export type Ev = "visit" | "buy_click" | "lead";

export function isBot(ua: string | null) {
  return !ua || BOT.test(ua);
}

export async function track(ev: Ev, src: string, ua: string | null, extra: Record<string, string> = {}) {
  console.log(JSON.stringify({ ev, src, ...extra }));
  if (isBot(ua)) return;
  const day = new Date().toISOString().slice(0, 10);
  const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const path = `events/${day}/${ev}/${src || "direct"}/${id}.json`;
  await storage.write(path, JSON.stringify(extra), { overwrite: false }).catch((e) => console.error("track", e));
}
