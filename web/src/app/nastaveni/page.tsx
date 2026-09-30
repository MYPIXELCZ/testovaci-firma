import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { listOrders } from "@/lib/orders";
import { getSecret, isAdminRequest } from "@/lib/secrets";
import { saveFioToken, saveResendKey } from "./actions";
import SecretForm from "./SecretForm";

export const metadata: Metadata = { title: "Nastavení", robots: { index: false } };

export default async function SettingsPage() {
  if (!(await isAdminRequest())) notFound();
  const [fio, resend, orders] = await Promise.all([getSecret("FIO_TOKEN"), getSecret("RESEND_API_KEY"), listOrders()]);
  const real = orders.filter((o) => !o.test);
  const paid = real.filter((o) => o.status === "paid");
  const month = new Date().toISOString().slice(0, 7);
  const paidMonth = paid.filter((o) => o.paidAt?.startsWith(month));
  const sum = (list: typeof paid) => list.reduce((s, o) => s + o.amount, 0).toLocaleString("cs-CZ") + " Kč";
  const recent = [...orders].sort((a, b) => b.createdAt.localeCompare(a.createdAt)).slice(0, 10);

  return (
    <section>
      <div className="wrap narrow">
        <h1 style={{ fontSize: "2.2rem" }}>Nastavení</h1>

        <h2 style={{ fontSize: "1.4rem" }}>Prodeje</h2>
        <div className="grid-2" style={{ marginBottom: 16 }}>
          <div className="card"><h3>{paidMonth.length} × {sum(paidMonth)}</h3><p>zaplaceno tento měsíc</p></div>
          <div className="card"><h3>{paid.length} × {sum(paid)}</h3><p>zaplaceno celkem</p></div>
          <div className="card"><h3>{real.filter((o) => o.status === "pending").length}</h3><p>čeká na platbu (mažou se po 30 dnech)</p></div>
          <div className="card"><h3>{real.length ? Math.round((paid.length / real.length) * 100) : 0} %</h3><p>objednávek zaplaceno</p></div>
        </div>
        {recent.length > 0 && (
          <table className="data-table" style={{ marginBottom: 40 }}>
            <thead><tr><th>VS</th><th>Vytvořeno</th><th>Kupující</th><th>Stav</th><th className="num">Kč</th></tr></thead>
            <tbody>
              {recent.map((o) => (
                <tr key={o.id}>
                  <td>{o.vs}</td>
                  <td>{new Date(o.createdAt).toLocaleDateString("cs-CZ")}</td>
                  <td>{o.name}<br /><span className="muted small">{o.email}</span></td>
                  <td>{o.status === "paid" ? "zaplaceno" : "čeká"}{o.test ? " (test)" : ""}</td>
                  <td className="num">{o.amount}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <h2 style={{ fontSize: "1.4rem" }}>Klíče</h2>
        <p className="muted">Tokeny se uloží do privátního úložiště projektu. Nikde se nezobrazují a stránka je dostupná jen členům týmu.</p>
        <SecretForm
          label="Token Fio API"
          hint="Fio internetbanking → Nastavení → API → Přidat token, účet 2202343801, oprávnění „Pouze sledovat účet“. Po uložení ho hned ověřím u banky."
          isSet={Boolean(fio)}
          action={saveFioToken}
        />
        <SecretForm
          label="Klíč Resend (e-maily)"
          hint="resend.com → API Keys → Create API Key (Sending access). Začíná „re_“."
          isSet={Boolean(resend)}
          action={saveResendKey}
        />
      </div>
    </section>
  );
}
