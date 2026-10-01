# Sklik obsahová síť: postupy, rizika a odhad pro Printopii

Zpracováno 2026-10-01, jen výzkum (nic nezaloženo; z API jen čtecí volání a `campaigns.check`). Platí pro každou obsahovou kampaň v Skliku: před založením projít **Kontrolní seznam**.

**Cílová skupina:** hledá a používá deváťák, **platí rodič**. V obsahové síti nikdo nehledá, reklama oslovuje rodiče při čtení webu, takže mluví k rodiči („Pro rodiče deváťáků“) a nesmí vyzývat dítě ke koupi ani k přemlouvání rodičů [48, 51]. Podíl rodičů mezi prokliky neznáme, změří test.

**Závěr (doporučení): NE za 82 Kč.** Za 82 Kč vyjde zhruba 20 až 40 prokliků (odhad), tedy 0,04 až 0,4 objednávky, a z toho se nedá nic vyhodnotit (rozhodnutí vyžaduje asi 190 návštěv, viz `plan/postupy/sklik.md`). Obsahová síť má smysl jen jako sonda s rozpočtem aspoň 400 Kč a až po rozhodnutí o rozpočtu firmy. Sonda: jedna sestava se záměrem „Rodiče dítěte školáka“, kombinovaná reklama a 3 bannery, max. CPC 3 Kč, 30 Kč denně.

## Zdroje
Navštíveny a ověřeny 2026-10-01, pokud není uvedeno jinak. Čísla označená ODHAD jsou naše výpočty.

API Drak v5 (JSON):
1. Úvod, endpoint `https://api.sklik.cz/drak/json/v5/`, binární data v JSON jako base64: https://api.sklik.cz/drak/
2. `campaigns.create`: https://api.sklik.cz/drak/campaigns.create.html
3. `groups.create`: https://api.sklik.cz/drak/groups.create.html
4. `banners.create`: https://api.sklik.cz/drak/banners.create.html
5. `ads.create` (adType `combined`): https://api.sklik.cz/drak/ads.create.html
6. `images.constraints.list`: https://api.sklik.cz/drak/images.constraints.list.html
7. Zájmy: https://api.sklik.cz/drak/interests.listCategories.html , https://api.sklik.cz/drak/interests.create.html
8. Záměry (v rozhraní „Zájmy o koupi“): https://api.sklik.cz/drak/intends.getCategoryList.html , https://api.sklik.cz/drak/intends.create.html
9. Témata: https://api.sklik.cz/drak/themes.listCategories.html , https://api.sklik.cz/drak/themes.create.html
10. Umístění (v API `patterns`): https://api.sklik.cz/drak/patterns.check.html
11. `keywords.create`: https://api.sklik.cz/drak/keywords.create.html
12. Retargeting: https://api.sklik.cz/drak/retargeting.lists.create.html , https://api.sklik.cz/drak/retargeting.group.lists.add.html
13. `campaigns.update` (excludedUrls, negativeKeywords): https://api.sklik.cz/drak/campaigns.update.html
14. API Fénix (REST, OpenAPI v1.30.0): https://api.sklik.cz/v1/openapi.json
15. Vlastní čtecí volání API 2026-10-01 (token z scratchpadu): `campaigns.listCampaignsTypes`, `campaigns.check` (jen kontrola, nic se nevytvořilo), `images.constraints.list`, `interests.listCategories`, `intends.getCategoryList`, `themes.listCategories`.

Nápověda Skliku:
16. Obsahová síť: https://napoveda.sklik.cz/zaciname-inzerovat/obsahova-sit/
17. Obsahová kampaň: https://napoveda.sklik.cz/kampane-a-sestavy/typy-kampani/obsahova-kampan/
18. Jednoduchá obsahová kampaň: https://napoveda.sklik.cz/kampane-a-sestavy/typy-kampani/jednoducha-obsahova-kampan/
19. Chytrá kampaň: https://napoveda.sklik.cz/kampane-a-sestavy/typy-kampani/chytra-kampan/
20. Zájmy: https://napoveda.sklik.cz/cileni/zajmy/
21. Zájmy o koupi: https://napoveda.sklik.cz/cileni/zajmy-o-koupi/
22. Témata: https://napoveda.sklik.cz/cileni/temata/
23. Umístění: https://napoveda.sklik.cz/cileni/umisteni/
24. Kombinace typů cílení: https://napoveda.sklik.cz/cileni/kombinace-typu-cileni/
25. Klíčová slova v obsahové síti: https://napoveda.sklik.cz/cileni/klicova-slova/cileni-pomoci-klicovych-slov-v-obsahove-siti/
26. Vylučující slova (OS), brand safety: https://napoveda.sklik.cz/cileni/klicova-slova/vylucujici-slova-os-brand-safety/
27. Filtr na věk: https://napoveda.sklik.cz/cileni/vek/
28. Individuální Max. CPC u typů cílení: https://napoveda.sklik.cz/cileni/individualni-nastaveni-max-cpc-u-ruznych-typu-cileni/
29. Frekvence zobrazení: https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/frekvence-zobrazeni-reklamy/
30. Rozpočet kampaně: https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/rozpocet-kampane/
31. Jak se platí: https://napoveda.sklik.cz/zaciname-inzerovat/jak-se-plati/
32. Nastavení sestav (minimální CPC a CPT): https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-sestav/
33. Přehled formátů bannerů: https://napoveda.sklik.cz/reklamy/bannery/prehled-podporovanych-formatu-bannerove-reklamy/ , úvod k bannerům: https://napoveda.sklik.cz/reklamy/bannery/
34. Pravidla pro bannery: https://napoveda.sklik.cz/pravidla/bannery/
35. Pravidla pro kombinovanou reklamu: https://napoveda.sklik.cz/pravidla/kombinovana-reklama/
36. Doporučení pro bannery: https://napoveda.sklik.cz/reklamy/bannery/doporuceni-pro-bannerovou-reklamu/
37. Dynamické proměnné (`{placement}`): https://napoveda.sklik.cz/mereni-uspesnosti/sledovaci-url/dynamicke-promenne/
38. Retargeting: https://napoveda.sklik.cz/cileni/retargeting/
39. Seznam webů obsahové sítě s kategoriemi a formáty (xlsx, 02/2026, 1 056 domén, návštěvnost Netmonitor 1/2026): https://napoveda.sklik.cz/wp-content/uploads/2026/02/weby-os-02-2026.xlsx
40. Témata a jejich nejvýznamnější weby (xlsx, 2023, neúplné): https://napoveda.sklik.cz/wp-content/uploads/2023/03/temata-weby-napoveda-sklik.xlsx
41. Smluvní podmínky pro inzerenty (neplatné klikání): https://napoveda.sklik.cz/pravidla/smluvni-podminky-pro-inzerenty/

Ceny, CTR, konverze:
42. ViVa marketing: průměrné ceny reklamy 1. 1. až 18. 2. 2025, Sklik čísla od specialisty Skliku, průřez všemi účty s inzercí (obsahová kampaň CPC 3,93 Kč, CPM 17,35 Kč; vyhledávací CPC 4,62 Kč, CPM 204,35 Kč): https://vivamarketing.cz/novinky/kolik-stoji-reklama-na-internetu-v-roce-2025/
43. marketingppc.cz: CTR v obsahové síti 4 až 8× nižší než ve vyhledávání, klasické bannery 0,06 až 0,2 %, remarketingové 0,1 až 1 %, průměr obsahové sítě kolem 0,5 %: https://www.marketingppc.cz/ppc/ctr/
44. Avedeo (data Google Ads 2021, ne Sklik): vyhledávání 3,17 %, obsahová síť 0,46 %: https://avedeo.cz/ctr-co-je-mira-prokliku-a-proc-ji-sledovat/
45. Seznam blog 2013: v obsahové síti je CTR i konverzní poměr nižší než ve vyhledávání, cena konverze může být podobná díky nižšímu CPC: https://blog.seznam.cz/2013/01/vyhodnocovani-kampani-v-obsahove-siti-z-hlediska-primeho-vykonu/
46. Seznam blog 2025: věkové kategorie 18–24, 25–39, 40–59, 60+; CTR prémiových formátů v přímém nákupu 0,12 až 0,48 % (nejde o aukce Skliku): https://blog.seznam.cz/2025/06/cilena-reklama-v-primem-nakupu/
47. Proficio, případová studie e-shopu: display přivedl asi 11 000 uživatelů za poloviční cenu než vyhledávání, přímých konverzí méně: https://proficio.cz/zvysili-jsme-vykon-kampani-o-32-diky-obsahove-siti-v-skliku

Právo:
48. Zákon 634/1992 Sb., příloha č. 2 písm. e (reklama, která děti přímo nabádá ke koupi nebo k přesvědčení dospělého, je klamavá obchodní praktika): https://www.zakonyprolidi.cz/cs/1992-634
49. Zákon 110/2019 Sb. § 7 (souhlas dítěte se službou informační společnosti od 15 let): https://www.zakonyprolidi.cz/cs/2019-110
50. DSA čl. 28 odst. 2 (platforma nesmí zobrazovat reklamu založenou na profilování, když ví, že příjemce je nezletilý; povinnost Seznamu, ne naše; text z nezávazného zrcadla): https://www.eu-digital-services-act.com/Digital_Services_Act_Article_28.html
51. Směrnice 2005/29/ES, příloha I bod 28 (zdroj původního zákazu): https://eur-lex.europa.eu/legal-content/CS/TXT/?uri=CELEX:32005L0029 (NEOVĚŘENO stažením, EUR-Lex z kontejneru nevrací text; český překlad je ověřen v [48]).
52. Nesrovnalost: ads-agency.cz uvádí minimální CPC 0,20 Kč, nápověda Skliku [31, 32] 1 Kč bez DPH. Platí nápověda. https://ads-agency.cz/blog/reklama-na-seznam-cz-kompletni-pruvodce-sklik-ppc-pro-cesky-trh-2026/
53. Interní: `plan/hledanost-printopia.md` (hledanost a CPC ve vyhledávání), `plan/prijimacky.md` (trh 156 tis. uchazečů), `plan/postupy/sklik.md` (kritérium 190 návštěv).

## Čeho se vyvarovat
- **Dětské a teenagerské weby.** Přepínač „dětské weby“ jsem v nápovědě ani v API nenašel. Dostupné nástroje: vyloučená umístění (`excludedUrls`), vyloučené zájmy, záměry a témata, vylučující slova a filtr na věk [13, 23, 24, 26, 27]. Z oficiálního seznamu [39] vyloučit hry, kvízy a teen weby: abicko.cz, jenpohadky.cz, minihry.net, hry.seznam.cz, games.tiscali.cz, hrej.cz, hrajeme.cz, hrajsisemnou.cz, jsemhrac.cz, rajhrace.cz, profigamers.cz, gamebot.cz, phgame.cz, playzone.cz, loupak.fun, onlinovky.cz, mojekvizy.cz, kviz.kvizky.cz, kvizy.qizy.cz, superkviz.cz, kvizonline.cz, zabavnaveda.cz, mangazine.cz, antiyoutuber.cz, rajce.idnes.cz, i60.cz, libimseti.cz, odpovedi.cz. Seznam [39] není úplný (277 domén v něm nemá kategorii, `#N/A`, a je to jen „TOP asi 1 000 webů“ podle [16]), proto po spuštění číst report umístění a vylučovat další.
- **Přímá výzva dítěti.** Žádné „kup si“, „řekni rodičům“, „přemluv“ a žádný tón určený deváťákovi („Nedáváš zlomky?“). Texty a obrázky mluví k rodiči. Pozor, že na stránkách pro studenty (prikladyzmatematiky.cz, ireferaty.cz, studentmag.cz, studium.cz v seznamu [39]) čtou reklamu hlavně děti: neumisťovat tam bez zvláštního zdůvodnění, i když je text pro rodiče [48].
- **Cílení na děti a mladé.** Zájmy „Maturanti“ (38900), „Studenti VŠ/VOŠ“ (38800), „Hry a hračky“ (37400 až 37402), záměry „Pořady o dětech“ (10293), „Vzdělávací pořady“ (10310, diváci Stream.cz) a „Dětské zboží“ (10008, převážně kojenci) nepoužívat. Zájmy a záměry vznikají jen u uživatelů, kteří souhlasili s cílenou reklamou [20, 21]. Zákaz profilování nezletilých je povinnost Seznamu [50]; jak ji u zájmů a záměrů plní, nevíme (NEZJIŠTĚNO), proto se chránit vyloučeními.
- **Filtr na věk není v API.** V Drak ani Fénix dokumentaci chybí (ověřeno prohledáním `groups.create/update/list`, `campaigns.create/update/list` a celé OpenAPI Fénix [3, 13, 14]), v rozhraní je to záložka Věk s kategoriemi 18–24, 25–39, 40–59, 60+ [27, 46]. Nelze na něj spoléhat jako na ochranu před dětmi. Samostatně se použít nedá, vždy jen jako filtr dalšího cílení [27]. Výběr 25–39 a 40–59 by děti vyloučil, ale přes API ho nenastavíme.
- **Příliš široké cílení.** „Nedoporučujeme cílit na publika pouze podle velikosti“ [20]. Záměr „Rodiče dítěte školáka“ (765 527 podle Skliku) zahrnuje rodiče všech ročníků 1. až 9. třídy, přijímačky řeší jen zlomek, pravděpodobně pod pětinu (ODHAD z [53]: asi 156 tis. uchazečů, tedy domácností asi 100 až 150 tis.). Bez dalšího zúžení platíme za rodiče prvňáků.
- **Kombinace typů cílení zužuje.** Různé typy cílení v jedné sestavě se omezují navzájem (průnik) [24]. Jedna sestava = jeden typ cílení, jinak publikum klesne téměř na nulu a reklama se nezobrazí. Výjimka: retargeting a zájmy o koupi se doplňují [24].
- **Jednoduchá a Chytrá kampaň.** Jednoduchá obsahová kampaň už nejde založit v rozhraní, nemá cílení, filtry na věk a pohlaví a zobrazuje se hlavně uživatelům bez souhlasu s cílením [18]. Chytrá kampaň cílení neřídíme vůbec (běží i ve vyhledávání) [19], v Drak ji nezaložíme (`campaigns.check` s `type: "smart"` vrátí `wrong_param_value`, vlastní test [15]) a ve Fénix potřebuje jiný přístupový token [14]. Pro citlivou skupinu obojí nevhodné.
- **Retargeting bez souhlasu.** Potřebuje retargetingový kód a souhlas s cookies [38, 53: sklik.md zdroje 15, 17]. Printopia nemá cookie lištu a má jen pár návštěv denně, seznam by byl prázdný. Zatím ne.
- **Nízký rozpočet proti CPC.** Doporučený poměr denní rozpočet : max. CPC je v obsahové síti 100 : 1, minimální denní rozpočet 30 Kč [30], tedy 30 Kč odpovídá CPC 0,30 Kč (menší než minimum 1 Kč [32]). Při 30 Kč a CPC 3 Kč je poměr 10 : 1, reklama se ukáže jen na část zobrazení (např. „na každý desátý refresh stránky“) a může dojít k přečerpání [30]. Přečerpání v 7denním okně je omezeno na sedminásobek denního rozpočtu a kredit se strhává dávkově, takže peněženka může krátce klesnout do mínusu [31].
- **Příliš nízká nabídka.** Při příliš nízké ceně za proklik nebo za zobrazení se reklama může nezobrazovat vůbec [31]. U CPT je minimum 5 Kč za 1 000 zobrazení a platí first price [31, 32]; průměr Skliku je 17,35 Kč [42], takže nabídka u minima prakticky nevyhrává.
- **Podvodné a náhodné prokliky.** Sklik se zavazuje neplatnému klikání aktivně i pasivně bránit, ale co je neplatný proklik, posuzuje výhradně on (přihlédne k našim argumentům) [41]; kvalita sítě se prý pravidelně kontroluje [47]. Vrácení peněz za takové prokliky nečekat. Reklamy na malých mobilních plochách (320×100, Interscroller) mají nejvíc prokliků [33], část mohou být omylem (ODHAD, tvrzení nenalezeno). Bránit se: vlastní trychtýř měří, kolik prokliků skutečně načetlo stránku a zůstalo víc než pár sekund; dle `{placement}` [37] vyloučit domény s prokliky bez chování.
- **Aplikace.** Nápověda o vyloučení mobilních aplikací nic neuvádí [16, 23]: vyloučit lze jen domény a URL. Nezjištěno, zda se obsahová síť zobrazuje i v aplikacích. Při testu sledovat, zda `{placement}` přijde prázdné.
- **Měření podle poslední konverze.** Konverze z obsahu bývají podhodnocené, lidé nekupují hned, hodnotí se i asistované [45, 47]. Rozhoduje náš vlastní trychtýř (`utm_source=sklik`, `utm_medium=display`, `utm_term={placement}`, `utm_content={creative}`); `{keywordId}` a `{keyword}` jsou jen pro vyhledávání [37].
- **Obrázky a texty zamítnuté při schválení.** Kombinovaná reklama: žádný uměle vložený text, loga eshopu a tlačítka v obrázku, žádný náhled stránky, žádná animace, obrázek se může na některých plochách oříznout o 7 % [35]. Banner: text povinný, vyplnit celou plochu, bez průhledného pozadí, nesmí napodobovat dialogová okna, max. 250 kB [34]. „Zdarma“ jen když je nepodmíněné [53: sklik.md].
- **Míchat síť v jedné kampani.** Obsahovou kampaň vést zvlášť od vyhledávací (naše `fulltext` kampaň zůstane beze změny), jinak se rozbije rozpočet i vyhodnocení [53: sklik.md].
- **Frekvence.** Výchozí je 10 zobrazení uživateli denně, u bannerů doporučeno 5 až 7, u obecné kombinované reklamy 8 až 10, týdně 20 až 30; při 30. zobrazení je CTR zhruba poloviční [29].

## Jak na to
### Typy kampaní a formáty, co umí API
- Typy v API (`campaigns.listCampaignsTypes`, naše volání [15]): product, simple, fulltext, video, context, audio, zbozi, smart. `campaigns.create` a `campaigns.check` přijímají jen fulltext, context, product, video, simple, zbozi [2, 15]. Pro nás platí **`context`** (obsahová kampaň, způsob úhrady `paymentMethod`: `cpc` nebo `cpm`) [2].
- Reklamní formáty v obsahové kampani: banner, kombinovaná reklama, branding, HTML5 banner (jen pro oprávněné), dynamický banner a retargeting, video, nativní, externí kód [16, 17]. Textové inzeráty (`eta`) jsou jen pro vyhledávání [16].
- **Banner** (`banners.create`: `groupId`, `name`, `clickthruUrl`, `file` jako base64, `status`) [1, 4]. Formáty z `images.constraints.list` (naše volání [15]), max. 256 000 B: 300×300, 160×600, 728×90, 300×250, 300×600, 970×310, 320×100, 970×210, 480×300, 480×480, 500×200 a Interscroller 720×1280; 468×60 a 930×180 jsou `supported: false`. API `banners.create` uvádí JPG, PNG, GIF [4], nápověda i WebP a AVIF [34]. Pořadí podle počtu prokliků (nápověda [33]): 320×100, 300×300, 300×600, 480×300, 480×480, 300×250, 970×310, 160×600, 970×210, 728×90, 500×200. Pro sondu stačí 320×100, 300×300 a 300×600. Banner se snáze zobrazí na ploše stejných rozměrů, proto více velikostí [33].
- **Kombinovaná reklama** (`ads.create`, `adType: "combined"`): `longLine` (dlouhý titulek, max. 90), `shortLine` (krátký, max. 25), `description` (max. 90), `companyName` (max. 25), `image` (1,91:1, min. 600×314, doporučeno 1200×628), `imageSquare` (1:1, min. 300×300, doporučeno 1200×1200), volitelně loga, `finalUrl`, `trackingTemplate`, max. 1 MB [5, 6, 35]. Obrázky jako base64 nebo `imageId` z `images.create` (tam jde o URL na CDN, proto v Drak použít base64 přímo v reklamě).
- **Schvalování.** Doba není v nápovědě uvedena (NEZJIŠTĚNO). Po spuštění zkontrolovat zamítnuté reklamy (`ads.list`, `banners.list`); v našem případě textové reklamy zobrazovaly i se stavem `new` (viz CLAUDE.md). Podpora odpovídá do 2 hodin v 95 % dotazů.
- **Cena a rozpočet.** Min. denní rozpočet obsahové kampaně 30 Kč (ověřeno `campaigns.check`: 2000 halířů vrátí `campaign_dayBudget_is_too_low`, `minimum: 30`, 3000 projde [15]). Min. CPC 1 Kč, min. CPT 5 Kč bez DPH [31, 32]. CPC je aukce druhé ceny („zaplatíte nejnižší potřebnou částku“), CPT je první cena [31]. V obsahové síti se nepoužívá optimalizace denního rozpočtu přes den, ta je funkce vyhledávání [30].

### Cílení na rodiče školáků: ID z API (naše volání 2026-10-01 [15])
Záměry (`intends`, v rozhraní Zájmy o koupi; „Rodiče dítěte školáka“ je ve větvi Životní události). Velikost publika je údaj Skliku bez uvedené jednotky a období:
| ID | název | publikum | poznámka |
|---|---|---:|---|
| 12573 | Rodiče dítěte školáka | 765 527 | hlavní volba, nejpřesnější na rodiče |
| 12260 | Základní školy (návštěvníci Firmy.cz) | 17 852 | menší, doplněk |
| 12510 | Vzdělávání (posluchači Podcasty.cz) | 84 776 | doplněk |
| 12444 | Děti a Rodina (posluchači Podcasty.cz) | 26 981 | doplněk |
| 10042 | Školní potřeby | 2 790 | příliš malé, jen kombinace |
| 12570 | Rodiče dítěte předškolního věku | 1 188 809 | NE, jiný ročník |

Zájmy (`interests`, pole `interestCategoryId`, 241 kategorií): 37300 Rodiny s dětmi (obecné), 37306 Základní škola, 37303 Učebnice pro děti, 38700 Vzdělávání (obecné), 38702 Školení a vzdělávání. Vyloučit (`interests.negative.create`): 37400 až 37402 Hry a hračky, 32600 až 32602 počítačové hry, 37200 až 37205 kojenci a batolata, 37100 až 37102 těhotenství.
Témata (`themes`, pole `categoryId`, 34 kategorií): 123 Práce a vzdělávání, 105 Děti a mateřství (podle [40] jen jsme.cz a eduzin.cz, většinou kojenci a těhotenství, tedy slabé), 125 Přírodní vědy, 136 Mezilidské vztahy (rodina.cz, ale i i60.cz s teens). Vyloučit (`themes.negative.create`): 122 Počítačové hry. Témata jsou podle webů, ne podle věku čtenáře, proto jako hlavní cílení nevhodná.
Klíčová slova v obsahové síti [25]: jen volná shoda (`broad`), podstatná jména, 5 až 10 (max. 20) slov v sestavě, diakritika, bez long-tailů, statistiky jen za celek sestavy. Návrh: „přijímačky“, „přijímací zkoušky“, „CERMAT“, „matematika“, „střední škola“, „gymnázium“, „deváťák“. Reklama se může zobrazit i na stránce, která neobsahuje všechna zadaná slova [25]. Podzim není sezóna článků o přijímačkách (ODHAD), vrchol je leden až duben [53].
Umístění (`patterns`): vlastní seznam jen z webů [39, kategorie Těhotenství a rodičovství: emimino.cz 9,96 mil. zobrazení stránky měsíčně, modrykonik.cz 2,68 mil., mimibazar.cz 2,03 mil., maminka.cz 1,75 mil., rodina.cz 0,32 mil., maminkam.cz 0,07 mil.]. Čtenářky jsou převážně matky malých dětí (ODHAD), tedy slabě relevantní. Použít jen jako zkoušku, ne hlavní cíl.
Věk a pohlaví: v API nejsou [3, 14]; v rozhraní je to filtr, nikdy samostatné cílení [27].

### Pořadí API volání (nic z toho zatím nespouštět)
Ve všech případech `call(metoda, user, [...])` jako v `printopia/marketing/sklik_api.py` (JSON, `https://api.sklik.cz/drak/json/v5/`), `user = {"session": session}`.
1. `client.loginByToken(SKLIK_TOKEN)` a `client.get` (kredit musí být ≥ 82 Kč).
2. `campaigns.check` na nový obsahový záměr (kontrola bez založení):
   `[{"name":"Printopia – obsah rodiče RRRR-MM-DD HH:MM","dayBudget":3000,"type":"context","paymentMethod":"cpc"}]` (název s časem, Sklik nepustí duplicitní ani u odstraněné kampaně).
3. `campaigns.create` s `status: "suspend"`, `dayBudget: 3000` (30 Kč), `totalBudget` ≥ denní (nastavit např. 4 000 = 40 Kč), `adSelection: "weighted"`, `excludedUrls` (seznam výše ve tvaru `"http://abicko.cz"`, bez protokolu rozlišení, platí pro celou doménu [23]), `negativeKeywords` (brand safety, jednoslovné podstatné jméno, volná shoda: např. „pohádky“, „omalovánky“, „minecraft“, „roblox“, „fortnite“, podle [26] nezadávat mnohoznačná slova, maximum 100).
4. `groups.create`: `[{"campaignId":ID,"name":"Záměr rodiče školáka","cpc":300,"maxUserDailyImpression":5}]` (CPC 3 Kč = 300 halířů, strop zobrazení 5 denně u bannerů [29]; `devicesPriceRatio` ponechat prázdné, upravovat až podle dat).
5. `intends.create`: `[{"groupId":GID,"intendCategoryId":12573}]`. Další sestavy (zájmy, klíčová slova) až po prvních datech, kvůli rozpočtu 30 Kč na celou kampaň (sestavy rozpočet nedělí, ale ředí zobrazení).
6. Vyloučení po sestavách (ne po kampani): `interests.negative.create` `[{"groupId":GID,"interestCategoryId":37400}]`, `themes.negative.create` `[{"groupId":GID,"categoryId":122}]`, `intends.negative.create` `[{"groupId":GID,"intendCategoryId":10293}]`, případně `patterns.negative.create` `[{"groupId":GID,"pattern":"abicko.cz"}]` (ID z tabulky výše; vyloučení webů na úrovni kampaně dělá `excludedUrls`).
7. `ads.create` s `adType: "combined"` (texty jen pro rodiče; fotka bez vloženého textu) a `banners.create` pro 320×100, 300×300, 300×600 (obrázky v base64, ≤ 250 kB; text na banneru je povinný, pozor na „kup si“). `finalUrl` s `?utm_source=sklik&utm_medium=display&utm_term={placement}&utm_content={creative}` [37]; automatické tagování musí zůstat vypnuté (viz `plan/postupy/sklik.md`).
8. Počkat na schválení (`ads.list`, `banners.list`), potom `campaigns.update` `status: "active"`; kredit a útratu hlídat `sklik_api.py --status|--stats` (skript je dnes jen pro `fulltext`, pro obsah napsat `sklik_os.py` se stejnou pojistkou).
9. Den 1 až 3: report umístění (`patterns.createReport` a `patterns.readReport`) a naše události podle `utm_term` (doména). Vyloučit domény s prokliky bez chování a všechny dětské weby (`campaigns.update` s doplněným `excludedUrls`). Den 7: ztracená zobrazení z rozpočtu a pořadí; snižovat CPC, ne vypínat [30].

## Odhad
Vše je ODHAD kromě čísel se zdrojem. Na našem účtu zatím nejsou vlastní data z obsahu, ani z vyhledávání (`vyhodnoceni.py`: 0 zobrazení, 4 návštěvy ze Skliku).

**Typické ceny a CTR (zdroje):**
| ukazatel | vyhledávání | obsahová síť | zdroj |
|---|---:|---:|---|
| ø CPC Sklik | 4,62 Kč | 3,93 Kč | [42] |
| ø CPM Sklik | 204,35 Kč | 17,35 Kč | [42] |
| CTR Sklik, VÝPOČET z CPM/CPC: CPM ÷ (10 × CPC) | asi 4,4 % | asi 0,44 % | z [42] |
| CTR obecně | 3 až 4 % | asi 0,5 % (banner 0,06 až 0,2 %, remarketing 0,1 až 1 %) | [43] |
| CTR Google Ads 2021 (ne Sklik) | 3,17 % | 0,46 % | [44] |
| naše CPC „cermat testy“ ve vyhledávání | 1,3 Kč (návrhy Skliku) | | [53] |

Minimální nabídka: CPC 1 Kč, CPT 5 Kč [31, 32]. Průměr 3,93 Kč je celoplošný, v úzké skupině rodičů školáků a s malým CTR čekat spíš 3 až 5 Kč (ODHAD). **Rozpětí 1 až 2 Kč je optimistický okraj**, ne střed: i kdyby se vyhrála každá aukce za minimální CPT 5 Kč, vyjde 82 Kč jen 16 400 zobrazení a při CTR 0,2 až 0,44 % 33 až 72 prokliků, a to při průměrném CPM 17,35 Kč [42] nevyjde.

**Co koupí kredit 82 Kč bez DPH** (kredit vydrží 2,7 dne při 30 Kč denně, předpoklad: reklama schválená, bez zpoždění):
| CPC | prokliků | zobrazení při CTR 0,44 % | podíl z 190 návštěv potřebných pro rozhodnutí |
|---:|---:|---:|---:|
| 1 Kč (minimum) | 82 | 18 600 | 43 % |
| 2 Kč | 41 | 9 300 | 22 % |
| 3,93 Kč (průměr [42]) | 21 | 4 700 | 11 % |
| 5 Kč | 16 | 3 700 | 9 % |

**Objednávky** (konverze prokliku na zaplacenou objednávku 349 Kč). Předpoklad: obsah konvertuje méně než vyhledávání [45], vyhledávání jsme dosud odhadovali na 0,5 až 1 % [53], pro obsah bereme 0,2 až 1 %, střed 0,3 % (ODHAD, bez dat):
| CPC | konverze 0,3 % (střed): objednávek | šance aspoň 1 objednávky při 0,3 % | šance při 1 % |
|---:|---:|---:|---:|
| 1 Kč | 0,25 | 22 % | 56 % |
| 2 Kč | 0,12 | 12 % | 34 % |
| 3,93 Kč | 0,06 | 6 % | 19 % |
Očekávaná tržba za 82 Kč: 15 až 290 Kč podle scénáře (nejčastěji pod 90 Kč), tedy téměř vždy ztráta. **Bod zvratu:** při ceně 349 Kč a CPC 1 Kč stačí konverze 0,29 %, při 2 Kč 0,57 %, při 3,93 Kč 1,13 %, při 5 Kč 1,43 %. Při konverzi 0,3 % stojí jedna objednávka 333 Kč (CPC 1), 667 Kč (CPC 2), 1 310 Kč (CPC 3,93).

**Statistická vypovídací hodnota:** 0 nákupů z 21 prokliků neříká nic (95% horní mez konverze 15,5 %), z 41 prokliků 8,6 %, z 82 prokliků 4,5 %; teprve 190 návštěv dává horní mez 2 % [53]. Test s 82 Kč proto **nic nerozhodne**.

**Cena sondy na 190 návštěv:** 190 Kč (CPC 1), 380 Kč (CPC 2), 747 Kč (CPC 3,93), 950 Kč (CPC 5). Firemní rozpočet je zhruba 350 Kč, test by ho sežral celý nebo přečerpal, proto dál čekat s rozhodnutím (CLAUDE.md: další kredit do Skliku do ledna ne).

**Srovnání s vyhledáváním:** „cermat testy“ má CPC asi 1,3 Kč a CTR kolem 3 % [53], takže klik je ve vyhledávání levnější než v obsahu (1,3 proti 3,93 Kč), ale hledají hlavně lidé chtějící testy zdarma, tedy s nižší konverzí. Obsahová síť má teoreticky větší dosah (95 % českého internetu, více než 3 000 webů [16]), ale agentury hlásí, že konverze přichází hlavně asistovaně [45, 47].

## Kontrolní seznam
Každý bod se ověřuje příkazem, výstupem API nebo pohledem do reportu. Před založením obsahové kampaně:
- [ ] Rozhodnuto o rozpočtu sondy: aspoň 400 Kč (190 návštěv při CPC 2 Kč), schválila firma (Ondřej, výdaj), a kredit v účtu je znám (`client.get`).
- [ ] Obsahová kampaň je typu `context` a zvlášť od `fulltext`; `paymentMethod: "cpc"`, denní rozpočet ≥ 30 Kč, celkový rozpočet ≥ denní, kampaň zakládána jako `suspend` po `campaigns.check`.
- [ ] Jedna sestava = jedno cílení (záměr 12573 nebo zájmy nebo klíčová slova), žádné kombinace typů, které by publikum zúžily téměř na nulu.
- [ ] Max. CPC aspoň 3 Kč a poměr denní rozpočet : CPC vědomě zvolený (30 Kč : 3 Kč = 10 : 1, doporučeno 100 : 1); `maxUserDailyImpression` 5 u bannerů (8 až 10 u kombinované reklamy).
- [ ] `excludedUrls` obsahuje všechny dětské, herní, kvízové a teen weby ze seznamu výše; seznam obnoven z aktuální verze xlsx [39] a po 3 dnech doplněn z reportu umístění.
- [ ] Vyloučené zájmy, záměry a témata (hry a hračky, kojenci, těhotenství, počítačové hry, pořady o dětech) nastavené; `negativeKeywords` bez mnohoznačných slov.
- [ ] Žádný text ani obrázek nevyzývá dítě ke koupi ani k přemlouvání rodičů, žádný tón pro deváťáka (`assert` v generátoru textů: zakázaná „kup si“, „řekni rodičům“, „přemluv“, oslovení „ty“); každý titulek nebo popisek oslovuje rodiče; čte člověk jako korektor.
- [ ] Kombinovaná reklama: fotka bez vloženého textu, loga a tlačítek, bez náhledu stránky, bez animace, 1,91:1 a 1:1, ≤ 1 MB; banner: formáty 320×100, 300×300, 300×600, ≤ 250 kB, text povinný, bez průhledného pozadí.
- [ ] Texty a ceny pravdivé a nepodmíněné („zdarma“ jen když opravdu zdarma), cílová stránka vrací 200 a má provozovatele v patičce.
- [ ] Automatické tagování je vypnuté (`autotagging.get`); měření: `utm_source=sklik&utm_medium=display&utm_term={placement}&utm_content={creative}` ukládá trychtýř a `vyhodnoceni.py` počítá obsah zvlášť od vyhledávání.
- [ ] Předem zapsané kritérium vyhodnocení: počet návštěv (190), co se počítá (klik na „Koupit“, e-mail rodiče, objednávka), a pravidlo zastavení (např. po 100 Kč bez jediného kliku na „Koupit“ pozastavit).
- [ ] `plan/hledanost-printopia.md` doplněna oddílem o obsahové síti (Sklik API nedává odhad zobrazení v obsahu, proto jen velikost publika z `intends.getCategoryList`, a ta je jen Seznam).
- [ ] Po spuštění: den 1 schválené reklamy, den 3 report umístění a vyloučení (dětské weby, domény bez chování), den 7 ztracená zobrazení a pozice, kontrola, zda `{placement}` nepřichází prázdné (aplikace); po vyčerpání kreditu nic nedobíjet bez nového rozhodnutí firmy.
