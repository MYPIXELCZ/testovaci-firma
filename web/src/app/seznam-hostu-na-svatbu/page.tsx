import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = articleMetadata(
  "seznam-hostu-na-svatbu",
  "Seznam hostů na svatbu: jak ho sestavit a koho pozvat",
  "Jak sestavit seznam hostů na svatbu krok za krokem: počet, okruhy hostů, doprovod a děti, oznámení vs. pozvánka na hostinu a sběr odpovědí.",
);

export default function GuestListPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Seznam hostů na svatbu: jak ho sestavit a nezbláznit se</h1>
        <p className="lead">
          Seznam hostů ovlivní skoro všechno: rozpočet, výběr místa, menu i zasedací pořádek. Proto ho sestavte co
          nejdřív, klidně zatím nahrubo.
        </p>

        <h2>1. Začněte číslem, ne jmény</h2>
        <p>
          Nejdřív si řekněte, kolik lidí si můžete dovolit a kolik se vejde do místa, které se vám líbí. Hostina se platí za
          osobu, takže každý host navíc je v rozpočtu znát. Teprve potom začněte psát jména.
        </p>

        <h2>2. Rozdělte hosty do tří okruhů</h2>
        <ul>
          <li><strong>Musí být:</strong> nejbližší rodina a přátelé, bez kterých si svatbu neumíte představit.</li>
          <li><strong>Chceme je tam:</strong> širší rodina a kamarádi, se kterými se pravidelně vídáte.</li>
          <li><strong>Bylo by hezké:</strong> kolegové, vzdálenější známí. Tenhle okruh se škrtá jako první.</li>
        </ul>
        <p>Nejdřív si seznam sepište každý zvlášť, pak oba spojte. Rodičům ho ukažte až potom.</p>

        <h2>3. Rozhodněte jednou pro všechny: doprovod a děti</h2>
        <p>
          Smí přijít každý host s doprovodem, nebo jen páry? Budou na svatbě děti? Pravidlo si stanovte na začátku a držte se
          ho u všech stejně. Předejdete tak nepříjemným výjimkám a vysvětlování.
        </p>

        <h2>4. Oznámení není pozvánka na hostinu</h2>
        <p>
          Svatební oznámení se v Česku běžně posílá širokému okruhu lidí. Pozvánku na hostinu přiložíte jen těm, kdo s vámi
          budou i na obědě a oslavě. Někoho můžete pozvat jen na večerní část. V seznamu hostů si u každého poznamenejte, na co je
          pozvaný, jinak se v tom rychle ztratíte.
        </p>

        <h2>5. Sbírejte odpovědi s termínem</h2>
        <p>
          Na pozvánce uveďte, do kdy mají hosté odpovědět, obvykle 4 až 6 týdnů před svatbou. Kdo se neozve, tomu po termínu
          zavolejte. Místo konání i catering potřebují konečný počet zhruba měsíc předem.
        </p>

        <h2>6. Zjistěte i to, na co se zapomíná</h2>
        <ul>
          <li>Stravovací omezení a alergie (vegetariáni, bezlepková dieta).</li>
          <li>Kolik přijde dětí a jak jsou staré.</li>
          <li>Kdo potřebuje ubytování nebo odvoz.</li>
          <li>Adresu pro oznámení.</li>
        </ul>

        <ArticleCta
          title="Hosté přehledně na jednom místě"
          text="V plánovači zapisujete ke každé pozvánce počet osob, děti, stravu, ubytování a odpověď. Na přehledu hned vidíte, kolik lidí potvrdilo, kolik jich ještě neodpovědělo a kolik potřebuje speciální menu."
        />
      </article>
    </section>
  );
}
