import "server-only";
import { notifyOwner, sendDelivery } from "./email";
import { markInvoiced, type Order } from "./orders";
import { issueInvoice, uolEnabled } from "./uol";

/**
 * Doručení zaplacené objednávky: nejdřív faktura v UOL (když je zapnuté a nejde o test), potom e-mail se sadou a fakturou v příloze.
 * Výpadek UOL doručení NIKDY nezastaví: e-mail odejde se starým dokladem a firmě přijde upozornění, aby fakturu vystavila ručně.
 * Vrací objednávku s případným číslem faktury.
 */
export async function deliverPaid(paid: Order): Promise<Order> {
  let order = paid;
  let invoice: { no: string; pdf: string } | undefined;
  if (uolEnabled() && !paid.test) {
    try {
      const issued = await issueInvoice(paid);
      order = await markInvoiced(paid, issued.no).catch((e) => {
        console.error("[uol] číslo faktury se nepodařilo uložit k objednávce", paid.vs, issued.no, e);
        return { ...paid, invoiceNo: issued.no };
      });
      if (issued.pdf) invoice = { no: issued.no, pdf: issued.pdf };
      else {
        await notifyOwner(`Faktura ${issued.no} vystavena, PDF se nestáhlo (${paid.vs})`, [
          `Objednávka ${paid.vs}: ${paid.name}, ${paid.email}. Faktura ${issued.no} v UOL už existuje, nevystavujte ji znovu.`,
          "Zákazník dostal e-mail se sadou a starým dokladem. Fakturu mu prosím pošlete z UOL ručně.",
        ]).catch(() => undefined);
      }
    } catch (e) {
      console.error("[uol] faktura se nevystavila", paid.vs, e);
      await notifyOwner(`Fakturu v UOL se nepodařilo vystavit (${paid.vs})`, [
        `Objednávka ${paid.vs}: ${paid.name}, ${paid.email}, ${paid.amount} Kč.`,
        "Zákazník dostal e-mail se sadou a starým dokladem. Fakturu prosím vystavte v UOL ručně.",
      ]).catch(() => undefined);
    }
  }
  await sendDelivery(order, invoice);
  return order;
}
