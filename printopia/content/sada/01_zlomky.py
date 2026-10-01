#!/usr/bin/env python3
"""Téma 1: Zlomky, desetinná čísla, mocniny a odmocniny. Vzor pro ostatní témata (formát v _lib.py).
Úlohy se liší od ukázky zdarma. Úlohy na mocniny a odmocniny se ověřují přímo z textu zadání (funkce ev)."""
import re
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, fr  # noqa: E402

# ------------------------------------------------------------------ ověření přímo z textu zadání
_TOK = re.compile(r"[0-9]+(?:,[0-9]+)?|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|√|[-+*/()]")
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def rt(x):
    """Druhá odmocnina z nezáporného racionálního čísla; spadne, když výsledek není racionální."""
    x = F(x)
    assert x >= 0, f"odmocnina ze záporného čísla: {x}"
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    assert F(n * n, d * d) == x, f"√{x} není racionální"
    return F(n, d)


def ev(s: str) -> F:
    """Vyhodnotí číselný výraz zapsaný tak, jak se sází (·, :, −, a/b, 2⁻³, √49, √(a/b), 1,5, smíšená čísla)
    přesně přes Fraction. Stejný řetězec tedy jde do zadání i do ověření."""
    s = re.sub(r"(\d+) (\d+/\d+)", r"(\1+\2)", s)
    s = s.replace("−", "-").replace("·", "*").replace(":", "/").replace(" ", "")
    toks = _TOK.findall(s)
    assert "".join(toks) == s, f"nerozpoznané znaky ve výrazu: {s}"
    out, prev, root = [], None, False
    for t in toks:
        k = "n" if t[0] in "0123456789" else "s" if t[0] in "⁰¹²³⁴⁵⁶⁷⁸⁹⁻" else "r" if t == "√" else t
        assert not (k == "n" and prev in ("n", "s", ")")), f"chybí operátor před číslem: {s}"
        if prev in ("n", "s", ")") and k in ("(", "r"):
            out.append("*")
        if k == "n":
            out.append(f"F('{t.replace(',', '.')}')" if not root else f"(F('{t.replace(',', '.')}'))")
        elif k == "s":
            out.append(f"**({t.translate(_SUP)})")
        elif k == "r":
            out.append("rt")
        else:
            assert not (root and k != "("), f"za √ má následovat číslo nebo závorka: {s}"
            out.append(t)
        root = k == "r"
        prev = k
    return F(eval("".join(out), {"__builtins__": {}, "F": F, "rt": rt}))


# Tvrzení z tipů (aby v nich nebyla chyba)
assert ev("(−3)²") == 9 and ev("−3²") == -9 and ev("(−2)³") == -8
assert ev("2⁻³") == F(1, 8) and ev("(2/3)⁻²") == F(9, 4) and ev("5⁰") == 1 and ev("10⁻²") == F(1, 100)
assert ev("√49") == 7 and 17 ** 2 == 289 and ev("√289") == 17
assert ev("√(9 + 16)") == 5 and ev("√9 + √16") == 7 and ev("√(4 · 25)") == ev("√4") * ev("√25") == 10
assert ev("2 1/3") == F(7, 3) and ev("1,5") == F(3, 2)

T = Topic(1, "zlomky", "Zlomky, desetinná čísla, mocniny a odmocniny",
          "Číselné výrazy se zlomky, desetinnými čísly, mocninami a odmocninami jsou u zkoušky každý rok, hlavně v úloze 2, "
          "a zlomky se vracejí i v rovnicích a slovních úlohách. Počítejte bez kalkulačky a výsledek vždy zkraťte na základní tvar.",
          ["Před sčítáním a odčítáním převeďte zlomky na společného jmenovatele (nejmenší společný násobek).",
           "Dělit zlomkem znamená násobit převrácenou hodnotou: a/b : c/d = a/b · d/c.",
           "Smíšené číslo převeďte na zlomek: 2 1/3 = 7/3. Desetinné číslo na zlomek: 0,25 = 1/4.",
           "Pořadí operací: nejdřív závorky, mocniny a odmocniny, pak násobení a dělení, nakonec sčítání a odčítání. "
           "U složeného zlomku spočítejte zvlášť čitatel a jmenovatel, pak je vydělte.",
           "Pozor na znaménka: (−3)² = 9, ale −3² = −9, a lichá mocnina záporného čísla je záporná: (−2)³ = −8. "
           "Záporný exponent znamená převrácenou hodnotu: 2⁻³ = 1/8 a (2/3)⁻² = 9/4. Dále 5⁰ = 1 a 10⁻² = 0,01.",
           "Odmocnina je nezáporné číslo, jehož druhá mocnina je číslo pod odmocninou: √49 = 7. Druhé mocniny čísel 11 až 20 máte u zkoušky "
           "na poslední straně sešitu (17² = 289, tedy √289 = 17). Odmocnina ze součtu není součet odmocnin: √(9 + 16) = 5, ne 3 + 4. "
           "Součin odmocnit smíte: √(4 · 25) = 2 · 5."])

q = "(−2)³ + 3² · 5/6 − √81 : 6"
r = ev(q)
T.example(f"Vypočtěte a výsledek zapište v základním tvaru: {q}",
          ["Nejdřív mocniny a odmocnina: (−2)³ = −8, 3² = 9 a √81 = 9.",
           "Pak násobení a dělení: 9 · 5/6 = 45/6 = 15/2 a 9 : 6 = 9/6 = 3/2.",
           "Zbývá sčítání a odčítání: −8 + 15/2 − 3/2 = −8 + 12/2 = −8 + 6.",
           "−8 + 6 = −2."],
          "−2", r == -2 and ev("(−2)³") == -8 and ev("3² · 5/6") == F(15, 2) and ev("√81 : 6") == F(3, 2))

# ---------------------------------------------------------------- Základ
r = F(5, 6) - F(3, 8)
T.task(1, "Vypočtěte: 5/6 − 3/8", fr(r),
       ["Společný jmenovatel čísel 6 a 8 je 24.", "5/6 = 20/24, 3/8 = 9/24.", "20/24 − 9/24 = 11/24."],
       r == F(11, 24) and F(5, 6) == F(20, 24) and F(3, 8) == F(9, 24))

r = F(7, 10) / F(14, 15)
T.task(1, "Vypočtěte: 7/10 : 14/15", fr(r),
       ["Dělení zlomkem nahradíme násobením převrácenou hodnotou: 7/10 · 15/14.", "Krátíme: 7 a 14 sedmi, 15 a 10 pěti: 1/2 · 3/2.",
        "1/2 · 3/2 = 3/4."],
       r == F(3, 4))

r = F(125, 100)
T.task(1, "Zapište desetinné číslo 1,25 jako zlomek v základním tvaru a jako smíšené číslo.", "5/4 = 1 1/4",
       ["1,25 = 125/100.", "Zkrátíme 25: 125/100 = 5/4.", "5/4 = 4/4 + 1/4 = 1 1/4."],
       r == F(5, 4))

q = "√81 − 2³ + (−3)²"
r = ev(q)
T.task(1, f"Vypočtěte: {q}", fr(r),
       ["Odmocnina: √81 = 9, protože 9² = 81.",
        "Mocniny: 2³ = 2 · 2 · 2 = 8 a (−3)² = (−3) · (−3) = 9. Záporné číslo v závorce se umocňuje celé.",
        "9 − 8 + 9 = 10."],
       r == 10 and ev("√81") == 9 and ev("2³") == 8 and ev("(−3)²") == 9, space=2)

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

q = "2⁻³ + (1/2)⁻² − 5⁰"
r = ev(q)
T.task(2, f"Vypočtěte a výsledek zapište v základním tvaru: {q}", fr(r),
       ["Záporný exponent znamená převrácenou hodnotu: 2⁻³ = 1/2³ = 1/8.",
        "(1/2)⁻² je převrácený zlomek na druhou: 2² = 4.",
        "Nultá mocnina je 1: 5⁰ = 1.",
        "1/8 + 4 − 1 = 1/8 + 3 = 1/8 + 24/8 = 25/8."],
       r == F(25, 8) and ev("2⁻³") == F(1, 8) and ev("(1/2)⁻²") == 4 and ev("5⁰") == 1 and F(1, 8) + 3 == F(25, 8))

q = "(2,5 · 10²) · (4 · 10⁻³) + 0,3²"
r = ev(q)
T.task(2, f"Vypočtěte a výsledek zapište jako desetinné číslo: {q}", "1,09",
       ["10² = 100 a 10⁻³ = 1/1 000 = 0,001.",
        "2,5 · 10² = 250 a 4 · 10⁻³ = 0,004, tedy 250 · 0,004 = 1.",
        "0,3² = 0,3 · 0,3 = 0,09 (ne 0,9).",
        "1 + 0,09 = 1,09."],
       r == ev("1,09") and ev("10²") == 100 and ev("10⁻³") == F(1, 1000) and ev("250 · 0,004") == 1 and ev("0,3²") == F(9, 100))

stmts = [F(2, 5) + F(1, 5) == F(3, 10), F(3, 4) / F(3, 8) == 2, F(1, 3) * 6 == 2]
T.task(2, "Platí tato tvrzení?", "NE, ANO, ANO",
       ["2/5 + 1/5 = 3/5, ne 3/10. Sčítáme jen čitatele, jmenovatel zůstává. Tvrzení neplatí.",
        "3/4 : 3/8 = 3/4 · 8/3 = 24/12 = 2. Platí.", "1/3 · 6 = 6/3 = 2. Platí."],
       stmts == [False, True, True], kind="yesno",
       options=["2/5 + 1/5 = 3/10", "3/4 : 3/8 = 2", "Třetina z šesti je 2."], space=1)

x = (F(7, 12) - F(1, 4)) / F(2, 3)
T.task(2, "Řešte rovnici: 2/3 · x + 1/4 = 7/12", f"x = {fr(x)}",
       ["Odečteme 1/4: 2/3 · x = 7/12 − 3/12 = 4/12 = 1/3.", "Vydělíme 2/3: x = 1/3 · 3/2 = 1/2.",
        "Zkouška: 2/3 · 1/2 + 1/4 = 1/3 + 1/4 = 4/12 + 3/12 = 7/12. ✓"],
       x == F(1, 2) and F(2, 3) * x + F(1, 4) == F(7, 12))

# ---------------------------------------------------------------- Náročnější
celkem = 60 / (1 - F(2, 5) - F(1, 4))
T.task(3, "Ve třídě si 2/5 žáků vybralo výlet do hor, 1/4 žáků výlet k vodě a zbylých 21 žáků muzeum. "
          "Kolik žáků vybíralo?", "60 žáků",
       ["Hory a voda dohromady: 2/5 + 1/4 = 8/20 + 5/20 = 13/20 žáků.", "Na muzeum zbývá 1 − 13/20 = 7/20 žáků, to je 21 žáků.",
        "1/20 žáků … 21 : 7 = 3 žáci, celá třída 20 · 3 = 60 žáků.",
        "Zkouška: 2/5 ze 60 = 24, 1/4 ze 60 = 15, 24 + 15 + 21 = 60. ✓"],
       21 / (1 - F(2, 5) - F(1, 4)) == 60 and F(2, 5) * 60 + F(1, 4) * 60 + 21 == 60, space=4)

r = (F(1, 2) - F(1, 3)) / (F(1, 3) - F(1, 4)) - F(4, 5) * (1 + F(1, 4))
T.task(3, "Vypočtěte: (1/2 − 1/3) : (1/3 − 1/4) − 4/5 · (1 + 1/4)", fr(r),
       ["První závorka: 1/2 − 1/3 = 3/6 − 2/6 = 1/6.", "Druhá závorka: 1/3 − 1/4 = 4/12 − 3/12 = 1/12.",
        "Podíl: 1/6 : 1/12 = 1/6 · 12 = 2.", "Součin: 4/5 · 5/4 = 1.", "Rozdíl: 2 − 1 = 1."],
       r == 1, space=4)

q = "(√(25/16) − (2/3)⁻¹) : (−1/2)³"
r = ev(q)
T.task(3, f"Vypočtěte a výsledek zapište v základním tvaru: {q}", fr(r),
       ["Odmocnina ze zlomku: √(25/16) = 5/4, protože (5/4)² = 25/16.",
        "Záporný exponent: (2/3)⁻¹ = 3/2.",
        "První závorka: 5/4 − 3/2 = 5/4 − 6/4 = −1/4.",
        "Druhá závorka: (−1/2)³ = −1/8, lichá mocnina záporného čísla je záporná.",
        "(−1/4) : (−1/8) = (−1/4) · (−8) = 2."],
       r == 2 and ev("√(25/16)") == F(5, 4) and ev("(2/3)⁻¹") == F(3, 2) and ev("5/4 − 3/2") == F(-1, 4) and ev("(−1/2)³") == F(-1, 8),
       space=4)

# Čtverec o stejném obsahu jako obdélník 8 m × 18 m: obsah 144 m², strana √144 = 12 m
strana = ev("√(8 · 18)")
rozdil_obvodu = 2 * (8 + 18) - 4 * strana
T.task(3, "Obdélníková zahrada má rozměry 8 m a 18 m. Majitel ji chce upravit na čtvercovou zahradu o stejném obsahu "
          "a celou ji oplotit. Metr plotu stojí 450 Kč. Kolik korun ušetří oproti oplocení původní obdélníkové zahrady?",
       "1 800 Kč",
       ["Obsah obdélníkové zahrady: 8 · 18 = 144 m².",
        "Čtverec o obsahu 144 m² má stranu √144 = 12 m.",
        "Obvod obdélníku: 2 · (8 + 18) = 52 m. Obvod čtverce: 4 · 12 = 48 m.",
        "Plotu je o 52 − 48 = 4 m méně, tedy 4 · 450 = 1 800 Kč."],
       strana == 12 and 8 * 18 == 144 == strana ** 2 and 2 * (8 + 18) == 52 and rozdil_obvodu == 4 and rozdil_obvodu * 450 == 1800,
       space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
q = "√(13² − 5²)"
r = ev(q)
vals = [F(8), F(72), F(12), F(144), F(-12)]
T.diagnostic(f"Kolik je {q}?", "C",
             ["Nejdřív mocniny pod odmocninou: 13² = 169 a 5² = 25, rozdíl 169 − 25 = 144.",
              "√144 = 12, protože 12² = 144.",
              "Pozor: odmocnina se s mocninou nezruší po částech. 13 − 5 = 8 je chyba (A), 144 je zapomenutá odmocnina (D)."],
             r == 12 and [v == r for v in vals] == [False, False, True, False, False] and 13 ** 2 - 5 ** 2 == 144,
             kind="choice", options=["8", "72", "12", "144", "−12"])
r = (F(2, 3) - F(1, 4)) / (1 + F(1, 4))
T.diagnostic("Vypočtěte: (2/3 − 1/4) : (1 + 1/4)", fr(r),
             ["Čitatel: 2/3 − 1/4 = 8/12 − 3/12 = 5/12.", "Jmenovatel: 1 + 1/4 = 5/4.", "5/12 : 5/4 = 5/12 · 4/5 = 20/60 = 1/3."],
             r == F(1, 3))

T.save()
