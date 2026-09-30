import procenta from "./procenta-prijimacky.json";
import rovnice from "./rovnice-prijimacky.json";
import slovni from "./slovni-ulohy-prijimacky.json";

export type Topic = typeof procenta;

// Tematické stránky s příklady (generuje content/temata.py). Zlomky mají vlastní stránku s ukázkou ke stažení.
export const TOPICS: Record<string, Topic> = { [procenta.slug]: procenta, [rovnice.slug]: rovnice, [slovni.slug]: slovni };
