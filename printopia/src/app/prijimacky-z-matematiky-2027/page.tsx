import type { Metadata } from "next";
import Link from "next/link";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import { PRICE } from "@/lib/config";

// Cílová skupina: rodiče deváťáků (hledají i platí) a žáci. Fakta z CERMAT a MŠMT, zdroje dole, plan/postupy/sbirka-prijimacky.md.
export const metadata: Metadata = {
  title: "Přijímačky z matematiky 2027: jak vypadá test, body a termíny",
  description:
    "Jak vypadá jednotná přijímací zkouška z matematiky: 16 úloh, 50 bodů, 70 minut. Typy úloh, bodování postupu, termíny 2027 a kde žáci ztrácejí nejvíc bodů.",
  alternates: { canonical: "/prijimacky-z-matematiky-2027" },
};

const TASKS: [string, string, string][] = [
  ["1–4", "Čísla, výrazy a rovnice", "zlomky, mocniny a odmocniny, úprava výrazů, lineární rovnice a od roku 2025 často soustava rovnic; v každé úloze je část s postupem za 2 body"],
  ["5–8", "Slovní úlohy a geometrie výpočtem", "„o třetinu víc, označme x“, procenta, úměrnost, pohyb, obsahy, úhly a tělesa"],
  ["9–10", "Konstrukce", "trojúhelníky a čtyřúhelníky, často s více řešeními, rýsuje se pravítkem a kružítkem"],
  ["11", "Tři tvrzení ANO/NE", "ke grafu, diagramu nebo tabulce, někdy ke geometrii"],
  ["12–14", "Výběr z pěti možností", "procenta, úhly, tělesa, slovní úlohy"],
  ["15", "Přiřazování", "u procent, tři podúlohy, nabídka A–F"],
  ["16", "Nestandardní úloha", "posloupnost obrazců, číselné vzory, logika"],
];

const LOSSES: [string, string, string][] = [
  ["Úsudek a vzory (úloha 16)", "14 %", "nejhorší část testu, často ji vynechá víc než čtvrtina žáků"],
  ["Konstrukce", "24 %", "35 % žáků konstrukci vůbec nezkusí"],
  ["Tělesa", "28 %", "žáci pletou povrch s pláštěm a chybují v jednotkách"],
  ["Slovní úlohy s neznámou", "29 %", "typické je „o třetinu víc“ a „o třetinu méně“"],
  ["Geometrie v rovině", "37 %", "obsahy, obvody, kruh a úhly"],
  ["Procenta", "47 %", "nejvíc bodů ze všech témat, asi 7 z 50"],
];

export default function ExamPage() {
  return (
    <section className="hero">
      <Beacon page="tema" topic="prijimacky-2027" />
      <div className="wrap narrow">
        <p className="eyebrow">Přijímačky z matematiky · pro rodiče i žáky</p>
        <h1>Přijímačky z matematiky 2027: jak vypadá test, body a termíny</h1>
        <p className="lead">
          Jednotná přijímací zkouška z matematiky je každý rok skoro stejná. Když víte, co v ní je a kde žáci ztrácejí
          nejvíc bodů, dá se příprava zacílit. Tady je přehled podle oficiálních údajů CERMAT.
        </p>

        <h2>Základní údaje</h2>
        <table className="pay-table">
          <tbody>
            <tr><td>Termín 2027</td><td>12. a 13. dubna (řádný), 29. a 30. dubna (náhradní)</td></tr>
            <tr><td>Rozsah testu</td><td>16 úloh: 11 otevřených, 5 uzavřených</td></tr>
            <tr><td>Body a čas</td><td>50 bodů, 70 minut</td></tr>
            <tr><td>Pomůcky</td><td>propiska, tužka, rýsovací potřeby; bez kalkulačky a tabulek</td></tr>
            <tr><td>Kolikrát psát</td><td>dvakrát, počítá se lepší výsledek</td></tr>
          </tbody>
        </table>
        <p className="small muted">
          Údaje o rozsahu platí pro zkoušku 2025/26 a stavba testu je od roku 2021 stejná. Specifikaci pro 2026/27
          CERMAT zatím nezveřejnil, počítáme se stejným rozsahem.
        </p>

        <h2>Z čeho se test skládá</h2>
        <table className="compare">
          <tbody>
            {TASKS.map(([n, title, text]) => (
              <tr key={n}><td style={{ whiteSpace: "nowrap" }}><strong>{n}</strong></td><td><strong>{title}</strong><br /><span className="muted small">{text}</span></td></tr>
            ))}
          </tbody>
        </table>
        <p>
          Na poslední straně testového sešitu jsou vzorce: druhé mocniny čísel 11 až 20, hodnota π, rozklady (a ± b)² a
          a² − b² a obvod a obsah kruhu. Ostatní vzorce, třeba objem a povrch těles, je potřeba umět.
        </p>

        <h2>Jak se boduje postup</h2>
        <ul>
          <li>Úloha s postupem je za 2 body. <strong>Bez postupu je 0 bodů</strong>, i když je výsledek správně.</li>
          <li>Jedna drobná chyba (znaménko, špatně opsané číslo, zlomek není v základním tvaru) stojí 1 bod.</li>
          <li>Chyba v postupu nebo víc chyb znamená 0 bodů. Záporné body nejsou.</li>
          <li>U uzavřených úloh se vždy vyplatí tipnout, špatná odpověď nic neubírá.</li>
        </ul>

        <h2>Kde žáci ztrácejí nejvíc bodů</h2>
        <p>
          Průměrný žák získá zhruba 17 až 21 bodů z 50 (v řádných termínech 2025 to bylo 35 %, v roce 2026 38 až 41 %).
          Úspěšnost jednotlivých okruhů podle dat CERMAT za roky 2025 a 2026:
        </p>
        <table className="compare">
          <tbody>
            {LOSSES.map(([what, rate, note]) => (
              <tr key={what}><td><strong>{what}</strong><br /><span className="muted small">{note}</span></td><td className="num"><strong>{rate}</strong></td></tr>
            ))}
          </tbody>
        </table>
        <p>
          Úlohy 2 až 4 jsou „levné“ body: zlomky, výrazy a rovnice se dají vypracovat tréninkem a postup v nich přináší
          dílčí body. Konstrukce a úloha 16 žáci často vynechají, přitom i první část úlohy 16 stojí za pokus.
        </p>

        <h2>Co z toho plyne pro přípravu</h2>
        <ul>
          <li>Začněte tématy, která se opakují každý rok: zlomky, výrazy, rovnice, procenta, obsahy a tělesa.</li>
          <li>Konstrukce se dají natrénovat a mají nejnižší úspěšnost, tedy největší prostor pro zlepšení.</li>
          <li>Procvičujte úlohy s postupem. Bez něj i správný výsledek nic nevynese.</li>
          <li>Psát celý test na čas začněte až v zimě, dřív je důležitější umět jednotlivá témata.</li>
        </ul>
        <p>
          Plán přípravy po měsících najdete v článku <Link href="/jak-se-pripravit-na-prijimacky" data-track="topic_link">Jak se připravit na přijímačky z matematiky</Link>.
          Příklady s postupem zdarma:{" "}
          <Link href="/procenta-prijimacky" data-track="topic_link">procenta</Link>,{" "}
          <Link href="/telesa-objem-povrch-prijimacky" data-track="topic_link">tělesa</Link>,{" "}
          <Link href="/konstrukcni-ulohy-prijimacky" data-track="topic_link">konstrukce</Link>,{" "}
          <Link href="/zlomky-prijimacky" data-track="topic_link">zlomky</Link>,{" "}
          <Link href="/rovnice-prijimacky" data-track="topic_link">rovnice</Link>.
        </p>

        <div className="box" style={{ marginTop: 28 }}>
          <h2 style={{ marginTop: 0 }}>Sada na všech 12 témat</h2>
          <p>
            Úvodní test ukáže slabá témata, 12 tematických listů má řešený příklad a postup u každé úlohy včetně konstrukcí
            a úlohy 16, plán rozvrhne přípravu do zkoušky. K tisku, za {PRICE} Kč jednorázově.
          </p>
          <p><Link href="/" className="btn btn-yellow" data-track="cta_buy">Podívat se na sadu</Link></p>
        </div>

        <h2>Zdroje</h2>
        <ul className="small">
          <li><a href="https://prijimacky.cermat.cz/menu/jednotna-prijimaci-zkouska.html" rel="noopener">CERMAT: Jednotná přijímací zkouška</a> (rozsah, čas, pomůcky)</li>
          <li><a href="https://prijimacky.cermat.cz/files/files/dokumenty/Hodnoceni_uloh_JPZ_MA.pdf" rel="noopener">CERMAT: Hodnocení úloh z matematiky</a> (bodování postupu)</li>
          <li><a href="https://data.cermat.cz/data-a-analyticke-vystupy-jednotna-prijimaci-zkouska/agregovana-data-jpz/agregovane-vysledky-uloh-jpz.html" rel="noopener">CERMAT: agregované výsledky úloh</a> (úspěšnost, výpočet z dat 2025 a 2026)</li>
          <li><a href="https://msmt.gov.cz/media/wp-content/uploads/2026/08/Sdeleni-o-terminech_2026-2027.pdf" rel="noopener">MŠMT: termíny zkoušek 2026/2027</a></li>
        </ul>
        <p className="muted small">Sada Printopia není oficiálním materiálem CERMAT.</p>

        <div style={{ marginTop: 32 }}><Feedback /></div>
      </div>
    </section>
  );
}
