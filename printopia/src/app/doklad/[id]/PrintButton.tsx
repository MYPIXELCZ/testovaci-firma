"use client";

export default function PrintButton() {
  return (
    <p className="no-print" style={{ marginTop: 32 }}>
      <button className="btn btn-ghost" onClick={() => window.print()}>Vytisknout nebo uložit do PDF</button>
    </p>
  );
}
