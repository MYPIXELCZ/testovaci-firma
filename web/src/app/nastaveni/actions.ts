"use server";

import { incomingPayments } from "@/lib/fio";
import { isAdminRequest, setSecret } from "@/lib/secrets";

export type SaveState = { ok: boolean; message: string } | null;

export async function saveFioToken(_prev: SaveState, form: FormData): Promise<SaveState> {
  if (!(await isAdminRequest())) return { ok: false, message: "Tady to nejde." };
  const token = String(form.get("token") ?? "").trim();
  if (!/^[A-Za-z0-9]{20,100}$/.test(token)) return { ok: false, message: "Tohle nevypadá jako token z Fio. Zkopírujte ho celý." };
  try {
    const payments = await incomingPayments(30, token);
    await setSecret("FIO_TOKEN", token);
    return { ok: true, message: `Token funguje a je uložený. Za posledních 30 dní vidím ${payments.length} příchozích plateb.` };
  } catch (e) {
    return { ok: false, message: `Banka token nepřijala: ${e instanceof Error ? e.message : e}. Nic jsem neuložil.` };
  }
}

export async function saveResendKey(_prev: SaveState, form: FormData): Promise<SaveState> {
  if (!(await isAdminRequest())) return { ok: false, message: "Tady to nejde." };
  const key = String(form.get("token") ?? "").trim();
  if (!/^re_[A-Za-z0-9_]{10,}$/.test(key)) return { ok: false, message: "Klíč z Resendu začíná „re_“. Zkopírujte ho celý." };
  await setSecret("RESEND_API_KEY", key);
  return { ok: true, message: "Klíč je uložený." };
}
