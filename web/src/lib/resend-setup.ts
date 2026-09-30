import "server-only";
import { getSecret } from "./secrets";

// Jednorázové nastavení odesílací domény v Resendu. Záznamy vypíše do logu, do DNS je zapíše Claude
// přes Vercel konektor (web sám k Vercel API přístup nemá).
const API = "https://api.resend.com";
const DOMAIN = "anoberu.cz";

type Domain = { id: string; name: string; status: string; records?: unknown[] };

async function call(key: string, path: string, init?: RequestInit) {
  const res = await fetch(API + path, {
    ...init,
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    cache: "no-store",
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`Resend ${path} ${res.status}: ${JSON.stringify(body)}`);
  return body;
}

export async function ensureSendingDomain() {
  const key = await getSecret("RESEND_API_KEY");
  if (!key) return "resend: klíč chybí";
  const list = (await call(key, "/domains")) as { data: Domain[] };
  let domain = list.data.find((d) => d.name === DOMAIN);
  if (!domain) domain = (await call(key, "/domains", { method: "POST", body: JSON.stringify({ name: DOMAIN, region: "eu-west-1" }) })) as Domain;
  if (domain.status === "verified") return `resend: ${DOMAIN} ověřena`;
  const detail = (await call(key, `/domains/${domain.id}`)) as Domain;
  await call(key, `/domains/${domain.id}/verify`, { method: "POST" }).catch(() => undefined);
  return `resend: ${DOMAIN} status=${detail.status} records=${JSON.stringify(detail.records)}`;
}
