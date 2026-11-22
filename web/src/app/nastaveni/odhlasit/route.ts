import { SPRAVA_COOKIE } from "@/lib/sprava";

/** Odhlášení ze správy anoberu: smaže cookie a vrátí na úvod. */
export async function POST() {
  const secure = process.env.NODE_ENV === "production" ? "; Secure" : "";
  return new Response(null, {
    status: 303,
    headers: { Location: "/", "Set-Cookie": `${SPRAVA_COOKIE}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax${secure}`, "Cache-Control": "no-store" },
  });
}
