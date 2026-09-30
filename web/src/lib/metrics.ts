// Anonymní měření cesty návštěvníka (pojistka z FAILS.md: metriky u každého projektu).
// Bez cookies, bez úložiště v prohlížeči, bez IP. Jedna návštěva stránky = náhodné ID jen v paměti.
export const PAGES = ["home", "clanek", "objednat", "objednavka", "stahnout", "jine"] as const;
export const EVENTS = [
  "view", "t10", "t30", "t60", "scroll25", "scroll50", "scroll75", "scroll100",
  "cta_buy", "cta_checklist", "form_start", "form_submit", "feedback",
] as const;
export const FEEDBACK = {
  drahe: "Je to na mě drahé",
  zdarma: "Stačí mi šablona zdarma",
  ukazky: "Chci nejdřív vidět víc",
  tabulky: "Nevím, jestli zvládnu tabulku",
  aplikace: "Radši bych aplikaci",
  pozdeji: "Svatbu řeším později",
  jine: "Jiný důvod",
} as const;
export type Page = (typeof PAGES)[number];
export type Event = (typeof EVENTS)[number];
export type FeedbackKey = keyof typeof FEEDBACK;

export function pageOf(pathname: string): { page: Page; topic: string } {
  if (pathname === "/") return { page: "home", topic: "" };
  const seg = pathname.split("/")[1] ?? "";
  if (seg === "objednat" || seg === "objednavka" || seg === "stahnout") return { page: seg, topic: "" };
  if (["nastaveni", "doklad", "obchodni-podminky", "ochrana-osobnich-udaju"].includes(seg)) return { page: "jine", topic: seg };
  return { page: "clanek", topic: seg };
}

const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|curl|wget|python|node-fetch|headless|lighthouse|seznam/i;
export const isBot = (ua: string | null) => !ua || BOT.test(ua);
