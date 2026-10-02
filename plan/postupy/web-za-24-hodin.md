# Web za 24 hodin: postupy, rizika a test poptávky přes Bazoš a Sbazar

Cílová skupina: hledá a **platí** majitel malé firmy nebo OSVČ s IČO (řemeslník, kadeřnictví, autoservis, konzultant), **používají** web jeho zákazníci. Prodej jen subjektům s IČO (B2B), jinak by platila spotřebitelská pravidla. Zpracováno 2026-10-02 (13:40 až 14:10 pražského času), jen výzkum: nic nezaloženo, nic nekoupeno, nikde jsem se neregistroval, žádný inzerát nepodán. Co je odhad, je označeno ODHAD, co jsem nemohl ověřit, NEOVĚŘENO. Tabulka konkurentů a čísla z portálů: `plan/konkurence-web-za-24-hodin.md`.

## Závěr

- **Test přes inzerát jde udělat za ~150 Kč a bez stavby**, ale 72 hodin je krátko. ODHAD: aspoň jeden dotaz za 72 h ≈ 60 % (rozsah 26 až 93 %), aspoň jedna **závazná** poptávka (zájemce s IČO přijme cenu a pošle podklady nebo zálohu) ≈ 20 až 25 % (rozsah 6 až 60 %). `plan/akce.md` uvádí 40 %, podle čísel z portálů vychází spíš polovina.
- Trh je plný a levný (medián Bazoše 3 999 Kč, 7 ověřených konkurentů slibuje „24 hodin“, nejpřímější WebDo24 má stejný model za 9 900 Kč). Kupující web na Bazoši nepoptávají a ve 100 nejhledanějších výrazech Služeb web není.
- **Jeden inzerát dá ODHADEM ~0,5 zakázky měsíčně (~2 300 Kč tržeb, náklad 392 Kč)**. Cíl A z `plan/alternativy.md` (≥ 10 000 Kč zisku měsíčně) tedy z Bazoše a Sbazaru samotných nevychází; potřeba ~5× víc kontaktů z dalších kanálů. Test se hodí jako levná sonda „má to vůbec někdo zájem“, ne jako důkaz škálovatelnosti.
- Formálně: `plan/verdikt.py` Bazoš spočítat neumí (bere cenu kliku ze Skliku, 59,6 Kč, ne cenu za zobrazení ~2 Kč (392 Kč / ~185 zobrazení)). Spuštění potřebuje řádek „Výjimka schválená Ondřejem: <důvod> (<datum>)“ v `plan/hledanost-alt-web.md`, nebo úpravu skriptu.

## Zdroje
Všechny navštíveny nebo staženy 2026-10-02. Konkurenti viz `plan/konkurence-web-za-24-hodin.md`.

Portály:
1. Bazoš, podmínky (zákazy, ověření, řazení, IČO u podnikatelů, ochrana údajů): https://www.bazos.cz/podminky.php
2. Bazoš, nápověda (poukázka 49 Kč, topování, maximální počty, doba 2 měsíce): https://www.bazos.cz/napoveda.php
3. Bazoš, Služby: https://sluzby.bazos.cz/ , rubrika IT, webdesign https://sluzby.bazos.cz/it/ , poptávka https://sluzby.bazos.cz/inzeraty/poptavka/ , nejvyhledávanější výrazy https://sluzby.bazos.cz/mapa-search.php , reklama https://www.bazos.cz/reklama.php
4. Sbazar, WWW služby: https://www.sbazar.cz/96-www-sluzby ; veřejné JSON rozhraní webu `https://www.sbazar.cz/api/v1/items/search?category_id=96&limit=60&offset=0&sort=-date` (3 čtecí dotazy, žádný zápis)
5. Sbazar, pravidla: https://o-seznam.cz/napoveda/sbazar/jak-inzerovat/pravidla-inzerce-sbazar/ ; topování: https://o-seznam.cz/napoveda/sbazar/jak-inzerovat/zvyhodneni-topovani-inzeratu/ ; smluvní podmínky (čl. 4.9, 4.12, 4.24, 7.1): https://o-seznam.cz/napoveda/sbazar/jak-inzerovat/smluvni-podminky/smluvni-podminky-sbazar-a-v-mobilni-aplikaci/ ; dotazy: https://o-seznam.cz/napoveda/sbazar/jak-inzerovat/dalsi-uzitecne-dotazy/
6. Firmy.cz, zdarma zápis: https://napoveda.firmy.cz/faq/je-profil-na-firmy-cz-bezplatny/

Hosting a cena webu:
7. Vercel, Terms of Service (čl. 4 Hobby jen nekomerční, čl. 10.1 DPA, čl. 11 zákaz „sublicense, resell, … or make the Services available to any third party“): https://vercel.com/legal/terms
8. Vercel, Fair Use Guidelines (komerční použití = i „receiving payment to create, update, or host the site“, vyžaduje Pro nebo Enterprise; aktualizováno 2026-09-14): https://vercel.com/docs/limits/fair-use-guidelines
9. Webnode blog, ceny webu (2026-08-21): https://www.webnode.com/cs/blog/kolik-stoji-webove-stranky/
10. Webglobe, kolik stojí web (2026-05-04): https://www.webglobe.cz/blog/tvorba-webu
11. ČSÚ, podíl firem s webem (2025): https://csu.gov.cz/ict-v-podnicich

Právo:
12. Rozsudek Městského soudu v Praze č. j. 10 C 13/2023-16 (AI obrázek není autorské dílo, pravomocný): https://msp.gov.cz/documents/14569/1865919/10C_13_2023_10/108cad3e-d9e8-454f-bfac-d58e1253c83a ; shrnutí https://www.epravo.cz/top/clanky/mestsky-soud-v-praze-o-umele-inteligenci-a-autorskem-pravu-117318.html
13. Právní rámec tvorby webů (smíšená smlouva, § 61 autorského zákona, licence): https://www.holec-advokati.cz/cs/pravni-ramec-tvorby-webovych-stranek/ ; co nezapomenout ve smlouvě: https://muj-pravnik.cz/smlouva-vytvoreni-webove-stranky/ ; licenční smlouva (§ 2358 a násl. OZ): https://www.businessinfo.cz/navody/vzor-ppbi-licencni-smlouva/
14. Cookies, § 89 odst. 3 zákona o elektronických komunikacích, opt-in od 2022: https://www.pravniprostor.cz/clanky/mezinarodni-a-evropske-pravo/souhlasy-s-cookies-pristupy-k-ochrane-osobnich-udaju
15. Identifikační údaje na webu podnikatele (článek z 2010 o § 13a obchodního zákoníku, dnes občanský zákoník, NEOVĚŘENO číslo paragrafu): https://www.podnikatel.cz/clanky/povinne-identifikacni-udaje-na-firemnim-webu/
16. ÚOOÚ, vzor informace o zpracování údajů pro web: https://uoou.gov.cz/media/informace-o-zpracovani-osobnich-udaju/7-informace-o-zpracovani-osobnich-udaju-web-vcetne-odberu-novinek.pdf
17. ARES, ověření IČO: https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/<IČO>

## Odhad za 72 hodin (číselně)

Vstupy a předpoklady (každý je ODHAD, kromě měřených zobrazení konkurence):
- **Zobrazení Bazoš s TOP (1 až 3×, 9. až 11. místo z 99)**: 40 až 90 za 72 h. Měřeno: 6 čerstvých inzerátů se 7× TOP mělo 41 až 95 zobrazení po 0,7 až 4,5 dne (věk z pořadových ID inzerátů, ±0,5 dne). Bez TOP: 20 až 35 (inzeráty staré 2,6 až 4,6 dne mají 20 až 35).
- **Zobrazení Sbazar**: nezveřejňuje se. ODHAD 15 až 40 za 72 h (polovina Bazoše, bez dat; nabídka je 2 týdny mezi prvními 60).
- **Zobrazení → dotaz (zpráva nebo zobrazení čísla)**: 0,5 až 2 %. PŘEDPOKLAD bez zdroje (žádná veřejná data o konverzi nenalezena): nákup za tisíce Kč, rubrika plná nabídek konkurentů, web není mezi 100 nejhledanějšími výrazy Služeb, na Bazoši nikdo web nepoptává.
- **Dotaz → závazná poptávka**: 20 až 35 % (`plan/alternativy.md` počítá 20 až 30 %).
- Součet za 72 h: 55 až 130 zobrazení, dotazů 0,3 až 2,6 (střed 0,9), závazných poptávek 0,06 až 0,9 (střed 0,25). Poissonovo rozdělení: P(≥ 1 dotaz) = 1 − e^−λ = **60 % (26 až 93 %)**, P(≥ 1 závazná) = **22 % (6 až 60 %)**.
- **Měsíčně, 1 inzerát se 7× TOP** (392 Kč: 49 vložení + 343 TOP): zobrazení ~170 až 200 za první 4 týdny (měřeno u 4 inzerátů se 6 až 7× TOP, 25 až 49 dnů staré, 168 až 204 zobrazení), dotazů 0,9 až 4, zakázek 0,2 až 1,4, tržby při ø 4 490 Kč ~800 až 6 300 Kč plus správa 290 Kč/měs. Střed ~0,5 zakázky, ~2 300 Kč.
- **Jak číst výsledek po 72 h:** 0 dotazů při ≥ 80 zobrazeních je jen slabé NE (i při skutečné míře 1 % vyjde nula dotazů s pravděpodobností ~45 %), proto prodloužit na 7 dní, ne zavřít. ≥ 2 dotazy = pokračovat. ≥ 1 závazná poptávka = sonda ANO. Do 72 h se počítá i rychlost odpovědi: B2B zákazníci odpovídají pomalu, po 72 h bývá závazných poptávek méně než po týdnu.

## Typické námitky a co přesvědčí
Zdroj: texty a ceníky konkurentů (jejich obrana a argumenty), ne výzkum zákazníků. NEOVĚŘENO měřením.

1. **„AI web je šablona nebo amatérská práce.“** Inzeráty MartinTusek a MartinGondek (5 z 47 inzerátů) na tom staví. Přesvědčí: živá ukázka, kontrola člověkem, vlastnictví webu, záruka vrácení peněz. Nelhat „bez AI“.
2. **„Kdo jste, jaké máte reference?“** Konkurence uvádí „120+“, „400+“, „4 roky praxe“, ukázky s časem dodání (WebDo24). Přesvědčí: 3 živé vzory označené jako ukázky, IČO a provozovatel, vrácení peněz. Žádné vymyšlené recenze.
3. **„Nechci platit předem.“** Platba až po schválení náhledu je standard (WebDo24, Kdo mi udělá web, chciweblevne.eu, Pupík, Gondek, atyco.cz). Přesvědčí: náhled před platbou, platba QR převodem až po schválení.
4. **„Kolik to bude stát celkem za rok a co je navíc?“** Konkurence mluví o „bez skrytých poplatků“, málokdo uvádí provoz po 1. roce (3 z 47). Přesvědčí: cena celkem za 12 měsíců s doménou, hostingem a formulářem, správa 290 Kč/měs. nepovinně.
5. **„Kdo mi to bude měnit?“** Podstatzký slibuje úpravy do 24 h (500 Kč/měs.), Weblik 700 Kč za hodinu úprav, FastSite podporu do 24 h. Přesvědčí: počet změn měsíčně v ceně správy.
6. **„Najde mě Google?“** SEO uvádí 30 z 47 inzerátů. Přesvědčí: základní SEO, profil na Googlu a Firmy.cz v ceně, **bez slibu pozice**.
7. **„Komu web patří, můžu odejít?“** Gondek: „100% vlastnictví, žádné pronájmy“, FastSite: web běží na jejich licenci. Přesvědčí: doména na jméno klienta, předání zdrojového kódu na vyžádání.

## Právní a rizikové body (B2B)
Není to právní porada. U každého je napsáno, co z toho plyne, a co schvaluje Ondřej (právo a finance mají jeho veto).

1. **Nabídka a smlouva.** Smlouva o vytvoření webu je smíšená (dílo + licence, § 61 autorského zákona, § 2358 a násl. občanského zákoníku, zdroj 13). Nabídka musí obsahovat: zhotovitele (MYPIXEL s.r.o., IČO 17617421, sídlo), přesný rozsah (1 stránka, počet sekcí, počet kol úprav), **cenu konečnou bez DPH** („nejsme plátci DPH“), termín od kompletních podkladů a úhrady zálohy, způsob platby (QR převod na firemní Fio účet), co je vyloučeno, správu 290 Kč/měs. a výpověď, platnost nabídky, záruku vrácení peněz. K schválení: **text obchodních podmínek a smlouvy, limit odpovědnosti (např. do výše ceny díla), záruka vrácení peněz (rozsah a lhůta)**.
2. **Jen subjekty s IČO.** Před přijetím objednávky ověřit IČO v ARES (zdroj 17). Spotřebitel (fyzická osoba bez IČO) = jiný režim (14 dní na odstoupení, informační povinnosti), v testu nesmlouvat.
3. **Co smíme slibovat.** Termín (od podkladů), cenu, rozsah, vrácení peněz, předání. **Nesmíme:** pozici v Google nebo počet poptávek, „bez AI“, „ručně psaný kód“, vymyšlené reference a hodnocení, „unikátní autorský návrh“ bez výhrad, „zdarma“ jako lákadlo bez jasné podmínky. Klamavé jednání je nekalá soutěž (§ 2976 a násl. občanského zákoníku, NEOVĚŘENO znění). Pro tvrzení „AI navrhuje, člověk kontroluje“ musí platit, že kontrola skutečně proběhla (Claude před odesláním kontroluje a odpovídá).
4. **Autorská práva.** Web = vzhled, texty, fotky, kód. Rozsudek (zdroj 12): AI obrázek není autorské dílo, prompt je jen námět, autorem je jen fyzická osoba. Důsledek: **neslibovat „autorská práva přejdou na vás“ na AI části**. Ve smlouvě: licence k užití webu (nevýhradní, bez časového a územního omezení, bez práva převodu na třetí osobu mimo prodej firmy, cena v odměně), závazek nepoužít týž návrh pro jiného klienta, klient prohlašuje, že má práva k podkladům (loga, fotky, texty), my zajistíme práva k fotkám (Unsplash: licence zdarma i komerčně, viz `CLAUDE.md`), fontům a ikonám pod otevřenými licencemi. **Zdrojový kód** předat na vyžádání.
5. **Odpovědnost za obsah.** Klient odpovídá za pravdivost svých údajů a podkladů, my za vady díla a dodržení termínu. AI nesmí vymýšlet ceny, certifikace, adresy, otevírací dobu ani reference klienta; **každý údaj schvaluje klient písemně e-mailem před spuštěním**.
6. **Identifikační údaje na webu klienta.** Podnikatel musí na webu uvést jméno nebo firmu, sídlo, IČO a zápis v rejstříku (zdroj 15: původně § 13a obchodního zákoníku, dnes občanský zákoník, NEOVĚŘENO číslo paragrafu a výše pokuty). Patička každého webu to musí mít podle údajů z ARES.
7. **GDPR u formuláře.** Klient je **správce**, my při hostingu a přeposílání zpráv **zpracovatel** (čl. 28 GDPR), tedy smlouva o zpracování jako příloha. Podprocesory: Vercel (DPA je součástí Terms, čl. 10.1; sídlo v USA, předávání mimo EU ověřit v jeho DPA), případně Resend. **Nejméně rizikové řešení:** jednoduchý web bez našeho serveru, kontakt přes `mailto:` a telefon; formulář jen s odesláním e-mailem bez ukládání, v patičce informace o zpracování podle vzoru ÚOOÚ (zdroj 16). K schválení: **role zpracovatele a text smlouvy o zpracování**.
8. **Cookies.** Od 2022 opt-in pro vše mimo technické (§ 89 odst. 3 zákona o elektronických komunikacích, zdroj 14). Základ: **žádná analytika ani marketingové skripty, fonty a knihovny z vlastního hostingu**, pak žádná cookie lišta není potřeba. Google Analytics, Meta Pixel a vložené mapy jen jako příplatek s lištou.
9. **Hosting na Vercelu (Pro) pro třetí osoby, RIZIKO.** Fair Use (zdroj 8) výslovně počítá „receiving payment to create, update, or host the site“ za komerční použití a to je povolené na Pro (Hobby jen nekomerčně, čl. 4). Terms čl. 11 (i) však zakazuje „sublicense, resell, … or otherwise commercially exploit or make the Services available to any third party“ a licence v čl. 2 je „for your internal business or personal purposes according to the service capacity of your account“. Výklad, zda hostování klientských webů je přeprodej Vercelu, nemám potvrzený. Rozumný postup: **neprodávat „Vercel hosting“, ale „provoz a správu webu“, který děláme my** (klient nedostane přístup do Vercelu, platí za službu správy), mít plán B (statický export ke klientovi na jeho hosting, doménu mu předat), a požádat Vercel support o písemné potvrzení. Trial Pro nepoužívat (tam smí Vercel trénovat AI na obsahu, na placeném Pro ne, čl. 3). Také ověřit, kdo Vercel Pro platí: pokud MYPIXEL s.r.o., jde o zahraniční placenou službu (pravidlo firmy: riziko identifikované osoby k DPH, `CLAUDE.md` říká „k dispozici zdarma“). K schválení: **přijetí rizika čl. 11 (i) nebo písemné potvrzení Vercelu**.
10. **Doména.** Registrovat na klienta jako držitele (u českého registrátora, ~170 až 230 Kč/rok podle Webliku, Webu za pár kaček a Webglobe, viz `plan/konkurence-web-za-24-hodin.md`), ne na nás. Jinak jsme přeprodejce domén a ručíme za spory.
11. **Nevyžádané nabídky.** E-maily a SMS firmám jen se souhlasem (zákon 480/2004 Sb., § 7, NEOVĚŘENO znění). Zůstat u inzerce a odpovědí na příchozí dotazy.
12. **Inzerce na Bazoši.** Název a IČO na konci inzerátu (zdroj 1, nařízení EU 2019/1150), jinak riziko smazání **bez vrácení 49 Kč**. Přestože konkurence IČO neuvádí (0 z 47), my ho uvádět budeme. K schválení: **veřejný telefon a e-mail v inzerátu** (inzerát ukáže číslo po kliknutí, zprávu může poslat jen ověřený uživatel).
13. **Finance.** Výdaje: Bazoš 49 Kč vložení + 49 Kč za každý TOP (1 až 3× = 98 až 196 Kč celkem; 7× = 392 Kč), Sbazar 0 Kč (TOP 29 Kč, volitelně). Test navržený v postupu: vložení + 2× TOP = **147 Kč** ze zbývajících 700 Kč. Příjmy jen na firemní Fio účet, faktura bez DPH.

## Čeho se vyvarovat
- **Slibovat „24 hodin“ bez definice.** Termín počítat od kompletních podkladů a platby; držet nejvýš 3 rozpracované weby najednou, jinak termín nestihneme (WebDo24 sám ukazuje „3/5 míst“).
- **Tvrdit „bez AI“, „ručně psaný kód“, „vlastní autorská práva na AI návrh“.** Je to pravda jen zčásti a klamavé (body 3 a 4). Naopak nemlčet: konkurence AI zmiňuje.
- **Vymyšlené reference, počty webů, recenze.** Ukázky označit „vzor (ukázka)“, nikdy jako zakázku. Použít jen vlastní vzorové texty, fotky z Unsplash, žádná cizí loga a firmy bez souhlasu.
- **Chyby v inzerátu, kvůli kterým se smaže bez vrácení poplatku:** hvězdičky, vykřičníky, emotikony a VELKÁ PÍSMENA (Bazoš zakazuje nadměrné hvězdičky a vykřičníky, Sbazar velká písmena a emotikony), seznam klíčových slov, duplicitní inzeráty, cena „Dohodou“, „V textu“ nebo 1 Kč (19 z 47 konkurentů nemá číselnou cenu), chybějící IČO. Pole Cena vyplnit číslem. Odkaz na vlastní web do inzerátu nedávat (zákaz „webové stránky a loga firmy“ je nejasný), ukázky vložit jako fotky (screenshoty), „nabízený produkt“ je dovolený.
- **Přijímat objednávky bez IČO, e-shopy, rezervační systémy s platbami, zdravotnictví a jiné regulované obory.** První verze nabídky je jednostránkový web pro lokální služby.
- **Nevyžádané oslovování.** Jen příchozí dotazy.
- **Předat klientovi přístup do Vercelu nebo prodávat Vercel jako hosting**, používat Hobby plán nebo trial Pro pro klientské weby.
- **Zdarma náhled bez limitu.** Jeden náhled na zájemce, jen po ověření IČO v ARES, jen jako screenshot a neindexovaná adresa s nápisem „náhled“, zdrojový kód a vlastní doména až po zaplacení.
- **AI text o službách klienta odeslat bez schválení klientem.**
- **Měřit jen „zakázky“.** Bez zobrazení, dotazů a důvodů „proč ne“ nebude po 72 h jasné, co zlepšit (pravidlo Metriky v `CLAUDE.md`).
- **Zavírat test po 72 h při nule dotazů** bez ohledu na počet zobrazení (viz výpočet výše).

## Jak na to (postup: nejdřív ověřit poptávku, až potom stavět)
0. **Schválení Ondřeje** (jen autorizace a schválení, žádná ruční práce mimo ni): „ano, test webu“, výjimka z verdiktu, výdaje ≤ 147 Kč, právní body 1, 4, 7, 9, 12, přihlášení a ověření účtů (níže).
1. **Příprava, Claude, 0 Kč, ~2 až 3 hodiny, nic z toho se neprodává:** jeden vzor jednostránkového webu (jedno odvětví, např. kadeřnictví nebo autoservis) jako screenshoty PC a mobil, ceník, text nabídky, návrh smluvních podmínek, e-mailová odpověď s pevnou cenou, tabulka „co dostanete, co ne“. Další vzory teprve po prvním dotazu. Před zveřejněním designový průzkum `plan/design-web-za-24-hodin.md` (CLAUDE.md, prodejní web) a korektura textů (pravidlo Texty).
2. **Inzerát (Bazoš Služby, rubrika IT, webdesign, a Sbazar WWW služby), kostra:** nadpis do ~60 znaků (např. „Web pro živnostníka za 3 990 Kč, hotový do 24 hodin“, bez emotikonů), pole Cena 3 990, v textu: komu je určen, co je v ceně (jednostránkový web, mobil, doména a hosting na 12 měsíců, formulář, profil na Google), co není (e-shop, rezervace, texty o službách vymýšlet nebudeme), **platba až po schválení náhledu**, termín od podkladů, kontakt a **na konci název a IČO**. Sbazar: totéž bez emotikonů a velkých písmen, 1× TOP za 29 Kč jen volitelně. Obě nabídky různým textem (duplicity jsou zakázané).
3. **Měření automaticky, ne ručně:** dva různé e-maily pro kanály (např. bazos@ a sbazar@ na firemní doméně) a otázka v odpovědi „kde jste nás našli“. Skript (curl) 2× denně přečte „Zobrazeno N x“ u našeho inzerátu a zapíše do tabulky: zobrazení, dotaz, nabídka, náhled, záloha, zaplaceno, důvod „proč ne“. Do `plan/web-za-24-hodin-vyhodnoceni.md` po testu zapsat poučení pro další RUN.
4. **„Poptávka na vzor“:** zájemce pošle 3 věty o podnikání a obor, do 24 h dostane **náhled svého webu (vzor)** a pevnou cenu; měří se konverze dotaz → náhled → záloha. Odpověď na dotaz do 1 hodiny (Claude připraví odpověď, odesílá firemní e-mail).
5. **Rozhodnutí po 72 h podle čísel** (viz „Odhad“): ≥ 1 závazná poptávka = sonda ANO, ≥ 2 dotazy = pokračovat do 7 dní, 0 dotazů při ≥ 80 zobrazeních = prodloužit na 7 dní a změnit text, potom vyhodnotit.
6. **Stavět proces až po první závazné poptávce:** objednávkový formulář a QR platba s párováním Fio (hotové komponenty v `web/` a `printopia/`), šablona webu, správa za 290 Kč/měs. Do té doby jen inzerát, vzor a odpovědi.

## Kontrolní seznam
Průzkum (hotovo v tomto dokumentu):
- [x] Konkurence zmapována, 22 konkurentů s cenou, rozsahem, termínem a důvěryhodností (`plan/konkurence-web-za-24-hodin.md`).
- [x] Pravidla a poplatky Bazoše a Sbazaru přečteny z oficiálních stránek.
- [x] Počty inzerátů, ceny, zobrazení a pořadí v rubrice změřeny 2026-10-02.
- [x] Podmínky Vercelu pro hostování cizích webů přečteny (Terms čl. 11, Fair Use) a riziko popsáno.
- [x] Odhad poptávky za 72 h spočítán s označenými předpoklady.

Než se cokoli spustí:
- [ ] Ondřej: „ano, test webu“ a řádek „Výjimka schválená Ondřejem: <důvod> (<datum>)“ v `plan/hledanost-alt-web.md`, nebo upravený `plan/verdikt.py` (cena zobrazení místo ceny kliku Skliku).
- [ ] Ondřej: schválil výdaje (Bazoš 49 Kč vložení + 2× TOP po 49 Kč = 147 Kč, strop 392 Kč, Sbazar 0 až 29 Kč).
- [ ] Ondřej: schválil právní rámec (obchodní podmínky a smlouva B2B, limit odpovědnosti, záruka vrácení peněz, role zpracovatele, licence k AI výstupům).
- [ ] Ondřej: rozhodl o riziku Vercel Terms čl. 11 (i) (přijetí rizika, nebo písemné potvrzení od Vercel support) a potvrdil, kdo Vercel Pro platí.
- [ ] Ondřej: autorizoval účet na Bazoši (SMS ověření telefonu, mikroplatba 1 Kč z firemního Fio účtu) a na Sbazaru (Seznam účet, SMS), rozhodl o veřejném telefonu v inzerátu.
- [ ] Claude: designový průzkum `plan/design-web-za-24-hodin.md` a vzor (screenshoty PC 1500 a mobil 390 a 360 prohlédnuty).
- [ ] Claude: korektura všech textů (inzerát, odpověď, nabídka, podmínky), nic vymyšleného (reference, hodnocení), ukázky označeny jako vzor.
- [ ] Claude: inzerát prošel kontrolou proti pravidlům (bez hvězdiček, vykřičníků, emotikonů a velkých písmen, číselná cena, název a IČO na konci, žádný duplicitní text, bez odkazu na vlastní web).
- [ ] Claude: měření (e-mail pro kanál, skript na zobrazení, tabulka trychtýře a důvodů „proč ne“) funguje a proběhl zkušební zápis.
- [ ] Claude: `plan/kontrola-spusteni.py` projde pro tento plán.
- [ ] Po testu: `plan/web-za-24-hodin-vyhodnoceni.md` s poučením pro další RUN a rozhodnutím (pokračovat, upravit, zastavit).
