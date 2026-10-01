import type { MetadataRoute } from "next";
import { TOPICS } from "@/content/temata";
import { SITE_URL } from "@/lib/config";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["/", "/jak-se-pripravit-na-prijimacky", "/zlomky-prijimacky", ...Object.keys(TOPICS).map((s) => `/${s}`), "/obchodni-podminky", "/ochrana-osobnich-udaju"].map((p) => ({ url: `${SITE_URL}${p === "/" ? "" : p}` }));
}
