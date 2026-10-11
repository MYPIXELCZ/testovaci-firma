"use client";

import { useState } from "react";

// Tlačítko „Zaplatit kartou“: založí platbu u Stripe a přesměruje zákazníka na hostovanou stránku.
export default function CardPay({ id }: { id: string }) {
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  async function go() {
    setSending(true);
    setError("");
    try {
      const res = await fetch("/api/stripe/checkout", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id }) });
      const data = await res.json();
      if (!res.ok || !data.url) throw new Error(data.error ?? "Platbu kartou se nepodařilo otevřít.");
      window.location.href = data.url;
    } catch (e) {
      setError(e instanceof Error ? e.message : "Platbu kartou se nepodařilo otevřít. Zaplaťte prosím převodem.");
      setSending(false);
    }
  }
  return (
    <>
      <button type="button" className="btn btn-yellow" onClick={go} disabled={sending}>{sending ? "Otevírám platbu…" : "Zaplatit kartou nebo mobilem"}</button>
      {error && <p className="error" role="alert">{error}</p>}
    </>
  );
}
