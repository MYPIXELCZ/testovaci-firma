# Měřítko kvality: zoo-hero (Ondřej 2026-10-02)

Zdroj: `reference/zoo-hero/index.html` (soubor od Ondřeje, jedna obrazovka úvodu zoo). **Je to měřítko ÚROVNĚ zpracování, ne stylu.** Umělecký, tmavý, filmový vzhled se nehodí pro každou cílovou skupinu. Styl volím podle toho, kdo hledá a kdo platí (plátce je rodič, živnostník…), kvalitu držím vždy.

## Co dělá z úvodu špičkové zpracování (a co z toho se přenáší na každý web)
1. **Vizuál je sám předmět, ne výplň.** Celá obrazovka je skutečná fotka hlavního „produktu“ (zvíře) v plné kvalitě (2400 px, ostrá, tmavá vinětace pro čitelnost textu). U nás: skutečný produkt velký a čitelný (list, tabulka, hotový web), ne stockové fotky lidí ani drobný mockup.
2. **Jedna silná myšlenka kompozice.** Obří nadpis ve dvou písmech (tučný grotesk + kurzivní patkový akcent v barvě značky) přes celý obraz, text vlevo dole, karta s faktem vpravo, miniatury dole. Hierarchie je okamžitě jasná: nadpis ≈ 8× větší než text těla (9,2 rem proti 1,18 rem).
3. **Jednoduchý barevný systém.** Téměř černá, teplá bílá, jeden ostrý akcent (limetková) a jeden doplňkový (oranžová) jako CSS proměnné; akcent jen na to, co má upoutat (CTA, kurzivní slovo, aktivní stav).
4. **Pohyb má choreografii.** Křížový přechod pozadí (1,1 s), pomalý Ken Burns (9 s), „duch“ nadpis se mění synchronně, karta s faktem a miniatury se přepínají se zpožděním 260–330 ms, jedna křivka zpomalení pro všechno (`cubic-bezier(.6,.05,.05,1)`), čítač čísel při zobrazení, tenký ukazatel postupu. Nic nepohybuje samo od sebe bez důvodu.
5. **Mikrodetaily.** Jemné zrno přes celou plochu, záře u tlačítka a tečky, šipka u tlačítka se posune při najetí, podtržení odkazu se roztáhne, aktivní miniatura se rozšíří, pauza při najetí na galerii.
6. **Responzivita jako úprava návrhu, ne zmenšení.** Na mobilu zmizí karta s faktem, tlačítka se zalomí do sloupce, třetí číslo se skryje, nadpis dostane vlastní `clamp`, galerie se stane posuvnou. 100dvh, `clamp()` všude, žádné pevné velikosti.
7. **Přístupnost a disciplína.** `prefers-reduced-motion`, `aria-label` u miniatur, `aria-hidden` u dekorace, `lang="cs"`, předpojení k fontům, vlastní fonty přes `display=swap`.
8. **Text je psaný pro člověka.** Krátké věty, konkrétní slova („koalice tří bratrů“, „řev na osm kilometrů“), žádné obecné fráze.

## Jak se to promítá do kontroly
- `tools/landing-kontrola.mjs` měří: poměr h1 k textu těla (≥ 3,5×), `prefers-reduced-motion` při animacích, barevné proměnné (≥ 6), plynulé přechody u tlačítek, vizuál produktu velký nad ohybem.
- Nezávislá revize vzhledu (rubrika 10 bodů v `plan/postupy/pristavaci-web.md`) porovnává web s touto úrovní zpracování: je vizuál konkrétní a velký, má hierarchie, pohyb a detaily dotažené, je to uvěřitelně dílo člověka?
- Poznámka: tento vzor sám používá Inter, skleněnou kartu a pilulková tlačítka. To dokazuje, že samotná volba prvku nedělá web „AI“, dělá ho jím obecnost, nesouvislost a chybějící dotažení.
