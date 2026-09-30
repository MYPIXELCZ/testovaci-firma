import type { MetadataRoute } from "next";
import { publicUrls } from "@/lib/indexnow";

export default function sitemap(): MetadataRoute.Sitemap {
  return publicUrls().map((url, i) => ({ url, changeFrequency: "monthly", priority: i === 0 ? 1 : 0.7 }));
}
