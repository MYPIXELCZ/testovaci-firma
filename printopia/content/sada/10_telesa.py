#!/usr/bin/env python3
"""Téma 10: Tělesa: objem a povrch. Obrázky (SVG) se kreslí ze stejných čísel, ze kterých se počítají výsledky, a objem
i povrch se navíc ověřují nezávisle (součet obsahů stěn, počítání čtverečků ve voxelové mřížce). Formát v _lib.py."""
import math
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402

PI = F(314, 100)  # π = 3,14, jako u zkoušky


def cz(x) -> str:
    """Číslo do textu: desetinná čárka, tisíce s mezerou, správné minus."""
    x = F(x)
    sign = "−" if x < 0 else ""
    x = abs(x)
    for k in range(7):
        if (x * 10 ** k).denominator == 1:
            break
    else:
        raise ValueError(f"neukončené desetinné číslo: {x}")
    s = str(int(x * 10 ** k)).rjust(k + 1, "0")
    ip, fp = (s[:-k], s[-k:]) if k else (s, "")
    return sign + f"{int(ip):,}".replace(",", " ") + ("," + fp if k else "")


# ------------------------------------------------------------------ nezávislé ověření: voxely a mnohoúhelníky
def surface(cubes) -> int:
    """Povrch tělesa z jednotkových krychliček = počet jejich stěn, které nesousedí s další krychličkou."""
    cubes = set(cubes)
    n = 0
    for (x, y, z) in cubes:
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (x + d[0], y + d[1], z + d[2]) not in cubes:
                n += 1
    return n


def block(a, b, c):
    return {(x, y, z) for x, y, z in product(range(a), range(b), range(c))}


def area(poly) -> float:
    """Obsah mnohoúhelníku (Gaussův vzorec), vrcholy proti směru hodin."""
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def perim(poly) -> float:
    return sum(math.dist(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))


def same(a, b) -> bool:
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-9)


# ------------------------------------------------------------------ obrázky (SVG, po zmenšení nejvýš 62 × 42 mm)
INK = "#1c2230"
K = 0.5 * math.cos(math.radians(45))  # volné rovnoběžné promítání: hloubka na polovinu, pod úhlem 45°


def P(x, y, z):
    """Bod tělesa (x doprava, y do hloubky, z nahoru) na papír."""
    return (x + K * y, z + K * y)


class Fig:
    """Kresba v centimetrech (y nahoru). Převod na SVG zvolí měřítko tak, aby po zmenšení na 62 × 42 mm měl text 2,9 mm."""
    U = 10  # jednotek viewBoxu na 1 cm kresby

    def __init__(self):
        self.el = []

    def line(self, p, q, dash=False, thin=False):
        self.el.append(("l", [p, q], dash, thin, None))

    def poly(self, pts, dash=False, thin=False, fill=None):
        self.el.append(("p", list(pts), dash, thin, fill))

    def curve(self, pts, dash=False, thin=False):
        self.el.append(("c", list(pts), dash, thin, None))

    def text(self, p, s, anchor="middle"):
        self.el.append(("t", p, s, anchor, None))

    def ellipse(self, c, rx, ry, a0=0, a1=360, dash=False):
        n = max(8, int((a1 - a0) / 6))
        self.curve([(c[0] + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
                    for i in range(n + 1)], dash=dash)

    def svg(self) -> str:
        U, fs = self.U, 8.0
        for _ in range(12):
            xs, ys = [], []
            for kind, d, a, b, _f in self.el:
                if kind == "t":
                    w = 0.56 * fs * len(a) / U
                    x0 = d[0] - w / 2 if b == "middle" else (d[0] if b == "start" else d[0] - w)
                    pts = [(x0, d[1] - 0.6 * fs / U), (x0 + w, d[1] + 0.6 * fs / U)]
                else:
                    pts = d
                xs += [p[0] for p in pts]
                ys += [p[1] for p in pts]
            x0, x1, y0, y1 = min(xs) - 0.25, max(xs) + 0.25, min(ys) - 0.25, max(ys) + 0.25
            W, H = (x1 - x0) * U, (y1 - y0) * U
            k = min(62 / W, 42 / H)  # mm na jednotku viewBoxu
            fs = 2.9 / k
        sw, sw2 = 0.35 / k, 0.2 / k
        dash = f"{1.3 / k:.1f} {0.9 / k:.1f}"

        def xy(p):
            return f"{(p[0] - x0) * U:.1f},{(y1 - p[1]) * U:.1f}"

        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Inter,Arial">']
        for kind, d, a, b, fill in self.el:
            if kind == "t":
                x, y = xy(d).split(",")
                out.append(f'<text x="{x}" y="{y}" dy=".35em" text-anchor="{b}" font-family="Inter,Arial" font-size="{fs:.1f}" fill="{INK}">{a}</text>')
                continue
            st = f'stroke="{INK}" stroke-width="{(sw2 if b else sw):.2f}" stroke-linejoin="round" stroke-linecap="round"'
            if a:
                st += f' stroke-dasharray="{dash}"'
            pts = " ".join(xy(p) for p in d)
            if kind == "p":
                out.append(f'<polygon points="{pts}" fill="{fill or "none"}" {st}/>')
            else:
                out.append(f'<polyline points="{pts}" fill="none" {st}/>')
        out.append("</svg>")
        return "".join(out)


def prism(f, base, depth):
    """Kolmý hranol v poloze na boku: přední stěna je `base` (konvexní mnohoúhelník proti směru hodin v rovině x–z),
    hloubka `depth` se kreslí šikmo. Neviditelné hrany jsou čárkované."""
    d = (K * depth, K * depth)
    n = len(base)
    vis = []
    for i in range(n):
        a, b = base[i], base[(i + 1) % n]
        nrm = (b[1] - a[1], -(b[0] - a[0]))  # vnější normála
        vis.append(nrm[0] * d[0] + nrm[1] * d[1] > 1e-9)
    sh = lambda p: (p[0] + d[0], p[1] + d[1])  # noqa: E731
    for i in range(n):
        a, b = base[i], base[(i + 1) % n]
        f.line(sh(a), sh(b), dash=not vis[i])
        f.line(a, sh(a), dash=not (vis[i - 1] or vis[i]))
    f.poly(base)
    return d


def box(f, a, b, c):
    return prism(f, [(0, 0), (a, 0), (a, c), (0, c)], b)


def fig_kvadr(a, b, c):
    f = Fig()
    d = box(f, a, b, c)
    f.text((a / 2, -0.55), f"{cz(a)} cm")
    f.text((-0.25, c / 2), f"{cz(c)} cm", "end")
    f.text((a + d[0] / 2 + 0.3, d[1] / 2 - 0.5), f"{cz(b)} cm", "start")
    return f.svg()


def fig_valec(r, h):
    f = Fig()
    ry = 0.3 * r
    f.line((-r, 0), (-r, h))
    f.line((r, 0), (r, h))
    f.ellipse((0, h), r, ry)
    f.ellipse((0, 0), r, ry, 180, 360)
    f.ellipse((0, 0), r, ry, 0, 180, dash=True)
    f.line((-r, h), (r, h), dash=True, thin=True)
    f.text((0, h + ry + 0.75), f"{cz(2 * r)} cm")
    f.text((r + 0.3, h / 2), f"{cz(h)} cm", "start")
    return f.svg()


def fig_hranol_trojuhelnik(zakl, vyska_tr, rameno, depth):
    base = [(0, 0), (zakl, 0), (zakl / 2, vyska_tr)]
    f = Fig()
    d = prism(f, base, depth)
    f.line((zakl / 2, 0), (zakl / 2, vyska_tr), dash=True, thin=True)
    f.text((zakl / 2 + 0.15, vyska_tr / 2 - 0.1), f"{cz(vyska_tr)} cm", "start")
    f.text((zakl / 2, -0.55), f"{cz(zakl)} cm")
    f.text((zakl * 0.25 - 0.45, vyska_tr / 2 + 0.55), f"{cz(rameno)} cm", "end")
    f.text((zakl + d[0] / 2 + 0.3, d[1] / 2 - 0.5), f"{cz(depth)} cm", "start")
    return f.svg()


def fig_hranol_lichobeznik(zakl, horni, vyska_l, depth):
    o = (zakl - horni) / 2
    base = [(0, 0), (zakl, 0), (zakl - o, vyska_l), (o, vyska_l)]
    f = Fig()
    d = prism(f, base, depth)
    f.line((o, 0), (o, vyska_l), dash=True, thin=True)
    f.text((o + 0.2, vyska_l / 2 - 0.25), f"{cz(vyska_l)} cm", "start")
    f.text((zakl / 2 + 0.5, vyska_l + 0.6), f"{cz(horni)} cm")
    f.text((zakl / 2, -0.55), f"{cz(zakl)} cm")
    f.text((zakl + d[0] / 2 + 0.3, d[1] / 2 - 0.5), f"{cz(depth)} cm", "start")
    return f.svg()


def fig_sit(a, b, c):
    """Síť kvádru: podstava a × b uprostřed, vlevo a vpravo stěny c × b, nad ní a pod ní stěny a × c, dole víko a × b."""
    rects = [(0, 0, a, b), (-c, 0, 0, b), (a, 0, a + c, b), (0, b, a, b + c), (0, -c, a, 0), (0, -c - b, a, -c)]
    f = Fig()
    for x0, y0, x1, y1 in rects:
        f.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    f.text((a / 2, b + c + 0.5), f"{cz(a)} cm")
    f.text((a + c + 0.3, b / 2), f"{cz(b)} cm", "start")
    f.text((-c / 2, -0.5), f"{cz(c)} cm")
    return f.svg(), rects


def fig_rez(a, b, c, x):
    """Kvádr a × b × c s řezem rovnoběžným se stěnou b × c ve vzdálenosti x od levé stěny."""
    f = Fig()
    d = box(f, a, b, c)
    f.poly([P(x, 0, 0), P(x, b, 0), P(x, b, c), P(x, 0, c)], dash=True, thin=True, fill="#dbe4fb")
    f.text((a / 2, -0.55), f"{cz(a)} cm")
    f.text((-0.25, c / 2), f"{cz(c)} cm", "end")
    f.text((a + d[0] / 2 + 0.3, d[1] / 2 - 0.5), f"{cz(b)} cm", "start")
    return f.svg()


T = Topic(10, "telesa", "Tělesa: objem a povrch",
          "Tělesa (krychle, kvádr, hranol, válec) se v testu objevují téměř každý rok, ale úspěšnost je jen kolem 28 %: žáci si pletou povrch s pláštěm "
          "a chybují v jednotkách. U jehlanu a kužele stačí tělesa poznat, u koule znát vztah poloměru a průměru.",
          ["Vzorce na objem a povrch v testu nejsou uvedeny, musíte je znát. Pamatujte: objem hranolu i válce je V = obsah podstavy · výška, povrch kvádru S = 2 · (ab + bc + ac).",
           "Povrch je součet obsahů všech stěn, plášť jen obsahů bočních stěn (bez podstav). U válce (r je poloměr podstavy, v výška) platí: plášť = 2 · π · r · v, povrch = 2 · π · r² + 2 · π · r · v.",
           "Jednotky: 1 l = 1 dm³ = 1 000 cm³, 1 m³ = 1 000 dm³ = 1 000 l. Před výpočtem převeďte všechny rozměry na stejnou jednotku.",
           "Poloměr je polovina průměru: při průměru 10 cm počítejte s r = 5 cm. Používejte π = 3,14 a nejdřív spočtěte r².",
           "Zvětšíte-li všechny rozměry tělesa na dvojnásobek, povrch se zvětší čtyřikrát a objem osmkrát, ne dvakrát.",
           "U tělesa slepeného z krychliček se odebráním krychličky z rohu povrch nezmění, odebráním z hrany nebo ze středu stěny se zvětší."])

# ---------------------------------------------------------------- Řešený příklad
o1, o2, o3, vh = 3, 4, 5, 10
sp = F(o1 * o2, 2)
V = sp * vh
S = 2 * sp + (o1 + o2 + o3) * vh
tri = [(0, 0), (o2, 0), (0, o1)]
T.example("Podstavou kolmého hranolu je pravoúhlý trojúhelník s odvěsnami 3 cm a 4 cm a přeponou 5 cm. "
          "Výška hranolu je 10 cm. Vypočtěte objem a povrch hranolu.",
          ["Obsah podstavy: 3 · 4 : 2 = 6 cm². Objem je obsah podstavy vynásobený výškou hranolu: V = 6 · 10 = 60 cm³.",
           "Plášť tvoří tři obdélníky s výškou 10 cm, jejich šířky se rovnají stranám podstavy. Obvod podstavy: 3 + 4 + 5 = 12 cm, obsah pláště: 12 · 10 = 120 cm².",
           "Povrch tvoří plášť a dvě podstavy: S = 120 + 2 · 6 = 132 cm²."],
          "V = 60 cm³, S = 132 cm²",
          V == 60 and S == 132 and o1 ** 2 + o2 ** 2 == o3 ** 2 and same(area(tri), 6) and same(perim(tri), 12))

# ---------------------------------------------------------------- Základ
a = 5
T.task(1, "Vypočtěte objem a povrch krychle s hranou 5 cm.", "V = 125 cm³, S = 150 cm²",
       ["Objem krychle: V = a · a · a = 5 · 5 · 5 = 125 cm³.",
        "Povrch tvoří 6 shodných čtverců o straně 5 cm. Obsah jednoho čtverce je 5 · 5 = 25 cm².",
        "Povrch: S = 6 · 25 = 150 cm²."],
       a ** 3 == 125 and 6 * a * a == 150 == surface(block(a, a, a)) and len(block(a, a, a)) == 125, space=2)

a, b, c = 8, 5, 3
S1, V1 = 2 * (a * b + a * c + b * c), a * b * c
T.task(1, "Kvádr má rozměry 8 cm, 5 cm a 3 cm (obrázek). Vypočtěte jeho objem a povrch.", f"V = {V1} cm³, S = {S1} cm²",
       [f"Objem: V = 8 · 5 · 3 = {V1} cm³.",
        "Kvádr má tři dvojice shodných stěn: 8 · 5 = 40 cm², 8 · 3 = 24 cm² a 5 · 3 = 15 cm².",
        f"Povrch: S = 2 · (40 + 24 + 15) = 2 · 79 = {S1} cm²."],
       (V1, S1) == (120, 158) and surface(block(a, b, c)) == S1 and len(block(a, b, c)) == V1, figure=fig_kvadr(a, b, c), space=2)

conv = [F(35, 10) * 1000, F(2400, 1000), F(6, 10) * 1000, F(1500, 1000)]
T.task(1, "Převeďte jednotky: a) 3,5 dm³ = … cm³, b) 2 400 cm³ = … l, c) 0,6 m³ = … l, d) 1 500 l = … m³.",
       "a) 3 500 cm³, b) 2,4 l, c) 600 l, d) 1,5 m³",
       ["a) 1 dm³ = 1 000 cm³, takže 3,5 · 1 000 = 3 500 cm³.",
        "b) 1 l = 1 000 cm³, takže 2 400 : 1 000 = 2,4 l.",
        "c) 1 m³ = 1 000 dm³ = 1 000 l, takže 0,6 · 1 000 = 600 l.",
        "d) 1 500 l = 1 500 dm³, 1 m³ = 1 000 dm³, takže 1 500 : 1 000 = 1,5 m³."],
       conv == [3500, F(12, 5), 600, F(3, 2)] and [cz(x) for x in conv] == ["3 500", "2,4", "600", "1,5"], space=2)

a, b, c = 60, 30, 40
litru = F(a * b * c, 1000)
T.task(1, "Akvárium tvaru kvádru má dno o rozměrech 60 cm a 30 cm a výšku 40 cm. Kolik litrů vody se do něj vejde, naplníme-li ho po okraj?",
       "72 l",
       ["Objem akvária: V = 60 · 30 · 40 = 72 000 cm³.",
        "1 l = 1 000 cm³, proto 72 000 : 1 000 = 72 l.",
        "Jiný postup: 6 dm · 3 dm · 4 dm = 72 dm³ = 72 l."],
       litru == 72 and F(6 * 3 * 4) == litru, space=2)


def tvrzeni_telesa():
    """Počty stěn, hran a vrcholů n-bokého hranolu a jehlanu (s kontrolou Eulerovy věty)."""
    def hranol(n):
        return {"s": n + 2, "h": 3 * n, "v": 2 * n}

    def jehlan(n):
        return {"s": n + 1, "h": 2 * n, "v": n + 1}
    for t in (hranol(3), hranol(4), jehlan(4)):
        assert t["v"] - t["h"] + t["s"] == 2
    return hranol, jehlan


hranol, jehlan = tvrzeni_telesa()
T.task(1, "Platí tato tvrzení o tělesech?", "NE, ANO, ANO",
       ["Čtyřboký jehlan má 4 hrany podstavy a 4 boční hrany, dohromady 8 hran, ne 5. Tvrzení neplatí (5 je počet jeho stěn).",
        "Kvádr má 4 hrany dole, 4 nahoře a 4 svislé, dohromady 12 hran. Vrcholů má 4 + 4 = 8. Platí.",
        "Trojboký hranol má dvě podstavy (trojúhelníky) a tři boční stěny (obdélníky), dohromady 5 stěn. Platí."],
       (jehlan(4)["h"], jehlan(4)["s"]) == (8, 5) and (12, 8) == (hranol(4)["h"], hranol(4)["v"]) and hranol(3)["s"] == 5,
       kind="yesno", options=["Čtyřboký jehlan má 5 hran.", "Kvádr má 12 hran a 8 vrcholů.", "Trojboký hranol má 5 stěn."], space=1)

# ---------------------------------------------------------------- Jako u zkoušky
a, b, V0 = 12, 5, 480
c = F(V0, a * b)
S2 = 2 * (a * b + a * c + b * c)
T.task(2, "Podstava kvádru má rozměry 12 cm a 5 cm, objem kvádru je 480 cm³. Vypočtěte výšku kvádru a jeho povrch. Uveďte celý postup.",
       f"v = {cz(c)} cm, S = {cz(S2)} cm²",
       ["Objem kvádru: V = a · b · c, tedy 480 = 12 · 5 · c = 60 · c.",
        "Výška: c = 480 : 60 = 8 cm.",
        "Obsahy stěn: 12 · 5 = 60 cm², 12 · 8 = 96 cm² a 5 · 8 = 40 cm².",
        "Povrch: S = 2 · (60 + 96 + 40) = 2 · 196 = 392 cm²."],
       c == 8 and S2 == 392 == surface(block(12, 5, 8)) and len(block(12, 5, 8)) == V0, space=4)

r, h = 5, 10
sp = PI * r * r
V3, plast, S3 = sp * h, 2 * PI * r * h, 2 * sp + 2 * PI * r * h
T.task(2, "Válec má průměr podstavy 10 cm a výšku 10 cm (obrázek). Vypočtěte objem, obsah pláště a povrch válce. Použijte π = 3,14.",
       f"V = {cz(V3)} cm³, plášť {cz(plast)} cm², S = {cz(S3)} cm²",
       ["Poloměr je polovina průměru: r = 10 : 2 = 5 cm.",
        "Obsah podstavy: π · r² = 3,14 · 25 = 78,5 cm². Objem: V = 78,5 · 10 = 785 cm³.",
        "Rozvinutý plášť je obdélník s výškou 10 cm a šířkou rovnou obvodu podstavy: 2 · π · r = 2 · 3,14 · 5 = 31,4 cm. Obsah pláště: 31,4 · 10 = 314 cm².",
        "Povrch tvoří dvě podstavy a plášť: S = 2 · 78,5 + 314 = 157 + 314 = 471 cm²."],
       (sp, V3, plast, S3) == (F(785, 10), 785, 314, 471) and 2 * r == 10, figure=fig_valec(r, h), space=4)

zakl, vt, ram, hh = 8, 3, 5, 10
tri = [(0, 0), (zakl, 0), (zakl / 2, vt)]
sp = F(zakl * vt, 2)
V4, S4 = sp * hh, 2 * sp + (zakl + 2 * ram) * hh
T.task(2, "Podstavou kolmého hranolu je rovnoramenný trojúhelník se základnou 8 cm, rameny 5 cm a výškou na základnu 3 cm. "
          "Výška hranolu je 10 cm (obrázek, hranol je na něm položený na boku). Vypočtěte objem a povrch hranolu.",
       f"V = {cz(V4)} cm³, S = {cz(S4)} cm²",
       ["Obsah podstavy: 8 · 3 : 2 = 12 cm².",
        "Objem: V = 12 · 10 = 120 cm³.",
        "Obvod podstavy: 5 + 5 + 8 = 18 cm. Plášť tvoří tři obdélníky s výškou 10 cm, jeho obsah je 18 · 10 = 180 cm².",
        "Povrch: S = 2 · 12 + 180 = 204 cm²."],
       (V4, S4) == (120, 204) and same(area(tri), 12) and same(perim(tri), 18) and same(math.dist(tri[0], tri[2]), ram),
       figure=fig_hranol_trojuhelnik(zakl, vt, ram, hh), space=4)

a, b, c = 4, 3, 2
sit, rects = fig_sit(a, b, c)
cells = {(x, y) for x0, y0, x1, y1 in rects for x in range(x0, x1) for y in range(y0, y1)}
sit_plocha = sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects)
V5, S5 = a * b * c, 2 * (a * b + a * c + b * c)
T.task(2, "Obrázek ukazuje síť kvádru. Vypočtěte objem a povrch kvádru.", f"V = {V5} cm³, S = {S5} cm²",
       ["Z obrázku: hrany kvádru mají délky 4 cm, 3 cm a 2 cm.",
        "Objem: V = 4 · 3 · 2 = 24 cm³.",
        "Povrch je obsah celé sítě. Síť tvoří tři dvojice shodných obdélníků: 4 · 3 = 12 cm², 4 · 2 = 8 cm² a 3 · 2 = 6 cm².",
        "Povrch: S = 2 · (12 + 8 + 6) = 52 cm²."],
       (V5, S5) == (24, 52) and sit_plocha == S5 == len(cells) and surface(block(a, b, c)) == S5, figure=sit, space=3)

dno_a, dno_b, nalito, vyska2 = 50, 40, 30, 35
dno = dno_a * dno_b
hladina = F(nalito * 1000, dno)
dolit = F(dno * vyska2, 1000) - nalito
T.task(2, "Prázdné akvárium tvaru kvádru má dno o rozměrech 50 cm a 40 cm. Nalijeme do něj 30 litrů vody. "
          "a) Do jaké výšky voda sahá? b) Kolik litrů vody musíme ještě dolít, aby voda sahala do výšky 35 cm?",
       f"a) {cz(hladina)} cm, b) {cz(dolit)} l",
       ["Obsah dna: 50 · 40 = 2 000 cm². Objem vody: 30 l = 30 000 cm³.",
        "a) Výška hladiny je objem vody dělený obsahem dna: 30 000 : 2 000 = 15 cm.",
        "b) Do výšky 35 cm je potřeba 2 000 · 35 = 70 000 cm³ = 70 l.",
        "Dolít musíme 70 − 30 = 40 l. Jiný postup: hladina musí vystoupit o 35 − 15 = 20 cm, tedy 2 000 · 20 = 40 000 cm³ = 40 l."],
       (hladina, dolit) == (15, 40) and F(dno * (vyska2 - hladina), 1000) == dolit, space=4)

a, b, c, x = 10, 6, 4, 4
ploch = lambda p, q, r_: 2 * (p * q + p * r_ + q * r_)  # noqa: E731
rozdily = {ploch(x, b, c) + ploch(a - x, b, c) - ploch(a, b, c) for x in (1, 2, 3, 4, 5, 7)}  # poloha řezu nehraje roli
vox = block(a, b, c)
levy = {p for p in vox if p[0] < x}
pravy = vox - levy
rozdil = surface(levy) + surface(pravy) - surface(vox)
moznosti = {"0 cm²": 0, "24 cm²": 24, "48 cm²": 48, "60 cm²": 60, "120 cm²": 120}
T.task(2, "Kvádr o rozměrech 10 cm, 6 cm a 4 cm rozřízneme jedním rovným řezem rovnoběžným se stěnou o rozměrech 6 cm a 4 cm (obrázek). "
          "Vzniknou dva menší kvádry. O kolik cm² je součet povrchů obou menších kvádrů větší než povrch původního kvádru?", "C",
       ["Každý ze dvou menších kvádrů má jednu novou stěnu, která vznikla řezem. Je to obdélník o rozměrech 6 cm a 4 cm.",
        "Obsah jedné nové stěny: 6 · 4 = 24 cm². Obě nové stěny: 2 · 24 = 48 cm².",
        "Ostatní stěny menších kvádrů jsou jen části původních stěn, jejich celkový obsah se nezměnil. Součet povrchů je tedy o 48 cm² větší, na poloze řezu nezáleží. Správně je C."],
       rozdily == {48} and rozdil == 48 and [k for k, v in moznosti.items() if v == rozdil] == ["48 cm²"],
       kind="choice", options=list(moznosti), figure=fig_rez(a, b, c, x), space=2)

mic_r, rada, rady, vrstvy = 5, 4, 3, 2
mic_d = 2 * mic_r
rozm = (rada * mic_d, rady * mic_d, vrstvy * mic_d)
V6 = F(rozm[0] * rozm[1] * rozm[2], 1000)
T.task(2, "Do kvádrové krabice je těsně uloženo 24 míčů o poloměru 5 cm: 4 míče v řadě, 3 řady vedle sebe a 2 vrstvy nad sebou. "
          "Míče se navzájem dotýkají i stěn krabice. a) Jaké rozměry má krabice? b) Jaký je její vnitřní objem v litrech?",
       f"a) 40 cm, 30 cm a 20 cm, b) {cz(V6)} l",
       ["Pozor: poloměr míče je 5 cm, tedy jeho průměr je 10 cm. V řadě vedle sebe zabere každý míč 10 cm.",
        "a) Délka: 4 · 10 = 40 cm, šířka: 3 · 10 = 30 cm, výška: 2 · 10 = 20 cm.",
        "b) Objem: V = 40 · 30 · 20 = 24 000 cm³ = 24 dm³ = 24 l."],
       rozm == (40, 30, 20) and rada * rady * vrstvy == 24 and V6 == 24, space=3)

# ---------------------------------------------------------------- Náročnější
zakl, horni, vl, hl = 12, 4, 3, 7
o = F(zakl - horni, 2)
rameno = math.hypot(o, vl)
lich = [(0, 0), (zakl, 0), (zakl - o, vl), (o, vl)]
sp = F((zakl + horni) * vl, 2)
V7 = sp * hl
S7 = 2 * sp + (zakl + horni + 2 * 5) * hl
T.task(3, "Podstavou kolmého hranolu je rovnoramenný lichoběžník se základnami 12 cm a 4 cm a výškou 3 cm. Výška hranolu je 7 cm (obrázek, hranol je na něm položený na boku). "
          "Vypočtěte objem a povrch hranolu.", f"V = {cz(V7)} cm³, S = {cz(S7)} cm²",
       ["Obsah podstavy: (12 + 4) : 2 · 3 = 24 cm². Objem: V = 24 · 7 = 168 cm³.",
        "Délku ramene spočteme Pythagorovou větou. Základny se liší o 12 − 4 = 8 cm, na každé straně tedy delší základna přesahuje kratší o 4 cm.",
        "Rameno je přepona pravoúhlého trojúhelníku s odvěsnami 4 cm a 3 cm: √(4² + 3²) = √25 = 5 cm.",
        "Obvod podstavy: 12 + 4 + 5 + 5 = 26 cm. Plášť: 26 · 7 = 182 cm².",
        "Povrch: S = 2 · 24 + 182 = 230 cm²."],
       (V7, S7) == (168, 230) and same(rameno, 5) and same(area(lich), 24) and same(perim(lich), 26)
       and same(2 * area(lich) + perim(lich) * hl, 230), figure=fig_hranol_lichobeznik(zakl, horni, vl, hl), space=5)

dno_a, dno_b, nalito_v, hrana = 25, 16, 12, 10
nahore = F(hrana ** 3, dno_a * dno_b)
T.task(3, "Nádoba tvaru kvádru má dno o rozměrech 25 cm a 16 cm a výšku 30 cm. Voda v ní sahá do výšky 12 cm. "
          "Do vody úplně ponoříme kovovou krychli o hraně 10 cm (voda nepřeteče). O kolik centimetrů vystoupí hladina?",
       f"o {cz(nahore)} cm",
       ["Krychle vytlačí tolik vody, jaký je její objem: 10 · 10 · 10 = 1 000 cm³.",
        "Obsah dna nádoby: 25 · 16 = 400 cm². Hladina vystoupí o x cm. Objem přibylé vrstvy vody je 400 · x cm³ a rovná se objemu krychle: 400 · x = 1 000.",
        "x = 1 000 : 400 = 2,5 cm.",
        "Kontrola: hladina je nyní ve výšce 12 + 2,5 = 14,5 cm. To je víc než 10 cm (krychle je celá pod vodou) a méně než 30 cm (voda nepřeteče)."],
       nahore == F(5, 2) and hrana < nalito_v + nahore < 30, space=4)

n = 4
barvy = {}
for p in product(range(n), repeat=3):
    barvy[p] = sum(1 for k in p if k in (0, n - 1))  # počet natřených stěn
pocty = {k: sum(1 for v in barvy.values() if v == k) for k in range(4)}
T.task(3, "Velkou krychli o hraně 4 cm slepíme z 64 malých krychliček o hraně 1 cm. Celý povrch velké krychle natřeme barvou "
          "a krychli potom rozebereme zpět na malé krychličky. Kolik malých krychliček má natřené a) právě dvě stěny, b) žádnou stěnu?",
       "a) 24, b) 8",
       ["Natřenou stěnu mají jen krychličky na povrchu velké krychle. Právě dvě natřené stěny mají krychličky na hranách velké krychle, ale ne v jejích rozích.",
        "a) Velká krychle má 12 hran. Na každé je 4 krychličky, dvě z nich jsou v rozích, zbývají 2. Celkem 12 · 2 = 24.",
        "b) Žádnou natřenou stěnu nemají krychličky uvnitř. Odebereme-li z každé strany vnější vrstvu, zbude krychle 2 · 2 · 2 = 8 krychliček.",
        "Kontrola: 8 rohových (tři stěny) + 24 (dvě stěny) + 6 · 4 = 24 (jedna stěna) + 8 (žádná stěna) = 64. ✓"],
       pocty == {0: 8, 1: 24, 2: 24, 3: 8} and sum(pocty.values()) == 64 == n ** 3 and 12 * (n - 2) == 24 and (n - 2) ** 3 == 8, space=4)

kostka = block(3, 3, 3)
base_s = surface(kostka)
zmena = {nm: surface(kostka - {p}) - base_s for nm, p in {"roh": (0, 0, 0), "hrana": (1, 0, 0), "stena": (1, 1, 0)}.items()}
T.task(3, "Krychle o hraně 3 cm je slepená z 27 krychliček o hraně 1 cm. Vždy z ní odebereme jednu krychličku a povrch vzniklého tělesa porovnáme s povrchem původní krychle. Platí tato tvrzení?",
       "ANO, ANO, NE",
       ["Povrch původní krychle je 6 · 9 = 54 cm².",
        "Krychlička v rohu má na povrchu 3 stěny. Po jejím odebrání zmizí 3 čtverce z povrchu a odkryjí se 3 nové. Povrch se nezmění. Platí.",
        "Krychlička uprostřed hrany má na povrchu 2 stěny a po jejím odebrání se odkryjí 4 nové. Povrch se zvětší o 4 − 2 = 2 cm². Platí.",
        "Krychlička uprostřed stěny má na povrchu 1 stěnu a po jejím odebrání se odkryje 5 nových. Povrch se zvětší o 5 − 1 = 4 cm², ne o 2 cm². Tvrzení neplatí."],
       base_s == 54 and zmena == {"roh": 0, "hrana": 2, "stena": 4},
       kind="yesno", options=["Odebereme-li krychličku z rohu, povrch se nezmění.",
                              "Odebereme-li krychličku uprostřed hrany (ne z rohu), povrch se zvětší o 2 cm².",
                              "Odebereme-li krychličku uprostřed stěny, povrch se zvětší o 2 cm²."], space=1)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
mnoz = {"2krát": 2, "4krát": 4, "6krát": 6, "8krát": 8, "9krát": 9}
T.diagnostic("Hranu krychle zdvojnásobíme. Kolikrát se zvětší její objem?", "D",
             ["Původní krychle má hranu a a objem a · a · a. Nová hrana je 2a a objem 2a · 2a · 2a = 8 · a · a · a.",
              "Objem se zvětší 8krát (povrch by se zvětšil 4krát)."],
             [k for k, v in mnoz.items() if F((2 * 3) ** 3, 3 ** 3) == v] == ["8krát"], kind="choice", options=list(mnoz))

r, h = 10, 5
dno_pl = PI * r * r
S8 = dno_pl + 2 * PI * r * h
T.diagnostic("Plechová nádoba bez víka má tvar válce s průměrem 20 cm a výškou 5 cm. Kolik cm² plechu je na ni potřeba (spoje zanedbejte)? Použijte π = 3,14.",
             f"{cz(S8)} cm²",
             ["Poloměr: r = 20 : 2 = 10 cm. Dno: π · r² = 3,14 · 100 = 314 cm².",
              "Plášť: 2 · π · r · v = 2 · 3,14 · 10 · 5 = 314 cm². Víko nepočítáme.",
              "Plechu je potřeba 314 + 314 = 628 cm²."],
             (dno_pl, 2 * PI * r * h, S8) == (314, 314, 628))

T.save()
