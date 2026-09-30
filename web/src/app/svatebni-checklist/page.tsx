import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";
import planner from "@/content/planner.json";

export const metadata: Metadata = articleMetadata(
  "svatebni-checklist",
  "Svatební checklist: co zařídit a kdy, měsíc po měsíci",
  "Kompletní svatební checklist od zásnub po svatební cestu. Co zařídit rok předem, co tři měsíce předem a na co se nejčastěji zapomíná.",
);

const phases = [...new Set(planner.tasks.map((t) => t.phase))];

export default function ChecklistPage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Svatební checklist: co zařídit a kdy</h1>
        <p className="lead">
          Od zásnub po svatební cestu, seřazeno podle toho, kolik času do svatby zbývá. Celkem {planner.tasks.length} úkolů,
          na které se při přípravách nejčastěji myslí, i těch, na které se zapomíná.
        </p>

        <p>
          <a className="btn btn-ghost btn-small" href="/ke-stazeni/svatebni-checklist-anoberu.pdf" download>
            Stáhnout checklist k tisku (PDF, zdarma)
          </a>
        </p>

        <div className="tip">
          <p>
            <strong>Máte na přípravu méně než rok?</strong> Nic se neděje. Nejdřív zajistěte místo, oddávajícího a fotografa,
            protože ti se vyprodávají nejdřív. Zbytek seznamu doženete postupně.
          </p>
        </div>

        {phases.map((phase) => (
          <div key={phase}>
            <h2>{phase === "Den D" || phase === "Po svatbě" || phase === "Poslední týden" ? phase : `${phase} před svatbou`}</h2>
            <ul>
              {planner.tasks.filter((t) => t.phase === phase).map((t) => <li key={t.task}>{t.task}</li>)}
            </ul>
          </div>
        ))}

        <h2>Na co se nejčastěji zapomíná</h2>
        <ul>
          <li>
            <strong>Dotazník na matrice.</strong> Podává se předem a spolu s doklady. Jaké doklady a v jaké lhůtě chce
            vaše matrika, si ověřte přímo u ní, liší se to podle místa a situace.
          </li>
          <li><strong>Doplatky dodavatelům.</strong> Zálohy se platí měsíce předem, doplatky často v hotovosti v den svatby. Připravte si obálky.</li>
          <li><strong>Nouzová taška.</strong> Jehla a nit, náplasti, léky na bolest hlavy, deodorant, nabíječka.</li>
          <li><strong>Jídlo pro vás dva.</strong> Novomanželé mají celý den program a často nestihnou sníst ani oběd.</li>
          <li><strong>Doklady po svatbě.</strong> Pokud měníte příjmení, čekají vás nové doklady a nahlášení změny bance, pojišťovně i zaměstnavateli.</li>
        </ul>

        <ArticleCta
          title="Termíny si hlídat nemusíte"
          text={`V našem plánovači je celý tento checklist. Zadáte datum svatby a u každého úkolu se dopočítá konkrétní termín. Co je po termínu, zčervená, a na přehledu vidíte, co vás čeká nejdřív.`}
        />
      </article>
    </section>
  );
}
