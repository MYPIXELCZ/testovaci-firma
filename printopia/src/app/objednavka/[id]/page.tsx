import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CONTACT, PAYMENT, PRODUCT, cardOffered as cardOfferedFor } from "@/lib/config";
import { FILES } from "@/content/sada";
import { getOrder } from "@/lib/orders";
import CardPay from "@/components/CardPay";
import CopyButton from "@/components/CopyButton";
import Icon from "@/components/Icon";
import TransferPanel from "@/components/TransferPanel";
import { headers } from "next/headers";
import { paymentConfigured, qrSvg } from "@/lib/payment";
import WaitForPayment from "./WaitForPayment";

export const metadata: Metadata = { title: "Vaše objednávka", robots: { index: false } };

export default async function OrderStatusPage(props: PageProps<"/objednavka/[id]">) {
  const { id } = await props.params;
  const afterCard = (await props.searchParams).karta === "ok";
  const cardOffered = cardOfferedFor((await headers()).get("host"));
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
  const bank = ready ? (
    <div className="pay">
      <div className="qr" dangerouslySetInnerHTML={{ __html: await qrSvg(order) }} aria-label="QR kód pro platbu" />
      <div>
        <p className="muted small" style={{ marginTop: 0 }}>Naskenujte QR kód v bankovní aplikaci. Z telefonu zkopírujte údaje níže, nebo QR kód uložte jako obrázek a načtěte ho z galerie (většina bankovních aplikací to umí).</p>
        <table className="pay-table">
          <tbody>
            <tr><td>Číslo účtu</td><td>{PAYMENT.account} <CopyButton value={PAYMENT.account} label="číslo účtu" /></td></tr>
            <tr><td>Částka</td><td>{order.amount} Kč <CopyButton value={String(order.amount)} label="částku" /></td></tr>
            <tr><td>Variabilní symbol</td><td>{order.vs} <CopyButton value={order.vs} label="variabilní symbol" /></td></tr>
          </tbody>
        </table>
        <p className="muted small">Platby párujeme automaticky každých pár minut, u okamžité platby sadu pošleme obvykle do 10 minut. Stránku můžete zavřít, vše vám přijde e-mailem na {order.email}.</p>
      </div>
    </div>
  ) : (
    <p className="error">Platby teď nepřijímáme. Napište nám prosím na {CONTACT}.</p>
  );

  return (
    <section className="hero">
      <div className="wrap narrow checkout">
        <p className="eyebrow">Objednávka {order.vs}</p>
        <h1>Dokončete objednávku</h1>
        <div className="summary">
          <span>
            {PRODUCT.name}
            <br />
            <span className="muted small">{FILES.length} pracovních listů v PDF k tisku, ke stažení hned po zaplacení</span>
          </span>
          <strong>{order.amount} Kč</strong>
        </div>
        {afterCard ? (
          <div className="pay-card" role="status">
            <h2>Děkujeme, platbu kartou zpracováváme</h2>
            <p className="muted">Stránka se za chvíli sama obnoví a sadu pošleme i e-mailem na {order.email}.</p>
            <p><WaitForPayment id={order.id} fast /></p>
          </div>
        ) : cardOffered ? (
          <>
            <div className="pay-card">
              <h2>Rychlá platba online</h2>
              <CardPay id={order.id} />
              <p className="secure small"><Icon name="lock" /> Platba je zabezpečená, zpracovává ji Stripe. Údaje o kartě nevidíme. Sadu dostanete okamžitě.</p>
            </div>
            <p className="or"><span>nebo</span></p>
            <TransferPanel id={order.id} notifyOnOpen>{bank}</TransferPanel>
            <p style={{ marginTop: 16 }}><WaitForPayment id={order.id} /></p>
          </>
        ) : (
          <>
            {bank}
            <p style={{ marginTop: 16 }}><WaitForPayment id={order.id} /></p>
          </>
        )}
      </div>
    </section>
  );
}
