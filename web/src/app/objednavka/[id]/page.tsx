import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { COMPANY, PAYMENT } from "@/lib/config";
import { getOrder } from "@/lib/orders";
import { paymentConfigured, qrSvg } from "@/lib/payment";
import WaitForPayment from "./WaitForPayment";

export const metadata: Metadata = { title: "Vaše objednávka", robots: { index: false } };

export default async function OrderStatusPage(props: PageProps<"/objednavka/[id]">) {
  const { id } = await props.params;
  const order = await getOrder(id);
  if (!order) notFound();

  if (order.status === "paid") {
    return (
      <section>
        <div className="wrap narrow">
          <p className="eyebrow">Objednávka {order.vs}</p>
          <h1>Zaplaceno, děkujeme!</h1>
          <p>Plánovač jsme poslali i na <strong>{order.email}</strong>. Hodně štěstí s přípravami.</p>
          <p style={{ display: "flex", gap: 16, flexWrap: "wrap", marginTop: 28 }}>
            <a className="btn" href={`/stahnout/${order.id}`}>Stáhnout plánovač</a>
            <Link className="btn btn-ghost" href={`/doklad/${order.id}`}>Doklad o zaplacení</Link>
          </p>
          <h2 style={{ fontSize: "1.4rem", marginTop: 48 }}>Jak začít</h2>
          <ol>
            <li>Otevřete soubor v Excelu, nebo ho nahrajte na Disk Google a otevřete v Google Tabulkách.</li>
            <li>Na listu Přehled vyplňte jména, datum svatby a rozpočet.</li>
            <li>Termíny úkolů se dopočítají samy. Začněte tím, co svítí nahoře.</li>
          </ol>
        </div>
      </section>
    );
  }

  const ready = paymentConfigured();
  return (
    <section>
      <div className="wrap narrow">
        <p className="eyebrow">Objednávka {order.vs}</p>
        <h1>Zbývá zaplatit</h1>
        <p className="muted">Naskenujte QR kód v bankovní aplikaci. Plánovač vám pošleme na {order.email}, jakmile platba dorazí.</p>
        {ready ? (
          <div className="pay" style={{ marginTop: 32 }}>
            <div className="qr" dangerouslySetInnerHTML={{ __html: await qrSvg(order) }} aria-label="QR kód pro platbu" />
            <div>
              <table className="pay-table">
                <tbody>
                  <tr><td>Číslo účtu</td><td>{PAYMENT.account}</td></tr>
                  <tr><td>Částka</td><td>{order.amount} Kč</td></tr>
                  <tr><td>Variabilní symbol</td><td>{order.vs}</td></tr>
                </tbody>
              </table>
              <p style={{ marginTop: 24 }}><WaitForPayment id={order.id} /></p>
              <p className="muted small">
                Platby párujeme automaticky každých pár minut. Tuto stránku můžete zavřít, vše vám přijde e-mailem.
              </p>
            </div>
          </div>
        ) : (
          <p className="error">Platby teď nepřijímáme. Napište nám prosím na {COMPANY.email}.</p>
        )}
      </div>
    </section>
  );
}
