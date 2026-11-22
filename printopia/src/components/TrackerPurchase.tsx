"use client";

import { useEffect } from "react";

// Zaplacená objednávka do měření Project Trackeru (n.js, bez cookies). Jednou na objednávku;
// n.js se načítá až po stránce, proto se chvíli čeká, než je window.mpn k dispozici.
export default function TrackerPurchase({ orderId }: { orderId: string }) {
  useEffect(() => {
    const key = `pt_purchase_${orderId}`;
    try { if (localStorage.getItem(key)) return; } catch {}
    let tries = 0;
    const t = setInterval(() => {
      const mpn = (window as Window & { mpn?: (e: string) => void }).mpn;
      if (mpn || ++tries > 20) {
        clearInterval(t);
        if (!mpn) return;
        mpn("purchase");
        try { localStorage.setItem(key, "1"); } catch {}
      }
    }, 500);
    return () => clearInterval(t);
  }, [orderId]);
  return null;
}
