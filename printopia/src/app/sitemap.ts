import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/config";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["/", "/ochrana-osobnich-udaju"].map((p) => ({ url: `${SITE_URL}${p === "/" ? "" : p}` }));
}
