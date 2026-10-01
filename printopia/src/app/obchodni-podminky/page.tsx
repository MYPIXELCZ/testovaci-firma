import type { Metadata } from "next";
import Link from "next/link";
import { COMPANY, PRODUCT, UNPAID_RETENTION_DAYS } from "@/lib/config";

export const metadata: Metadata = { title: "Obchodní podmínky" };

const TERMS_EFFECTIVE = "1. 10. 2026";

export default function TermsPage() {
  return (
    <section className="hero">
      <div className="wrap narrow legal">
        <h1>Obchodní podmínky</h1>
        <p className="muted">Platné od {TERMS_EFFECTIVE}</p>

        <h2>1. Kdo jsme</h2>
        <p>
          Web printopia.cz provozuje a digitální obsah na něm prodává společnost {COMPANY.name}, se sídlem {COMPANY.address},
          IČO {COMPANY.ico}, {COMPANY.register} (dále „prodávající“). Kontakt: <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a>.
          {" "}{COMPANY.vat}
        </p>
        <p>
          Tyto podmínky upravují práva a povinnosti prodávajícího a kupujícího (dále „kupující“) při koupi digitálního obsahu
          přes web printopia.cz. Je-li kupující spotřebitel, řídí se vztah také občanským zákoníkem a zákonem o ochraně spotřebitele.
        </p>

        <h2>2. Co prodáváme</h2>
        <ol>
          <li>
            Předmětem koupě je {PRODUCT.name}, digitální obsah ve formě souborů PDF k tisku (dále „sada“): úvodní test,
            tematické pracovní listy s postupy řešení a plán procvičování. Obsah sady je popsaný na úvodní stránce webu.
          </li>
          <li>Sada se otevře v libovolném prohlížeči PDF a je určená k tisku na papír formátu A4.</li>
          <li>
            Kupující získává nevýhradní a časově neomezenou licenci k užití sady pro potřebu své domácnosti, včetně
            opakovaného tisku. Sadu ani její části nesmí dále šířit, prodávat, zveřejňovat ani používat při placené výuce
            či doučování bez písemného souhlasu prodávajícího.
          </li>
          <li>
            Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky. Sada není oficiálním materiálem CERMAT a prodávající
            nezaručuje výsledek u přijímací zkoušky.
          </li>
        </ol>

        <h2>3. Objednávka a uzavření smlouvy</h2>
        <ol>
          <li>
            Kupující vyplní objednávkový formulář a odešle ho tlačítkem „Objednat s povinností platby“. Tím podává závazný
            návrh na uzavření kupní smlouvy.
          </li>
          <li>
            Smlouva je uzavřena ve chvíli, kdy prodávající objednávku potvrdí zobrazením stránky s platebními údaji a
            e-mailem na adresu kupujícího.
          </li>
          <li>Smlouvu uzavíráme v češtině. Uzavřenou smlouvu archivujeme v elektronické podobě, kupujícímu je dostupná v e-mailu.</li>
          <li>Náklady na internetové připojení nese kupující, žádné další náklady na komunikaci na dálku neúčtujeme.</li>
        </ol>

        <h2>4. Cena a platba</h2>
        <ol>
          <li>Cena sady je {PRODUCT.price} Kč. Je konečná, prodávající není plátcem DPH.</li>
          <li>
            Platí se bankovním převodem na účet prodávajícího s uvedeným variabilním symbolem, nejsnáze pomocí QR kódu na
            stránce objednávky.
          </li>
          <li>
            Pokud platba nedorazí do {UNPAID_RETENTION_DAYS} dnů od objednávky, smlouva zaniká a objednávku včetně osobních
            údajů smažeme.
          </li>
          <li>Po připsání platby vystavíme doklad o zaplacení a pošleme ho e-mailem.</li>
        </ol>

        <h2>5. Dodání</h2>
        <p>
          Sadu dodáme zpřístupněním odkazů ke stažení na stránce objednávky a e-mailem, jakmile platbu spárujeme.
          Platby párujeme automaticky. U okamžité platby to obvykle trvá několik minut, u běžného převodu nejpozději
          následující pracovní den po připsání.
        </p>

        <h2>6. Odstoupení od smlouvy</h2>
        <ol>
          <li>
            Spotřebitel může od smlouvy odstoupit bez udání důvodu do 14 dnů od jejího uzavření. Stačí poslat e-mail na{" "}
            <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a> s číslem objednávky (variabilním symbolem). Lhůta je
            zachována, pokud e-mail odešle v jejím průběhu.
          </li>
          <li>
            Peníze vrátíme do 14 dnů od odstoupení na účet, ze kterého přišla platba, pokud se nedomluvíme jinak. Kupujícímu
            tím nevznikají žádné další náklady.
          </li>
          <li>Po odstoupení kupující sadu dál nepoužívá a její kopie smaže.</li>
        </ol>

        <h2>7. Vady a reklamace</h2>
        <ol>
          <li>
            Prodávající odpovídá za to, že sada odpovídá popisu a výsledky úloh jsou správné. Práva z vadného
            plnění se řídí občanským zákoníkem, zejména ustanoveními o dodání digitálního obsahu (§ 2389a a násl.).
          </li>
          <li>
            Vadu kupující oznámí e-mailem na <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a> a popíše, v čem spočívá.
            Reklamaci vyřídíme bez zbytečného odkladu, nejpozději do 30 dnů. Kupující má právo na odstranění vady, a pokud to
            nejde, na přiměřenou slevu nebo odstoupení od smlouvy.
          </li>
        </ol>

        <h2>8. Stížnosti a spory</h2>
        <p>
          Stížnosti řešíme e-mailem na <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a>. Spotřebitel má právo na
          mimosoudní řešení sporu. Příslušným subjektem je Česká obchodní inspekce, Štěpánská 567/15, 120 00 Praha 2,{" "}
          <a href="https://adr.coi.cz" target="_blank" rel="noreferrer">adr.coi.cz</a>. Dozor nad dodržováním povinností
          prodávajícího vykonává Česká obchodní inspekce a v oblasti živnostenského podnikání příslušný živnostenský úřad.
        </p>

        <h2>9. Osobní údaje</h2>
        <p>
          Jak zpracováváme osobní údaje, popisují <Link href="/ochrana-osobnich-udaju">zásady ochrany osobních údajů</Link>.
        </p>

        <h2>10. Závěrečná ustanovení</h2>
        <p>
          Vztahy neupravené těmito podmínkami se řídí českým právem. Podmínky můžeme změnit, pro již uzavřenou smlouvu však
          platí znění účinné v době objednávky.
        </p>
      </div>
    </section>
  );
}
