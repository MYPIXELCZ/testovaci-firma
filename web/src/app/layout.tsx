import type { Metadata } from "next";
import Link from "next/link";
import { COMPANY, PRODUCT, SITE_URL } from "@/lib/config";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "Ano, beru: svatební plánovač pro Excel a Google Tabulky", template: "%s · Ano, beru" },
  description:
    "Naplánujte si svatbu v klidu. Rozpočet, hosté, úkoly s termíny a harmonogram dne D v jedné tabulce. " +
    `Jednorázově za ${PRODUCT.price} Kč, doručení e-mailem.`,
  openGraph: { type: "website", locale: "cs_CZ", siteName: "Ano, beru", images: ["/og.png"] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="cs">
      <body>
        <header className="header">
          <div className="wrap">
            <Link href="/" aria-label="Ano, beru – úvod">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/logo.svg" alt="Ano, beru" className="logo" width={150} height={37} />
            </Link>
            <nav>
              <Link href="/#co-najdete" className="navlink">Co najdete</Link>
              <Link href="/#jak-to-funguje" className="navlink">Jak to funguje</Link>
              <Link href="/#otazky" className="navlink">Otázky</Link>
              <Link href="/objednat" className="btn btn-small">Koupit</Link>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="wrap">
            <div>
              <p style={{ margin: 0 }}>
                Ano, beru provozuje {COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico},<br />
                {COMPANY.register}. {COMPANY.vat}
              </p>
            </div>
            <ul>
              <li><Link href="/svatebni-checklist">Svatební checklist</Link></li>
              <li><Link href="/obchodni-podminky">Obchodní podmínky</Link></li>
              <li><Link href="/ochrana-osobnich-udaju">Ochrana osobních údajů</Link></li>
              <li><a href={`mailto:${COMPANY.email}`}>{COMPANY.email}</a></li>
            </ul>
          </div>
        </footer>
      </body>
    </html>
  );
}
