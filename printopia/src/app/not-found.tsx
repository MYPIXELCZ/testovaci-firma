import Link from "next/link";

export default function NotFound() {
  return (
    <section className="hero">
      <div className="wrap narrow">
        <p className="eyebrow">Chyba 404</p>
        <h1>Tahle stránka tu není</h1>
        <p><Link href="/" className="btn">Zpět na úvod</Link></p>
      </div>
    </section>
  );
}
