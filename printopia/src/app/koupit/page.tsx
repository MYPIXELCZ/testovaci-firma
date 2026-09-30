import type { Metadata } from "next";
import { headers } from "next/headers";
import { after } from "next/server";
import LeadForm from "@/components/LeadForm";
import { track } from "@/lib/track";
import { LAUNCH_DATE, LAUNCH_PRICE, PRICE } from "@/lib/config";

export const metadata: Metadata = { title: "Koupit sadu", robots: { index: false } };

type Props = { searchParams: Promise<Record<string, string | string[] | undefined>> };

export default async function Buy({ searchParams }: Props) {
  const sp = await searchParams;
  const src = String(sp.src ?? "").slice(0, 40).replace(/[^\w.-]/g, "");
  const ua = (await headers()).get("user-agent");
  after(() => track("buy_click", src, ua));
  return (
    <section className="hero">
      <div className="wrap narrow">
        <p className="eyebrow">Přijímačky z matiky po tématech</p>
        <h1>Sadu spouštíme {LAUNCH_DATE}</h1>
        <p className="lead">
          Děkujeme za zájem! Kompletní sadu zatím připravujeme a nic si teď neplatíte. Nechte nám e-mail a v den spuštění
          vám pošleme odkaz se slevou 20 %: <strong>{LAUNCH_PRICE} Kč</strong> místo {PRICE} Kč.
        </p>
        <div className="box" style={{ marginTop: 28 }}>
          <LeadForm
            source="koupit"
            src={src}
            button="Chci upozornění se slevou"
            consentText={`Souhlasím se zasláním upozornění a slevy, až bude sada k dispozici (${LAUNCH_DATE}).`}
            done="Hotovo! V den spuštění vám napíšeme. Mezitím si můžete stáhnout ukázku zdarma na úvodní stránce."
          />
        </div>
      </div>
    </section>
  );
}
