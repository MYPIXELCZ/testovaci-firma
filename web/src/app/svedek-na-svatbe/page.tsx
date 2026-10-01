import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = articleMetadata(
  "svedek-na-svatbe",
  "Svědek na svatbě: co ho čeká a jak to zvládnout",
  "Co dělá svědek a svědkyně na svatbě: před svatbou, při obřadu i na oslavě. Přehled úkolů, na které se nezapomíná, a tipy, jak pomoct novomanželům.",
);

export default function WitnessPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Svědek na svatbě: co ho čeká a jak to zvládnout</h1>
        <p className="lead">
          Úřední role svědka trvá pár minut: být u obřadu a podepsat se. Ve skutečnosti ale svědek a svědkyně bývají pravou
          rukou novomanželů celý den. Tady je přehled toho, co od vás pár nejspíš bude potřebovat.
        </p>

        <h2>Co říká zákon</h2>
        <p>
          Sňatek se uzavírá za přítomnosti dvou svědků, kteří obřad stvrdí podpisem. Jaké doklady si mají svědci vzít s sebou a
          jaké podmínky musí splňovat, vám řekne matrika, kde se svatba koná. Zeptejte se tam s předstihem.
        </p>

        <h2>Před svatbou</h2>
        <ul>
          <li>Pomoct s přípravami, na které snoubencům nezbývá čas: obvolat dodavatele, vyzvednout výzdobu, rozvézt věci.</li>
          <li>Uspořádat rozlučku se svobodou, pokud o ni stojí.</li>
          <li>Promyslet krátký proslov a program: hry, soutěže, překvapení.</li>
          <li>Znát harmonogram dne D a mít kontakty na fotografa, kapelu i místo konání.</li>
        </ul>

        <h2>V den svatby</h2>
        <ul>
          <li><strong>Mít u sebe prsteny a občanské průkazy</strong> (svoje i snoubenců, pokud je o to požádají).</li>
          <li>Hlídat čas a harmonogram, aby novomanželé nemuseli.</li>
          <li>Být kontaktní osobou pro dodavatele a předat připravené obálky s doplatky.</li>
          <li>Řešit drobné nehody: nouzová taška s jehlou a nití, náplastmi a léky na bolest hlavy se vždycky hodí.</li>
          <li>Po obřadu svolat hosty ke skupinovému focení dřív, než se rozutečou.</li>
        </ul>

        <h2>Na oslavě</h2>
        <ul>
          <li>Pronést proslov: stačí dvě až tři minuty, jeden příběh a přípitek.</li>
          <li>Rozproudit zábavu a hry, ale nepřehánět to. Novomanželé se mají bavit, ne plnit úkoly.</li>
          <li>Na konci večera pomoct s úklidem, odvozem dárků a vrácením půjčených věcí.</li>
        </ul>

        <div className="tip">
          <p>
            <strong>Tip pro snoubence:</strong> řekněte svědkům včas, co od nich čekáte. Nejlépe to sepište do jednoho
            seznamu úkolů, ať nic nevisí na „to se nějak domluvíme“.
          </p>
        </div>

        <ArticleCta
          title="Úkoly rozdělené, nic nevisí ve vzduchu"
          text="V plánovači má každý úkol sloupec Kdo, takže snadno vidíte, co je na vás a co na svědcích. Harmonogram dne D jim pošlete jako hotovou tabulku."
        />
      </article>
    </section>
  );
}
