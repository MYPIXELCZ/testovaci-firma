# Služba „AI správa reklamních kampaní (PPC)“: kandidát od Ondřeje, 2026-10-02

Cílová skupina: hledá, používá i platí majitel malé firmy nebo e-shopu (B2B, reklama 3 až 20 tis. Kč měsíčně). Doloženo poptávkami na čtyřech portálech (oddíl 3). Nezletilých se služba netýká.
Čísla jsem četl nebo měřil 2026-10-02 (WebFetch, curl, nápověda Skliku a Googlu, ceníky). Co je odhad nebo úsudek, je označeno. Podklad hledanosti: `plan/hledanost-alt3-ppc.md`.

## Doporučení

**Samostatně NESTAVĚT. Jako vrstva k K2 (a K1) ANO, ale jen jako odpovědi na poptávky a audit zdarma, bez placené reklamy a bez stavby nástroje před první závaznou poptávkou.**

1. Poptávka je malá: ≈ 8 až 12 poptávek na PPC měsíčně napříč čtyřmi portály (překrývají se), koncových klientů ≈ 5 až 8, většinou chtějí Google Ads a Meta, Sklik výslovně 1 z ≈ 10 zadání, která jsem přečetl.
2. Cena je stlačená platformou samotnou: Seznam prodává založení + správu Skliku za 1 500 až 3 000 Kč (Mini, Standard), freelanceři 3 000 až 10 500 Kč měsíčně. „AI“ není důvod ke koupi. Na 10 000 Kč zisku je třeba 4 až 7 klientů za 1 500 až 2 500 Kč.
3. Nemáme výsledky: naše kampaň Printopia má za 7 dní 2 zobrazení, 0 prokliků, 0 Kč (`tools/stav.py` 2026-10-02), Nákupy na Zboží.cz 0 zobrazení. Nesmíme to skrývat ani vydávat za důkaz kvality.
4. Riziko je vyšší než u K1: odpovědnost za cizí útratu a za obsah reklam (§ 6b zákona 40/1995: zpracovatel a zadavatel odpovídají společně a nerozdílně).
5. `verdikt.py` (kopie ve scratchpadu, repo nezměněno): ověřitelnost do 3 dnů NE (0,9 dosažitelných vs. 9 potřebných návštěv/signálů), dostatečný prodej NE (zisk 855 Kč měsíčně při 7 poptávkách měsíčně, výhra 4 %, 2 500 Kč; při růstu 30 % měsíčně jen 4 127 Kč za 6 měsíců). Sonda potřebuje „Výjimku schválenou Ondřejem“.

Odhady (úsudek, ne měření): ≥ 1 závazná poptávka do 72 h ≈ **12 %** (5 až 20 %), věcná reakce ≈ 40 %; ≥ 3 klienti do 6 měsíců ≈ **12 %** (5 až 25 %); zisk ≥ 10 000 Kč měsíčně jen z PPC do 6 měsíců ≈ **3 %**. Jako vrstva k K2 přidá ve středním scénáři ≈ 2 500 až 3 500 Kč měsíčně v 6. měsíci (oddíl 4).

## 1. Konkurence a ceny (2026-10-02)

| Kdo | Nabídka a cena (bez DPH) | Min. rozpočet na reklamu | Reference, recenze | Zdroj |
|---|---|---|---|---|
| **Seznam (Sklik Mini)** | založení + správa 3 měs. 1 500 Kč, 6 měs. 2 000 Kč; **není pro e-shopy**; jen přímí zákazníci | < 30 000 Kč měsíčně | platforma sama | seznam.cz/reklama/…/sklik-podpora-cena |
| **Seznam (Sklik Standard / Profi)** | Standard: založení + 2 měs. 3 000 Kč, dál 2 000 Kč/měs.; Profi: založení 10 000 Kč, správa 5 000 Kč/měs. | Standard < 30 000, Profi ≥ 30 000 Kč | platforma sama | tamtéž |
| Filip Farník (filipfarnik.cz) | od 8 000 Kč/měs. za 1 systém (jen dohled od 4 000); škála 10 100 Kč při 30 tis., 15 000 při 100 tis. | do 20 000 Kč | neuvedeno na stránce | filipfarnik.cz/sluzba/sprava-ppc-kampani |
| Jiří Navrátil (jirinavra.cz) | 1 500 Kč/h; Lite 3 750 Kč/měs. (2,5 h), Standard 6 000 Kč/měs.; často 15 % z rozpočtu | neuvedeno | blog, bez referencí | jirinavra.cz/blog/kolik-stoji-sprava-ppc-kampani |
| Pajskr (pajskr.cz) | 4 597 až 12 597 Kč/měs.; audit 4 000 Kč (nyní zdarma) | od ≈ 10 000 Kč | bez referencí | pajskr.cz/sprava-ppc |
| Jiří Kroužek (jirikrouzek.cz) | 8 000 Kč/měs. (8 h), složité od 12 000; účty vždy majetkem klienta | neuvedeno | neuvedeno | jirikrouzek.cz |
| SEMTIX (Liberec) | 4 900+ (rozpočet do 15 tis.), 8 400+ (do 35 tis.), 14 900+ | do 15 000 Kč | bez referencí | semtix.cz/ppc |
| Klikavec.cz | od 10 500 / 18 000 / 24 000 Kč/měs.; 1 500 Kč/h; od 2013 | neuvedeno | Google Premier Partner, ≈ 12 log klientů | klikavec.cz |
| PPC Pohotovost | správa 5 000 Kč/měs. + min. 15 000 Kč reklamy; urgentní zásah od 3 000 Kč | 15 000 Kč | „150+ spravovaných účtů“ | ppcpohotovost.cz |
| ppcfreelancer.cz | 800 Kč/h; nové Google Ads účty s 8 500 Kč kreditu | neuvedeno | Google Partner, Sklik partner, Shoptet partner | ppcfreelancer.cz |
| ADVIS Marketing | e-shopy od 3 % z obratu; měření (GTM) 10 999 Kč; měsíčně bez závazku | od 5 000 Kč | neuvedeno | advis-marketing.cz/cenik-sprava-ppc |
| Petra Březinová (Firmy.cz) | „od 2 500 Kč“ v nadpisu, 3 000 Kč v detailu | neuvedeno | 7 let praxe, **0 recenzí** | firmy.cz/sluzby/nabidka/… |
| SeoAudits (jaudelam.cz) | textová kampaň Sklik 499 Kč (1 kampaň, 10 sestav) | – | **0 prodejů**, 2 recenze, prodejce offline | jaudelam.cz |
| Bazoš sekce Služby | ≈ 10 inzerátů „PPC“ (web + SEO + PPC): 3 999 až 6 000 Kč nebo dohodou | – | – | sluzby.bazos.cz |

**Automatizace, která už existuje (a kterou kupující zná):**
- **Sklik Chytrá kampaň** (Seznam AI, od 06/2025; podle blogu 05/2026 i pro vyhledávání): inzerent dodá texty a obrázky, cílení a umístění řeší systém. **Maximalizace konverzí** (od 08/2025, ≈ 300 inzerentů v únoru 2026): vyžaduje ≥ 30 konverzí za 30 dní. Seznam v podmínkách nezaručuje, že se nepřekročí zadané CPA.
- **Shoptet Kampaně** (Performance Max v administraci e-shopu): 6 až 10 % z útraty, zdroje se liší (8,5 až 10 %).
- **Google Performance Max**, **Mergado** (feedy pro Zboží.cz a Heureku od 229 Kč měsíčně), **MarketingPPC** (vlastní automatizace, „Alarmy“ od 3 500 Kč), **Conviu** (generátor reklam a feedů pro Google Ads a Sklik, „3 000+ klientů“).

Závěry: (a) cenová podlaha pro malé klienty je 1 500 až 2 000 Kč měsíčně u platformy samotné, my pod ni jít nemůžeme; (b) trh sám říká, že pod ≈ 10 000 Kč reklamy správa nedává smysl (Pajskr od 10 tis., Martin Kovalčík 20 tis., marketingppc.cz 10 až 15 tis.), segment 3 až 20 tis. Kč je tedy na hraně a rozumná správa má podíl na reklamě 15 až 50 %; (c) žádný konkurent neprodává „AI“, ale ani to nikdo nehledá; (d) audit nabízejí zdarma (Pajskr, ADVIS), takže zdarma audit je standard, ne výhoda.

## 2. Technika a pravidla

**Sklik (jádro, funguje nám přes API).**
- Přístup: klient v Nastavení účtu nabídne přístup našemu účtu, druhá strana ho potvrdí. Role: Reporter statistik (jen čtení), Správce kampaní (vytváří a upravuje kampaně, nemění zřizovací nastavení), Administrátor účtu (vše včetně přístupů). **Kredit může dobít jen přihlášený majitel účtu**, žádná role to neumí (napoveda.sklik.cz/en/acces-to-account).
- API: přihlášení `client.loginByToken` naším tokenem, u každého volání se posílá `user.userId` spravovaného účtu; `client.get` vrací `foreignAccounts[].userId`. Report max. 5 000 řádků na čtení; minutový a denní limit volání vrací `api.limits` (hodnoty neznám). Náš `sklik_api.py` posílá jen `user = {"session": …}` (řádek 78), pro cizí účty je třeba doplnit `userId` a parametrizovat kampaň (odhad ≈ 1 den práce). **Cizí účet jsme dosud nespravovali, technika je neotestovaná.**
- Podmínky Skliku: zákazník odpovídá za to, že třetí strana s přístupem přijme podmínky Skliku; zákazník plně odpovídá za obsah reklam; u Chytré kampaně a Maximalizace konverzí Seznam nezaručuje nepřekročení CPA/PNO a zákazník platí vše; Seznam a zákazník jsou nezávislí správci osobních údajů; platby jdou z kreditu v Seznam Peněžence (napoveda.sklik.cz/en/contractual-terms). Optimalizační služby Seznamu jsou jen pro přímé zákazníky (to je pravidlo pro nákup od Seznamu, nikoli zákaz správce).
- **Sklik Ověření / Certifikace:** Ověření chce místo v top 21 až 220 subjektů podle obratu klientů, ≥ 3 aktivní klienty a fakturační údaje účtu na IČO klienta; Certifikace top 20 (o-seznam.cz/reklama/certifikace). Pro nás nedosažitelné, **nesmíme používat označení „certifikovaný“ ani „ověřený partner Sklik“**.
- Neplatné kliky: Sklik je filtruje a vyřazuje ze statistik do 24 h, odhalené vrací kreditem (napoveda.sklik.cz/ochrana-proti-neplatnemu-klikani). Online dobití nejvýš 10 tis. Kč najednou, převod ≈ 2 pracovní dny.

**Google Ads (druhá fáze, nic z toho nemáme).**
- Manager account (MCC): z něj odešleme žádost o propojení podle ID klienta, klient ji potvrdí ve svém účtu; role Administrativní, Standard, Jen čtení, Billing (support.google.com/google-ads/answer/9978556). Billing je samostatná role, klient platí vlastním platebním profilem; Billing nežádáme.
- API: podle dokumentace z 2026-10-02 se úroveň přístupu váže na projekt v Google Cloud (developer tokeny se ruší od 2026-09-09, **nejisté, dokumentace je čerstvě změněná**). Explorer: 2 880 operací denně na produkčních účtech, bez plánovače klíčových slov, správy uživatelů a billingu. Basic: 15 000 operací denně, předpokladem je ověření značky projektu. Standard: ruční audit, ≈ 10 pracovních dnů, pro velké nástroje. Manager account už pro API není nutný, jen pro správu víc účtů (developers.google.com/google-ads/api/docs/api-policy/access-levels).
- Schválení Googlem a ověření značky zatím nikdo nezačal; zda Google API Terms dovolují autonomního agenta, jsem v plném znění nečetl.

**Kdo platí kredit:** vždy klient, na svůj účet a IČO (Sklik: dobít smí jen majitel; Google: platební profil klienta). Naše firma nikdy nedrží cizí kredit ani kartu. Kredit je zároveň přirozený strop škody při chybě AI.

**Co musí být ve smlouvě (B2B, jen podnikatelé):**
1. Rozsah: audit, založení, správa, měsíční report; co není: landing page, grafika, měření na webu klienta, SEO.
2. Měřitelné výstupy místo slibu výsledku (oddíl 5); výslovně žádný slib počtu poptávek, objednávek ani ROAS.
3. Účet je majetek klienta na jeho IČO, naše role Správce kampaní (Sklik) nebo Standard (Google), bez práva dobíjet a bez billingu; při ukončení odebrání přístupu.
4. Limity útraty: denní a měsíční písemně, změna jen klientem; bez Chytré kampaně a Maximalizace konverzí bez zadaného limitu CPA; klient hradí vše účtované platformou v mezích limitu; překročení limitu naší chybou hradíme do výše překročení.
5. Obsah reklam: klient dodá pravdivé údaje (ceny, slevy, „zdarma“), texty písemně schválí před spuštěním, vyloučené kategorie (zdraví, finance, hazard a další regulované); nespustíme text, který považujeme za rozporný se zákonem, i když klient trvá.
6. Neplatné kliky: platformy je filtrují a vracejí kredit, my zachycení všech nezaručujeme, dodáme podklady k reklamaci.
7. Reporting: týdenní krátký e-mail a měsíční report (zobrazení, kliky, útrata, konverze, změny, doporučení).
8. GDPR: zpracovatelská smlouva podle čl. 28, rozsah jen přístup k reklamním účtům; **žádné zákaznické seznamy ani retargetingové seznamy e-mailů**; poddodavatel jazykový model v USA (Anthropic), jen bez osobních údajů; Seznam a klient zůstávají nezávislými správci.
9. Odpovědnost omezená na poplatky za správu za poslední 3 měsíce, bez ušlého zisku a bez útraty za reklamu. Ve smlouvě i v nabídce se otevřeně uvede, že kampaně připravuje a spravuje AI (Claude) na odpovědnost MYPIXEL s.r.o., nikdy tvrzení „bez AI“.
10. Doba: měsíčně, výpověď 14 dní; kampaně a data zůstávají klientovi.

**Právní riziko ke schválení Ondřejem (jeho veto na právo):**
- **Společná odpovědnost za reklamu:** zpracovatel reklamy a zadavatel odpovídají společně a nerozdílně za soulad se zákonem (§ 6b zák. 40/1995), pokuty do 5 mil. Kč u právnické osoby (§ 8a). Reklamy píšeme my, takže riziko je naše, ne jen klientovo. Zmírnění: text jen z ověřených údajů klienta, vyloučené kategorie, písemné schválení, právo odmítnout.
- **Cizí peníze:** chyba AI může vyčerpat klientův kredit. Zmírnění: kredit dobíjí klient po malých částkách, denní limit, role bez dobíjení, denní kontrola útraty přes API, okamžité pozastavení.
- **GDPR a třetí země:** model běží v USA; v rozsahu služby žádné osobní údaje (neověřil jsem standardní smluvní doložky ani rámec EU–USA).
- **Klamavé označení:** žádný „certifikovaný partner“, žádné vymyšlené reference ani výsledky.
- **Podmínky platforem:** Sklik (třetí strana přijímá podmínky), Google API Terms (neověřeno v plném znění), podmínky portálů pro odpovědi (zda smějí odpovídat roboti, neověřeno).
- **Nevyžádaná sdělení:** jen odpovědi na poptávky, žádný studený e-mail (zákon 480/2004 § 7).
- **Pojištění odpovědnosti** za chybu ve službě: cenu jsem nezjišťoval.

## 3. Kanály a objem (měřeno 2026-10-02)

| Kanál | PPC poptávek měsíčně | Poznámka |
|---|---|---|
| ePoptávka, „Reklamní služby – internet“ (827 celkem) | ≈ 3 až 4 (4 za 3. až 29. 9., ≈ 10 za 90 dní) | kontakt zadavatele podle dřívějšího výzkumu až v placeném tarifu (od 2 990 Kč/3 měs.), znovu neověřeno |
| Poptavky.cz, „Marketing – online“ (391 celkem) | ≈ 3 (z 14 poptávek za 5. 8. až 29. 9. je 6 o reklamě) | **tytéž poptávky jako na ePoptávce** („bowling“ 21. 9., „optimalizace online reklamy“ 29. 9., „audit kampaně“ 11. 8.). Registrace zdarma, paušál 0 Kč do 4. 10. 2026, platí se až za realizaci; katalog „PPC a RTB reklamy“ je mrtvý (11 poptávek, poslední 23. 12. 2021) |
| Webtrh, „Poptávky obchodu a marketingu“ | ≈ 6 PPC nebo Meta za 29 dní z 28 poptávek | 3 jsou agentury hledající spolupracovníka, 1 je kopie z ePoptávky, pole rozpočtu u 4 z 6 „do 2 tisíc Kč“ (nespolehlivé); stránkování vrací stále první stranu |
| Shoptet Partneři, kategorie PPC (118 celkem) | 2 až 4 (10 za 21. 5. až 30. 9., 4 v září) | Google Ads, Meta, Merchant Center; polovina už „vyřízená“; odpověď přes formulář s reCAPTCHA |
| Seznam, hledání služby | 73 měsíčně za 16 dotazů | „reklama na seznamu“ 33, „ppc kampaně“ 14, „správa ppc“ 6, ostatní 0 až 2: žádný kanál |
| Bazoš, Služby | 0 poptávek, ≈ 10 inzerátů konkurentů | kanál pro prodávající |
| Firmy.cz, Služby | bez čísla | nabídka zdarma, až 25 služeb na provozovnu, zobrazí se na Seznamu; pasivní, neměřeno |

**Unikátních ≈ 8 až 12 měsíčně, z toho koncových klientů ≈ 5 až 8** (po odečtení agentur a kopií). Z ≈ 10 zadání, která jsem četl, výslovně Sklik zmínilo 1 (ePoptávka 21. 4. „Google Ads a Sklik“), ostatní Google Ads, Meta nebo obecně reklama. Malý vzorek.

**Souvislost s K1+K2:** je to stejná sběrná cesta (Webtrh, ePoptávka, Poptavky.cz, Shoptet Partneři). PPC přidá ≈ 15 až 20 % poptávek k ≈ 45 z K1, bez nového kanálu. Shoptet kategorie PPC míří na týž typ e-shopů jako K2, takže PPC se dá prodat jako doplněk paušálu K2 (věta v každé odpovědi na e-shop: „audit reklam zdarma“). Sdílené: obchodní podmínky, zpracovatelská smlouva, alias, tabulka reakcí. Nesdílené: technika cizího účtu a odpovědnost za cizí útratu.

## 4. Ekonomika

Předpoklady (ne měření): cena 2 500 Kč měsíčně + založení 2 000 Kč, odchod klientů 6 % měsíčně, náklady v hotovosti 0 Kč (kredit hradí klient; tokeny Clauda neznám).

Klientů na zisk 10 000 Kč měsíčně: při 1 490 Kč 7; 1 990 Kč 5; 2 990 Kč (paušál K2) 4; 4 990 Kč (spodek freelancerů) 2.

Kolik klientů v 6. a 12. měsíci (N = obsloužitelné poptávky měsíčně, w = podíl vyhraných; všechno odhad):

| N | w 2 % | w 4 % | w 8 % |
|---|---|---|---|
| 4 (pesimisticky) | 0,4 / 0,7 | 0,8 / 1,4 | 1,7 / 2,8 |
| 7 (střed) | 0,7 / 1,2 | **1,4 / 2,4** | 2,9 / 4,9 |
| 10 (optimisticky) | 1,0 / 1,7 | 2,1 / 3,5 | **4,1 / 7,0** |

Střed: ≈ 1,4 klienta (≈ 3 500 Kč měsíčně) v 6. měsíci a ≈ 2,4 (≈ 6 000 Kč) ve 12. 10 000 Kč dosáhne jen horní pravý roh. Pravděpodobnost ≥ 3 klientů do 6 měsíců při λ ≈ 1,2 (6 měsíců × 4 obsloužitelné poptávky × výhra ≈ 3,5 % + prodej z K2 ≈ 0,3) vychází ≈ 12 %.

**Čas Claude na klienta (odhad):** založení 2 až 3 h (audit, klíčová slova z `keywords.suggest`, vylučující slova, 3 sestavy po 3 až 4 reklamách, Odkazy a Popisky, UTM, 15bodový kontrolní seznam z `plan/postupy/sklik.md`); provoz ≈ 2 až 3 h měsíčně. Z toho ≈ 70 % automatické (čtení statistik, report dotazů, návrh vylučujících slov, report), ruční je komunikace, schvalování textů klientem, fakturace. 10 klientů ≈ 25 h měsíčně: kapacita není strop, strop je poptávka a cena. Ondřej: jen jednorázové autorizace a eskalace (telefony a schůzky s klienty proti zadání nepřijímáme).

**Nákladově:** test 0 Kč (Poptavky.cz), případně Webtrh Premium 399 až 465 Kč, který se stejně kupuje pro K1; Google Ads API Basic (ověření značky) cenu neznám.

## 5. Kritické body a co je řeší

| Bod | Řešení |
|---|---|
| **Nemáme výsledky** (2 zobrazení, 0 prokliků) | Slibujeme výstupy, ne výsledky: audit do 48 h (15 bodů z `plan/postupy/sklik.md`), kampaň do 3 pracovních dnů po přístupu, denní rozpočet nikdy nad limit, kontrola dotazů a vylučující slova do 7 dnů od spuštění, týdenní a měsíční report, odpověď do 1 pracovního dne. Otevřeně říkáme: „vlastní kampaň má 2 zobrazení za 7 dní, protože naše fráze mají 0 až 13 hledání měsíčně“. To je vysvětlení z měření hledanosti, nikoli důkaz kvality, a tak to prezentujeme. |
| **Důvěra** | Audit zdarma jen pro čtení (role Reporter statistik): klient nic neriskuje, my ukážeme kompetenci na jeho účtu. Pilot: první 2 klienti založení zdarma a první 2 měsíce správy za 1 490 Kč výměnou za souhlas s anonymizovanou případovou studií po 60 dnech. Reference jen skutečné, AI uvedená otevřeně. |
| **Cizí peníze** | Kredit klienta jako strop, role bez dobíjení, denní limit, denní kontrola útraty, žádná Chytrá kampaň ani Maximalizace konverzí bez limitu CPA, pozastavení jedním voláním. |
| **Platformy mají vlastní automatizaci** | Nekonkurujeme algoritmu. Prodáváme kontrolu nad ní: limity, vyloučení, kontrola dotazů a útraty, report česky. Sklik Chytrá kampaň a Shoptet Kampaně jsou levná alternativa, kterou musí klient odmítnout. |
| **Konkurence pod cenou** | Seznam Mini 1 500 Kč za 3 měsíce a nabídka za 499 Kč existují. Rozdíl, který můžeme nabídnout: e-shopy (Mini je nesmí), Sklik i Google Ads, odpověď do dne, týdenní report. Cena tím nad 2 000 až 3 000 Kč neporoste, proto strop zisku. |
| **Segment pod hranicí smyslu** | Rozpočet 3 až 20 tis. Kč je podle trhu pod hranicí, kde správa dává smysl; nespokojenost i při správné práci je riziko pro recenze. Proto dolní hranice rozpočtu u smluv ≥ 5 000 Kč měsíčně a otevřený text o očekávání. |

## 6. Nejmenší verze a test 72 hodin

Nic nestavět, žádná reklama, žádný web. Úkol pro Claude, ≈ 3 až 4 h:
1. Vybrat 5 až 6 aktuálních PPC poptávek (≤ 14 dní, koncový klient, Sklik nebo Google Ads): k 2026-10-02 jsou to 29. 9. „optimalizace online reklamy“ (architektonické studio, účet Google Ads), 29. 9. „on-line marketing pro začínající e-shop“, 21. 9. „správa reklamní kampaně na bowling centrum“, 1. až 2. 9. „nastavení reklamních účtů“ (výrobce potravin), Shoptet 30. 9. SPECTRUM.CZ (senior, spíš ne). Víc než ≈ 5 vhodných není, test je z podstaty slabě vybavený.
2. Každá odpověď na míru: 3 věty k jejich situaci, nabídka **auditu zdarma s přístupem jen pro čtení do 48 h**, cena správy (1 990 až 2 990 Kč měsíčně), AI uvedená otevřeně, žádný slib výsledku. Do každé odpovědi z K1/K2 na e-shop jedna věta o auditu.
3. Tabulka reakcí (portál, datum, reakce, stav).
4. Mezitím ověřit techniku cizího účtu na druhém vlastním Seznam účtu (nabídnout přístup, přihlásit se s `userId`, přečíst kampaň; 0 Kč).

**Kritérium úspěchu:** do 72 h ≥ 1 závazek (klient nabídne přístup do účtu nebo písemně přijme cenu), výhodně ≥ 2 věcné reakce z 5 až 6 odpovědí; 0 reakcí = PPC zůstane jen větou v odpovědích K2, nástroj se nestaví. Po 28 dnech: ≥ 1 klient za ≥ 1 490 Kč měsíčně → stavět multi-účtový nástroj; jinak zastavit. Náklad 0 Kč (Webtrh Premium se kupuje pro K1). Pravděpodobnost úspěchu ≈ 12 %.

## Co schvaluje Ondřej

1. **Právo (veto):** obchodní podmínky a zpracovatelskou smlouvu GDPR (rozšíření `plan/web-za-24-hodin.md`, znění připravím); společná odpovědnost za obsah reklam (§ 6b zákona 40/1995), limit odpovědnosti, žádné osobní údaje do jazykového modelu v USA.
2. **Výjimka z verdiktu** pro sondu (řádek „Výjimka schválená Ondřejem: sonda PPC jako odpovědi na poptávky, 0 Kč (datum)“ zapisuje on): `verdikt.py` dává NE/NE.
3. **Autorizace:** druhý Seznam účet pro správu cizích účtů (ověření telefonem), registrace na Poptavky.cz, ePoptávka a Webtrh, případně Webtrh Premium 399 až 465 Kč (finance, sdílené s K1), alias `ppc@mypixel.cz`.
4. **Zakázáno bez dalšího souhlasu:** placená reklama na nabídku, Google Ads API (ověření značky), cokoli co drží kredit nebo kartu klienta.
5. Jen informace, neschvaluje: ceny (audit zdarma, správa 1 990 až 2 990 Kč, pilot 1 490 Kč).

## Nejistoty a co jsem neověřil

- Počet poptávek vychází z prvních stránek výpisů 2026-10-02 a z ≈ 10 přečtených zadání; kopie mezi portály jsem počítal podle shodných názvů a dat. Webtrh vrací při stránkování stále první stranu.
- Výhra 2 až 8 %, odchod 6 %, cena 2 500 Kč a čas na klienta jsou předpoklady; pravděpodobnosti jsou úsudek.
- Ceník ePoptávky a provize Poptavky.cz (700/2 000/3 000 Kč) jsem znovu neověřil; ceny Poptavky.cz po 4. 10. 2026 neznám.
- Hodnoty `api.limits` Skliku, podpora Chytré kampaně v API a spravování cizího účtu naším nástrojem jsou neověřené. Google API: dokumentace se změnila v září 2026, plné API Terms jsem nečetl.
- Požadavky na nás podle Anthropic Usage Policy ani standardní smluvní doložky pro přenos dat do USA jsem nezkoumal. Pojištění odpovědnosti jsem nezjišťoval.
- Některé stránky jsem četl přes shrnutí nástroje, ceny konkurentů proto berte jako orientační (všechny bez DPH, pokud není uvedeno jinak).
- Zdroje: napoveda.sklik.cz (přístup k účtu, API Drak, podmínky, neplatné kliky, Chytrá kampaň, Maximalizace konverzí), seznam.cz/reklama (Podpora a cena), o-seznam.cz/reklama/certifikace, blog.seznam.cz (2025-06, 2026-02, 2026-05, 2026-01), developers.google.com/google-ads/api (access levels), support.google.com/google-ads, zakonyprolidi.cz (40/1995), ceníky a stránky konkurentů z tabulky (a martinkovalcik.cz/blog/sprava-ppc-kampani, marketingppc.cz/faq/kolik-stoji-google-ads), webtrh.cz/poptavky, poptavky.cz, poptavky.epoptavka.cz, partneri.shoptet.cz/poptavky/ppc, sluzby.bazos.cz, Shoptet Kampaně (vladimirprichystal.cz), mergado.cz.
