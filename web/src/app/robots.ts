import type { MetadataRoute } from "next";
import { INDEXING, SITE_URL } from "@/lib/config";

export default function robots(): MetadataRoute.Robots {
  if (!INDEXING) return { rules: { userAgent: "*", disallow: "/" } };
  return {
    rules: { userAgent: "*", allow: "/", disallow: ["/api/", "/nastaveni", "/objednavka/", "/stahnout/", "/doklad/", "/objednat"] },
    sitemap: new URL("/sitemap.xml", SITE_URL).toString(),
  };
}
