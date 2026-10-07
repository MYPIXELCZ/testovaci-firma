"use client";

import { useState } from "react";

// Odstoupení online ve dvou krocích (vyplnit, potvrdit). Nevyžaduje registraci ani přihlášení.
export default function WithdrawalForm() {
  const [step, setStep] = useState<"fill" | "confirm" | "done">("fill");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [vs, setVs] = useState("");
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  function review(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim()) || !vs.trim()) {
      setError("Vyplňte prosím jméno, e-mail a číslo objednávky.");
      return;
    }
    setError("");
    setStep("confirm");
  }

  async function confirm() {
    setSending(true);
    setError("");
    try {
      const res = await fetch("/api/odstoupeni", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, vs, website: (document.getElementById("wd-website") as HTMLInputElement | null)?.value ?? "" }),
      });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error ?? "Něco se nepovedlo.");
      setStep("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Něco se nepovedlo. Napište nám prosím na e-mail.");
    } finally {
      setSending(false);
    }
  }

  if (step === "done") {
    return <p role="status"><strong>Odstoupení jsme přijali.</strong> Potvrzení jsme poslali na {email}. Peníze vrátíme do 14 dnů od doručení odstoupení.</p>;
  }

  if (step === "confirm") {
    return (
      <div className="box">
        <p>Odstupujete od smlouvy o koupi sady Printopia. Zkontrolujte údaje:</p>
        <ul>
          <li>Jméno: {name}</li>
          <li>E-mail: {email}</li>
          <li>Číslo objednávky: {vs}</li>
        </ul>
        {error && <p className="error" role="alert">{error}</p>}
        <p style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <button type="button" className="btn btn-yellow" onClick={confirm} disabled={sending}>{sending ? "Odesílám…" : "Potvrdit odstoupení od smlouvy"}</button>
          <button type="button" className="btn btn-ghost" onClick={() => setStep("fill")} disabled={sending}>Zpět</button>
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={review} className="box form" noValidate>
      <div className="field"><label htmlFor="wd-name">Jméno a příjmení</label><input id="wd-name" type="text" value={name} onChange={(e) => setName(e.target.value)} autoComplete="name" /></div>
      <div className="field"><label htmlFor="wd-email">E-mail, který jste uvedli v objednávce</label><input id="wd-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" /></div>
      <div className="field"><label htmlFor="wd-vs">Číslo objednávky (variabilní symbol)</label><input id="wd-vs" type="text" value={vs} onChange={(e) => setVs(e.target.value)} inputMode="numeric" />
        <p className="small muted">Najdete ho v e-mailu s platebními údaji.</p></div>
      <div className="hp" aria-hidden="true"><input id="wd-website" type="text" tabIndex={-1} autoComplete="off" /></div>
      {error && <p className="error" role="alert">{error}</p>}
      <p><button type="submit" className="btn btn-ghost">Odstoupit od smlouvy</button></p>
    </form>
  );
}
