# Plán produktu: Ano, beru (svatební plánovač)

Doplněno zpětně 2026-10-01 podle šablony (produkt byl spuštěn 2026-09-30 před zavedením šablony, viz FAILS.md).

## 1. Poptávka
- Google Trends CZ (2026-09-30): „svatební plánovač“ ≈ 1/400 hledanosti „pracovní listy“, tedy velmi malá (`plan/research-2026-10-01.md`, kandidát H).
- Sezóna: zásnuby XII–II, plánování svateb hlavně I–IV. Teď (říjen) mimo sezónu.
- Konkurence placená: budemesebrat.com 333 Kč (Sheets), Svatebníček 549/849 Kč, Moje svatba 799 Kč/rok.

## 1b. Cílová skupina
- Hledá, používá i platí: snoubenci (hlavně nevěsty 25–35 let). Rodiče výjimečně jako dárek. Nezletilí nejsou cílová skupina.

## 3. Ekonomika
- Cena 349 Kč, náklady 0 Kč kromě domény (~200 Kč). Placená reklama zatím ne (malá hledanost, mimo sezónu).

## 4. Test poptávky
- Běží pasivně přes SEO (10 článků + kalkulačka, IndexNow, Search Console). Vyhodnotit v únoru 2027: návštěvy, objednávky, zaplaceno. Bez prodejů do 28. 2. 2027 → nic dalšího nevkládat.

## 5. Role Ondřeje
- Jen autorizace (Search Console hotovo) a schválení případného rozpočtu na Sklik v sezóně.

## 6. Rizika
- Ochranná známka neověřena (riziko přijato 2026-09-30). Malý trh, sezónnost.

## 7. Metriky a vyhodnocení
- Anonymní trychtýř (`web/src/components/Beacon.tsx` → `/api/e` → `/api/stats`): úvod a články → klik na Koupit → objednávka → zaplaceno, podle zařízení a zdroje.
- Proč ne: anketa na úvodu a u každého článku. Objednávky a platby ze serveru.
- Závěry: `/api/stats` → `findings`. Vyhodnocení do `plan/anoberu-vyhodnoceni.md`.
