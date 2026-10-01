#!/usr/bin/env python3
"""Téma 3: Lineární rovnice a soustavy (úloha 4 jednotné zkoušky). Formát v _lib.py, vzor 01_zlomky.py.

Rovnice v zadání i v postupech se ověřují přímo z textu (parser níže, Fraction): zápis v listu a výpočet se
nemohou rozejít. Mimo rozsah specifikace (kvadratické rovnice) zde nic není: násobení závorek je jen tam,
kde se členy s x² zruší a zbude lineární rovnice.
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402


# ---------------------------------------------------------------- ověřování rovnic zapsaných jako v textu
def _fn(s):
    """Výraz z textu (−, ·, a/b, desetinná čárka, „5 100“, 3x, x²) → funkce (x, y) → Fraction."""
    s = s.strip().replace("−", "-").replace("·", "*").replace("²", "**2")
    s = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", "", s)
    s = re.sub(r"(\d+),(\d+)", r"\1.\2", s)
    s = re.sub(r"\d+(?:\.\d+)?", lambda m: f"F('{m.group(0)}')", s)
    s = re.sub(r"(?<=[)xy])\s*(?=[(xy]|F\()", "*", s)
    return lambda x=0, y=0: eval(s, {"F": F, "__builtins__": {}}, {"x": F(x), "y": F(y)})


def _d(e):
    left, right = e.split("=")
    fl, fr_ = _fn(left), _fn(right)
    return lambda x=0, y=0: fl(x, y) - fr_(x, y)


def solve1(e):
    """Řešení lineární rovnice o jedné neznámé x: číslo, nebo „žádné“ / „všechna“."""
    d = _d(e)
    a = d(1) - d(0)
    assert d(2) - d(0) == 2 * a and d(-3) - d(0) == -3 * a, f"Rovnice není lineární: {e}"
    if a == 0:
        return "všechna" if d(0) == 0 else "žádné"
    return -d(0) / a


def solve2(e1, e2):
    """Jediné řešení soustavy dvou lineárních rovnic o x a y jako (x, y)."""
    rows = []
    for e in (e1, e2):
        d = _d(e)
        a, b, c = d(1, 0) - d(0, 0), d(0, 1) - d(0, 0), -d(0, 0)
        assert d(2, 3) - d(0, 0) == 2 * a + 3 * b and d(-1, 4) - d(0, 0) == -a + 4 * b, f"Rovnice není lineární: {e}"
        rows.append((a, b, c))
    (a1, b1, c1), (a2, b2, c2) = rows
    det = a1 * b2 - a2 * b1
    assert det != 0, "Soustava nemá jediné řešení"
    return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det


def holds(e, x=0, y=0):
    return _d(e)(x, y) == 0


def val(side, x=0, y=0):
    return _fn(side)(x, y)


def same(a, b):
    """Dva výrazy (stupeň nejvýše 2) se rovnají pro každé x: ověřeno na sedmi hodnotách."""
    fa, fb = _fn(a), _fn(b)
    return all(fa(t) == fb(t) for t in range(-3, 4))


def ok1(x0, q, *steps):
    """Řešení q je právě x0 a každá rovnice v postupu platí pro x0."""
    return solve1(q) == x0 and all(holds(s, x0) for s in steps)


def ok2(sol, e1, e2, *steps):
    return solve2(e1, e2) == sol and all(holds(s, *sol) for s in steps)


# ---------------------------------------------------------------- téma
T = Topic(3, "rovnice", "Lineární rovnice a soustavy",
          "Lineární rovnice a soustava dvou rovnic jsou úlohou 4 jednotné zkoušky a hodnotí se podle zapsaného postupu, bez postupu nejsou body. "
          "Pište každý krok na samostatný řádek a výsledek vždy dopočítejte do konce.",
          ["Rovnici se zlomky vynásobte společným jmenovatelem všech členů, i těch bez zlomku. Při násobení šesti se číslo 3 změní na 18, nezůstane 3.",
           "Minus před závorkou změní znaménko u každého členu v ní: 7 − 2 · (x − 1) = 7 − 2x + 2. Nejčastější chyba je nevynásobit druhý člen závorky.",
           "Dvě závorky násobte „každý člen s každým“: (x + 3) · (x − 2) = x² − 2x + 3x − 6 = x² + x − 6. Když se členy s x² na obou stranách zruší, zbude lineární rovnice.",
           "Členy převádějte na druhou stranu se změněným znaménkem a poslední krok vždy dopište (z 3x = 15 až x = 5). Nedokončený poslední krok stojí bod. Správnost ověřte dosazením do původní rovnice.",
           "Vyjde-li nepravdivá rovnost (např. 6 = 5), rovnice nemá řešení. Vyjde-li vždy pravdivá rovnost (např. 0 = 0), vyhovuje každé číslo a řešení je nekonečně mnoho.",
           "U soustavy najděte obě neznámé a zapište je jako x = …, y = …, chybějící druhá neznámá stojí body. Sčítací metoda: rovnice vynásobte tak, aby se u jedné neznámé objevila opačná čísla (např. 2y a −2y), a sečtěte je. "
           "Dosazovací metoda: z jedné rovnice vyjádřete neznámou a dosaďte ji do druhé."])

# ---------------------------------------------------------------- řešený příklad
q = "3 · (x − 2) − x/2 = 1/4 · (3x + 18)"
s1 = "3x − 6 − 1/2 · x = 3/4 · x + 9/2"
s2 = "12x − 24 − 2x = 3x + 18"
s3 = "10x − 24 = 3x + 18"
s4 = "10x − 3x = 18 + 24"
s5 = "7x = 42"
T.example(f"Řešte rovnici a zapište celý postup: {q}",
          [f"Roznásobíme závorky: {s1}.",
           f"Vynásobíme všechny členy čtyřmi, aby zmizely zlomky: {s2}.",
           f"Sloučíme členy s x na levé straně: {s3}.",
           f"Členy s x převedeme doleva, čísla doprava a změníme jim znaménka: {s4}, tedy {s5}.",
           "Vydělíme sedmi: x = 6.",
           "Zkouška: L = 3 · 4 − 3 = 9, P = 1/4 · 36 = 9. ✓"],
          "x = 6",
          ok1(6, q, s1, s2, s3, s4, s5) and (val("3 · (x − 2) − x/2", 6), val("1/4 · (3x + 18)", 6)) == (9, 9))

# ---------------------------------------------------------------- Základ
q = "5x − 7 = 2x + 8"; s1 = "5x − 2x = 8 + 7"; s2 = "3x = 15"
T.task(1, f"Řešte rovnici: {q}", "x = 5",
       [f"Členy s x převedeme doleva, čísla doprava a změníme jim znaménka: {s1}.", f"Sloučíme: {s2}.", "Vydělíme třemi: x = 5.",
        "Zkouška: L = 5 · 5 − 7 = 18, P = 2 · 5 + 8 = 18. ✓"],
       ok1(5, q, s1, s2) and (val("5x − 7", 5), val("2x + 8", 5)) == (18, 18), space=2)

q = "4 · (x − 3) = 2x + 6"; s1 = "4x − 12 = 2x + 6"; s2 = "4x − 2x = 6 + 12"; s3 = "2x = 18"
T.task(1, f"Řešte rovnici: {q}", "x = 9",
       [f"Roznásobíme závorku: {s1}.", f"Členy s x doleva, čísla doprava: {s2}, tedy {s3}.", "Vydělíme dvěma: x = 9.",
        "Zkouška: L = 4 · (9 − 3) = 24, P = 2 · 9 + 6 = 24. ✓"],
       ok1(9, q, s1, s2, s3) and (val("4 · (x − 3)", 9), val("2x + 6", 9)) == (24, 24), space=2)

q = "2/5 · x − 3 = 1"; s1 = "2x − 15 = 5"; s2 = "2x = 20"
T.task(1, f"Řešte rovnici: {q}", "x = 10",
       [f"Vynásobíme všechny členy pěti (i číslo −3 a číslo 1): {s1}.", f"Přičteme 15: {s2}.", "Vydělíme dvěma: x = 10.",
        "Zkouška: L = 2/5 · 10 − 3 = 4 − 3 = 1 = P. ✓"],
       ok1(10, q, s1, s2) and (val("2/5 · x − 3", 10), val("1", 10)) == (1, 1), space=2)

opts = ["x = 1", "x = 3", "x = 5", "x = 10", "x = −1"]
q = "3 · (x + 2) = 5x − 4"
good = [o for o in opts if holds(q, F(o.split("= ")[1].replace("−", "-")))]
T.task(1, f"Které číslo je řešením rovnice {q}?", "C",
       ["Roznásobíme závorku: 3x + 6 = 5x − 4.", "Členy převedeme: 6 + 4 = 5x − 3x, tedy 10 = 2x.", "x = 5, správná je možnost C.",
        "Ostatní možnosti jsou typické chyby: 3 (zapomenuté vynásobení čísla 2 trojkou), 1 (špatné znaménko u čísla 4), "
        "−1 (špatné znaménko u čísla 6), 10 (nedokončený poslední krok, chybí dělení dvěma)."],
       good == ["x = 5"] and solve1(q) == 5 and solve1("3x + 2 = 5x − 4") == 3 and solve1("3x + 6 = 5x + 4") == 1
       and solve1("3x − 6 = 5x − 4") == -1 and 6 + 4 == 10,
       kind="choice", options=opts, space=2)

q = "7 − 2 · (x − 1) = 3"; s1 = "7 − 2x + 2 = 3"; s2 = "9 − 2x = 3"; s3 = "−2x = −6"
T.task(1, f"Řešte rovnici: {q}", "x = 3",
       [f"Roznásobíme závorku, minus před ní změní obě znaménka: {s1}.", f"Sloučíme čísla: {s2}.", f"Odečteme 9: {s3}.", "Vydělíme číslem −2: x = 3.",
        "Zkouška: L = 7 − 2 · (3 − 1) = 7 − 4 = 3 = P. ✓"],
       ok1(3, q, s1, s2, s3) and val("7 − 2 · (x − 1)", 3) == 3, space=3)

# ---------------------------------------------------------------- Jako u zkoušky
q = "x/4 − 2 = x/6 + 1/3"; s1 = "3x − 24 = 2x + 4"; s2 = "3x − 2x = 4 + 24"
T.task(2, f"Řešte rovnici a uveďte celý postup: {q}", "x = 28",
       [f"Nejmenší společný násobek jmenovatelů 4, 6 a 3 je 12. Vynásobíme dvanácti všechny členy: {s1}.",
        f"Členy s x doleva, čísla doprava: {s2}.", "Sloučíme: x = 28.",
        "Zkouška: L = 28/4 − 2 = 7 − 2 = 5, P = 28/6 + 1/3 = 14/3 + 1/3 = 5. ✓"],
       ok1(28, q, s1, s2) and (val("x/4 − 2", 28), val("x/6 + 1/3", 28)) == (5, 5) and F(28, 6) + F(1, 3) == 5, space=4)

q = "3/4 · (x − 2) = 1/2 · (x + 1) + 1"; s1 = "3 · (x − 2) = 2 · (x + 1) + 4"; s2 = "3x − 6 = 2x + 2 + 4"; s3 = "3x − 6 = 2x + 6"; s4 = "3x − 2x = 6 + 6"
T.task(2, f"Řešte rovnici a uveďte celý postup: {q}", "x = 12",
       [f"Vynásobíme všechny členy čtyřmi (i číslo 1): {s1}.", f"Roznásobíme závorky: {s2}.", f"Sloučíme: {s3}.", f"Členy s x doleva, čísla doprava: {s4}, tedy x = 12.",
        "Zkouška: L = 3/4 · 10 = 15/2, P = 1/2 · 13 + 1 = 15/2. ✓"],
       ok1(12, q, s1, s2, s3, s4) and (val("3/4 · (x − 2)", 12), val("1/2 · (x + 1) + 1", 12)) == (F(15, 2), F(15, 2)), space=4)

e1, e2 = "x = 3y − 4", "2x − y = 7"
s1 = "2 · (3y − 4) − y = 7"; s2 = "6y − 8 − y = 7"; s3 = "5y = 15"
T.task(2, f"Řešte soustavu rovnic dosazovací metodou a uveďte celý postup: (I) {e1}, (II) {e2}", "x = 5, y = 3",
       [f"Z rovnice (I) dosadíme za x do rovnice (II): {s1}.", f"Roznásobíme a sloučíme: {s2}, tedy {s3}.", "Vydělíme pěti: y = 3.",
        "Dopočítáme x z rovnice (I): x = 3 · 3 − 4 = 5.", "Zkouška: (I) 3 · 3 − 4 = 5 ✓, (II) 2 · 5 − 3 = 7 ✓."],
       ok2((5, 3), e1, e2, s1, s2, s3) and 3 * 3 - 4 == 5 and 2 * 5 - 3 == 7, space=5)

e1, e2 = "2x + y = 11", "3x − 2y = 6"
s1 = "4x + 2y = 22"; s2 = "7x = 28"; s3 = "2 · 4 + y = 11"
T.task(2, f"Řešte soustavu rovnic sčítací metodou a uveďte celý postup: (I) {e1}, (II) {e2}", "x = 4, y = 3",
       [f"Rovnici (I) vynásobíme dvěma, aby u y byla čísla 2y a −2y: {s1}.", f"Sečteme s rovnicí (II), neznámá y se zruší: {s2}.", "Vydělíme sedmi: x = 4.",
        f"Dosadíme do rovnice (I): {s3}, tedy y = 3.", "Zkouška: (II) 3 · 4 − 2 · 3 = 12 − 6 = 6 ✓."],
       ok2((4, 3), e1, e2, s1, s2, s3) and 3 * 4 - 2 * 3 == 6 and (4 * 2, 2 * 11) == (8, 22), space=5)

e1, e2 = "x + y = 8", "3x − y = 4"
opts = ["x = 5, y = 3", "x = 2, y = 2", "x = 4, y = 4", "x = 3, y = 5", "x = 4, y = 8"]
pairs = [(5, 3), (2, 2), (4, 4), (3, 5), (4, 8)]
good = [i for i, (a, b) in enumerate(pairs) if holds(e1, a, b) and holds(e2, a, b)]
T.task(2, f"Která dvojice čísel je řešením soustavy rovnic (I) {e1}, (II) {e2}?", "D",
       ["Rovnice sečteme: 4x = 12, tedy x = 3.", "Z rovnice (I): y = 8 − 3 = 5. Řešení je x = 3, y = 5, možnost D.",
        "Zkouška: (I) 3 + 5 = 8 ✓, (II) 3 · 3 − 5 = 4 ✓.",
        "Ostatní možnosti splňují vždy jen jednu rovnici: A a C jen rovnici (I), B a E jen rovnici (II). Proto je nutné dosadit do obou rovnic."],
       good == [3] and solve2(e1, e2) == (3, 5) and [holds(e1, a, b) for a, b in pairs] == [True, False, True, True, False]
       and [holds(e2, a, b) for a, b in pairs] == [False, True, False, True, True],
       kind="choice", options=opts, space=3)

a1_, a2_, a3_ = "3 · (x + 2) = 3x + 5", "2 · (x − 4) = 2x − 8", "2x + 3 = x + 5"
T.task(2, "Rozhodněte, zda tvrzení platí.", "ANO, NE, ANO",
       [f"Rovnice {a1_} vede na 3x + 6 = 3x + 5, tedy 6 = 5. To neplatí pro žádné x, rovnice nemá řešení. Tvrzení platí.",
        f"Rovnice {a2_} vede na 2x − 8 = 2x − 8, což platí pro každé x. Rovnice má nekonečně mnoho řešení, ne jedno. Tvrzení neplatí.",
        f"Dosadíme x = 2 do rovnice {a3_}: L = 2 · 2 + 3 = 7, P = 2 + 5 = 7. Tvrzení platí."],
       solve1(a1_) == "žádné" and solve1(a2_) == "všechna" and holds(a3_, 2) and solve1(a3_) == 2
       and solve1("3x + 6 = 3x + 5") == "žádné" and 2 * 2 + 3 == 7 == 2 + 5,
       kind="yesno", options=[f"Rovnice {a1_} nemá žádné řešení.", f"Rovnice {a2_} má právě jedno řešení.", f"Číslo 2 je řešením rovnice {a3_}."], space=1)

q = "0,2x + 1,5 = 0,5x − 0,3"; s1 = "2x + 15 = 5x − 3"; s2 = "15 + 3 = 5x − 2x"; s3 = "18 = 3x"
T.task(2, f"Řešte rovnici s desetinnými čísly a uveďte celý postup: {q}", "x = 6",
       [f"Vynásobíme všechny členy deseti, aby zmizely desetinné čárky: {s1}.", f"Členy s x doprava, čísla doleva: {s2}.", f"Sloučíme: {s3}.", "Vydělíme třemi: x = 6.",
        "Zkouška: L = 0,2 · 6 + 1,5 = 1,2 + 1,5 = 2,7, P = 0,5 · 6 − 0,3 = 3 − 0,3 = 2,7. ✓"],
       ok1(6, q, s1, s2, s3) and (val("0,2x + 1,5", 6), val("0,5x − 0,3", 6)) == (F(27, 10), F(27, 10)), space=4)

# ---------------------------------------------------------------- Náročnější
q = "(x + 3) · (x − 2) − x · (x + 4) = 6"
p1 = "(x + 3) · (x − 2)"; p1v = "x² − 2x + 3x − 6"; p1w = "x² + x − 6"; p2 = "x · (x + 4)"; p2v = "x² + 4x"
s1 = "x² + x − 6 − x² − 4x = 6"; s2 = "−3x − 6 = 6"; s3 = "−3x = 12"
T.task(3, f"Řešte rovnici a uveďte celý postup: {q}", "x = −4",
       [f"Každý člen první závorky vynásobíme každým členem druhé: {p1} = {p1v} = {p1w}. Také {p2} = {p2v}.",
        f"Dosadíme a minus před závorkou změní znaménka: {p1w} − ({p2v}) = 6, tedy {s1}.", f"Členy s x² se zruší: {s2}.", f"Přičteme 6: {s3}, tedy x = −4.",
        "Zkouška: L = (−4 + 3) · (−4 − 2) − (−4) · (−4 + 4) = (−1) · (−6) − 0 = 6 = P. ✓"],
       ok1(-4, q, s1, s2, s3) and same(p1, p1v) and same(p1v, p1w) and same(p2, p2v) and holds(f"{p1w} − ({p2v}) = 6", -4)
       and val("(x + 3) · (x − 2) − x · (x + 4)", -4) == 6, space=5)

e1, e2 = "x/2 + y/3 = 6", "y = 2x − 3"
s1 = "3x + 2y = 36"; s2 = "3x + 2 · (2x − 3) = 36"; s3 = "7x − 6 = 36"; s4 = "7x = 42"
T.task(3, f"Řešte soustavu rovnic a uveďte celý postup: (I) {e1}, (II) {e2}", "x = 6, y = 9",
       [f"Rovnici (I) vynásobíme šesti: {s1}.", f"Za y dosadíme z rovnice (II): {s2}.", f"Roznásobíme a sloučíme: 3x + 4x − 6 = 36, tedy {s3}.", f"Přičteme 6: {s4}, x = 6.",
        "Dopočítáme y z rovnice (II): y = 2 · 6 − 3 = 9.", "Zkouška: (I) 6/2 + 9/3 = 3 + 3 = 6 ✓, (II) 2 · 6 − 3 = 9 ✓."],
       ok2((6, 9), e1, e2, s1, s2, s3, s4, "3x + 4x − 6 = 36") and F(6, 2) + F(9, 3) == 6 and 2 * 6 - 3 == 9, space=6)

q = "2/3 · (x − 4) − 1/2 · (x − 6) = 1/4 · x + 1"
s1 = "2/3 · x − 8/3 − 1/2 · x + 3 = 1/4 · x + 1"; s2 = "8x − 32 − 6x + 36 = 3x + 12"; s3 = "2x + 4 = 3x + 12"; s4 = "2x − 3x = 12 − 4"; s5 = "−x = 8"
T.task(3, f"Řešte rovnici a uveďte celý postup: {q}", "x = −8",
       [f"Roznásobíme závorky, minus před druhou změní znaménka obou členů: {s1}.", f"Vynásobíme všechny členy dvanácti: {s2}.", f"Sloučíme: {s3}.",
        f"Členy s x doleva, čísla doprava: {s4}, tedy {s5}.", "Vynásobíme číslem −1: x = −8.",
        "Zkouška: L = 2/3 · (−12) − 1/2 · (−14) = −8 + 7 = −1, P = 1/4 · (−8) + 1 = −2 + 1 = −1. ✓"],
       ok1(-8, q, s1, s2, s3, s4, s5) and (val("2/3 · (x − 4) − 1/2 · (x − 6)", -8), val("1/4 · x + 1", -8)) == (-1, -1), space=6)

e1, e2 = "3 · (x − 1) − 2y = 4", "2x + 3 · (y + 1) = 25"
s1 = "3x − 2y = 7"; s2 = "2x + 3y = 22"; s3 = "9x − 6y = 21"; s4 = "4x + 6y = 44"; s5 = "13x = 65"; s6 = "10 + 3y = 22"
T.task(3, f"Řešte soustavu rovnic a uveďte celý postup: (I) {e1}, (II) {e2}", "x = 5, y = 4",
       [f"Roznásobíme závorky a upravíme: (I) {s1}, (II) {s2}.", f"Sčítací metoda: (I) vynásobíme třemi a (II) dvěma, aby u y byla čísla −6y a 6y: {s3} a {s4}.",
        f"Rovnice sečteme: {s5}, tedy x = 5.", f"Dosadíme do rovnice {s2}: {s6}, tedy 3y = 12 a y = 4.",
        "Zkouška v původních rovnicích: (I) 3 · (5 − 1) − 2 · 4 = 12 − 8 = 4 ✓, (II) 2 · 5 + 3 · (4 + 1) = 10 + 15 = 25 ✓."],
       ok2((5, 4), e1, e2, s1, s2, s3, s4, s5, s6) and 3 * (5 - 1) - 2 * 4 == 4 and 2 * 5 + 3 * (4 + 1) == 25, space=7)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
q = "x/3 + 1/2 = 5/6 · x − 1"; s1 = "2x + 3 = 5x − 6"; s2 = "3 + 6 = 5x − 2x"; s3 = "9 = 3x"
T.diagnostic(f"Řešte rovnici a uveďte celý postup: {q}", "x = 3",
             [f"Vynásobíme všechny členy šesti: {s1}.", f"Členy s x doprava, čísla doleva: {s2}, tedy {s3}.", "Vydělíme třemi: x = 3.",
              "Zkouška: L = 3/3 + 1/2 = 3/2, P = 5/6 · 3 − 1 = 5/2 − 1 = 3/2. ✓"],
             ok1(3, q, s1, s2, s3) and (val("x/3 + 1/2", 3), val("5/6 · x − 1", 3)) == (F(3, 2), F(3, 2)))

e1, e2 = "x + y = 9", "3x − 2y = 2"
s1 = "y = 9 − x"; s2 = "3x − 2 · (9 − x) = 2"; s3 = "5x − 18 = 2"; s4 = "5x = 20"
T.diagnostic(f"Řešte soustavu rovnic a uveďte celý postup: (I) {e1}, (II) {e2}", "x = 4, y = 5",
             [f"Z rovnice (I) vyjádříme y: {s1}.", f"Dosadíme do rovnice (II): {s2}.", f"Roznásobíme a sloučíme: 3x − 18 + 2x = 2, tedy {s3}, {s4}.", "Vydělíme pěti: x = 4. Pak y = 9 − 4 = 5.",
              "Zkouška: (I) 4 + 5 = 9 ✓, (II) 3 · 4 − 2 · 5 = 12 − 10 = 2 ✓."],
             ok2((4, 5), e1, e2, s1, s2, s3, s4, "3x − 18 + 2x = 2") and 4 + 5 == 9 and 3 * 4 - 2 * 5 == 2)

T.save()
