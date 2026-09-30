import type { Metadata } from "next";
import { COMPANY, CONTACT } from "@/lib/config";

export const metadata: Metadata = { title: "Ochrana osobních údajů" };

export default function Privacy() {
  return (
    <section>
      <div className="wrap narrow">
        <h1>Ochrana osobních údajů</h1>
        <p className="muted">Platí od 1. 10. 2026.</p>

        <h2>Kdo údaje zpracovává</h2>
        <p>
          Správcem je {COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico}, {COMPANY.register}. Kontakt:{" "}
          <a href={`mailto:${CONTACT}`}>{CONTACT}</a>.
        </p>

        <h2>Jaké údaje a proč</h2>
        <p>
          Když nám necháte e-mail (u ukázky zdarma nebo u upozornění na spuštění), uložíme si ho spolu s datem, s tím,
          zda jste rodič, žák, nebo učitel, a odkud jste na web přišli (například z reklamy). E-mail použijeme jen k tomu, abychom vám dali vědět, že
          je kompletní sada k dispozici, případně se slevou, kterou jsme slíbili. Pošleme nejvýše dva e-maily. Právním
          základem je váš souhlas (čl. 6 odst. 1 písm. a) GDPR). Formulář je určen dospělým a žákům od 15 let,
          e-maily dětí mladších 15 let vědomě nesbíráme.
        </p>

        <h2>Jak dlouho</h2>
        <p>
          Nejdéle do 31. 12. 2026, pak e-maily smažeme. Pokud se rozhodneme sadu nevydat, smažeme je do 30 dnů od
          tohoto rozhodnutí. Dřív je smažeme, kdykoli o to požádáte.
        </p>

        <h2>Kdo k údajům má přístup</h2>
        <p>
          Údaje uchováváme u poskytovatele hostingu Vercel Inc. (servery ve Frankfurtu) a e-maily odesíláme přes službu
          Resend. Oba jsou zpracovateli s odpovídajícími zárukami pro předávání údajů mimo EU (EU–US Data Privacy
          Framework nebo standardní smluvní doložky). Nikomu dalšímu údaje nepředáváme ani je neprodáváme.
        </p>

        <h2>Cookies</h2>
        <p>Web nepoužívá žádné cookies ani analytické nebo reklamní sledovací nástroje.</p>

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
