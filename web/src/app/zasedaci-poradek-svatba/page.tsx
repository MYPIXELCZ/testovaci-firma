import type { Metadata } from "next";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = {
  title: "Zasedací pořádek na svatbě: jak rozsadit hosty",
  description:
    "Jak udělat zasedací pořádek na svatbu: kdy ho sestavit, kdo sedí u hlavního stolu, kulaté stoly nebo tabule a jak rozsadit rodinu, přátele i děti.",
  alternates: { canonical: "/zasedaci-poradek-svatba" },
};

export default function SeatingPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Zasedací pořádek na svatbě: jak rozsadit hosty</h1>
        <p className="lead">
          Zasedací pořádek je jeden z posledních úkolů před svatbou a zároveň jeden z nejvíc diplomatických. S pár pravidly
          ho zvládnete za jeden večer.
        </p>

        <h2>Kdy ho sestavit</h2>
        <p>
          Až budete znát konečný počet hostů, tedy po termínu pro odpovědi. Obvykle to vychází na dva až čtyři týdny před
          svatbou. Dřív to nemá smysl, stejně se bude měnit.
        </p>

        <h2>Kulaté stoly, nebo tabule?</h2>
        <ul>
          <li><strong>Kulaté stoly</strong> pro 8 až 10 lidí: hosté si lépe povídají, ale rozsazení je potřeba víc promyslet.</li>
          <li><strong>Dlouhé tabule:</strong> flexibilnější, víc lidí se vejde a skupiny se dají snadno prodloužit.</li>
        </ul>
        <p>Kapacitu stolů si potvrďte s místem konání, ať nepočítáte s místy, která nejsou.</p>

        <h2>Kdo sedí u hlavního stolu</h2>
        <p>
          Novomanželé a svědci, často i rodiče. Pokud jsou rodiče rozvedení nebo je rodina velká, bývá jednodušší posadit
          rodiče k vlastním stolům hned vedle a u hlavního stolu nechat jen vás a svědky.
        </p>

        <h2>Osvědčená pravidla</h2>
        <ul>
          <li>Rodiny nechte pohromadě, přátele rozsaďte podle party, ze které je znáte.</li>
          <li>Každý host by měl u stolu znát aspoň jednoho dalšího člověka.</li>
          <li>Starší hosty posaďte dál od reproduktorů a blíž k toaletám a východu.</li>
          <li>Rodiny s malými dětmi dejte ke kraji, ať mohou snadno odejít. U více dětí se hodí dětský stůl.</li>
          <li>Lidi, kteří spolu nevycházejí, posaďte k různým stolům, ne naproti sobě.</li>
        </ul>

        <h2>Nezapomeňte na jmenovky a tabuli</h2>
        <p>
          U vchodu do sálu pomůže tabule nebo plakát se zasedacím pořádkem, na stolech jmenovky. Připravte je až po
          konečné verzi pořádku, obvykle poslední dva týdny.
        </p>

        <ArticleCta
          title="Rozsazení bez papírků a přepisování"
          text="V plánovači přiřadíte hostům číslo stolu a v listu Stoly hned vidíte, kolik míst je obsazeno, kde je volno a kdo z potvrzených hostů ještě nemá místo."
        />
      </article>
    </section>
  );
}
