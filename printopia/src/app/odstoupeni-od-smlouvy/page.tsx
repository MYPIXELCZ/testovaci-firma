import type { Metadata } from "next";
import { WITHDRAWAL_FORM_HEAD, WITHDRAWAL_FORM_LINES, WITHDRAWAL_INFO } from "@/lib/withdrawal";
import WithdrawalForm from "./WithdrawalForm";

export const metadata: Metadata = {
  title: "Odstoupení od smlouvy",
  description: "Poučení o právu na odstoupení od smlouvy do 14 dnů, vzorový formulář a online formulář pro odstoupení.",
};

export default function WithdrawalPage() {
  return (
    <section className="hero">
      <div className="wrap narrow legal">
        <h1>Odstoupení od smlouvy</h1>
        <p className="muted">Sadu můžete do 14 dnů od objednávky vrátit bez udání důvodu. Peníze vrátíme na účet, ze kterého jste platili.</p>

        {WITHDRAWAL_INFO.map((s) => (
          <div key={s.h}>
            <h2>{s.h}</h2>
            {s.p.map((t) => <p key={t}>{t}</p>)}
          </div>
        ))}

        <h2>Odstoupit online</h2>
        <WithdrawalForm />

        <h2>Vzorový formulář pro odstoupení od smlouvy</h2>
        <p className="muted">{WITHDRAWAL_FORM_HEAD}</p>
        <ul className="withdrawal-form">{WITHDRAWAL_FORM_LINES.map((l) => <li key={l}>{l}</li>)}</ul>
      </div>
    </section>
  );
}
