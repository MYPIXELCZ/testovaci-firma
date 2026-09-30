import Link from "next/link";
import { PRODUCT } from "@/lib/config";

export default function ArticleCta({ title, text }: { title: string; text: string }) {
  return (
    <div className="cta-box">
      <h2>{title}</h2>
      <p className="muted">{text}</p>
      <p style={{ display: "flex", gap: 16, flexWrap: "wrap", alignItems: "center", margin: 0 }}>
        <Link href="/objednat" className="btn">Koupit plánovač za {PRODUCT.price} Kč</Link>
        <Link href="/" className="small">Co v plánovači najdete</Link>
      </p>
    </div>
  );
}
