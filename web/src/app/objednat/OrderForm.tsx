"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { send } from "@/components/Beacon";

export default function OrderForm() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setSending(true);
    const f = new FormData(e.currentTarget);
    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: f.get("email"),
          name: f.get("name"),
          terms: f.get("terms") === "on",
          marketing: f.get("marketing") === "on",
          website: f.get("website"),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Objednávku se nepodařilo odeslat.");
      send("form_submit");
      router.push(`/objednavka/${data.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Objednávku se nepodařilo odeslat.");
      setSending(false);
    }
  }

  return (
    <form className="form" onSubmit={onSubmit}>
      <div className="field">
        <label htmlFor="email">E-mail</label>
        <input id="email" name="email" type="email" required autoComplete="email" placeholder="vy@example.cz" />
        <p className="muted small" style={{ margin: "6px 0 0" }}>Sem vám pošleme plánovač.</p>
      </div>
      <div className="field">
        <label htmlFor="name">Jméno a příjmení</label>
        <input id="name" name="name" type="text" required autoComplete="name" maxLength={120} />
        <p className="muted small" style={{ margin: "6px 0 0" }}>Uvedeme ho na doklad o zaplacení.</p>
      </div>
      <div className="hp" aria-hidden="true">
        <label htmlFor="website">Web</label>
        <input id="website" name="website" type="text" tabIndex={-1} autoComplete="off" />
      </div>
      <label className="check">
        <input type="checkbox" name="terms" required />
        <span>
          Souhlasím s <Link href="/obchodni-podminky" target="_blank">obchodními podmínkami</Link> a beru na vědomí{" "}
          <Link href="/ochrana-osobnich-udaju" target="_blank">zásady ochrany osobních údajů</Link>.
        </span>
      </label>
      <label className="check">
        <input type="checkbox" name="marketing" />
        <span className="muted">Chci občas dostat e-mail s tipy na plánování svatby. (Nepovinné, odhlásit se jde kdykoli.)</span>
      </label>
      {error && <p className="error">{error}</p>}
      <div>
        <button className="btn" type="submit" disabled={sending}>
          {sending ? "Odesílám…" : "Objednat s povinností platby"}
        </button>
      </div>
      <p className="muted small">Po odeslání zobrazíme QR kód k platbě. Údaje pošleme i e-mailem.</p>
    </form>
  );
}
