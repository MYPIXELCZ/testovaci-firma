// Zlomky „a/b“ v textu úlohy zobrazí nad sebou (stejně jako v PDF).
export default function MathText({ text }: { text: string }) {
  const parts = text.split(/(\d+\/\d+)/g);
  return (
    <>
      {parts.map((p, i) => {
        const m = /^(\d+)\/(\d+)$/.exec(p);
        return m ? (
          <span className="fr" key={i} aria-label={`${m[1]} lomeno ${m[2]}`}><span>{m[1]}</span><span>{m[2]}</span></span>
        ) : (
          p
        );
      })}
    </>
  );
}
