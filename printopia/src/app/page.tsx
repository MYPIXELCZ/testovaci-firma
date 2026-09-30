import Link from "next/link";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
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
  console.log(JSON.stringify({ ev: "visit", page: "/", src }));
  const preview = ukazka.tasks.filter((t) => ["Složený zlomek", "Slovní úloha"].includes(t.topic)).slice(0, 2);

  return (
    <>
      <section className="hero">
        <div className="wrap">
          <p className="eyebrow">Přijímačky na SŠ 2027 · matematika</p>
          <h1>Přijímačky z matiky po tématech</h1>
          <p className="lead">
            Víte, že vaše dítě nejistí zlomky nebo slovní úlohy? Místo dalšího celého testu mu dejte sadu úloh přesně na to
            téma. U každé úlohy je postup řešení krok za krokem. Na papíře, bez videí a bez obrazovky.
          </p>
          <div className="actions">
            <a href="#ukazka" className="btn">Stáhnout ukázku zdarma</a>
            <Link href={`/koupit${src ? `?src=${src}` : ""}`} className="btn btn-ghost">Koupit sadu za {PRICE} Kč</Link>
          </div>
        </div>
      </section>

      <section>
        <div className="wrap">
          <div className="grid">
            <div className="card"><h3>Podle témat, ne podle testů</h3><p className="muted" style={{ margin: 0 }}>Procvičíte přesně to, co nejde. Zlomky zvlášť, procenta zvlášť.</p></div>
            <div className="card"><h3>Postup u každé úlohy</h3><p className="muted" style={{ margin: 0 }}>Ne jen výsledek. Dítě vidí, kde udělalo chybu, a rodič nemusí nic vysvětlovat.</p></div>
            <div className="card"><h3>K tisku</h3><p className="muted" style={{ margin: 0 }}>PDF, které si vytisknete, kolikrát chcete. Počítá se s tužkou, jako u zkoušky.</p></div>
            <div className="card"><h3>Plán do 12. dubna</h3><p className="muted" style={{ margin: 0 }}>Úvodní test ukáže slabá místa a plán rozvrhne procvičování až do zkoušky.</p></div>
          </div>
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <h2>Co v sadě bude</h2>
          <ul className="topics">{TOPICS.map((t) => <li key={t}>{t}</li>)}</ul>
          <p className="muted small">
            Chcete si to vyzkoušet hned? <Link href="/zlomky-prijimacky">Zlomky na přijímačky: 8 příkladů s postupem</Link>.
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
