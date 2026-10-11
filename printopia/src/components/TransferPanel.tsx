"use client";

import { useRef } from "react";

// Sbalitelný panel „Zaplatit převodem“. Při prvním otevření pošle kupujícímu e-mail s platebními údaji (jen když je k dispozici i karta).
export default function TransferPanel({ id, notifyOnOpen, children }: { id: string; notifyOnOpen: boolean; children: React.ReactNode }) {
  const sent = useRef(false);
  return (
    <details
      className="transfer"
      onToggle={(e) => {
        if ((e.currentTarget as HTMLDetailsElement).open && notifyOnOpen && !sent.current) {
          sent.current = true;
          fetch(`/api/orders/${id}/instructions`, { method: "POST" }).catch(() => undefined);
        }
      }}
    >
      <summary>Zaplatit bankovním převodem (QR kód)</summary>
      <div className="transfer-body">{children}</div>
    </details>
  );
}
