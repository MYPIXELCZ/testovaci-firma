#!/usr/bin/env python3
"""Téma 12: Úsudek a vzory (úloha 16 u zkoušky). Obrazce (SVG) se kreslí stejným generátorem, kterým se počítají výsledky,
vzorce se ověřují cyklem a kombinatorika hrubou silou. Formát v _lib.py, vzor je 01_zlomky.py."""
import sys
from datetime import date, timedelta
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402

# ------------------------------------------------------------------ pomůcky pro obrázky (SVG, šířka viewBox 248 = 62 mm)
INK, SOFT, GREY, HEAD = "#1c2230", "#dbe4fb", "#c4cfee", "#f5b82e"
W = 248


def svg(inner: str, h: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" font-family="Inter,Arial" font-size="10">{inner}</svg>'


def txt(x, y, s, size=10, anchor="middle") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{INK}">{s}</text>'


def rect(x, y, w, h, fill="#ffffff", sw=1.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, w=1.0, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="{w}"{d}/>'


def dot(x, y, r=2.6, fill=INK) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1"/>'


def bbox(f):
    xs, ys = [], []
    for c, r, _ in f.get("cells", []):
        xs += [c, c + 1]
        ys += [r, r + 1]
    for (x1, y1), (x2, y2) in f.get("segs", []):
        xs += [x1, x2]
        ys += [y1, y2]
    return min(xs), min(ys), max(xs), max(ys)


def frames_svg(frames, gap=1.2, smax=24, align="center") -> str:
    """Obrazce 1., 2., 3., … vedle sebe. Obrazec = {"cells": [(sloupec, řádek, výplň)], "segs": [((x1, y1), (x2, y2))]} v mřížkových jednotkách."""
    pad, cap = 6, 14
    boxes = [bbox(f) for f in frames]
    ws = [b[2] - b[0] for b in boxes]
    hs = [b[3] - b[1] for b in boxes]
    total = sum(ws) + gap * (len(frames) - 1)
    s = min((W - 2 * pad) / total, smax)
    hmax = max(hs)
    height = round(hmax * s + 2 * pad + cap)
    x = (W - total * s) / 2
    o = []
    for i, f in enumerate(frames):
        x0, y0 = boxes[i][0], boxes[i][1]
        top = pad + ((hmax - hs[i]) * s if align == "bottom" else (hmax - hs[i]) * s / 2)
        dx, dy = x - x0 * s, top - y0 * s
        for c, r, fill in f.get("cells", []):
            o.append(rect(dx + c * s, dy + r * s, s, s, fill))
        for (x1, y1), (x2, y2) in sorted(f.get("segs", [])):
            k = .07  # zápalka: kratší než hrana, s hlavičkou na jednom konci
            a, b = (dx + (x1 + (x2 - x1) * k) * s, dy + (y1 + (y2 - y1) * k) * s), (dx + (x2 - (x2 - x1) * k) * s, dy + (y2 - (y2 - y1) * k) * s)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
            o.append(dot(b[0], b[1], 1.8, HEAD))
        o.append(txt(x + ws[i] * s / 2, height - 3, f"{i + 1}.", 10))
        x += (ws[i] + gap) * s
    return svg("".join(o), height)


# generátory obrazců (stejné slouží k výpočtu výsledků)
def edges(squares):
    e = set()
    for c, r in squares:
        e |= {((c, r), (c + 1, r)), ((c, r + 1), (c + 1, r + 1)), ((c, r), (c, r + 1)), ((c + 1, r), (c + 1, r + 1))}
    return e


def row_squares(n):      # řada n čtverců ze zápalek
    return {"segs": edges([(i, 0) for i in range(n)])}


def row_triangles(n):    # řada n trojúhelníků ze zápalek
    h = 0.87
    v = [(k / 2, 0 if k % 2 == 0 else h) for k in range(n + 2)]
    e = {(v[k], v[k + 1]) for k in range(n + 1)} | {(v[k], v[k + 2]) for k in range(n)}
    return {"segs": {tuple(sorted(p)) for p in e}}


def stairs(n):           # schody z n sloupců
    return {"cells": [(c, n - 1 - k, SOFT) for c in range(n) for k in range(c + 1)]}


def cross(n):            # kříž: šedý střed a čtyři ramena po n bílých čtvercích
    cells = [(n, n, GREY)]
    for i in range(1, n + 1):
        cells += [(n - i, n, "#ffffff"), (n + i, n, "#ffffff"), (n, n - i, "#ffffff"), (n, n + i, "#ffffff")]
    return {"cells": cells}


def net(n):              # čtvercová síť n × n ze zápalek
    return {"segs": edges([(c, r) for c in range(n) for r in range(n)])}


def count(f):
    return len(f.get("cells", [])) + len(f.get("segs", []))


def magic_svg(given) -> str:
    s, x0, y0 = 26, (W - 78) / 2, 6
    o = []
    for r in range(3):
        for c in range(3):
            o.append(rect(x0 + c * s, y0 + r * s, s, s, SOFT if (r, c) in given else "#ffffff", 1.2))
            if (r, c) in given:
                o.append(txt(x0 + c * s + s / 2, y0 + r * s + s / 2 + 5, str(given[(r, c)]), 14))
    return svg("".join(o), 90)


def paths_svg(cols, rows, a, b, c) -> str:
    s, x0 = 40, (W - cols * 40) / 2
    y0 = 14
    X = lambda i: x0 + i * s
    Y = lambda j: y0 + (rows - j) * s
    o = []
    for i in range(cols + 1):
        o.append(line(X(i), Y(0), X(i), Y(rows), 1.2))
    for j in range(rows + 1):
        o.append(line(X(0), Y(j), X(cols), Y(j), 1.2))
    for i in range(cols + 1):
        for j in range(rows + 1):
            o.append(dot(X(i), Y(j), 2.2, "#ffffff"))
    for p, name, dxy in ((a, "A", (-9, 13)), (b, "B", (9, -6)), (c, "C", (-9, -5))):
        o.append(dot(X(p[0]), Y(p[1]), 3.6) + txt(X(p[0]) + dxy[0], Y(p[1]) + dxy[1], name, 11))
    return svg("".join(o), rows * s + 34)


def symmetry_svg(shaded) -> str:
    s, x0, y0 = 22, (W - 110) / 2, 14
    o = []
    for r in range(5):
        for c in range(5):
            o.append(rect(x0 + c * s, y0 + r * s, s, s, GREY if (r, c) in shaded else "#ffffff", .8))
    o.append(line(x0 + 2.5 * s, y0 - 8, x0 + 2.5 * s, y0 + 5 * s + 8, 1.1, "4 3") + txt(x0 + 2.5 * s + 6, y0 - 3, "o", 10, "start"))
    o.append(line(x0 - 8, y0 + 2.5 * s, x0 + 5 * s + 8, y0 + 2.5 * s, 1.1, "4 3") + txt(x0 + 5 * s + 10, y0 + 2.5 * s + 3.5, "p", 10, "start"))
    return svg("".join(o), 5 * s + 30)


# ------------------------------------------------------------------ téma
T = Topic(12, "vzory", "Úsudek a vzory",
          "Úloha 16 je nestandardní: posloupnost obrazců, číselný vzor nebo logická úvaha. Patří k nejhůř řešeným úlohám celého testu a hodně žáků ji vynechá. "
          "První podúlohu přitom často vyřešíte prostým vypsáním prvních kroků.",
          ["Prvních pár členů si zapište do tabulky (číslo kroku, počet). Teprve potom hledejte pravidlo a ověřte ho na všech zapsaných členech, ne jen na posledním.",
           "Stejné rozdíly mezi sousedními členy znamenají, že se pořád přičítá totéž číslo (posloupnost 3, 7, 11, 15, … je 4n − 1). Rostou-li samy rozdíly, jde o vzor typu schody nebo čtvercová síť.",
           "Vzor, který se stále opakuje (korálky, dny v týdnu), řešte zbytkem po dělení (délka skupiny je 4): 50 : 4 = 12 a zbytek 2, takže 50. člen je druhý ve skupině.",
           "Při počítání možností je vypisujte uspořádaně (podle prvního kroku nebo podle abecedy). Nic nevynechejte a nic nepočítejte dvakrát.",
           "U logických úloh vyškrtávejte v tabulce, co nejde. U výroků o pravdě a lži předpokládejte, že výrok platí, a hledejte spor.",
           "Úlohu nevynechávejte: za špatnou odpověď se body neodečítají a první podúlohu často zvládnete tím, že si prvních pár kroků nakreslíte nebo vypíšete."])

# ---------------------------------------------------------------- řešený příklad
mat = [count(row_squares(n)) for n in range(1, 60)]
n100 = max(n for n in range(1, 60) if count(row_squares(n)) <= 100)
T.example("Ze zápalek skládáme řadu čtverců: jeden čtverec potřebuje 4 zápalky, dva čtverce vedle sebe (se společnou stranou) 7 zápalek a tři čtverce 10 zápalek. "
          "a) Kolik zápalek potřebujeme na 10 čtverců v řadě? b) Kolik čtverců v řadě postavíme ze 100 zápalek?",
          ["Zapíšeme si členy: 1 čtverec → 4 zápalky, 2 čtverce → 7, 3 čtverce → 10. Každý další čtverec přidá 3 zápalky (tři nové strany).",
           "Pro n čtverců tedy potřebujeme 4 + 3 · (n − 1) = 3n + 1 zápalek. Ověříme: n = 3 dává 3 · 3 + 1 = 10. ✓",
           "a) n = 10: 3 · 10 + 1 = 31 zápalek.",
           "b) Řešíme 3n + 1 = 100, tedy 3n = 99 a n = 33 čtverců."],
          "a) 31 zápalek; b) 33 čtverců",
          mat[:3] == [4, 7, 10] and all(mat[n - 1] == 3 * n + 1 for n in range(1, 60)) and mat[9] == 31 and n100 == 33 and count(row_squares(33)) == 100)

# ---------------------------------------------------------------- Základ
a = [7 + 5 * i for i in range(6)]
b = [3 * 2 ** i for i in range(6)]
T.task(1, "Doplňte do každé řady další dva členy. a) 7, 12, 17, 22, …; b) 3, 6, 12, 24, …",
       "a) 27, 32; b) 48, 96",
       ["a) Každý člen je o 5 větší než předchozí: 22 + 5 = 27 a 27 + 5 = 32.",
        "b) Každý člen je dvojnásobkem předchozího: 24 · 2 = 48 a 48 · 2 = 96."],
       a[:4] == [7, 12, 17, 22] and a[4:] == [27, 32] and b[:4] == [3, 6, 12, 24] and b[4:] == [48, 96], space=2)

tri = [count(row_triangles(n)) for n in range(1, 40)]
n25 = [n for n in range(1, 40) if count(row_triangles(n)) == 25]
T.task(1, "Ze stejně dlouhých zápalek skládáme řadu trojúhelníků (obrázek ukazuje první tři obrazce). "
          "a) Kolik zápalek potřebujeme na 6 trojúhelníků v řadě? b) Kolik trojúhelníků v řadě postavíme z 25 zápalek?",
       "a) 13 zápalek; b) 12 trojúhelníků",
       ["Zapíšeme: 1 trojúhelník → 3 zápalky, 2 trojúhelníky → 5, 3 trojúhelníky → 7. Každý další trojúhelník přidá 2 zápalky.",
        "a) 3, 5, 7, 9, 11, 13: na 6 trojúhelníků je potřeba 13 zápalek.",
        "b) Pro n trojúhelníků je to 2n + 1 zápalek. Řešíme 2n + 1 = 25, tedy 2n = 24 a n = 12.",
        "Zkouška: 2 · 12 + 1 = 25. ✓"],
       tri[:3] == [3, 5, 7] and all(tri[n - 1] == 2 * n + 1 for n in range(1, 40)) and tri[5] == 13 and n25 == [12],
       figure=frames_svg([row_triangles(n) for n in (1, 2, 3)], smax=36), space=3)

barvy = ["červený", "modrý", "modrý", "žlutý"]
koraly = [barvy[i % 4] for i in range(100)]
vyroky = [koraly[49] == "modrý", koraly[:50].count("modrý") == 24, koraly[99] == "žlutý"]
T.task(1, "Korálky navlékáme na nit stále dokola v tomto pořadí: červený, modrý, modrý, žlutý, červený, modrý, modrý, žlutý a tak dále. Platí tato tvrzení?",
       "ANO, NE, ANO",
       ["Pořadí se opakuje po čtyřech korálcích: červený, modrý, modrý, žlutý.",
        "50 : 4 = 12 a zbytek 2. Po 12 úplných skupinách přijde červený a modrý korálek, 50. korálek je tedy modrý. Tvrzení platí.",
        "Ve 12 skupinách je 12 · 2 = 24 modrých, zbylé dva korálky (červený a modrý) přidají ještě jeden: celkem 25. Tvrzení neplatí.",
        "100 : 4 = 25 beze zbytku, 100. korálek je poslední ve skupině, tedy žlutý. Tvrzení platí."],
       vyroky == [True, False, True] and koraly[:50].count("modrý") == 25,
       kind="yesno", options=["50. korálek je modrý.", "Mezi prvními 50 korálky je právě 24 modrých.", "100. korálek je žlutý."], space=1)

osoby = ["Adam", "Bára", "Cyril", "Dana"]
poradi = [p for p in permutations(osoby)
          if p.index("Adam") < p.index("Bára") and p.index("Cyril") == p.index("Bára") + 1 and p.index("Dana") != 3 and p.index("Dana") > p.index("Adam")]
T.task(1, "Čtyři žáci (Adam, Bára, Cyril a Dana) běželi závod. Adam doběhl před Bárou. Cyril doběhl hned za Bárou, takže mezi nimi nikdo nedoběhl. "
          "Dana nedoběhla poslední a doběhla později než Adam. V jakém pořadí doběhli?",
       "Adam, Dana, Bára, Cyril",
       ["Adam je před Bárou a Cyril je hned za Bárou, takže pořadí těchto tří je Adam, Bára, Cyril (Adam nemusí být hned před Bárou).",
        "Dana je až po Adamovi, takže nemůže být první. Poslední také není, proto je buď druhá, nebo třetí.",
        "Kdyby Dana byla třetí, stála by mezi Bárou a Cyrilem, ale ti jdou hned za sebou. Dana je tedy druhá.",
        "Pořadí: Adam, Dana, Bára, Cyril."],
       poradi == [("Adam", "Dana", "Bára", "Cyril")], space=2)

zadano = {(0, 0): 2, (0, 2): 6, (1, 1): 5}
reseni = []
for p in permutations(range(1, 10)):
    m = [p[0:3], p[3:6], p[6:9]]
    sums = [sum(r) for r in m] + [sum(m[r][c] for r in range(3)) for c in range(3)] + [m[0][0] + m[1][1] + m[2][2], m[0][2] + m[1][1] + m[2][0]]
    if len(set(sums)) == 1 and all(m[r][c] == v for (r, c), v in zadano.items()):
        reseni.append(m)
T.task(1, "Do čtverce 3 × 3 vepište čísla 1 až 9, každé právě jednou, tak, aby byl součet čísel v každém řádku, v každém sloupci i na obou úhlopříčkách stejný. "
          "Tři čísla jsou už vepsaná. Doplňte ostatní.",
       "horní řádek 2, 7, 6; střední 9, 5, 1; dolní 4, 3, 8",
       ["Součet čísel 1 až 9 je 45 a rozdělí se do tří řádků, takže každý řádek má součet 45 : 3 = 15. Stejný součet musí mít i sloupce a úhlopříčky.",
        "Horní řádek: 2 + ? + 6 = 15, uprostřed je tedy 7. Úhlopříčky: 2 + 5 + ? = 15 dává 8 vpravo dole, 6 + 5 + ? = 15 dává 4 vlevo dole.",
        "Levý sloupec: 2 + ? + 4 = 15 dává 9. Pravý sloupec: 6 + ? + 8 = 15 dává 1. Prostřední sloupec: 7 + 5 + ? = 15 dává 3.",
        "Zkouška: střední řádek 9 + 5 + 1 = 15, dolní řádek 4 + 3 + 8 = 15. ✓"],
       reseni == [[(2, 7, 6), (9, 5, 1), (4, 3, 8)]],
       figure=magic_svg(zadano), space=1)

# ---------------------------------------------------------------- Jako u zkoušky
sch = [count(stairs(n)) for n in range(1, 30)]
prvni = min(n for n in range(1, 30) if count(stairs(n)) > 50)
T.task(2, "Schody skládáme ze čtverečků, obrázek ukazuje první čtyři obrazce. "
          "a) Kolik čtverečků má 8. obrazec? b) Kolikátý obrazec je první, který má víc než 50 čtverečků?",
       "a) 36 čtverečků; b) 10. obrazec",
       ["Počty čtverečků: 1, 3, 6, 10. Každý další obrazec přidá o jeden čtvereček víc než předchozí obrazec: nejdřív 2, pak 3, pak 4 čtverečky a tak dále.",
        "a) Pokračujeme: 15, 21, 28, 36. Osmý obrazec má 36 čtverečků (1 + 2 + 3 + … + 8).",
        "b) Devátý obrazec má 36 + 9 = 45 čtverečků, desátý 45 + 10 = 55. První obrazec přes 50 čtverečků je tedy desátý."],
       sch[:4] == [1, 3, 6, 10] and sch[7] == 36 and sch[8] == 45 and sch[9] == 55 and prvni == 10
       and all(sch[n - 1] == n * (n + 1) // 2 for n in range(1, 30)),
       figure=frames_svg([stairs(n) for n in (1, 2, 3, 4)], align="bottom"), space=3)

clenove = [3 + 4 * i for i in range(100)]
mozn = ["61", "74", "75", "80", "85"]
T.task(2, "V posloupnosti 3, 7, 11, 15, … je každý další člen o 4 větší než předchozí. Které z uvedených čísel je členem této posloupnosti?", "C",
       ["Členy jsou 3, 7, 11, 15, …, každý z nich dává po dělení čtyřmi zbytek 3 (3 = 4 · 0 + 3, 7 = 4 · 1 + 3, 11 = 4 · 2 + 3).",
        "Zbytky po dělení čtyřmi: 61 dává 1, 74 dává 2, 75 dává 3, 80 dává 0, 85 dává 1. Zbytek 3 má jen číslo 75.",
        "Zkouška: 3 + 4 · 18 = 75, číslo 75 je 19. člen. Číslo 80 je násobek čtyř (zbytek 0), čísla 61 a 85 patří do řady 1, 5, 9, … (zbytek 1)."],
       [m for m in mozn if int(m) in clenove] == ["75"] and mozn[2] == "75" and 3 + 4 * 18 == 75 and 75 % 4 == 3 and 80 % 4 == 0,
       kind="choice", options=mozn, space=2)

kr = [count(cross(n)) for n in range(1, 40)]
n81 = [n for n in range(1, 40) if count(cross(n)) == 81]
T.task(2, "Kříže skládáme ze čtverečků: uprostřed je šedý čtvereček a z každé ze čtyř stran k němu přiléhá rameno z bílých čtverečků (obrázek ukazuje první tři obrazce). "
          "a) Kolik čtverečků má 10. obrazec? b) Kolikátý obrazec se skládá z 81 čtverečků?",
       "a) 41 čtverečků; b) 20. obrazec",
       ["Počty čtverečků: 5, 9, 13. Každý další obrazec přidá čtyři čtverečky, po jednom na konec každého ramene.",
        "V n-tém obrazci je šedý čtvereček a čtyři ramena po n čtverečcích: 4n + 1. Ověříme: n = 3 dává 13. ✓",
        "a) n = 10: 4 · 10 + 1 = 41 čtverečků.", "b) Řešíme 4n + 1 = 81, tedy 4n = 80 a n = 20."],
       kr[:3] == [5, 9, 13] and all(kr[n - 1] == 4 * n + 1 for n in range(1, 40)) and kr[9] == 41 and n81 == [20],
       figure=frames_svg([cross(n) for n in (1, 2, 3)]), space=3)

jmena, krouzky = ["Jana", "Karel", "Lucie", "Martin"], ["šachy", "tanec", "florbal", "plavání"]
dobre = []
for p in permutations(krouzky):
    K = dict(zip(jmena, p))
    if (K["Jana"] not in ("tanec", "plavání") and K["Karel"] not in ("šachy", "tanec") and K["Lucie"] not in ("plavání", "florbal")
            and K["Martin"] not in ("florbal", "šachy") and any(K[d] == "tanec" for d in ("Jana", "Lucie"))):
        dobre.append(K)
T.task(2, "Jana, Karel, Lucie a Martin chodí každý do jiného z těchto kroužků: šachy, tanec, florbal a plavání. Jana nechodí na tanec ani na plavání. "
          "Karel nechodí na šachy ani na tanec. Lucie nechodí na plavání ani na florbal. Martin nechodí na florbal ani na šachy. "
          "Na tanec chodí dívka. Kdo chodí do kterého kroužku?",
       "Jana šachy, Karel florbal, Lucie tanec, Martin plavání",
       ["Martin nechodí na florbal ani na šachy, chodí tedy na tanec, nebo na plavání. Na tanec chodí dívka, takže Martin chodí na plavání.",
        "Karel může jen na florbal nebo na plavání, plavání už je obsazené, Karel chodí na florbal.",
        "Zbývají šachy a tanec pro Janu a Lucii. Jana nechodí na tanec, takže Jana chodí na šachy a Lucie na tanec.",
        "Zkouška: Jana (šachy), Karel (florbal), Lucie (tanec) i Martin (plavání) splňují všechny podmínky ze zadání. ✓"],
       dobre == [{"Jana": "šachy", "Karel": "florbal", "Lucie": "tanec", "Martin": "plavání"}], space=2)

# poctivec (T) vždy mluví pravdu, lhář (L) vždy lže; tvrzení Karla: „Aspoň jeden z nás dvou je lhář.“
mozne = [(k, l) for k, l in product("TL", repeat=2) if ((k == "T") == ("L" in (k, l)))]
T.task(2, "Na ostrově žijí poctivci, kteří vždy mluví pravdu, a lháři, kteří vždy lžou. Karel a Lucie jsou obyvatelé ostrova. "
          "Karel řekne: „Aspoň jeden z nás dvou je lhář.“ Kdo z nich je poctivec a kdo lhář?",
       "Karel je poctivec, Lucie je lhářka",
       ["Předpokládejme, že Karel je lhář. Pak je jeho věta nepravdivá, tedy nikdo z nich není lhář. To odporuje předpokladu, že Karel je lhář.",
        "Karel je tedy poctivec a jeho věta je pravdivá: aspoň jeden z nich je lhář.",
        "Karel lhář není, proto je lhářkou Lucie."],
       mozne == [("T", "L")], space=2)

cislice = [int(f"{x}{y}") for x, y in permutations([1, 2, 3, 4], 2)]
T.task(2, "Z číslic 1, 2, 3 a 4 vytváříme dvouciferná čísla, ve kterých se číslice neopakují (například 13, ale ne 22). "
          "a) Kolik takových čísel je? b) Kolik z nich je větších než 23?",
       "a) 12 čísel; b) 7 čísel",
       ["Čísla vypíšeme podle první číslice: 12, 13, 14, 21, 23, 24, 31, 32, 34, 41, 42, 43.",
        "a) Je jich 12. Kontrola: první číslici vybereme 4 způsoby, druhou už jen 3 způsoby, 4 · 3 = 12.",
        "b) Větší než 23 jsou: 24, 31, 32, 34, 41, 42, 43, to je 7 čísel."],
       len(cislice) == 12 and sorted(cislice) == [12, 13, 14, 21, 23, 24, 31, 32, 34, 41, 42, 43] and sum(c > 23 for c in cislice) == 7 and 4 * 3 == 12,
       space=3)

COLS, ROWS, PA, PB, PC = 3, 2, (0, 0), (3, 2), (1, 1)


def cesty(od, do, mimo=None):
    """Všechny cesty doprava (R) a nahoru (U) po mřížce, vypsané hrubou silou."""
    dx, dy = do[0] - od[0], do[1] - od[1]
    out = []
    for poradi in set(permutations("R" * dx + "U" * dy)):
        x, y = od
        body = [(x, y)]
        for krok in poradi:
            x, y = (x + 1, y) if krok == "R" else (x, y + 1)
            body.append((x, y))
        out.append(body)
    return out


vsechny = cesty(PA, PB)
pres_c = [p for p in vsechny if PC in p]
dp = {}
for i in range(COLS + 1):
    for j in range(ROWS + 1):
        dp[(i, j)] = 1 if i == 0 or j == 0 else dp[(i - 1, j)] + dp[(i, j - 1)]
T.task(2, "Mravenec leze po čarách mřížky z bodu A do bodu B. Smí jít jen doprava nebo nahoru, vždy o jednu úsečku. "
          "a) Kolik různých cest vede z A do B? b) Kolik z nich vede přes bod C?",
       "a) 10 cest; b) 6 cest",
       ["Do každého bodu vede tolik cest, kolik jich vede z bodu vlevo od něj a z bodu pod ním: počty sčítáme. Po dolním a levém okraji vede do každého bodu jen 1 cesta.",
        "Spodní řada zleva: 1, 1, 1, 1. Střední řada: 1, 2, 3, 4. Horní řada: 1, 3, 6, 10. Do bodu B vede 10 cest.",
        "b) Z A do C vedou 2 cesty. Z C do B musí mravenec 2krát doprava a 1krát nahoru, to jsou 3 cesty (NPP, PNP, PPN, kde P je krok doprava a N krok nahoru).",
        "Přes C vede 2 · 3 = 6 cest."],
       len(vsechny) == 10 == dp[PB] and len(pres_c) == 6 and len(cesty(PA, PC)) == 2 and len(cesty(PC, PB)) == 3,
       figure=paths_svg(COLS, ROWS, PA, PB, PC), space=3)

# ---------------------------------------------------------------- Náročnější


def vydlazdeni(radky, sloupce):
    """Počet vydláždění obdélníku dlaždicemi 1 × 2 (hrubá síla, zpětné prohledávání)."""
    volne = [[True] * sloupce for _ in range(radky)]

    def jdi():
        for r in range(radky):
            for c in range(sloupce):
                if volne[r][c]:
                    n = 0
                    if c + 1 < sloupce and volne[r][c + 1]:
                        volne[r][c] = volne[r][c + 1] = False
                        n += jdi()
                        volne[r][c] = volne[r][c + 1] = True
                    if r + 1 < radky and volne[r + 1][c]:
                        volne[r][c] = volne[r + 1][c] = False
                        n += jdi()
                        volne[r][c] = volne[r + 1][c] = True
                    return n
        return 1

    return jdi()


p = {1: 1, 2: 2}
for n in range(3, 12):
    p[n] = p[n - 1] + p[n - 2]
T.task(3, "Chodník široký 2 dlaždice a dlouhý 6 dlaždic chceme vydláždit obdélníkovými dlaždicemi 1 × 2, které můžeme klást vodorovně i svisle. "
          "Všechny dlaždice jsou stejné; dvě vydláždění jsou různá, jestliže aspoň jedna dlaždice leží jinak. Kolika způsoby lze chodník vydláždit?",
       "13 způsobů",
       ["Označíme p(n) počet vydláždění chodníku 2 × n. Pro krátké chodníky je spočítáme: p(1) = 1 (jedna svislá dlaždice), p(2) = 2 (dvě svislé, nebo dvě vodorovné nad sebou).",
        "Na začátku chodníku leží buď svislá dlaždice (zbývá chodník 2 × (n − 1)), nebo dvě vodorovné nad sebou (zbývá chodník 2 × (n − 2)). Proto p(n) = p(n − 1) + p(n − 2).",
        "p(3) = 2 + 1 = 3, p(4) = 3 + 2 = 5, p(5) = 5 + 3 = 8, p(6) = 8 + 5 = 13."],
       all(vydlazdeni(2, n) == p[n] for n in range(1, 9)) and vydlazdeni(2, 6) == 13 == p[6],
       space=4)

S = {(0, 0), (1, 1), (1, 3), (2, 0), (3, 1), (4, 3)}      # (řádek, sloupec), řádek 0 je nahoře


def uzavreni(mn, *zobrazeni):
    out = set(mn)
    for f in zobrazeni:
        out |= {f(x) for x in out}
    return out


osa_o = lambda x: (x[0], 4 - x[1])      # souměrnost podle svislé osy o
osa_p = lambda x: (4 - x[0], x[1])      # souměrnost podle vodorovné osy p
dosou = len(uzavreni(S, osa_o)) - len(S)
dvesy = len(uzavreni(S, osa_o, osa_p)) - len(S)
T.task(3, "V obrázku je vybarveno několik čtverečků. Svislá osa o a vodorovná osa p procházejí středem obrazce. "
          "a) Kolik nejméně dalších čtverečků musíme vybarvit, aby byl obrazec souměrný podle osy o? "
          "b) Kolik nejméně dalších čtverečků musíme vybarvit, aby byl obrazec souměrný podle osy o i podle osy p zároveň?",
       "a) 4 čtverečky; b) 8 čtverečků",
       ["Řádky číslujeme shora, sloupce zleva. Vybarveno je 6 čtverečků: v 1. řádku 1. sloupec, ve 2. řádku 2. a 4. sloupec, ve 3. řádku 1. sloupec, ve 4. řádku 2. sloupec a v 5. řádku 4. sloupec.",
        "a) Osa o vede 3. sloupcem: souměrně k 1. sloupci leží 5. sloupec a souměrně ke 2. sloupci 4. sloupec. Ve 2. řádku jsou čtverečky už souměrné, v řádcích 1, 3, 4 a 5 chybí vždy jeden souměrný čtvereček. Přidáme 4 čtverečky.",
        "b) Osa p vede 3. řádkem: souměrně k 1. řádku leží 5. řádek a souměrně ke 2. řádku 4. řádek. Řádky 2 a 4 jsou po úpravě podle a) stejné, 3. řádek leží na ose p. "
        "V 1. řádku jsou vybarveny sloupce 1 a 5, v 5. řádku sloupce 2 a 4, každý z těchto řádků potřebuje čtverečky druhého: přidáme 2 + 2 = 4 čtverečky.",
        "Celkem přidáme 4 + 4 = 8 čtverečků, výsledný obrazec má 14 čtverečků."],
       dosou == 4 and dvesy == 8 and len(uzavreni(S, osa_o, osa_p)) == 14 and len(uzavreni(S, osa_o)) == 10
       and all(osa_o(x) in uzavreni(S, osa_o, osa_p) and osa_p(x) in uzavreni(S, osa_o, osa_p) for x in uzavreni(S, osa_o, osa_p)),
       figure=symmetry_svg(S), space=3)

# věty na kartě: věta k říká „na kartě je právě k nepravdivých vět“
konzistentni = []
for pravda in product([True, False], repeat=4):
    nepravdivych = pravda.count(False)
    if all(pravda[k - 1] == (nepravdivych == k) for k in range(1, 5)):
        konzistentni.append(pravda)
T.task(3, "Na kartě jsou čtyři věty. 1. Na této kartě je právě jedna nepravdivá věta. 2. Na této kartě jsou právě dvě nepravdivé věty. "
          "3. Na této kartě jsou právě tři nepravdivé věty. 4. Na této kartě jsou právě čtyři nepravdivé věty. Které věty na kartě jsou pravdivé?",
       "jen třetí věta",
       ["Každá věta tvrdí jiný počet nepravdivých vět, takže dvě věty nemohou být pravdivé současně. Pravdivá je nejvýše jedna věta.",
        "Kdyby žádná věta nebyla pravdivá, byly by nepravdivé všechny čtyři. To ale říká věta 4, která by pak byla pravdivá. To je spor.",
        "Pravdivá je tedy právě jedna věta a nepravdivé jsou tři. To tvrdí věta 3, a ta je pravdivá.",
        "Zkouška: nepravdivé jsou věty 1, 2 a 4, tedy právě tři věty, a to věta 3 správně tvrdí. ✓"],
       konzistentni == [(False, False, True, False)],
       space=3)

site = [count(net(n)) for n in range(1, 30)]
nej = max(n for n in range(1, 30) if count(net(n)) <= 100)
T.task(3, "Čtvercovou síť n × n skládáme ze zápalek, obrázek ukazuje první tři obrazce (1 × 1, 2 × 2 a 3 × 3 čtverce). "
          "a) Kolik zápalek potřebujeme na síť 9 × 9 čtverců? "
          "b) Ze 100 zápalek chceme postavit co největší čtvercovou síť. Kolik čtverců bude mít na straně a kolik zápalek zbude?",
       "a) 180 zápalek; b) 6 × 6 čtverců, zbude 16 zápalek",
       ["Počty zápalek: 4, 12, 24. Síť n × n má (n + 1) vodorovných řad po n zápalkách a stejně tolik svislých řad: celkem 2 · n · (n + 1) zápalek.",
        "Ověříme: n = 2 dává 2 · 2 · 3 = 12 a n = 3 dává 2 · 3 · 4 = 24. ✓",
        "a) n = 9: 2 · 9 · 10 = 180 zápalek.",
        "b) n = 6 dává 2 · 6 · 7 = 84 zápalek, n = 7 dává 2 · 7 · 8 = 112, a to je víc než 100. Největší je síť 6 × 6, zbude 100 − 84 = 16 zápalek."],
       site[:3] == [4, 12, 24] and all(site[n - 1] == 2 * n * (n + 1) for n in range(1, 30)) and site[8] == 180 and nej == 6 and 100 - site[5] == 16,
       figure=frames_svg([net(n) for n in (1, 2, 3)], align="bottom"), space=3)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
q = [5 * n - 2 for n in range(1, 101)]
T.diagnostic("V posloupnosti 3, 8, 13, 18, … je každý další člen o stejné číslo větší než předchozí. Určete 25. člen a rozhodněte, zda je číslo 98 členem této posloupnosti.",
             "25. člen je 123; číslo 98 je členem (20. člen)",
             ["Sousední členy se liší o 5, člen na n-tém místě je 5n − 2 (3 = 5 · 1 − 2, 8 = 5 · 2 − 2).",
              "25. člen: 5 · 25 − 2 = 123.", "Řešíme 5n − 2 = 98, tedy 5n = 100 a n = 20. Číslo 98 je 20. člen."],
             q[:4] == [3, 8, 13, 18] and q[24] == 123 and q[19] == 98 and 98 in q)

dnes = date(2026, 9, 30)   # středa
assert dnes.weekday() == 2
za100 = dnes + timedelta(days=100)
dny = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]
opts = ["úterý", "čtvrtek", "pátek", "sobota", "neděle"]
T.diagnostic("Dnes je středa. Jaký den v týdnu bude za 100 dní?", "C",
             ["Dny v týdnu se opakují po 7 dnech. 100 : 7 = 14 a zbytek 2.", "Po 14 celých týdnech je zase středa, ještě 2 dny navíc: čtvrtek, pátek.",
              "Za 100 dní bude pátek. Čtvrtek vyjde, když žák přičte jen 1 zbylý den místo dvou."],
             dny[za100.weekday()] == "pátek" and opts[2] == "pátek" and 100 % 7 == 2,
             kind="choice", options=opts)

T.save()
