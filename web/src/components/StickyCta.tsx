"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

// Spodní lišta s nákupem na mobilu. Ukáže se až po odscrollování pod tlačítko v úvodu, ať nepřekrývá text nad ohybem.
export default function StickyCta({ href, label }: { href: string; label: string }) {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const anchor = document.querySelector("[data-hero-cta]");
    if (!anchor) return;
    const io = new IntersectionObserver(([e]) => setShow(!e.isIntersecting && e.boundingClientRect.top < 0));
    io.observe(anchor);
    return () => io.disconnect();
  }, []);
  return (
    <div className={`sticky-cta${show ? " on" : ""}`} aria-hidden={!show}>
      <Link href={href} className="btn" data-track="cta_buy" tabIndex={show ? 0 : -1}>{label}</Link>
    </div>
  );
}
