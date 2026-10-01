# Zboží.cz (Seznam Nákupy) a Heureka.cz: postupy a audit pro Printopii

Cílová skupina: hledá rodič (občas žák 9. třídy), používá žák, **platí rodič**. Nabídka v srovnávači mluví k rodiči a nikdy nevyzývá dítě ke koupi (zákon 634/1992 Sb., příloha č. 2 písm. e; UCPD příloha I bod 28). Kdo hledá, doložit až měřením v testu (zdroj `utm_source`).
Zpracováno 2026-10-01 (17:30 pražského času), jen výzkum, nic nezaloženo, nic nekoupeno, nikde se neregistrovalo. Co je odhad, je označeno slovem ODHAD.

## Závěr

- **Zboží.cz: ANO, technicky i podle pravidel lze, jako levná sonda.** Registrace zdarma, e-knihy a digitální zboží mají v feedu výslovnou podporu (`DELIVERY_ID` = `ONLINE`), min. CPC pro naši cenu 1,86 až 2,57 Kč bez DPH, účet Seznam/Sklik už máme. Slabina: návštěvnost pro náš dotaz je malá a neznámá, sada PDF bude vedle tištěných sbírek za 134 až 399 Kč.
- **Heureka.cz: NE teď.** Placený výdej (PPC) chce minimální dobití 499 Kč bez DPH (přesahuje zbytek rozpočtu), FREE režim dává jen 5 až 10 % návštěvnosti, web musí mít český telefon (nemáme), znění obchodních podmínek Heureky je za přihlášením. Vrátit se k ní po výsledku Zboží.cz.
- Čas do první návštěvy (ODHAD): 1 až 5 dní od registrace provozovny. Práce Clauda před tím 1 až 2 h (feed, obrázek, test).

## Zdroje
Všechny navštíveny 2026-10-01, pokud není uvedeno jinak.

Zboží.cz / Sklik (nápověda):
1. Pravidla pro internetové obchody v Inzerci Nákupy (dříve Zboží.cz): https://napoveda.sklik.cz/pravidla/pravidla-a-podminky-zbozi-cz/pravidla-pro-internetove-obchody/
2. Nepovolený obsah a postihy: https://napoveda.sklik.cz/pravidla/pravidla-a-podminky-zbozi-cz/nepovoleny-obsah-a-postihy/
3. Banování nabídek: https://napoveda.sklik.cz/pravidla/pravidla-a-podminky-zbozi-cz/banovani-nabidek/
4. Registrace provozovny: https://napoveda.sklik.cz/inzerce-nakupy/registrace-provozovny/
5. Ceník Inzerce Nákupy: https://napoveda.sklik.cz/inzerce-nakupy/cenik-inzerce-nakupy/ a dynamický ceník CSV (platnost od 2026-09-30): https://www.zbozi.cz/static/mincpc.csv
6. Specifikace feedu: https://napoveda.sklik.cz/reklamy/xml-feed/specifikace/
7. Doprava a výdejní místa (elektronické doručení): https://napoveda.sklik.cz/inzerce-nakupy/doprava-a-vydejni-mista-na-zbozi-cz/
8. Párování nabídek: https://napoveda.sklik.cz/inzerce-nakupy/parovani-nabidek/
9. Kde se inzerce Nákupů zobrazuje: https://napoveda.sklik.cz/inzerce-nakupy/kde-se-inzerce-nakupu-zobrazuje/
10. Technické podmínky (řazení nabídek): https://napoveda.sklik.cz/pravidla/pravidla-a-podminky-zbozi-cz/technicke-podminky-zbozi-cz/
11. Hodnocení a recenze: https://napoveda.sklik.cz/inzerce-nakupy/hodnoceni-a-recenze/
12. Měřicí a konverzní kód, API Zboží.cz: https://napoveda.sklik.cz/inzerce-nakupy/merici-a-konverzni-kod-zbozi-cz/
13. Jak se platí, dobití kreditu: https://napoveda.sklik.cz/zaciname-inzerovat/jak-se-plati/ , https://napoveda.sklik.cz/zaciname-inzerovat/jak-se-plati/dobiti-kreditu/
14. Smluvní podmínky pro inzerenty (Seznam.cz, a.s., IČ 26168685, Praha 5): https://napoveda.sklik.cz/pravidla/smluvni-podminky-pro-inzerenty/
15. Kampaň Nákupy a FAQ: https://napoveda.sklik.cz/kampane-a-sestavy/typy-kampani/seznam_nakupy/ , https://napoveda.sklik.cz/kampane-a-sestavy/typy-kampani/seznam_nakupy/faq-kampane-zbozi-cz/
16. Rozpočet kampaně (min. 30 Kč denně): https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/rozpocet-kampane/
17. API Fénix (OpenAPI, cesty `/nakupy/*`): https://api.sklik.cz/v1/openapi.json
18. Strom kategorií Zboží.cz: https://www.zbozi.cz/static/categories.json

Živá měření:
19. Zboží.cz, hledání „přijímačky matematika“ a další dotazy: https://www.zbozi.cz/hledej/?q=p%C5%99ij%C3%ADma%C4%8Dky%20matematika
20. Seznam, výsledky hledání se skupinou „Nabídky ze Zboží.cz“ (dotazy v oddílu Odhad): https://search.seznam.cz/?q=cvi%C4%8Debnice+matematika+9.+t%C5%99%C3%ADda
21. Firmy.cz, záznam MYPIXEL (zatím neověřená firma, převzato z rejstříků): https://www.firmy.cz/?q=MYPIXEL
22. Sklik `keywords.suggest.stats`, hledanost dotazů s nákupním záměrem (2026-10-01), plus `plan/hledanost-printopia.md`.

Heureka:
23. Registrace e-shopu: https://sluzby.heureka.cz/napoveda/registrace-eshopu/
24. Podmínky pro aktivaci e-shopu: https://sluzby.heureka.cz/napoveda/podminky-pro-aktivaci-e-shopu/
25. Ceník prokliků a CSV ceník: https://sluzby.heureka.cz/napoveda/cenik-prokliku/ , https://api.heureka.cz/v1/price-list/active/download/?format=csv
26. FREE a PPC režim: https://sluzby.heureka.cz/napoveda/jaky-je-rozdil-mezi-free-a-ppc-rezimem/
27. Dobíjení kreditu a faktury: https://sluzby.heureka.cz/napoveda/dobijeni-kreditu-a-faktury/
28. Specifikace XML souboru: https://sluzby.heureka.cz/napoveda/xml-feed/
29. Ověřeno zákazníky a úrovně: https://sluzby.heureka.cz/napoveda/co-je-sluzba-overeno-zakazniky/ , https://sluzby.heureka.cz/napoveda/urovne-sluzby-overeno-zakazniky-vbc/
30. Obchodní podmínky Heureky: NEDOSTUPNÉ (https://sluzby.heureka.cz/obchodni-podminky/ vede na přihlášení, https://heureka.group/cs/podminky-pouzivani dává 403). Seznam zakázaného zboží Heureky proto NEZJIŠTĚN.
31. Heureka Group a.s., IČO 07822774, Karolinská 706/3, Praha 8 (česká firma, faktury v CZ): https://www.podnikatel.cz/rejstrik/heureka-group-a-s-07822774/
32. E-knihy na Heurece existují (jen z výsledku vyhledávání, stránku jsem neotevřel): https://e-book-elektronicke-knihy.heureka.cz/

Právo:
33. Prodej digitálního obsahu v e-shopu (informační povinnosti, odstoupení, 2022-11-22): https://www.martindomes.cz/nova-pravidla-pro-e-shopy-dil-4-prodej-digitalniho-obsahu/

## Fakta k pravidlům

**Digitální zboží (zdroje 1, 2, 6, 7).** Výslovně se smí: e-knihy, audioknihy, softwarové licence, aktivační klíče, elektronické poukazy (doručení e-mailem, do účtu nebo odkazem ke stažení). V kategorii Elektronické knihy (id 1721) i v Učebnicích existují e-knihy k přijímačkám (např. „Ještě není pozdě: Přijímačky s Robinem“ [E-kniha] 278 Kč, 4 obchody). Výslovně zakázáno: služby, loga a melodie, tapety a hry do mobilů, placené stahování hudby a filmů, zájezdy, **jazykové, vzdělávací a motivační kurzy (prezenční i online)**, zboží, které nejde koupit přímo na webu obchodu, zprostředkovaný prodej třetích stran. PDF sbírka úloh v seznamu zakázaných není, ale hranice „vzdělávací kurz“ je výklad Seznamu (viz Čeho se vyvarovat).

**Požadavky na e-shop (zdroje 1, 4, 14).** Registrovat se mohou jen internetové obchody, které už fungují a jsou veřejné. Na webu musí být: IČO, kontakt (sídlo; e-mail nebo telefon), nákupní košík nebo objednávkový formulář, VOP, nabídky k prodeji, provozovatel shodný s registrací. Název subjektu max. 24 znaků, ověřitelný (doména, web, rejstřík). Žádný minimální počet produktů (jedna nabídka stačí; 20 nabídek chce jen varianta „provozovna bez e-shopu“, ta se nás netýká). Registrace zároveň vytvoří/propojí záznam na Firmy.cz a veřejný Detail obchodu s hodnocením.

**Feed (zdroj 6).** XML, UTF-8, kořen `<SHOP xmlns="http://www.zbozi.cz/ns/offer/1.0">`, položky `<SHOPITEM>`. Povinné: `PRODUCTNAME` (doporučeno 70, max 255 znaků), `DESCRIPTION` (doporučeno 250 až 1024 znaků, čistý text, žádné HTML), `URL` (unikátní, bez diakritiky a mezer, nesmí přesměrovat na hlavní stránku), `PRICE_VAT` (Kč, shodná s webem), `DELIVERY_DATE` (0 = ihned), `IMGURL` (JPEG/PNG/WebP, min. 425×440 px, bez loga a vodoznaků). Doporučené: `ITEM_ID`, `CATEGORYTEXT` (cesta ze stromu kategorií, oddělovač `|`), `DELIVERY` s `ONLINE`, `MANUFACTURER`, `ISBN` (nemáme, není nutný), `MAX_CPC_SEARCH` a `MAX_CPC` (1 až 1000 Kč; bez nich se účtuje ceníkové minimum). Feed se stahuje 1 až 12× denně.

**Příklad feedu pro Printopii** (text před nasazením zkontrolovat podle pravidla Texty):
```xml
<?xml version="1.0" encoding="utf-8"?>
<SHOP xmlns="http://www.zbozi.cz/ns/offer/1.0">
  <SHOPITEM>
    <ITEM_ID>printopia-matematika-sada</ITEM_ID>
    <PRODUCTNAME>Printopia Přijímačky z matematiky po tématech, sada PDF</PRODUCTNAME>
    <DESCRIPTION>Sada 14 souborů PDF k vytištění: úvodní test, 12 tematických listů s postupy řešení a studijní plán. Pro žáky 9. tříd, kteří se připravují na jednotnou přijímací zkoušku z matematiky. Digitální obsah, soubory ke stažení po zaplacení.</DESCRIPTION>
    <URL>https://printopia.cz/koupit?utm_source=zbozi&amp;utm_medium=cpc</URL>
    <PRICE_VAT>349</PRICE_VAT>
    <DELIVERY_DATE>0</DELIVERY_DATE>
    <IMGURL>https://printopia.cz/zbozi-sada.png</IMGURL>
    <CATEGORYTEXT>Kultura a zábava | Knihy | Učebnice | Přírodní vědy | Matematika</CATEGORYTEXT>
    <MANUFACTURER>Printopia</MANUFACTURER>
    <DELIVERY><DELIVERY_ID>ONLINE</DELIVERY_ID><DELIVERY_PRICE>0</DELIVERY_PRICE></DELIVERY>
    <MAX_CPC_SEARCH>3</MAX_CPC_SEARCH>
    <MAX_CPC>3</MAX_CPC>
  </SHOPITEM>
</SHOP>
```
Platná cesta kategorie ověřena ve stromu (id 1100 Matematika; alternativa id 1721 `Kultura a zábava | Knihy | Elektronické knihy`, levnější CPC, ale tam jsou jen knihy z knihkupectví). Nabídku v obchodě lze mít jen jednou, takže se vybírá jedna kategorie.

**Ceny (zdroje 5, 13, 14, 16, 25, 27).**

| | Zboží.cz | Heureka |
|---|---|---|
| Registrace | zdarma | zdarma |
| Zobrazení zdarma (free listing) | NE, jen placené, nutný kredit v Seznam Peněžence | ANO, FREE režim, jen 5 až 10 % návštěvnosti, nabídky až na konci fulltextu |
| Min. CPC pro cenu 349 Kč (bez DPH) | Matematika (učebnice) 2,57 Kč, Ostatní učebnice 2,42 Kč, Elektronické knihy 1,86 Kč | Učebnice 2,62 Kč, Knihy 5,29 Kč, fulltext a detail obchodu jednotně 3,49 Kč |
| Skutečná cena kliku | aukce (druhá cena), nejméně ceníkové minimum | ceník podle ceny produktu; `HEUREKA_CPC` ve feedu je nabízená maximální cena, bez tagu se nebiduje |
| Min. dobití / rozpočet | žádná vstupní platba ani minimální útrata; denní rozpočet kampaně min. 30 Kč (u kampaně Nákupy neověřeno) | **499 Kč bez DPH** na jedno dobití, záloha |
| Platba | Seznam Peněženka: karta (kredit týž den), převod 2 až 4 pracovní dny; faktura ke stažení | karta, převod online, bankovní převod (až 3 prac. dny); zálohová faktura e-mailem |
| Dodavatel (CZ) | Seznam.cz, a.s., IČ 26168685 | Heureka Group a.s., IČO 07822774 |

Ceny v Skliku a Heurece jsou bez DPH. Jako neplátce DPH zaplatíme navíc 21 % bez nároku na odpočet (ve smlouvách s českými dodavateli to není problém „zahraniční služby“, DPH dodavatelé odvádějí v CZ).

**Schvalování (zdroje 4, 14, 23).** Zboží.cz: nabídky se ukážou zhruba 4 hodiny po registraci při funkčním feedu a dobitém kreditu; formální schválení do 5 pracovních dnů; propojení s Firmy.cz 1 až 5 pracovních dnů; opravy se hlásí e-mailem, e-shop se znovu neregistruje. Heureka: kontrola údajů do 2 pracovních dnů, párování nabídek na produktové karty po změně URL, názvu nebo kategorie až cca 4 pracovní dny.

**API (zdroj 17).** Fénix API umí čtení obchodů, feedů, kampaní, statistik, diagnostiky položek, recenzí a odpověď na recenzi (`PUT /nakupy/reviews/{id}/reaction`), změnu URL feedu (`PATCH /nakupy/feeds/{feedId}`) a úpravu atributů položek, např. CPC (`PATCH /nakupy/shop-items/`), a kredit (`GET /user/me/credit`). **Vytvoření provozovny přes API neexistuje** (ani v Drak, ani ve Fénixu). Statistiky a API Zboží.cz podle zdroje 12 předpokládají zapnuté standardní měření konverzí.

## Čeho se vyvarovat
- **Slova „kurz“, „e-learning“, „online lekce“, „doučování“ v názvu, popisu i na cílové stránce nabídky.** Vzdělávací kurzy jsou zakázané (zdroj 1) a posuzovatel může PDF sadu zařadit mezi služby nebo kurzy. Psát: sada PDF, sbírka úloh, pracovní listy k tisku, digitální obsah.
- **Tvrdit „oficiální“, „CERMAT“, „zaručeně“, superlativy** (zdroj 2: superlativy, vykřičníky a reklamní slogany v názvu a popisu vedou k banu nabídky). Popis jen o věci, česky, bez HTML, bez emotikonů, bez reklamy na obchod.
- **Cena ve feedu jiná než na webu** (zdroje 1, 3): musí být 349 Kč i na `/koupit`. Testovací cena 1 Kč je jen na `*.vercel.app`, tu nikdy do feedu.
- **Nabídka, kterou nelze koupit přímo** (zdroj 2): `URL` musí vést na `/koupit`, kde je objednávkový formulář, ne na úvodní stránku ani na stránku s ukázkou. Nepřesměrovávat, nevyžadovat e-mail před nákupem.
- **Ukázka zdarma jako druhá nabídka**: cena musí být kladná. Ukázka zůstává jen na webu.
- **Obrázek z webu „Ukázka zdarma“ s logem** (soubor `nahled-ulohy.webp` ukazuje stránku ukázky a nese logo): vyrobit samostatný obrázek sady (zdroj 3: musí být zřejmé, co zákazník dostane, bez vodoznaků, min. 425×440 px, bez černého pozadí).
- **Duplicitní nabídka** (stejný produkt dvakrát nebo ve dvou kategoriích) a **více provozoven pod jedním IČO s podobným sortimentem** (zdroj 14): anoberu.cz (svatby) a printopia.cz (přijímačky) jsou různé obory, ale Sklik doporučuje jednu provozovnu na účet (zdroj 4), anoberu tedy nepřidávat do téhož účtu.
- **Rozdílné IČ** na webu a v registraci (zdroj 2): vždy 17617421, provozovatel MYPIXEL s.r.o. v patičce.
- **Slib „ověřeno zákazníky“ bez dat**: hodnocení Zboží.cz (24 měsíců, skóre až od 4 hodnocení, štítek „Nováček“ 3 měsíce) nejde smazat a zveřejňuje se (zdroj 11). Špatná recenze za 349 Kč u sady PDF bude vidět u každé nabídky.
- **Cena působí draze vedle tištěných sbírek** (náš odhad na základě zdroje 19): na první stránce hledání „přijímačky matematika“ (48 výsledků) je medián 211,50 Kč, 25 z 48 mezi 200 a 400 Kč, jen 10 od 300 Kč. Nabídka za 349 Kč bez recenzí je v nevýhodě u faktoru „cenová výhodnost“ a „kvalita obchodu“ (zdroj 10).
- **Měřicí kód Zboží.cz (SEM nebo standardní konverzní kód) nasadit bez souhlasu a bez úprav textů**: předání e-mailu zákazníka Seznamu vyžaduje oznámení s možností námitky (opt-out) v obchodních podmínkách a v košíku (zdroje 11, 12). Úprava VOP a GDPR je právní změna, schválit s Ondřejem. Pro vstup do Zboží.cz není měřicí kód podmínkou.
- **Dobíjet kredit mimo schválený rozpočet.** Kredit je společný se stávající textovou kampaní Skliku (zůstatek 82,64 Kč, 2026-10-01 17:30). Další kredit do ledna podle CLAUDE.md ne; sonda proto běží z existujícího kreditu a bez nového schválení nic dalšího neplatit.
- **Heureka: slibovat si FREE režim.** Cca 90 až 95 % přístupů jde do PPC (zdroj 26).
- **Digitální obsah v právu** (zdroj 33): před nákupem uvést technické požadavky (PDF, prohlížeč, tiskárna), způsob dodání, aktualizace a podporu; odstoupení bez udání důvodu do 14 dnů je v našich VOP bez vzdání se práva (to nemění žádný srovnávač). Rozpor „zboží“ a „digitální obsah“: v Zboží.cz je to zboží ke stažení (`ONLINE`), ve VOP digitální obsah (§ 2389a a násl.); v popisu nenazývat „služba“.

## Jak na to
Zboží.cz (doporučeno), kroky v pořadí:

1. **Claude**: obrázek sady (např. 1200×1200 px, světlé pozadí, nahled 14 PDF, bez „Ukázka zdarma“, logo Printopia jen malé jako výrobce) do `printopia/public/zbozi-sada.png`.
2. **Claude**: route handler `GET /feed/zbozi.xml` v `printopia/src/app` (cena z `src/lib/config.ts`, `PRICE`), jedna položka podle příkladu, hlavička `Content-Type: application/xml; charset=utf-8` a `Last-Modified`; test v `npm run test:e2e` (validní XML, cena 349, URL vrací 200 a obsahuje formulář, žádná diakritika v URL, v textu žádné slovo „kurz“); nasadit.
3. **Claude**: ověřit feed ve validátoru Zboží.cz (https://napoveda.sklik.cz/reklamy/xml-feed/validator/ nebo stránka v zdroji 6) a zapsat výsledek.
4. **Claude**: v obsahu stránky `/koupit` a patičky ověřit, že jsou: provozovatel, IČO, e-mail, VOP, ochrana údajů, ČOI, cena, popis nákupu digitálního obsahu a že je tam jedna nabídka. Přidat telefon jen pokud ho firma má (Zboží.cz stačí e-mail; Heureka telefon vyžaduje).
5. **Ondřej** (jen schválení, právo a finance): 1) souhlas s veřejným Detailem obchodu a veřejnými recenzemi na Zboží.cz a se záznamem MYPIXEL s.r.o. na Firmy.cz; 2) souhlas utratit z existujícího kreditu (82,64 Kč bez DPH) na prokliky ze Zboží.cz místo dalšího dobíjení; 3) souhlas s textem opt-out jen pokud se později nasadí měření (krok 9).
6. **Ondřej** (přihlášení a odeslání formuláře, nejde automatizovat, 3 až 5 minut): přihlásit se na https://www.sklik.cz účtem ondrej@mypixel.cz (Sklik účet 1183445), Nastavení účtu, Provozovny, Přidat provozovnu (nebo v patičce Zboží.cz „Přidat obchod“). Vložit hodnoty, které Claude připraví ke zkopírování: IČ `17617421`; obchodní název `Printopia`; URL `https://printopia.cz`; URL feedu `https://printopia.cz/feed/zbozi.xml`. Odsouhlasit Smluvní podmínky pro inzerenty (už je souhlasil při zřízení Skliku, formulář může chtít potvrdit). Pokud Firmy.cz požádá o ověření zápisu (kód e-mailem, poštou nebo telefonem), potvrdit.
7. **Claude** po registraci: sledovat `https://printopia.cz/api/stats` (zdroj `src=zbozi`), diagnostiku nabídky přes Fénix `GET /nakupy/diagnostics/item`, případné zamítnutí opravit ve feedu a napsat na sklik@firma.seznam.cz, že je opraveno (pro opravu se neregistruje znovu).
8. **Claude**: CPC řídit přes `MAX_CPC_SEARCH` ve feedu (začít na 3 Kč, strop 4 Kč) nebo přes Fénix `PATCH /nakupy/shop-items/`; kampaň Nákupy se ve Skliku vytvoří po propojení účtů (zdroj 15) a průvodce po registraci nabízí její založení hned (zdroj 4). Stav a denní rozpočet pak číst přes Fénix `GET /nakupy/campaigns/` a Sklik API; denní rozpočet min. 30 Kč platí pro kampaně obecně (zdroj 16), u Nákupů neověřeno.
9. **Později, po prvních prodejích** (volitelné): standardní konverzní kód nebo SEM na stránce `/objednavka/[id]` + serverová část (předání ID objednávky), aby šlo sbírat „Ověřený zákazník“ a používat API Zboží.cz. Vyžaduje odsouhlasit smluvní podmínky měření (Ondřej, v administraci Centra prodejce), tajný klíč do env (sensitive), úpravu GDPR a VOP (opt-out věta ze zdroje 11) a souhlas se cookies pro skript. Do té doby měřit jen přes `utm_source=zbozi` v naší vlastní analytice.
10. **Vyhodnocení**: po 14 dnech `plan/zbozi-vyhodnoceni.md` (zobrazení, prokliky, objednávky, útrata, důvody zamítnutí) a rozhodnutí pokračovat, zastavit, nebo přidat Heureku.

Heureka (až po výsledku Zboží.cz), kroky:
1. **Claude**: použít stejný feed rozšířený o povinné `ITEM_ID`, `PRODUCT`, `URL`, `PRICE_VAT` a `DELIVERY` `ONLINE` (zdroj 28 `ONLINE` doručení zná), `HEUREKA_CPC`; web musí mít český telefon, reklamační řád, ochranu údajů, ČOI (zdroj 24).
2. **Ondřej**: vytvořit uživatelský účet na heureka.cz (e-mail a heslo, ověření e-mailu), Přidat obchod: IČO (údaje se doplní z rejstříku), kontakt, název, URL, logo (JPG/PNG do 300 kB, min. 320×100 px), URL feedu, e-mail pro zákazníky. Kontrola do 2 pracovních dnů, start ve FREE režimu zdarma.
3. **Ondřej** (finance): PPC jen po dobití min. 499 Kč bez DPH; schválit až s čísly ze Zboží.cz.

## Odhad nákladů a návštěv

Měřeno 2026-10-01 (jisté):
- Seznam zobrazuje skupinu „Nabídky ze Zboží.cz“ (až 29 nabídek, max. 2 od jednoho obchodu) u dotazů s produktovým slovem: „cvičebnice matematika 9. třída“ (22 nabídek, 59 až 159 Kč), „sbírka přijímačky matematika kniha“ (34 nabídek, 77 až 416 Kč), „přijímačky v pohodě matematika“ (29 nabídek, 79 až 460 Kč). U dotazů „přijímačky matematika“, „cermat testy“, „příprava na přijímačky“, „přijímačky nanečisto“ se skupina nezobrazila (v HTML odpovědi, načítání skriptem nevyloučeno).
- Hledanost těchto produktových dotazů ve Skliku (jen Seznam, ø 2 měsíce, 2026-10-01): „přijímačky v pohodě“ 12, „přijímačky v pohodě matematika“ 0, „sbírka přijímačky matematika“ 0, „cvičebnice matematika 9. třída“ 0, „přijímačky matematika kniha“ 0 (0 znamená pod prahem Skliku). Dotaz s objemem „cermat testy“ (ø 728) skupinu Nákupů nemá.
- Konkurence ve Zboží.cz (zdroj 19, ceny od, počet obchodů): Přijímačky v pohodě 9 Matematika 2027 (Taktik) 359 Kč, 6 obchodů; Přijímačky 9 Matematika 2026 (Taktik) 374 Kč, 8; Přijímací zkoušky nanečisto 2027 (Computer Media) 197 Kč, 13; Testy 1 Průvodce 2027 (Didaktis) 189 Kč, 14; Testy 2 Nácvik 2027 (Didaktis) 160 Kč, 11; Přijímací zkoušky na SŠ Matematika (Scholastik) 342 Kč, 14; Testy z matematiky 2026 (Kapičková) 239 Kč, 18; Ještě není pozdě: Přijímačky s Robinem 290 Kč, 20 (e-kniha 278 Kč, 4 obchody: Dobre-knihy.cz, KNIHY DOBROVSKÝ, Palmknihy.cz, Luxor.cz). Prodejci v karuselu: Luxor.cz, KNIHY DOBROVSKÝ, Dobre-knihy.cz, KamPoMaturite.cz, UčebniceMapy.cz (793 hodnocení za 2 roky, 98 %), Reknihy.cz, MEGAKNIHY.cz, Alza.cz, SEVT, AUKRO.CZ. Samostatný digitální produkt k přijímačkám za cenu sbírky jsem ve výsledcích nenašel (jen e-knihy z knihkupectví).
- Náklad na proklik: 1,86 až 2,57 Kč bez DPH jako minimum (zdroj 5), s DPH 2,25 až 3,11 Kč. Za zůstatek 82,64 Kč lze koupit 32 až 44 prokliků při ceníkovém minimu (méně při vyšší nabídce v aukci).

ODHAD (bez dat, pouze úvaha):
- Návštěvy z Nákupů pro naši nabídku: 10 až 100 prokliků za měsíc v sezóně (listopad až duben), mimo sezónu méně. Důvody: produktové dotazy mají na Seznamu skoro nulovou hledanost, hlavní tok bude z procházení kategorie Matematika na Zboží.cz, kde nemáme recenze ani historii.
- Konverze prokliku na prodej 1 až 3 % (cena nad mediánem, bez recenzí; ODHAD). Při CPC 2,57 Kč je to 86 až 257 Kč na jednu objednávku bez DPH (104 až 311 Kč s DPH), proti tržbě 349 Kč. Při konverzi 1 % se sotva zaplatí, od 2 % je to ziskové (bez práce a poplatků); bod zlomu je cca 112 prokliků na objednávku při 3,11 Kč s DPH.
- Tržby ze sondy: 0 až 3 objednávky za měsíc, tedy 0 až cca 1 000 Kč. Strop placeného kanálu je ve stejném řádu jako u Skliku (2 až 4 tis. Kč za sezónu), ne řešení škálování.
- Čas: Claude 1 až 2 h (feed, obrázek, test, nasazení). Ondřej 10 až 15 minut celkem (schválení, přihlášení a formulář). Nabídka se zobrazí zhruba 4 hodiny po registraci (zdroj 4), první proklik 1 až 5 dnů po registraci (ODHAD podle objemu), formální ověření do 5 pracovních dnů.
- Heureka (ODHAD): FREE režim 5 až 10 % návštěvnosti nabídek (zdroj 26) a bez prokliků, tedy skoro nic; PPC min. 499 Kč kreditu na dobití a CPC 2,62 Kč (učebnice) nebo 3,49 Kč (fulltext), 499 Kč = cca 140 až 190 prokliků, což přesahuje zbývající rozpočet firmy (~350 Kč).

## Kontrolní seznam
Odškrtnout až po auditu (u každého bodu uvést zdroj nebo výsledek testu). Kampaň se nespouští před odškrtnutím.

- [x] Hledanost a konkurence: použít `plan/hledanost-printopia.md` a živá hledání z tohoto souboru; závěr: sonda Zboží.cz jen z existujícího kreditu, ne škálovat (Seznam sám produkt neuživí).
- [ ] Ondřej schválil právo: veřejný Detail obchodu a recenze na Zboží.cz, záznam MYPIXEL s.r.o. na Firmy.cz, přihlášení ke Smluvním podmínkám inzerentů (kroky v oddílu Jak na to, bod 5).
- [ ] Ondřej schválil finance: prokliky jen z existujícího kreditu Skliku (82,64 Kč bez DPH k 2026-10-01), žádné dobíjení; Heureka ne bez nového schválení (min. 499 Kč).
- [x] Obrázek sady `zbozi-sada.png` min. 425×440 px, bez „Ukázka zdarma“, bez vodoznaků, ukazuje, co zákazník dostane.
- [x] `GET /feed/zbozi.xml` nasazen na produkci, validní XML (UTF-8, `xmlns="http://www.zbozi.cz/ns/offer/1.0"`), 1 `SHOPITEM`, `PRICE_VAT` = 349 = cena na `/koupit`, `DELIVERY` `ONLINE` s cenou 0, kategorie id 1100 podle stromu `categories.json`.
- [x] `URL` v feedu vede na `/koupit`, vrací 200, nepřesměrovává, bez diakritiky, s `utm_source=zbozi&utm_medium=cpc`, na stránce je jediná nabídka a objednávkový formulář.
- [x] Text nabídky bez slov „kurz“, „e-learning“, „doučování“, „oficiální“, „CERMAT“, bez superlativů, vykřičníků, HTML a emotikonů; přečten jako korektor (pravidlo Texty).
- [x] Web má provozovatele, IČO, e-mail, VOP s 14 dny na vrácení a ČOI, ochranu údajů, informace o digitálním obsahu (technické požadavky, dodání); název subjektu „Printopia“ (max. 24 znaků) je ověřitelný z domény a webu.
- [x] E2E test feedu v `npm run test:e2e` je zelený (kontrola přes exit code).
- [ ] Ondřej provedl registraci provozovny (IČ, název, URL, URL feedu); kampaň Nákupy ve Skliku se vytvořila sama a je spuštěná.
- [ ] Diagnostika nabídky ve Skliku/Centru prodejce bez chyb; při zamítnutí opraveno a oznámeno na sklik@firma.seznam.cz.
- [ ] Měření: `src=zbozi` v `/api/stats` sleduje zobrazení stránky, začátek objednávky a nákup (trychtýř, důvody „proč ne“); po 14 dnech `plan/zbozi-vyhodnoceni.md`.
- [ ] Měřicí kód Zboží.cz (SEM nebo standardní) jen po schválení úpravy VOP a GDPR (opt-out) a s tajným klíčem v env (sensitive).
- [ ] Heureka: rozhodnout až po vyhodnocení Zboží.cz; předtím doplnit český telefon na web, ověřit obchodní podmínky Heureky po přihlášení (zdroj 30) a seznam zakázaného zboží.
