#!/usr/bin/env python3
"""Téma 2: Výrazy a mnohočleny (úloha 3 jednotné přijímací zkoušky: výrazy s postupem).

Ověření: zadání i výsledek se berou přímo z textu a počítají se jako mnohočleny s přesnými (zlomkovými) koeficienty
(třída Poly). Úprava je správná, jen když se mnohočlen zadání rovná mnohočlenu výsledku, a základní tvar výsledku se
porovná s vysázeným řetězcem (funkce show). Dosazení se ověřuje přes ev. Úlohy jsou vlastní, ne převzaté z testů CERMAT.
"""
import re
import string
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402


# ------------------------------------------------------------------ mnohočleny pro ověření
class Poly:
    """Mnohočlen s racionálními koeficienty. Klíč členu = seřazená dvojice (proměnná, exponent)."""

    def __init__(self, t=None):
        self.t = {k: F(c) for k, c in (t or {}).items() if c != 0}

    @staticmethod
    def of(x):
        return x if isinstance(x, Poly) else Poly({(): F(x)})

    def __add__(self, o):
        t = dict(self.t)
        for k, c in Poly.of(o).t.items():
            t[k] = t.get(k, 0) + c
        return Poly(t)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -c for k, c in self.t.items()})

    def __sub__(self, o):
        return self + (-Poly.of(o))

    def __rsub__(self, o):
        return Poly.of(o) + (-self)

    def __mul__(self, o):
        t = {}
        for k1, c1 in self.t.items():
            for k2, c2 in Poly.of(o).t.items():
                e = dict(k1)
                for v, n in k2:
                    e[v] = e.get(v, 0) + n
                k = tuple(sorted(e.items()))
                t[k] = t.get(k, 0) + c1 * c2
        return Poly(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0, "mocnina mnohočlenu jen s exponentem 0, 1, 2, …"
        r = Poly.of(1)
        for _ in range(n):
            r = r * self
        return r

    def __truediv__(self, o):
        o = Poly.of(o)
        assert list(o.t) == [()], "mnohočlenem se nedělí, jen číslem"
        return self * (1 / o.t[()])

    def __eq__(self, o):
        return self.t == Poly.of(o).t

    __hash__ = None


_SUPD = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_TOK = re.compile(r"[0-9]+(?:,[0-9]+)?|[a-z]|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|[-+*/()]")
_TR = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def ev(s: str, /, **v):
    """Vyhodnotí výraz zapsaný tak, jak se sází (·, :, −, 3a², 2(x − 1), (a + b)², 1,5), pro dané hodnoty proměnných
    (čísla → číslo, Poly → mnohočlen). Stejný řetězec jde do zadání i do ověření."""
    s = s.replace("−", "-").replace("·", "*").replace(":", "/").replace(" ", "")
    toks = _TOK.findall(s)
    assert "".join(toks) == s, f"nerozpoznané znaky ve výrazu: {s}"
    out, prev = [], None
    for t in toks:
        k = "n" if t[0].isascii() and t[0].isdigit() else "v" if t.isascii() and t.isalpha() else "s" if t[0] in "⁰¹²³⁴⁵⁶⁷⁸⁹⁻" else t
        assert not (k == "n" and prev in ("n", "v", "s", ")")), f"chybí operátor před číslem: {s}"
        if prev in ("n", "v", "s", ")") and k in ("v", "("):
            out.append("*")
        out.append(f"F('{t.replace(',', '.')}')" if k == "n" else f"v['{t}']" if k == "v" else f"**({t.translate(_TR)})" if k == "s" else t)
        prev = k
    return eval("".join(out), {"__builtins__": {}, "F": F}, {"v": v})


_VARS = {c: Poly({((c, 1),): 1}) for c in string.ascii_lowercase}


def P(s: str) -> Poly:
    """Výraz jako mnohočlen (symbolicky, všechny proměnné a–z)."""
    return Poly.of(ev(s, **_VARS))


def show(p) -> str:
    """Základní tvar mnohočlenu tak, jak se sází: od nejvyššího stupně, minus U+2212, bez zbytečných jedniček."""
    p = Poly.of(p)
    if not p.t:
        return "0"
    key = lambda k: (-sum(n for _, n in k), tuple(-dict(k).get(c, 0) for c in string.ascii_lowercase))  # noqa: E731
    out = ""
    for i, k in enumerate(sorted(p.t, key=key)):
        c = p.t[k]
        assert c.denominator == 1, "zlomkové koeficienty se tu nesází"
        mono = "".join(v + ("" if n == 1 else "".join(_SUPD[int(d)] for d in str(n))) for v, n in k)
        body = ("" if abs(c) == 1 and mono else str(abs(c.numerator))) + mono
        out += (("−" if c < 0 else "") + body) if i == 0 else ((" − " if c < 0 else " + ") + body)
    return out


def same(*exprs) -> bool:
    """Všechny výrazy jsou stejný mnohočlen (tedy rovnají se pro každé dosazení)."""
    return all(P(e) == P(exprs[0]) for e in exprs[1:])


# Tvrzení z tipů (aby v nich nebyla chyba)
assert show(P("(a + b)²")) == "a² + 2ab + b²" and show(P("(a − b)²")) == "a² − 2ab + b²" and same("a² − b²", "(a − b)(a + b)")
assert show(P("5 − (x − 2)")) == "−x + 7" and show(P("3a · 2a")) == "6a²" and show(P("3a² + 2a²")) == "5a²"
assert show(P("4x + 4")) == "4x + 4" and same("4x + 4", "4(x + 1)") and ev("(−2)²") == 4 and ev("−2²") == -4

T = Topic(2, "vyrazy", "Výrazy a mnohočleny",
          "Úprava výrazů je u zkoušky každý rok v úloze 3 (4 body) a jedna její část se píše s postupem. "
          "Postup musí být úplný: výsledek bez postupu se u takové úlohy nehodnotí.",
          ["Mínus před závorkou změní znaménka všech členů v závorce: 5 − (x − 2) = 5 − x + 2.",
           "(a + b)² není a² + b², chybí prostřední člen. Správně: (a + b)² = a² + 2ab + b²; (a − b)² = a² − 2ab + b².",
           "Rozdíl druhých mocnin se rozkládá: a² − b² = (a − b)(a + b). Součet a² + b² se takto rozložit nedá. "
           "Vzorce máte u zkoušky na poslední straně sešitu, rozhoduje ale to, jestli je ve výrazu poznáte.",
           "Sčítat a odčítat jde jen podobné členy (stejná proměnná ve stejné mocnině): 3a² + 2a² = 5a², ale 3a² + 2a se nespojí. "
           "Při násobení jednočlenů násobte zvlášť čísla a zvlášť proměnné: 3a · 2a = 6a².",
           "Při vytýkání zkontrolujte výsledek roznásobením. Když vytknete celý člen, zůstane v závorce jednička: 4x + 4 = 4(x + 1).",
           "Zkouška dosazením: dosaďte do zadání i do výsledku stejné jednoduché číslo (třeba x = 1). Musí vyjít totéž. "
           "Záporné číslo dosazujte do závorky: (−2)² = 4, ale −2² = −4."])

# ---------------------------------------------------------------- Řešený příklad
q = "(x + 4)² − (x − 1)(x + 3)"
T.example(f"Upravte výraz a zapište ho v základním tvaru: {q}",
          ["První závorku umocníme podle vzorce (a + b)²: (x + 4)² = x² + 8x + 16.",
           "Druhý součin roznásobíme každý člen s každým: (x − 1)(x + 3) = x² + 3x − x − 3 = x² + 2x − 3.",
           "Před druhým součinem je minus, proto změníme znaménka všech členů: x² + 8x + 16 − x² − 2x + 3.",
           "Sečteme podobné členy: x² − x² = 0, 8x − 2x = 6x, 16 + 3 = 19."],
          "6x + 19",
          show(P(q)) == "6x + 19" and show(P("(x + 4)²")) == "x² + 8x + 16" and show(P("(x − 1)(x + 3)")) == "x² + 2x − 3"
          and same(q, "x² + 8x + 16 − x² − 2x + 3") and ev(q, x=1) == ev("6x + 19", x=1) == 25)

# ---------------------------------------------------------------- Základ
q, a = "(5x² − 3x + 1) − (2x² − x − 4)", "3x² − 2x + 5"
T.task(1, f"Upravte a zapište v základním tvaru: {q}", a,
       ["Mínus před druhou závorkou změní znaménka všech jejích členů: 5x² − 3x + 1 − 2x² + x + 4.",
        "Sečteme podobné členy: x²: 5 − 2 = 3, x: −3 + 1 = −2, čísla: 1 + 4 = 5.",
        f"Výsledek: {a}."],
       show(P(q)) == a and same(q, "5x² − 3x + 1 − 2x² + x + 4"), space=2)

q, a = "2a · 3a − 5a · a + a", "a² + a"
T.task(1, f"Upravte a zapište v základním tvaru: {q}", a,
       ["Vynásobíme jednočleny: 2a · 3a = 6a² a 5a · a = 5a².",
        "6a² − 5a² + a = a² + a. Člen a se s a² nespojí, protože nemá stejnou mocninu."],
       show(P(q)) == a and show(P("2a · 3a")) == "6a²" and show(P("5a · a")) == "5a²", space=2)

q, a = "3(2x − 1) − 2(x − 4)", "4x + 5"
T.task(1, f"Roznásobte závorky a výraz zjednodušte: {q}", a,
       ["Roznásobíme: 3(2x − 1) = 6x − 3 a −2(x − 4) = −2x + 8 (minus krát minus je plus).",
        "6x − 3 − 2x + 8 = 4x + 5."],
       show(P(q)) == a and same(q, "6x − 3 − 2x + 8") and show(P("3(2x − 1)")) == "6x − 3" and show(P("−2(x − 4)")) == "−2x + 8",
       space=2)

q = "3a² − ab + 2b"
r = ev(q, a=-2, b=3)
T.task(1, f"Vypočtěte hodnotu výrazu {q} pro a = −2, b = 3.", "24",
       ["Dosadíme a záporné číslo dáme do závorky: 3 · (−2)² − (−2) · 3 + 2 · 3.",
        "(−2)² = 4 a −(−2) · 3 = +6: 3 · 4 + 6 + 6.",
        "12 + 6 + 6 = 24."],
       r == 24 and 3 * (-2) ** 2 - (-2) * 3 + 2 * 3 == 24 == 12 + 6 + 6, space=2)

q = "(a + 3)²"
opts = ["a² + 9", "a² + 3a + 9", "a² + 6a + 9", "a² − 6a + 9", "a² + 6a"]
T.task(1, f"Který z výrazů je roven {q}?", "C",
       ["Použijeme vzorec (a + b)² = a² + 2ab + b² pro b = 3.",
        "(a + 3)² = a² + 2 · a · 3 + 3² = a² + 6a + 9, tedy C.",
        "A zapomíná prostřední člen, B má místo 6a jen 3a, D má špatné znaménko prostředního členu, E chybí 9."],
       [P(o) == P(q) for o in opts] == [False, False, True, False, False],
       kind="choice", options=opts, space=1)

# ---------------------------------------------------------------- Jako u zkoušky
q, a = "(2a − 3b)²", "4a² − 12ab + 9b²"
T.task(2, f"Umocněte a zapište v základním tvaru: {q}", a,
       ["Druhá mocnina rozdílu je druhá mocnina prvního členu, minus dvojnásobek součinu obou členů, plus druhá mocnina druhého členu. První člen je 2a, druhý je 3b.",
        "(2a)² = 4a², 2 · 2a · 3b = 12ab, (3b)² = 9b².",
        f"(2a − 3b)² = {a}."],
       show(P(q)) == a and show(P("(2a)²")) == "4a²" and show(P("2 · 2a · 3b")) == "12ab" and show(P("(3b)²")) == "9b²", space=2)

q, a = "(3x + 5)(3x − 5) − (x − 2)²", "8x² + 4x − 29"
T.task(2, f"Upravte a zapište v základním tvaru: {q}", a,
       ["První součin je rozdíl čtverců: (3x + 5)(3x − 5) = (3x)² − 5² = 9x² − 25.",
        "Druhý výraz podle vzorce: (x − 2)² = x² − 4x + 4.",
        "Odčítáme celou závorku, proto změníme znaménka: 9x² − 25 − x² + 4x − 4.",
        f"Sečteme podobné členy: {a}."],
       show(P(q)) == a and show(P("(3x + 5)(3x − 5)")) == "9x² − 25" and show(P("(x − 2)²")) == "x² − 4x + 4"
       and same(q, "9x² − 25 − x² + 4x − 4"), space=4)

q, a = "6x² − 15x", "3x(2x − 5)"
T.task(2, f"Vytkněte před závorku největší možný společný činitel: {q}", a,
       ["Největší společný dělitel čísel 6 a 15 je 3. Proměnná x je v obou členech (x² a x), vytkneme jedno x. Společný činitel je 3x.",
        "6x² = 3x · 2x a 15x = 3x · 5.",
        "6x² − 15x = 3x(2x − 5).",
        "Zkouška roznásobením: 3x · 2x − 3x · 5 = 6x² − 15x. ✓"],
       same(q, a) and gcd(6, 15) == 3 and gcd(2, 5) == 1 and same("3x · 2x", "6x²") and same("3x · 5", "15x"), space=2)

stm = [("(x + 3)² = x² + 9", False), ("x² − 16 = (x − 4)(x + 4)", True), ("4x − 2(x − 3) = 2x + 6", True)]
T.task(2, "Platí rovnost pro všechna čísla x?", "NE, ANO, ANO",
       ["(x + 3)² = x² + 6x + 9, chybí prostřední člen 6x. Tvrzení neplatí (pro x = 1 vyjde vlevo 16, vpravo 10).",
        "Rozdíl čtverců: (x − 4)(x + 4) = x² − 16. Platí.",
        "4x − 2(x − 3) = 4x − 2x + 6 = 2x + 6. Platí."],
       all(same(*s.split(" = ")) == ok for s, ok in stm) and ev("(x + 3)²", x=1) == 16 and ev("x² + 9", x=1) == 10,
       kind="yesno", options=[s for s, _ in stm], space=1)

q, a = "(x + 2)(x − 2) − x(x − 1)", "x − 4"
T.task(2, f"Upravte výraz {q} a pak vypočtěte jeho hodnotu pro x = 5.", f"{a}, hodnota 1",
       ["(x + 2)(x − 2) = x² − 4 (rozdíl čtverců) a x(x − 1) = x² − x.",
        "x² − 4 − (x² − x) = x² − 4 − x² + x = x − 4.",
        "Dosadíme x = 5: 5 − 4 = 1.",
        "Zkouška v původním výrazu: 7 · 3 − 5 · 4 = 21 − 20 = 1. ✓"],
       show(P(q)) == a and ev(q, x=5) == ev(a, x=5) == 1 and 7 * 3 - 5 * 4 == 1, space=3)

q, a = "(2x − 1)² − 4x(x − 2)", "4x + 1"
T.task(2, f"Upravte výraz a uveďte celý postup: {q}", a,
       ["(2x − 1)² = 4x² − 4x + 1 (prostřední člen je 2 · 2x · 1 = 4x).",
        "4x(x − 2) = 4x² − 8x.",
        "Odečteme celou závorku: 4x² − 4x + 1 − 4x² + 8x.",
        f"Sečteme podobné členy: {a}."],
       show(P(q)) == a and show(P("(2x − 1)²")) == "4x² − 4x + 1" and show(P("4x(x − 2)")) == "4x² − 8x"
       and same(q, "4x² − 4x + 1 − 4x² + 8x"), space=5)

q, a = "9a² − 16b²", "(3a − 4b)(3a + 4b)"
T.task(2, f"Rozložte na součin pomocí vzorce: {q}", a,
       ["Obě části jsou druhé mocniny: 9a² = (3a)² a 16b² = (4b)².",
        "Rozdíl čtverců se rozloží na součin (první člen − druhý člen)(první člen + druhý člen).",
        f"{q} = {a}."],
       same(q, a) and same("9a²", "(3a)²") and same("16b²", "(4b)²"), space=2)

# ---------------------------------------------------------------- Náročnější
q = "103² − 97²"
r = ev(q)
T.task(3, f"Vypočtěte bez kalkulačky pomocí vzorce: {q}", "1 200",
       ["Použijeme rozdíl čtverců a² − b² = (a − b)(a + b).",
        "103² − 97² = (103 − 97)(103 + 97) = 6 · 200.",
        "6 · 200 = 1 200."],
       r == 1200 == (103 - 97) * (103 + 97) == 6 * 200 and 103 ** 2 == 10609 and 97 ** 2 == 9409)

q = "(x + 3)² − (x − 3)²"
opts = ["18", "6x + 18", "12x", "2x² + 18", "6x"]
T.task(3, f"Výraz {q} je roven:", "C",
       ["Obě mocniny rozepíšeme: (x + 3)² = x² + 6x + 9 a (x − 3)² = x² − 6x + 9.",
        "Druhou závorku odečítáme, proto změníme znaménka: x² + 6x + 9 − x² + 6x − 9.",
        "Sečteme: 6x + 6x = 12x, tedy C. Zkouška pro x = 1: 16 − 4 = 12. ✓",
        "Chyby: A vznikne při špatně změněných znaménkách, B z (x − 3)² = x² − 9, D ze sčítání místo odčítání, E z (x − 3)² = x² + 9."],
       [P(o) == P(q) for o in opts] == [False, False, True, False, False] and ev(q, x=1) == 12
       and show(P("(x + 3)² + (x − 3)²")) == "2x² + 18" and show(P("(x + 3)² − (x² − 9)")) == "6x + 18",
       kind="choice", options=opts, space=3)

q, a = "(x + 2)(x + 5) − x(x + 3)", "4x + 10"
T.task(3, "Obdélník má jednu stranu dlouhou x cm, druhá strana je o 3 cm delší. Obě strany prodloužíme o 2 cm. "
          "Zapište výrazem, o kolik cm² se zvětší obsah, a výraz zjednodušte.", f"{a} (cm²)",
       ["Původní strany jsou x a x + 3 cm, obsah x(x + 3) = x² + 3x.",
        "Nové strany jsou x + 2 a x + 5 cm, obsah (x + 2)(x + 5) = x² + 7x + 10.",
        f"Přírůstek: x² + 7x + 10 − (x² + 3x) = {a} (cm²).",
        "Zkouška pro x = 1: obdélník 1 × 4 má obsah 4, nový 3 × 6 má obsah 18, rozdíl 14 = 4 · 1 + 10. ✓"],
       show(P(q)) == a and show(P("x(x + 3)")) == "x² + 3x" and show(P("(x + 2)(x + 5)")) == "x² + 7x + 10"
       and 3 * 6 - 1 * 4 == 14 == ev(a, x=1), space=4)

q, a = "2x² − 12x + 18", "2(x − 3)²"
T.task(3, f"Rozložte na součin: {q}", a,
       ["Vytkneme společný činitel 2: 2x² − 12x + 18 = 2(x² − 6x + 9).",
        "V závorce je druhá mocnina dvojčlenu: x² − 2 · x · 3 + 3² = (x − 3)².",
        f"{q} = {a}.",
        "Zkouška roznásobením: 2(x² − 6x + 9) = 2x² − 12x + 18. ✓"],
       same(q, a) and same("x² − 6x + 9", "(x − 3)²") and same(q, "2(x² − 6x + 9)"), space=3)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
q, a = "(2x + 1)² − (2x − 1)(2x + 1)", "4x + 2"
T.diagnostic(f"Upravte výraz a zapište v základním tvaru: {q}", a,
             ["(2x + 1)² = 4x² + 4x + 1.", "(2x − 1)(2x + 1) = 4x² − 1 (rozdíl čtverců).",
              f"4x² + 4x + 1 − 4x² + 1 = {a}."],
             show(P(q)) == a and show(P("(2x + 1)²")) == "4x² + 4x + 1" and show(P("(2x − 1)(2x + 1)")) == "4x² − 1")

q = "9x² − 12x + 4"
opts = ["(3x + 2)²", "(3x − 2)(3x + 2)", "(3x − 4)²", "(3x − 2)²", "(9x − 2)²"]
T.diagnostic(f"Který z výrazů je roven {q}?", "D",
             ["Hledáme dvojčlen, jehož druhá mocnina je 9x² − 12x + 4: 9x² = (3x)² a 4 = 2².",
              "Prostřední člen −12x = −2 · 3x · 2 má znaménko minus, proto (3x − 2)² = 9x² − 12x + 4, tedy D.",
              "A má +12x, B je 9x² − 4 bez prostředního členu, C má −24x a E začíná 81x²."],
             [P(o) == P(q) for o in opts] == [False, False, False, True, False] and show(P("(3x + 2)²")) == "9x² + 12x + 4"
             and show(P("(3x − 2)(3x + 2)")) == "9x² − 4" and show(P("(3x − 4)²")) == "9x² − 24x + 16",
             kind="choice", options=opts)

T.save()
