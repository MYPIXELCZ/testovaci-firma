#!/usr/bin/env python3
"""Téma 4: Slovní úlohy řešené rovnicí (úlohy 5–8 jednotné zkoušky). Formát v _lib.py, vzor 01_zlomky.py.

Každá úloha je psaná stejně: „Označme x“, zápis rovnice, řešení, zkouška slovní odpovědí. Rovnice v zadání i v postupu
se ověřují přímo z textu (parser níže, Fraction), výsledek navíc nezávisle podle podmínek ze zadání.
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


def holds(e, x=0, y=0):
    return _d(e)(x, y) == 0


def val(side, x=0, y=0):
    return _fn(side)(x, y)


def same(a, b):
    """Dva výrazy (stupeň nejvýše 2) se rovnají pro každé x: ověřeno na sedmi hodnotách."""
    fa, fb = _fn(a), _fn(b)
    return all(fa(t) == fb(t) for t in range(-3, 4))


def ok1(x0, q, *steps):
    """Řešení rovnice q je právě x0 a každá rovnice v postupu platí pro x0."""
    return solve1(q) == x0 and all(holds(s, x0) for s in steps)


# ---------------------------------------------------------------- téma
T = Topic(4, "slovni", "Slovní úlohy řešené rovnicí",
          "Slovní úlohy s neznámou („označme x“) jsou v úlohách 5 až 8 jednotné zkoušky téměř v každém testu a správně je vyřeší jen necelá třetina žáků. "
          "Každou úlohu pište stejně: označení neznámé, rovnice, řešení, zkouška, slovní odpověď.",
          ["Neznámou zvolte tak, aby se k ní vztahovaly ostatní údaje, a pojmenujte ji větou: „Označme x počet žáků ve třídě.“ Odpověď na konci musí odpovídat na otázku zadání, ne jen vypsat x.",
           "Při „o třetinu víc“ je základem původní hodnota: nová = x + 1/3 · x = 4/3 · x. Když je zadaná nová hodnota, dělte číslem 4/3 (násobte 3/4), neodečítejte od ní třetinu. "
           "Příklad: 4/3 · x = 48 dává x = 36, ne 48 − 16 = 32.",
           "Typická chyba: „o třetinu méně“ a „o třetinu víc“ nejsou opak. Je-li A o třetinu menší než B, je B větší než A o polovinu, tedy o 50 %, ne o třetinu. "
           "Základem je vždy to, s čím se porovnává (co stojí za slovem „než“). Příklad: B = 90, A = 60, rozdíl 30 je třetina z 90, ale polovina z 60.",
           "Větu překládejte slovo po slovu: „o 5 víc než Jana“ je x + 5, „dvakrát tolik“ je 2x, „před 3 lety“ je x − 3, „za 4 roky“ je x + 4. U věku se ke každému z lidí přičítá nebo odčítá stejné číslo.",
           "Zlomek z části není zlomek z celku: třetina ze zbytku je jiná než třetina celku. Nejdřív zjistěte, co zbylo (x − x/3 = 2/3 · x), a z toho počítejte dál.",
           "Zkoušku dělejte podle textu úlohy, ne jen v rovnici. Posuďte, zda výsledek dává smysl: počet lidí je celé číslo, věk není záporný, strany trojúhelníku musí splnit trojúhelníkovou nerovnost."])

# ---------------------------------------------------------------- řešený příklad
q = "x + 4/3 · x = 42"; s1 = "3x + 4x = 126"; s2 = "7x = 126"
hoch, divky = F(18), F(4, 3) * 18
T.example("Ve sportovním kroužku je o třetinu víc dívek než chlapců. Celkem se kroužku účastní 42 dětí. Kolik je v něm chlapců a kolik dívek? "
          "Označte neznámou, zapište rovnici a vyřešte ji.",
          ["Označme x počet chlapců. Dívek je o třetinu víc: x + 1/3 · x = 4/3 · x.",
           f"Chlapců a dívek je dohromady 42: {q}.",
           f"Vynásobíme všechny členy třemi: {s1}, tedy {s2}, x = 18.",
           "Dívek je 4/3 · 18 = 24.",
           "Zkouška: 24 − 18 = 6 a 6 je třetina z 18 ✓, 18 + 24 = 42 ✓."],
          "18 chlapců a 24 dívek",
          ok1(18, q, s1, s2) and divky == 24 and divky - hoch == hoch / 3 and hoch + divky == 42)

# ---------------------------------------------------------------- Základ
q = "3x − 7 = 20"; s1 = "3x = 27"
T.task(1, "Myslím si číslo. Když jeho trojnásobek zmenším o 7, dostanu 20. Které číslo si myslím? Označte neznámou, zapište rovnici a vyřešte ji.", "9",
       ["Označme x číslo, které si myslím.", f"Trojnásobek čísla je 3x, po zmenšení o 7 dostaneme 20: {q}.", f"Přičteme 7: {s1}. Vydělíme třemi: x = 9.",
        "Zkouška: 3 · 9 − 7 = 27 − 7 = 20 ✓. Myslím si číslo 9."],
       ok1(9, q, s1) and 3 * 9 - 7 == 20, space=4)

q = "x + (x + 4) = 26"; s1 = "2x + 4 = 26"; s2 = "2x = 22"
T.task(1, "Jana je o 4 roky starší než její bratr. Dohromady mají 26 let. Kolik let je Janě a kolik bratrovi? Označte neznámou, zapište rovnici a vyřešte ji.",
       "bratrovi 11 let, Janě 15 let",
       ["Označme x věk bratra v letech. Janě je x + 4 let.", f"Dohromady mají 26 let: {q}.", f"Sloučíme: {s1}, tedy {s2}, x = 11.",
        "Janě je 11 + 4 = 15 let. Zkouška: 15 − 11 = 4 ✓, 11 + 15 = 26 ✓."],
       ok1(11, q, s1, s2) and 11 + 4 == 15 and 11 + 15 == 26, space=4)

q = "x + 2x + (x + 100) = 1 300"; s1 = "4x + 100 = 1 300"; s2 = "4x = 1 200"
T.task(1, "Tři kamarádi si rozdělili výdělek z brigády 1 300 Kč. Petr dostal dvakrát víc než Marek a Tomáš o 100 Kč víc než Marek. "
          "Kolik korun dostal každý? Označte neznámou, zapište rovnici a vyřešte ji.",
       "Marek 300 Kč, Petr 600 Kč, Tomáš 400 Kč",
       ["Označme x částku, kterou dostal Marek, v korunách. Petr dostal 2x, Tomáš x + 100.", f"Dohromady dostali 1 300 Kč: {q}.",
        f"Sloučíme: {s1}, tedy {s2}, x = 300.", "Petr dostal 2 · 300 = 600 Kč, Tomáš 300 + 100 = 400 Kč.", "Zkouška: 300 + 600 + 400 = 1 300 ✓."],
       ok1(300, q, s1, s2) and 300 + 2 * 300 + 400 == 1300 and 400 - 300 == 100, space=5)

nova = 300
opts = ["75 Kč", "100 Kč", "200 Kč", "225 Kč", "400 Kč"]
vals = [int(o.split()[0]) for o in opts]
q = "4/3 · x = 300"
T.task(1, "Po zdražení o třetinu stojí lyžařský pas 300 Kč. Kolik stál před zdražením?", "D",
       ["Označme x původní cenu v korunách. Po zdražení o třetinu je cena x + 1/3 · x = 4/3 · x.", f"Nová cena je 300 Kč: {q}.",
        "x = 300 : 4/3 = 300 · 3/4 = 225.", "Zkouška: třetina ze 225 je 75 a 225 + 75 = 300 ✓. Správná je možnost D.",
        "Ostatní možnosti jsou typické chyby: 200 vznikne odečtením třetiny od 300 (základem je ale původní cena, ne nová), 100 je třetina z 300, "
        "75 je samotné zdražení a 400 je 4/3 z 300."],
       solve1(q) == 225 and [v for v in vals if v + F(v, 3) == nova] == [225] and nova - nova // 3 == 200 and nova // 3 == 100
       and F(1, 3) * 225 == 75 and F(4, 3) * nova == 400,
       kind="choice", options=opts, space=3)

q = "2 · (x + x + 4) = 36"; s1 = "4x + 8 = 36"; s2 = "4x = 28"
T.task(1, "Obdélníková zahrada má obvod 36 m. Jedna její strana je o 4 m delší než druhá. Určete délky stran zahrady. "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "7 m a 11 m",
       ["Označme x délku kratší strany v metrech. Delší strana má x + 4 metry.", f"Obvod obdélníku je 2 · (a + b): {q}.",
        f"Roznásobíme: {s1}, tedy {s2}, x = 7.", "Kratší strana má 7 m, delší 7 + 4 = 11 m.", "Zkouška: 2 · (7 + 11) = 2 · 18 = 36 ✓."],
       ok1(7, q, s1, s2) and 2 * (7 + 11) == 36 and 11 - 7 == 4, space=4)

# ---------------------------------------------------------------- Jako u zkoušky
q = "x + 33 = 3 · (x + 5)"; s1 = "x + 33 = 3x + 15"; s2 = "18 = 2x"
syn, otec = 9, 37
T.task(2, "Otec je o 28 let starší než syn. Za 5 let bude otci třikrát tolik let co synovi. Kolik let je nyní synovi a kolik otci? "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "synovi 9 let, otci 37 let",
       ["Označme x věk syna nyní. Otci je nyní x + 28 let.", "Za 5 let bude synovi x + 5 let a otci x + 28 + 5 = x + 33 let.",
        f"Otci bude třikrát tolik: {q}.", f"Roznásobíme: {s1}, tedy {s2}, x = 9.",
        "Zkouška: za 5 let bude synovi 14 a otci 42 let, 3 · 14 = 42 ✓ a 42 − 14 = 28 ✓.", "Odpověď: Synovi je 9 let, otci 37 let."],
       ok1(9, q, s1, s2) and otec - syn == 28 and otec + 5 == 3 * (syn + 5) and otec == 9 + 28, space=5)

q = "x/3 + x/4 + 35 = x"; s1 = "4x + 3x + 420 = 12x"; s2 = "7x + 420 = 12x"; s3 = "420 = 5x"
T.task(2, "Cyklista ujel první den třetinu trasy, druhý den čtvrtinu trasy a třetí den zbylých 35 km. Jak dlouhá byla celá trasa? "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "84 km",
       ["Označme x délku celé trasy v kilometrech. První den ujel x/3, druhý den x/4 a třetí den 35 km.", f"Všechny tři dny dohromady dají celou trasu: {q}.",
        f"Vynásobíme všechny členy dvanácti: {s1}, tedy {s2}.", f"Odečteme 7x: {s3}, x = 84.",
        "Zkouška: 84 : 3 = 28 km, 84 : 4 = 21 km, 28 + 21 + 35 = 84 ✓."],
       ok1(84, q, s1, s2, s3) and F(84, 3) + F(84, 4) + 35 == 84, space=5)

q = "x + x + (x − 3) = 27"; s1 = "3x − 3 = 27"; s2 = "3x = 30"
T.task(2, "Rovnoramenný trojúhelník má obvod 27 cm. Základna je o 3 cm kratší než rameno. Jak dlouhé jsou strany trojúhelníku? "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "ramena 10 cm, základna 7 cm",
       ["Označme x délku ramene v centimetrech (obě ramena jsou stejně dlouhá). Základna má x − 3 cm.", f"Obvod je součet tří stran: {q}.",
        f"Sloučíme: {s1}, tedy {s2}, x = 10.", "Ramena mají 10 cm, základna 10 − 3 = 7 cm.",
        "Zkouška: 10 + 10 + 7 = 27 ✓. Trojúhelník existuje, protože 7 + 10 > 10."],
       ok1(10, q, s1, s2) and 10 + 10 + 7 == 27 and 7 + 10 > 10 and 10 + 10 > 7, space=4)

q = "x/4 + x/12 = 1"; s1 = "3x + x = 12"
T.task(2, "Petr by posekal zahradu sám za 4 hodiny, jeho táta by ji sám posekal za 12 hodin. Za jak dlouho ji posekají společně? "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "za 3 hodiny",
       ["Označme x počet hodin, za které zahradu posekají společně. Celá zahrada je 1.",
        "Petr poseká za hodinu 1/4 zahrady, táta 1/12 zahrady. Za x hodin posekají x/4 a x/12.", f"Dohromady posekají celou zahradu: {q}.",
        f"Vynásobíme dvanácti: {s1}, tedy 4x = 12 a x = 3.",
        "Zkouška: za 3 hodiny poseká Petr 3/4 zahrady a táta 3/12 = 1/4 zahrady, dohromady 3/4 + 1/4 = 1 ✓.", "Odpověď: Společně zahradu posekají za 3 hodiny."],
       ok1(3, q, s1, "4x = 12") and F(3, 4) + F(3, 12) == 1 and F(3, 12) == F(1, 4), space=5)

q = "x + (x + 2) + (x + 4) = 129"; s1 = "3x + 6 = 129"; s2 = "3x = 123"
T.task(2, "Součet tří po sobě jdoucích lichých čísel je 129. Určete tato čísla. Označte neznámou, zapište rovnici a vyřešte ji.", "41, 43 a 45",
       ["Označme x nejmenší z čísel. Další liché číslo je o 2 větší, třetí o 4 větší: x, x + 2, x + 4.", f"Součet je 129: {q}.",
        f"Sloučíme: {s1}, tedy {s2}, x = 41.", "Čísla jsou 41, 43 a 45.", "Zkouška: 41 + 43 + 45 = 129 ✓ a všechna tři čísla jsou lichá."],
       ok1(41, q, s1, s2) and 41 + 43 + 45 == 129 and all(n % 2 == 1 for n in (41, 43, 45)), space=4)

opts = ["x + 20 = 100", "2x + 20 = 100", "2x − 20 = 100", "2 · (x + 20) = 100", "x − 20 = 100"]
jana, petr = 40, 60
T.task(2, "Petr má o 20 Kč víc než Jana. Dohromady mají 100 Kč. Označme x počet korun, které má Jana. Která rovnice odpovídá zadání?", "B",
       ["Jana má x korun, Petr o 20 víc, tedy x + 20 korun.", "Dohromady mají x + (x + 20) = 2x + 20 korun, a to je 100 Kč: 2x + 20 = 100. Správná je možnost B.",
        "Zkouška: x = 40, Petr má 60 Kč, 60 − 40 = 20 ✓ a 40 + 60 = 100 ✓.",
        "Ostatní možnosti: A počítá jen s Petrem, C má minus místo plus, D počítá, že oba mají Petrovu částku, E odčítá místo přičítání."],
       [o for o in opts if solve1(o) == jana] == ["2x + 20 = 100"] and petr - jana == 20 and jana + petr == 100
       and len({solve1(o) for o in opts}) == 5,
       kind="choice", options=opts, space=2)

x = 90
pavel = x - F(x, 3)
# tvrzení 2: Lukáš má o třetinu víc než Pavel, tedy x = 4/3 · Pavel (neplatí); tvrzení 3: o 50 % víc, tedy x = 3/2 · Pavel (platí)
stm = [pavel == F(2, 3) * x, x == F(4, 3) * pavel, x == F(3, 2) * pavel]
T.task(2, "Pavel má o třetinu méně žetonů než Lukáš. Lukáš má x žetonů. Platí tato tvrzení?", "ANO, NE, ANO",
       ["Pavel má x − 1/3 · x = 2/3 · x žetonů. Tvrzení platí.",
        "Lukáš má víc o x − 2/3 · x = 1/3 · x, ale základem pro „víc“ je Pavlův počet: 1/3 · x : 2/3 · x = 1/2. Lukáš má víc o polovinu, ne o třetinu. "
        "Příklad: Lukáš 90, Pavel 60, rozdíl 30 je třetina z 90, ale polovina z 60. Tvrzení neplatí.",
        "Polovina je 50 %, takže Lukáš má o 50 % víc žetonů než Pavel. Tvrzení platí."],
       stm == [True, False, True] and F(90) - F(60) == 30 and F(30, 90) == F(1, 3) and F(30, 60) == F(1, 2) and pavel == 60
       and F(1, 3) / F(2, 3) == F(1, 2),
       kind="yesno", options=["Pavel má 2/3 · x žetonů.", "Lukáš má o třetinu víc žetonů než Pavel.", "Lukáš má o 50 % víc žetonů než Pavel."], space=1)

# ---------------------------------------------------------------- Náročnější
q = "x + 5/4 · x + 2x = 5 100"; s1 = "4x + 5x + 8x = 20 400"; s2 = "17x = 20 400"
T.task(3, "Babička rozdělila mezi tři vnuky dohromady 5 100 Kč. Prostřední dostal o čtvrtinu víc než nejmladší a nejstarší dvakrát tolik co nejmladší. "
          "Kolik korun dostal každý? Označte neznámou, zapište rovnici a vyřešte ji.",
       "nejmladší 1 200 Kč, prostřední 1 500 Kč, nejstarší 2 400 Kč",
       ["Označme x částku nejmladšího vnuka v korunách. Prostřední dostal x + 1/4 · x = 5/4 · x, nejstarší 2x.", f"Dohromady dostali 5 100 Kč: {q}.",
        f"Vynásobíme všechny členy čtyřmi: {s1}, tedy {s2} a x = 1 200.", "Prostřední dostal 5/4 · 1 200 = 1 500 Kč, nejstarší 2 · 1 200 = 2 400 Kč.",
        "Zkouška: 1 500 − 1 200 = 300 je čtvrtina z 1 200 ✓ a 1 200 + 1 500 + 2 400 = 5 100 ✓."],
       ok1(1200, q, s1, s2) and F(5, 4) * 1200 == 1500 and 1500 - 1200 == 1200 // 4 and 1200 + 1500 + 2400 == 5100, space=6)

q = "x − x/3 − 1/2 · (x − x/3) = 120"; s1 = "x − x/3 − 1/3 · x = 120"
T.task(3, "Honza dostal od babičky peníze. Třetinu z nich utratil za jízdenky. Z toho, co mu zbylo, utratil polovinu v kině. Nakonec mu zbylo 120 Kč. "
          "Kolik korun od babičky dostal? Označte neznámou, zapište rovnici a vyřešte ji.", "360 Kč",
       ["Označme x částku, kterou Honza dostal, v korunách. Na jízdenky utratil x/3, zbylo mu x − x/3 = 2/3 · x.",
        "V kině utratil polovinu zbytku: 1/2 · 2/3 · x = 1/3 · x.", f"Zbylo mu {s1}, tedy 1/3 · x = 120 a x = 360.",
        "Zkouška: jízdenky 360 : 3 = 120 Kč, zbývá 240 Kč, kino 240 : 2 = 120 Kč, zbude 240 − 120 = 120 Kč ✓."],
       ok1(360, q, s1, "1/3 · x = 120") and same("x − x/3", "2/3 · x") and same("1/2 · 2/3 · x", "1/3 · x")
       and 360 // 3 == 120 and 360 - 120 == 240 and 240 // 2 == 120 and 240 - 120 == 120, space=5)

q = "0,12 · (3 + x) = 0,2 · 3"; s1 = "0,36 + 0,12x = 0,6"; s2 = "0,12x = 0,24"
T.task(3, "Ke 3 kg roztoku, který obsahuje 20 % soli, přidáme vodu. Kolik kilogramů vody je třeba přidat, aby roztok obsahoval 12 % soli? "
          "Označte neznámou, zapište rovnici a vyřešte ji.", "2 kg vody",
       ["Označme x množství přidané vody v kilogramech. Ve 3 kg roztoku je 20 % soli, tedy 0,2 · 3 = 0,6 kg soli.",
        "Voda množství soli nezmění. Nový roztok váží 3 + x kg a má obsahovat 12 % soli: 0,12 · (3 + x) = 0,6.",
        f"Roznásobíme: {s1}, tedy {s2} a x = 2.",
        "Zkouška: nový roztok váží 5 kg a 12 % z 5 kg je 0,6 kg soli, stejně jako na začátku ✓."],
       ok1(2, q, s1, s2) and F(20, 100) * 3 == F(6, 10) and F(12, 100) * (3 + 2) == F(6, 10) and F(12, 100) * 5 == F(6, 10), space=5)

q = "(x + 3) · (x − 2) = x²"; s1 = "x² + x − 6 = x²"; s2 = "x − 6 = 0"
T.task(3, "Strana čtverce má délku x cm. Jeden rozměr čtverce zvětšíme o 3 cm a druhý zmenšíme o 2 cm, vznikne obdélník. "
          "Obsah obdélníku je stejný jako obsah původního čtverce. Určete délku strany čtverce. Zapište rovnici a vyřešte ji.", "6 cm",
       ["Označme x délku strany čtverce v centimetrech. Obdélník má rozměry (x + 3) cm a (x − 2) cm.", f"Obsahy se rovnají: {q}.",
        f"Roznásobíme levou stranu: (x + 3) · (x − 2) = x² − 2x + 3x − 6, tedy {s1}.", f"Členy x² se na obou stranách zruší: {s2}, x = 6.",
        "Zkouška: obdélník 9 cm na 4 cm má obsah 36 cm², čtverec 6 cm na 6 cm také 36 cm² ✓."],
       ok1(6, q, s1, s2) and same("(x + 3) · (x − 2)", "x² − 2x + 3x − 6") and same("x² − 2x + 3x − 6", "x² + x − 6")
       and (6 + 3) * (6 - 2) == 36 == 6 * 6, space=5)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
q = "x + 5/4 · x = 180"; s1 = "4x + 5x = 720"; s2 = "9x = 720"
T.diagnostic("Ve skladu bylo o čtvrtinu víc jablek než hrušek. Jablek a hrušek bylo dohromady 180 kg. Kolik kilogramů jablek bylo ve skladu? "
             "Označte neznámou, zapište rovnici a vyřešte ji.", "100 kg",
             ["Označme x hmotnost hrušek v kilogramech. Jablek je o čtvrtinu víc: x + 1/4 · x = 5/4 · x.", f"Dohromady je to 180 kg: {q}.",
              f"Vynásobíme čtyřmi: {s1}, tedy {s2} a x = 80.", "Jablek je 5/4 · 80 = 100 kg. Zkouška: 100 − 80 = 20 je čtvrtina z 80 ✓ a 80 + 100 = 180 ✓."],
             ok1(80, q, s1, s2) and F(5, 4) * 80 == 100 and 100 - 80 == 80 // 4 and 80 + 100 == 180)

opts = ["400 Kč", "800 Kč", "900 Kč", "1 200 Kč", "1 800 Kč"]
vals = [int(o.replace(" Kč", "").replace(" ", "")) for o in opts]
q = "2/3 · x = 600"
T.diagnostic("Mikina je o třetinu levnější než bunda. Mikina stojí 600 Kč. Kolik stojí bunda?", "C",
             ["Označme x cenu bundy v korunách. Mikina stojí x − 1/3 · x = 2/3 · x.", f"Mikina stojí 600 Kč: {q}.",
              "x = 600 : 2/3 = 600 · 3/2 = 900.", "Zkouška: třetina z 900 je 300 a 900 − 300 = 600 ✓. Správná je možnost C.",
              "Typické chyby: 800 je 600 + 1/3 · 600 (třetina se bere z ceny mikiny, ale základem je cena bundy), 400 je 2/3 · 600, 1 200 je dvojnásobek a 1 800 trojnásobek."],
             solve1(q) == 900 and [v for v in vals if v - F(v, 3) == 600] == [900] and 600 + 600 // 3 == 800 and F(2, 3) * 600 == 400
             and 2 * 600 == 1200 and 3 * 600 == 1800,
             kind="choice", options=opts)

T.save()
