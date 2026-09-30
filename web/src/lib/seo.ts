import type { Metadata } from "next";

/** Metadata článku včetně Open Graph náhledu z public/og/{slug}.png (generuje marketing/og/render.mjs). */
export function articleMetadata(slug: string, title: string, description: string): Metadata {
  return {
    title,
    description,
    alternates: { canonical: `/${slug}` },
    openGraph: { type: "article", locale: "cs_CZ", siteName: "Ano, beru", title, description, url: `/${slug}`, images: [`/og/${slug}.png`] },
  };
}
