import type { Metadata } from "next";
import ArticleCta from "@/components/ArticleCta";
import planner from "@/content/planner.json";

export const metadata: Metadata = {
  title: "Svatební rozpočet: jak ho rozdělit a nepřetáhnout",
  description:
    "Jak rozdělit svatební rozpočet do kategorií, příklad rozdělení 250 000 Kč a pět pravidel, díky kterým svatbu nepřetáhnete.",
  alternates: { canonical: "/svatebni-rozpocet" },
};

const EXAMPLE = 250_000;
const kc = (n: number) => `${Math.round(n).toLocaleString("cs-CZ")} Kč`;
const pct = (n: number) => `${Math.round(n * 100)} %`;

export default function BudgetPage() {
  const cats = planner.categories.filter((c) => c.share > 0);
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Svatební rozpočet: jak ho rozdělit a nepřetáhnout</h1>
        <p className="lead">
          Svatbu nejčastěji prodraží drobnosti, které nikdo nečekal, a pocit, že „tohle už je jedno“. Pomůže, když rozpočet
          rozdělíte do kategorií dřív, než začnete objednávat.
        </p>

        <h2>Orientační rozdělení rozpočtu</h2>
        <p>
          Tohle rozdělení vychází z běžné praxe českých svateb. Není to pravidlo: když vám záleží na fotkách víc než na
          výzdobě, klidně ho přesuňte. Důležité je mít rozdělení vůbec nějaké.
        </p>
        <table className="data-table">
          <thead>
            <tr><th>Kategorie</th><th className="num">Podíl</th><th className="num">Z {kc(EXAMPLE)}</th></tr>
          </thead>
          <tbody>
            {cats.map((c) => (
              <tr key={c.name}><td>{c.name}</td><td className="num">{pct(c.share)}</td><td className="num">{kc(c.share * EXAMPLE)}</td></tr>
            ))}
          </tbody>
        </table>
        <p className="muted small">Svatební cestu počítejte zvlášť, do rozpočtu svatby ji většina párů nezahrnuje.</p>

        <h2>Pět pravidel, díky kterým rozpočet vydrží</h2>
        <ol>
          <li>
            <strong>Začněte částkou a počtem hostů.</strong> Místo a hostina tvoří největší část rozpočtu a jejich cena roste
            s každým hostem. Než začnete vybírat, ujasněte si obojí.
          </li>
          <li><strong>Nechte si rezervu.</strong> Aspoň 5 % na věci, se kterými nikdo nepočítal. Téměř vždy se použije.</li>
          <li>
            <strong>Oddělte plán od skutečnosti.</strong> Ke každé položce si pište, kolik jste plánovali a kolik to nakonec
            stálo. Hned uvidíte, kde přetahujete, a můžete ubrat jinde.
          </li>
          <li>
            <strong>Hlídejte zálohy a doplatky.</strong> Většina dodavatelů chce zálohu při rezervaci a zbytek před svatbou
            nebo v den D. Mějte přehled, kdy a komu co platíte.
          </li>
          <li>
            <strong>Domluvte si, kdo co platí.</strong> Pokud přispívají rodiče, řekněte si to na začátku a připište si to
            ke konkrétním položkám.
          </li>
        </ol>

        <h2>Položky, na které se zapomíná</h2>
        <ul>
          {planner.budgetItems
            .filter((b) => ["Obřad a poplatky", "Dárky", "Doprava", "Oznámení a tiskoviny"].includes(b.category))
            .map((b) => <li key={b.item}>{b.item}</li>)}
          <li>Doplatky v hotovosti v den svatby</li>
        </ul>

        <ArticleCta
          title="Rozpočet, který se hlídá sám"
          text="V plánovači zadáte celkový rozpočet a k položkám plán, skutečnou cenu a zálohy. Uvidíte, kolik zbývá doplatit, kdy jsou nejbližší platby a ve které kategorii jste nad plánem."
        />
      </article>
    </section>
  );
}
