import "server-only";

// Fio API: https://www.fio.cz/docs/cz/API_Bankovnictvi.pdf
// Vlastní token jen pro čtení (env FIO_TOKEN), jiný než u anoberu, ať se limity nesčítají. Limit: jeden dotaz na token za 30 s, jinak HTTP 409.
const BASE = process.env.FIO_API_BASE ?? "https://fioapi.fio.cz/v1/rest";

export type IncomingPayment = { id: string; amount: number; currency: string; vs: string; date: string };

type Column = { value: string | number } | null;
type FioTransaction = Record<string, Column>;

const iso = (d: Date) => d.toISOString().slice(0, 10);

/** Příchozí platby za posledních `days` dní. Dotaz podle období je idempotentní, na rozdíl od „last“. */
export async function incomingPayments(days = 5, tokenOverride?: string): Promise<IncomingPayment[]> {
  const token = tokenOverride ?? process.env.FIO_TOKEN;
  if (!token) throw new Error("FIO_TOKEN není nastaven");
  const to = new Date();
  const from = new Date(to.getTime() - days * 86_400_000);
  const res = await fetch(`${BASE}/periods/${token}/${iso(from)}/${iso(to)}/transactions.json`, { cache: "no-store" });
  if (res.status === 409) throw new Error("Fio API: moc častý dotaz, zkuste to za 30 s");
  if (!res.ok) throw new Error(`Fio API odpovědělo ${res.status}`);
  const data = await res.json();
  const txs: FioTransaction[] = data?.accountStatement?.transactionList?.transaction ?? [];
  return txs
    .map((t) => ({
      id: String(t.column22?.value ?? ""),
      amount: Number(t.column1?.value ?? 0),
      currency: String(t.column14?.value ?? ""),
      vs: String(t.column5?.value ?? "").replace(/^0+/, ""),
      date: String(t.column0?.value ?? ""),
    }))
    .filter((p) => p.id && p.amount > 0);
}
