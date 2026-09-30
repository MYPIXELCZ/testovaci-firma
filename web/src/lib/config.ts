export const SITE_URL = process.env.SITE_URL ?? "https://anoberu.cz";

export const PRODUCT = {
  name: "Svatební plánovač Ano, beru",
  price: 349,
  file: "svatebni-planovac-anoberu.xlsx",
};

export const COMPANY = {
  name: "MYPIXEL s.r.o.",
  address: "Příčná 1892/4, Nové Město, 110 00 Praha 1",
  ico: "17617421",
  register: "zapsaná v obchodním rejstříku vedeném Městským soudem v Praze, oddíl C, vložka 373971",
  email: "anoberu@mypixel.cz",
  vat: "Nejsme plátci DPH.",
};

export const PAYMENT = {
  // Účet MYPIXEL s.r.o. u Fio banky. Doplní se přes env, dokud ho nemáme.
  iban: process.env.PAYMENT_IBAN ?? "",
  account: process.env.PAYMENT_ACCOUNT ?? "",
  recipient: "ANO BERU",
};

/** Po kolika dnech zrušíme nezaplacenou objednávku a smažeme její údaje. */
export const UNPAID_RETENTION_DAYS = 30;
