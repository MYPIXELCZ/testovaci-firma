import "server-only";
import { randomBytes, randomInt } from "node:crypto";
import { PRODUCT } from "./config";
import { storage } from "./storage";

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
  test?: boolean;
};

// Úložiště (produkce: privátní Vercel Blob):
//   orders/{id}.json      celý záznam
//   pending/{vs}_{id}     značka nezaplacené objednávky (pro párování plateb)
//   vs/{vs}               použitý VS; nemaže se, aby stará platba nemohla odemknout novou objednávku
const orderPath = (id: string) => `orders/${id}.json`;
const pendingPath = (o: Pick<Order, "vs" | "id">) => `pending/${o.vs}_${o.id}`;

const save = (order: Order) => storage.write(orderPath(order.id), JSON.stringify(order), { overwrite: true });

export async function getOrder(id: string): Promise<Order | null> {
  if (!/^[A-Za-z0-9_-]{22}$/.test(id)) return null;
  const json = await storage.read(orderPath(id));
  return json ? (JSON.parse(json) as Order) : null;
}

/** VS ve tvaru RRMMDDxxxx, nikdy nepoužitý. */
async function newVs(): Promise<string> {
  const prefix = new Date().toISOString().slice(2, 10).replaceAll("-", "");
  for (let i = 0; i < 5; i++) {
    const vs = prefix + String(randomInt(0, 10000)).padStart(4, "0");
    if (await storage.exists(`vs/${vs}`)) continue;
    await storage.write(`vs/${vs}`, "1", { overwrite: false });
    return vs;
  }
  throw new Error("Nepodařilo se vygenerovat variabilní symbol");
}

export async function createOrder(input: {
  email: string;
  name: string;
  marketing: boolean;
  test?: boolean;
  amount?: number;
}): Promise<Order> {
  const now = new Date().toISOString();
  const order: Order = {
    id: randomBytes(16).toString("base64url"),
    vs: await newVs(),
    email: input.email,
    name: input.name,
    amount: input.amount ?? PRODUCT.price,
    status: "pending",
    createdAt: now,
    consents: { terms: now, marketing: input.marketing },
    ...(input.test ? { test: true } : {}),
  };
  await save(order);
  await storage.write(pendingPath(order), order.id, { overwrite: true });
  return order;
}

export async function markPaid(order: Order, paymentId: string): Promise<Order> {
  const paid: Order = { ...order, status: "paid", paidAt: new Date().toISOString(), paymentId };
  await save(paid);
  await storage.remove([pendingPath(order)]);
  return paid;
}

export async function deleteOrder(order: Pick<Order, "vs" | "id">) {
  await storage.remove([orderPath(order.id), pendingPath(order)]);
}

/** Nezaplacené objednávky jako {vs, id, uploadedAt} bez načítání celých záznamů. */
export async function listPending() {
  const items = await storage.list("pending/");
  return items.flatMap((b) => {
    const [vs, id] = b.pathname.slice("pending/".length).split("_");
    return vs && id ? [{ vs, id, uploadedAt: b.uploadedAt }] : [];
  });
}
