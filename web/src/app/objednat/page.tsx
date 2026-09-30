import type { Metadata } from "next";
import { PRODUCT } from "@/lib/config";
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
        <OrderForm />
      </div>
    </section>
  );
}
