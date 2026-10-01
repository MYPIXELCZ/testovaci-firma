import { INDEXING, PRODUCT, SALES_OPEN, TEST_PRICE, UNPAID_RETENTION_DAYS } from "@/lib/config";
import { notifyOwner, sendDelivery } from "@/lib/email";
import { incomingPayments, type IncomingPayment } from "@/lib/fio";
import { pingSearchEngines } from "@/lib/indexnow";
import { deleteOrder, getOrder, listPending, markPaid, markPaymentAlerted, paymentSeen } from "@/lib/orders";
import { cleanupRateLimits } from "@/lib/ratelimit";
import { storage } from "@/lib/storage";
import { getSecret } from "@/lib/secrets";

export const maxDuration = 60;

const FIO_FAILS = "alerts/fio-fails"; // počet chyb Fio API po sobě, po úspěchu se maže
const FIO_ALERT_AFTER = 3;

/** Náš VS má tvar RRMMDDxxxx s platným datem v posledních 60 dnech. Firemní účet přijímá i jiné platby. */
function looksLikeOurVs(vs: string) {
  const m = /^(\d{2})(\d{2})(\d{2})\d{4}$/.exec(vs);
  if (!m) return false;
  const [month, day] = [Number(m[2]), Number(m[3])];
  if (month < 1 || month > 12 || day < 1 || day > 31) return false;
  const age = Date.now() - Date.UTC(2000 + Number(m[1]), month - 1, day);
  return age >= -86_400_000 && age < 60 * 86_400_000;
}

const describe = (p: IncomingPayment) => `${p.amount} ${p.currency}, VS ${p.vs || "bez VS"}, ${p.date.slice(0, 10)}, pohyb Fio ${p.id}`;

/** Vercel Cron (vercel.json): spáruje příchozí platby z Fio s nezaplacenými objednávkami. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }

  if (!SALES_OPEN) {
    // Před spuštěním hlásí připravenost do logu (bez obsahu tajemství). Testovací objednávky se párují i tak.
    const [fio, resend] = await Promise.all([getSecret("FIO_TOKEN"), getSecret("RESEND_API_KEY")]);
    console.log(`[cron] prodej vypnutý; fio=${Boolean(fio)} resend=${Boolean(resend)}`);
    // Jednorázový zkušební e-mail firmě: ověří Resend a doménu bez testovacího nákupu.
    if (resend && !(await storage.exists("alerts/email-test-ok"))) {
      try {
        await notifyOwner("E-maily fungují", [
          "Tohle je zkušební zpráva z anoberu.cz. Pokud ji čtete, odesílání přes Resend z domény anoberu.cz funguje.",
        ]);
        await storage.write("alerts/email-test-ok", new Date().toISOString(), { overwrite: true });
        console.log("[cron] zkušební e-mail odeslán");
      } catch (e) {
        console.error("[cron] zkušební e-mail selhal:", e instanceof Error ? e.message : e);
      }
    }
  }

  const pending = await listPending();
  const result = { pending: pending.length, paid: [] as string[], underpaid: [] as string[], orphans: 0, expired: 0 };

  if (pending.length > 0 || SALES_OPEN) {
    let payments: IncomingPayment[];
    try {
      payments = await incomingPayments();
    } catch (e) {
      // Jednotlivé selhání sítě je běžné (bankovní API nebo Vercel na pár sekund vypadne), proto se firmě píše až po třech chybách
      // v řadě (~15 min), nejvýš jednou denně. Limit 30 s (409) se nepočítá, to není porucha.
      const msg = e instanceof Error ? e.message : String(e);
      console.error("[cron] Fio API selhalo:", msg);
      if (!msg.includes("409") && !msg.includes("30 s")) {
        const fails = Number((await storage.read(FIO_FAILS).catch(() => null)) ?? 0) + 1;
        await storage.write(FIO_FAILS, String(fails), { overwrite: true }).catch(() => undefined);
        const marker = `alerts/fio-${new Date().toISOString().slice(0, 10)}`;
        if (fails >= FIO_ALERT_AFTER && !(await storage.exists(marker))) {
          const network = /fetch failed|timeout|ECONN|ENOTFOUND/i.test(msg);
          await notifyOwner("Párování plateb nefunguje", [
            `Fio API vrací chybu: ${msg} (${fails}× po sobě)`,
            network
              ? "Vypadá to na výpadek spojení s bankou. Obvykle se spraví samo, další pokus běží každých 5 minut."
              : "Nejspíš vypršel token. Vytvořte nový (Fio internetbanking → Nastavení → API, jen pro čtení) a vložte ho na https://anoberu-mypixelcz.vercel.app/nastaveni.",
            "Do té doby se zaplacené objednávky neodešlou automaticky.",
          ]).catch(() => undefined);
          await storage.write(marker, msg, { overwrite: true });
        }
      }
      return Response.json({ ...result, error: "fio" }, { status: 502 });
    }
    if (await storage.exists(FIO_FAILS)) await storage.remove([FIO_FAILS]).catch(() => undefined);
    const matched = new Set<string>();

    for (const p of pending) {
      // Platba musí přijít v den objednávky nebo později (Fio datum: "2026-09-30+0200").
      const created = p.uploadedAt.toISOString().slice(0, 10);
      const payment = payments.find((x) => x.vs === p.vs && x.currency === "CZK" && x.date.slice(0, 10) >= created);
      if (!payment) continue;
      matched.add(payment.id);
      const order = await getOrder(p.id);
      if (!order || order.status !== "pending") continue;
      if (payment.amount < order.amount) {
        result.underpaid.push(order.vs);
        if (!(await paymentSeen(payment.id))) {
          await notifyOwner(`Nedoplatek u objednávky ${order.vs}`, [
            `Zákazník ${order.name} (${order.email}) poslal ${payment.amount} Kč místo ${order.amount} Kč.`,
            `Platba: ${describe(payment)}`,
            "Objednávka zůstává nezaplacená. Domluvte doplatek, nebo peníze vraťte.",
          ]).catch((e) => console.error("[cron] upozornění selhalo", e));
          await markPaymentAlerted(payment.id, `underpaid ${order.vs}`);
        }
        continue;
      }
      const paid = await markPaid(order, payment.id);
      result.paid.push(paid.vs);
      await sendDelivery(paid).catch((e) => console.error("[cron] doručovací e-mail selhal", paid.vs, e));
      await notifyOwner(`Zaplaceno ${paid.amount} Kč${paid.test ? " (test)" : ""}`, [
        `Objednávka ${paid.vs}: ${paid.name}, ${paid.email}`,
        `Platba: ${describe(payment)}`,
      ]).catch((e) => console.error("[cron] upozornění selhalo", e));
    }

    // Platby, které vypadají jako naše, ale k žádné objednávce nesedí (překlep ve VS, platba bez VS, dvojí platba).
    for (const pay of payments) {
      if (matched.has(pay.id) || pay.currency !== "CZK") continue;
      const suspicious = looksLikeOurVs(pay.vs) || (!pay.vs && (pay.amount === PRODUCT.price || pay.amount === TEST_PRICE));
      if (!suspicious || (await paymentSeen(pay.id))) continue;
      result.orphans++;
      await notifyOwner("Platba bez objednávky", [
        `Přišla platba, kterou jsem nedokázal spárovat: ${describe(pay)}.`,
        "Nejspíš překlep ve variabilním symbolu, platba bez VS, nebo druhá platba za stejnou objednávku. Zkontrolujte výpis a zákazníkovi případně pošlete odkaz ručně.",
      ]).catch((e) => console.error("[cron] upozornění selhalo", e));
      await markPaymentAlerted(pay.id, "orphan");
    }
  }

  const cutoff = Date.now() - UNPAID_RETENTION_DAYS * 86_400_000;
  for (const p of pending) {
    if (p.uploadedAt.getTime() < cutoff && !result.paid.includes(p.vs)) {
      await deleteOrder(p);
      result.expired++;
    }
  }

  // Jednou za hodinu uklidit stará počítadla ochrany proti spamu.
  if (new Date().getUTCMinutes() < 5) await cleanupRateLimits().catch((e) => console.error("[cron] úklid limitů selhal", e));

  if (INDEXING) {
    const msg = await pingSearchEngines().catch((e) => `indexnow chyba: ${e instanceof Error ? e.message : e}`);
    if (msg !== "indexnow: beze změny") console.log("[cron]", msg);
  }

  if (result.paid.length || result.underpaid.length || result.orphans || result.expired) console.log("[cron]", JSON.stringify(result));
  return Response.json(result);
}
