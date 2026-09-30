import "server-only";
import { mkdir, readdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { BlobNotFoundError, del, get, head, list, put } from "@vercel/blob";

export type StoredItem = { pathname: string; uploadedAt: Date };

export interface Storage {
  read(pathname: string): Promise<string | null>;
  /** overwrite: false => při existujícím souboru vyhodí chybu */
  write(pathname: string, body: string, opts: { overwrite: boolean }): Promise<void>;
  exists(pathname: string): Promise<boolean>;
  list(prefix: string): Promise<StoredItem[]>;
  remove(pathnames: string[]): Promise<void>;
}

// Produkce: privátní Vercel Blob.
const blobStorage: Storage = {
  async read(pathname) {
    const res = await get(pathname, { access: "private", useCache: false });
    if (!res || res.statusCode !== 200) return null;
    return new Response(res.stream).text();
  },
  async write(pathname, body, { overwrite }) {
    await put(pathname, body, {
      access: "private",
      addRandomSuffix: false,
      allowOverwrite: overwrite,
      contentType: pathname.endsWith(".json") ? "application/json" : "text/plain",
    });
  },
  async exists(pathname) {
    try {
      await head(pathname);
      return true;
    } catch (e) {
      if (e instanceof BlobNotFoundError) return false;
      throw e;
    }
  },
  async list(prefix) {
    const out: StoredItem[] = [];
    let cursor: string | undefined;
    do {
      const page = await list({ prefix, cursor });
      out.push(...page.blobs.map((b) => ({ pathname: b.pathname, uploadedAt: b.uploadedAt })));
      cursor = page.hasMore ? page.cursor : undefined;
    } while (cursor);
    return out;
  },
  async remove(pathnames) {
    await del(pathnames);
  },
};

// Lokální vývoj a testy: soubory na disku.
const root = path.resolve(process.env.LOCAL_STORE_DIR ?? ".localstore");
const file = (pathname: string) => path.join(root, pathname);

const fileStorage: Storage = {
  async read(pathname) {
    return readFile(file(pathname), "utf8").catch(() => null);
  },
  async write(pathname, body, { overwrite }) {
    await mkdir(path.dirname(file(pathname)), { recursive: true });
    await writeFile(file(pathname), body, { flag: overwrite ? "w" : "wx" });
  },
  async exists(pathname) {
    return stat(file(pathname)).then(() => true, () => false);
  },
  async list(prefix) {
    const dir = path.dirname(file(prefix + "x"));
    const names = await readdir(dir).catch(() => [] as string[]);
    const base = path.relative(root, dir);
    const items = names
      .map((n) => (base ? `${base}/${n}` : n))
      .filter((p) => p.startsWith(prefix));
    return Promise.all(items.map(async (p) => ({ pathname: p, uploadedAt: (await stat(file(p))).mtime })));
  },
  async remove(pathnames) {
    await Promise.all(pathnames.map((p) => rm(file(p), { force: true })));
  },
};

function pick(): Storage {
  if (process.env.BLOB_READ_WRITE_TOKEN || process.env.BLOB_STORE_ID) return blobStorage;
  if (process.env.VERCEL) throw new Error("Na Vercelu chybí Blob úložiště (BLOB_READ_WRITE_TOKEN)");
  return fileStorage;
}

export const storage = pick();
