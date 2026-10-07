import t0 from "./cermat-testy-matematika-jak-procvicovat.json";
import t1 from "./grafy-a-prumer-prijimacky.json";
import t2 from "./konstrukcni-ulohy-prijimacky.json";
import t3 from "./obsahy-a-pythagorova-veta-prijimacky.json";
import t4 from "./pomer-a-umernost-prijimacky.json";
import t5 from "./procenta-prijimacky.json";
import t6 from "./rovnice-prijimacky.json";
import t7 from "./slovni-ulohy-prijimacky.json";
import t8 from "./telesa-objem-povrch-prijimacky.json";
import t9 from "./uhly-a-trojuhelniky-prijimacky.json";
import t10 from "./vyrazy-prijimacky.json";
import t11 from "./vzory-a-usudek-prijimacky.json";

export type Topic = typeof t0;

// Tematické stránky s příklady (generují content/temata.py a content/sada/stranky.py).
// Zlomky mají vlastní stránku s ukázkou ke stažení.
const ALL: Topic[] = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11];
export const TOPICS: Record<string, Topic> = Object.fromEntries(ALL.map((t) => [t.slug, t]));
