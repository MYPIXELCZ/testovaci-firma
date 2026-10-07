import { COMPANY, PRODUCT, SITE_URL } from "./config";

export const WITHDRAWAL_PATH = "/odstoupeni-od-smlouvy";
export const WITHDRAWAL_URL = `${SITE_URL}${WITHDRAWAL_PATH}`;

/**
 * Vzorové poučení o právu na odstoupení podle přílohy k nařízení vlády č. 29/2023 Sb. (smlouva uzavřená distančně,
 * digitální obsah, který není dodán na hmotném nosiči). Úpravy proti vzoru: bez telefonu (nemáme), bez nákladů na dodání
 * (žádné nejsou), doplněna věta o nepoužívání obsahu po odstoupení.
 */
export const WITHDRAWAL_INFO: { h: string; p: string[] }[] = [
  {
    h: "Právo odstoupit od smlouvy",
    p: [
      "Do 14 dnů máte právo odstoupit od této smlouvy bez udání důvodu.",
      "Lhůta pro odstoupení od smlouvy končí uplynutím 14 dnů ode dne následujícího po dni uzavření smlouvy.",
      `Odstoupit od této smlouvy můžete jakýmkoli jednoznačným prohlášením adresovaným ${COMPANY.name}, ${COMPANY.address}, e-mail ${COMPANY.email} (například dopisem zaslaným prostřednictvím provozovatele poštovních služeb nebo prostřednictvím elektronické pošty). Můžete použít přiložený vzorový formulář pro odstoupení od smlouvy, není to však Vaší povinností.`,
      `Na naší internetové stránce ${WITHDRAWAL_URL} můžete rovněž elektronicky vyplnit a odeslat formulář pro odstoupení od smlouvy nebo jakékoli jiné jednoznačné prohlášení. Využijete-li této možnosti, obratem Vám potvrdíme jeho přijetí v textové podobě (například prostřednictvím elektronické pošty).`,
      "Aby byla dodržena lhůta pro odstoupení od této smlouvy, postačuje odeslat odstoupení od smlouvy před uplynutím příslušné lhůty.",
    ],
  },
  {
    h: "Důsledky odstoupení od smlouvy",
    p: [
      "Pokud odstoupíte od této smlouvy, vrátíme Vám bez zbytečného odkladu, nejpozději do 14 dnů ode dne, kdy nám došlo Vaše odstoupení od smlouvy, všechny peněžní prostředky, které jsme od Vás na základě smlouvy přijali. Pro vrácení peněžních prostředků použijeme stejný platební prostředek, který jste použil(a) pro provedení počáteční transakce, pokud jste výslovně neurčil(a) jinak. V žádném případě Vám tím nevzniknou další náklady.",
      "Po odstoupení od smlouvy digitální obsah dál nepoužívejte a jeho kopie smažte.",
    ],
  },
];

/** Vzorový formulář pro odstoupení od smlouvy (příloha k nařízení vlády č. 29/2023 Sb.), upravený pro digitální obsah. */
export const WITHDRAWAL_FORM_HEAD = "Vyplňte tento formulář a pošlete jej zpět pouze v případě, že chcete odstoupit od smlouvy.";
export const WITHDRAWAL_FORM_LINES = [
  `Adresát: ${COMPANY.name}, ${COMPANY.address}, e-mail ${COMPANY.email}`,
  `Oznamuji, že tímto odstupuji od smlouvy o koupi tohoto digitálního obsahu: ${PRODUCT.name}`,
  "Datum objednání: …",
  "Číslo objednávky (variabilní symbol): …",
  "Jméno a příjmení spotřebitele: …",
  "Adresa spotřebitele: …",
  "Datum: …",
  "Podpis spotřebitele (pouze pokud je tento formulář zasílán na listině): …",
];
