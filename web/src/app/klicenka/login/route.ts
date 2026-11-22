import { redirectWithCookie } from "@mypixel/klicenka";
import { klicenkaLogin } from "@mypixel/klicenka/next";
import { SPRAVA_COOKIE, createSprava, findAdmin, jtiStore } from "@/lib/sprava";

// Přihlášení z Project Trackeru (Klíčenka): ověří podpis, adresáta, prostředí a jednorázovost a přihlásí přesně účet ze `sub`.
export const POST = klicenkaLogin({
  issuer: process.env.KLICENKA_ISSUER ?? "https://tracker.mypixel.cz",
  audience: process.env.KLICENKA_AUDIENCE ?? "anoberu",
  environment: (process.env.KLICENKA_ENVIRONMENT ?? "production") as "production" | "preview",
  jtiStore,
  findAccount: async (sub) => findAdmin(sub),
  startSession: async ({ user, claims, maxAgeSeconds }) =>
    redirectWithCookie("/nastaveni", {
      name: SPRAVA_COOKIE,
      value: await createSprava(user, maxAgeSeconds, claims.act),
      maxAgeSeconds,
      secure: process.env.NODE_ENV === "production",
    }),
  log: (e) => console.info("[klicenka]", JSON.stringify(e)),
});
