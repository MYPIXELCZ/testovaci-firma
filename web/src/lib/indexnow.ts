import "server-only";
import { createHash } from "node:crypto";
import { SITE_URL } from "./config";
import { ARTICLES } from "@/content/articles";
import { storage } from "./storage";

// IndexNow (Seznam, Bing a další): veřejný klíč leží v public/{KEY}.txt.
const KEY = "31de1fcd1629afe01591a762c249bc90";

export function publicUrls() {
  return ["/", ...ARTICLES.map((a) => a.href), "/obchodni-podminky", "/ochrana-osobnich-udaju"].map((p) => new URL(p, SITE_URL).toString());
}

/** Oznámí seznam stránek vyhledávačům, jen pokud se od minula změnil. */
export async function pingSearchEngines() {
  const urls = publicUrls();
  const digest = createHash("sha256").update(urls.join("\n")).digest("hex").slice(0, 16);
  const marker = `indexnow/${digest}`;
  if (await storage.exists(marker)) return "indexnow: beze změny";
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: new URL(SITE_URL).host, key: KEY, keyLocation: new URL(`/${KEY}.txt`, SITE_URL).toString(), urlList: urls }),
  });
  if (!res.ok && res.status !== 202) throw new Error(`IndexNow ${res.status}: ${await res.text()}`);
  await storage.write(marker, new Date().toISOString(), { overwrite: true });
  return `indexnow: oznámeno ${urls.length} URL (${res.status})`;
}
