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
          Seznam hostů ovlivní skoro všechno: rozpočet, výběr místa, menu i zasedací pořádek. Proto se vyplatí ho mít co
          nejdřív, i když zatím jen hrubě.
        </p>

        <h2>1. Začněte číslem, ne jmény</h2>
        <p>
          Nejdřív si řekněte, kolik lidí si můžete dovolit a kolik se vejde do místa, které se vám líbí. Hostina se platí za
          osobu, takže každý host navíc je znát. Teprve potom začněte psát jména.
        </p>

        <h2>2. Rozdělte hosty do tří okruhů</h2>
        <ul>
          <li><strong>Musí být:</strong> nejbližší rodina a přátelé, bez kterých si svatbu neumíte představit.</li>
          <li><strong>Chceme je tam:</strong> širší rodina a kamarádi, se kterými se pravidelně vídáte.</li>
          <li><strong>Bylo by hezké:</strong> kolegové, vzdálenější známí. Tenhle okruh se škrtá jako první.</li>
        </ul>
        <p>Každý z vás si nejdřív sepíše svůj seznam zvlášť, pak je spojte. Rodiče se k seznamu vyjádří až potom.</p>

        <h2>3. Rozhodněte jednou pro všechny: doprovod a děti</h2>
        <p>
          Smí přijít každý host s doprovodem, nebo jen páry? Budou na svatbě děti? Pravidlo si stanovte na začátku a držte se
          ho u všech stejně. Předejdete tak nepříjemným výjimkám a vysvětlování.
        </p>

        <h2>4. Oznámení není pozvánka na hostinu</h2>
        <p>
          V Česku se běžně rozesílá svatební oznámení širokému okruhu lidí a pozvánka na hostinu jen těm, kdo jsou pozvaní i
          na oběd a oslavu. Někoho můžete pozvat jen na večerní část. V seznamu hostů si u každého poznamenejte, na co je
          pozvaný, jinak se v tom rychle ztratíte.
        </p>

        <h2>5. Sbírejte odpovědi s termínem</h2>
        <p>
          Na pozvánce uveďte, do kdy mají hosté odpovědět, obvykle 4 až 6 týdnů před svatbou. Kdo se neozve, tomu po termínu
          zavolejte. Konečný počet potřebuje místo konání i catering zhruba měsíc předem.
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
          text="V plánovači zapisujete ke každé pozvánce počet osob, děti, stravu, ubytování a odpověď. Na přehledu hned vidíte, kolik lidí potvrdilo, kolik jich čeká na odpověď a kolik potřebuje speciální menu."
        />
      </article>
    </section>
  );
}
