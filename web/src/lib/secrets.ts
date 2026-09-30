import "server-only";
import { headers } from "next/headers";
import { storage } from "./storage";

export type SecretName = "FIO_TOKEN" | "RESEND_API_KEY";

// Tajemství z env mají přednost. Jinak se berou z privátního úložiště, kam je vloží Ondřej přes /nastaveni,
// aby nemusel chodit do nastavení Vercelu.
const path = (name: SecretName) => `secrets/${name}`;

export async function getSecret(name: SecretName): Promise<string | undefined> {
  return process.env[name] || (await storage.read(path(name)))?.trim() || undefined;
}

export async function setSecret(name: SecretName, value: string) {
  await storage.write(path(name), value.trim(), { overwrite: true });
}

/** Správa jen na *.vercel.app (chráněno Vercel Authentication) nebo lokálně mimo Vercel. */
export async function isAdminRequest() {
  const host = (await headers()).get("host") ?? "";
  return host.endsWith(".vercel.app") || !process.env.VERCEL;
}
