import "server-only";
import { randomBytes, randomInt } from "node:crypto";
import { del, get, list, put } from "@vercel/blob";
import { PRODUCT } from "./config";

export type OrderStatus = "pending" | "paid";

export type Order = {
  id: string;
  vs: string;
  email: string;
  name: string;
  amount: number;
  status: OrderStatus;
  createdAt: string;
  paidAt?: string;
  paymentId?: string;
  consents: { terms: string; marketing: boolean };
};

// Objednávky jsou v privátním Vercel Blob úložišti:
//   orders/{id}.json      celý záznam
//   pending/{vs}_{id}     značka nezaplacené objednávky (pro párování plateb)
//   vs/{vs}               použitý VS; nemaže se, aby stará platba nemohla odemknout novou objednávku
const orderPath = (id: string) => `orders/${id}.json`;
const pendingPath = (o: Pick<Order, "vs" | "id">) => `pending/${o.vs}_${o.id}`;

async function save(order: Order) {
  await put(orderPath(order.id), JSON.stringify(order), {
    access: "private",
    addRandomSuffix: false,
    allowOverwrite: true,
    contentType: "application/json",
  });
}

export async function getOrder(id: string): Promise<Order | null> {
  if (!/^[A-Za-z0-9_-]{22}$/.test(id)) return null;
  const res = await get(orderPath(id), { access: "private", useCache: false });
  if (!res || res.statusCode !== 200) return null;
  return JSON.parse(await new Response(res.stream).text()) as Order;
}

/** VS ve tvaru RRMMDDxxxx, nikdy nepoužitý. */
async function newVs(): Promise<string> {
  const prefix = new Date().toISOString().slice(2, 10).replaceAll("-", "");
  for (let i = 0; i < 5; i++) {
    const vs = prefix + String(randomInt(0, 10000)).padStart(4, "0");
    try {
      // allowOverwrite: false => při kolizi put selže
      await put(`vs/${vs}`, "", { access: "private", addRandomSuffix: false, allowOverwrite: false });
      return vs;
    } catch {
      continue;
    }
  }
  throw new Error("Nepodařilo se vygenerovat variabilní symbol");
}

export async function createOrder(input: { email: string; name: string; marketing: boolean }): Promise<Order> {
  const now = new Date().toISOString();
  const order: Order = {
    id: randomBytes(16).toString("base64url"),
    vs: await newVs(),
    email: input.email,
    name: input.name,
    amount: PRODUCT.price,
    status: "pending",
    createdAt: now,
    consents: { terms: now, marketing: input.marketing },
  };
  await save(order);
  await put(pendingPath(order), order.id, { access: "private", addRandomSuffix: false, allowOverwrite: true });
  return order;
}

export async function markPaid(order: Order, paymentId: string): Promise<Order> {
  const paid: Order = { ...order, status: "paid", paidAt: new Date().toISOString(), paymentId };
  await save(paid);
  await del(pendingPath(order));
  return paid;
}

export async function deleteOrder(order: Pick<Order, "vs" | "id">) {
  await del([orderPath(order.id), pendingPath(order)]);
}

/** Nezaplacené objednávky jako {vs, id, uploadedAt} bez načítání celých záznamů. */
export async function listPending() {
  const out: { vs: string; id: string; uploadedAt: Date }[] = [];
  let cursor: string | undefined;
  do {
    const page = await list({ prefix: "pending/", cursor });
    for (const b of page.blobs) {
      const [vs, id] = b.pathname.slice("pending/".length).split("_");
      if (vs && id) out.push({ vs, id, uploadedAt: b.uploadedAt });
    }
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);
  return out;
}
