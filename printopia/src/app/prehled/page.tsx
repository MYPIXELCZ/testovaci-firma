import type { Metadata } from "next";
import { headers } from "next/headers";
import { notFound } from "next/navigation";
import OwnerOverview from "@/components/OwnerOverview";
import { isInternalHost } from "@/lib/config";

export const metadata: Metadata = { title: "Přehled", robots: { index: false } };
export const dynamic = "force-dynamic";

/** Přehled pro majitele: jen na chráněné adrese *.vercel.app (Vercel Authentication), na printopia.cz je /sprava s Klíčenkou. */
export default async function Overview() {
  if (!isInternalHost((await headers()).get("host"))) notFound();
  return <OwnerOverview />;
}
