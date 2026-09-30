"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

/** Každých 15 s se zeptá na stav objednávky a po zaplacení překreslí stránku. */
export default function WaitForPayment({ id }: { id: string }) {
  const router = useRouter();
  useEffect(() => {
    const timer = setInterval(async () => {
      const res = await fetch(`/api/orders/${id}`, { cache: "no-store" }).catch(() => null);
      const data = res?.ok ? await res.json() : null;
      if (data?.status === "paid") {
        clearInterval(timer);
        router.refresh();
      }
    }, 15_000);
    return () => clearInterval(timer);
  }, [id, router]);

  return (
    <span className="status">
      <span className="dot" /> Čekáme na platbu
    </span>
  );
}
