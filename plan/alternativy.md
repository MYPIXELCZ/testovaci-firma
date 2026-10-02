# Alternativní businessy (portfolio gate, FAILS.md 2026-10-02 13:34)

Pravidlo: dokud žádný aktivní business nemá verdikt „ověřitelné do 3 dnů: ANO“ a „dostatečný prodej: ANO“ (`plan/verdikt.py`), hledá se alternativa.

**Cíl (Ondřej 2026-10-02 13:46):** 3 000 Kč měsíčně není cíl. Hledáme buď (A) **škálovatelný business**: zisk ≥ 10 000 Kč měsíčně hned, nebo doložená cesta k němu do ~6 měsíců (Ondřej 14:16) (Ondřej 14:13: nemusí to být zisk první měsíc, perspektiva musí být dlouhodobá; v `plan/verdikt.py` parametry `--rust-mesicne` a `--horizont`, růst s odůvodněním) s cestou k desítkám tisíc, kolísání OK (např. 50 000 → 10 000 → 15 000), nebo (B) **plně pasivní business**: po spuštění žádná práce, náklady ≤ ⅓ tržeb (tržby 3 000, náklad 1 000, zisk 2 000). Čísla níže (tržby při 3 000 Kč cíli) jsou proto jen horní odhad; podle nového cíle neprojde ani jeden kandidát přes Seznam.
V každém probuzení posunout nejlepšího kandidáta o krok (research, test 72 hodin, rozhodnutí). Stav vypisuje `tools/stav.py` (sekce portfolio).

## Rozšíření prostoru řešení (Ondřej 2026-10-02 14:20)
Plně automatizovaný produkt zůstává preferovaný, ale smí se hledat i: **(2) hotové výrobky z Ondřejovy 3D tiskárny** (katalogový produkt, ne zakázkový tisk; Ondřej akceptuje tisk, balení a expedici u schváleného produktu) a **(3) zakázkový web, systém nebo e-shop** (custom, vyšší cena za zakázku, stavím já).
Co u nich rozhoduje (moje výhrady, jednou): 3D tisk: ruční práce na každou objednávku (balení, expedice, vratky), nízká marže na kus a strop jedné tiskárny; licence cizích modelů (Printables a Thingiverse často zakazují komerční použití, jen vlastní návrhy nebo komerční licence); odpovědnost za výrobek a GPSR; poptávku ověřit ještě před tiskem (nabídka „vyrobíme na objednávku“ na Zboží.cz a Fleru). Zakázkové systémy: vyšší cena umožní cíl A už s 1 až 3 zakázkami měsíčně, ale dlouhý obchodní cyklus a každá zakázka je práce; vyhodnotit jako samostatného kandidáta.

## Aktivní businessy a jejich verdikt (stav 2026-10-02)
| Business | Verdikt | Poznámka |
|---|---|---|
| Printopia (sada přijímaček 349 Kč) | NE / NE | Seznam: ~3 návštěvy za 3 dny, tržby ~100 Kč měsíčně při dnešní hledanosti |
| Anoberu (svatební plánovač 349 Kč) | NE / NE | Seznam: 0,1 návštěvy za 3 dny, sezóna až od prosince |
| A2 čeština pro cizince | NE / NE | zamítnuto, nepostaveno |

## Kandidáti proti Seznamu (Sklik hledanost, předpoklady: konverze na platbu 1,5 %, na poptávku 5 %, CTR 3 %, 150 Kč na dokoupené kliky)
| Kandidát | Cena | Ověřitelné do 3 dnů | Dosažitelné návštěvy | Tržby měsíčně z hledání | Ve špičce |
|---|---:|---|---:|---:|---:|
| Web na klíč (`alt-web`) | 4 990 | NE (CPC kolem 60 Kč) | 3,0 | 375 | 555 |
| E-shop na klíč (`alt-eshop`) | 9 990 | NE | 2,7 | 90 | 234 |
| Audit webu / SEO (`alt-audit`) | 1 990 | ANO (jen dokoupením kliků) | 79 | 30 | 4 502 |
| Překlady (`alt-preklady`) | 600 | ANO | 20 | 60 | 2 206 |
| Vzory smluv (`alt-smlouvy`) | 199 | ANO | 153 | 84 | 187 |
| Životopis na míru (`alt-zivotopis`) | 590 | ANO | 35 | 13 | 29 |
| Korektury (`alt-korektura`) | 900 | ANO | 33 | 9 | 134 |
| Texty na web (`alt-texty`) | 1 500 | ANO | 30 | 26 | 44 |
| Online pozvánky (`alt-pozvanky`) | 290 | ANO | 48 | 25 | 96 |
| Generátor životopisu (`alt-generator`) | 149 | ANO | 40 | 8 | 15 |
| Loga, prezentace, Excel na míru | 990 až 1 500 | ANO | ~30 | 0 až 4 | do 21 |

**Závěr:** žádný kandidát nemá „dostatečný prodej“ (cíl 3 000 Kč měsíčně) přes hledání na Seznamu, a to ani ve špičce. Problém není jen produkt, ale **kanál**: Seznam
vyhledávání má pro všechny naše nápady hledanost v desítkách až nízkých stovkách měsíčně. Jakýkoli další produkt postavený na „najdou nás ve Skliku“ skončí stejně.

## Modely, které se dají ověřit do 72 hodin bez objemu hledání
1. **Produktizovaná služba, kterou doděláme my (AI) a prodáme přes kanály s vlastní návštěvností** (Bazoš, Sbazar, Firmy.cz, lokální skupiny, přímá nabídka firmám přes kontaktní formuláře webu).
   Kandidát č. 1: **„Web za 24 hodin“** (jednostránkový nebo malý web pro živnostníky a malé firmy, 3 990 až 4 990 Kč + 290 Kč měsíčně správa), doména `webprodava.cz` (zdarma, Ondřejova).
   Ověření: za 72 hodin aspoň 1 závazná poptávka s cenovou nabídkou. Náklad 0 Kč. Dostatečný prodej podle nového cíle (A): ≥ 2 zakázky měsíčně (2 × 4 990 ≈ 10 000 Kč zisku, náklad skoro 0), tedy ≈ 8–10 poptávek měsíčně při 20–30 % uzavření; 1 závazná poptávka za 72 h tomu odpovídá. Přírůstek: opakované platby za správu (20 klientů × 290 Kč = 5 800 Kč měsíčně). Není pasivní (každý web = práce Clauda), proto platí jen kritérium A.
   **Korekce po průzkumu 2026-10-02:** Bazoš/Sbazar mají slabou poptávku po webu (jeden inzerát ≈ 0,5 zakázky měsíčně, ~2 300 Kč tržeb), P(≥1 závazná poptávka za 72 h) ≈ 20 až 25 %, samotné kanály kritérium A (10 000 Kč zisku) nesplní. Kandidát zůstává jen jako levná sonda zájmu (147 Kč) a vyžaduje rozhodnutí o riziku Vercel Terms čl. 11 (hosting cizích webů). Formální verdikt `plan/verdikt.py alt-web`: NE/NE.
   Potřebuje od Ondřeje: schválení obchodních podmínek služby (právo), účet na inzertním portálu (ověření telefonem), souhlas s tím, že odpovídám zákazníkům z firemního e-mailu.
2. **Soukromá placená reklama Ondřeje (Google/Meta) na stávající produkt** jako jednorázový test poptávky: ověřitelné do 3 dnů (asi 100 kliků za 500 Kč), ale strop produktu zůstává nízký (viz verdikt).
3. **SEO, afiliace, obsahové weby**: kanál je pomalý (týdny až měsíce), pravidlo 3 dnů nesplňují. Nezačínat.

## Další krok
Rozhodnutí Ondřeje o variantě 1 (jedna odpověď: „ano, test webu“ a schválení podmínek). Do té doby připravuji jen texty a podmínky jako návrh, nic nestavím (verdikt NE vyžaduje jeho výjimku).
