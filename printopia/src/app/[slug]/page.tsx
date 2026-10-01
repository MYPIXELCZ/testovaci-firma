import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import { TOPICS } from "@/content/temata";
import { PRICE } from "@/lib/config";

export const dynamicParams = false;
export const generateStaticParams = () => Object.keys(TOPICS).map((slug) => ({ slug }));

export async function generateMetadata({ params }: PageProps<"/[slug]">): Promise<Metadata> {
  const topic = TOPICS[(await params).slug];
  if (!topic) return {};
  return { title: topic.title, description: topic.description, alternates: { canonical: `/${topic.slug}` } };
}

export default async function TopicPage({ params }: PageProps<"/[slug]">) {
  const topic = TOPICS[(await params).slug];
  if (!topic) notFound();
  return (
    <section className="hero">
      <Beacon page="tema" topic={topic.slug} />
      <div className="wrap narrow">
        <p className="eyebrow">Přijímačky z matematiky</p>
        <h1>{topic.h1}</h1>
        <p className="lead">{topic.lead}</p>

        <h2>Na co si dát pozor</h2>
        <ul>{topic.tips.map((tip) => <li key={tip}><MathText text={tip} /></li>)}</ul>

        <h2>Příklady</h2>
        {topic.tasks.map((t, i) => (
          <div className="task" key={t.text}>
            <span className="tag">{t.topic}</span>
            <p className="q">{i + 1}. <MathText text={t.text} /></p>
            <details>
              <summary className="small" style={{ cursor: "pointer", color: "var(--blue)" }}>Zobrazit postup a výsledek</summary>
              <ol>{t.steps.map((s) => <li key={s}><MathText text={s} /></li>)}</ol>
              <p className="a">Výsledek: <MathText text={t.answer} /></p>
            </details>
          </div>
        ))}

        <div className="box" style={{ marginTop: 32 }}>
          <h2 style={{ marginTop: 0 }}>Ukázka k tisku zdarma</h2>
          <p>8 úloh na zlomky jako PDF s místem na počítání a postupy na konci. Stáhnete ho bez e-mailu.</p>
          <p><a className="btn" href="/ukazka-zlomky.pdf" download data-track="pdf_download">Stáhnout PDF zdarma</a></p>
          <details className="tips-box">
            <summary>Chci k tomu i tipy na přípravu e-mailem</summary>
            <LeadForm
              source="ukazka"
              src={topic.slug.replace("-prijimacky", "")}
              button="Posílejte mi tipy"
              consentText="Souhlasím se zasíláním tipů k přípravě na přijímačky a nabídek Printopie (nejvýše dvakrát měsíčně)."
              done="Děkujeme! Tipy vám budeme posílat nejvýše dvakrát měsíčně a odhlásit se můžete kdykoli."
            />
          </details>
        </div>

        <div style={{ marginTop: 32 }}><Feedback /></div>

        <p style={{ marginTop: 32 }}>
          Další témata: <Link href="/zlomky-prijimacky">zlomky</Link>
          {Object.values(TOPICS).filter((o) => o.slug !== topic.slug).map((o) => (
            <span key={o.slug}>, <Link href={`/${o.slug}`}>{o.h1.split(" na ")[0].toLowerCase()}</Link></span>
          ))}
          . Kompletní sada všech 12 témat k tisku stojí {PRICE} Kč, <Link href="/">podívejte se, co v ní je</Link>.
        </p>
      </div>
    </section>
  );
}
