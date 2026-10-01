#!/usr/bin/env python3
"""Téma 1: Zlomky a desetinná čísla. Vzor pro ostatní témata (formát v _lib.py). Úlohy se liší od ukázky zdarma."""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, fr  # noqa: E402

T = Topic(1, "zlomky", "Zlomky a desetinná čísla",
          "Zlomky jsou na přijímačkách skoro každý rok, samostatně i uvnitř rovnic a slovních úloh. "
          "Počítejte bez kalkulačky a výsledek vždy zkraťte na základní tvar.",
          ["Před sčítáním a odčítáním převeďte zlomky na společného jmenovatele (nejmenší společný násobek).",
           "Dělit zlomkem znamená násobit převrácenou hodnotou: a/b : c/d = a/b · d/c.",
           "Smíšené číslo převeďte na zlomek: 2 1/3 = 7/3. Desetinné číslo na zlomek: 0,25 = 1/4.",
           "U složeného zlomku spočítejte zvlášť čitatel a jmenovatel, pak je vydělte.",
           "Pořadí operací: závorky, pak násobení a dělení, nakonec sčítání a odčítání."])

T.example("Vypočtěte a výsledek zapište v základním tvaru: 3/4 − 1/6 · 3/2",
          ["Nejdřív násobení: 1/6 · 3/2 = 3/12 = 1/4.",
           "Pak odčítání: 3/4 − 1/4 = 2/4.",
           "Zkrátíme dvěma: 2/4 = 1/2."],
          "1/2", F(3, 4) - F(1, 6) * F(3, 2) == F(1, 2))

# ---------------------------------------------------------------- Základ
r = F(5, 6) - F(3, 8)
T.task(1, "Vypočtěte: 5/6 − 3/8", fr(r),
       ["Společný jmenovatel čísel 6 a 8 je 24.", "5/6 = 20/24, 3/8 = 9/24.", "20/24 − 9/24 = 11/24."],
       r == F(11, 24) and F(5, 6) == F(20, 24) and F(3, 8) == F(9, 24))

r = F(4, 9) * F(15, 8)
T.task(1, "Vypočtěte a výsledek zkraťte: 4/9 · 15/8", fr(r),
       ["Před násobením krátíme křížem: 4 a 8 dělíme 4, 9 a 15 dělíme 3.", "Dostaneme 1/3 · 5/2.", "1/3 · 5/2 = 5/6."],
       r == F(5, 6))

r = F(7, 10) / F(14, 15)
T.task(1, "Vypočtěte: 7/10 : 14/15", fr(r),
       ["Dělení zlomkem nahradíme násobením převrácenou hodnotou: 7/10 · 15/14.", "Krátíme: 7 a 14 sedmi, 15 a 10 pěti: 1/2 · 3/2.",
        "1/2 · 3/2 = 3/4."],
       r == F(3, 4))

r = F(125, 100)
T.task(1, "Zapište desetinné číslo 1,25 jako zlomek v základním tvaru a jako smíšené číslo.", "5/4 = 1 1/4",
       ["1,25 = 125/100.", "Zkrátíme 25: 125/100 = 5/4.", "5/4 = 4/4 + 1/4 = 1 1/4."],
       r == F(5, 4))

opts = {"3/5": F(3, 5), "0,58": F(58, 100), "4/7": F(4, 7), "5/9": F(5, 9), "0,56": F(56, 100)}
T.task(1, "Které z čísel je největší?", "A",
       ["Převedeme zlomky na desetinná čísla: 3/5 = 0,6; 4/7 ≈ 0,571; 5/9 ≈ 0,556.",
        "Porovnáme: 0,6 > 0,58 > 0,571 > 0,56 > 0,556.", "Největší je 3/5, možnost A."],
       max(opts, key=opts.get) == "3/5",
       kind="choice", options=list(opts), space=1)

# ---------------------------------------------------------------- Jako u zkoušky
r = (2 + F(1, 3)) * F(3, 14) - F(1, 4)
T.task(2, "Vypočtěte: 2 1/3 · 3/14 − 1/4", fr(r),
       ["Smíšené číslo převedeme: 2 1/3 = 7/3.", "7/3 · 3/14 = 21/42 = 1/2.", "1/2 − 1/4 = 2/4 − 1/4 = 1/4."],
       r == F(1, 4) and F(7, 3) * F(3, 14) == F(1, 2))

r = (F(3, 4) + F(5, 6)) / (F(5, 3) - F(1, 2))
T.task(2, "Vypočtěte složený zlomek: (3/4 + 5/6) / (5/3 − 1/2)", fr(r),
       ["Čitatel: 3/4 + 5/6 = 9/12 + 10/12 = 19/12.", "Jmenovatel: 5/3 − 1/2 = 10/6 − 3/6 = 7/6.",
        "19/12 : 7/6 = 19/12 · 6/7 = 114/84 = 19/14."],
       r == F(19, 14) and F(3, 4) + F(5, 6) == F(19, 12) and F(5, 3) - F(1, 2) == F(7, 6))

r = F(15, 10) * F(2, 3) + F(25, 100) / F(1, 2)
T.task(2, "Vypočtěte a výsledek zapište zlomkem v základním tvaru: 1,5 · 2/3 + 0,25 : 1/2", fr(r),
       ["Desetinná čísla na zlomky: 1,5 = 3/2 a 0,25 = 1/4.", "Násobení: 3/2 · 2/3 = 1.", "Dělení: 1/4 : 1/2 = 1/4 · 2 = 1/2.",
        "Součet: 1 + 1/2 = 3/2."],
       r == F(3, 2))

x = (F(7, 12) - F(1, 4)) / F(2, 3)
T.task(2, "Řešte rovnici: 2/3 · x + 1/4 = 7/12", f"x = {fr(x)}",
       ["Odečteme 1/4: 2/3 · x = 7/12 − 3/12 = 4/12 = 1/3.", "Vydělíme 2/3: x = 1/3 · 3/2 = 1/2.",
        "Zkouška: 2/3 · 1/2 + 1/4 = 1/3 + 1/4 = 4/12 + 3/12 = 7/12. ✓"],
       x == F(1, 2) and F(2, 3) * x + F(1, 4) == F(7, 12))

stmts = [F(2, 5) + F(1, 5) == F(3, 10), F(3, 4) / F(3, 8) == 2, F(1, 3) * 6 == 2]
T.task(2, "Platí tato tvrzení?", "NE, ANO, ANO",
       ["2/5 + 1/5 = 3/5, ne 3/10. Sčítáme jen čitatele, jmenovatel zůstává. Tvrzení neplatí.",
        "3/4 : 3/8 = 3/4 · 8/3 = 24/12 = 2. Platí.", "1/3 · 6 = 6/3 = 2. Platí."],
       stmts == [False, True, True], kind="yesno",
       options=["2/5 + 1/5 = 3/10", "3/4 : 3/8 = 2", "Třetina z šesti je 2."], space=1)

T.task(2, "Tablet stál 4 800 Kč. V akci ho prodávali za 5/8 původní ceny. O kolik korun zlevnil?", "o 1 800 Kč",
       ["Akční cena: 5/8 · 4 800 = 3 000 Kč.", "Sleva: 4 800 − 3 000 = 1 800 Kč.",
        "Jinak: zlevnil o 3/8 ceny, 3/8 · 4 800 = 1 800 Kč."],
       4800 * F(5, 8) == 3000 and 4800 - 3000 == 1800 == 4800 * F(3, 8))

# ---------------------------------------------------------------- Náročnější
celkem = 60 / (1 - F(2, 5) - F(1, 4))
T.task(3, "Ve třídě si 2/5 žáků vybralo výlet do hor, 1/4 žáků výlet k vodě a zbylých 21 žáků muzeum. "
          "Kolik žáků vybíralo?", "60 žáků",
       ["Hory a voda dohromady: 2/5 + 1/4 = 8/20 + 5/20 = 13/20 žáků.", "Na muzeum zbývá 1 − 13/20 = 7/20 žáků, to je 21 žáků.",
        "1/20 žáků … 21 : 7 = 3 žáci, celá třída 20 · 3 = 60 žáků.",
        "Zkouška: 2/5 ze 60 = 24, 1/4 ze 60 = 15, 24 + 15 + 21 = 60. ✓"],
       21 / (1 - F(2, 5) - F(1, 4)) == 60 and F(2, 5) * 60 + F(1, 4) * 60 + 21 == 60, space=4)

hod = 1 / (F(1, 4) + F(1, 6) - F(1, 12))
T.task(3, "Bazén napustí první přívod za 4 hodiny, druhý za 6 hodin. Odtok ho vypustí za 12 hodin. "
          "Za jak dlouho se bazén naplní, když jsou otevřené oba přívody i odtok?", "za 3 hodiny",
       ["Za hodinu napustí první přívod 1/4 bazénu, druhý 1/6 bazénu, odtok vypustí 1/12.",
        "Za hodinu přibude 1/4 + 1/6 − 1/12 = 3/12 + 2/12 − 1/12 = 4/12 = 1/3 bazénu.", "Celý bazén se naplní za 3 hodiny."],
       hod == 3, space=4)

r = (F(1, 2) - F(1, 3)) / (F(1, 3) - F(1, 4)) - F(4, 5) * (1 + F(1, 4))
T.task(3, "Vypočtěte: (1/2 − 1/3) : (1/3 − 1/4) − 4/5 · (1 + 1/4)", fr(r),
       ["První závorka: 1/2 − 1/3 = 3/6 − 2/6 = 1/6.", "Druhá závorka: 1/3 − 1/4 = 4/12 − 3/12 = 1/12.",
        "Podíl: 1/6 : 1/12 = 1/6 · 12 = 2.", "Součin: 4/5 · 5/4 = 1.", "Rozdíl: 2 − 1 = 1."],
       r == 1, space=4)

x = F(1, 4) / (F(5, 8) - F(1, 2))
T.task(3, "Řešte rovnici: x/2 + 1/4 = 5/8 · x", f"x = {fr(x)}",
       ["Odečteme x/2 od obou stran: 1/4 = 5/8 · x − 4/8 · x = 1/8 · x.", "Vynásobíme osmi: x = 2.",
        "Zkouška: 2/2 + 1/4 = 5/4 a 5/8 · 2 = 10/8 = 5/4. ✓"],
       x == 2 and F(2, 2) + F(1, 4) == F(5, 8) * 2, space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
r = F(5, 12) + F(3, 8) - F(1, 6)
T.diagnostic("Vypočtěte: 5/12 + 3/8 − 1/6", fr(r),
             ["Společný jmenovatel čísel 12, 8 a 6 je 24.", "10/24 + 9/24 − 4/24 = 15/24.", "Zkrátíme třemi: 15/24 = 5/8."],
             r == F(5, 8))
r = (F(2, 3) - F(1, 4)) / (1 + F(1, 4))
T.diagnostic("Vypočtěte: (2/3 − 1/4) : (1 + 1/4)", fr(r),
             ["Čitatel: 2/3 − 1/4 = 8/12 − 3/12 = 5/12.", "Jmenovatel: 1 + 1/4 = 5/4.", "5/12 : 5/4 = 5/12 · 4/5 = 20/60 = 1/3."],
             r == F(1, 3))

T.save()
