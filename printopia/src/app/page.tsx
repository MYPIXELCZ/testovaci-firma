import Image from "next/image";
import Link from "next/link";
import { headers } from "next/headers";
import { after } from "next/server";
import Beacon from "@/components/Beacon";
import Feedback from "@/components/Feedback";
import Icon from "@/components/Icon";
import LeadForm from "@/components/LeadForm";
import MathText from "@/components/MathText";
import foto from "@/content/foto.json";
import ukazka from "@/content/ukazka.json";
import { COMPANY, CONTACT, LAUNCH_DATE, PRICE } from "@/lib/config";
import { track } from "@/lib/track";

// Cílová skupina (plan/prijimacky.md 1b): hledají deváťáci, platí rodiče i žáci 15+ (měří test).
// Prodejní sdělení pro dospělé, žákům jen informace; žádná výzva dětem ke koupi. Design: plan/design-prijimacky.md.
const TOPICS = [
  "Zlomky a desetinná čísla", "Procenta", "Poměr a úměrnost", "Mocniny a odmocniny",
  "Výrazy a mnohočleny", "Lineární rovnice", "Slovní úlohy (pohyb, práce, směsi)", "Jednotky a převody",
  "Úhly a trojúhelníky", "Obvody a obsahy", "Pythagorova věta", "Tělesa: objem a povrch",
];
const EXAM = new Date("2027-04-12T08:00:00+02:00");

// Srovnání ceny přípravy, zdroje v plan/research-2026-10-01.md a plan/zdroje-2026-10-01/konkurence-prijimacky.md.
const PRICES: [string, string][] = [
  ["Doučování s lektorem", "200–350 Kč za hodinu"],
  ["Online videokurz", "od 3 990 Kč"],
  ["Videořešení testů", "7 900–9 900 Kč"],
];

type Props = { searchParams: Promise<Record<string, string | string[] | undefined>> };

export default async function Home({ searchParams }: Props) {
  const sp = await searchParams;
  const src = String(sp.utm_source ?? sp.src ?? "").slice(0, 40).replace(/[^\w.-]/g, "");
  const ua = (await headers()).get("user-agent");
  after(() => track("visit", src, ua));
  const days = Math.max(0, Math.ceil((EXAM.getTime() - Date.now()) / 86_400_000));
  const w = Math.max(1, Math.floor(days / 7 / 12));
  const perTopic = w === 1 ? "týden" : w < 5 ? `${w} týdny` : `${w} týdnů`;
  const preview = ukazka.tasks.filter((t) => ["Složený zlomek", "Slovní úloha"].includes(t.topic)).slice(0, 2);
  const buyHref = `/koupit${src ? `?src=${src}` : ""}`;

  return (
    <>
      <Beacon page="home" />

      <section className="hero-dark">
        <div className="wrap hero-grid">
          <div>
            <p className="eyebrow eyebrow-light">Přijímačky na SŠ 2027 · matematika</p>
            <h1>Procvičte přesně to téma, které na přijímačkách nejde</h1>
            <ul className="checks">
              <li><strong>12 témat</strong> podle jednotné přijímací zkoušky, každé zvlášť</li>
              <li><strong>Postup krok za krokem</strong> u každé úlohy, ne jen výsledek</li>
              <li><strong>PDF k tisku</strong>: počítá se tužkou, jako u zkoušky</li>
              <li><strong>Plán procvičování</strong> až do 12. dubna 2027</li>
            </ul>
            <div className="actions">
              <Link href={buyHref} className="btn btn-yellow" data-track="cta_buy">Koupit sadu za {PRICE} Kč</Link>
              <a href="#ukazka" className="btn btn-outline-light" data-track="cta_sample">8 úloh zdarma</a>
            </div>
            <p className="trust">Jednorázová platba, bez předplatného · 14 dní na vrácení peněz · Provozuje {COMPANY.name}</p>
          </div>
          <div className="hero-visual">
            <Image src="/foto/rodic-a-dcera-1400.webp" width={1400} height={788} priority sizes="(max-width: 800px) 100vw, 520px"
                   alt="Maminka pomáhá dceři s úlohami u psacího stolu" className="hero-photo" />
            <Image src="/nahled-postup.webp" width={909} height={719} alt="Stránka sady s postupy řešení krok za krokem" className="hero-paper" />
            <p className="credit">Foto: <a href={foto["rodic-a-dcera"].author_url}>{foto["rodic-a-dcera"].author}</a>, <a href={foto["rodic-a-dcera"].page}>Unsplash</a></p>
          </div>
        </div>
      </section>

      <div className="strip">
        <div className="wrap strip-inner">
          <span className="strip-num">{days}</span>
          <span>dní do přijímaček. Kdo začne teď, má na každé z 12 témat zhruba {perTopic} v klidu.</span>
        </div>
      </div>

      <section>
        <div className="wrap">
          <div className="two">
            <div className="card card-photo">
              <Image src="/foto/rodic-podpora-800.webp" width={800} height={450} sizes="(max-width: 800px) 100vw, 460px"
                     alt="Maminka povzbuzuje dceru při učení" className="card-img" />
              <p className="credit credit-dark">Foto: <a href={foto["rodic-podpora"].author_url}>{foto["rodic-podpora"].author}</a>, <a href={foto["rodic-podpora"].page}>Unsplash</a></p>
              <p className="eyebrow">Pro rodiče</p>
              <ul className="checks checks-dark">
                <li><strong>Nemusíte umět matiku.</strong> Postup je u každé úlohy, stačí zkontrolovat výsledek.</li>
                <li><strong>Víte, na čem dítě je.</strong> Úvodní test ukáže slabá témata, plán rozvrhne čas.</li>
                <li><strong>Za cenu jedné až dvou hodin doučování.</strong> A dá se tisknout znovu.</li>
              </ul>
            </div>
            <div className="card card-photo">
              <Image src="/foto/sesit-matematika-800.webp" width={800} height={600} sizes="(max-width: 800px) 100vw, 460px"
                     alt="Žák počítá úlohy z matematiky do sešitu" className="card-img" />
              <p className="credit credit-dark">Foto: <a href={foto["sesit-matematika"].author_url}>{foto["sesit-matematika"].author}</a>, <a href={foto["sesit-matematika"].page}>Unsplash</a></p>
              <p className="eyebrow">Pro deváťáky</p>
              <ul className="checks checks-dark">
                <li><strong>Jen to, co nejde.</strong> Zlomky zvlášť, procenta zvlášť, žádné zbytečné testy dokola.</li>
                <li><strong>Když se zasekneš,</strong> postup ukáže krok, kde se výpočet rozešel.</li>
                <li><strong>Na papíře,</strong> bez obrazovky, stejně jako u zkoušky.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="soft">
        <div className="wrap narrow">
          <p className="eyebrow">Ukázka</p>
          <h2 style={{ marginTop: 0 }}>Takhle vypadá postup řešení</h2>
          {preview.map((t) => (
            <div className="task" key={t.text}>
              <span className="tag">{t.topic}</span>
              <p className="q"><MathText text={t.text} /></p>
              <ol>{t.steps.map((s) => <li key={s}><MathText text={s} /></li>)}</ol>
              <p className="a">Výsledek: <MathText text={t.answer} /></p>
            </div>
          ))}
          <p className="small muted">
            Víc příkladů zdarma: <Link href="/zlomky-prijimacky" data-track="topic_link">zlomky</Link>,{" "}
            <Link href="/procenta-prijimacky" data-track="topic_link">procenta</Link>, <Link href="/rovnice-prijimacky" data-track="topic_link">rovnice</Link>,{" "}
            <Link href="/slovni-ulohy-prijimacky" data-track="topic_link">slovní úlohy</Link> a{" "}
            <Link href="/jak-se-pripravit-na-prijimacky" data-track="topic_link">plán přípravy od října do dubna</Link>.
          </p>
        </div>
      </section>

      <section>
        <div className="wrap narrow">
          <p className="eyebrow">Obsah sady</p>
          <h2 style={{ marginTop: 0 }}>12 témat, která se na přijímačkách opakují</h2>
          <ol className="topics">{TOPICS.map((t) => <li key={t}>{t}</li>)}</ol>
          <p className="muted small">
            Všechny úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky. Každý výsledek ověřujeme výpočtem. Sada není
            oficiálním materiálem CERMAT.
          </p>
        </div>
      </section>

      <section className="soft">
        <div className="wrap narrow">
          <p className="eyebrow">Cena</p>
          <h2 style={{ marginTop: 0 }}>Kolik stojí příprava na přijímačky</h2>
          <table className="compare">
            <tbody>
              {PRICES.map(([k, v]) => <tr key={k}><td>{k}</td><td className="num">{v}</td></tr>)}
              <tr className="us"><td><strong>Sada Printopia</strong>, 12 témat k tisku s postupy</td><td className="num"><strong>{PRICE} Kč jednorázově</strong></td></tr>
            </tbody>
          </table>
          <p className="small muted">Ceny konkurence podle veřejných ceníků a článků k 1. 10. 2026. Doučování a kurzy dávají víc než sada, ta je levný začátek nebo doplněk.</p>
          <div className="actions"><Link href={buyHref} className="btn btn-yellow" data-track="cta_buy">Koupit sadu za {PRICE} Kč</Link></div>
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
          <div className="guarantee">
            <Icon name="target" />
            <div>
              <h3>Nic neriskujete</h3>
              <p className="muted" style={{ margin: 0 }}>
                Když vám sada nesedne, do 14 dnů vrátíme peníze, bez vysvětlování. Platíte jednou, převodem nebo QR kódem,
                žádné předplatné ani karta.
              </p>
            </div>
          </div>
          <div style={{ marginTop: 24 }}><Feedback /></div>
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
            <dt>Kdo za Printopií stojí?</dt>
            <dd>{COMPANY.name}, {COMPANY.address}, IČO {COMPANY.ico}. Napište nám na <a href={`mailto:${CONTACT}`}>{CONTACT}</a>.</dd>
          </dl>
        </div>
      </section>

      <div className="sticky-cta">
        <Link href={buyHref} className="btn btn-yellow" data-track="cta_buy">Koupit sadu za {PRICE} Kč</Link>
      </div>
    </>
  );
}
