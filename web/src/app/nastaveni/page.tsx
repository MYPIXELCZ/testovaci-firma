import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getSecret, isAdminRequest } from "@/lib/secrets";
import { saveFioToken, saveResendKey } from "./actions";
import SecretForm from "./SecretForm";

export const metadata: Metadata = { title: "Nastavení", robots: { index: false } };

export default async function SettingsPage() {
  if (!(await isAdminRequest())) notFound();
  const [fio, resend] = await Promise.all([getSecret("FIO_TOKEN"), getSecret("RESEND_API_KEY")]);

  return (
    <section>
      <div className="wrap narrow">
        <h1 style={{ fontSize: "2.2rem" }}>Nastavení</h1>
        <p className="muted">Tokeny se uloží do privátního úložiště projektu. Nikde se nezobrazují a stránka je dostupná jen členům týmu.</p>
        <SecretForm
          label="Token Fio API"
          hint="Fio internetbanking → Nastavení → API → Přidat token, účet 2202343801, oprávnění „Pouze sledovat účet“. Po uložení ho hned ověřím u banky."
          isSet={Boolean(fio)}
          action={saveFioToken}
        />
        <SecretForm
          label="Klíč Resend (e-maily)"
          hint="resend.com → API Keys → Create API Key (Sending access). Začíná „re_“."
          isSet={Boolean(resend)}
          action={saveResendKey}
        />
      </div>
    </section>
  );
}
