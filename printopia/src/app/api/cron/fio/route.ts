import { TEST_PRICE, UNPAID_RETENTION_DAYS } from "@/lib/config";
import { notifyOwner, sendDelivery } from "@/lib/email";
import { incomingPayments, type IncomingPayment } from "@/lib/fio";
import { deleteOrder, getOrder, listPending, markPaid, markPaymentAlerted, paymentSeen } from "@/lib/orders";
import { cleanupRateLimits } from "@/lib/ratelimit";
import { storage } from "@/lib/storage";

export const maxDuration = 60;

const FIO_FAILS = "alerts/fio-fails"; // počet chyb Fio API po sobě, po úspěchu se maže
const FIO_ALERT_AFTER = 3;

/** Náš VS má tvar 8RRMMDDxxx s platným datem v posledních 60 dnech. Na účtu chodí i platby anoberu (RRMMDDxxxx). */
function looksLikeOurVs(vs: string) {
  const m = /^8(\d{2})(\d{2})(\d{2})\d{3}$/.exec(vs);
  if (!m) return false;
  const [month, day] = [Number(m[2]), Number(m[3])];
  if (month < 1 || month > 12 || day < 1 || day > 31) return false;
  const age = Date.now() - Date.UTC(2000 + Number(m[1]), month - 1, day);
  return age >= -86_400_000 && age < 60 * 86_400_000;
}

const describe = (p: IncomingPayment) => `${p.amount} ${p.currency}, VS ${p.vs || "bez VS"}, ${p.date.slice(0, 10)}, pohyb Fio ${p.id}`;

/** Vercel Cron (vercel.json, posunutý o 2 min proti anoberu): spáruje platby z Fio s nezaplacenými objednávkami. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }

  const pending = await listPending();
  const result = { pending: pending.length, paid: [] as string[], underpaid: [] as string[], orphans: 0, expired: 0 };

  if (pending.length > 0) {
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
              : "Nejspíš vypršel token. Ve Fio internetbankingu (Nastavení → API) vytvořte nový token jen pro čtení a vložte ho do env FIO_TOKEN projektu printopia ve Vercelu.",
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

    // Platby s naším VS, které k žádné objednávce nesedí (překlep, dvojí platba). Platby bez VS hlásí anoberu.
    for (const pay of payments) {
      if (matched.has(pay.id) || pay.currency !== "CZK" || !looksLikeOurVs(pay.vs) || (await paymentSeen(pay.id))) continue;
      result.orphans++;
      await notifyOwner("Platba bez objednávky", [
        `Přišla platba, kterou jsem nedokázal spárovat: ${describe(pay)}.`,
        `Nejspíš překlep ve variabilním symbolu nebo druhá platba za stejnou objednávku${pay.amount === TEST_PRICE ? " (testovací částka)" : ""}. Zkontrolujte výpis a zákazníkovi případně pošlete odkaz ručně.`,
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

  if (result.paid.length || result.underpaid.length || result.orphans || result.expired) console.log("[cron]", JSON.stringify(result));
  return Response.json(result);
}
