import "server-only";
import type { Order } from "./orders";

/**
 * Faktury v účetním systému UOL (https://api.uol.cz). Aplikace po zaplacení vytvoří kontakt a POTVRZENOU fakturu
 * (daňový doklad stejně jako ručně účetní: standardní typ, nulová sazba, středisko Sídlo, účet Fio) a její PDF
 * přiloží k doručovacímu e-mailu. Fakturu NEOZNAČUJE jako zaplacenou, párování s bankou dělá účetní.
 * Zapíná se env UOL_AUTH ("e-mail:token", sensitive); bez něj se vystavuje starý doklad `/doklad/[id]`.
 */
const API = process.env.UOL_API_URL ?? "https://mypixel.ucetnictvi.uol.cz/api";
const PRODUCT = process.env.UOL_PRODUCT ?? "vyvoj_softwaru";
const BANK = process.env.UOL_BANK ?? "fio_801_czk";
const DEPARTMENT = process.env.UOL_DEPARTMENT ?? "sidlo";
const CONSTANT_SYMBOL = process.env.UOL_CONSTANT_SYMBOL ?? "308";
const ITEM_TEXT = "Digitální materiály";

export const uolEnabled = () => !!process.env.UOL_AUTH;

async function call(path: string, init: { method?: string; body?: unknown; accept?: string } = {}) {
  const res = await fetch(`${API}/v1/${path}`, {
    method: init.method ?? "GET",
    headers: {
      Authorization: `Basic ${Buffer.from(process.env.UOL_AUTH ?? "").toString("base64")}`,
      Accept: init.accept ?? "application/json",
      ...(init.body ? { "Content-Type": "application/json" } : {}),
    },
    body: init.body ? JSON.stringify(init.body) : undefined,
    signal: AbortSignal.timeout(20_000),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`UOL ${init.method ?? "GET"} ${path.split("?")[0]} odpověděl ${res.status}: ${(await res.text()).slice(0, 300)}`);
  return res;
}

const pragueDate = (iso: string) => new Date(iso).toLocaleDateString("sv-SE", { timeZone: "Europe/Prague" }); // RRRR-MM-DD
const czDate = (iso: string) => new Date(iso).toLocaleDateString("cs-CZ", { timeZone: "Europe/Prague" });

async function findContact(externalId: string): Promise<string | null> {
  const list = (await (await call(`contacts?external_id=${encodeURIComponent(externalId)}`)).json()) as { items?: { contact_id: string }[] };
  return list.items?.[0]?.contact_id ?? null;
}

async function ensureContact(o: Order): Promise<string> {
  const existing = await findContact(o.id);
  if (existing) return existing;
  const created = (await (
    await call("contacts", {
      method: "POST",
      body: {
        name: o.name,
        country_id: "CZ",
        external_id: o.id,
        addresses: [{ name: o.name, country_id: "CZ", email: o.email, address_types: ["accounting"] }],
      },
    })
  ).json()) as { contact_id: string };
  return created.contact_id;
}

/**
 * Vystaví (nebo při opakování najde už vystavenou) fakturu k zaplacené objednávce a vrátí její číslo a PDF v base64.
 * Když se faktura vystaví, ale PDF nejde stáhnout, vrátí číslo a `pdf: null` (faktura už existuje, nesmí se vystavit podruhé).
 */
export async function issueInvoice(o: Order): Promise<{ no: string; pdf: string | null }> {
  const found = (await (await call(`sales_invoices?external_id=${encodeURIComponent(o.id)}`)).json()) as { items?: { public_id: string }[] };
  let no = found.items?.[0]?.public_id;
  if (!no) {
    const paidAt = o.paidAt ?? new Date().toISOString();
    const how = o.paymentId?.startsWith("stripe_") ? "platební kartou" : "bankovním převodem";
    const created = (await (
      await call("sales_invoices", {
        method: "POST",
        body: {
          buyer_id: await ensureContact(o),
          status: "confirmed",
          external_id: o.id,
          payment_method: o.paymentId?.startsWith("stripe_") ? "credit_card" : "bank_transfer",
          constant_symbol: CONSTANT_SYMBOL,
          issue_date: pragueDate(paidAt),
          tax_payment_date: pragueDate(paidAt),
          note: `VS ${o.vs}`,
          text: `Již uhrazeno ${how} dne ${czDate(paidAt)}, nic neplaťte.`,
          consumption_country_id: "CZ",
          ...(BANK ? { bank_account_id: BANK } : {}),
          ...(DEPARTMENT ? { department_id: DEPARTMENT } : {}),
          items: [
            {
              product_id: PRODUCT,
              description: ITEM_TEXT,
              quantity: 1,
              unit_price: o.amount,
              unit_price_vat_inclusive: o.amount,
              vat_rate: 0,
              vat_calculation_method: "from_below",
            },
          ],
        },
      })
    ).json()) as { public_id: string };
    no = created.public_id;
  }
  try {
    const pdf = Buffer.from(await (await call(`sales_invoices/${encodeURIComponent(no)}`, { accept: "application/pdf" })).arrayBuffer());
    if (pdf.subarray(0, 4).toString() !== "%PDF") throw new Error("odpověď není PDF");
    return { no, pdf: pdf.toString("base64") };
  } catch (e) {
    console.error("[uol] PDF faktury se nepodařilo stáhnout", no, e);
    return { no, pdf: null };
  }
}
