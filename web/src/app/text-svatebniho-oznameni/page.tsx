import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";

export const metadata: Metadata = articleMetadata(
  "text-svatebniho-oznameni",
  "Text svatebního oznámení: vzory a co v něm nesmí chybět",
  "Vzory textů svatebního oznámení (klasický, moderní, krátký i s nadsázkou), pozvánka na hostinu a co všechno musí oznámení obsahovat. Plus kdy ho rozeslat.",
);

const TEMPLATES: [string, string][] = [
  [
    "Klasický",
    "S radostí oznamujeme, že si 12. června 2027 ve 14 hodin v zámecké kapli v Lysé nad Labem řekneme své ano.\nTereza Nováková a Jakub Svoboda",
  ],
  [
    "Moderní",
    "Po sedmi letech, dvou stěhováních a jednom psovi to konečně zpečetíme.\nBereme se 12. 6. 2027 ve 14:00, Statek Na Kopci, Hřebečníky.\nTereza & Jakub",
  ],
  ["Krátký", "Tereza a Jakub se berou.\n12. června 2027, 14:00, radnice v Brně"],
  [
    "S nadsázkou",
    "Oznamujeme, že od 12. června 2027 přestáváme být „ti dva, co spolu chodí“.\nObřad začne ve 14 hodin na Statku Na Kopci a útěk už nebude možný.\nTereza a Jakub",
  ],
  [
    "Za rodiče",
    "Manželé Novákovi a manželé Svobodovi si dovolují oznámit sňatek svých dětí Terezy a Jakuba, který se uskuteční 12. června 2027 ve 14 hodin v kostele sv. Jakuba v Praze.",
  ],
];

export default function AnnouncementPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Text svatebního oznámení: vzory a co v něm nesmí chybět</h1>
        <p className="lead">
          Oznámení je pro většinu hostů první věc, kterou ze svatby uvidí. Nemusí být dlouhé, ale musí z něj být jasné, kdo,
          kdy a kde. Níž najdete pět vzorů, které stačí upravit.
        </p>

        <h2>Co musí oznámení obsahovat</h2>
        <ul>
          <li>Jména obou snoubenců (obvykle nevěsta první, ale není to pravidlo).</li>
          <li>Datum a čas obřadu.</li>
          <li>Místo obřadu: název a obec, u méně známých míst i adresu.</li>
          <li>Případně kontakt nebo termín, do kdy mají hosté odpovědět.</li>
        </ul>
        <p>
          Místo hostiny, doporučené oblečení nebo tipy na dary patří spíš na samostatnou pozvánku pro ty, kdo jsou pozvaní
          i na oslavu.
        </p>

        <h2>Vzory textů</h2>
        {TEMPLATES.map(([name, text]) => (
          <div className="tip" key={name}>
            <p style={{ margin: "0 0 6px" }}><strong>{name}</strong></p>
            <p style={{ whiteSpace: "pre-line", fontFamily: "var(--serif)", fontSize: "1.1rem", margin: 0 }}>{text}</p>
          </div>
        ))}

        <h2>Pozvánka na hostinu</h2>
        <p>Vkládá se do oznámení jen těm, kdo jsou pozvaní i na oběd nebo oslavu. Stačí jedna nebo dvě věty:</p>
        <div className="tip">
          <p style={{ whiteSpace: "pre-line", fontFamily: "var(--serif)", fontSize: "1.1rem", margin: 0 }}>
            {"Budeme rádi, když s námi po obřadu zůstanete i na svatební hostině na Statku Na Kopci.\nDejte nám prosím vědět do 1. května na 777 123 456."}
          </p>
        </div>

        <h2>Kdy oznámení rozeslat</h2>
        <p>
          Zhruba tři měsíce před svatbou. Hosté, kteří cestují zdaleka nebo potřebují ubytování, ocení, když se termín
          dozví dřív, třeba z krátkého „save the date“ několik měsíců předem.
        </p>

        <h2>Na co si dát pozor</h2>
        <ul>
          <li>Před tiskem nechte text přečíst někomu dalšímu. Překlep v datu je nejčastější a nejdražší chyba.</li>
          <li>Objednejte o pár kusů víc, vždycky se na někoho zapomene.</li>
          <li>Veďte si seznam, komu jste oznámení poslali a kdo dostal i pozvánku na hostinu.</li>
        </ul>

        <ArticleCta
          title="Kdo už oznámení dostal?"
          text="V plánovači si u každého hosta značíte, zda mu oznámení odešlo, na co je pozvaný a jak odpověděl. Úkol „rozeslat oznámení“ se vám navíc ukáže ve správný čas."
        />
      </article>
    </section>
  );
}
