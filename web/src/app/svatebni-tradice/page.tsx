import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = articleMetadata(
  "svatebni-tradice",
  "Svatební tradice a zvyky: které dodržet a kdy na ně dojde",
  "Přehled českých svatebních tradic od rána do půlnoci: požehnání, zatahování, rozbití talíře, polévka z jednoho talíře, únos nevěsty, čepení a svatební koláčky.",
);

const PARTS: [string, [string, string][]][] = [
  [
    "Ráno a cesta na obřad",
    [
      ["Poděkování rodičům", "Před odjezdem na obřad snoubenci poděkují rodičům za výchovu a rodiče jim popřejí. Stačí pár vět v kruhu nejbližších, ale bývá to jeden z nejdojemnějších okamžiků dne."],
      ["Něco starého, nového, půjčeného a modrého", "Zvyk, který k nám přišel z anglosaských zemí: nevěsta má na sobě čtyři věci pro štěstí. Starou po babičce, novou, půjčenou od šťastně vdané kamarádky a něco modrého."],
      ["Zatahování", "Hlavně na vesnicích přehradí místní svatebčanům cestu provazem nebo stuhou a pustí je dál až za výkupné, obvykle za láhev a pár drobných. Mějte je připravené v autě."],
    ],
  ],
  [
    "Po obřadu",
    [
      ["Házení rýže nebo okvětních lístků", "Rýže má novomanželům přinést plodnost a hojnost. Pozor: řada obřadních síní a kostelů ji nedovoluje, protože se špatně uklízí. Zeptejte se předem, okvětní lístky nebo bublifuk bývají povolené."],
      ["Špalír", "Hosté vytvoří uličku, kterou novomanželé projdou. Kolegové nebo spolužáci ho často doplní rekvizitami z práce či koníčků."],
    ],
  ],
  [
    "Před hostinou a na ní",
    [
      ["Rozbití talíře", "U vchodu na hostinu se rozbije talíř a novomanželé společně zametají střepy. Ukazuje, že spolu zvládnou práci. Hosté jim to rádi ztíží tím, že střepy rozkopávají."],
      ["Přenesení přes práh", "Ženich přenese nevěstu přes práh, aby zlé síly zůstaly venku."],
      ["Polévka z jednoho talíře", "Novomanželé se navzájem krmí polévkou, často s jedním ubrusem uvázaným kolem krku. Symbolizuje, že se o sebe budou starat."],
      ["Krájení dortu", "Novomanželé krájí dort společně jedním nožem. Kdo má ruku navrchu, prý bude doma vládnout."],
    ],
  ],
  [
    "Večer a o půlnoci",
    [
      ["První tanec", "Novomanželé otevírají taneční část večera. Pak tančí nevěsta s otcem a ženich s maminkou."],
      ["Házení kytice", "Svobodné ženy chytají kytici nevěsty. Která ji chytí, bude se prý vdávat příští. Mnoho nevěst si na házení nechává vyrobit menší kopii kytice."],
      ["Únos nevěsty", "Kamarádi nevěstu „unesou“ do nedaleké hospody a ženich ji musí najít a vyplatit, většinou zaplacením útraty. Domluvte předem pravidla, ať únos nezabere půl večera."],
      ["Čepení nevěsty", "O půlnoci nevěstě vdané ženy z rodiny sejmou závoj a nasadí čepec, symbol přechodu mezi vdané ženy. Dnes spíš jako vtipná scénka, často spojená s půlnočním překvapením."],
    ],
  ],
];

export default function TraditionsPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Svatební tradice a zvyky: které dodržet a kdy na ně dojde</h1>
        <p className="lead">
          Žádná tradice není povinná. Vyberte si ty, které vás baví nebo na kterých záleží rodině, a zbytek klidně
          vynechte. Tady je přehled těch nejběžnějších v pořadí, v jakém během dne přicházejí.
        </p>

        {PARTS.map(([part, items]) => (
          <div key={part}>
            <h2>{part}</h2>
            <ul>
              {items.map(([name, text]) => (
                <li key={name}><strong>{name}.</strong> {text}</li>
              ))}
            </ul>
          </div>
        ))}

        <h2>A co svatební koláčky?</h2>
        <p>
          Svatební koláčky jsou česká klasika. Rodina je peče nebo objednává předem a rozdávají se hostům i sousedům, kteří
          se na svatbu přišli podívat. Počítejte s několika kusy na hosta a objednejte je s předstihem, v sezóně mají
          cukrárny plno.
        </p>

        <div className="tip">
          <p>
            <strong>Tip:</strong> řekněte svědkům a moderátorovi, které tradice chcete a které ne. Předejdete tomu, že vás
            o půlnoci překvapí čepení, o které jste nestáli.
          </p>
        </div>

        <ArticleCta
          title="Tradice rovnou v harmonogramu"
          text="Plánovač obsahuje harmonogram svatebního dne s nejběžnějšími tradicemi na správném místě. Upravíte časy, smažete, co nechcete, a pošlete ho svědkům i dodavatelům."
        />
      </article>
    </section>
  );
}
