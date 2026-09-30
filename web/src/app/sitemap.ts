import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/config";
import { ARTICLES } from "@/content/articles";

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ["/", ...ARTICLES.map((a) => a.href), "/obchodni-podminky", "/ochrana-osobnich-udaju"];
  return pages.map((p) => ({ url: new URL(p, SITE_URL).toString(), changeFrequency: "monthly", priority: p === "/" ? 1 : 0.7 }));
}
