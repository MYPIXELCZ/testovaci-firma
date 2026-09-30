import type { Metadata } from "next";
import { COMPANY, UNPAID_RETENTION_DAYS } from "@/lib/config";

export const metadata: Metadata = { title: "Ochrana osobních údajů" };

export default function PrivacyPage() {
  const mail = <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a>;
  return (
    <section>
      <div className="wrap narrow legal">
        <h1>Ochrana osobních údajů</h1>
        <p className="muted">Platné od 1. 10. 2026</p>

        <h2>Kdo údaje zpracovává</h2>
        <p>
          Správcem osobních údajů je {COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico}. Kontakt pro vše, co se týká
          osobních údajů: {mail}.
        </p>

        <h2>Jaké údaje, proč a jak dlouho</h2>
        <ul>
          <li>
            <strong>Vyřízení objednávky:</strong> e-mail, jméno a příjmení, údaje o objednávce a platbě. Právním základem je
            plnění smlouvy. Nezaplacené objednávky mažeme po {UNPAID_RETENTION_DAYS} dnech.
          </li>
          <li>
            <strong>Účetnictví a daně:</strong> údaje z dokladu o zaplacení a z bankovního výpisu (včetně čísla účtu plátce)
            uchováváme po dobu, kterou ukládají účetní a daňové předpisy (nejvýše 10 let). Právním základem je plnění
            právní povinnosti.
          </li>
          <li>
            <strong>Reklamace a právní nároky:</strong> údaje o objednávce uchováváme po dobu promlčecích lhůt, obvykle 3 roky od
            nákupu. Právním základem je oprávněný zájem na obhajobě právních nároků.
          </li>
          <li>
            <strong>E-maily s tipy:</strong> jen pokud k tomu dáte souhlas v objednávce. Souhlas můžete kdykoli odvolat
            odkazem v e-mailu nebo napsáním na {mail}.
          </li>
        </ul>

        <h2>Komu údaje předáváme</h2>
        <p>Údaje neprodáváme. Předáváme je jen zpracovatelům, které potřebujeme k provozu:</p>
        <ul>
          <li>Vercel Inc. (hosting webu a úložiště objednávek),</li>
          <li>Resend (odesílání e-mailů),</li>
          <li>Fio banka, a.s. (příjem plateb),</li>
          <li>účetní, který vede naše účetnictví.</li>
        </ul>
        <p>
          Někteří zpracovatelé mohou údaje zpracovávat i mimo Evropskou unii. Děje se tak jen se zárukami podle GDPR, například
          v rámci EU–USA pro ochranu osobních údajů (Data Privacy Framework) nebo podle standardních smluvních doložek.
        </p>

        <h2>Vaše práva</h2>
        <p>
          Máte právo na přístup ke svým údajům, jejich opravu, výmaz, omezení zpracování a přenositelnost. Proti zpracování
          na základě oprávněného zájmu můžete vznést námitku a udělený souhlas můžete kdykoli odvolat. Stačí napsat na {mail}.
          Stížnost můžete podat u Úřadu pro ochranu osobních údajů, Pplk. Sochora 27, 170 00 Praha 7,{" "}
          <a href="https://uoou.gov.cz" target="_blank" rel="noreferrer">uoou.gov.cz</a>.
        </p>

        <h2>Cookies</h2>
        <p>
          Web nepoužívá analytické ani reklamní cookies a nesleduje vás. Písma hostujeme sami, nenačítají se od třetích stran.
          Anonymně počítáme, jak se stránky používají (například jak daleko lidé dočtou a na co kliknou), bez IP adresy a bez
          jakéhokoli identifikátoru, který by šel spojit s konkrétním člověkem. Stejně anonymní je i krátká anketa, co vám na
          nabídce chybí.
        </p>
      </div>
    </section>
  );
}
