import Link from "next/link";
import { PRODUCT } from "@/lib/config";
import Feedback from "@/components/Feedback";

export default function ArticleCta({ title, text }: { title: string; text: string }) {
  return (
    <div className="cta-box">
      <h2>{title}</h2>
      <p className="muted">{text}</p>
      <p style={{ display: "flex", gap: 16, flexWrap: "wrap", alignItems: "center", margin: 0 }}>
        <Link href="/objednat" className="btn" data-track="cta_buy">Koupit plánovač za {PRODUCT.price} Kč</Link>
        <Link href="/" className="small">Co v plánovači najdete</Link>
      </p>
      <div style={{ marginTop: 24 }}><Feedback /></div>
    </div>
  );
}
