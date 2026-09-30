// Anonymní měření cesty návštěvníka (test poptávky): bez cookies, bez úložiště v prohlížeči, bez IP.
// Jedna návštěva stránky = náhodné ID jen v paměti stránky (po zavření zmizí).
export const PAGES = ["home", "koupit", "tema"] as const;
export const EVENTS = [
  "view", "scroll25", "scroll50", "scroll75", "scroll100", "t10", "t30", "t60",
  "cta_sample", "cta_buy", "topic_link", "solution_open", "form_start", "form_submit", "pdf_download", "feedback",
] as const;
export const FEEDBACK = {
  drahe: "Je to na mě drahé",
  ukazky: "Chci nejdřív vidět víc ukázek",
  pomuze: "Nevím, jestli to pomůže",
  zdarma: "Stačí mi testy zdarma",
  jine_hledam: "Hledal/a jsem něco jiného",
  pozdeji: "Zatím je brzy, řeším později",
  jine: "Jiný důvod",
} as const;
export type Page = (typeof PAGES)[number];
export type Event = (typeof EVENTS)[number];
export type FeedbackKey = keyof typeof FEEDBACK;
