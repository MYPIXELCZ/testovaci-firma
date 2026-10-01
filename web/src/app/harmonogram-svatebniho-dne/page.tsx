import type { Metadata } from "next";
import { articleMetadata } from "@/lib/seo";
import ArticleCta from "@/components/ArticleCta";
import planner from "@/content/planner.json";

export const metadata: Metadata = articleMetadata(
  "harmonogram-svatebniho-dne",
  "Harmonogram svatebního dne: vzor, který můžete převzít",
  "Vzorový harmonogram svatebního dne od ranní přípravy po půlnoční překvapení. S tradicemi, rezervami a tipy, jak den zvládnout v klidu.",
);

export default function SchedulePage() {
  return (
    <section>
      <article className="wrap article">
        <p className="eyebrow">Plánování svatby</p>
        <h1>Harmonogram svatebního dne: vzor k převzetí</h1>
        <p className="lead">
          Dobrý harmonogram nepotřebujete kvůli sobě. Potřebují ho fotograf, kapela, kuchyně i svědci. Když každý ví, co se
          kdy děje, vy dva si můžete den užít.
        </p>

        <h2>Vzorový harmonogram pro obřad v poledne</h2>
        <table className="data-table">
          <thead><tr><th>Čas</th><th>Co se děje</th><th>Kdo zajišťuje</th></tr></thead>
          <tbody>
            {planner.dayPlan.map((d) => (
              <tr key={d.time + d.what}><td className="num" style={{ textAlign: "left" }}>{d.time}</td><td>{d.what}</td><td className="muted">{d.who}</td></tr>
            ))}
          </tbody>
        </table>
        <p className="muted small">Časy posuňte podle začátku obřadu, rozestupy mezi body můžete nechat.</p>

        <h2>Jak harmonogram sestavit, aby vydržel</h2>
        <ul>
          <li>
            <strong>Mezi body nechte rezervu 15 až 30 minut.</strong> Gratulace a skupinové focení trvají vždycky déle, než
            se čeká.
          </li>
          <li>
            <strong>Focení novomanželů plánujte na pozdní odpoledne.</strong> Hodina před západem slunce dává nejhezčí světlo.
            S fotografem se domluvte předem.
          </li>
          <li>
            <strong>Určete jednoho koordinátora.</strong> Obvykle svědka nebo svědkyni. Hlídá čas, řeší dodavatele a vy se
            nemusíte o nic starat.
          </li>
          <li>
            <strong>Harmonogram pošlete všem předem.</strong> Fotografovi, kapele, místu konání, kadeřnici i svědkům. Stačí
            týden před svatbou.
          </li>
          <li><strong>Nezapomeňte jíst.</strong> Vyhraďte si v programu chvíli, kdy se vy dva v klidu najíte.</li>
        </ul>

        <h2>Tradice, se kterými počítejte</h2>
        <ul>
          <li><strong>Rozbití talíře.</strong> Před hostinou se rozbije talíř a novomanželé společně zametají střepy. Mají tím ukázat, že spolu zvládnou každou práci.</li>
          <li><strong>Krmení polévkou.</strong> Novomanželé se navzájem krmí polévkou z jednoho talíře, často s jedním ubrusem kolem krku.</li>
          <li><strong>Házení kytice.</strong> Svobodné ženy chytají kytici nevěsty. Která ji chytí, ta se prý vdá jako další.</li>
          <li><strong>Čepení nevěsty.</strong> O půlnoci dostane nevěsta čepec jako symbol přechodu mezi vdané ženy.</li>
        </ul>

        <ArticleCta
          title="Harmonogram je součástí plánovače"
          text="V listu Den D najdete tento harmonogram připravený k úpravě. Doplníte místa a kontakty a pošlete ho všem, kdo se na svatbě podílejí."
        />
      </article>
    </section>
  );
}
