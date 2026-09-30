import Link from "next/link";
import { headers } from "next/headers";
import { after } from "next/server";
import { track } from "@/lib/track";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import Icon from "@/components/Icon";
import Image from "next/image";
import ukazka from "@/content/ukazka.json";
import { LAUNCH_DATE, PRICE } from "@/lib/config";

// Témata kompletní sady (matematika, jednotná přijímací zkouška pro čtyřleté obory).
const TOPICS = [
  "Zlomky a desetinná čísla", "Procenta", "Poměr a úměrnost", "Mocniny a odmocniny",
  "Výrazy a mnohočleny", "Lineární rovnice", "Slovní úlohy (pohyb, práce, směsi)", "Jednotky a převody",
  "Úhly a trojúhelníky", "Obvody a obsahy", "Pythagorova věta", "Tělesa: objem a povrch",
];

type Props = { searchParams: Promise<Record<string, string | string[] | undefined>> };

export default async function Home({ searchParams }: Props) {
  const sp = await searchParams;
  const src = String(sp.utm_source ?? sp.src ?? "").slice(0, 40).replace(/[^\w.-]/g, "");
  const ua = (await headers()).get("user-agent");
  after(() => track("visit", src, ua));
  const preview = ukazka.tasks.filter((t) => ["Složený zlomek", "Slovní úloha"].includes(t.topic)).slice(0, 2);

  return (
    <>
      <Beacon page="home" />
      <section className="hero">
        <div className="wrap hero-grid">
          <div>
          <p className="eyebrow">Přijímačky na SŠ 2027 · matematika</p>
          <h1>Přijímačky z matiky po tématech</h1>
          <p className="lead">
            Víte, že vaše dítě nejistí zlomky nebo slovní úlohy? Místo dalšího celého testu mu dejte sadu úloh přesně na to
            téma. U každé úlohy je postup řešení krok za krokem. Na papíře, bez videí a bez obrazovky.
          </p>
          <div className="actions">
            <a href="#ukazka" className="btn" data-track="cta_sample">Stáhnout ukázku zdarma</a>
            <Link href={`/koupit${src ? `?src=${src}` : ""}`} className="btn btn-ghost" data-track="cta_buy">Koupit sadu za {PRICE} Kč</Link>
          </div>
          </div>
          <div className="papers" aria-label="Ukázka stránek sady">
            <Image src="/nahled-ulohy.webp" alt="Stránka s úlohami na zlomky a místem na počítání" width={909} height={719} priority className="paper paper-back" />
            <Image src="/nahled-postup.webp" alt="Stránka s postupy řešení krok za krokem" width={909} height={719} priority className="paper paper-front" />
          </div>
        </div>
      </section>

      <section>
        <div className="wrap">
          <div className="grid">
            <div className="card"><Icon name="target" /><h3>Podle témat, ne podle testů</h3><p className="muted" style={{ margin: 0 }}>Procvičíte přesně to, co nejde. Zlomky zvlášť, procenta zvlášť.</p></div>
            <div className="card"><Icon name="steps" /><h3>Postup u každé úlohy</h3><p className="muted" style={{ margin: 0 }}>Ne jen výsledek. Dítě vidí, kde udělalo chybu, a rodič nemusí nic vysvětlovat.</p></div>
            <div className="card"><Icon name="print" /><h3>K tisku</h3><p className="muted" style={{ margin: 0 }}>PDF, které si vytisknete, kolikrát chcete. Počítá se s tužkou, jako u zkoušky.</p></div>
            <div className="card"><Icon name="calendar" /><h3>Plán do 12. dubna</h3><p className="muted" style={{ margin: 0 }}>Úvodní test ukáže slabá místa a plán rozvrhne procvičování až do zkoušky.</p></div>
          </div>
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <h2>Co v sadě bude</h2>
          <ol className="topics">{TOPICS.map((t) => <li key={t}>{t}</li>)}</ol>
          <p className="muted small">
            Chcete si to vyzkoušet hned? Příklady s postupem: <Link href="/zlomky-prijimacky" data-track="topic_link">zlomky</Link>,{" "}
            <Link href="/procenta-prijimacky" data-track="topic_link">procenta</Link>, <Link href="/rovnice-prijimacky" data-track="topic_link">rovnice</Link>,{" "}
            <Link href="/slovni-ulohy-prijimacky" data-track="topic_link">slovní úlohy</Link>.
            Všechny úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky. Výsledky ověřujeme výpočtem. Sada není
            oficiálním materiálem CERMAT.
          </p>
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <h2>Ukázka: jak vypadá postup</h2>
          {preview.map((t) => (
            <div className="task" key={t.text}>
              <span className="tag">{t.topic}</span>
              <p className="q"><MathText text={t.text} /></p>
              <ol>{t.steps.map((s) => <li key={s}><MathText text={s} /></li>)}</ol>
              <p className="a">Výsledek: <MathText text={t.answer} /></p>
            </div>
          ))}
        </div>
      </section>

      <section id="ukazka">
        <div className="wrap narrow">
          <div className="box">
            <h2 style={{ marginTop: 0 }}>Ukázka zdarma: {ukazka.tasks.length} úloh na zlomky</h2>
            <p>PDF k tisku: úlohy s místem na počítání a na konci postupy řešení.</p>
            <LeadForm
              source="ukazka"
              src={src}
              button="Stáhnout ukázku"
              consentText={`Souhlasím se zasláním upozornění, až bude kompletní sada k dispozici (${LAUNCH_DATE}).`}
              done="Děkujeme! Ukázka je připravená ke stažení."
            />
          </div>
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <Feedback />
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <h2>Časté otázky</h2>
          <dl className="faq">
            <dt>Kdy bude kompletní sada?</dt>
            <dd>{LAUNCH_DATE}. Do zkoušky 12. dubna 2027 tak zbývá dost času na procvičení všech témat.</dd>
            <dt>Pro koho je?</dt>
            <dd>Pro žáky 9. tříd, kteří dělají jednotnou přijímací zkoušku na čtyřleté obory s maturitou.</dd>
            <dt>Je to oficiální materiál?</dt>
            <dd>Ne. Úlohy jsou vlastní, ve stylu zkoušky. Oficiální testy z minulých let najdete zdarma na webu CERMAT a doporučujeme je projít také.</dd>
            <dt>Zaručíte přijetí?</dt>
            <dd>Ne, to nemůže slíbit nikdo. Sada pomáhá procvičit slabá místa, výsledek je na přípravě.</dd>
          </dl>
        </div>
      </section>
    </>
  );
}
