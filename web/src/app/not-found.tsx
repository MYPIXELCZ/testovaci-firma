import Link from "next/link";
import { COMPANY } from "@/lib/config";

export default function NotFound() {
  return (
    <section>
      <div className="wrap narrow">
        <p className="eyebrow">Chyba 404</p>
        <h1>Tahle stránka tu není</h1>
        <p className="muted">
          Odkaz je možná neúplný nebo už neplatí. Pokud hledáte svou objednávku, použijte odkaz z e-mailu, nebo nám napište na{" "}
          <a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a>.
        </p>
        <p style={{ marginTop: 28 }}>
          <Link href="/" className="btn">Zpět na úvod</Link>
        </p>
      </div>
    </section>
  );
}
