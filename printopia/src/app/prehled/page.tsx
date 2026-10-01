import type { Metadata } from "next";
import { headers } from "next/headers";
import { notFound } from "next/navigation";
import { isInternalHost } from "@/lib/config";
import { listOrders } from "@/lib/orders";
import { computeStats } from "@/lib/stats";

export const metadata: Metadata = { title: "Přehled", robots: { index: false } };
export const dynamic = "force-dynamic";

const STEP_LABEL: Record<string, string> = {
  view: "Zobrazení stránky", t10: "Zůstali aspoň 10 s", t30: "Zůstali aspoň 30 s", scroll50: "Dočetli do poloviny",
  scroll100: "Dočetli do konce", cta_sample: "Klik na „8 úloh zdarma“", cta_buy: "Klik na „Koupit“", pdf_download: "Stažení ukázky",
  form_start: "Začali psát e-mail (tipy)", form_submit: "Přihlásili se k tipům", solution_open: "Rozbalili postup", topic_link: "Klik na tematickou stránku",
};
const dayFmt = (d: string) => `${Number(d.slice(8, 10))}. ${Number(d.slice(5, 7))}.`;

/** Přehled pro majitele: jen na chráněné adrese *.vercel.app (Vercel Authentication), na printopia.cz se nezobrazí. */
export default async function Overview() {
  if (!isInternalHost((await headers()).get("host"))) notFound();
  const st = await computeStats();
  const orders = await listOrders();
  const home = st.funnel.byPage.home;
  const today = new Date().toISOString().slice(0, 10);
  const visitsTotal = Object.values(st.server.visits).reduce((a, b) => a + b, 0);
  const paid = orders.filter((o) => o.status === "paid" && !o.test);
  const days = Object.entries(st.server.visitsByDay).sort().slice(-14);

  return (
    <section className="hero">
      <div className="wrap narrow">
        <p className="eyebrow">Jen pro majitele</p>
        <h1>Přehled Printopie</h1>
        <p className="muted">Návštěvy se počítají bez robotů a bez osobních údajů. Čas je UTC (v Praze +2 h).</p>

        <h2>Návštěvnost</h2>
        <table className="pay-table">
          <tbody>
            <tr><td>Dnes ({dayFmt(today)})</td><td>{st.server.visitsByDay[today] ?? 0}</td></tr>
            <tr><td>Celkem od spuštění</td><td>{visitsTotal}</td></tr>
            <tr><td>Podle zdroje</td><td>{Object.entries(st.server.visits).map(([k, v]) => `${k === "direct" ? "přímo / vyhledávač" : k}: ${v}`).join(", ") || "zatím nic"}</td></tr>
            <tr><td>Posledních 14 dní</td><td>{days.map(([d, v]) => `${dayFmt(d)}: ${v}`).join(" · ") || "zatím nic"}</td></tr>
          </tbody>
        </table>
        <p className="small muted">Počítá se vstup na úvodní stránku. Vstupy na tematické stránky ukazuje trychtýř níže (sloupec Zobrazení).</p>

        <h2>Prodej</h2>
        <table className="pay-table">
          <tbody>
            <tr><td>Zaplacené objednávky</td><td>{paid.length} ({paid.reduce((a, o) => a + o.amount, 0)} Kč)</td></tr>
            <tr><td>Vytvořené a zatím nezaplacené</td><td>{orders.filter((o) => o.status === "pending" && !o.test).length}</td></tr>
            <tr><td>Kliky na Koupit</td><td>{Object.values(st.server.buyClicks).reduce((a, b) => a + b, 0)}</td></tr>
            <tr><td>Tipy e-mailem (souhlas)</td><td>{st.server.leads}</td></tr>
          </tbody>
        </table>

        <h2>Co lidé na úvodní stránce dělají</h2>
        <table className="pay-table">
          <tbody>
            {Object.entries(STEP_LABEL).map(([k, label]) => (
              <tr key={k}><td>{label}</td><td>{(home as Record<string, number> | undefined)?.[k] ?? 0}</td></tr>
            ))}
          </tbody>
        </table>

        <h2>Tematické stránky a objednávka</h2>
        <table className="pay-table">
          <tbody>
            {Object.entries(st.funnel.byPage).filter(([k]) => k !== "home").map(([k, f]) => (
              <tr key={k}><td>{k === "tema" ? "Tematické stránky (zlomky, tělesa…)" : k === "koupit" ? "Objednávka" : k}</td><td>{f.view} zobrazení</td></tr>
            ))}
          </tbody>
        </table>

        {(Object.keys(st.sklik.byKeyword).length > 0 || Object.keys(st.sklik.byAd).length > 0) && (
          <>
            <h2>Reklama Sklik</h2>
            <p>Podle klíčového slova: {Object.entries(st.sklik.byKeyword).map(([k, v]) => `${k}: ${v}`).join(", ")}</p>
            <p>Podle reklamy: {Object.entries(st.sklik.byAd).map(([k, v]) => `${k}: ${v}`).join(", ")}</p>
          </>
        )}

        <h2>Proč nekupují (anketa)</h2>
        {Object.keys(st.feedback).length ? (
          <ul>{Object.entries(st.feedback).map(([k, v]) => <li key={k}>{k}: {v}×</li>)}</ul>
        ) : <p className="muted">Zatím nikdo neodpověděl.</p>}
        {st.feedbackTexts.length > 0 && <ul>{st.feedbackTexts.map((t) => <li key={t}>{t}</li>)}</ul>}

        <h2>Závěry</h2>
        <ul>{st.findings.map((f) => <li key={f}>{f}</li>)}</ul>
      </div>
    </section>
  );
}
