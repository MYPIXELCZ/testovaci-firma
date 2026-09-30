# Printopia: test poptávky (přijímačky z matiky po tématech)

Testovací web podle `plan/prijimacky.md` (oddíl 4). Nic se neprodává: stránka Koupit jen sbírá e-maily
se souhlasem (GDPR text schválil Ondřej 2026-10-01).

- Vercel projekt `printopia` (prj_2qqb7t2Wi8muOarlj04j6vK8lQOP), root `printopia`, domény printopia.cz + www (308).
- Blob `printopia-leads` (privátní, fra1): `leads/{hash}.json`.
- Měření: runtime logy s `{"ev":"visit"|"buy_click"|"lead"}` a `src` (utm_source).
- Ukázka: `python3 content/ukazka.py && node scripts/render-ukazka.mjs` (výsledky ověřené přes Fraction).
- Test: `npm run test:e2e`.
- Kampaň Sklik: `marketing/sklik.py`.
