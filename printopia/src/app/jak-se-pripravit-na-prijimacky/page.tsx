import type { Metadata } from "next";
import Link from "next/link";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import Icon from "@/components/Icon";

// Cílová skupina: rodiče deváťáků (plátci) a starší žáci. Výukový obsah, bez výzvy dětem ke koupi.
export const metadata: Metadata = {
  title: "Jak se připravit na přijímačky z matematiky: plán do dubna",
  description:
    "Plán přípravy na přijímačky z matematiky od října do dubna: jak zjistit slabá témata, kolik procvičovat, kdy psát celé testy nanečisto a co dělat poslední týden.",
  alternates: { canonical: "/jak-se-pripravit-na-prijimacky" },
};

const PHASES: [string, string, string][] = [
  ["calendar", "Říjen: zjistit, kde to drhne", "Napište jeden test z minulých let (zdarma na webu CERMAT) bez časového limitu. Chyby si zapište podle témat: zlomky, procenta, rovnice, slovní úlohy, geometrie. Tenhle seznam je váš plán."],
  ["target", "Listopad až leden: téma po tématu", "Dvakrát až třikrát týdně 30 až 45 minut. Vždy jedno téma, začněte tím nejslabším. U každé chyby projít postup krok za krokem a najít, kde se výpočet rozešel. Pak pár podobných úloh navíc."],
  ["steps", "Únor a březen: celé testy na čas", "Jednou týdně celý test nanečisto na čas, jako u zkoušky. Mezi testy dál opravovat témata, kde se body ztrácejí. Sledujte, jestli se skóre zvedá."],
  ["print", "Duben: opakovat, ne dohánět", "Poslední dva týdny už nic nového. Krátké opakování jistých témat, jeden test na zahřátí a dost spánku. Zkouška bude 12. a 13. dubna 2027."],
];

export default function PreparePage() {
  return (
    <section className="hero">
      <Beacon page="tema" topic="jak-se-pripravit" />
      <div className="wrap narrow">
        <p className="eyebrow">Přijímačky z matematiky · pro rodiče i žáky</p>
        <h1>Jak se připravit na přijímačky z matematiky: plán do dubna</h1>
        <p className="lead">
          Na přijímačky z matiky se nedá naučit za víkend, ale ani není potřeba dřít každý den. Stačí pravidelnost a vědět,
          co procvičovat. Tady je plán od října do dubna, který funguje i bez drahého doučování.
        </p>

        {PHASES.map(([icon, title, text]) => (
          <div className="card" key={title} style={{ margin: "14px 0" }}>
            <Icon name={icon} />
            <h3>{title}</h3>
            <p className="muted" style={{ margin: 0 }}>{text}</p>
          </div>
        ))}

        <h2>Kolik času to zabere</h2>
        <p>
          Zhruba dvě hodiny týdně od listopadu do března, tedy kolem 40 hodin celkem. Víc než délka přípravy rozhoduje
          pravidelnost: tři kratší bloky týdně jsou lepší než jeden dlouhý o víkendu.
        </p>

        <h2>Rady pro rodiče</h2>
        <ul>
          <li>Nemusíte umět matiku. Stačí hlídat, že se procvičuje, a na konci se podívat, jestli sedí výsledek.</li>
          <li>Nevysvětlujte za dítě. Nechte ho najít chybu v postupu samo, zapamatuje si to líp.</li>
          <li>Chvalte pokrok v tématech, ne body. Body přijdou, až se slabá témata zlepší.</li>
          <li>Když se dítě v jednom tématu dlouho točí na místě, je to chvíle na doučování, ne na víc stejných úloh.</li>
        </ul>

        <h2>Začněte procvičovat hned</h2>
        <p>
          Příklady s postupem řešení zdarma: <Link href="/zlomky-prijimacky" data-track="topic_link">zlomky</Link>,{" "}
          <Link href="/procenta-prijimacky" data-track="topic_link">procenta</Link>,{" "}
          <Link href="/rovnice-prijimacky" data-track="topic_link">rovnice</Link> a{" "}
          <Link href="/slovni-ulohy-prijimacky" data-track="topic_link">slovní úlohy</Link>. Oficiální testy z minulých let
          najdete zdarma na webu <a href="https://prijimacky.cermat.cz/" rel="noopener">CERMAT</a>.
        </p>
        <p className="muted small">
          Připravujeme sady úloh k tisku podle témat s postupem u každé úlohy a plánem do zkoušky.{" "}
          <Link href="/">Podívejte se, co v nich bude</Link>.
        </p>

        <div style={{ marginTop: 32 }}><Feedback /></div>
      </div>
    </section>
  );
}
