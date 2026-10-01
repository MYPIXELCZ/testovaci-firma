import "server-only";
import { createHash } from "node:crypto";
import { storage } from "./storage";

// Jednoduché počítadlo v úložišti (bez atomicity, pro náš objem stačí). Klíče jsou hashované (GDPR).
const hash = (s: string) => createHash("sha256").update(`printopia:${s}`).digest("hex").slice(0, 24);

/** Vrátí true, pokud je v okně ještě místo, a zároveň pokus započítá. */
export async function allow(kind: string, subject: string, limit: number, windowId: string) {
  const path = `ratelimit/${windowId}/${kind}-${hash(subject)}`;
  const count = Number((await storage.read(path)) ?? 0);
  if (count >= limit) return false;
  await storage.write(path, String(count + 1), { overwrite: true });
  return true;
}

export const hourWindow = () => new Date().toISOString().slice(0, 13).replace(/[-T]/g, ""); // RRRRMMDDHH
export const dayWindow = () => new Date().toISOString().slice(0, 10).replaceAll("-", ""); // RRRRMMDD

/** Smaže počítadla starší než 2 dny (volá cron). */
export async function cleanupRateLimits() {
  const keep = new Set([0, 1, 2].map((d) => new Date(Date.now() - d * 86_400_000).toISOString().slice(0, 10).replaceAll("-", "")));
  const old = (await storage.list("ratelimit/")).filter((i) => !keep.has(i.pathname.split("/")[1].slice(0, 8)));
  if (old.length) await storage.remove(old.map((i) => i.pathname));
  return old.length;
}
