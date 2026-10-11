"use client";

import { useState } from "react";

// Zkopíruje hodnotu do schránky (pro zadání platby v bankovní aplikaci na mobilu).
export default function CopyButton({ value, label }: { value: string; label: string }) {
  const [done, setDone] = useState(false);
  return (
    <button
      type="button"
      className="copy-btn"
      aria-label={`Zkopírovat: ${label}`}
      onClick={() => {
        navigator.clipboard?.writeText(value).then(() => { setDone(true); setTimeout(() => setDone(false), 1800); }).catch(() => undefined);
      }}
    >
      {done ? "Zkopírováno" : "Kopírovat"}
    </button>
  );
}
