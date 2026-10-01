import "server-only";
import { COMPANY, PAYMENT, PRODUCT, SITE_URL } from "./config";
import type { Order } from "./orders";

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
<p style="font-size:14px;color:#5f6675">Bez variabilního symbolu platbu nedokážeme spárovat automaticky.</p>`,
    ),
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
<p style="font-size:14px"><a href="${SITE_URL}/doklad/${o.id}" style="color:#2952cc">Doklad k tisku</a></p>`,
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
