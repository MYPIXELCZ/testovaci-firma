import type { Metadata } from "next";
import { headers } from "next/headers";
import { COMPANY, PRODUCT, SALES_OPEN, TEST_PRICE, isInternalHost } from "@/lib/config";
import OrderForm from "./OrderForm";

export const metadata: Metadata = { title: "Objednávka", robots: { index: false } };

export default async function OrderPage() {
  const test = isInternalHost((await headers()).get("host"));
  return (
    <section>
      <div className="wrap narrow">
        <h1>Objednávka</h1>
        <div className="summary">
          <span>{PRODUCT.name}<br /><span className="muted small">Digitální soubor pro Excel a Google Tabulky</span></span>
          <strong>{test ? TEST_PRICE : PRODUCT.price} Kč</strong>
        </div>
        {test && <p className="error">Testovací objednávka (jen pro tým): cena {TEST_PRICE} Kč.</p>}
        {SALES_OPEN || test ? (
          <OrderForm />
        ) : (
          <p>
            Prodej spouštíme už brzy. Chcete vědět hned, až to bude? Napište nám na{" "}
            <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a>.
          </p>
        )}
      </div>
    </section>
  );
}
