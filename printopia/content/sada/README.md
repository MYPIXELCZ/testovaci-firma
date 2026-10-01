# Jak psát tematické listy sady (zadání pro autora tématu)

Produkt: PDF pracovní listy k tisku na jednotnou přijímací zkoušku z matematiky (4leté obory, 9. třída), cena 349 Kč. Platí rodiče, úlohy řeší deváťák. Texty česky, přesně, bez vaty. Podklady o zkoušce: `plan/postupy/sbirka-prijimacky.md` (struktura testu, váhy témat, didaktika, právo).

## Co vytvořit
Pro každé přidělené téma jeden soubor `printopia/content/sada/NN_slug.py` podle vzoru `01_zlomky.py` (čti ho celý) a formátu v `_lib.py`:
- `Topic(num, slug, title, intro, tips)`: intro 1–2 věty (kde se téma v testu objevuje a proč), 4–6 tipů „na co si dát pozor“ včetně typických chyb žáků.
- `T.example(...)`: jeden řešený příklad s postupem (typický pro zkoušku).
- `T.task(level, ...)`: **14–16 úloh**, úrovně 1 Základ (4–5), 2 Jako u zkoušky (6–7), 3 Náročnější (3–4), seřazené podle úrovně. Mix typů jako u zkoušky: otevřené s výsledkem, otevřené s postupem, `choice` (5 možností A–E, `answer` začíná písmenem), `yesno` (výroky, `answer` např. „ANO, NE, ANO“), případně `construct`. Každá úloha má `steps` (postup krok za krokem, 2–6 kroků, u slovních úloh se zkouškou) a **`check`: výraz, který výsledek i klíčové mezikroky ověří výpočtem v Pythonu** (fractions.Fraction, math, sympy není k dispozici, počítej ručně přes Fraction/int/float s tolerancí). Když ověření neprojde, skript spadne: tak má být.
- `T.diagnostic(...)` dvakrát: dvě úlohy tématu do úvodního testu (úroveň jako u zkoušky, jiné než na listu).
- `T.save()` na konci. Skript spusť: `python3 printopia/content/sada/NN_slug.py` (musí vypsat „ověřeno“).

## Pravidla (porušení = nepoužitelné)
- **Úlohy jsou vlastní.** Nepřebírej ani neupravuj úlohy CERMAT (ani „stejná úloha s jinými čísly“); čerpat smíš jen styl, typ úlohy a váhy témat. Nikdy nepiš, že jde o „oficiální“ úlohy.
- **Správnost je všechno.** Každé zadání jednoznačné, s jedním správným výsledkem, čísla „hezká“ (bez kalkulačky, jako u zkoušky), výsledky v základním tvaru. U `choice` jsou distraktory pravděpodobné chyby žáků (např. špatné procento, zapomenutý krok), ne náhodná čísla. Zkontroluj, že žádná jiná možnost není také správně.
- Zápis: zlomek `a/b` (vysází se nad sebou, i `x/2`), násobení „·“, dělení „:“, minus „−“ (U+2212), desetinná čárka, tisíce s mezerou (`12 500`), jednotky s mezerou (`5 cm`, `cm²`, `cm³`), české uvozovky „…“. Poměr piš s dvojtečkou (`3 : 5`), ne s lomítkem. Lomítko jen pro zlomky a složený zlomek ve tvaru `(a) / (b)`. Mocniny: `3²`, `10⁻²`, odmocniny `√49`.
- Čeština jako od korektora: pády, čárky, žádné kostrbaté věty. Reálné situace (ceny, jízda, brigáda), žádné vymyšlené osoby s divnými jmény, žádné značky.
- Obrázky (geometrie, grafy, tabulky): volitelný parametr `figure` = inline SVG (viewBox, tahy `stroke="#1c2230"`, bez fontů mimo `font-family="Inter,Arial"`), rozměry se přizpůsobí (max 62 × 42 mm). Obrázek musí odpovídat zadání (čísla v obrázku = čísla v textu) a geometrii ověř výpočtem. Tabulky radši jako text.
- **Neměň** `_lib.py`, `scripts/*`, `01_zlomky.py`, ani cizí soubory. Nespouštěj `scripts/render-sada.mjs` (renderuje ho vedoucí najednou). Necommituj.

## Výstup
Stručně (max 10 řádků): soubory, počet úloh a typů, cokoli podezřelého nebo co nešlo ověřit výpočtem.
