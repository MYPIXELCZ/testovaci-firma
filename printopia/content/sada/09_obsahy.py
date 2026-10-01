#!/usr/bin/env python3
"""Téma 9: Obvody, obsahy, kruh a Pythagorova věta (formát v _lib.py, vzor 01_zlomky.py). Úlohy jsou vlastní, ve stylu jednotné
přijímací zkoušky.

Obrázky se kreslí z rozměrů v cm (nebo dm) a při sestavení se z nich zpětně přepočítají délky a obsahy (assert), takže obrázek
odpovídá zadání. Měřítko: 4 jednotky = 1 mm při tisku (obrázek se vejde do 62 × 42 mm = 248 × 168 jednotek)."""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, dec  # noqa: E402

PI = F(314, 100)   # π ≈ 3,14
PI7 = F(22, 7)     # π ≈ 22/7


def iroot(n):
    """Celá druhá odmocnina; úloha musí vycházet přesně."""
    r = math.isqrt(n)
    assert r * r == n, f"{n} není druhá mocnina"
    return r


# ------------------------------------------------------------------ pomůcky pro obrázky
INK = "#1c2230"
SHADE = "#e3e9f7"


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def same(a, b, tol=1e-6):
    return abs(a - b) < tol


def shoelace(*pts):
    """Obsah mnohoúhelníku ze souřadnic (Gaussův vzorec)."""
    s = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return abs(s) / 2


def pol(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


class Fig:
    """Obrázek v matematických souřadnicích (osa y nahoru); 4 jednotky = 1 mm."""

    def __init__(self, w, h):
        assert w <= 248 and h <= 168, "obrázek se nevejde do 62 × 42 mm"
        self.w, self.h, self.el = w, h, []

    def _xy(self, p):
        return f"{p[0]:.2f}", f"{self.h - p[1]:.2f}"

    def line(self, p, q, w=1.6, dash=False):
        (x1, y1), (x2, y2) = self._xy(p), self._xy(q)
        d = ' stroke-dasharray="5 4"' if dash else ""
        self.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"{d}/>')

    def poly(self, pts, fill="none", w=1.6):
        s = " ".join(",".join(self._xy(p)) for p in pts)
        self.el.append(f'<polygon points="{s}" fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>')

    def polyline(self, pts, w=1.2):
        s = " ".join(",".join(self._xy(p)) for p in pts)
        self.el.append(f'<polyline points="{s}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')

    def circle(self, c, r, fill="none", w=1.6):
        x, y = self._xy(c)
        self.el.append(f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="{fill}" stroke="{INK}" stroke-width="{w}"/>')

    def path(self, cmds, fill="none", w=1.6):
        """cmds: ("M", p), ("L", p), ("A", r, p) = oblouk proti směru hodin do bodu p (menší než půlkruh nebo půlkruh), ("Z",)."""
        d = []
        for c in cmds:
            if c[0] in "ML":
                d.append(f"{c[0]} {self._xy(c[1])[0]} {self._xy(c[1])[1]}")
            elif c[0] == "A":
                d.append(f"A {c[1]:.2f} {c[1]:.2f} 0 0 0 {self._xy(c[2])[0]} {self._xy(c[2])[1]}")
            else:
                d.append("Z")
        self.el.append(f'<path d="{" ".join(d)}" fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>')

    def text(self, p, s, size=13, anchor="middle"):
        x, y = self._xy(p)
        self.el.append(f'<text x="{x}" y="{y}" dy=".35em" text-anchor="{anchor}" font-family="Inter,Arial" font-size="{size}" fill="{INK}" stroke="none">{s}</text>')

    def vlabel(self, p, s, center, d=11, size=14):
        """Popisek vrcholu mimo obrazec (ve směru od středu)."""
        dx, dy = p[0] - center[0], p[1] - center[1]
        n = math.hypot(dx, dy) or 1
        self.text((p[0] + d * dx / n, p[1] + d * dy / n), s, size=size)

    def elabel(self, p, q, s, center, d=20, size=13):
        """Popisek délky u úsečky PQ, posunutý kolmo ven (od středu obrazce)."""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        nx, ny = -(q[1] - p[1]), q[0] - p[0]
        if (mx - center[0]) * nx + (my - center[1]) * ny < 0:
            nx, ny = -nx, -ny
        n = math.hypot(nx, ny)
        self.text((mx + d * nx / n, my + d * ny / n), s, size=size)

    def right(self, v, a1, a2, s=8):
        """Značka pravého úhlu u vrcholu v mezi směry a1 a a2 (stupně)."""
        p1, p2 = pol(v, s, a1), pol(v, s, a2)
        self.polyline([p1, (p1[0] + p2[0] - v[0], p1[1] + p2[1] - v[1]), p2])

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w / 4:g}mm" height="{self.h / 4:g}mm">'
                + "".join(self.el) + "</svg>")


# ------------------------------------------------------------------ obrázky k úlohám (rozměry v cm, k = jednotek na cm)
def obr_pythagoras():
    """Pravoúhlý trojúhelník, pravý úhel při C, AC = 9 cm, BC = 12 cm, AB = 15 cm."""
    k = 11
    f = Fig(208, 150)
    pt = lambda x, y: (52 + k * x, 24 + k * y)  # noqa: E731
    C, B, A = pt(0, 0), pt(12, 0), pt(0, 9)
    assert same(dist(A, C) / k, 9) and same(dist(B, C) / k, 12) and same(dist(A, B) / k, 15) and same(shoelace(A, B, C) / k ** 2, 54)
    f.poly([A, B, C], fill=SHADE)
    f.right(C, 0, 90, 9)
    f.elabel(A, C, "9 cm", B, d=22)
    f.elabel(C, B, "12 cm", A, d=12)
    ctr = (C[0] + 4 * k, C[1] + 3 * k)
    f.vlabel(A, "A", ctr, d=11)
    f.vlabel(B, "B", ctr, d=11)
    f.vlabel(C, "C", ctr, d=11)
    return f.svg(), {"AC": dist(A, C) / k, "BC": dist(B, C) / k, "AB": dist(A, B) / k}


def obr_rovnobeznik():
    """Rovnoběžník ABCD: AB = 15 cm, AD = 13 cm, výška na AB 12 cm (pata výšky 5 cm od A)."""
    k = 9
    f = Fig(228, 150)
    pt = lambda x, y: (24 + k * x, 20 + k * y)  # noqa: E731
    A, B, C, D, H = pt(0, 0), pt(15, 0), pt(20, 12), pt(5, 12), pt(5, 0)
    assert same(dist(A, B) / k, 15) and same(dist(A, D) / k, 13) and same(dist(B, C) / k, 13) and same(dist(D, H) / k, 12)
    assert same(shoelace(A, B, C, D) / k ** 2, 180)
    f.poly([A, B, C, D], fill=SHADE)
    f.line(D, H, dash=True, w=1.4)
    f.right(H, 0, 90, 8)
    ctr = (A[0] + 10 * k, A[1] + 6 * k)
    f.elabel(A, B, "15 cm", ctr, d=11)
    f.elabel(A, D, "13 cm", ctr, d=22)
    f.text((H[0] + 25, H[1] + 6 * k), "12 cm")
    for P, s in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        f.vlabel(P, s, ctr, d=11)
    return f.svg(), {"AB": dist(A, B) / k, "AD": dist(A, D) / k, "v": dist(D, H) / k, "S": shoelace(A, B, C, D) / k ** 2}


def obr_lichobeznik():
    """Rovnoramenný lichoběžník ABCD: AB = 22 cm, CD = 10 cm, ramena 10 cm, výška 8 cm."""
    k = 8
    f = Fig(228, 114)
    pt = lambda x, y: (26 + k * x, 22 + k * y)  # noqa: E731
    A, B, C, D, H = pt(0, 0), pt(22, 0), pt(16, 8), pt(6, 8), pt(6, 0)
    assert same(dist(A, B) / k, 22) and same(dist(C, D) / k, 10) and same(dist(A, D) / k, 10) and same(dist(B, C) / k, 10)
    assert same(dist(D, H) / k, 8) and same(shoelace(A, B, C, D) / k ** 2, 128)
    f.poly([A, B, C, D], fill=SHADE)
    f.line(D, H, dash=True, w=1.4)
    f.right(H, 0, 90, 8)
    ctr = (A[0] + 11 * k, A[1] + 4 * k)
    f.elabel(A, B, "22 cm", ctr, d=11)
    f.elabel(C, D, "10 cm", ctr, d=11)
    f.elabel(A, D, "10 cm", ctr, d=22)
    f.elabel(B, C, "10 cm", ctr, d=22)
    f.text((H[0] + 9, H[1] + 4 * k), "v")
    for P, s in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        f.vlabel(P, s, ctr, d=10)
    return f.svg(), {"AB": 22, "CD": dist(C, D) / k, "AD": dist(A, D) / k, "v": dist(D, H) / k, "S": shoelace(A, B, C, D) / k ** 2}


def obr_rovnoramenny():
    """Rovnoramenný trojúhelník ABC: AB = 10 cm, AC = BC = 13 cm, výška 12 cm."""
    k = 9
    f = Fig(172, 150)
    pt = lambda x, y: (40 + k * x, 20 + k * y)  # noqa: E731
    A, B, C, H = pt(0, 0), pt(10, 0), pt(5, 12), pt(5, 0)
    assert same(dist(A, B) / k, 10) and same(dist(A, C) / k, 13) and same(dist(B, C) / k, 13) and same(dist(C, H) / k, 12)
    f.poly([A, B, C], fill=SHADE)
    f.line(C, H, dash=True, w=1.4)
    f.right(H, 0, 90, 8)
    ctr = (A[0] + 5 * k, A[1] + 4 * k)
    f.elabel(A, B, "10 cm", ctr, d=11)
    f.elabel(A, C, "13 cm", ctr, d=22)
    f.elabel(B, C, "13 cm", ctr, d=22)
    f.text((H[0] + 9, H[1] + 5 * k), "v")
    f.vlabel(A, "A", ctr, d=10)
    f.vlabel(B, "B", ctr, d=10)
    f.vlabel(C, "C", ctr, d=10)
    return f.svg(), {"AB": dist(A, B) / k, "AC": dist(A, C) / k, "v": dist(C, H) / k, "S": shoelace(A, B, C) / k ** 2}


def obr_ctvrtkruh():
    """Čtvrtkruh s poloměrem 14 cm (střed O, krajní body A, B)."""
    k = 8
    f = Fig(182, 144)
    O = (52, 22)
    r = 14 * k
    A, B = (O[0] + r, O[1]), (O[0], O[1] + r)
    assert same(dist(O, A) / k, 14) and same(dist(O, B) / k, 14)
    f.path([("M", O), ("L", A), ("A", r, B), ("Z",)], fill=SHADE)
    f.right(O, 0, 90, 9)
    f.text(((O[0] + A[0]) / 2, O[1] - 12), "14 cm")
    f.text((O[0] - 22, (O[1] + B[1]) / 2), "14 cm")
    f.text((O[0] - 8, O[1] - 10), "O", size=13)
    return f.svg(), {"r": dist(O, A) / k}


def obr_slozeny():
    """Obrazec tvaru L: obdélník 12 × 9 cm bez rohu 5 × 3 cm vpravo nahoře; v obrázku jsou čtyři rozměry (12, 9, 7, 3)."""
    k = 14
    f = Fig(226, 166)
    pt = lambda x, y: (44 + k * x, 20 + k * y)  # noqa: E731
    cm = [(0, 0), (12, 0), (12, 6), (7, 6), (7, 9), (0, 9)]
    P = [pt(*c) for c in cm]
    hrany = [dist(P[i], P[(i + 1) % 6]) / k for i in range(6)]
    assert [round(h, 6) for h in hrany] == [12, 6, 5, 3, 7, 9]
    assert same(shoelace(*P) / k ** 2, 93) and same(sum(hrany), 42)
    f.poly(P, fill=SHADE)
    f.text((pt(6, 0)[0], 9), "12 cm")
    f.text((44 - 22, pt(0, 4.5)[1]), "9 cm")
    f.text((pt(3.5, 9)[0], pt(0, 9)[1] + 11), "7 cm")
    f.text((pt(7, 7.5)[0] + 21, pt(7, 7.5)[1]), "3 cm")
    return f.svg(), {"hrany": hrany, "S": shoelace(*P) / k ** 2, "dano": (12, 9, 7, 3)}


def obr_okno():
    """Okno: obdélník 14 × 10 dm zakončený půlkruhem o průměru 14 dm."""
    k = 8
    f = Fig(172, 162)
    pt = lambda x, y: (44 + k * x, 20 + k * y)  # noqa: E731
    L, Rr, TL, TR = pt(0, 0), pt(14, 0), pt(0, 10), pt(14, 10)
    r = 7 * k
    assert same(dist(L, Rr) / k, 14) and same(dist(L, TL) / k, 10) and same(dist(TL, TR) / 2, r)
    f.path([("M", L), ("L", Rr), ("L", TR), ("A", r, TL), ("Z",)], fill=SHADE)
    f.line(TL, TR, dash=True, w=1.2)
    f.text((pt(7, 0)[0], 9), "14 dm")
    f.text((44 - 22, pt(0, 5)[1]), "10 dm")
    return f.svg(), {"sirka": dist(L, Rr) / k, "vyska": dist(L, TL) / k, "r": r / k}


def obr_ctverec_kruh():
    """Čtverec o straně 10 cm s vepsaným kruhem (r = 5 cm); vybarvené jsou rohy."""
    k = 14
    f = Fig(178, 168)
    pt = lambda x, y: (26 + k * x, 22 + k * y)  # noqa: E731
    A, B, C, D, S = pt(0, 0), pt(10, 0), pt(10, 10), pt(0, 10), pt(5, 5)
    r = 5 * k
    assert same(dist(A, B) / k, 10) and same(S[0] - A[0], r) and same(B[0] - S[0], r) and same(S[1] - A[1], r) and same(D[1] - S[1], r)
    f.poly([A, B, C, D], fill="#b9c4de")
    f.circle(S, r, fill="#ffffff")
    f.text((pt(5, 0)[0], 10), "10 cm")
    return f.svg(), {"a": dist(A, B) / k, "r": r / k}


# ------------------------------------------------------------------ téma
T = Topic(9, "obsahy", "Obvody, obsahy, kruh a Pythagorova věta",
          "Obvody a obsahy se v testu objevují každý rok, často ve složeném obrazci nebo spolu s kruhem. Pythagorova věta se většinou skrývá uvnitř jiné úlohy: "
          "jako úhlopříčka obdélníku, výška rovnoramenného trojúhelníku nebo výška lichoběžníku.",
          ["Obvod je délka čáry kolem obrazce (v cm, m), obsah je velikost plochy uvnitř (v cm², m²). Před počítáním si podtrhněte, co zadání žádá a v jakých jednotkách.",
           "Vzorce: čtverec S = a², obdélník S = a · b, rovnoběžník S = a · v, trojúhelník S = a · v : 2, lichoběžník S = (a + c) · v : 2. "
           "Výška je kolmá k základně, často není stranou obrazce a do obvodu nepatří.",
           "Kruh: o = 2 · π · r, S = π · r². Pozor na záměnu poloměru a průměru. Za π dosazujte hodnotu uvedenou v zadání (3,14 nebo 22/7; zlomek se hodí, když je poloměr násobkem sedmi). "
           "Výseč je část kruhu (například čtvrtina nebo třetina), mezikruží je rozdíl dvou kruhů: S = π · (R² − r²), ne π · (R − r)².",
           "Pythagorova věta: v pravoúhlém trojúhelníku platí c² = a² + b², kde c je přepona (leží proti pravému úhlu). Odvěsnu spočtete odečtením: "
           "a² = c² − b². Hodí se znát trojice 3, 4, 5; 5, 12, 13; 8, 15, 17; 7, 24, 25 a jejich násobky (například 6, 8, 10).",
           "Převody obsahu: 1 m² = 10 000 cm², 1 a (ar) = 100 m², 1 ha = 10 000 m². Typická chyba: násobit nebo dělit číslem 100 místo 10 000.",
           "Složený obrazec rozdělte na jednoduché části, nebo od většího obrazce odečtěte vyříznutou část. "
           "Do obvodu patří jen vnější čára obrazce, společné hranice částí se nepočítají."])

# ---------------------------------------------------------------- Řešený příklad
b = F(68, 2) - 24
u = iroot(24 ** 2 + 10 ** 2)
T.example("Obdélníkový pozemek má obvod 68 m a jednu stranu dlouhou 24 m. Vypočtěte jeho obsah a délku úhlopříčky.",
          ["Polovina obvodu je 68 : 2 = 34 m, druhá strana je tedy 34 − 24 = 10 m.",
           "Obsah: S = 24 · 10 = 240 m².",
           "Úhlopříčka u je přepona pravoúhlého trojúhelníku s odvěsnami 24 m a 10 m: u² = 24² + 10² = 576 + 100 = 676.",
           "u = √676 = 26 m (dvojnásobek trojice 5, 12, 13)."],
          "S = 240 m², u = 26 m",
          b == 10 and 2 * (24 + b) == 68 and 24 * b == 240 and u == 26 and 26 ** 2 == 676 and (10, 24, 26) == (2 * 5, 2 * 12, 2 * 13))

# ---------------------------------------------------------------- Základ
a = F(36, 4)
T.task(1, "Čtverec má obvod 36 cm. Vypočtěte jeho obsah.", "81 cm²",
       ["Čtverec má čtyři stejné strany: a = 36 : 4 = 9 cm.", "Obsah: S = a² = 9² = 81 cm²."],
       a == 9 and a * a == 81, space=2)

svg, g = obr_pythagoras()
c = iroot(9 ** 2 + 12 ** 2)
T.task(1, "Pravoúhlý trojúhelník ABC má pravý úhel při vrcholu C a odvěsny AC = 9 cm a BC = 12 cm. Vypočtěte délku přepony AB "
          "a obvod trojúhelníku.", "AB = 15 cm, obvod 36 cm",
       ["Pythagorova věta: c² = 9² + 12² = 81 + 144 = 225.", "c = √225 = 15 cm (trojnásobek trojice 3, 4, 5).",
        "Obvod: 9 + 12 + 15 = 36 cm."],
       same(g["AC"], 9) and same(g["BC"], 12) and same(g["AB"], c) and c == 15 and 9 + 12 + c == 36 and (9, 12, 15) == (3 * 3, 4 * 3, 5 * 3),
       figure=svg, space=2)

T.task(1, "Převeďte: a) 3,5 m² na cm², b) 2 400 m² na hektary, c) 45 000 cm² na m².", "a) 35 000 cm², b) 0,24 ha, c) 4,5 m²",
       ["1 m² = 100 · 100 = 10 000 cm², 1 ha = 10 000 m².", "a) 3,5 · 10 000 = 35 000 cm².", "b) 2 400 : 10 000 = 0,24 ha.",
        "c) 45 000 : 10 000 = 4,5 m²."],
       100 * 100 == 10000 and F(7, 2) * 10000 == 35000 and F(2400, 10000) == F(24, 100) and F(45000, 10000) == F(9, 2), space=2)

r = 20 / 2
o_, S_ = 2 * PI * 10, PI * 10 ** 2
T.task(1, "Kruh má průměr 20 cm. Vypočtěte jeho obvod a obsah (použijte π ≈ 3,14).", f"o = {dec(o_)} cm, S = {dec(S_)} cm²",
       ["Poloměr je poloviční než průměr: r = 20 : 2 = 10 cm.", "Obvod: o = 2 · π · r = 2 · 3,14 · 10 = 62,8 cm.",
        "Obsah: S = π · r² = 3,14 · 10² = 3,14 · 100 = 314 cm²."],
       r == 10 and o_ == F(628, 10) and S_ == 314, space=3)

svg, g = obr_rovnobeznik()
T.task(1, "Rovnoběžník ABCD má strany AB = 15 cm a AD = 13 cm. Výška na stranu AB je 12 cm (viz obrázek). Vypočtěte obsah a obvod "
          "rovnoběžníku.", "S = 180 cm², o = 56 cm",
       ["Obsah rovnoběžníku: S = a · v = 15 · 12 = 180 cm².", "Obvod: o = 2 · (15 + 13) = 56 cm.",
        "Pozor: výška 12 cm není stranou rovnoběžníku, do obvodu nepatří."],
       same(g["AB"], 15) and same(g["AD"], 13) and same(g["v"], 12) and same(g["S"], 15 * 12) and 15 * 12 == 180 and 2 * (15 + 13) == 56
       and iroot(13 ** 2 - 12 ** 2) == 5, figure=svg, space=2)

# ---------------------------------------------------------------- Jako u zkoušky
opts = ["2krát", "3krát", "4krát", "6krát", "8krát"]
pomery = {F((2 * a_) ** 2, a_ ** 2) for a_ in (1, 3, 7)}
T.task(2, "Strana čtverce se zdvojnásobí. Kolikrát se zvětší jeho obsah?", "C (4krát)",
       ["Původní strana a, původní obsah a². Nová strana 2a, nový obsah (2a)² = 4a².",
        "Ověření na čísle: a = 3 cm má obsah 9 cm², strana 6 cm má obsah 36 cm², 36 : 9 = 4.",
        "Zdvojnásobí se obvod, ale obsah se zvětší čtyřikrát. Chyby: 2krát je změna obvodu, 8krát by byl objem krychle."],
       pomery == {4} and opts[2] == "4krát" and opts.count("4krát") == 1 and 2 ** 3 == 8, kind="choice", options=opts, space=1)

svg, g = obr_lichobeznik()
x = (22 - 10) // 2
v = iroot(10 ** 2 - x ** 2)
S_ = F((22 + 10) * v, 2)
T.task(2, "Rovnoramenný lichoběžník ABCD má základny AB = 22 cm a CD = 10 cm a ramena AD = BC = 10 cm. Vypočtěte jeho výšku a obsah.",
       "v = 8 cm, S = 128 cm²",
       ["Výšky z vrcholů C a D rozdělí lichoběžník na obdélník a dva shodné pravoúhlé trojúhelníky. Kratší odvěsna každého z nich je (22 − 10) : 2 = 6 cm.",
        "Rameno je přepona: v² = 10² − 6² = 100 − 36 = 64, v = 8 cm (trojice 6, 8, 10).",
        "Obsah: S = (a + c) · v : 2 = (22 + 10) · 8 : 2 = 128 cm²."],
       x == 6 and v == 8 and S_ == 128 and same(g["v"], v) and same(g["S"], S_) and same(g["AD"], 10) and same(g["CD"], 10),
       figure=svg, space=3)

svg, g = obr_rovnoramenny()
polovina = 10 // 2
v = iroot(13 ** 2 - polovina ** 2)
S_ = F(10 * v, 2)
T.task(2, "Rovnoramenný trojúhelník ABC má základnu AB = 10 cm a ramena AC = BC = 13 cm. Vypočtěte jeho výšku na základnu a obsah. "
          "Uveďte celý postup.", "v = 12 cm, S = 60 cm²",
       ["Výška na základnu ji půlí: polovina základny je 10 : 2 = 5 cm.",
        "Pythagorova věta v pravoúhlém trojúhelníku s přeponou 13 cm: v² = 13² − 5² = 169 − 25 = 144, v = 12 cm.",
        "Obsah: S = a · v : 2 = 10 · 12 : 2 = 60 cm²."],
       polovina == 5 and v == 12 and S_ == 60 and same(g["v"], v) and same(g["S"], S_) and same(g["AC"], 13), figure=svg, space=4)

S_ = PI * (10 ** 2 - 5 ** 2)
T.task(2, "Mezikruží je omezené dvěma soustřednými kružnicemi o poloměrech 10 cm a 5 cm. Vypočtěte jeho obsah (použijte π ≈ 3,14). "
          "Uveďte celý postup.", f"{dec(S_)} cm²",
       ["Obsah velkého kruhu: S₁ = π · 10² = 3,14 · 100 = 314 cm².", "Obsah malého kruhu: S₂ = π · 5² = 3,14 · 25 = 78,5 cm².",
        "Mezikruží: 314 − 78,5 = 235,5 cm². Stejně: π · (10² − 5²) = 3,14 · 75 = 235,5 cm².",
        "Pozor: výpočet π · (10 − 5)² dává 78,5 cm², což je chybný výsledek (to je obsah malého kruhu)."],
       S_ == F(2355, 10) and PI * 100 - PI * 25 == S_ and PI * (10 - 5) ** 2 == F(785, 10) != S_, space=4)

svg, g = obr_ctvrtkruh()
S_ = PI7 * 14 ** 2 / 4
oblouk = 2 * PI7 * 14 / 4
o_ = 14 + 14 + oblouk
T.task(2, "Obrazec má tvar čtvrtiny kruhu o poloměru 14 cm (viz obrázek). Vypočtěte jeho obsah a obvod (použijte π ≈ 22/7).",
       f"S = {dec(S_)} cm², o = {dec(o_)} cm",
       ["Celý kruh: S = π · r² = 22/7 · 14² = 22/7 · 196 = 616 cm². Čtvrtina: 616 : 4 = 154 cm².",
        "Oblouk je čtvrtina obvodu kruhu: 2 · 22/7 · 14 = 88 cm, 88 : 4 = 22 cm.",
        "Obvod obrazce tvoří oblouk a dva poloměry: 22 + 14 + 14 = 50 cm."],
       same(g["r"], 14) and PI7 * 14 ** 2 == 616 and S_ == 154 and oblouk == 22 and o_ == 50, figure=svg, space=3)

# 1) všechny obdélníky s obvodem 24 cm (strany a, 12 − a) mají obsah 35 cm²? ne, 6 × 6 má 36 cm²
st = [all(a_ * (12 - a_) == 35 for a_ in range(1, 12)), 6 ** 2 + 8 ** 2 == 10 ** 2, F(1, 2) * 10000 == 5000]
T.task(2, "Platí tato tvrzení?", "NE, ANO, ANO",
       ["Obvod 24 cm má například obdélník 5 × 7 (obsah 35 cm²), ale i čtverec 6 × 6 (obsah 36 cm²) nebo obdélník 4 × 8 (obsah 32 cm²). "
        "Tvrzení neplatí.",
        "6² + 8² = 36 + 64 = 100 = 10². Podle obrácené Pythagorovy věty je trojúhelník pravoúhlý. Platí.",
        "1 m² = 10 000 cm², takže 0,5 m² = 0,5 · 10 000 = 5 000 cm². Platí."],
       st == [False, True, True] and 2 * (5 + 7) == 24 and 5 * 7 == 35 and 6 * 6 == 36 and 4 * 8 == 32, kind="yesno",
       options=["Každý obdélník s obvodem 24 cm má obsah 35 cm².", "Trojúhelník o stranách 6 cm, 8 cm a 10 cm je pravoúhlý.",
                "Obsah 0,5 m² je 5 000 cm²."], space=1)

c = iroot(600 ** 2 + 800 ** 2)
plot = 600 + 800 + c
S_ = F(600 * 800, 2)
T.task(2, "Pole má tvar pravoúhlého trojúhelníku s odvěsnami 600 m a 800 m. Vypočtěte a) délku plotu kolem celého pole, "
          "b) obsah pole v hektarech.", "a) 2 400 m, b) 24 ha",
       ["Přepona: c² = 600² + 800² = 360 000 + 640 000 = 1 000 000, c = 1 000 m (200násobek trojice 3, 4, 5).",
        "Plot: 600 + 800 + 1 000 = 2 400 m.", "Obsah: S = 600 · 800 : 2 = 240 000 m².",
        "1 ha = 10 000 m², tedy 240 000 m² = 24 ha."],
       c == 1000 and plot == 2400 and S_ == 240000 and S_ / 10000 == 24 and (600, 800, 1000) == (3 * 200, 4 * 200, 5 * 200), space=4)

# ---------------------------------------------------------------- Náročnější
svg, g = obr_slozeny()
hrany = g["hrany"]
obvod = sum(round(h) for h in hrany)
obsah = 12 * 9 - 5 * 3
T.task(3, "Sousední strany obrazce na obrázku jsou na sebe kolmé, rozměry jsou v centimetrech. Vypočtěte jeho obvod a obsah.",
       "o = 42 cm, S = 93 cm²",
       ["Chybějící strany: pravá svislá strana má 9 − 3 = 6 cm, vodorovná strana v zářezu má 12 − 7 = 5 cm.",
        "Obvod: 12 + 6 + 5 + 3 + 7 + 9 = 42 cm (stejně jako obvod obdélníku 12 × 9).",
        "Obsah: obdélník 12 · 9 = 108 cm² bez zářezu 5 · 3 = 15 cm² je 93 cm².",
        "Jinak: dolní obdélník 12 · 6 = 72 cm² a horní obdélník 7 · 3 = 21 cm², dohromady 93 cm²."],
       obvod == 42 == 2 * (12 + 9) and obsah == 93 and same(g["S"], 93) and 12 * 6 + 7 * 3 == 93 and 9 - 3 == 6 and 12 - 7 == 5
       and g["dano"] == (12, 9, 7, 3), figure=svg, space=3)

svg, g = obr_okno()
S_ = 14 * 10 + PI7 * 7 ** 2 / 2
o_ = 10 + 10 + 14 + PI7 * 7
T.task(3, "Okno má tvar obdélníku zakončeného nahoře půlkruhem (viz obrázek). Šířka okna je 14 dm, výška obdélníkové části je 10 dm "
          "a průměr půlkruhu je roven šířce okna. Vypočtěte obsah okna a délku jeho obvodu (použijte π ≈ 22/7).",
       f"S = {dec(S_)} dm², o = {dec(o_)} dm",
       ["Obdélníková část: 14 · 10 = 140 dm².",
        "Půlkruh má poloměr 14 : 2 = 7 dm, jeho obsah je 22/7 · 7² : 2 = 22 · 7 : 2 = 77 dm².",
        "Obsah okna: 140 + 77 = 217 dm².",
        "Obvod: dvě svislé strany 2 · 10 = 20 dm, spodní strana 14 dm a oblouk půlkruhu 22/7 · 7 = 22 dm, dohromady 56 dm. "
        "Horní strana obdélníku do obvodu nepatří."],
       same(g["sirka"], 14) and same(g["vyska"], 10) and same(g["r"], 7) and PI7 * 49 / 2 == 77 and S_ == 217 and PI7 * 7 == 22 and o_ == 56,
       figure=svg, space=3)

svg, g = obr_ctverec_kruh()
S_ = F(10 ** 2) - PI * 5 ** 2
T.task(3, "Do čtverce o straně 10 cm je vepsán kruh, který se dotýká všech čtyř stran. Vypočtěte obsah vybarvené části obrázku "
          "(použijte π ≈ 3,14).", f"{dec(S_)} cm²",
       ["Průměr kruhu je roven straně čtverce, d = 10 cm, takže r = 5 cm.", "Obsah kruhu: π · r² = 3,14 · 25 = 78,5 cm².",
        "Obsah čtverce: 10 · 10 = 100 cm².", "Vybarvená část: 100 − 78,5 = 21,5 cm²."],
       same(g["a"], 10) and same(g["r"], 5) and PI * 25 == F(785, 10) and S_ == F(215, 10), figure=svg, space=3)

rameno = F(50 - 16, 2)
v = iroot(17 ** 2 - 8 ** 2)
S_ = F(16 * v, 2)
T.task(3, "Rovnoramenný trojúhelník má obvod 50 cm a základnu 16 cm. Vypočtěte jeho obsah. Uveďte celý postup.", "120 cm²",
       ["Ramena: (50 − 16) : 2 = 17 cm.",
        "Výška na základnu ji půlí, polovina základny je 8 cm: v² = 17² − 8² = 289 − 64 = 225, v = 15 cm (trojice 8, 15, 17).",
        "Obsah: S = 16 · 15 : 2 = 120 cm²."],
       rameno == 17 and 16 + 2 * rameno == 50 and v == 15 and S_ == 120 and 8 ** 2 + 15 ** 2 == 17 ** 2, space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
bc = iroot(25 ** 2 - 7 ** 2)
T.diagnostic("Obdélník ABCD má stranu AB = 7 cm a úhlopříčku AC = 25 cm. Vypočtěte jeho obsah.", "168 cm²",
             ["Trojúhelník ABC je pravoúhlý s pravým úhlem při vrcholu B a přeponou AC.",
              "BC² = 25² − 7² = 625 − 49 = 576, BC = 24 cm (trojice 7, 24, 25).", "Obsah: S = 7 · 24 = 168 cm²."],
             bc == 24 and 7 * bc == 168)

opts = ["31,4 cm²", "100 cm²", "314 cm²", "628 cm²", "1 256 cm²"]
r = F(628, 10) / (2 * PI)
S_ = PI * r ** 2
T.diagnostic("Obvod kruhu je 62,8 cm. Jaký je obsah kruhu (použijte π ≈ 3,14)?", "C (314 cm²)",
             ["Z obvodu o = 2 · π · r vyjde r = 62,8 : (2 · 3,14) = 62,8 : 6,28 = 10 cm.", "Obsah: S = π · r² = 3,14 · 10² = 314 cm².",
              "Chybné možnosti vznikly takto: 31,4 cm² je π · r, 100 cm² je r², 628 cm² je 2 · π · r² a 1 256 cm² je π · d² (průměr místo poloměru)."],
             r == 10 and S_ == 314 and opts[2] == "314 cm²" and PI * r == F(314, 10) and PI * (2 * r) ** 2 == 1256 and 2 * PI * r ** 2 == 628,
             kind="choice", options=opts)

T.save()
