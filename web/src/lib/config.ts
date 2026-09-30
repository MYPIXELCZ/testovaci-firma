export const SITE_URL = process.env.SITE_URL ?? "https://anoberu.cz";

/** Prodej a indexace se zapínají až při spuštění (env SALES_OPEN=1, INDEXING=1). */
export const SALES_OPEN = process.env.SALES_OPEN === "1";
export const INDEXING = process.env.INDEXING === "1";

/** Objednávky přes chráněné *.vercel.app (jen tým) jsou testovací: za 1 Kč a i při vypnutém prodeji. */
export const TEST_PRICE = 1;
export const isInternalHost = (host: string | null) => (host ?? "").endsWith(".vercel.app");

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
  // Účet MYPIXEL s.r.o. u Fio banky (veřejný údaj pro platby).
  iban: process.env.PAYMENT_IBAN ?? "CZ5220100000002202343801",
  account: process.env.PAYMENT_ACCOUNT ?? "2202343801/2010",
  recipient: "ANO BERU",
};

/** Po kolika dnech zrušíme nezaplacenou objednávku a smažeme její údaje. */
export const UNPAID_RETENTION_DAYS = 30;
