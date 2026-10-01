# Research poptávky: třetí produkt (2026-10-01, varianta b)

Stav: research hotový, nic nestaveno, nic nekoupeno, žádné placené ani zapisující API nevolány. Navazuje na `plan/research-2026-09-30.md`, `plan/research-2026-10-01.md`, `plan/prijimacky.md`; nenavrhuji svatební plánovač, rodinný rozpočet, pracovní listy 1.–5. třídy ani přijímačky.
Zadání: produkt s poptávkou teď nebo celoročně, obsluha automaticky (platba QR + Fio, e-mail Resend), test do ~1 000 Kč, žádné placené zahraniční služby, Ondřej jen schvaluje.

## 0. Doporučení

**Vítěz (podmíněně): příprava na zkoušku z češtiny A2 pro trvalý pobyt, nový formát od 11. 4. 2026.** Pracovní název „Zkouška A2: příprava s vysvětlením“. Kupuje a používá dospělý cizinec. Test: ukázkový test zdarma + balíček 3 testů za 190 Kč. Plná verze: 8 testů za 390 Kč jednorázově (oddíl 5).

Proč právě on:
1. **Jediný kandidát s tvrdými čísly poptávky:** 8 819 uchazečů a 7 602 úspěšných v roce 2023, přes 12 000 úspěšných v roce 2024 (neověřeno), zkouška stojí 3 200 Kč, v ČR žije 1 131 197 cizinců (k 31. 12. 2025).
2. **Celoroční, nesezónní:** zkoušky se konají průběžně, termíny se přidělují z fronty. Nový formát platí od 11. 4. 2026, starší materiály jsou zastaralé.
3. **Doložená ochota platit:** 199 Kč/měsíc (a2zkouska.cz), 1 900 Kč za 3 testy se zpětnou vazbou (ExamOnline, neověřeno), kurzy 5 400–8 100 Kč (ICJ).
4. **Doložená mezera:** podle AUČCJ většině uchazečů nepředchází žádná systematická příprava. Oficiální materiál jsou 2 modelové testy a nejslabší část zkoušky je psaní (úspěšnost 65,9 %).
5. Právní riziko nízké, klíče a body ověřitelné kódem, platby, doručení a metriky z Printopie/anoberu se použijí.

**Největší riziko: dosah a velikost trhu.** Google Trends ukazuje českou hledanost „zkouška a2“ skoro nulovou (0,01 vůči „pracovní listy“, −68 % za 5 let) a Seznam našeptávač pro A2 nevrací nic. Kupující tedy nejspíš hledají přes Google, v angličtině a ve Facebook skupinách, ne přes Sklik. Absolutní hledanost nezjištěna. Strop tržeb při 1–3 % z ~12 tisíc uchazečů ročně je ~47–140 tis. Kč/rok (odhad, podíl kupujících neměřen). Při 390 Kč a konverzi 2 % je na 20 tis. Kč/měsíc potřeba ~2 560 návštěv měsíčně.

**Záloha:** domácí únikovky k tisku (kandidát B). Lepší dosah (Seznam, brand printopia.cz, vrchol v prosinci), ale slabší důkaz poptávky po produktu.

**Poctivé shrnutí:** kde je poptávka velká (životopis 4,0, autoškola 2,0, smlouvy 0,3–0,5 vůči „pracovní listy“), je zdarma nebo zavedený konkurent. Kde konkurence chybí, je poptávka pod měřitelností. Žádný kandidát neslibuje víc než řádově desítky tisíc Kč ročně bez rozšíření. U A2 je rozšíření možné (další zkoušky pro cizince).

## 1. Metoda a zdroje

- **Google Trends CZ, 5 let** (do 2026-09-30, stáhnuto 2026-10-01), skripty `plan/zdroje-2026-10-01/trends.py`, `an.py`. Trends dává relativní hodnoty 0–100 jen uvnitř skupiny max. 5 dotazů. Index = hledanost / „pracovní listy“ (PL = 1,0, stejná jednotka jako `research-2026-10-01.md`). Skupiny bez PL jsem převedl přes kotvu „nájemní smlouva“ = 0,40 PL (skupina „pracovní listy, nájemní smlouva, smlouva o dílo, životopis, podnikatelský plán“: 5,1 vs 12,7). Sloupec „poslední rok“ = posledních 52 týdnů, trend = poslední rok vůči prvnímu roku.
- **Omezení Trends:** celá čísla, hodnoty pod ~0,01 PL jsou 0 (v tabulce „<0,01“ = pod měřitelností, ne nula). Absolutní počty hledání nemám (Sklik/Keyword Planner vyžaduje účet). Dotazy na informace v posledních letech klesají (AI odpovědi), proto trend −20 až −60 % u většiny „vzorů“.
- **Našeptávače:** Google (`client=firefox`, cs/en/uk/ru) a Seznam (`suggest.seznam.cz`, u frází četnost `_count`), 2026-10-01.
- **Web:** WebSearch a WebFetch 2026-10-01. U každého čísla je v oddíle 7 URL. „Neověřeno“ = číslo jen z výsledku vyhledávání, stránka se nenačetla.
- Surová data Trends jsou ve scratchpadu relace, ne v repu (zadání zakázalo měnit jiné soubory). Všechna čísla použitá v rozhodnutí jsou v tabulkách níže.

## 2. Přehled kandidátů (14)

Index = Trends vůči „pracovní listy“ = 1,0 (poslední rok / 5 let). Min/max = nejslabší/nejsilnější měsíc (1,0 = nesezónní).

| # | Kandidát | Hledanost (index) | Trend 5 let | Min/max měsíc | Konkurence a ceny (zdroj č.) | Právo | Verdikt |
|---|---|---|---|---|---|---|---|
| 1 | **Příprava A2 pro trvalý pobyt (cizinci)** | „zkouška a2“ 0,01 / 0,045; tvrdá data: 8 819 uchazečů 2023 | −68 % (nízké hodnoty) | nesezónní | a2zkouska.cz 199 Kč/měs; kurzy 5 400–8 100 Kč; zdarma NPI [1][4][5][6] | nízké | **TOP 1** |
| 2 | **Domácí únikovky/bojovky (PDF)** | „úniková hra“ 0,55 / 0,67; „únikovka“ 0,29; produktové dotazy <0,01 | −29 % / +49 % | 0,58 (vrchol prosinec) | 55–390 Kč, 6+ prodejců [10–14] | nízké | **TOP 2** |
| 3 | **Tvůrce životopisu (PDF)** | „životopis“ 4,0 / 4,7 | −38 % | 0,64 | 5+ nástrojů zdarma; ZivotopisOnline 199 Kč, 216 331 CV [15][16] | nízké | TOP 3, nedoporučeno |
| 4 | Autoškola, testy (a zbrojní průkaz) | „autoškola testy“ 2,0 / 1,9; „zbrojní průkaz test“ <0,01 | −12 % | 0,67 | eTesty od 2007: web 99 Kč, app 79–199 Kč; MDČR zdarma [17][18] | nízké | zamítnuto (zavedený konkurent) |
| 5 | Vzory smluv (nájem, auto, plná moc, DPP) | nájemní 0,45; kupní auto 0,30; plná moc 0,24; protokol 0,28; DPP 0,53 | −2 až −50 % | 0,56–0,70 | Sepsáno.cz 133 vzorů zdarma + generátor; vzorovedokumenty.cz 99 Kč/vzor [20][21] | střední | zamítnuto (zdarma + odpovědnost) |
| 6 | Hospodský / domácí kvíz | „hospodský kvíz“ 0,66; „… otázky“ <0,01 | +803 % | 0,48 | Hospodský kvíz s.r.o., stovky podniků týdně, kvíz na doma 249/349 Kč [19] | nízké | zamítnuto (držitel značky) |
| 7 | Dokumenty pro SVJ | „společenství vlastníků“ 0,53; konkrétní dokumenty <0,01 | +34 % | 0,66 | zdarma + 99 Kč/vzor (149 Kč za pozvánku neověřeno) [21] | střední | zamítnuto |
| 8 | Pronajímatel: vyúčtování služeb (Excel) | „vyúčtování služeb“ 0,035; „pronajímatel“ 0,18 | +106 % | vrchol duben–červen | zdarma Excel (mojenajmy.cz), placený Excel 200 Kč (neověřeno) [23] | střední | zamítnuto |
| 9 | Rodokmen PDF na míru | „rodokmen“ 0,82; „rodokmen online“ 0,005; „šablona/vzor“ ≈ 0 | −19 % | 0,58 | šablony zdarma, obrazy na míru 999–1 899 Kč (research 10-01) | nízké | zamítnuto (hledá se historie rodů, ne vlastní strom) |
| 10 | Dědictví / pozůstalost (průvodce) | „dědictví“ 1,64; „dědické řízení“ 0,19 | +11 % | 0,66 | zdarma průvodci, Dědický plán 249 Kč [22] | **vysoké** | zamítnuto |
| 11 | Paušální daň / OSVČ kalkulačka | „paušální daň“ 1,04 | +37 % | **0,18** (leden 46, červenec 8) | kalkulačky zdarma (předpoklad, neověřeno) | střední | zamítnuto (sezóna prosinec–leden) |
| 12 | Plánovače událostí, jídelníček | rekonstrukce 0,003; stěhování 0,003; taška do porodnice 0,010; týdenní jídelníček <0,01 (výsledky jsou menu restaurací) | −68 % | – | – | zdraví | zamítnuto (pod měřitelností) |
| 13 | Matematika 6.–9. tř. / maturita | „slovní úlohy“ 0,52; „rovnice příklady“ 0,26; „maturita z matematiky“ 0,11 | −36 až −57 % | **0,01–0,02** | zdarma, přesycené | nízké | zamítnuto (sezónní, klesá) |
| 14 | Domácí vzdělávání, zápis do 1. třídy, daň z akcií, rybářské zkoušky | všechny <0,04 | – | – | – | – | zamítnuto (pod měřitelností) |

## 3. Důvody vyřazení (pravidla)

| Pravidlo | Kdo odpadl |
|---|---|
| K1 Sezónnost: min/max < 0,2 nebo vrchol mimo „teď“ (pravidlo CLAUDE.md) | 11, 13 |
| K2 Zdarma kompletní řešení nebo zavedený konkurent s cenou ≤ 199 Kč a tisíci uživatelů | 3 (nedoporučeno), 4, 5, 6, 7, 8, 10 |
| K3 Poptávka po produktu pod měřitelností (<0,01 PL) a bez jiného tvrdého čísla | 9, 12, 14 |
| K4 Právní riziko (právní informace, zdraví): „minimální“ je podmínka zadání | 5, 7, 10, 12 |
| K5 Už hotové nebo zamítnuté | svatební plánovač, rozpočet, pracovní listy, přijímačky |

Prošli: **1 (A2)** a **2 (únikovky)**. Kandidát 3 (životopis) má největší poptávku z celého přehledu a prokázaný placený model, proto je jako třetí zpracován, ale neprošel K2.

## 4. Top 3 podle šablony

### 4A. Příprava na zkoušku A2 z češtiny pro trvalý pobyt (cizinci)

**1. Poptávka**

| Údaj | Hodnota | Zdroj |
|---|---|---|
| Uchazeči 2023 | 8 819, uspělo 7 602 (86,2 %) | [1] |
| Úspěšní 2024 | přes 12 000 (+58 % proti 2023), **neověřeno** (stránka MŠMT vrací 404) | [2] |
| Cena zkoušky | 3 200 Kč (od 01/2024), opakování = další 3 200 Kč | [1][4] |
| Nový formát | od 11. 4. 2026; čtení 25 b, psaní 20 b, poslech 25 b (min. 42 z 70), mluvení 40 b (min. 24) | [3][6] |
| Cizinci v ČR | 1 131 197 (31. 12. 2025, +37 108); trvalý pobyt 394 268; Ukrajina 612 953, Slovensko 125 280, Vietnam 69 685, Rusko 37 524 | [9] |
| Fronta | online registrace, termín přiděluje škola z fronty [4]; čekání ≥ 6 měsíců jen z výsledku vyhledávání (neověřeno) | [4] |
| Trends CZ | „zkouška a2“ 0,01 (5 let 0,045), „czech a2 exam“, „zkouška a2 trvalý pobyt“ <0,01 | Trends |
| Google našeptávač | cs: „zkouška a2 trvalý pobyt“, „… test pdf“, „… test online“, „… psaní“, „… mluvení“; en: „czech a2 exam preparation / preparation book / preparation pdf / topics / questions / registration“; uk, ru: nic | Google |
| Seznam našeptávač | pro „zkouška a2 trvalý pobyt“, „příprava“, „nový formát“ prázdný | Seznam |
| Zájem o oficiální web | „Zobrazení stránky: 432 276“ (počítadlo cestina-pro-cizince.cz) | [4] |

- Sezónnost: nesezónní. Teď (10/2026) je zájem o materiály k novému formátu, který platí od dubna.
- Kdo už prodává: oddíl 2. První tržba: ukázka a 3 testy za 1–3 dny práce, první prodej odhaduji na 1–3 týdny po spuštění reklamy (odhad).

**1b. Cílová skupina (z dat)**
- **Hledá:** dospělý cizinec ze třetí země před zkouškou, někdy partner nebo zaměstnavatel (nezjištěno). Kanály: Google (cs, en), Facebook skupiny (oficiální stránka NPI má 37 000 sledujících), YouTube [1].
- **Používá:** totéž. **Platí:** totéž, výjimečně zaměstnavatel nebo agentura (nezjištěno, změřit dotazem ve formuláři).
- **Segmenty (2023):** úspěšní podle státu: Ukrajina 4 943 (65 %), Rusko 764 (10 %), Vietnam 377 (5 %). Úspěšnost: Kazachstán 98 %, Rusko a Bělorusko 97 %, Ukrajina a Srbsko 90 %, **Indie 52 %, Vietnam 47 %, Mongolsko 30 %, Nepál 29 %**. Úspěšnost podle dovedností: čtení 82,8 %, poslech 86,9 %, mluvení 77,2 %, **psaní 65,9 %** [1]. Nejvyšší ochotu platit mají ti, kdo neuspěli (opakování 3 200 Kč), nejvíc pomůže psaní.
- **Omezení:** jen dospělí (žádný GDPR problém s nezletilými), spotřebitelská smlouva a VOP v češtině + angličtině, platba v Kč převodem/QR (kolik cizinců má český účet, nezjištěno).

**2. Konkurence a proč koupí od nás**

| Konkurent | Cena | Co dává | Zdroj |
|---|---|---|---|
| NPI / cestina-pro-cizince.cz | zdarma | učební materiál, 2 modelové testy (48 stran) platné od 04/2026, test nanečisto online, videa; web cs/en/uk | [3][4] |
| a2zkouska.cz | 0 / 199 Kč/měs / 499 Kč/3 měs | čtení, poslech, psaní jen v placené verzi; zdarma 1 cvičení denně | [5] |
| ExamOnline | 1 900 Kč | 3 testy s audiem a zpětnou vazbou učitele (neověřeno) | [7] |
| ICJ kurz | 5 400 Kč/40 h (cs), 8 100 Kč/60 h (en) | kurz v malé skupině, nový formát | [6] |
| Language Hub „Ready for A2“ | nezjištěno | příručka | [7] |

- **Proč od nás:** (1) 8 modelových testů nového formátu místo 2 oficiálních; (2) klíč s vysvětlením v ukrajinštině, angličtině, ruštině (oficiální web má rozhraní cs/en/uk, modelový test jsem četl jen česky a vysvětlení úloh v dalších jazycích jsem nenašel; neověřeno u všech oficiálních materiálů); (3) psaní: modelové odpovědi a bodovací mřížka podle oficiálních kritérií, nejslabší dovednost; (4) tisk (PDF) i web s automatickým vyhodnocením čtení a poslechu; (5) jednorázových 390 Kč místo 199 Kč měsíčně; (6) audio ze zdarma hlasu (Piper cs_CZ jirka, CC0; kasandra, CC BY 4.0) [8].
- **Kde nejsme lepší:** oficiální nahrávky a autorita NPI, živá zpětná vazba (ExamOnline), kurz s lektorem pro mluvení. Mluvení nelze automaticky hodnotit (nabídneme otázky, vzorové odpovědi a sebehodnocení). Syntetické audio se liší od zkušebních nahrávek a řekneme to na webu.

**3. Ekonomika**
- Cena: ukázka 0 Kč, balíček 3 testy 190 Kč, plná verze 8 testů 390 Kč (neplátce DPH, tržba = cena). Náklady výroby 0 Kč (Claude), audio zdarma, Fio a Resend z anoberu. Nová doména ~200 Kč až po úspěšném testu (viz rozpočet v oddíle 4).
- Cena za zákazníka (CAC = CPC / konverze, CPC a konverze jsou **odhady**, neměřeno):

| CPC \ konverze | 1 % | 2 % | 4 % |
|---|---|---|---|
| 3 Kč | 300 Kč | 150 Kč | 75 Kč |
| 5 Kč | 500 Kč | 250 Kč | 125 Kč |
| 8 Kč | 800 Kč | 400 Kč | 200 Kč |

  Plná verze 390 Kč: reklama se vyplatí od konverze ~1,3 % při CPC 5 Kč. U balíčku za 190 Kč je to ztráta, pokud není konverze ≥ 2,6 % (tedy balíček slouží jako test a vstup, ne jako zdroj zisku).
- Strop (odhad): 12 000 uchazečů ročně × 1–3 % kupujících × 390 Kč = 47–140 tis. Kč/rok.

**4. Test poptávky před stavbou**
- **Krok 0 (0 Kč, před čímkoli):** zjistit absolutní hledanost 12 frází (A2 test, příprava, psaní, mluvení, nový formát, v cs a en) ve Sklik „Návrh klíčových slov“ (přístup už máme, token v env projektu printopia) nebo v Google Keyword Planner (potřebuje přihlášení Ondřeje). Když Sklik ukáže < 50 hledání/měsíc pro hlavní fráze, Sklik pro A2 nepoužít.
- **Co se staví před testem (max. pár hodin):** 1 ukázkový test (čtení + psaní + klíč, uk/en/ru) a objednávka na 3 testy. Zbytek až po splnění kritéria.
- **Rozpočet:** volných firemních peněz je ~350–400 Kč (1 000 − 200 doména − 400 schválený test Printopie, případně − dalších 50 Kč, pokud kredit 50 Kč do těch 400 Kč nepatří; podle CLAUDE.md, bez tržeb). Navrhuji: web na subdoméně existující domény (0 Kč), Sklik ≤ 300 Kč (jen pokud krok 0 vyjde), volitelně Google Ads ≤ 500 Kč soukromě od Ondřeje mimo účetnictví (dohoda 2026-09-30).
- **Doba:** 14 dní od spuštění reklamy, plus SEO stránky (uk/en/ru/cs) po celou dobu.
- **Statistika (předem):** pravděpodobnost aspoň 1 objednávky při n návštěvách:

| Návštěv | konverze 1 % | 2 % | 4 % |
|---|---|---|---|
| 60 | 45 % | 70 % | 91 % |
| 120 | 70 % | 91 % | 99 % |
| 190 | 85 % | 98 % | 100 % |

  190 návštěv stojí při CPC 3/5/8 Kč 570/950/1 520 Kč. Rozpočet výše (300 Kč firma + 500 Kč soukromě) stačí na ~100–160 návštěv, výsledek při méně než 190 návštěvách je jen orientační.
- **Kritérium:**
  - **Pokračovat (stavět 8 testů, koupit doménu):** ≥ 1 zaplacená objednávka z placeného provozu do 14 dní, nebo ≥ 3 zaplacené celkem včetně organiky do 28 dní.
  - **Zastavit reklamu:** 0 objednávek po ≥ 190 návštěvách (s 95 % jistotou konverze < 1,6 %). SEO a obsah zůstávají (nic nestojí).
  - **Prodloužit o 14 dní jen SEO a upravit nabídku:** 0 objednávek, ale ≥ 25 % návštěvníků dokončí ukázku (produkt zaujal, brzdí cena nebo důvěra).

**6. Rizika (právo, finance)**
- **Autorská práva:** oficiální testy NPI nepřebírat, psát vlastní a formát jen popisovat. Název „NPI“ a „zkouška z češtiny pro trvalý pobyt“ jen popisně, žádné logo ani tvrzení o spolupráci, na webu „není oficiální materiál“.
- **Chyby v češtině a překladech (uk, ru):** vysvětlení psát krátká a šablonovitá, zpětné hlášení chyby = oprava + vrácení peněz do 14 dní. Ověřitelné kódem: klíč odpovídá textu (každá úloha má v datech doslovný důkaz, který musí v textu být), součty bodů 25/20/25/40, délka vět a slovní zásoba proti frekvenčnímu seznamu (zdroj seznamu nezjištěn, zvolit při stavbě).
- **Žádný slib výsledku** („zaručíme úspěch“) ani statistiky úspěšnosti našich zákazníků.
- **Změna pravidel:** zákonodárce může změnit požadovanou úroveň nebo formu zkoušky (nezjištěno, hrozí jen u vyšší úrovně). Produkt by pak zastaral.
- **Finance:** test ≤ 350 Kč firmy. Při neúspěchu ztráta stejná a pár hodin práce.
- **Spotřebitelské právo:** VOP a odstoupení do 14 dní v cs + en (+ uk), jako u anoberu. Text schvaluje Ondřej.

**7. Metriky a vyhodnocení**
- Trychtýř anonymně (Beacon → /api/e → /api/stats z Printopie): zobrazení → začátek ukázky → dokončení ukázky → klik na koupi → začátek formuláře → objednávka → zaplaceno → stažení. Dělení podle **jazyka stránky (cs/en/uk/ru)**, zdroje (sklik/google/organické), zařízení.
- Proč ne: anketa „Co vás drží od koupě?“ (cena, nedůvěra v nezávislý materiál, stačí oficiální, jiný jazyk, jiné) + role kupujícího („já / zaměstnavatel / škola“) a zda už zkoušku skládal.
- Reklama: hledané dotazy a CPC ze Skliku, z Google Ads (Ondřej exportuje) jen pokud je použit.
- Automatické závěry (`/api/stats` → `findings`, od 30 návštěv): kde odpadají, který jazyk konvertuje, který dotaz přivádí kupující.
- Po testu zapsat `plan/a2-vyhodnoceni.md` (čísla, pokračovat/zastavit, poučení). Před spuštěním musí projít `python3 plan/kontrola-spusteni.py plan/a2.md <aplikace>` a existovat `plan/design-a2.md` a `plan/postupy/` pro každý kanál (pravidla CLAUDE.md).

### 4B. Domácí únikovky a bojovky k tisku (PDF)

**1. Poptávka**
- Trends: „úniková hra“ 0,55 (5 let 0,67), −29 %; **prosinec 70, listopad 63** vůči nejslabším měsícům 41–43 (+50–70 %), jinak 41–52 po celý rok. „Únikovka“ 0,29, +49 %. Našeptávač Seznamu ale u „únikovka“ nabízí hlavně města (praha 29, ostrava 33, brno 37, plzeň): hledá se návštěva provozovny. Produktové dotazy („domácí únikovka“, „únikovka pdf“, „únikovka k tisku“, „únikovka pro děti“) jsou pod měřitelností (<0,01). Seznam nabízí „únikovka k vytisknutí zdarma“, „úniková hra pro děti pdf“, „bojovka pro děti zdarma“ bez četnosti. „Bojovka“ 0,10 (duben a říjen, prosinec a leden slabé).
- Prodejci (ověřeno 2026-10-01): Hranice reality přes Slevomat 179 Kč (z 249 Kč, platnost do 28. 2. 2027) [10], Mozkonaut 9 her 249–359 Kč [11], Unikoffka 11 položek, PDF 270–390 Kč, balíčky 550 Kč [12], Táborovky 39 položek 70–130 Kč [13], Elis v papíru 55–80 Kč [14]. Indikátor prodeje: vlajková hra za 390 Kč má **2 recenze** (24. 3. a 21. 6. 2026) [12].
- Sezónnost: teď vrchol. Hra musí být živá do ~15. 11., aby chytila advent.

**1b. Cílová skupina:** hledá a platí rodič (hra pro děti 7–12) nebo dospělý (rodinná zábava, narozeniny, vánoční večer, učitel nebo vedoucí oddílu). Používá dítě/rodina. Prodejní sdělení jen dospělým (zákaz přímé výzvy dětem, UCPD příloha I bod 28). Podíly rodič/dospělý/vedoucí nezjištěny, změřit rolí ve formuláři.

**2. Konkurence:** 6+ drobných prodejců s cenou 55–390 Kč a pěknou ilustrací, část her zdarma. Naše výhody: každá šifra ověřená kódem (jednoznačné řešení, žádná slepá cesta), jasný čas a počet hráčů, tisk bez střihání. Nevýhody: bez ilustrátora, bez recenzí, bez značky.

**3. Ekonomika:** 249 Kč za hru (spodní hranice pásma 249–359 Kč u Mozkonaut a 270–390 Kč u Unikoffky), balíček 3 her 599 Kč. Náklady 0 Kč (fotky Unsplash, vlastní sazba, kód). CAC stejná tabulka jako u 4A, pro 249 Kč je hranice ztráty při CPC 5 Kč konverze ~2 %. Strop nezjištěn (produktová hledanost pod měřitelností). Odhad první tržby 1–2 týdny.

**4. Test:** krok 0 stejně (Sklik „Návrh klíčových slov“: „únikovka k vytisknutí“, „úniková hra pdf“, „… pro děti na doma“). Rozpočet Sklik ≤ 300 Kč na printopia.cz (brand tisknutelných materiálů, rodiče). Kritérium: pokračovat při ≥ 1 zaplacené objednávce do 14 dní a ≤ 150 návštěvách, zastavit při 0 po ≥ 190 návštěvách.

**6. Rizika:** vzhled proti ilustrovaným konkurentům (design průzkum povinný), neměřená velikost trhu, sezónní vrchol (po 20. 12. úbytek), licence fotek (Unsplash, uvést autora), reklama jen na dospělé.

**7. Metriky:** stejný trychtýř, navíc „hra dokončena“ (zpětná vazba e-mailem), role kupujícího, věk hráčů.

### 4C. Tvůrce životopisu (PDF za jednorázový poplatek)

**1. Poptávka:** „životopis“ 4,0 PL (5 let 4,7), −38 %, nejslabší měsíc 0,64 vůči nejsilnějšímu (leden 73, červenec 46). Seznam: „životopis“ 919, „životopis šablona“ 357. Největší poptávka z celého přehledu.
**1b.** Hledá, používá i platí uchazeč o práci (dospělý, často 18–25). Platba převodem u impulzního nákupu 99–199 Kč snižuje konverzi.
**2. Konkurence:** zdarma „bez limitů“ ŽivotopisZdarma.cz, cvzdarma.cz, CVčko.eu, Jobs.cz, Životopisy.cz [16]; placený ŽivotopisOnline.cz 199 Kč za PDF a **216 331 vytvořených CV**, 16 vzorů [15]; Cvapp.cz 7denní zkouška 75 Kč, pak 299 Kč [16]. Zavedený placený model existuje, proto je čtvrtý nástroj bez přednosti marginální.
**3. Ekonomika:** při ceně 199 Kč a CPC 3–6 Kč (odhad) vychází CAC 150–600 Kč při konverzi 1–2 %, tedy ztráta, pokud konverze není ≥ 3 % a CPC ≤ 5 Kč. SEO boj proti ≥ 5 zavedeným nástrojům trvá měsíce.
**4. Test:** nedoporučuji. Kdyby: Sklik 300 Kč na „životopis šablona word“, kritérium ≥ 1 objednávka ze 100 návštěv.
**6. Rizika:** nízké právní (data zpracovat jen v prohlížeči), finanční (ztráta reklamy), trend −38 % kvůli AI nástrojům.
**7. Metriky:** standardní trychtýř, navíc „kolik lidí dokončí editor“ (u produktu s editorem klíčové).

## 5. Doporučení: vítěz a první specifikace

**Vítěz: 4A, příprava na zkoušku A2 pro trvalý pobyt.** Pořadí: A2 > únikovky > životopis. Rozhoduje to, že A2 je jediný celoroční kandidát s tvrdým číslem poptávky, doloženou ochotou platit a doloženou mezerou. Únikovky mají lepší dosah, ale poptávku po produktu neumím změřit.

**Co přesně vyrobit (v1)**
- **Zdarma (vstup, sběr e-mailů s souhlasem):** 1 kompletní ukázkový test nového formátu: čtení 5 úloh (25 b), psaní 2 úlohy (3 odpovědi do formuláře + e-mail podle obrázků, 20 b), poslech 5 úloh s audiem (25 b), mluvení 4 úlohy (40 b), klíč a bodování podle oficiálních minim (42 z 70, 24 ze 40) [3]. Vysvětlení klíče uk/en/ru.
- **Balíček 3 testy, 190 Kč (test poptávky):** 3 kompletní testy stejné struktury, klíč, vysvětlení uk/en/ru, PDF k tisku + web s automatickým vyhodnocením čtení a poslechu.
- **Plná verze, 390 Kč jednorázově (po splnění kritéria):** 8 testů, 40 vzorových odpovědí k psaní s mřížkou, 60 otázek k mluvení se vzory, slovník ~600 slov podle 12 témat (PDF kartičky), plán na 4 týdny. Přístup 12 měsíců, doručení e-mailem po zaplacení.
- Texty vlastní, ne z NPI. Obrázky pro psaní a mluvení: Unsplash nebo piktogramy z kódu. Audio: Piper cs_CZ (CC0 nebo CC BY 4.0, uvést autora u kasandry) [8].
- Správnost: strukturovaná data úloh (JSON) → generátor PDF/webu → kontrola v kódu (klíč, důkaz v textu, body, délka vět, slovní zásoba), stejně jako u Printopie.

**Kde prodávat:** vlastní web, QR platba a Fio párování, Resend (vše z anoberu/Printopie). Marketing: SEO stránky v cs/en/uk/ru („zkouška A2 psaní e-mail vzor“, „A2 mluvení otázky“, „A2 nový formát 2026: co se změnilo“, „kolik bodů potřebuji“), IndexNow, Sklik jen po kroku 0, Google Ads volitelně soukromě. Žádné příspěvky ani skupiny.

**Jaký web:** Next 16 podle `printopia/` (Beacon, `/api/stats`, objednávka, QR, e-mail), přepínač jazyků cs/en/uk (ru později), na subdoméně existující domény (nová doména ~200 Kč až po testu). Před spuštěním: `plan/design-a2.md` (3–5 konkurenčních stránek, texty), `plan/postupy/` pro Sklik a SEO, screenshoty 1500/1280/390/360 px, korektura češtiny a překladů, úvod bez provozovatele (patří do patičky), povinné prvky: skutečná fotka, náhled produktu, cena se srovnáním (199 Kč/měs, kurzy 5 400 Kč, zkouška 3 200 Kč), záruka 14 dní, FAQ, výrazné CTA.

**Role Ondřeje (jen autorizace a schválení)**
1. Schválit rozpočet testu ≤ 350 Kč z firmy (Sklik) a případně soukromý Google Ads ≤ 500 Kč.
2. Pro krok 0 jen případně přihlásit Google Keyword Planner (Sklik už je autorizovaný).
3. Schválit text VOP/GDPR v cs + en (+ uk) a riziko z oddílu 6.
Nic dalšího.

## 6. Co nezjištěno a jak změřit

| Nezjištěno | Jak změřit |
|---|---|
| Absolutní hledanost A2, únikovek, životopisu (Google a Seznam) | Sklik „Návrh klíčových slov“, Google Keyword Planner, 0 Kč, autorizace Ondřejem |
| Skutečný počet uchazečů 2024 a 2025 (>12 000?) | primární zdroj MŠMT/NPI nebo dotaz na NPI (stránka MŠMT vrací 404) |
| Doba čekání ve frontě na zkoušku | oficiální registrace (registrace.cestina-pro-cizince.cz), nebo anketa ve formuláři |
| Konverze a CPC | test oddílu 4, do té doby jen odhad |
| Podíl cizinců s českým účtem (QR) | anketa při objednávce, počet opuštěných formulářů |
| Prodeje konkurentů (a2zkouska.cz, ExamOnline, únikovky) | nelze zjistit, jen nepřímo (recenze) |
| Kvalita syntetického českého audia pro A2 a licence enginu Piper (hlasy jsou CC0/CC BY, engine ověřit) | zkušební nahrávka před stavbou, kontrola licence |
| Zdroj frekvenčního seznamu pro kontrolu slovní zásoby A2 | zvolit a ověřit při stavbě (licence) |
| Kolik kupuje zaměstnavatel nebo agentura | role ve formuláři |

## 7. Zdroje (přístup 2026-10-01, pokud není uvedeno jinak)

1. AUČCJ, Zkouška z češtiny pro trvalý pobyt: aktuální podoba a možnosti přípravy: https://www.auccj.cz/zkouska-z-cestiny-pro-trvaly-pobyt-aktualni-podoba-a-moznosti-pripravy-uchazecu/ (data 2023)
2. MŠMT, Rostoucí zájem o zkoušku z češtiny pro trvalý pobyt: https://msmt.gov.cz/zajem-o-zkousku-z-cestiny-pro-trvaly-pobyt-roste-stat-jiz (vrací 404, číslo „>12 000 úspěšných v roce 2024“ jen ze shrnutí vyhledávače, neověřeno)
3. NPI, Modelový test, platný od 04/2026 (48 stran, stažen a přečten): https://cestina-pro-cizince.cz/trvaly-pobyt/wp-content/uploads/2026/01/A2_Modelovy_test_1.pdf
4. Oficiální web zkoušky (cena 3 200 Kč, verze cs/en/uk, zdarma materiály, počítadlo 432 276): https://cestina-pro-cizince.cz/trvaly-pobyt/ ; registrace: https://registrace.cestina-pro-cizince.cz/
5. a2zkouska.cz (199 Kč/měs, 499 Kč/3 měs): https://a2zkouska.cz/en
6. ICJ, příprava na A2 (5 400 Kč/40 h, 8 100 Kč/60 h): https://icj.cz/en/preparation-for-the-a2-exam-for-permanent-residence-new-format-2026/
7. ExamOnline 1 900 Kč (https://examonline.cz/en/courses/cestina-trvaly-pobyt/, 404, z výsledku vyhledávání), Language Hub: https://store.language-hub.org/en/home/137-305-crfea2-ready-for-a2-czech-permanent-residence-exam.html (503, cena nezjištěna), kurz 4 250 Kč/20 lekcí (studyfun.cz, z vyhledávání, neověřeno)
8. Piper hlasy cs_CZ (jirka CC0, kasandra CC BY 4.0): https://huggingface.co/rhasspy/piper-voices/tree/main/cs/cs_CZ
9. ČSÚ, Počet cizinců (31. 12. 2025, aktualizace 2026-06-30): https://csu.gov.cz/pocet-cizincu-demograficke-udalosti
10. Slevomat, domácí únikovka v PDF (Hranice reality): https://www.slevomat.cz/akce/2399294-domaci-unikovka-v-pdf-tajemstvi-michelinske-restaurace
11. Mozkonaut: https://www.mozkonaut.cz/hry-pro-deti-k-vytisknuti
12. Unikoffka: https://www.unikovkanadoma.cz/unikove-hry/ ; vlajková hra (390 Kč, 2 recenze): https://www.unikovkanadoma.cz/unikova-hra-tajemstvi-ztraceneho-dortu--pdf-k-vytisteni/
13. Táborovky: https://www.taborovky.cz/unikovky/
14. Elis v papíru: https://www.elisvpapiru.cz/unikovky
15. ŽivotopisOnline.cz (199 Kč, 216 331 CV): https://www.zivotopisonline.cz/
16. Zdarma nástroje a Cvapp.cz (z výsledků vyhledávání, nenačteno): https://zivotopiszdarma.cz/ , https://www.cvzdarma.cz/ , https://cvcko.eu/ , https://www.jobs.cz/zivotopis/ , https://cvapp.cz/cv-sablony
17. eTesty autoškola (99 Kč, od 2007): https://www.etesty.cz/etesty_autoskola.php
18. eTesty v App Store (79/199 Kč, 4,7 z 2,7 tis. hodnocení, cs/en/ru/uk): https://apps.apple.com/cz/app/auto%C5%A1kola-testy-2026-etesty/id1401498212?l=cs ; oficiální testy MDČR zdarma a zbrojní průkaz (837 otázek od 1. 1. 2026, eTesty 199 Kč/30 dní) jen z výsledků vyhledávání, nenačteno: https://zbranekvalitne.cz/zbrojni-prukaz/testove-otazky?verze=20260101
19. Hospodský kvíz s.r.o. (IČO 03980138, Brno), 249/349 Kč, stovky podniků: https://www.hospodskykviz.cz/kviz-na-doma , https://www.hospodskykviz.cz/jdeme-poprve/
20. Sepsáno.cz, 133 vzorů zdarma + generátor: https://sepsano.cz/
21. vzorovedokumenty.cz, 99 Kč/vzor, 500 vzorů, >10 000 stažení: https://www.vzorovedokumenty.cz/33/zapis-ze-schuze-shromazdeni-vlastniku-jednotek-uniqueidgOkE4NvrWuPMs6LesOEd4DjVEOBggxt-i1eMHGUagh0/ ; placený balíček nájemní smlouvy: https://muj-pravnik.cz/najemni-smlouva-na-dobu-urcitou/
22. Dědický plán 249 Kč (z vyhledávání): https://eshop.cimpel.cz/produkt/dedicky-plan/
23. Excel vyúčtování služeb zdarma a placený za 200 Kč (z vyhledávání, nenačteno): https://mojenajmy.cz/cs/vzory/vyuctovani-sluzeb , https://www.vzorysablon.cz/nemovitosti/vyuctovani-sluzeb-najemnikovi/
