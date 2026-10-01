import type { Metadata } from "next";
import { COMPANY, CONTACT, UNPAID_RETENTION_DAYS } from "@/lib/config";

export const metadata: Metadata = { title: "Ochrana osobních údajů" };

export default function Privacy() {
  return (
    <section className="hero">
      <div className="wrap narrow legal">
        <h1>Ochrana osobních údajů</h1>
        <p className="muted">Platí od 1. 10. 2026.</p>

        <h2>Kdo údaje zpracovává</h2>
        <p>
          Správcem je {COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico}, {COMPANY.register}. Kontakt:{" "}
          <a href={`mailto:${CONTACT}`}>{CONTACT}</a>.
        </p>

        <h2>Jaké údaje, proč a jak dlouho</h2>
        <ul>
          <li>
            <strong>Vyřízení objednávky:</strong> e-mail, jméno a příjmení, údaje o objednávce a platbě a odkud jste na web
            přišli (například z reklamy). Právním základem je plnění smlouvy. Nezaplacené objednávky mažeme po{" "}
            {UNPAID_RETENTION_DAYS} dnech.
          </li>
          <li>
            <strong>Účetnictví:</strong> doklady o zaplacení uchováváme po dobu, kterou ukládají účetní a daňové předpisy
            (nejvýše 10 let). Právním základem je plnění právní povinnosti.
          </li>
          <li>
            <strong>Reklamace a právní nároky:</strong> údaje o objednávce uchováváme po dobu promlčecích lhůt, obvykle 3 roky
            od nákupu. Právním základem je oprávněný zájem.
          </li>
          <li>
            <strong>Ukázka zdarma a tipy k přípravě:</strong> když nám u ukázky necháte e-mail, uložíme ho s datem, s tím, zda
            jste rodič, žák, nebo učitel, a odkud jste přišli. Budeme vám posílat tipy k přípravě na přijímačky a nabídky
            Printopie, nejvýše dvakrát měsíčně. Právním základem je váš souhlas, který můžete kdykoli odvolat. E-maily
            smažeme nejpozději 30. 6. 2027, po přijímačkách. Formulář je určen dospělým a žákům od 15 let, e-maily dětí
            mladších 15 let vědomě nesbíráme.
          </li>
        </ul>

        <h2>Kdo k údajům má přístup</h2>
        <p>
          Údaje uchováváme u poskytovatele hostingu Vercel Inc. (servery ve Frankfurtu) a e-maily odesíláme přes službu
          Resend. Oba jsou zpracovateli s odpovídajícími zárukami pro předávání údajů mimo EU (EU–US Data Privacy
          Framework nebo standardní smluvní doložky). Nikomu dalšímu údaje nepředáváme ani je neprodáváme.
        </p>

        <h2>Cookies</h2>
        <p>
          Web nepoužívá žádné cookies ani reklamní sledovací nástroje. Anonymně počítáme, jak se stránky používají (například
          jak daleko lidé dočtou a na co kliknou), bez IP adresy a bez jakéhokoli identifikátoru, který by šel spojit
          s konkrétním člověkem. Stejně anonymní je i krátká anketa, co vám na nabídce chybí.
        </p>

        <h2>Vaše práva</h2>
        <p>
          Máte právo na přístup ke svým údajům, jejich opravu a výmaz a můžete kdykoli odvolat souhlas. Stačí napsat na{" "}
          <a href={`mailto:${CONTACT}`}>{CONTACT}</a>. Pokud máte za to, že údaje zpracováváme v rozporu s předpisy, můžete
          podat stížnost u Úřadu pro ochranu osobních údajů (<a href="https://uoou.gov.cz">uoou.gov.cz</a>).
        </p>
      </div>
    </section>
  );
}
