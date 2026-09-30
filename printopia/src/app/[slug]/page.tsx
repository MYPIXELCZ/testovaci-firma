import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import { TOPICS } from "@/content/temata";
import { LAUNCH_DATE, PRICE } from "@/lib/config";

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
          <p>8 úloh na zlomky jako PDF s místem na počítání a postupy na konci.</p>
          <LeadForm
            source="ukazka"
            src={topic.slug.replace("-prijimacky", "")}
            button="Stáhnout PDF zdarma"
            consentText={`Souhlasím se zasláním upozornění, až bude kompletní sada k dispozici (${LAUNCH_DATE}).`}
            done="Děkujeme! PDF je připravené ke stažení."
          />
        </div>

        <div style={{ marginTop: 32 }}><Feedback /></div>

        <p style={{ marginTop: 32 }}>
          Další témata: <Link href="/zlomky-prijimacky">zlomky</Link>
          {Object.values(TOPICS).filter((o) => o.slug !== topic.slug).map((o) => (
            <span key={o.slug}>, <Link href={`/${o.slug}`}>{o.h1.split(" na ")[0].toLowerCase()}</Link></span>
          ))}
          . Připravujeme kompletní sadu na všech 12 témat za {PRICE} Kč, <Link href="/">co v ní bude</Link>.
        </p>
      </div>
    </section>
  );
}
