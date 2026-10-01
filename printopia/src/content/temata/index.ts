import t0 from "./grafy-a-prumer-prijimacky.json";
import t1 from "./konstrukcni-ulohy-prijimacky.json";
import t2 from "./obsahy-a-pythagorova-veta-prijimacky.json";
import t3 from "./pomer-a-umernost-prijimacky.json";
import t4 from "./procenta-prijimacky.json";
import t5 from "./rovnice-prijimacky.json";
import t6 from "./slovni-ulohy-prijimacky.json";
import t7 from "./telesa-objem-povrch-prijimacky.json";
import t8 from "./uhly-a-trojuhelniky-prijimacky.json";
import t9 from "./vyrazy-prijimacky.json";
import t10 from "./vzory-a-usudek-prijimacky.json";

export type Topic = typeof t0;

// Tematické stránky s příklady (generují content/temata.py a content/sada/stranky.py).
// Zlomky mají vlastní stránku s ukázkou ke stažení.
const ALL: Topic[] = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10];
export const TOPICS: Record<string, Topic> = Object.fromEntries(ALL.map((t) => [t.slug, t]));
