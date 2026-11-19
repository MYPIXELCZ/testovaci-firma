import type { Metadata } from "next";
import { cookies } from "next/headers";
import OwnerOverview from "@/components/OwnerOverview";
import { SPRAVA_COOKIE, readSprava } from "@/lib/sprava";

export const metadata: Metadata = { title: "Správa", robots: { index: false, follow: false } };
export const dynamic = "force-dynamic";

/** Správa na printopia.cz: přihlášení jen přes Klíčenku z Project Trackeru. */
export default async function Sprava() {
  const s = await readSprava((await cookies()).get(SPRAVA_COOKIE)?.value).catch(() => null);
  if (!s) {
    return (
      <section className="hero">
        <div className="wrap narrow">
          <h1>Správa Printopie</h1>
          <p className="muted" id="sprava-stav">Nejste přihlášeni. Přihlaste se přes Klíčenku v Project Trackeru.</p>
        </div>
      </section>
    );
  }
  return (
    <OwnerOverview
      who={
        <form action="/sprava/odhlasit" method="post" className="muted" id="sprava-stav">
          Přihlášen: {s.email}
          {s.act?.email && s.act.email !== s.email ? ` (přes Klíčenku: ${s.act.name ?? s.act.email})` : ""}{" "}
          <button type="submit" className="btn btn-ghost">Odhlásit</button>
        </form>
      }
    />
  );
}
