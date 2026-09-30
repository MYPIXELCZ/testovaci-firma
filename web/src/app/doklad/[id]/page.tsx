import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { COMPANY, PRODUCT } from "@/lib/config";
import { getOrder } from "@/lib/orders";
import PrintButton from "./PrintButton";

export const metadata: Metadata = { title: "Doklad o zaplacení", robots: { index: false } };

export default async function ReceiptPage(props: PageProps<"/doklad/[id]">) {
  const { id } = await props.params;
  const order = await getOrder(id);
  if (!order || order.status !== "paid") notFound();
  const paid = new Date(order.paidAt!).toLocaleDateString("cs-CZ");

  return (
    <section>
      <div className="wrap narrow">
        <h1 style={{ fontSize: "2rem" }}>Doklad o zaplacení č. {order.vs}</h1>
        <table className="pay-table" style={{ marginTop: 24 }}>
          <tbody>
            <tr><td>Prodávající</td><td>{COMPANY.name}<br />{COMPANY.address}<br />IČO {COMPANY.ico}<br /><span className="small">{COMPANY.register}</span></td></tr>
            <tr><td>Kupující</td><td>{order.name}<br />{order.email}</td></tr>
            <tr><td>Položka</td><td>{PRODUCT.name} (digitální obsah), 1 ks</td></tr>
            <tr><td>Cena</td><td>{order.amount} Kč</td></tr>
            <tr><td>Datum přijetí platby</td><td>{paid}</td></tr>
            <tr><td>Způsob úhrady</td><td>bankovní převod</td></tr>
          </tbody>
        </table>
        <p className="muted small" style={{ marginTop: 16 }}>{COMPANY.vat}{order.test ? " Testovací objednávka." : ""}</p>
        <PrintButton />
      </div>
    </section>
  );
}
