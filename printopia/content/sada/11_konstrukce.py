#!/usr/bin/env python3
"""Téma 11: Konstrukční úlohy. Papírovou konstrukci nelze ověřit přímo, proto se každá úloha počítá v souřadnicích:
bod C se hledá jako průsečík kružnic a přímek (počet průsečíků = počet řešení), splnění všech podmínek zadání se ověří
a měřitelná kontrola (délka strany, výška, poloměr) se spočítá nezávisle druhým způsobem. Obrázek hotové konstrukce
(`key_figure`, do klíče) se kreslí ze stejných souřadnic. Formát v _lib.py, vzor je 01_zlomky.py."""
import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402

EPS = 1e-9
INK = "#1c2230"


# ------------------------------------------------------------------ geometrie v rovině (body jsou komplexní čísla, 1 = 1 cm)
def P(x, y):
    return complex(x, y)


def cross(a, b):
    return a.real * b.imag - a.imag * b.real


def circ_circ(c1, r1, c2, r2):
    """Průsečíky kružnic (c1; r1) a (c2; r2): 0, 1 nebo 2 body (první leží vlevo od směru c1 → c2)."""
    d = abs(c2 - c1)
    if d < EPS or d > r1 + r2 + EPS or d < abs(r1 - r2) - EPS:
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0.0))
    m = c1 + a * (c2 - c1) / d
    n = 1j * (c2 - c1) / d
    return [m] if h < 1e-7 else [m + h * n, m - h * n]


def line_circ(p, u, c, r):
    """Průsečíky přímky p + t·u (|u| = 1) s kružnicí (c; r)."""
    u = u / abs(u)
    w = p - c
    b = w.real * u.real + w.imag * u.imag
    disc = b * b - (abs(w) ** 2 - r * r)
    if disc < -EPS:
        return []
    if disc < 1e-9:
        return [p - b * u]
    s = math.sqrt(disc)
    return [p + (-b - s) * u, p + (-b + s) * u]


def line_line(p, u, q, v):
    """Průsečík přímek p + s·u a q + t·v."""
    den = cross(u, v)
    assert abs(den) > EPS
    return p + cross(q - p, v) / den * u


def unit(deg):
    return cmath.exp(1j * math.radians(deg))


def angle(a, v, b):
    """Velikost úhlu AVB ve stupních."""
    return math.degrees(abs(cmath.phase((a - v) / (b - v))))


def dist_line(x, a, b):
    return abs(cross(b - a, x - a)) / abs(b - a)


def near(a, b, tol=1e-7):
    return abs(a - b) < tol


def above(*pts):
    """Všechny body leží nad přímkou AB (osa x)."""
    return all(p.imag > EPS for p in pts)


def cm(x) -> str:
    """Délka v cm na milimetry s desetinnou čárkou. Hlídá, aby zaokrouhlení nebylo na hraně (jinak by měření vyšlo jinak)."""
    mm = x * 10
    assert abs((mm % 1) - 0.5) > 0.1, f"zaokrouhlení na hraně: {x}"
    return f"{round(mm) / 10:.1f}".replace(".", ",")


# ------------------------------------------------------------------ obrázek hotové konstrukce (SVG do klíče)
class Fig:
    """Kresba v centimetrech (y nahoru). Měřítko SVG se zvolí tak, aby po zmenšení na 62 × 42 mm měl text 2,8 mm.
    Styly čar: main (výsledek), thin (pomocné úsečky), aux (kružnice, oblouky, přímky), dash (přerušovaně).
    Popisky bodů a délek se umísťují automaticky tam, kde nepřekrývají čáry ani jiné popisky."""
    U = 10

    def __init__(self):
        self.el = []
        self.c = None  # střed kresby, od kterého se popisky raději odsazují směrem ven

    @staticmethod
    def xy(p):
        return (p.real, p.imag) if isinstance(p, complex) else (float(p[0]), float(p[1]))

    def seg(self, p, q, st="main"):
        self.el.append(("l", [self.xy(p), self.xy(q)], st))

    def poly(self, pts, st="main"):
        pts = [self.xy(p) for p in pts]
        self.el.append(("l", pts + [pts[0]], st))

    def arc(self, c, r, a0, a1, st="aux"):
        n = max(6, int(abs(a1 - a0) / 3))
        self.el.append(("l", [self.xy(c + r * unit(a0 + (a1 - a0) * i / n)) for i in range(n + 1)], st))

    def circle(self, c, r, st="aux"):
        self.arc(c, r, 0, 360, st)

    def arc_at(self, c, r, p, span=26, st="aux"):
        """Oblouk kružnice (c; r) kolem bodu p (p leží na kružnici), jako stopa kružítka."""
        a = math.degrees(cmath.phase(p - c))
        self.arc(c, r, a - span / 2, a + span / 2, st)

    def dot(self, p, label=None, d=None):
        """Bod s popiskem; d = pevné odsazení popisku v cm (jinak automaticky)."""
        self.el.append(("d", self.xy(p), label, d))

    def text(self, p, s, anchor="middle"):
        self.el.append(("t", self.xy(p), s, anchor))

    def dim(self, p, q, s, side=0):
        """Popisek délky u úsečky pq; side = 1 vlevo od směru p → q, −1 vpravo, 0 automaticky."""
        self.el.append(("m", self.xy(p), self.xy(q), s, side))

    def rmark(self, v, p1, p2, s=0.4):
        u1, u2 = (p1 - v) / abs(p1 - v), (p2 - v) / abs(p2 - v)
        self.el.append(("l", [self.xy(v + s * u1), self.xy(v + s * (u1 + u2)), self.xy(v + s * u2)], "thin"))

    def amark(self, v, p1, p2, r, s=None):
        a1, a2 = math.degrees(cmath.phase(p1 - v)), math.degrees(cmath.phase(p2 - v))
        if (a2 - a1) % 360 > 180:
            a1, a2 = a2, a1
        a2 = a1 + (a2 - a1) % 360
        self.arc(v, r, a1, a2, "thin")
        if s:
            self.el.append(("a", self.xy(v), r, a1, a2, s))

    # ---- automatické umístění popisků
    def _samples(self):
        pts = []
        for e in self.el:
            if e[0] == "l":
                for (x0, y0), (x1, y1) in zip(e[1], e[1][1:]):
                    n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 0.1))
                    pts += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
            elif e[0] == "d":
                pts += [e[1]] * 6  # bod popisek nepřekrývá
        return pts

    def _resolve(self, k, fs):
        """Převede popisky na pevné polohy při měřítku k (mm na jednotku) a velikosti písma fs (jednotek)."""
        U = self.U
        cx, cy = self.xy(self.c) if self.c is not None else (0.0, 0.0)
        samples = self._samples()
        boxes, out = [], []

        def box(pos, s):
            w, h = 0.58 * fs * len(s) / U, 1.15 * fs / U
            return (pos[0] - w / 2, pos[1] - h / 2, pos[0] + w / 2, pos[1] + h / 2)

        def cost(b, pos, base):
            x0, y0, x1, y1 = b[0] - 0.06, b[1] - 0.06, b[2] + 0.06, b[3] + 0.06
            pen = sum(1 for (x, y) in samples if x0 <= x <= x1 and y0 <= y <= y1)
            for o in boxes:
                if b[0] < o[2] and o[0] < b[2] and b[1] < o[3] and o[1] < b[3]:
                    pen += 40
            return pen + 0.02 * (-math.hypot(pos[0] - cx, pos[1] - cy))

        for e in self.el:
            if e[0] == "l":
                out.append(("l", e[1], e[2]))
            elif e[0] == "d":
                out.append(("d", e[1]))
            elif e[0] == "t":
                out.append(("t", e[1], e[2], e[3], False))
                boxes.append(box(e[1], e[2]))
        for e in self.el:
            if e[0] == "d" and e[2]:
                p, label, d = e[1], e[2], e[3]
                if d is not None:
                    pos = (p[0] + d[0], p[1] + d[1])
                else:
                    best = None
                    for ring in (3.6, 5.0):
                        r = ring / (k * U)
                        for ang in range(0, 360, 30):
                            pos = (p[0] + r * math.cos(math.radians(ang)), p[1] + r * math.sin(math.radians(ang)))
                            c = cost(box(pos, label), pos, p) + (ring - 3.6) * 2
                            if best is None or c < best[0]:
                                best = (c, pos)
                    pos = best[1]
                out.append(("t", pos, label, "middle", True))
                boxes.append(box(pos, label))
        for e in self.el:
            if e[0] == "a":
                v, r, a1, a2, s = e[1], e[2], e[3], e[4], e[5]
                best = None
                for dr in (0.45, 0.8):
                    for da in (0, 10, -10, 20, -20):
                        ang = math.radians((a1 + a2) / 2 + da)
                        pos = (v[0] + (r + dr) * math.cos(ang), v[1] + (r + dr) * math.sin(ang))
                        c = cost(box(pos, s), pos, v) + abs(da) * 0.01 + (dr - 0.45)
                        if best is None or c < best[0]:
                            best = (c, pos)
                out.append(("t", best[1], s, "middle", False))
                boxes.append(box(best[1], s))
        for e in self.el:
            if e[0] == "m":
                p, q, s, side = e[1], e[2], e[3], e[4]
                v = complex(q[0] - p[0], q[1] - p[1])
                n = 1j * v / abs(v)
                best = None
                for t in (0.5, 0.35, 0.65, 0.25, 0.75):
                    for sd in ((1, -1) if side == 0 else (side,)):
                        for ring in (3.3, 4.6, 6.0):
                            r = ring / (k * U)
                            pos = ((p[0] + (q[0] - p[0]) * t) + sd * n.real * r, (p[1] + (q[1] - p[1]) * t) + sd * n.imag * r)
                            mid = (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
                            inside = math.hypot(pos[0] - cx, pos[1] - cy) < math.hypot(mid[0] - cx, mid[1] - cy)
                            c = cost(box(pos, s), pos, p) + abs(t - 0.5) * 1.5 + (ring - 3.3) * 1.0 + (0.6 if inside else 0)
                            if best is None or c < best[0]:
                                best = (c, pos)
                out.append(("t", best[1], s, "middle", False))
                boxes.append(box(best[1], s))
        return out

    def svg(self, single=False) -> str:
        U, fs, k = self.U, 8.0, 0.4
        for _ in range(10):
            xs, ys = [], []
            for e in self._resolve(k, fs):
                if e[0] == "t":
                    w = 0.58 * fs * len(e[2]) / U
                    pts = [(e[1][0] - w / 2, e[1][1] - 0.6 * fs / U), (e[1][0] + w / 2, e[1][1] + 0.6 * fs / U)]
                elif e[0] == "d":
                    pts = [e[1]]
                else:
                    pts = e[1]
                xs += [p[0] for p in pts]
                ys += [p[1] for p in pts]
            x0, x1, y0, y1 = min(xs) - 0.2, max(xs) + 0.2, min(ys) - 0.2, max(ys) + 0.2
            W, H = (x1 - x0) * U, (y1 - y0) * U
            k = min(62 / W, 42 / H)
            fs = 2.8 / k
        widths = {"main": 0.45 / k, "thin": 0.25 / k, "aux": 0.2 / k, "dash": 0.25 / k}
        dash = f"{1.3 / k:.1f} {0.9 / k:.1f}"

        def xy(p):
            return f"{(p[0] - x0) * U:.1f},{(y1 - p[1]) * U:.1f}"

        order = {"aux": 0, "dash": 1, "thin": 2, "main": 3}
        res = self._resolve(k, fs)
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Inter,Arial">']
        for e in sorted([e for e in res if e[0] == "l"], key=lambda e: order[e[2]]):
            st = f'stroke="{INK}" stroke-width="{widths[e[2]]:.2f}" stroke-linejoin="round" stroke-linecap="round"'
            if e[2] in ("aux", "dash"):
                st += ' stroke-opacity=".6"'
            if e[2] == "dash":
                st += f' stroke-dasharray="{dash}"'
            out.append(f'<polyline points="{" ".join(xy(p) for p in e[1])}" fill="none" {st}/>')
        for e in res:
            if e[0] == "d":
                x, y = xy(e[1]).split(",")
                out.append(f'<circle cx="{x}" cy="{y}" r="{0.6 / k:.1f}" fill="{INK}"/>')
        for e in res:
            if e[0] == "t":
                x, y = xy(e[1]).split(",")
                wt = ' font-weight="600"' if e[4] else ""
                out.append(f'<text x="{x}" y="{y}" dy=".35em" text-anchor="middle" font-family="Inter,Arial" font-size="{fs:.1f}"{wt} fill="{INK}">{e[2]}</text>')
        out.append("</svg>")
        s = "".join(out)
        return s.replace('"', "'") if single else s


def pt_labels(f, **pts):
    for name, p in pts.items():
        f.dot(p, name.replace("_", "′"))


def task(level, text, answer, steps, check, fig):
    """Konstrukční úloha: místo na rýsování 8 řádků, obrázek hotové konstrukce jde do klíče (key_figure, jednoduché uvozovky)."""
    T.task(level, text, answer, steps, check, kind="construct", space=8)
    T.data["tasks"][-1]["key_figure"] = fig.svg(single=True)


T = Topic(11, "konstrukce", "Konstrukční úlohy",
          "Konstrukce jsou v testu v úlohách 9 a 10 (5 až 6 bodů z 50), ale úspěšnost je jen kolem 24 % a třetina žáků je vůbec nezkusí. "
          "Přitom stačí několik základních kroků a bodují se i správně sestrojené části.",
          ["Nejdřív náčrt a rozbor (do sešitu): nakreslete hotový útvar odhadem, označte dané prvky a hledejte neznámý bod jako průsečík dvou množin bodů.",
           "Množiny bodů: dané vzdálenosti od bodu je kružnice, dané vzdálenosti od přímky jsou dvě rovnoběžky, stejně vzdálené od A a B jsou na ose úsečky AB, "
           "stejně vzdálené od ramen úhlu na ose úhlu a z bodů Thaletovy kružnice (průměr AB) je úsečka AB vidět pod pravým úhlem.",
           "Osa úsečky: z obou konců oblouky stejného poloměru, větší než polovina úsečky, průsečíky spojit. Osa úhlu: oblouk kolem vrcholu, z jeho průsečíků "
           "s rameny dva oblouky stejného poloměru, průsečík spojit s vrcholem.",
           "Kolmici a rovnoběžku sestrojíte trojúhelníkem s ryskou nebo kružítkem. Úhly 90°, 60°, 45° a 30° lze sestrojit bez úhloměru (osa úsečky, rovnostranný trojúhelník, osa úhlu).",
           "Všechna řešení: kružnice protíná přímku ve dvou, jednom nebo žádném bodě. Najděte všechny průsečíky, ověřte, které vyhovují zadání, a nezapomeňte na souměrný obraz.",
           "U zkoušky se konstrukce obtahuje propiskou a postup se nepíše. Měřte až nakonec, kontrolní délky v klíči jsou zaokrouhlené na milimetry (rozdíl 1 až 2 mm je v pořádku)."])

# ---------------------------------------------------------------- Řešený příklad
A, B = P(0, 0), P(7, 0)
Cs = [c for c in circ_circ(A, 5, B, 4) if c.imag > 0]
C = Cs[0]
v_ex = dist_line(C, A, B)
T.example("Sestrojte trojúhelník ABC, v němž |AB| = 7 cm, |AC| = 5 cm, |BC| = 4 cm a bod C leží nad přímkou AB. Kolik má úloha řešení? Změřte výšku na stranu AB.",
          ["Rozbor (náčrt): bod C je od A vzdálený 5 cm a od B 4 cm, leží tedy na kružnici k (A; 5 cm) a zároveň na kružnici l (B; 4 cm).",
           "Konstrukce: narýsujeme úsečku AB, |AB| = 7 cm. Kružítkem narýsujeme oblouk k (A; 5 cm) a oblouk l (B; 4 cm). Jejich průsečík nad přímkou AB je bod C, spojíme ho s A a B.",
           "Počet řešení: platí trojúhelníková nerovnost (5 + 4 > 7), proto se kružnice protnou ve dvou bodech. Jeden leží nad přímkou AB a druhý pod ní, úloha má 1 řešení.",
           f"Kontrola: výška na stranu AB (vzdálenost bodu C od přímky AB) vychází asi {cm(v_ex)} cm."],
          f"1 řešení, výška ≈ {cm(v_ex)} cm",
          len(circ_circ(A, 5, B, 4)) == 2 and len(Cs) == 1 and near(abs(C - A), 5) and near(abs(C - B), 4)
          and near(v_ex, math.sqrt(5 ** 2 - ((49 + 25 - 16) / 14) ** 2)) and cm(v_ex) == "2,8")

# ================================================================ Základ
# 1. Osa úsečky a bod na ose
A, B = P(0, 0), P(7, 0)
S = (A + B) / 2
bods = line_circ(S, 1j, A, 5)  # osa o: přímka kolmá k AB ve středu S
assert len(bods) == 2
C2, C1 = sorted(bods, key=lambda z: z.imag)
SC = abs(C1 - S)
f = Fig()
f.c = S
f.seg(A, B)
f.seg(S + 1j * -4.9, S + 1j * 5.0, "dash")
for X in circ_circ(A, 4.5, B, 4.5):
    f.arc_at(A, 4.5, X, 22)
    f.arc_at(B, 4.5, X, 22)
f.arc_at(A, 5, C1)
f.arc_at(A, 5, C2)
f.seg(A, C1, "thin")
f.seg(S, C1, "main")
f.seg(A, C2, "thin")
f.seg(S, C2, "main")
f.rmark(S, B, C1)
pt_labels(f, A=A, B=B, S=S, C=C1, C_=C2)
f.text(S + P(0.35, 5.0), "o", "start")
f.dim(A, C1, "5 cm")
f.dim(S, C1, f"{cm(SC)} cm")
f.dim(A, B, "7 cm")
task(1, "Narýsujte úsečku AB délky 7 cm a sestrojte její osu o. Najděte všechny body C, které leží na ose o a mají od bodu A vzdálenost 5 cm. "
        "Kolik takových bodů je? Změřte vzdálenost bodu C od středu S úsečky AB.",
     f"2 body (jeden nad a jeden pod přímkou AB). Kontrola: |SC| ≈ {cm(SC)} cm.",
     ["Rozbor: body stejně vzdálené od A a B leží na ose úsečky AB. Body vzdálené 5 cm od A leží na kružnici k (A; 5 cm). Hledané body jsou průsečíky osy a kružnice.",
      "Narýsujeme úsečku AB, |AB| = 7 cm. Z bodů A a B narýsujeme oblouky o stejném poloměru větším než polovina úsečky (třeba 4,5 cm). Jejich průsečíky spojíme: vznikne osa o a její průsečík s AB je střed S.",
      "Kružítkem narýsujeme kružnici k (A; 5 cm).",
      "Kružnice k protne osu o ve dvou bodech C a C′, protože |AS| = 3,5 cm je menší než poloměr 5 cm. Úloha má 2 řešení.",
      f"Kontrola: v pravoúhlém trojúhelníku ASC je |SC| = √(5² − 3,5²) = √12,75 ≈ {cm(SC)} cm. Také |BC| = |AC| = 5 cm."],
     near(abs(C1 - A), 5) and near(abs(C1 - B), 5) and near(abs(C2 - A), 5) and near(abs(C2 - B), 5) and near(C1.real, 3.5) and near(C2.real, 3.5)
     and near(C1, C2.conjugate()) and near(SC, math.sqrt(12.75)) and cm(SC) == "3,6" and 5 > abs(S - A), f)

# 2. Trojúhelník sss
A, B = P(0, 0), P(6, 0)
sol = circ_circ(A, 5, B, 4.5)
Cs = [c for c in sol if c.imag > 0]
C = Cs[0]
v = C.imag
foot = C.real
f = Fig()
f.c = (A + B + C) / 3
f.poly([A, B, C])
f.arc_at(A, 5, C)
f.arc_at(B, 4.5, C)
f.seg(C, P(foot, 0), "dash")
f.rmark(P(foot, 0), B, C)
pt_labels(f, A=A, B=B, C=C)
f.dim(A, B, "6 cm")
f.dim(B, C, "4,5 cm")
f.dim(C, A, "5 cm")
f.dim(P(foot, 0), C, f"{cm(v)} cm")
task(1, "Narýsujte vodorovnou úsečku AB, |AB| = 6 cm. Sestrojte trojúhelník ABC, v němž |AC| = 5 cm, |BC| = 4,5 cm a bod C leží nad přímkou AB. "
        "Kolik řešení má úloha? Změřte vzdálenost bodu C od přímky AB (výšku na stranu AB).",
     f"1 řešení. Kontrola: výška na stranu AB ≈ {cm(v)} cm.",
     ["Rozbor: bod C je od A vzdálený 5 cm a od B 4,5 cm, leží tedy na kružnici k (A; 5 cm) a na kružnici l (B; 4,5 cm).",
      "Narýsujeme úsečku AB, |AB| = 6 cm. Pak kružítkem narýsujeme oblouky k (A; 5 cm) a l (B; 4,5 cm). Jejich průsečík nad přímkou AB je bod C.",
      "Trojúhelník existuje, protože platí trojúhelníková nerovnost (5 + 4,5 > 6). Kružnice se protnou ve dvou bodech, nad přímkou AB je jen jeden. Úloha má 1 řešení.",
      f"Kontrola: kolmice z bodu C dopadne na AB asi {cm(foot)} cm od bodu A a výška vychází asi {cm(v)} cm."],
     len(sol) == 2 and len(Cs) == 1 and near(abs(C - A), 5) and near(abs(C - B), 4.5) and 5 + 4.5 > 6 and 5 + 6 > 4.5 and 4.5 + 6 > 5
     and near(foot, (36 + 25 - 20.25) / 12) and near(v, dist_line(C, A, B)) and cm(v) == "3,7" and cm(foot) == "3,4", f)

# 3. Osa úhlu 60°
V = P(0, 0)
arm_a = P(7, 0)
arm_b = 7 * unit(60)
Pp = P(4, 0)
Q = 4 * unit(60)
assert near(abs(Q - Pp), 4)  # trojúhelník VPQ je rovnostranný
Rs = [r for r in circ_circ(Pp, 3, Q, 3) if abs(r) > abs(Pp)]
R = Rs[0]
X = 5 * R / abs(R)
assert near(angle(arm_a, V, X), 30) and near(angle(X, V, arm_b), 30) and near(angle(arm_a, V, arm_b), 60)
d1, d2 = dist_line(X, V, arm_a), dist_line(X, V, arm_b)
f = Fig()
f.c = V
f.seg(V, arm_a)
f.seg(V, arm_b)
f.seg(V, 7 * R / abs(R), "dash")
f.arc(V, 4, -4, 64)
f.arc_at(Pp, 3, R, 24)
f.arc_at(Q, 3, R, 24)
f.arc_at(V, 5, X, 20)
f.seg(X, P(X.real, 0), "thin")
f.rmark(P(X.real, 0), V, X)
f.amark(V, arm_a, arm_b, 1.2, "60°")
pt_labels(f, V=V, A=arm_a, B=arm_b, P=Pp, Q=Q, X=X)
f.text(7.4 * R / abs(R) + P(0.1, 0.3), "o")
f.dim(P(X.real, 0), X, f"{cm(d1)} cm")
task(1, "Sestrojte úhel AVB o velikosti 60° (použijte kružítko, ne úhloměr) a jeho osu o. Na ose najděte bod X, který má od vrcholu V vzdálenost 5 cm. "
        "Změřte vzdálenost bodu X od ramene VA (kolmo k rameni).",
     f"1 řešení. Kontrola: bod X je od každého ramene vzdálený {cm(d1)} cm.",
     ["Rozbor: osa úhlu je množina bodů stejně vzdálených od obou ramen. Bod X leží na ose a na kružnici k (V; 5 cm).",
      "Úhel 60°: narýsujeme polopřímku VA a kružnici (V; 4 cm), která ji protne v bodě P. Kružnice (P; 4 cm) protne první kružnici v bodě Q. "
      "Trojúhelník VPQ je rovnostranný, proto má úhel PVQ 60° a polopřímka VQ je druhé rameno.",
      "Osa úhlu: z bodů P a Q narýsujeme oblouky o stejném poloměru (třeba 3 cm), které se protnou v bodě R. Polopřímka VR je osa o a svírá s rameny úhly 30°.",
      "Kružnice k (V; 5 cm) protne polopřímku VR v bodě X. Úloha má 1 řešení.",
      f"Kontrola: v pravoúhlém trojúhelníku s úhlem 30° je odvěsna proti tomuto úhlu poloviční oproti přeponě, tedy 5 : 2 = {cm(d1)} cm. Stejně daleko je X od ramene VB."],
     near(d1, 2.5) and near(d2, 2.5) and near(abs(X), 5) and near(abs(R - Pp), 3) and near(abs(R - Q), 3), f)

# 4. Množiny bodů: vzdálenost od bodu a od přímky
S0 = P(0, 0)
pts4 = [z for yy in (2, -2) for z in line_circ(P(0, yy), 1, S0, 3)]
assert len(pts4) == 4
Xu = [z for z in pts4 if z.imag > 0]
xx = abs(Xu[1] - Xu[0])
f = Fig()
f.c = S0
f.seg(P(-4.6, 0), P(4.6, 0))
f.seg(P(0, -3.8), P(0, 3.8), "dash")
f.seg(P(-4.2, 2), P(4.2, 2), "dash")
f.seg(P(-4.2, -2), P(4.2, -2), "dash")
f.circle(S0, 3)
f.seg(Xu[0], Xu[1], "main")
pt_labels(f, S=S0)
for z in pts4:
    f.dot(z, "X" + ("1" if z.real > 0 and z.imag > 0 else "2" if z.real < 0 and z.imag > 0 else "3" if z.real < 0 else "4"))
f.text(P(4.6, 0.35), "p", "end")
f.dim(Xu[0], Xu[1], f"{cm(xx)} cm")
f.text(P(4.3, 2.0), "r", "start")
f.text(P(4.3, -2.0), "r′", "start")
task(1, "Narýsujte přímku p a na ní bod S. Najděte všechny body X, které mají od bodu S vzdálenost 3 cm a od přímky p vzdálenost 2 cm. "
        "Kolik takových bodů je? Změřte vzdálenost dvou nalezených bodů, které leží na téže rovnoběžce s přímkou p.",
     f"4 body. Kontrola: dva body na téže rovnoběžce s p jsou od sebe ≈ {cm(xx)} cm.",
     ["Rozbor: body vzdálené 3 cm od S leží na kružnici k (S; 3 cm). Body vzdálené 2 cm od přímky p leží na dvou rovnoběžkách s p, jedné v každé polorovině.",
      "Narýsujeme přímku p a bod S. V bodě S sestrojíme kolmici k přímce p a naneseme na ni od S na obě strany 2 cm.",
      "Oběma nanesenými body vedeme rovnoběžky r a r′ s přímkou p.",
      "Narýsujeme kružnici k (S; 3 cm). Každá rovnoběžka je od S vzdálená 2 cm, to je méně než poloměr 3 cm, proto protne kružnici ve dvou bodech. Celkem je 4 body.",
      f"Kontrola: dva body na téže rovnoběžce jsou od sebe 2 · √(3² − 2²) = 2 · √5 ≈ {cm(xx)} cm."],
     all(near(abs(z - S0), 3) and near(abs(z.imag), 2) for z in pts4) and len({round(z.real, 6) + 1j * round(z.imag, 6) for z in pts4}) == 4
     and near(xx, 2 * math.sqrt(5)) and cm(xx) == "4,5", f)

# 5. Rovnoramenný trojúhelník: základna a výška
A, B = P(0, 0), P(6, 0)
S = (A + B) / 2
C = S + 4j
ram = abs(C - A)
f = Fig()
f.c = S
f.poly([A, B, C])
f.seg(S + P(0, -3), S + P(0, 4.8), "dash")
for X in circ_circ(A, 4, B, 4):
    f.arc_at(A, 4, X, 22)
    f.arc_at(B, 4, X, 22)
f.seg(S, C, "thin")
f.rmark(S, B, C)
pt_labels(f, A=A, B=B, C=C)
f.dot(S, "S", (0.25, -0.65))
f.text(P(3.35, 4.95), "o", "start")
f.dim(A, B, "6 cm")
f.dim(S, C, "4 cm")
f.dim(A, C, f"{cm(ram)} cm")
task(1, "Sestrojte rovnoramenný trojúhelník ABC se základnou AB, |AB| = 6 cm, a výškou na základnu 4 cm (bod C leží nad přímkou AB). Změřte délku ramene AC.",
     f"1 řešení. Kontrola: |AC| = |BC| = {cm(ram)} cm.",
     ["Rozbor: v rovnoramenném trojúhelníku leží vrchol C na ose základny AB. Výška na základnu je 4 cm, takže C je na ose ve vzdálenosti 4 cm od AB.",
      "Narýsujeme úsečku AB, |AB| = 6 cm, a její osu o. Střed úsečky AB označíme S.",
      "Na ose o naneseme od bodu S nad přímku AB vzdálenost 4 cm: dostaneme bod C.",
      "Spojíme A s C a B s C. Úloha má 1 řešení.",
      f"Kontrola: |AS| = 3 cm a |SC| = 4 cm, takže |AC| = √(3² + 4²) = {cm(ram)} cm. Totéž platí pro |BC|."],
     near(abs(C - B), abs(C - A)) and near(ram, 5) and near(C.imag, 4) and near(dist_line(C, A, B), 4) and cm(ram) == "5,0", f)

# ================================================================ Jako u zkoušky
# 6. SUS
A, B = P(0, 0), P(6, 0)
C = 5 * unit(50)
BC = abs(C - B)
assert above(C) and near(angle(B, A, C), 50)
f = Fig()
f.c = (A + B + C) / 3
f.poly([A, B, C])
f.arc_at(A, 5, C, 20)
f.seg(A, 5.8 * unit(50), "dash")
f.amark(A, B, C, 1.2, "50°")
pt_labels(f, A=A, B=B, C=C)
f.dim(A, B, "6 cm")
f.dim(A, C, "5 cm")
f.dim(B, C, f"{cm(BC)} cm")
bx, by = round(C.real, 1), round(C.imag, 1)
task(2, "Narýsujte úsečku AB, |AB| = 6 cm. Sestrojte trojúhelník ABC, v němž |AC| = 5 cm, velikost úhlu BAC je 50° a bod C leží nad přímkou AB. "
        "Změřte délku strany BC.",
     f"1 řešení. Kontrola: |BC| ≈ {cm(BC)} cm.",
     ["Rozbor: bod C leží na rameni úhlu BAC (velikost 50°) a na kružnici k (A; 5 cm). Stačí tedy na rameni odměřit od A vzdálenost 5 cm.",
      "Narýsujeme úsečku AB, |AB| = 6 cm. Úhloměrem sestrojíme při bodě A úhel 50° a narýsujeme jeho rameno nad přímkou AB.",
      "Kružítkem narýsujeme kružnici k (A; 5 cm). Její průsečík s ramenem je bod C. Spojíme B s C.",
      "Rameno protne kružnici právě jednou, úloha má 1 řešení.",
      f"Kontrola: bod C leží asi {cm(bx)} cm vpravo od A a {cm(by)} cm nad přímkou AB. Podle Pythagorovy věty je |BC| = √((6 − {cm(bx)})² + {cm(by)}²) ≈ {cm(BC)} cm."],
     near(abs(C - A), 5) and near(angle(B, A, C), 50) and near(BC, math.sqrt(36 + 25 - 60 * math.cos(math.radians(50)))) and cm(BC) == "4,7"
     and len([h for h in line_circ(A, unit(50), A, 5) if ((h - A) * unit(-50)).real > 0]) == 1
     and cm(math.hypot(6 - bx, by)) == cm(BC) and (bx, by) == (3.2, 3.8), f)

# 7. USU
A, B = P(0, 0), P(7, 0)
C = line_line(A, unit(45), B, unit(180 - 60))
AC, BC = abs(C - A), abs(C - B)
gam = angle(A, C, B)
f = Fig()
f.c = (A + B + C) / 3
f.poly([A, B, C])
f.seg(C, C + 0.9 * (C - A) / abs(C - A), "dash")
f.seg(C, C + 0.9 * (C - B) / abs(C - B), "dash")
f.amark(A, B, C, 1.3, "45°")
f.amark(B, C, A, 1.0, "60°")
pt_labels(f, A=A, B=B, C=C)
f.dim(A, B, "7 cm")
f.dim(A, C, f"{cm(AC)} cm")
f.dim(B, C, f"{cm(BC)} cm")
task(2, "Narýsujte úsečku AB, |AB| = 7 cm. Sestrojte trojúhelník ABC, v němž velikost úhlu BAC je 45°, velikost úhlu ABC je 60° a bod C leží nad přímkou AB. "
        "Změřte délky stran AC a BC.",
     f"1 řešení. Kontrola: |AC| ≈ {cm(AC)} cm, |BC| ≈ {cm(BC)} cm.",
     ["Rozbor: bod C leží na rameni úhlu 45° s vrcholem A a zároveň na rameni úhlu 60° s vrcholem B. Je to průsečík těchto dvou polopřímek.",
      "Narýsujeme úsečku AB, |AB| = 7 cm.",
      "Při bodě A sestrojíme nad přímkou AB úhel 45° (úhloměrem nebo jako polovinu pravého úhlu) a při bodě B úhel 60°.",
      "Průsečík volných ramen je bod C. Součet úhlů 45° + 60° je menší než 180°, polopřímky se proto protnou právě jednou. Úloha má 1 řešení.",
      f"Kontrola: úhel při bodě C má 180° − 45° − 60° = 75°. Změřením vyjde |AC| ≈ {cm(AC)} cm a |BC| ≈ {cm(BC)} cm."],
     above(C) and near(angle(B, A, C), 45) and near(angle(A, B, C), 60) and near(gam, 75)
     and near(AC, 7 * math.sin(math.radians(60)) / math.sin(math.radians(75))) and near(BC, 7 * math.sin(math.radians(45)) / math.sin(math.radians(75)))
     and (cm(AC), cm(BC)) == ("6,3", "5,1"), f)

# 8. Čtverec z úhlopříčky
A, Cc = P(0, 0), P(5, 0)
S = (A + Cc) / 2
bd = line_circ(S, 1j, S, 2.5)
assert len(bd) == 2
D, Bq = sorted(bd, key=lambda z: -z.imag)
side = abs(Bq - A)
sq = [A, Bq, Cc, D]
f = Fig()
f.c = S
f.poly(sq)
f.circle(S, 2.5)
f.seg(Bq, D, "thin")
f.seg(A, Cc, "thin")
f.seg(S + P(0, -3.4), S + P(0, 3.4), "dash")
for X in circ_circ(A, 3, Cc, 3):
    f.arc_at(A, 3, X, 20)
    f.arc_at(Cc, 3, X, 20)
f.rmark(S, Cc, D)
pt_labels(f, A=A, B=Bq, C=Cc, D=D)
f.dot(S, "S", (0.3, -0.6))
f.dim(A, Cc, "5 cm")
f.dim(A, Bq, f"{cm(side)} cm")
task(2, "Sestrojte čtverec ABCD, jehož úhlopříčka AC má délku 5 cm. Změřte délku strany čtverce.",
     f"1 řešení (čtverec je určen jednoznačně). Kontrola: strana ≈ {cm(side)} cm.",
     ["Rozbor: úhlopříčky čtverce jsou stejně dlouhé, navzájem kolmé a půlí se. Vrcholy B a D proto leží na ose úhlopříčky AC a jsou od jejího středu S vzdálené 2,5 cm (polovina úhlopříčky).",
      "Narýsujeme úsečku AC, |AC| = 5 cm, její osu a střed S.",
      "Kružnice k (S; 2,5 cm) protne osu ve dvou bodech B a D. (Kružnice prochází i body A a C.)",
      "Spojíme A, B, C, D. Čtverec je určen jednoznačně, úloha má 1 řešení.",
      f"Kontrola: v pravoúhlém trojúhelníku ASB je |SA| = |SB| = 2,5 cm, takže |AB|² = 2,5² + 2,5² = 12,5 a |AB| = √12,5 ≈ {cm(side)} cm."],
     all(near(abs(sq[i] - sq[(i + 1) % 4]), side) for i in range(4)) and near(angle(A, Bq, Cc), 90) and near(abs(D - Bq), 5) and near(side, math.sqrt(12.5))
     and cm(side) == "3,5", f)

# 9. Rovnoběžník
A, B = P(0, 0), P(6, 0)
D = 4 * unit(60)
Cp = line_line(D, 1, B, D - A)  # rovnoběžka s AB bodem D a rovnoběžka s AD bodem B
AC, BD = abs(Cp - A), abs(D - B)
f = Fig()
f.c = (A + B + Cp + D) / 4
f.poly([A, B, Cp, D])
f.seg(D + P(-1.0, 0), Cp + P(1.0, 0), "dash")
f.seg(B - D / abs(D), Cp + D / abs(D), "dash")
f.seg(A, Cp, "thin")
f.seg(B, D, "thin")
f.amark(A, B, D, 1.0, "60°")
pt_labels(f, A=A, B=B, C=Cp, D=D)
f.dim(A, B, "6 cm")
f.dim(D, A, "4 cm")
f.dim(A, Cp, f"{cm(AC)} cm")
f.dim(B, D, f"{cm(BD)} cm")
h9 = D.imag
task(2, "Sestrojte rovnoběžník ABCD, v němž |AB| = 6 cm, |AD| = 4 cm a velikost úhlu DAB je 60°. Změřte délky obou úhlopříček AC a BD.",
     f"1 řešení. Kontrola: |AC| ≈ {cm(AC)} cm, |BD| ≈ {cm(BD)} cm.",
     ["Rozbor: v rovnoběžníku jsou protější strany rovnoběžné a stejně dlouhé. Bod D leží na rameni úhlu 60° ve vzdálenosti 4 cm od A. Bod C je průsečík rovnoběžky s AB vedené bodem D a rovnoběžky s AD vedené bodem B.",
      "Narýsujeme úsečku AB, |AB| = 6 cm, při bodě A úhel 60° a na jeho rameni bod D, |AD| = 4 cm.",
      "Bodem D vedeme rovnoběžku s AB a bodem B rovnoběžku s AD. Jejich průsečík je bod C. Spojíme A, B, C, D. Úloha má 1 řešení.",
      f"Kontrola: bod D je asi {cm(h9)} cm nad přímkou AB a 2 cm vpravo od A. Proto |AC| = √(8² + {cm(h9)}²) ≈ {cm(AC)} cm a |BD| = √(4² + {cm(h9)}²) ≈ {cm(BD)} cm."],
     near(Cp, B + D) and near(abs(Cp - B), 4) and near(abs(Cp - D), 6) and near(AC, math.sqrt(76)) and near(BD, math.sqrt(28))
     and (cm(AC), cm(BD)) == ("8,7", "5,3") and cm(math.hypot(8, float(cm(h9).replace(",", ".")))) == cm(AC)
     and cm(math.hypot(4, float(cm(h9).replace(",", ".")))) == cm(BD), f)

# 10. Pravoúhlý trojúhelník: přepona a výška na přeponu
A, B = P(0, 0), P(10, 0)
S = (A + B) / 2
Cs10 = [z for z in line_circ(P(0, 4.8), 1, S, 5)]
assert len(Cs10) == 2 and above(*Cs10)
Cl, Cr = sorted(Cs10, key=lambda z: z.real)
leg1, leg2 = abs(Cl - A), abs(Cl - B)
f = Fig()
f.c = S
f.circle(S, 5)
f.seg(P(-1, 4.8), P(11, 4.8), "dash")
f.poly([A, B, Cl])
f.poly([A, B, Cr], "thin")
f.seg(Cl, P(Cl.real, 0), "dash")
f.rmark(Cl, A, B)
f.rmark(P(Cl.real, 0), B, Cl, 0.3)
pt_labels(f, A=A, B=B, C=Cl, C_=Cr)
f.dot(S, "S", (0.0, -0.7))
f.dim(A, Cl, f"{cm(leg1)} cm")
f.dim(Cl, B, f"{cm(leg2)} cm")
f.dim(P(Cl.real, 0), Cl, "4,8 cm")
task(2, "Sestrojte všechny pravoúhlé trojúhelníky ABC s přeponou AB, |AB| = 10 cm, a výškou 4,8 cm na přeponu AB, v nichž bod C leží nad přímkou AB. "
        "Kolik řešení má úloha? Změřte délky obou odvěsen.",
     f"2 řešení (shodné trojúhelníky souměrné podle osy úsečky AB). Kontrola: odvěsny {cm(leg1)} cm a {cm(leg2)} cm.",
     ["Rozbor: podle Thaletovy věty leží vrchol pravého úhlu C na kružnici s průměrem AB (Thaletova kružnice). Výška na přeponu je 4,8 cm, takže C leží i na rovnoběžce s AB ve vzdálenosti 4,8 cm.",
      "Narýsujeme úsečku AB, |AB| = 10 cm, její střed S a Thaletovu kružnici k (S; 5 cm).",
      "Sestrojíme rovnoběžku r s AB ve vzdálenosti 4,8 cm nad AB (kolmice k AB v bodě S, na ní 4,8 cm, rovnoběžka).",
      "Rovnoběžka r protne kružnici k ve dvou bodech C a C′, protože 4,8 < 5. Úloha má 2 řešení: trojúhelníky ABC a ABC′ jsou shodné a souměrné podle osy úsečky AB.",
      f"Kontrola: bod C je od S vodorovně √(5² − 4,8²) = √1,96 = 1,4 cm, takže pata výšky je 3,6 cm od A. Odvěsny: √(3,6² + 4,8²) = {cm(leg1)} cm a √(6,4² + 4,8²) = {cm(leg2)} cm."],
     near(angle(A, Cl, B), 90) and near(angle(A, Cr, B), 90) and near(Cl.real, 3.6) and near(Cr.real, 6.4) and near(leg1, 6) and near(leg2, 8) and near(leg1 * leg2 / 10, 4.8)
     and near(abs(Cr - B), leg1) and (cm(leg1), cm(leg2)) == ("6,0", "8,0"), f)

# 11. Tečna kružnice v bodě
S0, r0 = P(0, 0), 3
T0 = P(0, 3)
Xs = line_circ(T0, 1, T0, 4)  # tečna je kolmá k poloměru ST, tedy vodorovná přímka y = 3
assert len(Xs) == 2 and all(near(abs(x - T0), 4) for x in Xs)
XL, XR = sorted(Xs, key=lambda z: z.real)
SX = abs(XR - S0)
f = Fig()
f.c = S0
f.circle(S0, 3)
f.seg(P(-5.2, 3), P(5.2, 3))
f.seg(S0, T0, "thin")
f.seg(S0, XR, "thin")
f.seg(S0, XL, "thin")
f.arc_at(T0, 4, XR, 26)
f.arc_at(T0, 4, XL, 26)
f.rmark(T0, S0, XR)
pt_labels(f, S=S0, T=T0, X=XR, X_=XL)
f.text(P(5.4, 3.35), "t", "end")
f.dim(S0, T0, "3 cm")
f.dim(T0, XR, "4 cm")
f.dim(S0, XR, f"{cm(SX)} cm")
task(2, "Narýsujte kružnici k se středem S a poloměrem 3 cm a na ní libovolný bod T. Sestrojte tečnu t ke kružnici k v bodě T. "
        "Najděte všechny body X na tečně t, které mají od bodu T vzdálenost 4 cm. Kolik takových bodů je? Změřte vzdálenost |SX|.",
     f"2 body. Kontrola: |SX| = |SX′| = {cm(SX)} cm.",
     ["Rozbor: tečna je kolmá na poloměr ST v bodě dotyku T. Hledané body X leží na tečně t a na kružnici l (T; 4 cm).",
      "Narýsujeme kružnici k (S; 3 cm), bod T na ní a polopřímku ST.",
      "Tečna t je kolmice k přímce ST vedená bodem T.",
      "Kružnice l (T; 4 cm) protne tečnu t ve dvou bodech X a X′, po jednom na každé straně od bodu T. Úloha má 2 řešení.",
      f"Kontrola: trojúhelník STX je pravoúhlý s odvěsnami 3 cm a 4 cm, takže |SX| = √(3² + 4²) = {cm(SX)} cm. Totéž platí pro X′."],
     near(abs(XL - S0), SX) and near(SX, 5) and near(dist_line(S0, P(-5, 3), P(5, 3)), r0) and near(abs(T0 - S0), r0) and cm(SX) == "5,0", f)

# 12. Trojúhelník: úhel a výška
A, B = P(0, 0), P(7, 0)
C = line_line(P(0, 4), 1, A, unit(60))
AC, BC = abs(C - A), abs(C - B)
f = Fig()
f.c = (A + B + C) / 3
f.poly([A, B, C])
f.seg(P(-0.8, 4), P(7.8, 4), "dash")
f.seg(A, A + 5.4 * unit(60), "dash")
f.seg(C, P(C.real, 0), "thin")
f.rmark(P(C.real, 0), B, C)
f.amark(A, B, C, 1.3, "60°")
pt_labels(f, A=A, B=B, C=C)
f.text(P(7.9, 4.0), "r", "start")
f.dim(A, B, "7 cm")
f.dim(P(C.real, 0), C, "4 cm")
f.dim(A, C, f"{cm(AC)} cm")
f.dim(B, C, f"{cm(BC)} cm")
cx = round(C.real, 1)
task(2, "Narýsujte úsečku AB, |AB| = 7 cm. Sestrojte trojúhelník ABC, v němž velikost úhlu BAC je 60° a výška na stranu AB je 4 cm (bod C leží nad přímkou AB). "
        "Změřte délky stran AC a BC.",
     f"1 řešení. Kontrola: |AC| ≈ {cm(AC)} cm, |BC| ≈ {cm(BC)} cm.",
     ["Rozbor: výška na stranu AB je 4 cm, takže C leží na rovnoběžce s AB ve vzdálenosti 4 cm nad přímkou AB. Zároveň leží na rameni úhlu 60° s vrcholem A.",
      "Narýsujeme úsečku AB, |AB| = 7 cm, a při bodě A úhel 60°: rameno vedeme nad přímku AB.",
      "Sestrojíme rovnoběžku r s AB ve vzdálenosti 4 cm nad AB (kolmice v bodě A, na ní 4 cm, rovnoběžka).",
      "Průsečík ramene a rovnoběžky r je bod C. Rameno protne rovnoběžku právě jednou, úloha má 1 řešení.",
      f"Kontrola: bod C leží asi {cm(cx)} cm vpravo od A a 4 cm nad přímkou AB. Podle Pythagorovy věty |AC| = √({cm(cx)}² + 4²) ≈ {cm(AC)} cm a "
      f"|BC| = √({cm(7 - cx)}² + 4²) ≈ {cm(BC)} cm."],
     near(C.imag, 4) and near(angle(B, A, C), 60) and near(AC, 8 / math.sqrt(3)) and near(BC, math.sqrt((7 - 4 / math.sqrt(3)) ** 2 + 16))
     and (cm(AC), cm(BC)) == ("4,6", "6,2") and cm(math.hypot(cx, 4)) == cm(AC) and cm(math.hypot(7 - cx, 4)) == cm(BC), f)

# ================================================================ Náročnější
# 13. Ssu: dvě řešení
A, B = P(0, 0), P(8, 0)
u = unit(180 - 30)  # rameno úhlu ABC (30°) nad přímkou AB
hits = line_circ(B, u, A, 5)
assert len(hits) == 2
Cf, Cn = sorted(hits, key=lambda z: -abs(z - B))
assert above(Cf, Cn) and all(near(angle(A, B, z), 30) and near(abs(z - A), 5) for z in hits)
BCf, BCn = abs(Cf - B), abs(Cn - B)
dA = dist_line(A, B, B + u)
pe = math.sqrt(64 - 16)
f = Fig()
f.c = (A + B + Cf) / 3
f.circle(A, 5)
f.seg(B, B + 10.4 * u, "dash")
f.poly([A, B, Cf])
f.seg(A, Cn, "main")
f.amark(B, Cf, A, 1.3, "30°")
pt_labels(f, A=A, B=B, C=Cf, C_=Cn)
f.dim(A, B, "8 cm")
f.dim(B, Cf, f"{cm(BCf)} cm")
f.dim(B, Cn, f"{cm(BCn)} cm")
f.dim(A, Cf, "5 cm")
task(3, "Narýsujte úsečku AB, |AB| = 8 cm. Sestrojte všechny trojúhelníky ABC, v nichž velikost úhlu ABC je 30°, |AC| = 5 cm a bod C leží nad přímkou AB. "
        "Kolik řešení má úloha? U každého řešení změřte délku strany BC.",
     f"2 řešení. Kontrola: |BC| ≈ {cm(BCf)} cm (bod C) a |BC′| ≈ {cm(BCn)} cm (bod C′).",
     ["Rozbor: bod C leží na rameni úhlu 30° s vrcholem B a zároveň na kružnici k (A; 5 cm). Hledáme všechny průsečíky ramene s kružnicí.",
      "Narýsujeme úsečku AB, |AB| = 8 cm. Při bodě B sestrojíme nad přímkou AB úhel 30° (polovina úhlu 60°) a jeho rameno narýsujeme dostatečně dlouhé, aspoň 10 cm.",
      "Narýsujeme kružnici k (A; 5 cm).",
      "Vzdálenost bodu A od ramene je 8 : 2 = 4 cm (v pravoúhlém trojúhelníku s úhlem 30° je protilehlá odvěsna poloviční oproti přeponě). To je méně než 5 cm, proto kružnice protne rameno ve dvou bodech C a C′. Úloha má 2 řešení: trojúhelníky ABC a ABC′.",
      f"Kontrola: pata kolmice z A na rameno je od B vzdálená √(8² − 4²) = √48 ≈ {cm(pe)} cm a polovina tětivy je √(5² − 4²) = 3 cm. Proto |BC| ≈ {cm(pe)} + 3 ≈ {cm(BCf)} cm a |BC′| ≈ {cm(pe)} − 3 ≈ {cm(BCn)} cm."],
     near(dA, 4) and 4 < 5 < 8 and near(BCf, pe + 3) and near(BCn, pe - 3) and (cm(BCf), cm(BCn)) == ("9,9", "3,9")
     and sorted(round(5 * math.sin(math.radians(180 - 30 - cang)) / 0.5, 6) for cang in (math.degrees(math.asin(0.8)), 180 - math.degrees(math.asin(0.8))))
     == sorted([round(BCf, 6), round(BCn, 6)]) and cm(pe + 3) == cm(BCf) and cm(pe - 3) == cm(BCn), f)

# 14. Lichoběžník
A, B = P(0, 0), P(8, 0)
E = P(5, 0)
Ds = [z for z in circ_circ(A, 5, E, 4) if z.imag > 0]
assert len(Ds) == 1
D = Ds[0]
Cl = D + 3
vl = D.imag
AC = abs(Cl - A)
f = Fig()
f.c = (A + B + Cl + D) / 4
f.poly([A, B, Cl, D])
f.seg(D, E, "dash")
f.arc_at(A, 5, D, 22)
f.arc_at(E, 4, D, 22)
f.seg(D, P(D.real, 0), "thin")
f.rmark(P(D.real, 0), B, D, 0.3)
pt_labels(f, A=A, B=B, C=Cl, D=D)
f.dot(E, "E", (0.0, -0.7))
f.dim(A, B, "8 cm")
f.dim(Cl, D, "3 cm")
f.dim(B, Cl, "4 cm")
f.dim(D, A, "5 cm")
f.dim(P(D.real, 0), D, f"{cm(vl)} cm")
task(3, "Sestrojte lichoběžník ABCD se základnami AB a CD, v němž |AB| = 8 cm, |CD| = 3 cm, |BC| = 4 cm, |AD| = 5 cm a body C, D leží nad přímkou AB. "
        "Změřte výšku lichoběžníku.",
     f"1 řešení. Kontrola: výška ≈ {cm(vl)} cm, úhlopříčka |AC| ≈ {cm(AC)} cm.",
     ["Rozbor: bodem D vedeme rovnoběžku s ramenem BC, která protne AB v bodě E. Čtyřúhelník EBCD je rovnoběžník, takže |EB| = |CD| = 3 cm a |DE| = |BC| = 4 cm. "
      "Proto |AE| = 8 − 3 = 5 cm.",
      "Trojúhelník AED má strany |AE| = 5 cm, |AD| = 5 cm a |DE| = 4 cm, můžeme ho sestrojit (sss).",
      "Narýsujeme úsečku AB, |AB| = 8 cm, a na ní bod E, |AE| = 5 cm. Oblouky k (A; 5 cm) a l (E; 4 cm) se protnou nad přímkou AB v bodě D.",
      "Bodem D vedeme rovnoběžku s AB a naneseme na ni od D směrem k B vzdálenost 3 cm: bod C. Spojíme B s C. Úloha má 1 řešení.",
      f"Kontrola: výška lichoběžníku je výška trojúhelníku AED a vychází asi {cm(vl)} cm. Úhlopříčka |AC| vychází asi {cm(AC)} cm."],
     near(abs(D - A), 5) and near(abs(Cl - B), 4) and near(Cl.imag, D.imag) and near(abs(Cl - D), 3) and near(abs(D - E), 4) and near(abs(B - E), 3)
     and near(vl, 2 * math.sqrt(7 * 2 * 2 * 3) / 5) and (cm(vl), cm(AC)) == ("3,7", "7,4"), f)

# 15. Čtyřúhelník z úhlopříčky
A, Cc = P(0, 0), P(7, 0)
Bs = [z for z in circ_circ(A, 6, Cc, 5) if z.imag > 0]
Ds = [z for z in circ_circ(A, 3, Cc, 6) if z.imag < 0]
assert len(Bs) == 1 and len(Ds) == 1 and len(circ_circ(A, 6, Cc, 5)) == 2 and len(circ_circ(A, 3, Cc, 6)) == 2
Bq, D = Bs[0], Ds[0]
BD = abs(Bq - D)
# čtyřúhelník je konvexní: úsečka BD protíná úhlopříčku AC uvnitř
t = Bq.imag / (Bq.imag - D.imag)
xc = (Bq + t * (D - Bq)).real
f = Fig()
f.c = (A + Cc + Bq + D) / 4
f.poly([A, Bq, Cc, D])
f.seg(A, Cc, "thin")
f.seg(Bq, D, "dash")
f.arc_at(A, 6, Bq, 20)
f.arc_at(Cc, 5, Bq, 20)
f.arc_at(A, 3, D, 20)
f.arc_at(Cc, 6, D, 20)
pt_labels(f, A=A, B=Bq, C=Cc, D=D)
f.dim(A, Cc, "7 cm")
f.dim(A, Bq, "6 cm")
f.dim(Bq, Cc, "5 cm")
f.dim(Cc, D, "6 cm")
f.dim(D, A, "3 cm")
f.dim(Bq, D, f"{cm(BD)} cm")
task(3, "Sestrojte čtyřúhelník ABCD, v němž |AB| = 6 cm, |BC| = 5 cm, |CD| = 6 cm, |AD| = 3 cm a úhlopříčka AC má délku 7 cm. "
        "Body B a D leží na opačných stranách přímky AC. Změřte druhou úhlopříčku BD.",
     f"1 řešení. Kontrola: |BD| ≈ {cm(BD)} cm.",
     ["Rozbor: úhlopříčka AC rozdělí čtyřúhelník na trojúhelníky ABC (strany 6, 5 a 7 cm) a ACD (strany 3, 6 a 7 cm). Mají společnou stranu AC, sestrojíme je za sebou.",
      "Narýsujeme úsečku AC, |AC| = 7 cm.",
      "Bod B je průsečík oblouků k (A; 6 cm) a l (C; 5 cm) na jedné straně přímky AC.",
      "Bod D je průsečík oblouků m (A; 3 cm) a n (C; 6 cm) na opačné straně přímky AC.",
      "Spojíme A, B, C, D. Obě trojúhelníkové nerovnosti platí (6 + 5 > 7 a 3 + 6 > 7). Body B a D mají podle zadání ležet na opačných stranách přímky AC, proto má úloha 1 řešení.",
      f"Kontrola: vzdálenost bodů B a D vychází asi {cm(BD)} cm."],
     near(abs(Bq - A), 6) and near(abs(Bq - Cc), 5) and near(abs(D - A), 3) and near(abs(D - Cc), 6) and Bq.imag > 0 > D.imag
     and 0 < xc < 7 and near(BD, math.hypot((36 + 49 - 25) / 14 - (9 + 49 - 36) / 14, math.sqrt(36 - ((36 + 49 - 25) / 14) ** 2) + math.sqrt(9 - ((9 + 49 - 36) / 14) ** 2))) and cm(BD) == "7,3", f)

# 16. Úloha bez řešení
A, B = P(0, 0), P(7, 0)
u = unit(180 - 40)
hits = line_circ(B, u, A, 3)
dd = dist_line(A, B, B + u)
foot_pt = B + u * ((A - B).real * u.real + (A - B).imag * u.imag)
f = Fig()
f.c = P(3.5, 1.5)
f.circle(A, 3)
f.seg(A, B)
f.seg(B, B + 7.5 * u, "main")
f.seg(A, foot_pt, "dash")
f.rmark(foot_pt, A, B, 0.4)
f.amark(B, A, B + u, 1.2, "40°")
pt_labels(f, A=A, B=B)
f.dim(A, B, "7 cm")
f.dim(A, foot_pt, f"{cm(dd)} cm")
f.text(A + P(1.55, 1.0), "k", "middle")
task(3, "Rozhodněte, zda existuje trojúhelník ABC, v němž |AB| = 7 cm, velikost úhlu ABC je 40° a |AC| = 3 cm (bod C leží nad přímkou AB). "
        "Pokud existuje, sestrojte ho. Pokud ne, zdůvodněte to změřením vzdálenosti bodu A od ramene úhlu.",
     f"0 řešení: trojúhelník neexistuje. Kontrola: vzdálenost bodu A od přímky BC je ≈ {cm(dd)} cm, což je víc než 3 cm.",
     ["Rozbor: bod C by musel ležet na rameni úhlu 40° s vrcholem B a na kružnici k (A; 3 cm). Řešení existuje jen tehdy, když kružnice rameno protne.",
      "Narýsujeme úsečku AB, |AB| = 7 cm, při bodě B nad přímkou AB úhel 40° (úhloměrem) a jeho rameno. Narýsujeme kružnici k (A; 3 cm).",
      "Z bodu A spustíme kolmici na přímku BC a změříme její délku. Vyjde asi 4,5 cm.",
      "Nejbližší bod přímky BC je od A vzdálený 4,5 cm, tedy víc než poloměr 3 cm. Kružnice k přímku BC vůbec neprotne, úloha má 0 řešení.",
      f"Kontrola pro rodiče: výpočet 7 · sin 40° ≈ {cm(dd)} cm měření potvrzuje (sinus se u zkoušky nepočítá, k řešení ho žák nepotřebuje)."],
     hits == [] and near(dd, 7 * math.sin(math.radians(40))) and cm(dd) == "4,5" and dd > 3 and near(abs(foot_pt - A), dd), f)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
A, B = P(0, 0), P(7, 0)
S = (A + B) / 2
samples = [S, S + 2j, S - 3j, P(1, 0), S + 3.5 * unit(30), P(0, 7)]  # dva body osy, střed, bod přímky AB, bod Thaletovy kružnice, bod kružnice kolem A
equid = [near(abs(p - A), abs(p - B)) for p in samples]
moznosti = {
    "jen střed úsečky AB": lambda p: near(p, S),
    "body přímky AB": lambda p: abs(p.imag) < EPS,
    "body osy úsečky AB": lambda p: abs(p.real - 3.5) < EPS,
    "body kružnice s průměrem AB": lambda p: abs(abs(p - S) - 3.5) < EPS,
    "body kružnice se středem A a poloměrem |AB|": lambda p: abs(abs(p - A) - 7) < EPS,
}
# možnost je správná, jen když popisuje přesně ty body, které jsou stejně vzdálené od A a B
spravne = [k for k, pred in moznosti.items() if [pred(p) for p in samples] == equid]
T.diagnostic("Které body mají od dvou různých bodů A a B stejnou vzdálenost?", "C",
             ["Body stejně vzdálené od A a B tvoří osu úsečky AB: kolmici k AB vedenou jejím středem.",
              "Střed úsečky AB je jen jeden z těchto bodů. Přímka AB, Thaletova kružnice a kružnice kolem A obsahují body, které od A a B stejně daleko nejsou."],
             spravne == ["body osy úsečky AB"], kind="choice", options=list(moznosti))
S0 = P(5, 0)
Cts = circ_circ(S0, 5, P(0, 0), 6)
assert len(Cts) == 2
bcs = [abs(c - P(10, 0)) for c in Cts]
T.diagnostic("Bod C leží na kružnici s průměrem AB, |AB| = 10 cm, a platí |AC| = 6 cm. Jak dlouhá je strana BC?", "8 cm",
             ["Podle Thaletovy věty je úhel ACB pravý, trojúhelník ABC je pravoúhlý s přeponou AB.",
              "Pythagorova věta: |BC|² = 10² − 6² = 100 − 36 = 64, tedy |BC| = 8 cm."],
             all(near(b, 8) and near(angle(P(0, 0), c, P(10, 0)), 90) for b, c in zip(bcs, Cts)))

T.save()
