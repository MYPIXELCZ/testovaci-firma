#!/usr/bin/env python3
"""Tematické stránky s příklady (procenta, rovnice) → src/content/temata/{slug}.json.

    python3 printopia/content/temata.py

Každý výsledek i mezikrok se ověří přes fractions.Fraction; když nesedí, skript spadne.
Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky (ne převzaté z testů CERMAT).
Cílová skupina: úlohy řeší žák (uživatel); stránky jsou výukový obsah zdarma, prodejní sdělení míří na dospělé.
"""
import json
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "content" / "temata"


def page(slug, title, h1, description, lead, tips, tasks):
    OUT.mkdir(parents=True, exist_ok=True)
    data = {"slug": slug, "title": title, "h1": h1, "description": description, "lead": lead, "tips": tips, "tasks": tasks}
    (OUT / f"{slug}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(slug, len(tasks), "úloh ověřeno")


def t(topic, text, answer, steps, check):
    assert check, f"Ověření selhalo: {text}"
    return {"topic": topic, "text": text, "answer": answer, "steps": steps}


# ------------------------------------------------------------------ Procenta
p = []
p.append(t("Část z celku", "Kolik je 15 % z 240?", "36",
           ["15 % = 15/100 = 0,15.", "0,15 · 240 = 36."], F(15, 100) * 240 == 36))
p.append(t("Kolik procent", "Kolik procent je 18 z 72?", "25 %",
           ["Podíl části a celku: 18 : 72 = 1/4.", "1/4 = 0,25 = 25 %."], F(18, 72) == F(1, 4)))
p.append(t("Zdražení", "Bunda stála 1 800 Kč a zdražila o 15 %. Kolik stojí teď?", "2 070 Kč",
           ["Nová cena je 100 % + 15 % = 115 % původní ceny.", "1,15 · 1 800 = 2 070 Kč."], F(115, 100) * 1800 == 2070))
p.append(t("Původní cena", "Po slevě 20 % stojí kolo 6 400 Kč. Kolik stálo před slevou?", "8 000 Kč",
           ["Po slevě 20 % platíme 80 % původní ceny.", "80 % … 6 400 Kč, tedy 1 % … 80 Kč.", "100 % … 8 000 Kč.",
            "Zkouška: 20 % z 8 000 = 1 600, 8 000 − 1 600 = 6 400. ✓"],
           6400 / F(80, 100) == 8000 and 8000 - F(20, 100) * 8000 == 6400))
p.append(t("Dvě změny za sebou", "Cena se nejdřív zvýšila o 10 % a pak snížila o 10 %. Jak se změnila oproti původní ceně?",
           "klesla o 1 %",
           ["Po zdražení: 1,1 násobek původní ceny.", "Po zlevnění: 0,9 · 1,1 = 0,99 původní ceny.",
            "0,99 = 99 %, cena tedy klesla o 1 %.", "Pozor: nevrátí se na původní cenu, protože 10 % se podruhé počítá z vyšší částky."],
           F(11, 10) * F(9, 10) == F(99, 100)))
p.append(t("Podíl ve skupině", "Ve třídě je 12 chlapců a 18 dívek. Kolik procent třídy tvoří chlapci?", "40 %",
           ["Celkem je 12 + 18 = 30 žáků.", "12 : 30 = 2/5 = 0,4 = 40 %."], F(12, 30) == F(2, 5)))
p.append(t("Roztoky", "Ve 40 kg roztoku je 15 % soli. Kolik kg vody musíme přidat, aby měl roztok 10 % soli?", "20 kg",
           ["Sůl: 15 % ze 40 kg = 6 kg. Přidáním vody se množství soli nemění.",
            "6 kg má být 10 % nového roztoku, celý roztok tedy váží 6 : 0,1 = 60 kg.",
            "Přidáme 60 − 40 = 20 kg vody."],
           F(15, 100) * 40 == 6 and 6 / F(10, 100) == 60))
p.append(t("Úrok", "Na účet uložíme 20 000 Kč s úrokem 3 % ročně (bez daně). Kolik na něm bude po dvou letech, když úroky necháme na účtu?",
           "21 218 Kč",
           ["Po 1. roce: 20 000 · 1,03 = 20 600 Kč.", "Po 2. roce se úročí i loňský úrok: 20 600 · 1,03 = 21 218 Kč."],
           20000 * F(103, 100) == 20600 and 20600 * F(103, 100) == 21218))
page("procenta-prijimacky", "Procenta na přijímačky: příklady s postupem řešení",
     "Procenta na přijímačky: příklady s postupem",
     "8 příkladů na procenta ve stylu přijímaček z matematiky: část z celku, zdražení a sleva, dvě změny za sebou, roztoky a úrok. S postupem řešení.",
     "Procenta jsou v přijímačkách hlavně ve slovních úlohách: zdražení, slevy, roztoky nebo úroky. Tady je 8 příkladů od základů po složitější. Nejdřív počítejte sami, postup si rozbalte až potom.",
     ["1 % je setina celku: 1 % ze 300 je 3.", "Zdražení o p % = násobení číslem 1 + p/100, sleva o p % = násobení 1 − p/100.",
      "Když znáte cenu po slevě, dělte, ne násobte: původní cena = cena po slevě : 0,8 (u slevy 20 %).",
      "Dvě procentní změny za sebou se násobí, nesčítají.", "U roztoků se při ředění mění jen voda, množství látky zůstává."], p)

# ------------------------------------------------------------------ Rovnice
r = []
x = F(12)
r.append(t("Lineární rovnice", "Řešte rovnici: 3x − 7 = 2x + 5", "x = 12",
           ["Neznámé převedeme na levou stranu, čísla na pravou: 3x − 2x = 5 + 7.", "x = 12.",
            "Zkouška: L = 3 · 12 − 7 = 29, P = 2 · 12 + 5 = 29. ✓"], 3 * x - 7 == 2 * x + 5))
x = F(10)
r.append(t("Závorky", "Řešte rovnici: 2(x − 3) = x + 4", "x = 10",
           ["Roznásobíme závorku: 2x − 6 = x + 4.", "2x − x = 4 + 6, tedy x = 10.", "Zkouška: 2 · 7 = 14, 10 + 4 = 14. ✓"],
           2 * (x - 3) == x + 4))
x = F(12)
r.append(t("Zlomky v rovnici", "Řešte rovnici: x/3 + x/4 = 7", "x = 12",
           ["Vynásobíme celou rovnici společným jmenovatelem 12: 4x + 3x = 84.", "7x = 84, tedy x = 12.",
            "Zkouška: 12/3 + 12/4 = 4 + 3 = 7. ✓"], x / 3 + x / 4 == 7))
x = F(7)
r.append(t("Zlomky v rovnici", "Řešte rovnici: (x + 1)/2 − (x − 1)/3 = 2", "x = 7",
           ["Vynásobíme šesti: 3(x + 1) − 2(x − 1) = 12.", "Pozor na znaménko před závorkou: 3x + 3 − 2x + 2 = 12.",
            "x + 5 = 12, tedy x = 7.", "Zkouška: 8/2 − 6/3 = 4 − 2 = 2. ✓"], (x + 1) / 2 - (x - 1) / 3 == 2))
x = F(2)
r.append(t("Závorky", "Řešte rovnici: 5 − 2(3 − x) = 3(x − 1)", "x = 2",
           ["Roznásobíme: 5 − 6 + 2x = 3x − 3.", "−1 + 2x = 3x − 3.", "2x − 3x = −3 + 1, tedy −x = −2 a x = 2.",
            "Zkouška: L = 5 − 2 · 1 = 3, P = 3 · 1 = 3. ✓"], 5 - 2 * (3 - x) == 3 * (x - 1)))
x = F(9)
r.append(t("Slovní úloha", "Obvod obdélníku je 46 cm, délka je o 5 cm větší než šířka. Jaké má obdélník rozměry?",
           "9 cm a 14 cm",
           ["Šířka x, délka x + 5.", "Obvod: 2(x + x + 5) = 46, tedy 4x + 10 = 46.", "4x = 36, x = 9.",
            "Šířka 9 cm, délka 14 cm. Zkouška: 2 · (9 + 14) = 46. ✓"], 2 * (x + x + 5) == 46))
x = F(26)
r.append(t("Slovní úloha", "Součet tří po sobě jdoucích přirozených čísel je 81. Která to jsou?", "26, 27 a 28",
           ["Čísla označíme x, x + 1, x + 2.", "x + x + 1 + x + 2 = 81, tedy 3x + 3 = 81.", "3x = 78, x = 26."],
           x + (x + 1) + (x + 2) == 81))
tt = F(1, 2)
r.append(t("Pohyb", "V 8:00 vyjel z Brna cyklista rychlostí 18 km/h. V 9:00 za ním vyjelo auto rychlostí 54 km/h. "
                     "V kolik hodin a jak daleko od Brna cyklistu dohoní?", "v 9:30, 27 km od Brna",
           ["Auto jede t hodin, cyklista o hodinu déle: t + 1.", "Dohoní ho, až ujedou stejnou dráhu: 54t = 18(t + 1).",
            "54t = 18t + 18, tedy 36t = 18 a t = 1/2 hodiny.", "Auto vyjelo v 9:00, dohoní ho v 9:30.",
            "Dráha: 54 · 1/2 = 27 km. Zkouška: cyklista 18 · 3/2 = 27 km. ✓"],
           54 * tt == 18 * (tt + 1) and 54 * tt == 27))
page("rovnice-prijimacky", "Rovnice na přijímačky: příklady s postupem řešení",
     "Rovnice na přijímačky: příklady s postupem",
     "8 příkladů na lineární rovnice ve stylu přijímaček z matematiky: závorky, zlomky, slovní úlohy a pohyb. U každého postup krok za krokem a zkouška.",
     "Lineární rovnice jsou v přijímačkách samostatně i uvnitř slovních úloh. Tady je 8 příkladů od jednoduchých po úlohu o pohybu. Nejdřív počítejte sami, postup si rozbalte až potom.",
     ["Co uděláte s jednou stranou rovnice, udělejte i s druhou.", "Zlomků se zbavíte vynásobením celé rovnice společným jmenovatelem.",
      "Minus před závorkou mění znaménka všech členů v závorce.", "U slovní úlohy si nejdřív napište, co je x.",
      "Vždy udělejte zkoušku dosazením do původní rovnice."], r)

# ------------------------------------------------------------------ Slovní úlohy
w = []
tt = F(3, 4)
w.append(t("Pohyb proti sobě", "Z měst vzdálených 105 km vyjeli proti sobě ve stejnou chvíli cyklista rychlostí 20 km/h a auto rychlostí 120 km/h. Za jak dlouho se potkají?",
           "za 45 minut",
           ["Při jízdě proti sobě se rychlosti sčítají: 20 + 120 = 140 km/h.", "Čas = dráha : rychlost = 105 : 140 = 3/4 h.",
            "3/4 hodiny = 45 minut.", "Zkouška: 20 · 3/4 + 120 · 3/4 = 15 + 90 = 105 km. ✓"],
           F(105, 140) == tt and 20 * tt + 120 * tt == 105))
tt = 1 / (F(1, 12) + F(1, 4))
w.append(t("Společná práce", "Malý bagr vykope jámu za 12 hodin, velký za 4 hodiny. Za kolik hodin ji vykopou společně?", "za 3 hodiny",
           ["Malý bagr za hodinu vykope 1/12 jámy, velký 1/4 jámy.", "Společně za hodinu: 1/12 + 1/4 = 1/12 + 3/12 = 4/12 = 1/3 jámy.",
            "Celou jámu tedy vykopou za 3 hodiny."], tt == 3))
x = F(4)
w.append(t("Směsi", "Kolik kg kávy po 400 Kč/kg musíme smíchat s 6 kg kávy po 250 Kč/kg, aby směs stála 310 Kč/kg?", "4 kg",
           ["Dražší kávy je x kg. Cena směsi = součet cen obou druhů.", "400x + 250 · 6 = 310 · (x + 6).",
            "400x + 1 500 = 310x + 1 860, tedy 90x = 360 a x = 4.", "Zkouška: 1 600 + 1 500 = 3 100 Kč za 10 kg = 310 Kč/kg. ✓"],
           400 * x + 250 * 6 == 310 * (x + 6)))
x = F(8)
w.append(t("Věk", "Matka je dnes čtyřikrát starší než dcera. Za 16 let bude jen dvakrát starší. Kolik je dceři dnes?", "8 let",
           ["Dceři je dnes x let, matce 4x.", "Za 16 let: 4x + 16 = 2(x + 16).", "4x + 16 = 2x + 32, tedy 2x = 16 a x = 8.",
            "Zkouška: dnes 8 a 32 let, za 16 let 24 a 48 let, 48 = 2 · 24. ✓"], 4 * x + 16 == 2 * (x + 16)))
x = F(360)
w.append(t("Části celku", "Jana utratila 1/3 kapesného za kino a 1/4 za jídlo. Zbylo jí 150 Kč. Kolik měla kapesného?", "360 Kč",
           ["Utratila 1/3 + 1/4 = 4/12 + 3/12 = 7/12 kapesného.", "Zbylo 5/12 kapesného, to je 150 Kč.", "1/12 … 30 Kč, celé kapesné 12 · 30 = 360 Kč.",
            "Zkouška: 120 + 90 = 210 Kč, 360 − 210 = 150 Kč. ✓"], x - x / 3 - x / 4 == 150))
x = F(12)
w.append(t("Pohyb stejným směrem", "Chodec vyšel rychlostí 5 km/h. Za 1 hodinu 12 minut za ním vyjel cyklista rychlostí 20 km/h. Za kolik minut chodce dohoní?", "za 24 minut",
           ["1 h 12 min = 1,2 h. Za tu dobu ujde chodec 5 · 1,2 = 6 km.", "Cyklista se každou hodinu přiblíží o 20 − 5 = 15 km.",
            "Náskok 6 km dožene za 6 : 15 = 0,4 h = 24 minut.", "Zkouška: cyklista 20 · 0,4 = 8 km, chodec 5 · 1,6 = 8 km. ✓"],
           5 * F(6, 5) == 6 and F(6, 15) * 60 == 24 and 20 * F(2, 5) == 5 * (F(6, 5) + F(2, 5))))
x = F(21)
w.append(t("Počty kusů", "V ohradě jsou slepice a králíci, celkem 35 hlav a 98 nohou. Kolik je slepic?", "21 slepic",
           ["Slepic je x, králíků 35 − x.", "Nohy: 2x + 4(35 − x) = 98, tedy 140 − 2x = 98.", "2x = 42, x = 21 slepic a 14 králíků.",
            "Zkouška: 42 + 56 = 98 nohou. ✓"], 2 * x + 4 * (35 - x) == 98))
k = F(3, 2)
w.append(t("Úměrnost", "6 stejných čerpadel vyčerpá nádrž za 9 hodin. Za kolik hodin ji vyčerpají 4 taková čerpadla?", "za 13,5 hodiny",
           ["Méně čerpadel = víc času: nepřímá úměrnost.", "Čerpadlohodiny: 6 · 9 = 54.", "4 čerpadla: 54 : 4 = 13,5 hodiny."],
           F(6 * 9, 4) == F(27, 2)))
page("slovni-ulohy-prijimacky", "Slovní úlohy na přijímačky: příklady s postupem řešení",
     "Slovní úlohy na přijímačky: příklady s postupem",
     "8 slovních úloh ve stylu přijímaček z matematiky: pohyb, společná práce, směsi, věk, části celku a úměrnost. U každé postup řešení a zkouška.",
     "Slovní úlohy dělají v přijímačkách největší potíže, protože je potřeba nejdřív převést text na výpočet. Tady je 8 nejčastějších typů. Nejdřív počítejte sami, postup si rozbalte až potom.",
     ["Nejdřív si napište, co je neznámá x, a všechno ostatní vyjádřete pomocí ní.", "Pohyb proti sobě: rychlosti se sčítají. Stejným směrem: odčítají.",
      "Společná práce: sčítají se části práce za hodinu (1/a + 1/b), ne časy.", "Směsi: cena (nebo množství látky) celé směsi = součet cen jednotlivých částí.",
      "Na konci vždy zkouška dosazením do zadání, ne do rovnice."], w)
