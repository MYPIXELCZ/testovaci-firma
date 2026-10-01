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
  consents: { terms: string };
  src?: string; // odkud zákazník přišel (sklik, seo…), pro vyhodnocení kanálů
  test?: boolean;
};

// Úložiště (produkce: privátní Vercel Blob):
//   orders/{id}.json      celý záznam
//   pending/{vs}_{id}     značka nezaplacené objednávky (pro párování plateb)
//   vs/{vs}               použitý VS; nemaže se, aby stará platba nemohla odemknout novou objednávku
//   payments/{fioId}      platba už zpracovaná (paid) nebo nahlášená firmě (alert), aby se nehlásila znovu
const orderPath = (id: string) => `orders/${id}.json`;
const pendingPath = (o: Pick<Order, "vs" | "id">) => `pending/${o.vs}_${o.id}`;

const save = (order: Order) => storage.write(orderPath(order.id), JSON.stringify(order), { overwrite: true });

export async function getOrder(id: string): Promise<Order | null> {
  if (!/^[A-Za-z0-9_-]{22}$/.test(id)) return null;
  const json = await storage.read(orderPath(id));
  return json ? (JSON.parse(json) as Order) : null;
}

/** VS ve tvaru 8RRMMDDxxx, nikdy nepoužitý. Úvodní 8 ho odliší od VS anoberu (RRMMDDxxxx) na stejném účtu. */
async function newVs(): Promise<string> {
  const prefix = "8" + new Date().toISOString().slice(2, 10).replaceAll("-", "");
  for (let i = 0; i < 5; i++) {
    const vs = prefix + String(randomInt(0, 1000)).padStart(3, "0");
    if (await storage.exists(`vs/${vs}`)) continue;
    await storage.write(`vs/${vs}`, "1", { overwrite: false });
    return vs;
  }
  throw new Error("Nepodařilo se vygenerovat variabilní symbol");
}

export async function createOrder(input: {
  email: string;
  name: string;
  src?: string;
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
    consents: { terms: now },
    ...(input.src ? { src: input.src } : {}),
    ...(input.test ? { test: true } : {}),
  };
  await save(order);
  await storage.write(pendingPath(order), order.id, { overwrite: true });
  return order;
}

export async function markPaid(order: Order, paymentId: string): Promise<Order> {
  const paid: Order = { ...order, status: "paid", paidAt: new Date().toISOString(), paymentId };
  await save(paid);
  await storage.write(`payments/${paymentId}`, `paid ${order.vs}`, { overwrite: true });
  await storage.remove([pendingPath(order)]);
  return paid;
}

export const paymentSeen = (paymentId: string) => storage.exists(`payments/${paymentId}`);
export const markPaymentAlerted = (paymentId: string, note: string) =>
  storage.write(`payments/${paymentId}`, `alert ${note}`, { overwrite: true });

/** Všechny objednávky (pro měsíční přehled). Při malém objemu stačí projít úložiště. */
export async function listOrders(): Promise<Order[]> {
  const items = await storage.list("orders/");
  const orders = await Promise.all(items.map(async (i) => JSON.parse((await storage.read(i.pathname)) ?? "null") as Order | null));
  return orders.filter((o): o is Order => o !== null);
}

export async function deleteOrder(order: Pick<Order, "vs" | "id">) {
  await storage.remove([orderPath(order.id), pendingPath(order)]);
}

/** Nezaplacené objednávky jako {vs, id, uploadedAt} bez načítání celých záznamů. */
export async function listPending() {
  const items = await storage.list("pending/");
  return items.flatMap((b) => {
    // VS obsahuje jen číslice, ID (base64url) může obsahovat „_“, proto dělit jen podle prvního podtržítka.
    const rest = b.pathname.slice("pending/".length);
    const sep = rest.indexOf("_");
    const [vs, id] = [rest.slice(0, sep), rest.slice(sep + 1)];
    return sep > 0 && id ? [{ vs, id, uploadedAt: b.uploadedAt }] : [];
  });
}
