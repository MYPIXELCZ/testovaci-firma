import "server-only";
import { SignJWT, jwtVerify } from "jose";
import { createJtiStore } from "@mypixel/klicenka";
import { storage } from "./storage";

/**
 * Správa anoberu na anoberu.cz/nastaveni: přihlášení jen přes Klíčenku z Project Trackeru (passkey),
 * heslo tu žádné není. Účty, které se smí přihlásit, jsou v env SPRAVA_UCTY (e-maily oddělené čárkou),
 * session podepisuje SESSION_SECRET (sensitive). Bez nich se nikdo nepřihlásí.
 */
export const SPRAVA_COOKIE = "anoberu_sprava";

const secret = () => {
  const s = process.env.SESSION_SECRET;
  if (!s || s.length < 32) throw new Error("SESSION_SECRET chybí nebo je krátký");
  return new TextEncoder().encode(s);
};

export type Admin = { email: string };
export type Act = { sub?: string; name?: string | null; email?: string | null } | undefined;

export function findAdmin(sub: string): Admin | null {
  const allowed = (process.env.SPRAVA_UCTY ?? "").split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
  const email = sub.trim().toLowerCase();
  return allowed.includes(email) ? { email } : null;
}

export async function createSprava(admin: Admin, maxAgeSeconds: number, act: Act) {
  return new SignJWT({ email: admin.email, act: act ? { name: act.name ?? null, email: act.email ?? null } : undefined })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(admin.email)
    .setIssuedAt()
    .setExpirationTime(`${maxAgeSeconds}s`)
    .sign(secret());
}

export async function readSprava(token: string | undefined) {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, secret(), { algorithms: ["HS256"] });
    // Účet mohl být mezitím odebrán z SPRAVA_UCTY: platí jen dokud je na seznamu.
    if (typeof payload.email !== "string" || !findAdmin(payload.email)) return null;
    return payload as { email: string; act?: { name: string | null; email: string | null } };
  } catch {
    return null;
  }
}

/** Použitá jti (jednorázovost tokenu) ve sdíleném úložišti: zápis bez přepisu selže, když už jti existuje. */
export const jtiStore = createJtiStore({
  insert: (jti, expiresAt) =>
    storage.write(`klicenka-jti/${encodeURIComponent(jti)}`, expiresAt.toISOString(), { overwrite: false }).then(() => true),
  cleanup: async (now) => {
    const old = (await storage.list("klicenka-jti/")).filter((i) => now.getTime() - i.uploadedAt.getTime() > 86_400_000);
    if (old.length) await storage.remove(old.map((i) => i.pathname));
  },
  isDuplicate: (e) => {
    const err = e as { code?: string; message?: string } | null;
    return err?.code === "EEXIST" || /already exists/i.test(err?.message ?? "");
  },
});
