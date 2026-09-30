"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { pageOf, type Event as Ev } from "@/lib/metrics";

// Posílá anonymní události (viz lib/metrics.ts). ID návštěvy žije jen v paměti stránky, mění se s každou stránkou.
let pv = "";
let meta = { page: "home", topic: "", src: "" };

export function send(ev: Ev, extra: Record<string, string> = {}) {
  if (!pv) return;
  const body = JSON.stringify({ pv, ev, ...meta, ...extra });
  if (!navigator.sendBeacon?.("/api/e", new Blob([body], { type: "application/json" })))
    fetch("/api/e", { method: "POST", body, keepalive: true, headers: { "Content-Type": "application/json" } }).catch(() => {});
}

export default function Beacon() {
  const pathname = usePathname();
  useEffect(() => {
    if (pathname.startsWith("/nastaveni")) return; // interní stránka, neměřit
    pv = crypto.randomUUID();
    const q = new URLSearchParams(location.search);
    meta = { ...pageOf(pathname), src: (q.get("utm_source") ?? q.get("src") ?? "").slice(0, 40) };
    send("view", { ref: document.referrer ? new URL(document.referrer).hostname : "" });

    const seen = new Set<string>();
    const once = (ev: Ev) => { if (!seen.has(ev)) { seen.add(ev); send(ev); } };
    const onScroll = () => {
      const h = document.documentElement;
      const p = (h.scrollTop + window.innerHeight) / h.scrollHeight;
      if (p >= 0.25) once("scroll25");
      if (p >= 0.5) once("scroll50");
      if (p >= 0.75) once("scroll75");
      if (p >= 0.97) once("scroll100");
    };
    let visible = 0;
    const tick = setInterval(() => {
      if (document.visibilityState !== "visible") return;
      visible += 1;
      if (visible === 10) once("t10");
      if (visible === 30) once("t30");
      if (visible === 60) once("t60");
    }, 1000);
    const onClick = (e: MouseEvent) => {
      const el = (e.target as HTMLElement).closest("[data-track]");
      if (el) send(el.getAttribute("data-track") as Ev);
    };
    const onFocus = (e: FocusEvent) => {
      if ((e.target as HTMLElement).matches?.("input[type=email]")) once("form_start");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("click", onClick);
    document.addEventListener("focusin", onFocus);
    onScroll();
    return () => {
      clearInterval(tick);
      window.removeEventListener("scroll", onScroll);
      document.removeEventListener("click", onClick);
      document.removeEventListener("focusin", onFocus);
    };
  }, [pathname]);
  return null;
}
