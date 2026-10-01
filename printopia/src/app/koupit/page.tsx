import type { Metadata } from "next";
import { headers } from "next/headers";
import { after } from "next/server";
import Beacon from "@/components/Beacon";
import { track } from "@/lib/track";
import { CONTACT, PRODUCT, SALES_OPEN, TEST_PRICE, isInternalHost } from "@/lib/config";
import { FILES } from "@/content/sada";
import OrderForm from "./OrderForm";

export const metadata: Metadata = { title: "Objednávka", robots: { index: false } };

type Props = { searchParams: Promise<Record<string, string | string[] | undefined>> };

export default async function Buy({ searchParams }: Props) {
  const sp = await searchParams;
  const src = String(sp.src ?? "").slice(0, 40).replace(/[^\w.-]/g, "");
  const h = await headers();
  const ua = h.get("user-agent");
  const test = isInternalHost(h.get("host"));
  after(() => track("buy_click", src, ua));
  return (
    <section className="hero">
      <Beacon page="koupit" />
      <div className="wrap narrow">
        <h1>Objednávka</h1>
        <div className="summary">
          <span>
            {PRODUCT.name}
            <br />
            <span className="muted small">{FILES.length} pracovních listů v PDF k tisku, ke stažení hned po zaplacení</span>
          </span>
          <strong>{test ? TEST_PRICE : PRODUCT.price} Kč</strong>
        </div>
        {test && <p className="error">Testovací objednávka (jen pro tým): cena {TEST_PRICE} Kč.</p>}
        {SALES_OPEN || test ? (
          <OrderForm src={src} />
        ) : (
          <p>Prodej právě spouštíme. Napište nám na <a href={`mailto:${CONTACT}`}>{CONTACT}</a> a pošleme vám odkaz, jakmile to půjde.</p>
        )}
      </div>
    </section>
  );
}
