"use client";

import { useState } from "react";
import Link from "next/link";

type Props = { source: "ukazka" | "koupit"; src: string; button: string; consentText: string; done: string };

export default function LeadForm({ source, src, button, consentText, done }: Props) {
  const [state, setState] = useState<"idle" | "sending" | "done">("idle");
  const [error, setError] = useState("");
  const [download, setDownload] = useState<string | null>(null);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setState("sending");
    setError("");
    const res = await fetch("/api/lead", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: f.get("email"), consent: f.get("consent") === "on", website: f.get("website"), source, src }),
    }).catch(() => null);
    const data = res ? await res.json().catch(() => ({})) : {};
    if (!res?.ok) {
      setState("idle");
      setError(data.error ?? "Něco se nepovedlo, zkuste to prosím znovu.");
      return;
    }
    setDownload(data.download ?? null);
    setState("done");
  }

  if (state === "done")
    return (
      <div>
        <p style={{ fontWeight: 600 }}>{done}</p>
        {download && <a className="btn" href={download} download>Stáhnout ukázku (PDF)</a>}
      </div>
    );

  return (
    <form className="form" onSubmit={submit}>
      <input type="email" name="email" required placeholder="vas@email.cz" autoComplete="email" aria-label="E-mail" />
      <div className="hp" aria-hidden="true"><input type="text" name="website" tabIndex={-1} autoComplete="off" /></div>
      <label className="check">
        <input type="checkbox" name="consent" required />
        <span>{consentText} <Link href="/ochrana-osobnich-udaju" target="_blank">Jak s e-mailem naložíme</Link>.</span>
      </label>
      {error && <p className="error" role="alert">{error}</p>}
      <div><button className="btn" type="submit" disabled={state === "sending"}>{button}</button></div>
    </form>
  );
}
