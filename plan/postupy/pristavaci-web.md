# Přistávací web na jeden produkt: normy, prémiový vzhled, revize, vyvarování

Zpracováno 2026-10-02 po Ondřejově hlášení (FAILS.md 13:50, „weby nesplňují normy přistávacího webu a vypadají průměrně“, „nesmí vypadat, že je dělala AI“). Jen výzkum, v kódu webů nic nezměněno.
Cílová skupina tohoto dokumentu: Claude (staví) a nezávislý recenzent (hodnotí). Weby, na které se vztahuje: Printopia (hledá rodič, používá žák, platí rodič) a anoberu (hledají, používají i platí snoubenci).
Legenda sloupce **Auto**: **A** = ověří skript (Playwright computed styles, Lighthouse), **Č** = skript upozorní, rozhodne recenzent, **N** = jen recenzent. Číslo v hranatých závorkách = zdroj v oddílu Zdroje. „vlastní“ = náš práh bez normy (odhad z příkladů a praxe), dá se změnit.
Omezení průzkumu: Chromium v kontejneru nedůvěřuje CA proxy a TLS jsem nevypínal, proto jsou hodnoty příkladů čtené z CSS a HTML kódu (curl), ne z vykreslení. Číselné statistiky z blogů dodavatelů nástrojů jsou označené „orientačně“.

## Závěr

- Normy nejsou o ozdobách: jedna nabídka, jedno primární tlačítko opakované aspoň 3×, cena a důkaz v prvních dvou obrazovkách (74 % času čtenáři stráví v prvních dvou obrazovkách [3]), námitky v FAQ, rychlost (LCP ≤ 2,5 s, CLS ≤ 0,1, INP ≤ 200 ms [16]), kontrast 4,5:1 [23], cíle k dotyku ≥ 44 px [25][28].
- Špičkové jednoproduktové stránky mají velký skutečný náhled produktu, konkrétní čísla (218 stran, 50 kapitol, 200 lekcí) a pojmenované reference s rolí.
- „AI vzhled“ je statistický průměr: Inter, fialovo-indigový akcent, gradient, vycentrovaný hero se štítkem nad nadpisem a třemi stejnými kartami s ikonou, emoji, krémové pozadí s terakotou [31][32][33][34][35][36][37]. Studie 1 590 stránek: 54 % má aspoň 2 znaky, 22 % čtyři a více [31].
- **Naše weby zasahuje většina znaků:** Inter + Fraunces, krémové pozadí, štítek (eyebrow) velkými písmeny nad H1, ikony v zaoblených čtvercích, dvě akcentní barvy (Printopia), 17 (Printopia) a 15 (anoberu) různých velikostí písma proti limitu 8, popisek 11,5 px, krátké sekce (48 a 72 px). Podrobně v oddílu 2.5.
- Reference nevymýšlet: recenze musí být skutečné a označené, jinak hrozí pokuta (tisk uvádí až 5 mil. Kč) [9]. Bez recenzí se prodává ukázkou zdarma, ověřitelnými čísly produktu, zárukou a tím, kdo za tím stojí (oddíl 1.3).
- Recenze vzhledu: rubrika 10 bodů (oddíl 4), spuštění od 8/10 a zároveň body K7 (poctivost) a K9 (nepůsobí jako AI) musí být 1.
- Měřitelné prahy jsou v posledním oddílu „Automaticky ověřitelné prahy“ pro kontrolní skript.

## 1. Normy přistávacího webu (jeden produkt)

### 1.1 Pořadí sekcí

1. Hlavička: logo, nanejvýš jedno tlačítko, bez menu pryč z nabídky (poměr pozornosti 1:1 [2]).
2. Hero: H1 (4–12 slov), podnadpis, primární tlačítko s cenou, sekundární obrysové (ukázka zdarma), velký náhled produktu.
3. Pás důkazů: čísla o produktu, externí hodnocení nebo „jak vzniklo“. Důkaz patří k tlačítku, kde se kupující rozhoduje [1].
4. Problém a řešení: 3–5 přínosů, každý jiným rozvržením, ne tři stejné karty.
5. Jak to vypadá: velký náhled, ukázka z produktu zdarma.
6. Co je uvnitř: obsah výčtem.
7. Námitky: pro koho je a pro koho ne, srovnání s alternativami.
8. Cena: jedna nabídka, kotva (srovnání), záruka, tlačítko.
9. FAQ.
10. Závěrečné tlačítko.
11. Patička: provozovatel, IČO, VOP, ochrana údajů, kontakt (jen tady, ne v hero).

Pořadí odpovídá doporučení Unbounce [1] a příkladům E1–E7 (oddíl 2.3).

### 1.2 Pravidla a prahy

| Oblast | Pravidlo a práh | Auto | Zdroj |
|---|---|---|---|
| Hero | H1 jediný na stránce, 4–12 slov (příklady 4–9, Things 20 = výjimka), nabídka pro plátce, ne název firmy | A počet slov, N obsah | [1] E1–E7, vlastní |
| Hero | Podnadpis ≤ 30 slov, v hero aspoň 2 konkrétní čísla (např. 12 témat, 349 Kč) | A | [4] vlastní |
| Hero | Na PC 1440×900 i mobilu 390×844 je nad ohybem H1, primární tlačítko a vizuál produktu | A geometrie | [1][3] (57 % času nad ohybem) |
| CTA | Jedno plné primární tlačítko v první obrazovce, ostatní obrysová; stejné znění a cíl všude; ≤ 5 slov; u prodejního tlačítka cena | A | [2] |
| CTA | Opakování ≥ 3× na stránce, od předchozího nejdál 2,5 výšky obrazovky (E1 6–8×, E4 7×, E7 4+) | A | E1, E4, E7 |
| CTA | Výška ≥ 48 px, plocha tlačítka ≥ 44×44 px | A | [25][28] |
| Navigace | V hlavičce ≤ 3 odkazy, žádný pryč z nabídky | A | [2] |
| Text | Odstavec ≤ 4 věty, nadpisy nesou smysl, odrážky; objektivní jazyk místo superlativů (užitečnost +27 %, stručnost +58 %, skenovatelnost +47 %, vše dohromady +124 %) | Č | [4][5] |
| Text | Délka řádku 45–80 znaků na PC, ≥ 30 na mobilu | A | [12][13][27] |
| Text | Tělo 16–24 px (příklady 16–18), nejmenší text ≥ 12 px, výška řádku těla 1,4–1,7, nadpisů 1,05–1,25 | A | [13][27] E1, E3, E4 |
| Důkaz | ≥ 3 ověřitelná čísla o produktu (počet úloh, stran, témat); recenze jen skutečné a označené | Č | [8][9] |
| Důkaz | Kdo za tím stojí: značka nebo jméno, kontakt v patičce, krátké „O nás“ | Č | [6] |
| Cena | Cena v hero tlačítku i v oddílu Cena, viditelná do dvou výšek obrazovky | A | [3] |
| Cena | Kotva = srovnání s reálnou alternativou se zdrojem. Přeškrtnutá „původní cena“ jen s nejnižší cenou za posledních 30 dní, jinak zákaz | N | [10] |
| Cena | Jedna nabídka a jedna cena u jednoho produktu, záruka (konkrétně, kolik dní a jak) vedle tlačítka | Č | E1, E5, E7 |
| FAQ | 5–12 otázek z reálných námitek (ne vymyšlených), odpověď ≤ 60 slov | Č | [7] |
| Objednávka | ≤ 3 viditelná pole, jen e-mail (+ jméno), bez účtu, label, `type=email`, `autocomplete`, chyba u pole; od tlačítka k platebním pokynům ≤ 2 kliky | A | [11] |
| Výkon | LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 (75. percentil), FCP ≤ 1,8 s, TBT ≤ 200 ms (labor), Lighthouse mobil ≥ 90 | A labor, pole až při provozu | [16][17][18][20] |
| Výkon | LCP obrázek bez `loading=lazy`, s `fetchpriority=high`; všechny obrázky se `width`/`height`; WebP/AVIF/SVG; přenos při prvním načtení ≤ 1 600 KiB (Lighthouse selže nad 5 000 KiB) | A | [19][21] |
| Výkon | Rychlost je tržba: 0,1 s rychleji = +8,4 % konverzí (retail), 3 s na mobilu je hranice ztrát (orientačně, sekundární zdroje) | – | [1][22] |
| Přístupnost | Kontrast textu ≥ 4,5:1, velkého textu (≥ 24 px, tučného ≥ 18,66 px) ≥ 3:1, ovládací prvky a okraje polí ≥ 3:1 | A | [23][24] |
| Přístupnost | Cíle k dotyku ≥ 44 px (AAA), absolutní minimum 24 px (AA), mezera ≥ 8 px | A | [25][28] |
| Přístupnost | Žádné vodorovné posouvání od šířky 320 px (400 % zoom) | A | [26] |
| Přístupnost | `lang="cs"`, `alt` u obrázků, jeden H1, nadpisy bez přeskoků, viditelný `:focus-visible`, `prefers-reduced-motion`, pole formuláře ≥ 16 px (jinak iOS Safari přibližuje) | A | [29] |
| Mobil | Navrhnout od 390 px (83 % návštěv landing pages je z mobilu, orientačně) a prověřit i 360; nejvýš jeden plovoucí prvek (lišta s nákupem), až po odscrollování tlačítka v hero | A | [1] CLAUDE.md |
| Měření | ≥ 4 události: zobrazení, klik na CTA, začátek objednávky, nákup (trychtýř podle pravidla Metriky) | A | CLAUDE.md |
| Animace | Přechody 100–400 ms, nic delšího, žádný parallax a scroll-jacking | A | [14] |

Co automaticky ověřit nejde: pravdivost čísel a referencí, srozumitelnost nabídky, smysluplnost kotvy, skutečná čitelnost textu na náhledu produktu, „pocit“ šablonovosti. To posuzuje recenzent podle rubriky (oddíl 4).

### 1.3 Situace bez recenzí: poctivě

Zákaz: vymyšlené citáty, jména („Jana K.“), „4,9/5“, „stovky spokojených“, portréty ze stocku jako zákazníci. Recenze musí být skutečné a označené, zda jsou ověřené, a jak se ověřují; informace nesmí být jen ve VOP; recenze od lidí s produktem zdarma se označí „sponzorované“ [9]. Pokuta až 5 mil. Kč (podle tisku, viz [9]). Slevu počítat jen z nejnižší ceny za posledních 30 dní [10].

Náhrada důkazu, kterou můžeme splnit hned:
1. Ukázka zdarma (PDF) a velký náhled produktu: kupující si důkaz vyrobí sám.
2. Ověřitelná čísla produktu: počet témat, úloh, stran, „každá úloha ověřená výpočtem“ (jen pokud je to pravda).
3. Záruka vrácení peněz u ceny (14 dní podle VOP) a věta „jsme nový obchod“ místo předstírání zkušeností.
4. Kdo za tím stojí: skutečný autor nebo značka, kontakt, odpověď na dotaz do 24 h.
5. Externí hodnocení, které nevyrábíme: Zboží.cz „Ověřeno zákazníky“, Firmy.cz. Odkaz místo okopírované hvězdičky [6].
6. Sběr skutečných recenzí: e-mail 14 dní po nákupu s odkazem; ověřené označit („koupeno u nás“) a způsob uvést u recenzí [9]. Do první recenze sekci Recenze nezobrazovat.
7. Prvním zákazníkům za zpětnou vazbu zdarma: označit jako sponzorovanou [9].

### 1.4 Právní rámec v kostce

- Recenze: [9] (zákon o ochraně spotřebitele po novele Omnibus, účinnost 6. 1. 2023).
- Slevy: [10].
- Přístupnost: evropský zákon o přístupnosti (EAA) zná výjimku pro mikropodniky (< 10 zaměstnanců a obrat nebo bilance ≤ 2 mil. EUR) u služeb [30]. WCAG AA držíme i tak jako kvalitu a kvůli Lighthouse; při růstu firmy ověřit s právníkem (právo = veto Ondřeje).

## 2. Co dělá web prémiovým a ne průměrným

### 2.1 Principy s hodnotami

| Oblast | Prémiově | Levně | Auto |
|---|---|---|---|
| Typografie | ≤ 2 rodiny písma, výrazné nadpisy a čitelný text; H1 ≥ 2,5× tělo na PC (E1 4×, E2 4,5×, E4 3×); škála ≤ 8 velikostí; max. 3 tloušťky; řádkování těla 1,4–1,7 [13]; nadpisy mezery mezi písmeny −0,01 až −0,03 em | 10 různých velikostí, malé písmo 11 px, těsné nadpisy pod −0,05 em, plochá hierarchie (H1 do 2× těla) [33] | A |
| Mezery a rytmus | Mřížka 8 px, pro text 4 px [15]; sekce 80–160 px nahoře i dole na PC (E1 96/160), 48–96 px na mobilu; blízkost: mezera nadpis → text menší než mezera mezi sekcemi | Různé mezery po 5–7 px, stejné odsazení všeho, sekce 48 px natěsno | A |
| Barva | Neutrální tmavý text, 1 akcent jen na tlačítka a pár prvků, sémantické barvy (chyba, úspěch) navíc; kontrast 4,5:1 / 3:1 | 2+ akcentů bez hierarchie, gradienty, záře, neon [37] | A |
| Vizuály produktu | Velký skutečný náhled (≥ 560 px na PC, ≥ 85 % šířky mobilu) s čitelným textem, ořez na jednu úlohu nebo list, popisky; vlastní grafika odvozená z produktu; foto jen když nese informaci | Drobný mockup, stock lidé u notebooku, dekorativní fotka bez vztahu k produktu | A rozměr, N čitelnost |
| Mikrointerakce | Hover, focus a stisk u všeho klikacího, přechod 100–300 ms [14], plynulé otevření FAQ ≤ 300 ms, respekt k `prefers-reduced-motion`; stavy chyb a prázdné stavy napsané lidsky [36] | Nic se nehýbe, nebo vše stejně „fade-in“ [36] | Č |
| Hierarchie | V každé sekci jedno ohnisko, 3 úrovně textu (nadpis, text, popisek), tlačítko je nejvýraznější prvek stránky | Vše stejně velké, karty všude [36][37] | Č |
| Konzistence | 2–4 hodnoty zaoblení podle role (tlačítko, karta, obrázek), jedna sada ikon, jeden styl stínu, jeden levý okraj | Jedno zaoblení a `shadow-lg` na všem [34][36] | A |
| Texty | Konkrétní čísla a slova z jazyka zákazníka, jednotné vykání, žádné fráze (oddíl Znaky AI) | „Posuňte na vyšší úroveň“ [36] | A frázemi |

### 2.2 Vlastní vizuální jazyk z produktu (návrh k ověření recenzí, nic nenasazeno)

Odlišení od šablony se nedá koupit písmem, vzniká z toho, co produkt je. Návrhy:
- Printopia: produkt je tištěný pracovní list. Vizuální jazyk z papíru: kostičkovaný nebo linkovaný podklad, korektura tužkou, razítko u vyřešené úlohy; v hero velká skutečná strana PDF s jednou úlohou a postupem, ne tři rotované drobné listy.
- anoberu: produkt je tabulka. Jazyk z buněk tabulky: mřížka, záhlaví sloupců, skutečný snímek obrazovky přehledu s opravdovými daty (velký, ≥ 560 px), ne ilustrovaný pár u notebooku.
- Fotky jen tam, kde nesou informaci (autor, situace), ne jako výplň. Vlastní kresba nebo skutečný snímek produktu vždy před stockem.

### 2.3 Příklady špičkových stránek (7)

Hodnoty z CSS a HTML (curl) 2026-10-02. Našich barev a písem se z toho nepřebírá nic, přebírá se přístup a měřítka.

| Příklad | Typ | Co dělá dobře | Hodnoty z kódu |
|---|---|---|---|
| E1 [Refactoring UI](https://refactoringui.com) | digitální produkt (kniha + zdroje) | 8 celých stran PDF a galerie komponent velké na stránce; čísla produktu (218 stran, 50 kapitol); 15+ referencí s účty; dvě ceny (99 a 149 USD), tlačítko 6–8× | Inter, H1 64 px (PC, řádek 76), H2 56 px, text 18 px (text-lg), kontejner 1 152–1 280 px, sloupec textu 672–896 px, sekce py-24/py-40 (96/160 px), tlačítko h-14 (56 px), `rounded-full` 54×, `shadow-lg` 41×. Pozor: H1 s gradientem a těsným řádkováním jsou naše zakázané znaky |
| E2 [CSS for JavaScript Developers](https://www.css-for-js.dev) | kurz | Osobní hlas („CSS can be fun. I promise.“), vlastní ilustrace, 30+ pojmenovaných referencí s rolemi (Netflix, tvůrce Tailwindu), sekce „Hi, I'm Josh“, FAQ 16 otázek, záruka 30 dní, regionální ceny | Wotfard + Sriracha + League Mono, H1 `min(72px, 8vw)` váha 500, na mobilu 12vw vlevo, citát 24 px, pozadí hsl(274 16% 8%), akcent hsl(333 100% 52%). Přebrat: osobnost a vlastní kresby, ne barvy |
| E3 [Things](https://culturedcode.com/things/) | jednoprodukt (aplikace) | Obrovské snímky produktu, ceny a ocenění (Apple Design Award), citáty konkrétně o funkcích, jedna hlavní výzva (video) | systémové písmo, tělo 18 px, řádek 1,4, text #303336 na bílé, H2 1,5 em řádek 1,25, `max-width: 900px` (3×) |
| E4 [Fakturoid](https://www.fakturoid.cz) (CZ) | malá firma, SaaS | H1 6 slov o výsledku („Fakturujte jednoduše a dostaňte rychleji zaplaceno“), čísla měsíce (895 350 faktur), „88 % doporučuje“, „Napsali o nás“, reference s fotkou u každé funkce, mikrotext pod tlačítkem „Bez zbytečných složitostí“, 7× CTA „Začněte zdarma“ | nadpisy Cocon, tělo systémové, tělo řádek 1,625, H1 36 px → 48 px (xl), základ mezer 4 px, zelený akcent, `rounded-full` 43×, `rounded-2xl` 11× |
| E5 [Ultimate Brain](https://thomasjfrank.com/brain/) | šablona (Notion) | „+40 000 uživatelů“ u tlačítka, video ukázka, FAQ řeší rozdíl od jiných produktů, záruka 30 dní a postup, ceny před/po s kódem. Nepřebírat: emoji v nadpisech | systémové písmo, H1 6 slov, CTA „Get Started“ 2× + „Buy“ |
| E6 [Plausible](https://plausible.io) | malý produkt (SaaS) | H1 8 slov, dvě tlačítka (zkouška a živé demo), pás čísel (21 tis. předplatitelů), srovnání s alternativou („54× menší skript“), snímek produktu je hlavní vizuál, ceny v tabulce | systémové písmo, jeden akcent; hodnoty jen z čtení stránky, ne z kódu |
| E7 [Hatchly](https://www.hatchly.co.uk) | produktizovaná služba | Cena v hero („od 995 £ první měsíc“), Trustpilot 4,5, 4sloupcová srovnávací tabulka (my / interně / freelancer / agentura s cenami), 4 kroky, záruka 7 dní, CTA 4+× | – |

Pozn.: český trh jednoproduktových stránek nemá srovnatelně špičkové příklady v našem oboru (konkurence přijímaček a svatebních plánovačů je v `plan/design-prijimacky.md`, `plan/design-anoberu.md`), proto E1–E3, E5–E7 jsou zahraniční. Z příkladů E1–E4 plyne: tělo 16–18 px, řádek 1,4–1,625, H1 48–72 px, sekce 96–160 px (E1), kontejner 1 152–1 280 px (E1), tlačítko 56 px (E1), 6–8 výzev k akci.

### 2.4 Měřítka z příkladů pro náš kontrolní skript
H1 PC 40–72 px (E1 64, E2 72, E4 48), mobil 28–40 px (E4 36); tělo 16–24 px; řádek těla 1,4–1,7; sekce 80–160 px; sloupec textu 672–900 px (E1, E3); tlačítko 48–56 px; zaoblení tlačítek pilulka, karet 12–16 px.

### 2.5 Naše weby proti měřítkům (z CSS kódu, nevykresleno)

| Nález | Kde | Práh | Verdikt |
|---|---|---|---|
| Písma Inter + Fraunces | oba | zakázané/varování (oddíl Znaky AI) | selhává |
| Krémové pozadí #fbfaf6 / #faf7f2 | oba | varování | selhává |
| Štítek `.eyebrow` velkými písmeny nad H1 | oba | zakázáno | selhává |
| Ikony v zaoblených čtvercích 44 px (`.icon`) | Printopia | zakázáno | selhává |
| Dvě akcentní barvy (modrá, žlutá) | Printopia | 1 akcent | selhává |
| Tmavý hero #1c2230 + žlutý akcent | Printopia | varování (druhotný default) | varování |
| 17 (Printopia) a 15 (anoberu) různých deklarací `font-size`, nejmenší 0,72 rem = 11,5 px (`.credit`) | oba | ≤ 8 velikostí, ≥ 12 px | selhává |
| Sekce 48 px (mobil 36 px) u Printopie, 72 px u anoberu | oba | 80–160 / 48–96 | selhává |
| Žlutá číslice 1,71:1 na papíře (`ol.topics::before`, dekorativní) | Printopia | 3:1 pro text | selhává, pokud nese informaci |
| `.accent` terakota #b5694a 3,87:1 | anoberu | text 4,5:1 | jen pro velký text |
| Ostatní dvojice text/pozadí (měřeno) | oba | 4,5:1 | splněno (5,1–11,8) |
| `.btn-small` ≈ 34–38 px, `.chip` ≈ 37 px | oba | 44 px | selhává |
| `.btn` ≈ 47–48 px | oba | 48 px | splněno |
| Chybí `:focus-visible` pro odkazy a tlačítka, chybí `prefers-reduced-motion` | oba | povinné | selhává |
| Formulář: 2 pole + 1–2 zaškrtnutí, label, type, autocomplete | oba | ≤ 3 pole | splněno |
| `lang="cs"`, písma vlastní (self-host), `font-display: swap` | oba | povinné | splněno |
| Šířka obsahu 1 340 px + 80 px okraj (pravidlo Ondřeje) | oba | – | splněno, ale text sloupce musí držet 45–80 znaků |

## Znaky webů navržených AI a jak se jim vyhnout

Příčina: model vrací průměr tréninkových dat, a průměrný web od roku 2019 má výchozí paletu Tailwindu (indigo-500), Inter, kulaté karty [35][34]. Studie 1 590 stránek Show HN, měřeno deterministicky z DOM a CSS, ne okem: 22 % má 4 a více znaků, 32 % dva až tři, 46 % nula až jeden [31][32]. Cíl našich webů: 0 znaků třídy A, celkem ≤ 1. Třída A = znaky, které pozná i laik (obdoba P0 v [34]): Z3, Z4, Z5, Z8, Z9, Z10, Z14; zařazení je naše.
Zdroje [31]–[38], u textů [39][40]. Sloupec Auto: A skript, Č částečně, N recenzent.

| # | Znak | Jak poznat v kódu | Čím nahradit | Auto |
|---|---|---|---|---|
| Z1 | Výchozí písmo: Inter (a druhotně Roboto, Arial, systémové jako hlavní); „trendové“ dvojice (Space Grotesk, Instrument Serif, Geist, a druhotně Fraunces, Playfair Display, Poppins, DM Sans, Montserrat, Open Sans) [31][32][33][34][35] | `font-family`: první rodina v seznamu zakázaných; soubory `inter-*.woff2`; `@font-face` | Písmo vybrat podle povahy produktu: tři kandidáti, vykreslit H1 a odstavec česky se všemi diakritikami, zapsat důvod do `plan/design-<projekt>.md`. Kandidáti s ověřenou latin-ext podporou (Google Fonts, 2026-10-02): nadpisy Newsreader, Source Serif 4, Literata, Young Serif, Besley, Libre Caslon Text, Gelasio, Spectral, Crimson Pro; text Public Sans, Work Sans, IBM Plex Sans, Albert Sans, Hanken Grotesk, Schibsted Grotesk, Onest; display Bricolage Grotesque. Hostovat lokálně. Rozhoduje záznam důvodu, ne seznam | A |
| Z2 | Serifová kurzíva u jednoho slova v H1 [32] | `h1 em`, `h1 i` se serifem | Důraz váhou nebo bez důrazu | A |
| Z3 | Fialovo-indigový akcent („VibeCode purple“, indigo-500 #6366f1) [33][35][37] | HSL odstín 240–295°, sytost ≥ 35 % na tlačítku nebo akcentu; hex #B8A8D9, #C9B0E3 | Akcent z produktu: papír a tužka, zelená tabulky, barva razítka. Jeden | A |
| Z4 | Gradient v nadpisu [33][34] | `background-clip: text` + gradient, `-webkit-text-fill-color: transparent` | Jednobarevný nadpis | A |
| Z5 | Gradienty všude, aurora, záře, glassmorphism [32][33][37] | ≥ 5 prvků s `linear-gradient`/`radial-gradient`; `backdrop-filter: blur`; `box-shadow` barevný s blur ≥ 24 px; `filter: blur` na dekoračních prvcích | Plné plochy, nejvýš 1 jemný přechod; neprůhledné podklady a 1px okraj; neutrální stín | A |
| Z6 | Trvale tmavý režim s šedým textem [32][33] | pozadí body tmavé (jas < 10 %) a text #666–#999 | Světlé stránky s kontrastem; tmavá jen jedna sekce s důvodem | A |
| Z7 | Krémové pozadí + terakota nebo šalvěj; near-black + akcent (druhotné výchozí volby) [33][34] | pozadí HSL odstín 30–50°, sytost 20–60 %, jas 90–97 % | Neutrální bílá nebo plná barevná plocha zvolená záměrně; paleta z produktu. Výjimka jen se zdůvodněním | A (varování) |
| Z8 | Vycentrovaný hero + tlačítka uprostřed [31][32][33] | H1 `text-align: center` (nebo ve vycentrovaném kontejneru) na PC | Hero ve dvou sloupcích: text vlevo, velký náhled vpravo; podnadpis a tlačítka zarovnané vlevo | A |
| Z9 | Štítek nad H1 („Nově“, pill, „PŘIJÍMAČKY 2027“) [31][32][33] | element těsně před `h1` s `text-transform: uppercase`, `letter-spacing` ≥ 0,08 em, nebo `border-radius` ≥ 999 px | Zrušit; kontext do podnadpisu nebo do věty | A |
| Z10 | Mřížka 3 stejných karet s ikonou nahoře [31][32][33][35][37] | ≥ 3 sourozenci stejné struktury, první potomek `svg`/`img` ≤ 64 px | Každý přínos jiné rozvržení: řádek text + velký obrázek, před/po, tabulka, ukázka úlohy; ikony jen kde nesou význam | A |
| Z11 | Ikona v zaobleném čtverci [33][34] | `svg` v prvku s pozadím a `border-radius` 8–16 px, 36–56 px | Vlastní kresba nebo číslo/typografie | A |
| Z12 | Karty pro každý blok, karta v kartě, barevný okraj zleva/shora [32][33][37] | podíl bloků s `border` + `border-radius` + stín; vnoření karet; `border-left/top` ≥ 3 px barevný | Seskupit mezerou, nadpisem a čarou; karty jen pro klikatelné nebo srovnávané | A |
| Z13 | Stejné zaoblení, stín a odsazení všude [34][36] | 1 hodnota `border-radius` pro vše; `box-shadow` na > 50 % bloků | 2–4 hodnoty podle role; stín jen pro to, co se vznáší | A |
| Z14 | Emoji místo ikon, jiskry ✨ [33][37][39] | regex emoji v textech UI (`h1`–`h6`, `li`, `button`, `a`, `label`) | Skutečné ikony jedné sady, nebo bez | A |
| Z15 | Číslované kroky 01/02/03, pás statistik („10k+“, „99,9 %“) [32][33] | dekorativní číslování; řádek ≥ 3 velkých čísel s popiskem | Číslovat jen skutečný postup; čísla vložit do vět o produktu | A |
| Z16 | Popisky a nadpisy velkými písmeny [32][33] | `text-transform: uppercase` na `h1`–`h3` a popiscích | Věta s malými písmeny | A |
| Z17 | Těsné písmo a předimenzovaný H1; plochá hierarchie [33] | `letter-spacing` < −0,05 em; H1 ≥ 72 px a ≥ 40 znaků; velikosti s poměrem max/min < 2 | −0,01 až −0,03 em; H1 40–72 px a ≥ 2,5× tělo | A |
| Z18 | Nízký kontrast textu, šedý text na barvě [32][33] | poměr < 4,5:1; šedý text na chromatickém pozadí | ≥ 4,5:1, tmavší odstín téže barvy | A |
| Z19 | Drobné mockupy a tři rotované listy místo skutečného velkého náhledu | náhled < 560 px na PC nebo < 85 % šířky mobilu; efektivní velikost textu na náhledu < 9 px | Jeden velký ořez (jedna úloha, jeden list) se zvýrazněním | A rozměr, N čitelnost |
| Z20 | Generické stockové fotky (lidé u notebooku, usmívající se tým) a nic vlastního [35][38] | `alt` typu „person“/„laptop“; fotka je největší vizuál v hero; v hero není produktová grafika | Produkt v hero; foto jen s informací (autor, situace), s uvedením autora | Č |
| Z21 | Chybí kontext a vlastní grafika: nadpis bez čísla a bez konkrétní věci [35][36] | H1 bez číslice a podnadpis bez konkrétního podstatného jména produktu; v hero < 2 čísla | „12 témat, 340 úloh s postupem“; autor a příklad | Č |
| Z22 | Vymyšlené reference [9] | `blockquote`/hvězdičky bez zdroje a označení ověření; generická jména; „tisíce spokojených“ | Oddíl 1.3 | Č |
| Z23 | Marketingové fráze, vzorec „není X, ale Y“, trojice, vykřičníky [39][40] | regex (seznam v posledním oddílu): bezproblémově, na vyšší úroveň, odemkněte, vše, co potřebujete, ponořte se, komplexní řešení, „není to jen…, ale“, nadpis „A, B a C“ | Konkrétní věty s čísly; žádná výčtová trojice v nadpisech | A |
| Z24 | Dlouhá pomlčka — a přemíra pomlček [39][40] | U+2014; > 3 pomlčky (–) na 1 000 znaků | Čárka, tečka, závorka; pomlčka (–) s mezerami jen výjimečně | A |
| Z25 | Chybějící stavy a pohyb: žádný focus, chyba formuláře bez textu, vše se plynule objevuje stejně [36] | chybí `:focus-visible`; `fade-in` na všech blocích; chybí hlášky chyb | Focus, hover, stisk; hláška u pole česky; animace jen u tlačítek a FAQ | Č |

Pravidlo: 0 znaků třídy A (Z3, Z4, Z5, Z8, Z9, Z10, Z14) a celkem ≤ 1 znak (obdoba „clean 0–1“ [31]).

## 4. Rubrika nezávislé revize vzhledu (10 bodů)

Recenzent je jiný agent než autor. Vidí jen: screenshoty PC 1440×900 (první obrazovka i celá stránka), mobil 390×844 (první obrazovka i celá stránka), vykreslené HTML a výstup kontrolního skriptu (JSON z oddílu Automaticky ověřitelné prahy). Každé kritérium 0 nebo 1, žádné půlbody. Bod dostane jen ten, kdo splní VŠECHNY dílčí podmínky. Při pochybnosti 0. U každého uvede jednu větu důkazu a jednu konkrétní opravu.

| # | Kritérium | 1 bod, pokud platí vše |
|---|---|---|
| K1 | Sdělení do 5 sekund | V první obrazovce PC i mobilu lze odpovědět: pro koho to je, co dostane, kolik to stojí nebo co kliknout. H1 nese výsledek pro plátce, ne název firmy; je tam cena nebo konkrétní číslo a jedno primární tlačítko |
| K2 | Hierarchie | Každá sekce má jedno ohnisko; tlačítko je nejvýraznější prvek stránky; 3 jasné úrovně textu; H1 ≥ 2,5× tělo; oko vede shora dolů k tlačítku |
| K3 | Typografie | ≤ 2 rodiny, řádek 45–80 znaků, řádkování 1,4–1,7, žádný text < 12 px, škála ≤ 8 velikostí, nadpisy se nelámou na sirotky (jednoslovné řádky) |
| K4 | Mezery a rytmus | Sekce 80–160 px (mobil 48–96), mezery na mřížce 4/8 px, stejné okraje, nic není natěsno a žádná prázdnota > 200 px bez obsahu; podobné věci blízko sebe |
| K5 | Barva a kontrast | 1 akcent, sémantické barvy navíc; kontrast textu ≥ 4,5:1 a tlačítka/okrajů ≥ 3:1; žádný gradient, záře ani neon; barva je použita stejně na celé stránce |
| K6 | Vizuál produktu | Skutečný náhled produktu nebo vlastní grafika je největším vizuálem; na PC ≥ 560 px, na mobilu ≥ 85 % šířky; text na něm je čitelný při reálné velikosti; stock foto není hlavním vizuálem |
| K7 | Důvěra a poctivost (**veto**) | Žádný vymyšlený ani neověřitelný důkaz; recenze označené nebo žádné; záruka konkrétně u ceny; kotva se zdrojem, sleva podle pravidla 30 dní; kdo za tím stojí a kontakt v patičce; provozovatel není v hero; zákaz výzvy dětem ke koupi dodržen. 0 znamená nespustit, i při 9/10 |
| K8 | Konzistence a řemeslo včetně mobilu | 2–4 hodnoty zaoblení podle role, jedna sada ikon, jeden styl stínu; zarovnání na společné hrany; na 360 a 390 px nic nepřetéká ani se nepřekrývá; cíle k dotyku ≥ 44 px; focus je vidět; obrázky ostré |
| K9 | Nepůsobí jako vygenerované AI (**podmínka spuštění**) | Z oddílu Znaky AI je přítomno ≤ 1 znak a žádný třídy A (Z3 fialový akcent, Z4 gradient v nadpisu, Z5 gradienty a glass, Z8 vycentrovaný hero, Z9 štítek nad H1, Z10 3 stejné karty s ikonou, Z14 emoji); a recenzent upřímně odpoví „neřekl bych šablona ani AI“. Bez kontextu, bez čísel nebo s frází ze seznamu = 0 |
| K10 | Cesta k nákupu a texty | Tlačítko ≥ 3× se stejným textem a cílem; FAQ 5–12 otázek; námitky vyřešené před cenou; formulář ≤ 3 pole; žádná zakázaná fráze; texty konkrétní (bez „vaty“); český text bez chyb, uvozovky „ “ |

**Spuštění:** součet ≥ 8/10 a zároveň K7 = 1 a K9 = 1. Jinak oprava podle konkrétních oprav recenzenta a nová revize jiným recenzentem. Zápis výsledku do `plan/revize-vzhledu-<projekt>-<datum>.md` (skóre, důkazy, opravy).
Formát výstupu recenzenta: JSON `{"K1":{"b":0|1,"dukaz":"…","oprava":"…"},…,"soucet":n,"spustit":true|false}`.

## 5. Čeho se vyvarovat

- Stavět vzhled „z hlavy“ bez porovnání s 3 příklady a bez měření (FAILS.md 2026-10-01 01:43, 2026-10-02 13:50).
- Brát výchozí volby nástroje: Inter, indigo, 3 karty, krémové pozadí s terakotou. Každá hodnota má mít důvod z produktu.
- Přidávat prvek „protože se to dělá“: štítek, ikony, pás čísel, číslování, pozadí s přechodem.
- Drobné náhledy produktu (nic neukazují) a stockové fotky místo produktu.
- Vymyšlené reference, hvězdičky bez zdroje, „původní cena“ bez nejnižší ceny za 30 dní [9][10].
- Několik různých tlačítek a cílů v první obrazovce, odkazy pryč z nabídky [2].
- Superlativy a fráze místo čísel; trojice v nadpisech; dlouhé pomlčky [4][39][40].
- Kontrola jen v jednom viewportu: prověřit 360, 390, 768, 1280, 1440.
- Výkonová regrese kvůli obrázkům: LCP obrázek lazy, bez rozměrů, JPEG/PNG velké než potřeba [19].
- Opravy vlastního vzhledu hodnotit samotným autorem: hodnotí jiný agent (oddíl 4).

## Kontrolní seznam před spuštěním přistávací stránky

Odškrtnout až po provedení, u každého bodu uvést výsledek nebo odkaz. Nic nebylo ještě provedeno na webech.

- [x] Průzkum norem z ≥ 2 nezávislých zdrojů (Unbounce, NN/g, Baymard, WCAG, web.dev, ČOI), zdroje v oddílu Zdroje.
- [x] Průzkum znaků AI vzhledu a textů ze ≥ 3 nezávislých zdrojů ([31]–[40]), seznam prahů v posledním oddílu.
- [x] 7 příkladů špičkových stránek s hodnotami z kódu (oddíl 2.3).
- [ ] `plan/design-<projekt>.md` obsahuje vizuální směr z oddílu 2.2, výběr písem se zdůvodněním (3 kandidáti) a paletu s jedním akcentem; oddíl „## Texty“ (blok → otázka).
- [ ] Hero: H1 4–12 slov, ≥ 2 čísla, primární tlačítko s cenou, velký náhled produktu ≥ 560 px, vše nad ohybem na PC 1440×900 i mobilu 390×844.
- [ ] Tlačítko stejného znění ≥ 3×, nikdy dál než 2,5 výšky obrazovky; v hlavičce ≤ 3 odkazy.
- [ ] Cena viditelná do 2 obrazovek, kotva se zdrojem, záruka konkrétně vedle tlačítka; žádná „původní cena“ bez nejnižší ceny za 30 dní.
- [ ] Důkazy: ověřitelná čísla produktu, ukázka zdarma, kdo za tím stojí; recenze jen skutečné a označené, jinak sekce skryta (oddíl 1.3).
- [ ] FAQ 5–12 otázek z reálných námitek (data z ankety „proč ne“, hledaných dotazů).
- [ ] Žádný znak třídy A z oddílu AI, celkem ≤ 1 (spustit skript).
- [ ] Kontrast, velikosti písma, délka řádku, cíle k dotyku, mezery, sekce: skript prahů bez chyby na 320, 360, 390, 768, 1280, 1440.
- [ ] Lighthouse mobil: výkon ≥ 90, přístupnost ≥ 95, LCP ≤ 2,5 s, CLS ≤ 0,1, TBT ≤ 200 ms, přenos ≤ 1 600 KiB.
- [ ] `:focus-visible`, `prefers-reduced-motion`, `lang="cs"`, `alt`, pole formuláře ≥ 16 px.
- [ ] Texty přečteny jako korektor (CLAUDE.md), žádná fráze ze seznamu, žádná dlouhá pomlčka.
- [ ] Měření: ≥ 4 události (zobrazení, klik na CTA, začátek objednávky, nákup).
- [ ] Nezávislá revize podle rubriky (oddíl 4) ≥ 8/10, K7 = 1, K9 = 1; zápis do `plan/revize-vzhledu-<projekt>-<datum>.md`.
- [ ] Screenshoty PC i mobil si Claude po každé změně vzhledu prohlédl (CLAUDE.md, Vzhled).

## Zdroje

Všechny navštíveny 2026-10-02 (WebFetch nebo curl), pokud není uvedeno jinak.

Normy a UX
1. Unbounce, Landing Page Best Practices: https://unbounce.com/landing-page-articles/landing-page-best-practices/
2. Unbounce, Attention Ratio (1:1, „One Page. One Purpose.“): https://unbounce.com/conversion-glossary/definition/attention-ratio/
3. NN/g, Scrolling and Attention (57 % času nad ohybem, 74 % v prvních dvou obrazovkách): https://www.nngroup.com/articles/scrolling-and-attention/
4. NN/g, How Users Read on the Web (79 % skenuje, stručnost +58 %, objektivní jazyk +27 %, vše +124 %): https://www.nngroup.com/articles/how-users-read-on-the-web/
5. NN/g, F-Shaped Pattern: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
6. NN/g, Trustworthiness in Web Design: https://www.nngroup.com/articles/trustworthy-design/
7. NN/g, FAQs (otázky z reálných dotazů): https://www.nngroup.com/articles/faqs-deliver-value/
8. Spiegel Research Center (Northwestern), How Online Reviews Influence Sales (5 recenzí = +270 % pravděpodobnosti nákupu, vrchol hodnocení 4,0–4,7): https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/
9. ČOI, Recenze (označit ověřené/neověřené a způsob, zákaz falešných, sponzorované označit): https://coi.gov.cz/recenze/ . Výši pokuty (až 5 mil. Kč) uvádí tisk (Podnikatel.cz, Aktuálně.cz, ve výsledcích vyhledávání, stránky jsem neotevřel), na stránce ČOI jsem ji neověřoval
10. ČOI, Slevy (nejnižší cena za 30 dní před slevou): https://coi.gov.cz/slevy/ . Číslo zákona 374/2022 Sb. a účinnost 6. 1. 2023 jsou ze zpravodajských zdrojů z vyhledávání
11. Baymard, Checkout form fields (průměr 11,3, ideál 8 u fyzické objednávky): https://baymard.com/blog/checkout-flow-average-form-fields
12. Baymard, Line length (50–75, max 80): https://baymard.com/blog/line-length-readability
13. Butterick, Practical Typography: https://practicaltypography.com/line-length.html (45–90 znaků), https://practicaltypography.com/line-spacing.html (120–145 %), https://practicaltypography.com/point-size.html (web 15–25 px)
14. NN/g, Animation Duration (100–500 ms, malé prvky ≈ 100 ms, 200–300 ms větší, 400 ms už pomalé): https://www.nngroup.com/articles/animation-duration/
15. spec.fm, 8-Point Grid: https://spec.fm/specifics/8-pt-grid

Výkon
16. web.dev, Web Vitals (LCP 2,5 s, INP 200 ms, CLS 0,1, 75. percentil): https://web.dev/articles/vitals
17. web.dev, FCP (≤ 1,8 s): https://web.dev/articles/fcp
18. web.dev, TBT (< 200 ms): https://web.dev/articles/tbt
19. web.dev, Optimize LCP (nikdy lazy-load LCP obrázku, `fetchpriority=high`): https://web.dev/articles/optimize-lcp
20. Chrome, Lighthouse performance scoring (90–100 zelená): https://developer.chrome.com/docs/lighthouse/performance/performance-scoring
21. Chrome, Total byte weight (cíl ≤ 1 600 KiB, selhání nad 5 000 KiB): https://developer.chrome.com/docs/lighthouse/performance/total-byte-weight
22. Deloitte a Google, Milliseconds Make Millions (0,1 s = +8,4 % konverzí retail; sekundárně): https://marcradziwill.com/blog/milliseconds-make-millions/

Přístupnost
23. WCAG 1.4.3: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
24. WCAG 1.4.11: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
25. WCAG 2.5.8 (24 px, AAA 2.5.5 44 px): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
26. WCAG 1.4.10 Reflow (320 px): https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
27. WCAG 1.4.8 (řádek ≤ 80 znaků, řádkování ≥ 1,5): https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
28. web.dev, Accessible tap targets (48 px, mezera 8 px): https://web.dev/articles/accessible-tap-targets
29. iOS Safari přibližuje pole s písmem pod 16 px: https://guidefari.com/safari-ios-input-zoom/ (potvrzují i další zdroje z vyhledávání, jediný načtený zdroj je neoficiální)
30. EAA, výjimka pro mikropodniky (< 10 zaměstnanců a obrat nebo bilance ≤ 2 mil. EUR, jen služby, e-shop je služba): https://www.xictron.com/en/blog/accessibility-act-exemptions-microenterprises-2026/ (sekundární zdroj, český přepis zákona neověřen)

Znaky AI
31. Adrian Krebs, Scoring Show HN submissions for AI design patterns (1 590 stránek, 16 vzorců, deterministicky): https://www.adriankrebs.ch/blog/design-slop/
32. Developers Digest, AI Design Slop: 16 patterns (detekce): https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it
33. slop-detect, 27 vzorců s prahy (odstín 240–295°, ≥ 5 gradientů, blur ≥ 24 px, −0,05 em, ≥ 72 px a ≥ 40 znaků): https://github.com/ravidsrk/slop-detect
34. avoid-ai-design, 67 znaků a „druhotné výchozí volby“ (krémová + terakota, near-black + akcent, Fraunces): https://github.com/funboy322/avoid-ai-design
35. 925 Studios, AI slop tells: https://www.925studios.co/blog/ai-slop-design-tells
36. Mania Design, Spot the Slop: https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/
37. The Fountain Institute, 7 Signs a UI Has Been Vibe Coded: https://www.thefountaininstitute.com/blog/signs-vibe-coded-ui
38. daily.dev, Vibe-coded landing pages: https://daily.dev/posts/vibe-coded-landing-pages-are-now-a-bounce-rate-liability-ldzdj5ylc
39. Wikipedia, Signs of AI writing (propagační slovník, „není jen X, ale Y“, trojice, pomlčky, emoji): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
40. 365tipu.cz, AI texty a pomlčky v češtině: https://365tipu.cz/2025/09/24/tip3066-ai-vytvorene-texty-jde-poznat-podle-pomlcek-respektive-podle-en-dash-je-to-tak/ (a články na Živě.cz a Techzprávy.cz o dlouhé pomlčce, z vyhledávání)

Příklady: E1 https://refactoringui.com, E2 https://www.css-for-js.dev, E3 https://culturedcode.com/things/, E4 https://www.fakturoid.cz, E5 https://thomasjfrank.com/brain/, E6 https://plausible.io, E7 https://www.hatchly.co.uk

## Automaticky ověřitelné prahy

Formát: jeden řádek `klíč: hodnota`. Číslo = práh (`-min` nejméně, `-max` nejvýše), `povinne` a `zakazano` = pravidlo, `varovani` = nahlásit, ale samo nezakládá chybu (počítá se do K9), seznam oddělený čárkou = hodnoty. Měří se Playwrightem (computed styles) na viditelných prvcích při viewportech PC 1440×900 a 1280×800, mobil 390×844, 360×740, 320×640, 768×1024; Lighthouse v režimu mobil. „pc“ a „mobil“ v názvu klíče určují viewport. Skrytá pole (`.hp`, `tabindex=-1`) se nepočítají. 
```text
lcp-max-s: 2.5
inp-max-ms: 200
cls-max: 0.1
fcp-max-s: 1.8
tbt-max-ms: 200
lighthouse-vykon-mobil-min: 90
lighthouse-pristupnost-min: 95
lighthouse-seo-min: 90
lighthouse-best-practices-min: 90
vaha-stranky-max-kb: 1600
obrazek-lcp-lazy: zakazano
obrazek-lcp-fetchpriority: high
obrazky-width-height: povinne
obrazky-format-povolene: webp, avif, svg
obrazek-natural-pomer-min: 1.0
obrazek-natural-pomer-max: 2.5
font-display: swap
externi-pisma: zakazano
animace-min-ms: 100
animace-max-ms: 400
kontrast-text-min: 4.5
kontrast-velky-text-min: 3
kontrast-ui-min: 3
kontrast-velky-text-px: 24
pismo-telo-min-px: 16
pismo-telo-max-px: 24
pismo-nejmensi-min-px: 12
pismo-formular-min-px: 16
vyska-radku-telo-min: 1.4
vyska-radku-telo-max: 1.7
vyska-radku-nadpis-min: 1.05
vyska-radku-nadpis-max: 1.25
delka-radku-pc-min-znaku: 45
delka-radku-pc-max-znaku: 80
delka-radku-mobil-min-znaku: 30
pocet-rodin-pisem-max: 2
pocet-velikosti-pisma-max: 8
pocet-vah-pisma-max: 3
h1-pc-min-px: 40
h1-pc-max-px: 72
h1-mobil-min-px: 28
h1-mobil-max-px: 40
pomer-h1-k-telu-pc-min: 2.5
pomer-h1-k-telu-mobil-min: 1.75
nadpis-letter-spacing-min-em: -0.05
text-letter-spacing-max-em: 0.05
tap-target-min-px: 44
tap-target-abs-min-px: 24
tap-target-mezera-min-px: 8
cta-vyska-min-px: 48
pretekani-vodorovne: zakazano
viewport-meta: povinne
html-lang: cs
obrazky-alt: povinne
h1-pocet: 1
nadpisy-bez-preskoku: povinne
formular-label: povinne
placeholder-jako-label: zakazano
focus-viditelny: povinne
prefers-reduced-motion: povinne
obsah-max-sirka-px: 1340
okraj-pc-px: 80
okraj-mobil-min-px: 16
sekce-padding-pc-min-px: 80
sekce-padding-pc-max-px: 160
sekce-padding-mobil-min-px: 48
sekce-padding-mobil-max-px: 96
mezery-nasobek-px: 4
mezery-na-mrizce-min-pct: 90
border-radius-ruznych-min: 2
border-radius-ruznych-max: 4
box-shadow-ruznych-max: 3
fixed-prvky-max: 1
fixed-prvky-z-index: povinne
akcentni-barvy-max: 1
h1-slov-min: 4
h1-slov-max: 12
hero-podnadpis-slov-max: 30
hero-cisla-min: 2
hero-vizual-povinny: povinne
hero-zarovnani-pc: left
nahled-produktu-sirka-pc-min-px: 560
nahled-produktu-sirka-mobil-min-pct: 85
cta-primarni-v-prvni-obrazovce: 1
cta-nad-ohybem-pc: povinne
cta-nad-ohybem-mobil: povinne
cta-text-stejny: povinne
cta-text-slov-max: 5
cta-obsahuje-cenu: povinne
cta-opakovani-min: 3
cta-max-vzdalenost-obrazovek: 2.5
cena-viditelna-do-obrazovek: 2
hlavicka-odkazy-max: 3
faq-polozek-min: 5
faq-polozek-max: 12
zaruka-u-ceny: povinne
provozovatel-v-hero: zakazano
provozovatel-v-patice: povinne
pole-objednavky-max: 3
checkboxy-objednavky-max: 2
objednavka-bez-uctu: povinne
objednavka-kliky-max: 2
input-type-email: povinne
autocomplete-atributy: povinne
chyba-u-pole: povinne
data-track-udalosti-min: 4
recenze-oznaceni-overeni: povinne
recenze-bez-zdroje: zakazano
placeholder-texty: zakazano
placeholder-texty-seznam: lorem ipsum, john doe, jan novak, jana k., acme
font-family-zakazane: Inter, Space Grotesk, Geist, Instrument Serif
font-family-varovani: Roboto, Fraunces, Playfair Display, Poppins, DM Sans, Outfit, Plus Jakarta Sans, Montserrat, Open Sans, Lato, Arial, Helvetica, system-ui
font-podpora-cestiny: povinne
h1-serifova-kurziva: zakazano
cta-barva-hue-zakazane-stupne: 240-295
cta-barva-sytost-zakazana-min-pct: 35
gradient-text: zakazano
gradienty-max-prvku: 1
glassmorphism: zakazano
glow-stin: zakazano
glow-stin-blur-px: 24
tmave-pozadi-body-se-sedym-textem: zakazano
pozadi-kremove: varovani
pozadi-kremove-hue: 30-50
pozadi-kremove-sat-pct: 20-60
pozadi-kremove-light-pct: 90-97
vycentrovane-textove-bloky-max-pct: 30
eyebrow-nad-h1: zakazano
uppercase-prvky-max: 2
max-stejnych-karet-v-rade: 3
karty-ikona-nahore-3-stejne: zakazano
bloky-karet-na-strance-max: 2
karty-v-kartach: zakazano
karty-barevny-okraj: zakazano
ikona-v-zaoblenem-ctverci: zakazano
emoji-v-ui: zakazano
ai-jiskry: zakazano
cislovane-kroky-bloky-max: 1
stat-banner-radky-max: 1
ai-znaky-trida-a-max: 0
ai-znaky-celkem-max: 1
text-zakazane-fraze: bezproblémov, bezstarostn, na vyšší úroveň, na další úroveň, odemkněte, odemknout, revoluční, revoluci, v dnešní uspěchané, v dnešním digitálním, ponořte se, objevte sílu, vše, co potřebujete, vše na jednom místě, komplexní řešení, inovativní, špičkov, nejmodernější, bez kompromisů, přeměňte, posuňte
text-regex-zakazane: (?i)\b(není|nejde)\s+(to\s+)?(jen|pouze|pouhý|pouhá|pouhé)\b.{3,80}?,\s*(ale|nýbrž)\b
h1-trojice-slov: zakazano
pomlcka-em-dash: zakazano
pomlcky-en-na-1000-znaku-max: 3
vykricniky-max: 0
```
