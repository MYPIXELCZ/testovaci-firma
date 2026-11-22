"use client";

import { useEffect } from "react";

// Krok nákupní cesty do měření Project Trackeru (n.js, bez cookies): mpn("product" | "checkout" …).
// n.js se načítá až po stránce, proto se chvíli čeká, než je window.mpn k dispozici. NEMAZAT.
export default function TrackerEvent({ event }: { event: "product" | "add_to_cart" | "cart" | "checkout" }) {
  useEffect(() => {
    let tries = 0;
    const t = setInterval(() => {
      const mpn = (window as Window & { mpn?: (e: string) => void }).mpn;
      if (mpn || ++tries > 20) {
        clearInterval(t);
        mpn?.(event);
      }
    }, 500);
    return () => clearInterval(t);
  }, [event]);
  return null;
}
