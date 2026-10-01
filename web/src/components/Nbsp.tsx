"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

// Česká typografie: jednopísmenné předložky a spojky a čísla nezůstanou na konci řádku (nezlomitelná mezera).
const RULES: [RegExp, string][] = [
  [/(^|[\s(„])([kKsSvVzZoOuUaAiI])\s+/g, "$1$2 "],
  [/(\d\.?)\s+(?=[\p{L}%])/gu, "$1 "],
];

export default function Nbsp() {
  const path = usePathname();
  useEffect(() => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.parentElement?.closest("script,style,textarea,input,code,pre") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
    });
    let prev: Node | null = null;
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const before = n.nodeValue ?? "";
      let after = RULES.reduce((t, [rx, to]) => t.replace(rx, to), before);
      // React dělí „349 Kč“ do více textových uzlů: mezera na začátku navazuje na číslo v předchozím uzlu.
      if (prev?.parentElement === n.parentElement && /\d$/.test(prev.nodeValue ?? "")) after = after.replace(/^\s+(?=[\p{L}%])/u, "\u00a0");
      if (after !== before) n.nodeValue = after;
      prev = n;
    }
  }, [path]);
  return null;
}
