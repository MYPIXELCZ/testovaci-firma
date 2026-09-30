import Image from "next/image";
import Link from "next/link";
import { ARTICLES } from "@/content/articles";
import { COMPANY, PRODUCT, SALES_OPEN, SITE_URL } from "@/lib/config";
import prehled from "../../public/img/prehled.png";
import ukoly from "../../public/img/ukoly.png";
import rozpocet from "../../public/img/rozpocet.png";

const SHEETS = [
  ["Přehled", "Odpočet do svatby, stav rozpočtu, počty hostů a co vás čeká nejdřív."],
  ["Úkoly", "55 úkolů od zásnub po svatební cestu. Termíny se dopočítají podle vašeho data."],
  ["Rozpočet", "Plán, skutečná cena, zálohy a doplatky. Hlídá, kde přetahujete."],
  ["Hosté", "Pozvánky, odpovědi, děti, strava i ubytování. Kdo ještě neodpověděl, vidíte hned."],
  ["Zasedací pořádek", "Přiřadíte hosty ke stolům a uvidíte, kde je volno a kde už je plno."],
  ["Dodavatelé", "Kontakty, ceny, zálohy a smlouvy všech dodavatelů na jednom místě."],
  ["Den D", "Hotový harmonogram svatebního dne, který jen upravíte a pošlete dál."],
  ["Návod", "Krátký a srozumitelný. Za pět minut víte, jak na to."],
];

const FAQ = [
  ["Funguje to v Google Tabulkách?",
    "Ano. Soubor nahrajete na Disk Google a otevřete v Tabulkách. Pak ho můžete sdílet s partnerem a plánovat spolu, každý ze svého telefonu nebo počítače."],
  ["A v Excelu?", "Ano, v Excelu 2019, 2021 i Microsoft 365. Na Macu doporučujeme Excel nebo Google Tabulky, v aplikaci Numbers nefungují všechny funkce."],
  ["Jak rychle plánovač dostanu?",
    "Platby párujeme automaticky každých pár minut. Když zaplatíte okamžitou platbou, přijde vám e-mail s plánovačem obvykle do 10 minut. U běžného převodu nejpozději další pracovní den."],
  ["Proč jen převodem a ne kartou?",
    "Platba kartou nás stojí poplatky, převod nic. Díky tomu může být plánovač levnější. QR kód naskenujete v bankovní aplikaci a je hotovo."],
  ["Co když mi plánovač nebude vyhovovat?",
    "Do 14 dnů od nákupu můžete od smlouvy odstoupit. Stačí napsat e-mail a peníze vám vrátíme, bez vysvětlování."],
  ["Je to předplatné?", `Ne. Zaplatíte jednou ${PRODUCT.price} Kč a plánovač je váš.`],
  ["Platí termíny úkolů pro každou svatbu?",
    "Jsou to osvědčené orientační termíny. Každý si můžete posunout nebo přidat vlastní úkol. Doklady a lhůty pro sňatek vždy ověřte na své matrice."],
];

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Product",
  name: PRODUCT.name,
  description: "Svatební plánovač pro Excel a Google Tabulky: rozpočet, hosté, úkoly s termíny, zasedací pořádek a harmonogram dne D.",
  image: `${SITE_URL}/og.png`,
  brand: { "@type": "Brand", name: "Ano, beru" },
  offers: {
    "@type": "Offer",
    price: PRODUCT.price,
    priceCurrency: "CZK",
    availability: "https://schema.org/InStock",
    url: `${SITE_URL}/objednat`,
    seller: { "@type": "Organization", name: COMPANY.name },
  },
};

export default function Home() {
  return (
    <>
      {SALES_OPEN && (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      )}
      <section className="hero">
        <div className="wrap hero-grid">
          <div>
            <p className="eyebrow">Svatební plánovač</p>
            <h1>Naplánujte si svatbu v&nbsp;klidu<span className="accent">.</span></h1>
            <p className="lead">
              Rozpočet, hosté, úkoly s termíny i harmonogram dne D v jedné přehledné tabulce. Pro Excel
              i Google Tabulky.
            </p>
            <div className="hero-cta">
              <Link href="/objednat" className="btn">Koupit za {PRODUCT.price} Kč</Link>
              <span className="muted small">Jednorázově · bez předplatného · doručení e‑mailem</span>
            </div>
          </div>
          <div className="shot">
            <Image src={prehled} alt="Přehled plánovače: odpočet do svatby, rozpočet, hosté a nejbližší úkoly" priority sizes="(max-width: 900px) 100vw, 520px" />
          </div>
        </div>
      </section>

      <section className="band" id="jak-to-funguje">
        <div className="wrap">
          <div className="section-head">
            <h2>Jak to funguje</h2>
          </div>
          <div className="grid-3">
            <div className="card"><div className="num">1</div><h3>Objednáte</h3><p>Stačí e-mail a jméno pro doklad. Žádná registrace.</p></div>
            <div className="card"><div className="num">2</div><h3>Zaplatíte QR kódem</h3><p>Naskenujete ho v bankovní aplikaci. Číslo účtu ani symbol nemusíte opisovat.</p></div>
            <div className="card"><div className="num">3</div><h3>Začnete plánovat</h3><p>Plánovač vám přijde e-mailem. Vyplníte datum a rozpočet, zbytek se spočítá sám.</p></div>
          </div>
        </div>
      </section>

      <section id="co-najdete">
        <div className="wrap">
          <div className="feature-row">
            <div className="feature-text">
              <h2>Termíny si hlídat nemusíte</h2>
              <p className="muted">Zadáte datum svatby a plánovač rozloží 55 úkolů do celého roku. Co je po termínu, zčervená.</p>
              <ul className="checks">
                <li>od výběru místa po změnu příjmení po svatbě</li>
                <li>české zvyklosti: matrika, oznámení, koláčky, čepení</li>
                <li>vlastní úkoly přidáte jedním řádkem</li>
              </ul>
            </div>
            <div className="shot"><Image src={ukoly} alt="List Úkoly s termíny podle data svatby" sizes="(max-width: 900px) 100vw, 580px" /></div>
          </div>
          <div className="feature-row">
            <div className="feature-text">
              <h2>Rozpočet, který nepřeteče</h2>
              <p className="muted">Ke každé položce plán, skutečná cena a zálohy. Plánovač hlídá, kolik ještě doplácíte a kdy.</p>
              <ul className="checks">
                <li>doporučené rozdělení rozpočtu podle kategorií</li>
                <li>přehled nejbližších plateb dodavatelům</li>
                <li>hned vidíte, kde jste nad plánem</li>
              </ul>
            </div>
            <div className="shot"><Image src={rozpocet} alt="List Rozpočet se souhrnem po kategoriích" sizes="(max-width: 900px) 100vw, 580px" /></div>
          </div>

          <div className="section-head">
            <h2>Co všechno v plánovači je</h2>
          </div>
          <div className="grid-3">
            {SHEETS.map(([title, text]) => (
              <div className="card" key={title}><h3>{title}</h3><p>{text}</p></div>
            ))}
            <div className="card"><h3>Pro vás dva</h3><p>V Google Tabulkách ho sdílíte a upravujete spolu. Oba vidíte totéž.</p></div>
          </div>
        </div>
      </section>

      <section className="band" id="cena">
        <div className="wrap">
          <div className="price-box">
            <p className="eyebrow">Jedna cena, všechno uvnitř</p>
            <p className="price">{PRODUCT.price} Kč</p>
            <p className="muted small">jednorázově, včetně budoucích drobných aktualizací</p>
            <ul className="checks">
              <li>8 propojených listů pro Excel i Google Tabulky</li>
              <li>55 úkolů s termíny podle data svatby</li>
              <li>rozpočet, hosté, stoly, dodavatelé, den D</li>
              <li>14 dní na vrácení peněz bez udání důvodu</li>
            </ul>
            <div><Link href="/objednat" className="btn">Koupit plánovač</Link></div>
          </div>
        </div>
      </section>

      <section id="clanky">
        <div className="wrap">
          <div className="section-head">
            <h2>Než začnete plánovat</h2>
            <p className="muted">Zdarma: přehledy, které vám ušetří spoustu hledání.</p>
          </div>
          <div className="grid-3 article-list">
            {ARTICLES.map((a) => (
              <Link href={a.href} key={a.href}>
                <div className="card"><h3>{a.title}</h3><p>{a.description}</p></div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section id="otazky">
        <div className="wrap narrow">
          <h2>Časté otázky</h2>
          {FAQ.map(([q, a]) => (
            <details key={q}>
              <summary>{q}</summary>
              <p>{a}</p>
            </details>
          ))}
        </div>
      </section>
    </>
  );
}
