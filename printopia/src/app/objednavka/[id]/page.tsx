import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CONTACT, PAYMENT } from "@/lib/config";
import { FILES } from "@/content/sada";
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
      <section className="hero">
        <div className="wrap narrow">
          <p className="eyebrow">Objednávka {order.vs}</p>
          <h1>Zaplaceno, děkujeme!</h1>
          <p>Odkaz na tuto stránku jsme poslali i na <strong>{order.email}</strong>. Pracovní listy si můžete stáhnout kdykoli znovu.</p>
          <h2>Jak začít</h2>
          <ol>
            <li>Vytiskněte <strong>úvodní test</strong> a nechte dítě spočítat ho bez nápovědy. Vyhodnocení ukáže, která témata procvičit nejdřív.</li>
            <li>Podle <strong>plánu procvičování</strong> berte jedno téma týdně. Každý list začíná řešeným příkladem.</li>
            <li>Postupy a výsledky jsou až na konci listu. Kontrolujte je až po spočítání.</li>
          </ol>
          <h2>Ke stažení</h2>
          <ul className="downloads">
            {FILES.map((f) => (
              <li key={f.slug}>
                <a href={`/stahnout/${order.id}?soubor=${f.slug}`} data-track="pdf_download">{f.title}</a>
                <span className="muted small">{f.desc}</span>
              </li>
            ))}
          </ul>
          <p><Link className="btn btn-ghost" href={`/doklad/${order.id}`}>Doklad o zaplacení</Link></p>
        </div>
      </section>
    );
  }

  const ready = paymentConfigured();
  return (
    <section className="hero">
      <div className="wrap narrow">
        <p className="eyebrow">Objednávka {order.vs}</p>
        <h1>Zbývá zaplatit</h1>
        <p className="muted">Naskenujte QR kód v bankovní aplikaci. Odkaz ke stažení pošleme na {order.email}, jakmile platba dorazí.</p>
        {ready ? (
          <div className="pay">
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
              <p className="muted small">Platby párujeme automaticky každých pár minut. Stránku můžete zavřít, vše vám přijde e-mailem.</p>
            </div>
          </div>
        ) : (
          <p className="error">Platby teď nepřijímáme. Napište nám prosím na {CONTACT}.</p>
        )}
      </div>
    </section>
  );
}
