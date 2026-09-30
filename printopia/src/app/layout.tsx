import type { Metadata } from "next";
import Link from "next/link";
import { COMPANY, CONTACT, SITE_URL } from "@/lib/config";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "Přijímačky z matiky po tématech · Printopia", template: "%s · Printopia" },
  description:
    "Sady úloh k tisku na přijímačky z matematiky, rozdělené podle témat. U každé úlohy postup řešení krok za krokem. Ukázka zdarma.",
  openGraph: { type: "website", locale: "cs_CZ", siteName: "Printopia" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="cs">
      <body>
        <header className="header">
          <div className="wrap">
            <Link href="/" className="logo" aria-label="Printopia – úvod">Printopia<span>.</span></Link>
            <Link href="/#ukazka" className="small">Ukázka zdarma</Link>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="wrap">
            <p style={{ margin: 0 }}>
              Printopia provozuje {COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico},<br />
              {COMPANY.register}.
            </p>
            <p style={{ margin: 0 }}>
              <Link href="/ochrana-osobnich-udaju">Ochrana osobních údajů</Link> ·{" "}
              <a href={`mailto:${CONTACT}`}>{CONTACT}</a>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
