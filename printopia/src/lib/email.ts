import "server-only";
import { COMPANY, PAYMENT, PRODUCT, SITE_URL } from "./config";
import type { Order } from "./orders";
import { WITHDRAWAL_FORM_HEAD, WITHDRAWAL_FORM_LINES, WITHDRAWAL_INFO, WITHDRAWAL_URL } from "./withdrawal";

const FROM = process.env.EMAIL_FROM ?? "Printopia <objednavky@printopia.cz>";
const RESEND_URL = process.env.RESEND_API_URL ?? "https://api.resend.com/emails";

const kc = (n: number) => `${n.toLocaleString("cs-CZ")} Kč`;
const orderUrl = (o: Order) => `${SITE_URL}/objednavka/${o.id}`;
const escape = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);

function layout(title: string, body: string) {
  return `<!doctype html><html lang="cs"><body style="margin:0;background:#fbfaf6;font-family:Arial,sans-serif;color:#1c2230">
<div style="max-width:560px;margin:0 auto;padding:32px 24px">
<p style="font-family:Georgia,serif;font-size:22px;font-weight:bold;margin:0 0 24px">Printopia<span style="color:#f5b82e">.</span></p>
<h1 style="font-family:Georgia,serif;font-size:24px;font-weight:normal;margin:0 0 16px">${title}</h1>
${body}
<p style="font-size:12px;color:#5f6675;margin-top:40px;border-top:1px solid #e4e2da;padding-top:16px">
${COMPANY.name}, ${COMPANY.address}, IČO ${COMPANY.ico}<br>Dotazy: <a href="mailto:${COMPANY.email}" style="color:#2952cc">${COMPANY.email}</a></p>
</div></body></html>`;
}

const button = (href: string, label: string) =>
  `<p style="margin:24px 0"><a href="${href}" style="background:#2952cc;color:#fff;text-decoration:none;padding:12px 20px;border-radius:8px;display:inline-block">${label}</a></p>`;

type Attachment = { filename: string; content: string }; // content = base64

/** Poučení o odstoupení a vzorový formulář přímo v textu e-mailu (trvalý nosič, § 1820 a § 1824 občanského zákoníku). */
function withdrawalBlock() {
  const info = WITHDRAWAL_INFO.map((s) => `<h3 style="font-size:15px;margin:18px 0 6px">${escape(s.h)}</h3>${s.p.map((x) => `<p style="font-size:14px;line-height:1.6;margin:6px 0">${escape(x)}</p>`).join("")}`).join("");
  const form = `<div style="border:1px solid #e4e2da;border-radius:8px;padding:12px 16px;margin:12px 0;font-size:14px;line-height:1.7"><strong>Vzorový formulář pro odstoupení od smlouvy</strong><br><em>${escape(WITHDRAWAL_FORM_HEAD)}</em><br>${WITHDRAWAL_FORM_LINES.map(escape).join("<br>")}</div>`;
  return `<h2 style="font-family:Georgia,serif;font-size:18px;font-weight:normal;margin:32px 0 8px">Právo odstoupit od smlouvy</h2>${info}${form}<p style="font-size:14px">Odstoupit můžete i online na <a href="${WITHDRAWAL_URL}" style="color:#2952cc">${WITHDRAWAL_URL}</a>. Obchodní podmínky najdete v příloze tohoto e-mailu.</p>`;
}

/**
 * Obchodní podmínky jako příloha (stejné znění jako na webu, bere se přímo z veřejné stránky), aby je kupující měl na trvalém nosiči.
 * Když stránku nejde načíst, e-mail odejde bez přílohy (poučení a formulář jsou v textu e-mailu) a chyba se zapíše do logu.
 */
async function termsAttachment(): Promise<Attachment[]> {
  try {
    const res = await fetch(`${SITE_URL}/obchodni-podminky`, { cache: "no-store" });
    const page = await res.text();
    const main = page.match(/<main[^>]*>([\s\S]*?)<\/main>/)?.[1];
    if (!res.ok || !main) throw new Error(`stránka s obchodními podmínkami vrátila ${res.status}`);
    const body = main.replace(/href="\//g, `href="${SITE_URL}/`).replace(/<!-- -->/g, "");
    const html = `<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>Obchodní podmínky Printopia</title><style>body{font-family:Arial,sans-serif;max-width:720px;margin:32px auto;padding:0 20px;line-height:1.6;color:#1c2230}h1,h2{font-family:Georgia,serif;font-weight:normal}</style></head><body>${body}</body></html>`;
    return [{ filename: "obchodni-podminky-printopia.html", content: Buffer.from(html, "utf-8").toString("base64") }];
  } catch (e) {
    console.error("[email] obchodní podmínky se nepodařilo přiložit", e);
    return [];
  }
}

async function send(to: string, subject: string, html: string, attachments?: Attachment[]) {
  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.warn(`[email] RESEND_API_KEY chybí, e-mail „${subject}“ pro ${to} se neposlal`);
    return;
  }
  const res = await fetch(RESEND_URL, {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: FROM, to, subject, html, reply_to: COMPANY.email, ...(attachments ? { attachments } : {}) }),
  });
  if (!res.ok) throw new Error(`Resend odpověděl ${res.status}: ${await res.text()}`);
}

export async function sendPaymentInstructions(o: Order) {
  await send(
    o.email,
    `Objednávka ${o.vs}: platební údaje`,
    layout(
      "Děkujeme za objednávku",
      `<p>Sadu vám pošleme hned, jak dorazí platba. Nejrychlejší je naskenovat QR kód na stránce objednávky.</p>
<table style="font-size:15px;margin:16px 0">
<tr><td style="color:#5f6675;padding:4px 16px 4px 0">Číslo účtu</td><td><strong>${PAYMENT.account}</strong></td></tr>
<tr><td style="color:#5f6675;padding:4px 16px 4px 0">Částka</td><td><strong>${kc(o.amount)}</strong></td></tr>
<tr><td style="color:#5f6675;padding:4px 16px 4px 0">Variabilní symbol</td><td><strong>${o.vs}</strong></td></tr>
</table>
${button(orderUrl(o), "Zobrazit QR platbu")}
<p style="font-size:14px;color:#5f6675">Bez variabilního symbolu platbu nedokážeme spárovat automaticky.</p>${withdrawalBlock()}`,
    ),
    await termsAttachment(),
  );
}

export async function sendDelivery(o: Order) {
  await send(
    o.email,
    "Vaše sada na přijímačky je tady",
    layout(
      "Platba dorazila, děkujeme!",
      `<p>Všechny pracovní listy k tisku najdete na stránce objednávky. Začněte úvodním testem, ukáže, která témata procvičit nejdřív.</p>
${button(orderUrl(o), "Stáhnout pracovní listy")}
<p>Odkaz funguje i později, stačí si tento e-mail nechat.</p>
<h2 style="font-family:Georgia,serif;font-size:18px;font-weight:normal;margin:32px 0 8px">Doklad o zaplacení č. ${o.vs}</h2>
<p style="font-size:14px;line-height:1.6">
Prodávající: ${COMPANY.name}, ${COMPANY.address}, IČO ${COMPANY.ico}, ${COMPANY.register}<br>
Kupující: ${escape(o.name)}, ${escape(o.email)}<br>
Položka: ${PRODUCT.name} (digitální obsah), 1 ks<br>
Cena: ${kc(o.amount)}, zaplaceno převodem ${new Date(o.paidAt!).toLocaleDateString("cs-CZ")}<br>
${COMPANY.vat}</p>
<p style="font-size:14px"><a href="${SITE_URL}/doklad/${o.id}" style="color:#2952cc">Doklad k tisku</a></p>
<p style="font-size:14px;color:#5f6675">Do 14 dnů můžete od smlouvy odstoupit bez udání důvodu: <a href="${WITHDRAWAL_URL}" style="color:#2952cc">${WITHDRAWAL_URL}</a>. Úplné poučení a formulář jsou v e-mailu s platebními údaji.</p>`,
    ),
  );
}

/** Upozornění pro firmu (printopia@mypixel.cz). */
export async function notifyOwner(subject: string, lines: string[]) {
  await send(COMPANY.email, `[Printopia] ${subject}`, layout(subject, lines.map((l) => `<p style="margin:4px 0">${escape(l)}</p>`).join("")));
}

export async function sendMonthlyReport(month: string, csv: string, count: number, total: number) {
  await send(
    COMPANY.email,
    `[Printopia] Přehled prodejů ${month}`,
    layout(`Přehled prodejů ${month}`, `<p>Zaplacených objednávek: <strong>${count}</strong>, tržba celkem <strong>${kc(total)}</strong>.</p>
<p>V příloze je CSV pro účetní (číslo dokladu = variabilní symbol). ${COMPANY.vat}</p>`),
    [{ filename: `printopia-prodeje-${month}.csv`, content: Buffer.from("﻿" + csv, "utf8").toString("base64") }],
  );
}

/** Potvrzení přijetí odstoupení od smlouvy v textové podobě (včetně obsahu a data a času odeslání). */
export async function sendWithdrawalReceipt(d: { name: string; email: string; vs: string; sentAt: Date }) {
  const when = d.sentAt.toLocaleString("cs-CZ", { timeZone: "Europe/Prague" });
  await send(
    d.email,
    `Potvrzení přijetí odstoupení od smlouvy (objednávka ${d.vs})`,
    layout(
      "Odstoupení od smlouvy jsme přijali",
      `<p>Potvrzujeme přijetí Vašeho odstoupení od smlouvy o koupi digitálního obsahu ${escape(PRODUCT.name)}.</p>
<p style="font-size:14px;line-height:1.7">Jméno: ${escape(d.name)}<br>E-mail: ${escape(d.email)}<br>Číslo objednávky: ${escape(d.vs)}<br>Odesláno: ${when}</p>
<p>Peníze Vám vrátíme bez zbytečného odkladu, nejpozději do 14 dnů od doručení odstoupení, na účet, ze kterého byla platba provedena. Digitální obsah prosím dál nepoužívejte a jeho kopie smažte.</p>`,
    ),
  );
}
