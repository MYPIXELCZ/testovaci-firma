# Akce na tržby (živý žebříček)

Pojistka z FAILS.md 2026-10-01 17:17: čekání na událost s pravděpodobností blízkou nule není práce. Tady je vždy seřazený seznam kroků, které
šanci na první tržbu zvyšují. **P7** = odhad pravděpodobnosti aspoň jedné zaplacené objednávky z té akce do 7 dní (odhad, ne měření).
Stav: `další` (dělat teď), `běží`, `research`, `čeká na Ondřeje` (jen autorizace/rozhodnutí), `hotovo`, `zamítnuto`. Stop hook vypíše první řádek `další` nebo `research`.
V každém probuzení udělat aspoň jeden krok z nejvyšší akce a přehodnotit P7 podle čísel.

| # | Akce | P7 | Stav | Další krok |
|---|------|----|------|-----------|
| 1 | Zboží.cz a Heureka: produktový feed sady přijímaček (lidé s nákupním záměrem, ceny kniha vs. 349 Kč) | 10–15 % | další | Ondřej registroval provozovnu 2026-10-01 17:4x a odsouhlasil podmínky. Nabídka je ŽIVÁ od 21:2x (kampaň Nákupy id 7986551, 30 Kč/den), formální schválení do 5 prac. dnů. Kontrolovat: https://www.zbozi.cz/hledej/?q=printopia a živé hledání na search.seznam.cz (skupina Nabídky ze Zboží.cz), `src=zbozi` v `/api/stats`; po 14 dnech `plan/zbozi-vyhodnoceni.md` |
| 2 | Sklik obsahová síť: zobrazení rodičům (zájmy, témata), klik 1–2 Kč | 6–22 % šance na 1 objednávku za 82 Kč | zamítnuto (zatím) | Research hotov (`plan/postupy/sklik-obsahova-sit.md`): průměrné CPC 3,93 Kč, 21 prokliků za 82 Kč, rodiče všech ročníků, dětské weby nejdou vyloučit v API. Až s rozpočtem aspoň 400 Kč |
| 3 | Nabídka s nízkou bariérou: úvodní test + plán za 49 Kč nebo jedno téma za 79 Kč místo jen sady za 349 Kč | zvyšuje konverzi 3–5× | čeká na kanál | Návrh hotový (`plan/nabidka-printopia.md`); implementovat po prvním kanálu s reálnými návštěvami (akce 1 nebo 2) |
| 4 | Soukromá reklama Google/Meta (Ondřej platí mimo účetnictví), rodiče deváťáků na Facebooku | 30 % při ~500 Kč | čeká na Ondřeje | Předložit Ondřejovi konkrétní číslo a očekávaný výsledek až po akcích 1–3 |
| 5 | B2B licence sady doučovacím centrům a učitelům (kontakt přes formulář webu, ne hromadný e-mail) | 5–10 % | čeká na Ondřeje | Právní riziko (zákon 480/2004 §7): Ondřej rozhodne |
| 6 | Sklik skupina „Testy“ (cermat testy, cermat přijímačky) | ~5 % | běží | Sledovat `sklik_api.py --stats` |
| 7 | SEO tematické stránky Printopie a články anoberu | <3 % | běží | Search Console (Ondřej ověří), IndexNow hotovo |
