import { createHash } from "node:crypto";
import { after } from "next/server";
import { storage } from "@/lib/storage";
import { track } from "@/lib/track";

const SOURCES = ["ukazka", "koupit"] as const;
type Source = (typeof SOURCES)[number];
const ROLES = ["rodic", "zak", "ucitel"] as const;
type Role = (typeof ROLES)[number];
type Lead = { email: string; sources: Source[]; role: Role; firstAt: string; lastAt: string; src: string };

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function POST(req: Request) {
  const body = (await req.json().catch(() => null)) as Record<string, unknown> | null;
  if (!body) return Response.json({ error: "Neplatný požadavek." }, { status: 400 });
  // Honeypot: roboti vyplní i skryté pole. Tváříme se, že je vše v pořádku.
  if (typeof body.website === "string" && body.website) return Response.json({ ok: true });

  const email = String(body.email ?? "").trim().toLowerCase();
  const source = String(body.source ?? "") as Source;
  const src = String(body.src ?? "").slice(0, 40).replace(/[^\w.-]/g, "");
  if (!EMAIL.test(email) || email.length > 200) return Response.json({ error: "Zkontrolujte prosím e-mail." }, { status: 400 });
  if (body.consent !== true) return Response.json({ error: "Bez souhlasu vám nemůžeme nic poslat." }, { status: 400 });
  // Role měří, kdo kupuje; souhlas může dítě v ČR dát samo až od 15 let, proto jiné volby nejsou.
  const role = String(body.role ?? "") as Role;
  if (!ROLES.includes(role)) return Response.json({ error: "Vyberte prosím, kdo formulář vyplňuje." }, { status: 400 });
  if (!SOURCES.includes(source)) return Response.json({ error: "Neplatný požadavek." }, { status: 400 });

  const key = `leads/${createHash("sha256").update(email).digest("hex").slice(0, 32)}.json`;
  const now = new Date().toISOString();
  const prev = await storage.read(key).then((s) => (s ? (JSON.parse(s) as Lead) : null));
  const lead: Lead = prev
    ? { ...prev, sources: [...new Set([...prev.sources, source])], role, lastAt: now }
    : { email, sources: [source], role, firstAt: now, lastAt: now, src };
  await storage.write(key, JSON.stringify(lead), { overwrite: true });
  const ua = req.headers.get("user-agent");
  if (!prev) after(() => track("lead", src, ua, { source, role }));
  return Response.json({ ok: true, download: source === "ukazka" ? "/ukazka-zlomky.pdf" : null });
}
