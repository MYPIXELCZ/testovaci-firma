"use client";

import { useState } from "react";
import { FEEDBACK, type FeedbackKey } from "@/lib/metrics";
import { send } from "./Beacon";

// Anonymní otázka „proč ne“: bez e-mailu, jen volba a nepovinný krátký text.
export default function Feedback() {
  const [choice, setChoice] = useState<FeedbackKey | "">("");
  const [text, setText] = useState("");
  const [done, setDone] = useState(false);

  if (done) return <p className="small" style={{ fontWeight: 600 }}>Děkujeme, moc nám to pomůže.</p>;
  return (
    <div className="card">
      <h3>Pomozte nám: co vás zatím drží od objednání?</h3>
      <p className="small muted" style={{ marginTop: 0 }}>Anonymně, stačí jedno kliknutí.</p>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {(Object.keys(FEEDBACK) as FeedbackKey[]).map((k) => (
          <button key={k} type="button" className={`chip${choice === k ? " on" : ""}`} onClick={() => setChoice(k)}>{FEEDBACK[k]}</button>
        ))}
      </div>
      {choice && (
        <div style={{ marginTop: 12, display: "grid", gap: 10 }}>
          <input className="text" maxLength={200} value={text} onChange={(e) => setText(e.target.value)}
                 placeholder="Chcete něco doplnit? (nepovinné, bez osobních údajů)" aria-label="Doplnění" />
          <div><button type="button" className="btn btn-small" onClick={() => { send("feedback", { choice, text: text.slice(0, 200) }); setDone(true); }}>Odeslat</button></div>
        </div>
      )}
    </div>
  );
}
