// Zlomky „a/b“ (čísla i proměnné x/2) v textu úlohy zobrazí nad sebou (stejně jako v PDF).
// Jednotky jako km/h se nesází jako zlomek: vlevo musí být číslo nebo proměnná a–d, n, x, y.
const FRACTION = /(?<![\p{L}\d,])(−?(?:\d+(?:,\d+)?|[a-dnxy]))\/(\d+(?:,\d+)?|[a-dnxy])(?![\p{L}\d(])/gu;

export default function MathText({ text }: { text: string }) {
  const out: React.ReactNode[] = [];
  let last = 0;
  for (const m of text.matchAll(FRACTION)) {
    out.push(text.slice(last, m.index));
    out.push(
      <span className="fr" key={m.index} aria-label={`${m[1]} lomeno ${m[2]}`}><span>{m[1]}</span><span>{m[2]}</span></span>,
    );
    last = m.index + m[0].length;
  }
  out.push(text.slice(last));
  return <>{out}</>;
}
