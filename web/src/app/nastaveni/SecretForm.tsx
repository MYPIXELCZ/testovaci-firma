"use client";

import { useActionState } from "react";
import type { SaveState } from "./actions";

type Props = {
  label: string;
  hint: string;
  isSet: boolean;
  action: (prev: SaveState, form: FormData) => Promise<SaveState>;
};

export default function SecretForm({ label, hint, isSet, action }: Props) {
  const [state, formAction, pending] = useActionState(action, null);
  return (
    <form action={formAction} className="form card" style={{ marginBottom: 24 }}>
      <div className="field">
        <label>
          {label} {isSet && !state && <span className="muted small">(uloženo, novým se přepíše)</span>}
        </label>
        <input type="text" name="token" autoComplete="off" spellCheck={false} required />
        <p className="muted small" style={{ margin: "6px 0 0" }}>{hint}</p>
      </div>
      {state && <p className={state.ok ? "" : "error"} style={{ margin: 0 }}>{state.message}</p>}
      <div>
        <button className="btn btn-small" type="submit" disabled={pending}>{pending ? "Ověřuji…" : "Uložit"}</button>
      </div>
    </form>
  );
}
