#!/usr/bin/env python3
"""Téma 7: Grafy, tabulky a průměr. Obrázky (SVG) se kreslí ze stejných dat, ze kterých se počítají výsledky a tvrzení,
takže čísla v grafu souhlasí s textem i s řešením. Formát v _lib.py, vzor je 01_zlomky.py."""
import sys
from fractions import Fraction as F
from math import cos, pi, sin
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, dec  # noqa: E402

# ------------------------------------------------------------------ pomůcky pro obrázky (SVG, viewBox 248 × 168 = 62 × 42 mm)
INK, GRID, SOFT = "#1c2230", "#c9ccd4", "#dbe4fb"
W, H = 248, 168


def svg(inner: str, h: int = H) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" font-family="Inter,Arial" font-size="10">{inner}</svg>'


def nf(v) -> str:
    """Číslo do obrázku a textu: desetinná čárka, správné minus."""
    return f"{v:g}".replace(".", ",").replace("-", "−")


def pt_txt(x, y) -> str:
    return f"[{nf(x)}; {nf(y)}]"


def txt(x, y, s, size=10, anchor="middle") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{INK}">{s}</text>'


def ln(x1, y1, x2, y2, c=INK, w=1.0, dash=None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, r=2.3, fill=INK) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1"/>'


class Plot:
    """Graf s osami: převod hodnot na souřadnice obrázku, mřížka a popisky."""

    def __init__(self, xmin, xmax, ymin, ymax, left=30, right=8, top=18, bottom=24):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.l, self.t = left, top
        self.pw, self.ph = W - left - right, H - top - bottom
        self.b = top + self.ph

    def X(self, x):
        return self.l + self.pw * (x - self.xmin) / (self.xmax - self.xmin)

    def Y(self, y):
        return self.b - self.ph * (y - self.ymin) / (self.ymax - self.ymin)

    def ticks(self, lo, hi, step):
        n = round((hi - lo) / step)
        return [lo + i * step for i in range(n + 1)]

    def grid(self, ystep, ylab, xstep=None, xlab=1, ytitle="", xtitle="", xshow=None):
        o = []
        for k, v in enumerate(self.ticks(self.ymin, self.ymax, ystep)):
            o.append(ln(self.l, self.Y(v), self.l + self.pw, self.Y(v), GRID, .6))
            if k % ylab == 0:
                o.append(txt(self.l - 4, self.Y(v) + 3.3, nf(v), 9.5, "end"))
        if xstep:
            for k, v in enumerate(self.ticks(self.xmin, self.xmax, xstep)):
                o.append(ln(self.X(v), self.t, self.X(v), self.b, GRID, .6))
                if k % xlab == 0 and (xshow is None or v in xshow):
                    o.append(txt(self.X(v), self.b + 11, nf(v), 9.5))
        if ytitle:
            o.append(txt(2, 10, ytitle, 9.5, "start"))
        if xtitle:
            o.append(txt(self.l + self.pw, self.b + 22, xtitle, 9.5, "end"))
        return "".join(o)

    def axes(self):
        return ln(self.l, self.t, self.l, self.b, INK, 1.2) + ln(self.l, self.b, self.l + self.pw, self.b, INK, 1.2)


def bar_chart(cats, vals, ymax, ystep, ylab=1, ytitle="") -> str:
    p = Plot(0, len(cats), 0, ymax, left=30, right=6, top=18, bottom=30)
    o = [p.grid(ystep, ylab, ytitle=ytitle)]
    slot = p.pw / len(cats)
    bw = slot * 0.56
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = p.l + slot * i + (slot - bw) / 2
        o.append(f'<rect x="{x:.1f}" y="{p.Y(v):.1f}" width="{bw:.1f}" height="{p.Y(0) - p.Y(v):.1f}" fill="{SOFT}" stroke="{INK}" stroke-width="1"/>')
        for j, word in enumerate(c.split()):
            o.append(txt(p.l + slot * (i + .5), p.b + 11 + 10 * j, word, 9.5))
    o.append(p.axes())
    return svg("".join(o))


def line_chart(p: Plot, pts, grid_svg, dots=True) -> str:
    poly = " ".join(f"{p.X(x):.1f},{p.Y(y):.1f}" for x, y in pts)
    o = [grid_svg, f'<polyline points="{poly}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>']
    if dots:
        o += [dot(p.X(x), p.Y(y), 2.2, "#ffffff") for x, y in pts]
    o.append(p.axes())
    return svg("".join(o))


FILLS = ["#ffffff", "#dbe4fb", "#fbe9b7", "#c4cfee", "#e8eaf0"]


def pie(values, names, shown, r=48, cx=124, cy=84) -> str:
    """Kruhový diagram od 12 hodin po směru hodinových ručiček; shown = druhý řádek popisku (např. „30 %“, „72°“)."""
    total = sum(values)
    o, a0 = [], 0.0
    for i, v in enumerate(values):
        a1 = a0 + 2 * pi * v / total
        x0, y0, x1, y1 = cx + r * sin(a0), cy - r * cos(a0), cx + r * sin(a1), cy - r * cos(a1)
        large = 1 if a1 - a0 > pi else 0
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f} Z" fill="{FILLS[i % len(FILLS)]}" stroke="{INK}" stroke-width="1"/>')
        am = (a0 + a1) / 2
        tx, ty = cx + (r + 6) * sin(am), cy - (r + 6) * cos(am)
        anchor = "start" if sin(am) > .2 else "end" if sin(am) < -.2 else "middle"
        if cos(am) > .6:
            y1_, y2_ = ty - 11, ty - 1
        elif cos(am) < -.6:
            y1_, y2_ = ty + 9, ty + 19
        else:
            y1_, y2_ = ty - 1, ty + 10
        o.append(txt(tx, y1_, names[i], 10, anchor) + txt(tx, y2_, shown[i], 10, anchor))
        a0 = a1
    return svg("".join(o))


class Plane:
    """Soustava souřadnic s mřížkou po jednotkách; s = délka jednotky v obrázku."""

    def __init__(self, xmin, xmax, ymin, ymax, s):
        self.xmin, self.xmax, self.ymin, self.ymax, self.s = xmin, xmax, ymin, ymax, s
        self.ox = (W - (xmax - xmin) * s) / 2 - xmin * s
        self.oy = (H - (ymax - ymin) * s) / 2 + ymax * s

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy - y * self.s

    def base(self) -> str:
        o = []
        for i in range(self.xmin, self.xmax + 1):
            o.append(ln(self.X(i), self.Y(self.ymin), self.X(i), self.Y(self.ymax), GRID, .6))
        for j in range(self.ymin, self.ymax + 1):
            o.append(ln(self.X(self.xmin), self.Y(j), self.X(self.xmax), self.Y(j), GRID, .6))
        xe, ye = self.X(self.xmax) + 9, self.Y(self.ymax) - 8
        o.append(ln(self.X(self.xmin) - 4, self.oy, xe, self.oy, INK, 1.2))
        o.append(ln(self.ox, self.Y(self.ymin) + 4, self.ox, ye, INK, 1.2))
        o.append(f'<polygon points="{xe + 3:.1f},{self.oy:.1f} {xe - 4:.1f},{self.oy - 2.6:.1f} {xe - 4:.1f},{self.oy + 2.6:.1f}" fill="{INK}"/>')
        o.append(f'<polygon points="{self.ox:.1f},{ye - 3:.1f} {self.ox - 2.6:.1f},{ye + 4:.1f} {self.ox + 2.6:.1f},{ye + 4:.1f}" fill="{INK}"/>')
        o.append(txt(xe, self.oy + 11, "x", 10) + txt(self.ox + 8, ye + 3, "y", 10))
        for i in range(self.xmin, self.xmax + 1):
            if i:
                o.append(ln(self.X(i), self.oy - 2, self.X(i), self.oy + 2, INK, 1))
                o.append(txt(self.X(i), self.oy + 11, nf(i), 8.5))
        for j in range(self.ymin, self.ymax + 1):
            if j:
                o.append(ln(self.ox - 2, self.Y(j), self.ox + 2, self.Y(j), INK, 1))
                o.append(txt(self.ox - 4, self.Y(j) + 3, nf(j), 8.5, "end"))
        o.append(txt(self.ox - 4, self.oy + 11, "0", 8.5, "end"))
        return "".join(o)

    def point(self, x, y, name, dx=5, dy=-5) -> str:
        anchor = "start" if dx >= 0 else "end"
        return dot(self.X(x), self.Y(y), 2.4) + txt(self.X(x) + dx, self.Y(y) + dy, name, 10.5, anchor)


def table_svg(row_labels, rows, first_w=92, cell_w=34, cell_h=20) -> str:
    o = []
    for r, (lab, vals) in enumerate(zip(row_labels, rows)):
        y = 2 + r * cell_h
        o.append(f'<rect x="2" y="{y}" width="{first_w}" height="{cell_h}" fill="{SOFT}" stroke="{INK}" stroke-width="1"/>')
        o.append(txt(2 + first_w / 2, y + cell_h / 2 + 3.5, lab, 10))
        for c, v in enumerate(vals):
            x = 2 + first_w + c * cell_w
            o.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#ffffff" stroke="{INK}" stroke-width="1"/>')
            o.append(txt(x + cell_w / 2, y + cell_h / 2 + 3.5, str(v), 10.5))
    return svg("".join(o), h=2 * len(rows) * 10 + 6)


def mean(xs):
    return F(sum(xs), len(xs))


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def modes(xs):
    top = max(xs.count(v) for v in set(xs))
    return sorted(v for v in set(xs) if xs.count(v) == top)


# ------------------------------------------------------------------ téma
T = Topic(7, "grafy", "Grafy, tabulky a průměr",
          "Práce s grafem, tabulkou nebo průměrem se objevuje skoro v každém testu, nejčastěji jako úloha 11 se třemi tvrzeními ANO/NE. "
          "Jsou to „levné“ body: stačí pozorně číst a počítat jednoduše.",
          ["Než začnete počítat, přečtěte název grafu, popisky os a jednotky. Zjistěte, kolik odpovídá jeden dílek stupnice: čáry v mřížce nemusí znamenat 1.",
           "Aritmetický průměr = součet všech hodnot : jejich počet. Chybějící hodnotu najdete ze součtu: součet = průměr · počet hodnot. "
           "Průměry různě velkých skupin nesčítejte a nedělte dvěma, počítejte vážený průměr.",
           "Medián je prostřední hodnota až po seřazení podle velikosti (u sudého počtu průměr dvou prostředních). Modus je nejčastější hodnota. "
           "Nejčastější chyba: medián vybraný z neseřazených čísel.",
           "Kruhový diagram: celý kruh je 100 % a 360°, tedy 1 % je 3,6°. Čtvrtina kruhu je 25 % a 90°.",
           "U tvrzení ANO/NE ověřte každé zvlášť a přesně podle grafu. Pozor na slova „dvakrát víc“, „o třetinu víc“, „nejméně“, „celkem“.",
           "Souřadnice bodu se píší [x; y]: nejdřív vodorovně, pak svisle. U lineární závislosti y = kx + q je q hodnota y pro x = 0 "
           "a k říká, o kolik se y změní, když x vzroste o 1."])

# ---------------------------------------------------------------- řešený příklad
znamky = {1: 5, 2: 8, 3: 6, 4: 1}
n_zaku = sum(znamky.values())
soucet = sum(z * k for z, k in znamky.items())
serazene = sorted(z for z, k in znamky.items() for _ in range(k))
T.example(f"V písemce dopadly známky takto: jedničku dostalo {znamky[1]} žáků, dvojku {znamky[2]} žáků, trojku {znamky[3]} žáků a čtyřku {znamky[4]} žák. "
          "Vypočtěte průměrnou známku a určete medián známek.",
          [f"Počet žáků: 5 + 8 + 6 + 1 = {n_zaku}.",
           "Součet všech známek: 1 · 5 + 2 · 8 + 3 · 6 + 4 · 1 = 5 + 16 + 18 + 4 = 43.",
           "Průměr: 43 : 20 = 2,15.",
           "Medián: známek je 20, prostřední jsou 10. a 11. v pořadí. Jedničky jsou na místech 1 až 5, dvojky na místech 6 až 13.",
           "Obě prostřední známky jsou dvojky, medián je tedy 2."],
          "průměr 2,15; medián 2",
          n_zaku == 20 and soucet == 43 and mean(serazene) == F(215, 100) and median(serazene) == 2
          and serazene[9] == serazene[10] == 2)

# ---------------------------------------------------------------- Základ
dny, knihy = ["po", "út", "st", "čt", "pá"], [15, 25, 20, 10, 30]
T.task(1, "Sloupcový graf ukazuje, kolik knih si čtenáři školní knihovny vypůjčili v jednotlivých dnech jednoho týdne. "
          "a) Kolik knih bylo vypůjčeno za celý týden? b) O kolik knih víc si čtenáři půjčili v pátek než ve středu?",
       "a) 100 knih; b) o 10 knih",
       ["Z grafu přečteme: pondělí 15, úterý 25, středa 20, čtvrtek 10, pátek 30 knih.",
        "a) Za týden: 15 + 25 + 20 + 10 + 30 = 100 knih.", "b) Pátek − středa: 30 − 20 = 10 knih."],
       sum(knihy) == 100 and knihy[4] - knihy[2] == 10 and len(dny) == len(knihy),
       figure=bar_chart(dny, knihy, 30, 5, ytitle="počet knih"), space=2)

cisla = [9, 1, 5, 9, 7, 2, 9]
T.task(1, f"Je dáno sedm čísel: {', '.join(map(str, cisla))}. Určete jejich aritmetický průměr, medián a modus.",
       "průměr 6, medián 7, modus 9",
       ["Součet: 9 + 1 + 5 + 9 + 7 + 2 + 9 = 42, průměr 42 : 7 = 6.",
        "Seřazená čísla: 1, 2, 5, 7, 9, 9, 9. Prostřední (čtvrté) číslo je 7, medián je 7.",
        "Nejčastěji se opakuje číslo 9 (třikrát), modus je 9."],
       sum(cisla) == 42 and mean(cisla) == 6 and sorted(cisla) == [1, 2, 5, 7, 9, 9, 9] and median(cisla) == 7 and modes(cisla) == [9],
       space=2)

body = {"A": (2, 3), "B": (-3, 1), "C": (-1, -2), "D": (4, -3)}
pl = Plane(-5, 5, -4, 4, 18)
fig = svg(pl.base() + pl.point(2, 3, "A") + pl.point(-3, 1, "B", -5, -5) + pl.point(-1, -2, "C", -5, 11) + pl.point(4, -3, "D", 5, 11))
T.task(1, "Určete souřadnice bodů A, B, C a D zakreslených v soustavě souřadnic.",
       ", ".join(f"{k}{pt_txt(*v)}" for k, v in body.items()),
       ["Souřadnice čteme jako [x; y]: nejdřív vodorovně od svislé osy, pak svisle od vodorovné osy.",
        "A: 2 doprava, 3 nahoru, tedy A[2; 3]. B: 3 doleva, 1 nahoru, tedy B[−3; 1].",
        "C: 1 doleva, 2 dolů, tedy C[−1; −2]. D: 4 doprava, 3 dolů, tedy D[4; −3]."],
       body == {"A": (2, 3), "B": (-3, 1), "C": (-1, -2), "D": (4, -3)},
       figure=fig, space=2)

jidlo = {"guláš": 35, "těstoviny": 30, "ryba": 15, "saláty": 20}
n_obed = 240
pocty = {k: F(n_obed * v, 100) for k, v in jidlo.items()}
opts = ["8", "30", "48", "72", "168"]
T.task(1, f"Kruhový diagram ukazuje, které jídlo si vybralo {n_obed} žáků ve školní jídelně. Kolik žáků si vybralo těstoviny?", "D",
       ["Těstoviny si vybralo 30 % žáků.", f"30 % z {n_obed} = {n_obed} : 100 · 30 = 2,4 · 30 = 72 žáků.",
        "Číslo 30 je procento, ne počet žáků. Číslo 48 jsou saláty (20 %), 168 žáků si vybralo něco jiného než těstoviny."],
       sum(jidlo.values()) == 100 and pocty["těstoviny"] == 72 and pocty["saláty"] == 48 and n_obed - pocty["těstoviny"] == 168
       and opts[3] == str(int(pocty["těstoviny"])) and n_obed / 30 == 8,
       kind="choice", options=opts,
       figure=pie(list(jidlo.values()), list(jidlo), [f"{v} %" for v in jidlo.values()]), space=2)

T.task(1, "Funkce je dána předpisem y = 2x + 3. a) Vypočtěte y pro x = 5. b) Určete x, pro které je y = 15. "
          "c) Leží bod M[−2; −1] na grafu této funkce?",
       "a) 13; b) x = 6; c) ano",
       ["a) Dosadíme x = 5: y = 2 · 5 + 3 = 13.", "b) Řešíme 2x + 3 = 15, tedy 2x = 12 a x = 6.",
        "c) Dosadíme x = −2: y = 2 · (−2) + 3 = −4 + 3 = −1. Souřadnice y bodu M je −1, bod na grafu leží."],
       2 * 5 + 3 == 13 and (15 - 3) // 2 == 6 and 2 * 6 + 3 == 15 and 2 * (-2) + 3 == -1,
       space=3)

# ---------------------------------------------------------------- Jako u zkoušky
hodiny, teploty = [6, 9, 12, 15, 18], [8, 12, 18, 20, 12]
pt = Plot(3, 21, 0, 24, left=30, right=8, top=18, bottom=26)
T.task(2, "Spojnicový graf ukazuje teplotu venku, která se měřila v 6, 9, 12, 15 a 18 hodin. "
          "a) O kolik stupňů Celsia byla nejvyšší naměřená teplota vyšší než nejnižší? b) Jaká byla průměrná teplota z těchto pěti měření?",
       "a) o 12 °C; b) 14 °C",
       ["Z grafu přečteme teploty: 8 °C, 12 °C, 18 °C, 20 °C, 12 °C.",
        "a) Nejvyšší je 20 °C, nejnižší 8 °C: 20 − 8 = 12 °C.",
        "b) Součet: 8 + 12 + 18 + 20 + 12 = 70. Průměr: 70 : 5 = 14 °C."],
       max(teploty) - min(teploty) == 12 and sum(teploty) == 70 and mean(teploty) == 14 and len(hodiny) == len(teploty),
       figure=line_chart(pt, list(zip(hodiny, teploty)), pt.grid(2, 2, 3, 1, ytitle="teplota (°C)", xtitle="čas (h)", xshow=hodiny)), space=3)

krouzky = {"florbal": 16, "volejbal": 12, "plavání": 8, "atletika": 10, "stolní tenis": 6}
k = krouzky
vyroky = [k["florbal"] - k["volejbal"] == F(k["volejbal"], 3),            # o třetinu víc
          k["atletika"] == 2 * k["stolní tenis"],                          # dvakrát víc
          k["plavání"] * 2 == k["florbal"]]                                # polovina
T.task(2, "Sloupcový graf ukazuje, kolik žáků chodí do jednotlivých sportovních kroužků. Každý žák chodí nejvýše do jednoho kroužku. Platí tato tvrzení?",
       "ANO, NE, ANO",
       ["Z grafu: florbal 16, volejbal 12, plavání 8, atletika 10, stolní tenis 6 žáků.",
        "Florbal má o 4 žáky víc než volejbal. Třetina z 12 je 4, tvrzení platí.",
        "Dvakrát víc než stolní tenis (6) by bylo 12 žáků, atletika jich má 10. Tvrzení neplatí.",
        "Polovina z 16 žáků florbalu je 8, přesně tolik chodí do plavání. Tvrzení platí."],
       vyroky == [True, False, True] and sum(k.values()) == 52,
       kind="yesno",
       options=["Do florbalu chodí o třetinu víc žáků než do volejbalu.",
                "Do atletiky chodí dvakrát víc žáků než do stolního tenisu.",
                "Do plavání chodí polovina počtu žáků z florbalu."],
       figure=bar_chart(list(krouzky), list(krouzky.values()), 18, 2, 1, ytitle="počet žáků"), space=1)

uhly = {"autobus": 144, "pěšky": 90, "auto": 72, "kolo": 54}
n_dojizdi = 120
poc = {a: F(n_dojizdi * u, 360) for a, u in uhly.items()}
vyroky = [poc["autobus"] == 48,
          poc["auto"] - poc["kolo"] == 6,
          poc["pěšky"] == F(n_dojizdi, 3)]
T.task(2, f"Kruhový diagram ukazuje, jak do školy dojíždí {n_dojizdi} žáků. Velikost každé výseče je vyznačena středovým úhlem. Platí tato tvrzení?",
       "ANO, ANO, NE",
       ["Celý kruh je 360° a představuje 120 žáků, 1° tedy odpovídá 120 : 360 = 1/3 žáka.",
        "Autobus: 144° → 144 : 3 = 48 žáků. Tvrzení platí.",
        "Auto: 72° → 24 žáků, kolo: 54° → 18 žáků. Rozdíl je 24 − 18 = 6 žáků. Tvrzení platí.",
        "Pěšky chodí 90° → 30 žáků. Třetina ze 120 žáků je 40, tvrzení neplatí (90° je čtvrtina kruhu)."],
       sum(uhly.values()) == 360 and vyroky == [True, True, False] and poc["pěšky"] == 30,
       kind="yesno",
       options=["Autobusem dojíždí 48 žáků.", "Autem jezdí o 6 žáků víc než na kole.", "Pěšky chodí třetina všech žáků."],
       figure=pie(list(uhly.values()), list(uhly), [f"{u}°" for u in uhly.values()]), space=1)

hodin, ceny = [1, 2, 3, 4], [80, 140, 200, 260]
rozdily = {ceny[i + 1] - ceny[i] for i in range(3)}
vyroky = [rozdily == {80},
          ceny[3] + (ceny[1] - ceny[0]) == 320 and rozdily == {60},
          F(ceny[3], hodin[3]) == 60]
T.task(2, "Tabulka ukazuje, kolik stojí půjčení kola v půjčovně podle počtu hodin. Platí tato tvrzení?",
       "NE, ANO, NE",
       ["Ceny rostou o 140 − 80 = 60, 200 − 140 = 60, 260 − 200 = 60 Kč. Každá další hodina zdraží půjčení o 60 Kč, ne o 80 Kč. Tvrzení neplatí.",
        "Za 5 hodin: 260 + 60 = 320 Kč. Tvrzení platí.",
        "Průměrná cena za hodinu při 4 hodinách: 260 : 4 = 65 Kč, ne 60 Kč. Tvrzení neplatí."],
       vyroky == [False, True, False] and F(ceny[3], hodin[3]) == 65,
       kind="yesno",
       options=["Každá další hodina zdraží půjčení o 80 Kč.", "Za 5 hodin by půjčení stálo 320 Kč.",
                "Při půjčení na 4 hodiny vychází průměrně 60 Kč za hodinu."],
       figure=table_svg(["doba půjčení (h)", "cena (Kč)"], [hodin, ceny]), space=1)

ujeto = [52, 60, 48, 64]
cil = 58
pata = cil * (len(ujeto) + 1) - sum(ujeto)
T.task(2, f"Cyklista ujel za čtyři dny {ujeto[0]} km, {ujeto[1]} km, {ujeto[2]} km a {ujeto[3]} km. "
          f"Kolik kilometrů musí ujet pátý den, aby byl průměr za všech pět dnů {cil} km denně?",
       "66 km",
       ["Součet za pět dnů musí být 5 · 58 = 290 km.", "Za první čtyři dny: 52 + 60 + 48 + 64 = 224 km.",
        "Pátý den: 290 − 224 = 66 km.", "Zkouška: (224 + 66) : 5 = 290 : 5 = 58 km. ✓"],
       pata == 66 and mean(ujeto + [pata]) == cil and sum(ujeto) == 224,
       space=3)

A, B, C = (-5, 1), (-1, 1), (-1, 4)
D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
sirka, vyska = B[0] - A[0], C[1] - B[1]
pl = Plane(-6, 2, -1, 5, 20)
fig = svg(pl.base()
          + ln(pl.X(A[0]), pl.Y(A[1]), pl.X(B[0]), pl.Y(B[1]), INK, 1.6) + ln(pl.X(B[0]), pl.Y(B[1]), pl.X(C[0]), pl.Y(C[1]), INK, 1.6)
          + pl.point(*A, "A", -5, 12) + pl.point(*B, "B", -5, 13) + pl.point(*C, "C", -5, -2))
T.task(2, "Body A, B a C v soustavě souřadnic jsou tři vrcholy obdélníku ABCD. Jedna jednotka na osách odpovídá 1 cm. "
          "Určete souřadnice bodu D a vypočtěte obvod a obsah obdélníku ABCD.",
       f"D{pt_txt(*D)}; obvod 14 cm; obsah 12 cm²",
       ["Z obrázku: A[−5; 1], B[−1; 1], C[−1; 4]. Strana AB je vodorovná, strana BC svislá.",
        "Bod D leží nad bodem A ve výšce bodu C, tedy D[−5; 4].",
        "Délky stran: AB = −1 − (−5) = 4 cm, BC = 4 − 1 = 3 cm.", "Obvod: 2 · (4 + 3) = 14 cm, obsah: 4 · 3 = 12 cm²."],
       D == (-5, 4) and sirka == 4 and vyska == 3 and 2 * (sirka + vyska) == 14 and sirka * vyska == 12
       and D[1] - A[1] == vyska and C[0] - D[0] == sirka and B[0] - A[0] == C[0] - D[0],
       figure=fig, space=3)

mozn = ["y = 5x", "y = 2x + 3", "y = 3x + 2", "y = 3x + 5", "y = 4x + 1"]
fs = [(lambda x: 5 * x), (lambda x: 2 * x + 3), (lambda x: 3 * x + 2), (lambda x: 3 * x + 5), (lambda x: 4 * x + 1)]
dobre = [i for i, f in enumerate(fs) if f(1) == 5 and f(4) == 14]
T.task(2, "Pro lineární funkci y = kx + q platí: pro x = 1 je y = 5 a pro x = 4 je y = 14. Která rovnice vyjadřuje tuto funkci?", "C",
       ["Z rozdílu hodnot určíme k: k = (14 − 5) : (4 − 1) = 9 : 3 = 3.", "Dosadíme x = 1 a y = 5: 5 = 3 · 1 + q, tedy q = 2. Rovnice je y = 3x + 2.",
        "Ostatní možnosti vyhovují nejvýše jednomu bodu: y = 5x, y = 2x + 3 i y = 4x + 1 dají pro x = 1 správně 5, ale pro x = 4 vyjde 20, 11 a 17. Možnost y = 3x + 5 nevyhovuje ani prvnímu bodu (pro x = 1 vyjde 8)."],
       dobre == [2] and [f(4) for f in (fs[0], fs[1], fs[4])] == [20, 11, 17] and fs[3](1) == 8,
       kind="choice", options=mozn, space=2)

# ---------------------------------------------------------------- Náročnější
cas = [(0, 0), (1, 20), (1.5, 20), (2.5, 35), (4, 5)]
rychlosti = [(cas[i + 1][1] - cas[i][1]) / (cas[i + 1][0] - cas[i][0]) for i in range(len(cas) - 1)]
stoji = sum(cas[i + 1][0] - cas[i][0] for i in range(len(cas) - 1) if cas[i + 1][1] == cas[i][1])
vyroky = [stoji == 1, max(y for _, y in cas) == 35, abs(rychlosti[3]) == abs(rychlosti[0])]
pd = Plot(0, 4, 0, 40, left=30, right=10, top=18, bottom=26)
T.task(3, "Graf ukazuje vzdálenost cyklisty od domova podle času od vyjetí. Platí tato tvrzení?",
       "NE, ANO, ANO",
       ["Vodorovná část grafu od 1 h do 1,5 h znamená stání na místě. Cyklista stál půl hodiny, ne hodinu. Tvrzení neplatí.",
        "Nejvyšší bod grafu je v čase 2,5 h a leží ve vzdálenosti 35 km od domova. Tvrzení platí.",
        "První hodina: 20 km za 1 h, tedy 20 km/h. Zpět (od 2,5 h do 4 h) se vzdálenost zmenšila z 35 km na 5 km, to je 30 km za 1,5 h, tedy 20 km/h.",
        "Rychlosti jsou stejné, tvrzení platí."],
       vyroky == [False, True, True] and rychlosti == [20, 0, 15, -20] and stoji == .5,
       kind="yesno",
       options=["Cyklista se cestou zastavil na hodinu.", "Nejdál od domova byl 35 km.",
                "Na zpáteční cestě jel stejnou rychlostí jako v první hodině."],
       figure=line_chart(pd, cas, pd.grid(5, 2, .5, 2, ytitle="vzdálenost od domova (km)", xtitle="čas (h)")), space=1)

PA, PB = (1, -1), (3, 3)
kk = F(PB[1] - PA[1], PB[0] - PA[0])
qq = PA[1] - kk * PA[0]
pl = Plane(-2, 5, -3, 6, 16)
x_lo, x_hi = F(F(-7, 2) - qq, kk), F(6 - qq, kk)
fig = svg(pl.base() + ln(pl.X(float(x_lo)), pl.Y(-3.5), pl.X(float(x_hi)), pl.Y(6), INK, 1.6)
          + pl.point(*PA, "A", 5, 11) + pl.point(*PB, "B", -5, -4))
x15 = (15 - qq) / kk
T.task(3, "Přímka na obrázku je grafem lineární funkce y = kx + q. Body A a B leží v průsečících mřížky. "
          "a) Určete čísla k a q. b) Pro jakou hodnotu x je y = 15?",
       "a) k = 2, q = −3 (y = 2x − 3); b) x = 9",
       ["Z obrázku: A[1; −1], B[3; 3].",
        "k = (3 − (−1)) : (3 − 1) = 4 : 2 = 2.", "Dosadíme bod B do y = 2x + q: 3 = 2 · 3 + q, tedy q = −3. Funkce je y = 2x − 3.",
        "Řešíme 2x − 3 = 15, tedy 2x = 18 a x = 9."],
       kk == 2 and qq == -3 and x15 == 9 and all(kk * x + qq == y for x, y in (PA, PB)) and 2 * 9 - 3 == 15,
       figure=fig, space=3)

d, ch, pd_, pch = 12, 18, 20, 15
prumer = F(d * pd_ + ch * pch, d + ch)
T.task(3, "Ve třídě je 12 dívek a 18 chlapců. Z písemky měly dívky průměrně 20 bodů a chlapci průměrně 15 bodů. Jaký je průměr bodů celé třídy?",
       "17 bodů",
       ["Dívky získaly dohromady 12 · 20 = 240 bodů.", "Chlapci získali dohromady 18 · 15 = 270 bodů.",
        "Celá třída má 12 + 18 = 30 žáků a 240 + 270 = 510 bodů.", "Průměr: 510 : 30 = 17 bodů.",
        "Chybný je průměr 17,5 (průměr čísel 20 a 15): chlapců je víc než dívek, výsledek proto musí být blíž k 15."],
       prumer == 17 and F(pd_ + pch, 2) == F(35, 2) and d * pd_ == 240 and ch * pch == 270,
       space=4)

reseni = []
for a in range(1, 41):
    for b in range(a, 41):
        for c in range(b, 41):
            for dd in range(c, 41):
                e = 40 - a - b - c - dd
                if e < dd:
                    continue
                s = [a, b, c, dd, e]
                if c == 7 and modes(s) == [6] and e == 2 * a and mean(s) == 8 and median(s) == 7:
                    reseni.append(s)
T.task(3, "Pět přirozených čísel má tyto vlastnosti: jejich aritmetický průměr je 8, medián je 7, modus je 6 a největší z nich je "
          "dvakrát větší než nejmenší. Určete všech pět čísel.",
       "6, 6, 7, 9, 12",
       ["Součet čísel je 5 · 8 = 40. Medián je prostřední číslo po seřazení, třetí číslo je tedy 7.",
        "Modus 6 znamená, že se 6 vyskytuje aspoň dvakrát. Protože 6 < 7, jsou dvě šestky nejmenší čísla: 6, 6, 7, …",
        "Největší číslo je 2 · 6 = 12, takže řada je 6, 6, 7, ?, 12.", "Čtvrté číslo: 40 − (6 + 6 + 7 + 12) = 40 − 31 = 9.",
        "Zkouška: 6, 6, 7, 9, 12 má součet 40, medián 7, modus 6 a 12 = 2 · 6. ✓"],
       reseni == [[6, 6, 7, 9, 12]],
       space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
n_jezdi, uhel = 150, 72
kolo = F(n_jezdi * uhel, 360)
opts = ["20", "30", "72", "78", "108"]
T.diagnostic(f"Kruhový diagram ukazuje, jak do školy dojíždí {n_jezdi} žáků. Výseč „kolo“ má středový úhel {uhel}°. Kolik žáků jezdí do školy na kole?", "B",
             ["Celý kruh má 360°, výseč 72° je tedy 72 : 360 = 1/5 kruhu, to je 20 %.", "1/5 ze 150 žáků je 150 : 5 = 30 žáků.",
              "Číslo 72 je úhel, ne počet žáků. Číslo 108 by byla chybná představa „72 % ze 150“, číslo 20 je procento."],
             kolo == 30 and F(uhel, 360) == F(1, 5) and F(150 * 72, 100) == 108 and 150 - 72 == 78 and str(int(kolo)) == opts[1],
             kind="choice", options=opts,
             figure=pie([72, 90, 144, 54], ["kolo", "pěšky", "autobus", "auto"], ["72°", "", "", ""]))

cisla2 = [17, 4, 9, 12, 4, 20, 8, 14]
T.diagnostic(f"Určete aritmetický průměr a medián čísel {', '.join(map(str, cisla2))}.", "průměr 11, medián 10,5",
             ["Součet: 17 + 4 + 9 + 12 + 4 + 20 + 8 + 14 = 88, průměr 88 : 8 = 11.",
              "Seřazená čísla: 4, 4, 8, 9, 12, 14, 17, 20. Čísel je osm, prostřední jsou čtvrté a páté: 9 a 12.",
              "Medián: (9 + 12) : 2 = 10,5."],
             mean(cisla2) == 11 and median(cisla2) == F(21, 2) and sorted(cisla2)[3:5] == [9, 12] and dec(median(cisla2)) == "10,5")

T.save()
