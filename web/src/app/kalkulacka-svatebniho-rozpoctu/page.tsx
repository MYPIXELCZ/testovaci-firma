import type { Metadata } from "next";
import Link from "next/link";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";
import BudgetCalculator from "./BudgetCalculator";

export const metadata: Metadata = articleMetadata(
  "kalkulacka-svatebniho-rozpoctu",
  "Kalkulačka svatebního rozpočtu: kolik na co dát",
  "Zadejte, kolik chcete za svatbu utratit a kolik máte hostů. Kalkulačka rozpočet rozdělí do kategorií a spočítá, kolik vychází na hostinu na jednoho hosta.",
);

export default function BudgetCalculatorPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Nástroj zdarma</p>
        <h1>Kalkulačka svatebního rozpočtu</h1>
        <p className="lead">
          Zadejte celkovou částku a počet hostů. Kalkulačka ji rozdělí do kategorií podle běžné praxe českých svateb a
          ukáže, kolik vám vychází na hostinu na jednoho hosta.
        </p>

        <BudgetCalculator />

        <h2>Jak s výsledkem pracovat</h2>
        <ul>
          <li>
            <strong>Částka na hosta je nejdůležitější číslo.</strong> Porovnejte ji s nabídkami míst a cateringu. Když
            vychází výrazně méně, než kolik si místa účtují, uberte hosty, nebo přesuňte peníze z jiné kategorie.
          </li>
          <li>
            <strong>Rozdělení není pravidlo.</strong> Pokud vám záleží na fotkách víc než na výzdobě, klidně ho upravte.
            Důležité je, aby součet seděl.
          </li>
          <li>
            <strong>Rezervu nechte v rozpočtu.</strong> Pět procent na nečekané výdaje se téměř vždy použije.
          </li>
          <li><strong>Svatební cestu počítejte zvlášť.</strong> Většina párů ji do rozpočtu svatby nezahrnuje.</li>
        </ul>
        <p>
          Víc o tom, jak rozpočet hlídat, najdete v článku{" "}
          <Link href="/svatebni-rozpocet">Svatební rozpočet: jak ho rozdělit a nepřetáhnout</Link>.
        </p>

        <ArticleCta
          title="Z odhadu skutečný rozpočet"
          text="Kalkulačka dá první odhad. V plánovači pak ke každé položce zapíšete plán, skutečnou cenu a zálohy a hned vidíte, kde přetahujete, kolik zbývá doplatit a kdy jsou nejbližší platby."
        />
      </article>
    </section>
  );
}
