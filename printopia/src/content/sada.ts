// Seznam souborů sady ke stažení po zaplacení. Generuje scripts/render-sada.mjs (PDF leží v private/sada/).
import files from "./sada-soubory.json";

export type SadaFile = { slug: string; file: string; title: string; desc: string };
export const FILES: SadaFile[] = files;
