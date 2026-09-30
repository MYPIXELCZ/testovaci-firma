import type { Metadata } from "next";
import { COMPANY, PRODUCT, SALES_OPEN } from "@/lib/config";
import OrderForm from "./OrderForm";

export const metadata: Metadata = { title: "Objednávka", robots: { index: false } };

export default function OrderPage() {
  return (
    <section>
      <div className="wrap narrow">
        <h1>Objednávka</h1>
        <div className="summary">
          <span>{PRODUCT.name}<br /><span className="muted small">Digitální soubor pro Excel a Google Tabulky</span></span>
          <strong>{PRODUCT.price} Kč</strong>
        </div>
        {SALES_OPEN ? (
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
