"use client";

import { useEffect } from "react";

export default function Error({ error, retry }: { error: Error & { digest?: string }; retry: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <section>
      <div className="wrap narrow">
        <p className="eyebrow">Něco se pokazilo</p>
        <h1>Omlouváme se, stránku se nepodařilo načíst</h1>
        <p className="muted">
          Zkuste to prosím znovu. Pokud jste právě platili, nic se neztratilo: platbu spárujeme a plánovač vám pošleme e-mailem.
          Když potíže trvají, napište nám na anoberu@mypixel.cz.
        </p>
        <p style={{ marginTop: 28 }}>
          <button className="btn" onClick={() => retry()}>Zkusit znovu</button>
        </p>
      </div>
    </section>
  );
}
