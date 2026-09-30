import "server-only";
import QRCode from "qrcode";
import { PAYMENT } from "./config";
import type { Order } from "./orders";

/** QR Platba (SPAYD 1.0), kterou umí všechny české bankovní aplikace. */
export function spayd(order: Pick<Order, "vs" | "amount">) {
  return [
    "SPD*1.0",
    `ACC:${PAYMENT.iban.replaceAll(" ", "")}`,
    `AM:${order.amount.toFixed(2)}`,
    "CC:CZK",
    `X-VS:${order.vs}`,
    `RN:${PAYMENT.recipient}`,
    `MSG:ANO BERU ${order.vs}`,
  ].join("*");
}

export async function qrSvg(order: Pick<Order, "vs" | "amount">) {
  return QRCode.toString(spayd(order), { type: "svg", margin: 0, errorCorrectionLevel: "M", color: { dark: "#2B2A28", light: "#FFFFFF" } });
}

export function paymentConfigured() {
  return PAYMENT.iban !== "" && PAYMENT.account !== "";
}
