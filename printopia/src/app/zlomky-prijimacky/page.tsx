import type { Metadata } from "next";
import Link from "next/link";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
import ukazka from "@/content/ukazka.json";
import { LAUNCH_DATE, PRICE } from "@/lib/config";

export const metadata: Metadata = {
  title: "Zlomky na přijímačky: příklady s postupem řešení",
  description:
    "8 příkladů na zlomky ve stylu přijímaček z matematiky: sčítání, dělení, složené zlomky, rovnice a slovní úlohy. U každého postup krok za krokem.",
  alternates: { canonical: "/zlomky-prijimacky" },
};

export default function FractionsPage() {
  return (
    <section className="hero">
      <div className="wrap narrow">
        <p className="eyebrow">Přijímačky z matematiky · zlomky</p>
        <h1>Zlomky na přijímačky: příklady s postupem</h1>
        <p className="lead">
          Zlomky jsou v přijímačkách z matematiky skoro každý rok a navazují na ně rovnice i slovní úlohy. Tady je {ukazka.tasks.length}{" "}
          příkladů od nejjednodušších po slovní úlohy. Nejdřív počítejte sami, postup si rozbalte až potom.
        </p>

        <h2>Na co si dát pozor</h2>
        <ul>
          <li>Před sčítáním a odčítáním převeďte zlomky na společného jmenovatele (nejmenší společný násobek).</li>
          <li>Dělit zlomkem znamená násobit převrácenou hodnotou.</li>
          <li>U složeného zlomku spočítejte zvlášť čitatel a jmenovatel, pak je vydělte.</li>
          <li>Desetinná čísla a smíšená čísla nejdřív převeďte na zlomky.</li>
          <li>Výsledek vždy zkraťte na základní tvar a u slovní úlohy udělejte zkoušku.</li>
        </ul>

        <h2>Příklady</h2>
        {ukazka.tasks.map((t, i) => (
          <div className="task" key={t.text}>
            <span className="tag">{t.topic}</span>
            <p className="q">{i + 1}. <MathText text={t.text} /></p>
            <details>
              <summary className="small" style={{ cursor: "pointer", color: "var(--blue)" }}>Zobrazit postup a výsledek</summary>
              <ol>{t.steps.map((s) => <li key={s}><MathText text={s} /></li>)}</ol>
              <p className="a">Výsledek: <MathText text={t.answer} /></p>
            </details>
          </div>
        ))}

        <div className="box" style={{ marginTop: 32 }}>
          <h2 style={{ marginTop: 0 }}>Stáhněte si je k tisku</h2>
          <p>Stejné příklady jako PDF s místem na počítání a postupy na konci.</p>
          <LeadForm
            source="ukazka"
            src="zlomky"
            button="Stáhnout PDF zdarma"
            consentText={`Souhlasím se zasláním upozornění, až bude kompletní sada k dispozici (${LAUNCH_DATE}).`}
            done="Děkujeme! PDF je připravené ke stažení."
          />
        </div>

        <p style={{ marginTop: 32 }}>
          Další témata: <Link href="/procenta-prijimacky">procenta</Link>, <Link href="/rovnice-prijimacky">rovnice</Link>, <Link href="/slovni-ulohy-prijimacky">slovní úlohy</Link>.
          Připravujeme kompletní sadu na všech 12 témat přijímaček z matematiky za {PRICE} Kč.{" "}
          <Link href="/">Co v ní bude</Link>.
        </p>
      </div>
    </section>
  );
}
