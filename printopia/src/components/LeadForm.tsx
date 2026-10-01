"use client";

import { useState } from "react";
import Link from "next/link";
import { send } from "./Beacon";

// Kdo formulář vyplňuje: test poptávky tím měří, kdo je kupující. Mladší 15 let možnost nemají (GDPR, souhlas v ČR od 15 let).
const ROLES = [["rodic", "Rodič"], ["zak", "Žák/žákyně, je mi aspoň 15 let"], ["ucitel", "Učitel/lektor"]] as const;

type Props = { source: "ukazka"; src: string; button: string; consentText: string; done: string };

export default function LeadForm({ source, src, button, consentText, done }: Props) {
  const [state, setState] = useState<"idle" | "sending" | "done">("idle");
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setState("sending");
    setError("");
    const res = await fetch("/api/lead", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: f.get("email"), consent: f.get("consent") === "on", role: f.get("role"), website: f.get("website"), source, src }),
    }).catch(() => null);
    const data = res ? await res.json().catch(() => ({})) : {};
    if (!res?.ok) {
      setState("idle");
      setError(data.error ?? "Něco se nepovedlo, zkuste to prosím znovu.");
      return;
    }
    send("form_submit");
    setState("done");
  }

  if (state === "done") return <p style={{ fontWeight: 600 }}>{done}</p>;

  return (
    <form className="form" onSubmit={submit}>
      <input type="email" name="email" required placeholder="vas@email.cz" autoComplete="email" aria-label="E-mail" />
      <div className="hp" aria-hidden="true"><input type="text" name="website" tabIndex={-1} autoComplete="off" /></div>
      <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
        <legend className="small" style={{ fontWeight: 600, marginBottom: 6 }}>Kdo jste?</legend>
        <div style={{ display: "flex", gap: "8px 18px", flexWrap: "wrap" }}>
          {ROLES.map(([value, label]) => (
            <label className="check" key={value}><input type="radio" name="role" value={value} required /><span>{label}</span></label>
          ))}
        </div>
      </fieldset>
      <label className="check">
        <input type="checkbox" name="consent" required />
        <span>{consentText} <Link href="/ochrana-osobnich-udaju" target="_blank">Jak s e-mailem naložíme</Link>.</span>
      </label>
      {error && <p className="error" role="alert">{error}</p>}
      <div><button className="btn" type="submit" disabled={state === "sending"}>{button}</button></div>
    </form>
  );
}
