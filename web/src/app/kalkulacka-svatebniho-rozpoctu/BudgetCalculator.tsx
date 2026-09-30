"use client";

import { useState } from "react";
import planner from "@/content/planner.json";

// Zaokrouhleno na stovky, přesnější čísla by u odhadu působila falešně přesně.
const kc = (n: number) => `${(Math.round(n / 100) * 100).toLocaleString("cs-CZ")} Kč`;
const digits = (s: string) => Number(s.replace(/\D/g, "").slice(0, 9)) || 0;
const VENUE = "Místo a hostina";

export default function BudgetCalculator() {
  const [budget, setBudget] = useState("250000");
  const [guests, setGuests] = useState("60");
  const total = digits(budget);
  const count = digits(guests);
  const cats = planner.categories.filter((c) => c.share > 0);
  const venue = cats.find((c) => c.name === VENUE)?.share ?? 0;

  return (
    <div className="calc">
      <div className="calc-inputs">
        <div className="field">
          <label htmlFor="budget">Celkový rozpočet (Kč)</label>
          <input id="budget" type="text" inputMode="numeric" value={budget} onChange={(e) => setBudget(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="guests">Počet hostů na hostině</label>
          <input id="guests" type="text" inputMode="numeric" value={guests} onChange={(e) => setGuests(e.target.value)} />
        </div>
      </div>

      {total > 0 && (
        <>
          <table className="data-table">
            <thead>
              <tr><th>Kategorie</th><th className="num">Podíl</th><th className="num">Částka</th></tr>
            </thead>
            <tbody>
              {cats.map((c) => (
                <tr key={c.name}>
                  <td>{c.name}</td>
                  <td className="num">{Math.round(c.share * 100)} %</td>
                  <td className="num">{kc(c.share * total)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {count > 0 && (
            <div className="summary" style={{ marginTop: 20 }}>
              <span>Na místo a hostinu vám vychází na jednoho hosta</span>
              <strong>{kc((venue * total) / count)}</strong>
            </div>
          )}
        </>
      )}
    </div>
  );
}
