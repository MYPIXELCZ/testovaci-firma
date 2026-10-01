import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = articleMetadata(
  "podekovani-za-svatebni-dar",
  "Poděkování za svatební dar: vzory textů a kdy je poslat",
  "Vzory poděkování za svatební dar a za účast na svatbě: klasické, osobní, krátké i pro finanční dar. Kdy poděkování poslat a jak na nikoho nezapomenout.",
);

const TEMPLATES: [string, string][] = [
  [
    "Klasické",
    "Milí Jano a Petře,\nděkujeme, že jste s námi 12. června oslavili náš velký den, a také za krásný dar. Moc si vážíme, že jste byli u toho.\nTereza a Jakub",
  ],
  [
    "Osobní",
    "Milá teto Marie,\nsada hrnků od Tebe má u nás čestné místo a každé ráno si při kávě vzpomeneme na svatbu. Děkujeme, že jsi s námi slavila až do konce.\nTereza a Jakub",
  ],
  [
    "Za finanční dar",
    "Milí Novákovi,\nděkujeme za štědrý příspěvek. Použijeme ho na svatební cestu do Itálie a pošleme vám odtud pohled. A hlavně díky, že jste s námi byli.\nTereza a Jakub",
  ],
  [
    "Krátké",
    "Děkujeme za dar, a hlavně za to, že jste s námi slavili. Byl to nejkrásnější den.\nTereza a Jakub",
  ],
  [
    "Za pomoc se svatbou",
    "Milá Kláro,\nbez Tebe by výzdoba nevznikla a my bychom ráno nevěděli, kde nám hlava stojí. Děkujeme za všechno, co jsi pro nás udělala.\nTereza a Jakub",
  ],
];

export default function ThankYouPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Poděkování za svatební dar: vzory textů a kdy je poslat</h1>
        <p className="lead">
          Po svatbě přijde únava, fotky a hromada dárků. Poděkování hostům je poslední úkol, který se snadno odkládá. Tady je
          pár vzorů, které stačí upravit, a rada, jak na nikoho nezapomenout.
        </p>

        <h2>Kdy poděkování poslat</h2>
        <p>
          Nejlépe do jednoho až dvou měsíců po svatbě, dokud mají hosté den v živé paměti. Pokud chcete přiložit společnou
          fotku, klidně počkejte, až dorazí od fotografa. Poděkování s fotkou potěší víc než rychlá zpráva bez ní.
        </p>

        <h2>Co do poděkování napsat</h2>
        <ul>
          <li>Oslovení jménem, ne hromadné „milí hosté“.</li>
          <li>Konkrétní dar nebo to, na co použijete finanční příspěvek.</li>
          <li>Jednu osobní větu: vzpomínku ze svatby nebo to, co pro vás host znamená.</li>
          <li>Podpis obou novomanželů.</li>
        </ul>

        <h2>Vzory textů</h2>
        {TEMPLATES.map(([name, text]) => (
          <div className="tip" key={name}>
            <p style={{ margin: "0 0 6px" }}><strong>{name}</strong></p>
            <p style={{ whiteSpace: "pre-line", fontFamily: "var(--serif)", fontSize: "1.1rem", margin: 0 }}>{text}</p>
          </div>
        ))}

        <h2>Kartička, dopis, nebo zpráva?</h2>
        <p>
          Tištěná kartička s fotkou ze svatby je klasika, kterou si hosté často schovají. Babičkám a starší rodině udělá
          radost nejvíc. Kamarádům, se kterými si běžně píšete, stačí osobní zpráva, jen ne hromadná. Důležité je, aby
          poděkování dostal každý, kdo vám něco dal nebo pomohl.
        </p>

        <h2>Jak na nikoho nezapomenout</h2>
        <ul>
          <li>Dary si zapište hned po svatbě, dokud víte, co je od koho. Přání a kartičky od darů nevyhazujte.</li>
          <li>U každého hosta si poznamenejte, jestli už poděkování odešlo.</li>
          <li>Nezapomeňte na lidi, kteří nic nedali, ale pomohli: svědky, rodiče, kamarády u výzdoby.</li>
        </ul>

        <ArticleCta
          title="Kdo dal co a komu už jste poděkovali"
          text="V seznamu hostů v plánovači si ke každému zapíšete dar a zaškrtnete, zda už dostal poděkování. Hned vidíte, komu ještě dlužíte kartičku."
        />
      </article>
    </section>
  );
}
