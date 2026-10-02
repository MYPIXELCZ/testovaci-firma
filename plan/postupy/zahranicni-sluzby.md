# Zahraniční služby: Google hledanost, tržiště pro šablony, hosting klientských webů (akce #15)

Cílová skupina: interní podklad. Hledá a rozhoduje Claude, **platí a schvaluje výdaj Ondřej** (jeho veto: finance a právo). Zpracováno 2026-10-02 (14:25 až 14:55 pražského času), jen výzkum: nic nezaloženo, nic nekoupeno, nikde jsem se neregistroval. Co je odhad, je označeno ODHAD, co jsem nemohl ověřit u zdroje, NEOVĚŘENO. Kurzy ČNB z 2026-10-02: 1 USD = 21,80 Kč, 1 EUR = 24,47 Kč (zdroj 21). „+ DPH“ = 21 % přes režim identifikované osoby (nelze odečíst, tedy skutečný náklad ×1,21).

## Závěr

1. **Google hledanost: DataForSEO, Google Ads Search Volume API.** Tvrdí exaktní čísla z Keyword Planneru, 100 dotazů = 1 úkol = 0,06 USD (1,3 Kč), na zkoušku $1 zdarma bez karty (podle jejich stránek). Pro ≈ 100 dotazů tedy **0 Kč**; další provoz až po vstupním vkladu $50 (1 090 Kč + DPH), který dnes nepotřebujeme. **Korekce `plan/alternativy-2026-10-02.md` (K4):** Keywords Everywhere už nemá „10 USD za 100 tis. kreditů“, jen roční plán od **84 USD (1 831 Kč + DPH)**; 280 Kč v plánu neplatí.
2. **Seznam je jen asi šestina českého hledání** (StatCounter září 2026: Google 78,7 %, Seznam 15,1 %, Bing 4,7 %; ODHAD, měří odkazy z webů ve vzorku, ne dotazy). Čísla ze Skliku (`plan/hledanost-*.md`) tedy podhodnocují celý trh zhruba **5×**. Než se to přepočítá, vyžádat skutečná čísla z DataForSEO.
3. **Prodej šablon: jen Etsy je plně automatizovatelný** (Open API v3 umí vytvořit koncept a nahrát soubor). Lemon Squeezy a Payhip nemají v API vytvoření produktu (zdroj 12), takže produkty by musel zakládat člověk v dashboardu, což je proti pravidlu „Ondřej dělá jen autorizace“. Poplatky Etsy ≈ **14 % (s DPH z poplatků 17 %)** u šablony za 15 USD, Lemon Squeezy ≈ 10 %, Gumroad 13 %, Payhip ≈ 8 až 10 %. **Povinnost registrace k DPH z prodeje nevzniká** (platforma DPH vybírá a odvádí).
4. **Hosting klientských webů: Netlify** (jediný, kdo to oficiálně dovoluje: návod pro agentury a odpověď zaměstnance fóra), zdarma do 300 kreditů měsíčně, pak 9 USD (196 Kč + DPH). Vercel čl. 11 (i) a (iv) to **zakazuje výslovně**. Cloudflare Pages je zdarma a nejsilnější limity, ale čl. 2.2.1(a) je šedá zóna. WEDOS (dnes VEDOS) je nejlevnější, ale jen FTP, a z našeho kontejneru nejde nic než HTTPS (ověřeno).

## 1. Absolutní měsíční hledanost na Googlu (≈ 100 dotazů, cs i en)

| Možnost | Cena | Přesnost | Claude to udělá sám? | Poznámka |
|---|---|---|---|---|
| **DataForSEO Google Ads Search Volume** (`/v3/keywords_data/google_ads/search_volume/live` nebo standard task) | $0,06 (standard, 1 až 3 h) nebo $0,09 (live) za úkol až se 1 000 slovy; $1 zdarma po registraci; poté min. vklad $50 | podle výrobce exaktní hodnoty, ne pásma 1K–10K; Google slučuje podobné dotazy a u nízkých objemů nevrací nic | ano, HTTPS API (z kontejneru dostupné: `api.dataforseo.com` odpovídá 401) | ČR `location_code` 2203 (z paměti, ověřit voláním `/keywords_data/google_ads/locations`), jazyk `cs`; EN: 2840 (USA), 2826 (UK), jazyk `en`; limit 12 live požadavků za minutu |
| Google Ads Keyword Planner, účet bez kampaně | 0 Kč | **jen pásma** (0–100, 100–1K, 1K–10K, 10K–100K), nízké objemy nezjistitelné | ne (rozhraní; API vyžaduje developer token) | k rozhodování o hranici ~1 000 hledání nepoužitelné; nutná fakturační údaje (zdroj 1), zdroje se liší, jestli i bez platební karty (zdroj 3) |
| Keyword Planner s běžící kampaní | ODHAD 5 až 10 USD/den na 7 až 14 dní = 760 až 3 050 Kč + DPH | exaktní (podle zdrojů 2, 3; práh Google neuvádí, NEOVĚŘENO) | částečně | neúměrné rozpočtu; „forecast s vysokým CPC“ dává jen impresní odhad |
| Keywords Everywhere (Bronze) | 84 USD/rok = 1 831 Kč + DPH; platí se jen ročně | data z Keyword Planneru, 1 kredit na slovo, 100 slov na požadavek, API na všech plánech | ano, REST + Bearer | ČR v seznamu zemí: NEOVĚŘENO (oficiální seznam vrací 404, nepřímý zdroj říká ano) |
| Semrush free, Ubersuggest free, Ahrefs Keyword Generator | 0 Kč | Semrush Free: 10 reportů denně; Ubersuggest: 3 hledání denně; Ahrefs: odhady, ČR NEOVĚŘENO | **ne** (jen rozhraní, API je v dražších plánech: Semrush od 455,67 USD/měs.) | ruční práce, nevhodné |
| Google Search Console | 0 Kč | skutečné imprese a kliky **jen našich webů** | ano, API, ale potřebuje jednorázové OAuth/servisní účet od Ondřeje | po spuštění ověřuje odhady, před spuštěním nic nezjistí |
| Google Trends | 0 Kč | jen relativní (index 0 až 100) | z kontejneru jde (viz CLAUDE.md) | použít max. jako kalibraci vůči absolutním číslům |

**Doporučený nejlevnější postup (≈ 0 Kč):**
1. Claude připraví seznam ≈ 100 dotazů (cs i en) do jednoho úkolu, soubor `plan/hledanost-google-<projekt>.md` (stejný formát jako Sklik) + sloupec „poměr Google/Seznam“ u dotazů, které už máme ze Skliku. Tím se **změří skutečný poměr** místo mého ODHADU ×5.
2. Ondřej (autorizace): zaregistruje účet DataForSEO na firemní e-mail (ověření e-mailu) a předá Claudovi přihlašovací údaje API do scratchpadu (`.dataforseo`, do repa NEUKLÁDAT). Platební metoda se snad nevyžaduje (stránky DataForSEO: „No Credit Card“, jedna recenze píše, že kredit přibude až po zadání platební metody, NEOVĚŘENO; pak karta firmy a bez vkladu).
3. Claude pošle 1 úkol (100 slov, $0,06 až $0,09), zapíše výsledek a spustí `plan/verdikt.py` s parametry pro Google.
4. Vklad $50 (≈ 1 090 Kč + DPH, přesahuje zbývajících ~700 Kč) **jen když** výsledek ukáže niku s ≥ 1 000 hledání měsíčně, nebo $1 nestačí. DataForSEO uvádí vrácení nevyužitého vkladu do 30 dnů, ale jiný zdroj tvrdí „nevratné“ (NEOVĚŘENO).

**Čeho se vyvarovat:** koupit Keywords Everywhere za 1 831 Kč kvůli 100 dotazům; spoléhat na pásma z Keyword Planneru; psát „hledanost na Googlu“ z Trends; hledat obcházení (scraping Googlu, captcha), je zakázáno.

## 2. Prodej digitálních šablon z ČR: Etsy, Lemon Squeezy, Gumroad, Payhip

Výpočet na šabloně za **15 USD (327 Kč)**.

| | Etsy | Lemon Squeezy | Gumroad | Payhip |
|---|---|---|---|---|
| Poplatky | inzerát 0,20 USD (každé 4 měs. a při každém prodeji u vícekusového), 6,5 % transakční, platba **4 % + 0,30 EUR** (zdroj 9, ČR) | 5 % + 0,50 USD, +1,5 % mezinárodní, +1,5 % PayPal, výplata Stripe do zahraničí 1 %, PayPal mimo USA 3 % (max. 30 USD) | 10 % + 0,50 USD přímý prodej, **30 %** přes Discover | 5 % (zdarma), 29 USD/měs. = 2 %, 99 USD/měs. = 0 %; k tomu Stripe/PayPal zvlášť |
| Při 15 USD | 2,11 USD = **14 %**; s DPH z poplatků 2,55 USD = 17 %; Offsite Ads +15 % (u prodejů z jejich reklamy; do 10 000 USD ročně lze vypnout, nad to 12 % povinně) | 1,48 USD = 9,8 % (+ výplata ≈ 10,8 %) | 2,00 USD = 13,3 % | 0,75 USD + Stripe/PayPal ≈ 8 až 10 % (poplatky Stripe NEOVĚŘENO) |
| Jednorázově | **15 až 29 USD** za otevření obchodu (327 až 632 Kč, nevratné, částka proměnlivá, zdroje 9) | 0 | 0 | 0 |
| DPH z prodeje | Etsy je **plátcem DPH místo vás** pro digitální položky kupujícím v EU od 2021-07-01 (vybírá a odvádí, částku dostanete očištěnou); zdroj 10 | Merchant of Record, daně řeší sám | Merchant of Record od 2025-01-01 | Payhip vybírá a odvádí EU a UK DPH, ostatní země (USA, Kanada…) ne |
| Výplata do ČR | Etsy Payments, banka v EU (ověřená), CZK účet; **14 až 20 dní po prodeji prvních 90 dní**, rolling reserve až 45 dní, někdy 180 (zdroje 9, NEOVĚŘENO přímo u Etsy) | bankou (CZ i CZK podporovány) nebo PayPal, 2× měsíčně | bankou (ČR v seznamu), PayPal nebo Stripe Connect | hned na vlastní Stripe/PayPal |
| Doručení souboru | automaticky po platbě; **max. 5 souborů po 20 MB**, PDF/ZIP/obrázky; Google Tabulky = PDF s odkazem „vytvořit kopii“ (běžná praxe) | hostují soubory sami, soubory bez limitu | hostují | hostují |
| Pravidla k AI a šablonám | povoleno, **nutné uvést AI**: atribut „Designed by seller“ a věta v popisu; zakázáno hromadné generování téměř stejných inzerátů a prodej surového AI výstupu; porušení = smazání inzerátu nebo obchodu (zdroje 9; oficiální stránky Etsy blokují roboty, text je ze sekundárních zdrojů, NEOVĚŘENO) | neověřeno, obecná pravidla (zakázané produkty, KYC obchodu) | neověřeno | neověřeno |
| Vlastní návštěvnost | **ano** (tržiště; konkurence TheSheetCode 3,9 tis. prodejů za 4 roky) | ne | jen Discover (30 %) | ne |
| Otevření | obchod týž den po ověření (ID + selfie, banka); první výplata za ≈ 3 až 5 týdnů (ODHAD) | schválení obchodu **2 až 3 pracovní dny podle dokumentace, v praxi 1 až 4 týdny** (zdroj 11), Stripe jej postupně převádí na „Managed Payments“ (náhled ≈ 6,4 % + 0,30 USD), poplatky se tedy mohou změnit; zda se nový obchod ještě dá založit bez omezení: NEOVĚŘENO | hned, výplata bankou podle zdroje 12 | hned |
| Vytvoření produktu přes API | **ano** (`createDraftListing`, `uploadListingFile`, scope `listings_w`; klíč z „Your Apps“, schválení klíče NEOVĚŘENO) | **ne** (jen čtení a soubory) | NEOVĚŘENO | **ne** (jen kupóny a licenční klíče) |

**DPH pro neplátce s.r.o. (shrnutí):**
- **Registrace k DPH z těchto prodejů nevzniká.** Limit plátce je 2 mil. Kč za 12 měsíců (zdroj 14), cíl šablon je 3 až 10 tis. Kč měsíčně. Prodej přes platformu se do limitu 10 000 EUR pro OSS nepočítá (platforma je zdaňující osoba; zdroj 10, ODHAD).
- **Vlastní prodej do EU (printopia.cz, anoberu.cz):** do 10 000 EUR ročně spotřebitelům v jiných státech EU zůstává český režim = bez DPH; nad limit OSS nebo registrace v zemi (zdroj 14). Prodáváme dnes jen do ČR, hlídat slovenské kupující.
- **Poplatky platforem:** Etsy bez DIČ účtuje DPH ze svých poplatků (sazba vaší země = 21 %), s DIČ reverse charge (zdroj 10). U Lemon Squeezy, Gumroad a Payhip je otázka, zda jejich odpočet z platby je „přijatá služba“ (pak identifikovaná osoba: přihláška do 15 dnů, měsíční přiznání do 25. dne, DPH nelze odečíst, kontrolní hlášení ne; zdroj 14) nebo jen snížení ceny dodávky platformě. **NEOVĚŘENO, jedna otázka pro účetní**, do té doby počítat +21 % ze všech poplatků.
- Platformy hlásí příjmy prodejců finančním úřadům (EU směrnice DAC7; ze zdrojů neověřeno), příjem zaúčtovat jako tržbu s.r.o. v USD/EUR podle kurzu.

**Co je nutné před prvním prodejem (Etsy):**
- [ ] Rozhodnutí o výdajích: setup 15 až 29 USD (327 až 632 Kč) + inzeráty 0,20 USD; sonda 12 inzerátů ≈ 770 až 1 160 Kč včetně DPH (odpovídá `plan/alternativy-2026-10-02.md`). Přesahuje zbývajících ~700 Kč. Ondřej schvaluje.
- [ ] Ondřej (autorizace): účet Etsy za s.r.o. (IČO, sídlo, kontaktní osoba, telefon), ověření totožnosti (průkaz + selfie), 2FA, ověřený bankovní účet (Fio CZK), firemní karta na poplatky.
- [ ] DIČ Etsymu nezadávat, pokud nechceme reverse charge (jinak identifikovaná osoba); rozhodnout s účetní.
- [ ] Claude: požádat o Etsy API klíč (Your Apps), OAuth souhlas dá Ondřej jednorázově.
- [ ] Claude: texty v angličtině, AI uvést v každém popisu, atribut „Designed by seller“, žádné cizí obrázky/značky, vzorce ověřené přepočtem (odpovědnost).
- [ ] Claude: 12 inzerátů ve 4 nikách, ne 100 klonů (riziko zákazu hromadného generování).
- [ ] Právo: obchodní podmínky/licence v angličtině a práva spotřebitele EU (14 dní na odstoupení a výjimka u digitálního obsahu při okamžitém stažení: jak to řeší Etsy a jak se to promítne do našich podmínek, NEOVĚŘENO), výslovné schválení Ondřejem.

## 3. Hosting klientských webů („Web za 24 hodin“, správa e-shopů)

| Služba | Cena | Podmínky pro hosting cizích webů | Automatizace Claudem | Přístup klienta |
|---|---|---|---|---|
| **Vercel Pro** (máme) | 20 USD/uživatel/měs. = 436 Kč + DPH; plné zdroje: Fair Use zdroj 15 | **čl. 11 (i)** zakazuje „sublicense, resell, rent, lease … or make the Services available to any third party“ a **(iv)** „use the Services for timesharing or service bureau purposes or otherwise for the benefit of a third-party“ (přečteno z plného textu 2026-10-02); Fair Use ale říká, že komerční je i „receiving payment to create, update, or host the site“ a to Pro dovoluje. Rozpor, rozhodne jen písemný souhlas supportu | ano (HTTPS API, konektor už máme) | jen jako člen týmu |
| **Cloudflare Pages Free** | 0 Kč; 100 projektů, 100 domén na projekt, 500 buildů/měs., 20 000 souborů × 25 MiB; statické požadavky zdarma a neomezeně | Self-Serve Agreement **2.2.1(a)**: nesmíte „sell access to the Services to any third party, or sign up for the Services on behalf of a third party“; **(h)**: na free webu se nesmí sbírat údaje o platebních kartách. Komunita: hostování klientů pod vlastním účtem je prý OK, **není to potvrzeno Cloudflarem**; oficiální cesta je agenturní program | ano (`wrangler pages deploy`, API; z kontejneru `api.cloudflare.com` odpovídá) | klient si založí vlastní účet a přizve nás (komunitní doporučení) |
| **Netlify** | Free 0 Kč, 300 kreditů, **tvrdý limit** (web se zastaví); Personal 9 USD = 196 Kč + DPH, 1 000 kreditů; Pro 20 USD = 436 Kč + DPH, 3 000 kreditů, neomezeně členů. Kredity: deploy 15, 1 GB přenosu 20, 10 000 požadavků 2, formuláře zdarma | SSA říjen 2025 **2.4(a)**: „resell or license the Netlify Services to third parties“ (užší než Vercel). **Zaměstnanec fóra: klientům smíte účtovat, co vám účtuje Netlify, doporučuje se samostatný účet na klienta; Pro není povinné**; oficiální návod „free cloud hosting … great for client projects“ | ano (HTTPS API, `api.netlify.com` odpovídá) | klient má vlastní účet (zdarma) nebo web převedeme na jeho tým (ODHAD, ověřit) |
| **VEDOS (dříve WEDOS)** | NoLimit: 1. rok 47,19 Kč/měs. s DPH (kupón), potom **121 Kč/měs. s DPH**; LowCost 39,93 Kč s DPH 1. rok, 66,55 po obnovení; Extra 242 Kč po obnovení | „NoLimit je univerzální hosting pro vývojáře, agentury“, aliasy (3 zdarma, lze neomezeně); české faktury, žádná zahraniční služba ani identifikovaná osoba | **ne, nebo jen obtížně**: nasazení je FTP a z kontejneru je dostupné jen HTTPS (FTP/SSH porty ověřeně zablokované), HTTPS API není známo (NEOVĚŘENO) | FTP přístupy sdílené, klient bez vlastního panelu |
| **Hetzner Cloud CX23** | 5,49 EUR/měs. (od 15. 6. 2026) = 134 Kč + DPH, 20 TB provozu | všeobecné podmínky 7.1: zákazník smí poskytnout třetím stranám právo užívat službu; zákaz jen přeprodeje | částečně: vytvoření serveru přes HTTPS API, nasazení stahováním z GitHubu (Caddy + cron), SSH ne | klient bez přístupu, nutná správa a zálohy Claudem |
| GitHub Pages | 0 Kč | **nepoužít**: podmínky zakazují provoz podnikání a e-shopů | – | – |

**Doporučení (nejjednodušší bezpečná varianta):**
1. **Statické weby klientů (3 990 až 4 990 Kč): Netlify**, jeden účet firmy, Free do ~5 malých webů, pak Personal 9 USD (196 Kč + DPH, platí se až při překročení, nikdy dřív). ODHAD: malý web 1 až 3 GB/měs. = 20 až 60 kreditů + deploy 15 → 5 webů vyjde ≈ 300 kreditů. **Smluvně prodávat „zhotovení webu + správu“, ne „hosting Netlify“** (2.4(a)); kontrolu podmínek potvrdit e-mailem na support Netlify, odpověď přiložit.
2. **Náhledy před zaplacením (`noindex`) a vlastní ukázky: Cloudflare Pages Free** (náš obsah, ne klientův; bez zadávání karet na free webu).
3. **Plán B pro klienta, který chce vlastnit hosting:** předat zdrojové soubory (z našeho repa), nebo nasadit na jeho vlastní účet Netlify/Cloudflare (klient se registruje sám, Claude nasadí s jeho přizváním).
4. **Vercel pro cizí weby ne**, dokud Vercel support nepotvrdí písemně (alternativa: projekt v klientově týmu, klient platí 20 USD/měs.).
5. **E-shopy na Shoptetu** hosting neřešíme (hostuje Shoptet), řešíme jen přístup do administrace (zpracovatelská smlouva).
6. **VEDOS** jen pro klienty, kteří už hosting mají (WordPress, PHP); nasazení by museli dělat oni nebo Ondřej, ne Claude.

Co autorizuje Ondřej: účet Netlify na firemní e-mail (přihlášení, ověření, osobní přístupový token do scratchpadu), případně schválení 9 USD měsíčně při překročení Free (finance); smlouvu o správě a podmínky (právo; v `plan/web-za-24-hodin.md` už je, doplnit větu, že hosting není předmětem přeprodeje).

## 4. Další zahraniční kanály s vlastním provozem (max. 3)

1. **SEO pro Google, měřené přes Search Console API.** Google = 78,7 % českých vyhledávání (zdroj 6), Seznam jen 15,1 %. Pokud poměr platí, „cermat testy“ (Sklik podzim 1,1 až 1,4 tis., špička 4,1 tis.) má na Googlu ≈ 5,7 až 7,3 tis. měsíčně (špička ≈ 21 tis.), Printopie ø 53 → ≈ 277 (špička 360 → ≈ 1 880) (**ODHAD**, ověřit krokem 1). Cena 0 Kč, všechny weby už mají značku Search Console. Ondřej: jednorázový souhlas OAuth pro API (nebo servisní účet přidaný jako vlastník). Přepočet verdiktu `plan/verdikt.py` na Google až s daty z DataForSEO.
2. **Upwork a Fiverr pro služby K1 až K3 zahraničním klientům.** Fiverr bere 20 % z objednávky (zdroj 17), Upwork 0 až 15 % podle smlouvy (od 2025-05-01; jiný zdroj píše 10 %), nabídka stojí 6 až 16 Connects po 0,15 USD = 0,90 až 2,40 USD (20 až 52 Kč) (zdroj 17). Pro test 20 nabídek ≈ 18 až 48 USD (390 až 1 050 Kč) + DPH; nad rozpočtem, proto až po výsledku sondy K1. Poptávka a ceny za web od zahraničních zadavatelů: NEOVĚŘENO, konkurence obrovská.
3. **Google Merchant Center, bezplatné nabídky (free listings).** Česko je podporováno (zdroj 16), feed pro Zboží.cz už máme (`/feed/zbozi.xml`), náklad 0 Kč a 1 až 2 h práce Clauda na převod do formátu Google. **Riziko:** pravidla Google říkají, že prodej digitálních knih/e-booků není povolen (oficiální stránka bez rozlišení kanálů, sekundární zdroje tvrdí, že free listings je výjimka); jestli Google sadu PDF listů za e-book považuje, je NEOVĚŘENO, zjistí se až při odeslání feedu. Ondřej: založení účtu Merchant Center a ověření domény (stačí stávající značka Search Console).

## Zdroje

Všechny navštíveny 2026-10-02, pokud není uvedeno jinak. Oficiální stránky Etsy (help.etsy.com, etsy.com/legal) odpovídají robotům 403, proto čísla Etsy pocházejí ze sekundárních zdrojů a jsou označena.

Google hledanost:
1. Google Ads Help, požadavky Keyword Planneru: https://support.google.com/google-ads/answer/7337243
2. Keywords Everywhere (zdroj s konfliktem zájmů), pásma bez útraty: https://keywordseverywhere.com/google-keyword-planner-volume.html
3. Rankdots (účet bez kampaně v Expert Mode): https://rankdots.com/blog/google-keyword-planner
4. Keywords Everywhere, plány a API: https://keywordseverywhere.com/compare-plans.html , https://keywordseverywhere.com/api-documentation.html
5. DataForSEO, ceny: https://dataforseo.com/pricing/keywords-data/google-ads , https://dataforseo.com/pricing (min. vklad 50 USD), FAQ (trial 1 USD, faktury, vrácení DPH): https://dataforseo.com/faq , exaktní hodnoty a 1 USD zdarma: https://dataforseo.com/keyword-planner-api , dokumentace: https://docs.dataforseo.com/v3/keywords_data-google_ads-search_volume-live/
6. StatCounter, podíl vyhledávačů v ČR (září 2026): https://gs.statcounter.com/search-engine-market-share/all/czech-republic
7. Semrush ceny: https://www.semrush.com/prices/ ; Ahrefs: https://ahrefs.com/keyword-generator ; Ubersuggest (sekundární, 29 USD/měs. nebo 290 USD jednorázově): https://seoscaleup.com/blog/ubersuggest-pricing/
8. ČNB, denní kurz: https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt

Tržiště:
9. Etsy poplatky (sekundární): https://www.edesk.com/blog/etsy-seller-fees/ , https://craftybase.com/blog/the-complete-guide-to-etsy-fees , https://www.valueaddedresource.net/etsy-variable-shop-setup-fee/ (setup 15 až 29,5 USD, od 2024) ; rozpor: https://www.voolist.com/blog/etsy-fees-explained-2026 („bez setup poplatku“); AI pravidla: https://www.promptlesspress.com/blog-etsy-ai-policy-2026-digital-products (výklad komerčního nástroje); platby a rezervy: https://www.insightagent.app/guides/etsy-payment-holds-new-sellers-guide
10. Etsy DPH: https://www.bontello.com/en/blog/eu-vat-etsy-sellers-2026 (Etsy jako „deemed supplier“, nepočítá se do OSS), https://synder.com/fees-etsy/vat-on-etsy/ (DPH z poplatků, reverse charge s DIČ)
11. Lemon Squeezy: https://www.lemonsqueezy.com/pricing , https://docs.lemonsqueezy.com/help/getting-started/fees , https://www.lemonsqueezy.com/migration-offer , doba schválení: https://www.passivekit.com/lemonsqueezy-verification-time/ , Stripe Managed Payments (sekundární): https://www.paritydeals.com/stripe-managed-payments-vs-lemon-squeezy-fees/
12. Gumroad: https://gumroad.com/pricing , výplaty: https://help.gumroad.com/article/13-getting-paid ; API produkty: Lemon Squeezy https://lemonsqueezy.nolt.io/279 , Payhip https://payhip.com/api-reference
13. Payhip: https://payhip.com/pricing , DPH: https://payhip.com/blog/payhip-takes-care-of-vat/
14. DPH: Fakturoid (OSS, neplátce, 10 000 EUR) https://www.fakturoid.cz/almanach/dane/dph-oss-zvlastni-rezim-jednoho-spravniho-mista ; Pohoda (identifikovaná osoba: 15 dní, přiznání do 25. dne, bez kontrolního hlášení) https://portal.pohoda.cz/dane-ucetnictvi-mzdy/dph/prijeti-sluzeb-ze-zahranici-z-pohledu-dph/ ; limit plátce 2 mil. Kč: https://pexpats.com/how-czech-vat-works

Hosting:
15. Vercel Terms (čl. 11, stažen a přečten celý text): https://vercel.com/legal/terms ; Fair Use (aktualizováno 2026-09-14): https://vercel.com/docs/limits/fair-use-guidelines ; Cloudflare Self-Serve Agreement 2.2.1: https://www.cloudflare.com/terms/ ; Pages limity: https://developers.cloudflare.com/pages/platform/limits/ , statická aktiva: https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ ; Netlify SSA (říjen 2025, 2.4a): https://www.netlify.com/pdf/self-serve-subscription-agreement.pdf/ , fórum: https://answers.netlify.com/t/netlify-hosting-for-clients-websites/107102 , návod: https://www.netlify.com/guides/netlify-free-cloud-hosting/ , ceny a kredity: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/ ; VEDOS (wedos.cz přesměruje na vedos.cz): https://vedos.cz/webhosting/ ; Hetzner ceny: https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ , podmínky 7.1: https://www.hetzner.com/legal/terms-and-conditions/
16. Google Merchant Center: digitální knihy https://support.google.com/merchants/answer/14183113 , země free listings https://support.google.com/merchants/answer/9199328
17. Fiverr, Upwork (sekundární): https://freelancercalculator.com/fiverr-seller-fees-2026-official-guide/ , https://www.vortenza.com/guides/upwork-fees-2026 , Connects https://aiproposer.com/learn/upwork-connects-explained

## Kontrolní seznam před výdajem nebo registrací

- [ ] Hledanost Google: Ondřej zaregistruje DataForSEO (firemní e-mail), Claude odešle 1 úkol (≈ 100 slov), zapíše `plan/hledanost-google-<projekt>.md` a změřený poměr Google/Seznam; vklad $50 jen po výsledku.
- [ ] Hosting: napsat na support Netlify s popisem služby (web + správa, jeden účet, klienti bez přístupu), odpověď uložit do `plan/postupy/`; do té doby jen vlastní ukázky.
- [ ] Zeptat se účetní jednou: poplatky Etsy/Lemon Squeezy/Gumroad/Payhip = přijatá služba (identifikovaná osoba)? Etsy s DIČ nebo bez?
- [ ] Etsy: schválení výdaje (setup 15 až 29 USD + inzeráty) a právní text v angličtině od Ondřeje; žádné obcházení captcha, ověřování, TLS.
- [ ] Opravit v `plan/alternativy-2026-10-02.md` a `plan/akce.md` číslo „Keywords Everywhere 280 Kč“ na DataForSEO zdarma a upozornit na poměr Google/Seznam (nic v plánu jsem nezměnil).

## Nejistoty (souhrn)

- Přesnost DataForSEO je tvrzení výrobce; ověřit na dvou dotazech, které známe ze Skliku (poměr musí vyjít kolem 3 až 7).
- $1 zdarma „bez karty“: dvě verze, ověří registrace.
- Etsy: oficiální stránky blokují roboty, poplatek ČR (4 % + 0,30 EUR), setup 15 až 29 USD, rezervy a pravidla k AI jsou ze sekundárních zdrojů.
- Zda poplatky Lemon Squeezy/Gumroad/Payhip zakládají identifikovanou osobu, nevím (jedna otázka pro účetní).
- Cloudflare 2.2.1(a) a Vercel (i)/(iv): výklad čeká na písemné vyjádření dodavatele, rozhodnutí o riziku je Ondřejovo (právo).
- Google Merchant Center: nevím, zda je sada PDF „digitální kniha“.
