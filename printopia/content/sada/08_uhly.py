#!/usr/bin/env python3
"""Téma 8: Úhly a trojúhelníky (formát v _lib.py, vzor 01_zlomky.py). Úlohy jsou vlastní, ve stylu jednotné přijímací zkoušky.

Obrázky se kreslí ze souřadnic a velikosti úhlů se z nich při sestavení zpětně přepočítají (assert), takže obrázek
odpovídá zadání. Měřítko: 4 jednotky = 1 mm při tisku (obrázek se vejde do 62 × 42 mm = 248 × 168 jednotek)."""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic  # noqa: E402

# ------------------------------------------------------------------ pomůcky pro obrázky
INK = "#1c2230"
SHADE = "#e3e9f7"


def ang(v, p, q):
    """Velikost úhlu PVQ ve stupních (0–180)."""
    d = abs(math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]) - math.atan2(q[1] - v[1], q[0] - v[0]))) % 360
    return 360 - d if d > 180 else d


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def pol(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def same(a, b, tol=1e-6):
    return abs(a - b) < tol


def shoelace(*pts):
    """Obsah mnohoúhelníku ze souřadnic (Gaussův vzorec); funguje i s Fraction."""
    s = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return abs(s) / 2


class Fig:
    """Obrázek v matematických souřadnicích (osa y nahoru)."""

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

    def dot(self, p, r=2.4):
        x, y = self._xy(p)
        self.el.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}" stroke="none"/>')

    def text(self, p, s, size=13, anchor="middle", bold=False):
        x, y = self._xy(p)
        wt = ' font-weight="700"' if bold else ""
        self.el.append(f'<text x="{x}" y="{y}" dy=".35em" text-anchor="{anchor}" font-family="Inter,Arial" font-size="{size}"{wt} fill="{INK}" stroke="none">{s}</text>')

    def vlabel(self, p, s, center, d=11, size=14):
        """Popisek vrcholu mimo obrazec (ve směru od středu)."""
        dx, dy = p[0] - center[0], p[1] - center[1]
        n = math.hypot(dx, dy) or 1
        self.text((p[0] + d * dx / n, p[1] + d * dy / n), s, size=size)

    def angle(self, v, a1, a2, r, label=None, lr=None, size=12):
        """Oblouk úhlu u vrcholu v od směru a1 po směr a2 (proti směru hodin, stupně) a popisek."""
        a2 = a2 + 360 if a2 < a1 else a2
        assert a2 - a1 < 180
        (x1, y1), (x2, y2) = self._xy(pol(v, r, a1)), self._xy(pol(v, r, a2))
        self.el.append(f'<path d="M {x1} {y1} A {r} {r} 0 0 0 {x2} {y2}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        if label:
            self.text(pol(v, lr if lr is not None else r + 12, (a1 + a2) / 2), label, size=size)

    def right(self, v, a1, a2, s=9):
        """Značka pravého úhlu u vrcholu v mezi směry a1 a a2."""
        p1, p2 = pol(v, s, a1), pol(v, s, a2)
        self.polyline([p1, (p1[0] + p2[0] - v[0], p1[1] + p2[1] - v[1]), p2])

    def tick(self, p, q, n=1, s=4.5):
        """Čárky na úsečce PQ: stejně dlouhé strany."""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ux, uy = (q[0] - p[0]) / dist(p, q), (q[1] - p[1]) / dist(p, q)
        for i in range(n):
            o = (i - (n - 1) / 2) * 4
            cx, cy = mx + o * ux, my + o * uy
            self.line((cx - s * uy, cy + s * ux), (cx + s * uy, cy - s * ux), w=1.2)

    def chevron(self, p, deg, s=5):
        """Značka rovnoběžnosti „>“ na přímce se směrem deg."""
        u, nrm = (math.cos(math.radians(deg)), math.sin(math.radians(deg))), (-math.sin(math.radians(deg)), math.cos(math.radians(deg)))
        tip = (p[0] + s * u[0], p[1] + s * u[1])
        self.polyline([(p[0] - s * u[0] + s * nrm[0], p[1] - s * u[1] + s * nrm[1]), tip,
                       (p[0] - s * u[0] - s * nrm[0], p[1] - s * u[1] - s * nrm[1])])

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w / 4:g}mm" height="{self.h / 4:g}mm">'
                + "".join(self.el) + "</svg>")


# ------------------------------------------------------------------ obrázky k úlohám
def obr_protinaji():
    """Dvě přímky p a q: α = 54°, β = 126° (vedlejší), γ = 54° (vrcholový)."""
    f, O, L = Fig(200, 160), (100, 80), 64
    dp, dq = 20, 74
    p1, p2, q1, q2 = pol(O, L, dp), pol(O, L, dp + 180), pol(O, L, dq), pol(O, L, dq + 180)
    assert same(ang(O, p1, q1), 54) and same(ang(O, q1, p2), 126) and same(ang(O, p2, q2), 54) and same(ang(O, q2, p1), 126)
    f.line(p2, p1)
    f.line(q2, q1)
    f.angle(O, dp, dq, 20, "α", 34)
    f.angle(O, dq, dp + 180, 14, "β", 30)
    f.angle(O, dp + 180, dq + 180, 20, "γ", 34)
    f.text(pol(O, L + 11, dp), "p")
    f.text(pol(O, L + 11, dq), "q")
    f.text((O[0] + 11, O[1] - 11), "O", size=12)
    return f.svg(), {"alfa": ang(O, p1, q1), "beta": ang(O, q1, p2), "gama": ang(O, p2, q2)}


def obr_rovnobezky():
    """Rovnoběžky a, b a příčka c: α = 112°, β (střídavý k α) = 112°, γ (vedlejší k β) = 68°."""
    f = Fig(220, 160)
    ya, yb = 118, 58
    P = (118, ya)
    down = 248                      # směr příčky dolů z bodu P: úhel mezi pravou polopřímkou přímky a a příčkou je 112°
    Q = pol(P, (ya - yb) / -math.sin(math.radians(down)), down)
    assert same(Q[1], yb)
    a_alfa = ang(P, (P[0] + 1, P[1]), Q)
    a_beta = ang(Q, (Q[0] - 1, Q[1]), P)
    a_gama = ang(Q, (Q[0] + 1, Q[1]), P)
    assert same(a_alfa, 112) and same(a_beta, 112) and same(a_gama, 68)
    f.line((10, ya), (206, ya))
    f.line((10, yb), (206, yb))
    f.line(pol(P, 30, down + 180), pol(Q, 30, down))
    f.chevron((194, ya), 0)
    f.chevron((194, yb), 0)
    f.angle(P, down, 360, 20, "α", 33)
    f.angle(Q, 68, 180, 16, "β", 31)
    f.angle(Q, 0, 68, 25, "γ", 38)
    f.text((8, ya + 11), "a")
    f.text((8, yb + 11), "b")
    f.text(pol(P, 40, down + 180), "c")
    return f.svg(), {"alfa": a_alfa, "beta": a_beta, "gama": a_gama}


def obr_rovnoramenny():
    """Rovnoramenný trojúhelník ABC se základnou AB, úhel při C = 40°, úhly při základně 70°."""
    f = Fig(150, 160)
    A, B = (35, 18), (115, 18)
    C = (75, 18 + 40 * math.tan(math.radians(70)))
    assert same(ang(C, A, B), 40) and same(ang(A, B, C), 70) and same(ang(B, A, C), 70) and same(dist(A, C), dist(B, C))
    f.poly([A, B, C])
    f.tick(A, C)
    f.tick(B, C)
    f.angle(C, 270 - 20, 270 + 20, 30, "40°", 46, size=11)
    f.angle(A, 0, 70, 22, "α", 37)
    f.angle(B, 110, 180, 22, "β", 37)
    for P, s in ((A, "A"), (B, "B"), (C, "C")):
        f.vlabel(P, s, (75, 70))
    return f.svg(), {"C": ang(C, A, B), "A": ang(A, B, C), "B": ang(B, A, C)}


def obr_rovnobezka_C():
    """Přímka p ∥ AB procházející C; úhly mezi p a stranami 47° a 58°, γ = 75°."""
    f = Fig(204, 160)
    A, B = (20, 22), (170, 22)
    al, be = 47, 58
    AC = dist(A, B) * math.sin(math.radians(be)) / math.sin(math.radians(al + be))
    C = pol(A, AC, al)
    assert same(ang(A, B, C), 47) and same(ang(B, A, C), 58) and same(ang(C, A, B), 75)
    left, right = (6, C[1]), (198, C[1])
    assert same(ang(C, left, A), 47) and same(ang(C, right, B), 58)
    f.poly([A, B, C])
    f.line(left, right)
    f.chevron((165, C[1]), 0)
    f.chevron((95, 22), 0)
    f.angle(C, 180, 180 + 47, 26, "47°", 44, size=11)
    f.angle(C, 360 - 58, 360, 26, "58°", 46, size=11)
    f.angle(C, 180 + 47, 360 - 58, 20, "γ", 31)
    f.angle(A, 0, 47, 24, "α", 40)
    f.angle(B, 180 - 58, 180, 22, "β", 38)
    f.text((200, C[1] + 11), "p")
    for P, s, c in ((A, "A", (95, 60)), (B, "B", (95, 60)), (C, "C", (95, 60))):
        f.vlabel(P, s, c, d=11)
    return f.svg(), {"alfa": ang(A, B, C), "beta": ang(B, A, C), "gama": ang(C, A, B)}


def obr_thales():
    """Kružnice se středem S, průměr AB, C na kružnici, ∠CAB = 35° (středový ∠CSB = 70°)."""
    f = Fig(210, 166)
    S, r = (105, 80), 68
    A, B = (S[0] - r, S[1]), (S[0] + r, S[1])
    C = pol(S, r, 70)
    assert same(ang(C, A, B), 90) and same(ang(A, B, C), 35) and same(ang(B, A, C), 55) and same(ang(S, C, B), 70)
    f.circle(S, r)
    f.line(A, B)
    f.poly([A, B, C], w=1.6)
    f.line(S, C, dash=True, w=1.2)
    f.angle(A, 0, 35, 26, "35°", 46, size=11)
    f.dot(S)
    f.text((S[0] + 1, S[1] - 11), "S", size=12)
    f.vlabel(A, "A", S, d=11)
    f.vlabel(B, "B", S, d=11)
    f.vlabel(C, "C", S, d=11)
    return f.svg(), {"A": A, "B": B, "C": C, "S": S}


def smer(v, p):
    """Směr z bodu v do bodu p ve stupních (0–360)."""
    return math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360


def obr_vyska_teznice():
    """Pravoúhlý trojúhelník ABC (pravý úhel při C), úhel při A 28°, D pata výšky, S střed přepony; ∠DCS = 34°."""
    f = Fig(210, 124)
    A, B = (20, 22), (190, 22)
    C = pol(A, dist(A, B) * math.cos(math.radians(28)), 28)
    D, S = (C[0], 22), ((A[0] + B[0]) / 2, 22)
    assert same(ang(C, A, B), 90) and same(ang(A, B, C), 28) and same(ang(C, D, S), 34) and same(dist(S, C), dist(S, A))
    assert S[0] < D[0]            # S leží mezi A a D, takže úhel DCS = ACD − ACS
    f.poly([A, B, C])
    f.line(C, D, dash=True, w=1.4)
    f.line(C, S, dash=True, w=1.4)
    f.right(C, smer(C, B), smer(C, A), 7)
    f.right(D, 90, 0, 7)
    f.angle(A, 0, 28, 32, "28°", 54, size=11)
    f.angle(C, smer(C, S), smer(C, D), 30, "x", 46, size=12)
    f.vlabel(A, "A", (105, 60))
    f.vlabel(B, "B", (105, 60))
    f.vlabel(C, "C", (105, 60), d=10)
    f.text((D[0] + 3, 9), "D")
    f.text((S[0], 9), "S")
    f.dot(D, 1.8)
    f.dot(S, 1.8)
    return f.svg(), {"C": C, "D": D, "S": S, "A": A, "x": ang(C, D, S)}


def obr_ctverec_trojuhelnik():
    """Čtverec ABCD, uvnitř rovnostranný trojúhelník ABE; ∠DEC = 150°."""
    f = Fig(166, 158)
    a = 118
    A, B, C, D = (24, 14), (24 + a, 14), (24 + a, 14 + a), (24, 14 + a)
    E = (24 + a / 2, 14 + a * math.sqrt(3) / 2)
    assert E[1] < D[1] and same(dist(A, E), a) and same(dist(B, E), a)
    assert same(ang(E, A, B), 60) and same(ang(E, A, D), 75) and same(ang(E, B, C), 75) and same(ang(E, D, C), 150)
    f.poly([A, B, C, D])
    f.poly([A, B, E], w=1.4)
    f.line(E, D, w=1.4)
    f.line(E, C, w=1.4)
    f.angle(E, smer(E, C), smer(E, D), 13, "x", 7, size=11)
    ctr = (A[0] + a / 2, A[1] + a / 2)
    for P, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        f.vlabel(P, t, ctr, d=10)
    f.text((E[0], E[1] - 12), "E", size=12)
    return f.svg(), {"E": ang(E, D, C)}


def obr_vyska_trojuhelnik():
    """Trojúhelník ABC, α = 70°, β = 50°, výška CP; ∠ACP = 20°, ∠PCB = 40°."""
    f = Fig(190, 165)
    A, B = (20, 14), (170, 14)
    AC = dist(A, B) * math.sin(math.radians(50)) / math.sin(math.radians(60))
    C = pol(A, AC, 70)
    P = (C[0], 14)
    assert same(ang(A, B, C), 70) and same(ang(B, A, C), 50) and same(ang(C, A, P), 20) and same(ang(C, P, B), 40) and C[1] < 150
    f.poly([A, B, C])
    f.line(C, P, dash=True, w=1.4)
    f.right(P, 90, 0, 8)
    f.angle(A, 0, 70, 24, "70°", 40, size=11)
    f.angle(B, 130, 180, 24, "50°", 42, size=11)
    f.vlabel(A, "A", (95, 70))
    f.vlabel(B, "B", (95, 70))
    f.vlabel(C, "C", (95, 70), d=10)
    f.text((P[0], 2), "P", size=12)
    f.dot(P, 1.8)
    return f.svg(), {"ACP": ang(C, A, P), "PCB": ang(C, P, B)}


# ------------------------------------------------------------------ téma
T = Topic(8, "uhly", "Úhly a trojúhelníky",
          "Úhly a trojúhelníky se v testu objevují skoro každý rok, ve výpočtových úlohách s obrázkem i v úlohách s výběrem z možností. "
          "Velikosti úhlů se počítají, neměří: obrázek jen ukazuje, co je zadáno.",
          ["Vedlejší úhly dávají dohromady 180°, vrcholové úhly jsou stejně velké. U rovnoběžek jsou souhlasné i střídavé úhly stejné. "
           "Rovnoběžnost smíte použít jen tehdy, když ji zadání říká, a pozor na záměnu souhlasných a střídavých úhlů.",
           "Součet vnitřních úhlů je v trojúhelníku 180° a ve čtyřúhelníku 360°. Vnější úhel trojúhelníku se rovná součtu dvou vnitřních úhlů, "
           "které k němu nepřiléhají.",
           "Rovnoramenný trojúhelník má stejné úhly při základně, rovnostranný má všechny úhly 60°. Stejné strany hledejte i skryté, "
           "například dva poloměry téže kružnice.",
           "Výška je kolmá ke straně a svírá s ní 90°, těžnice vede do středu protější strany. Těžnice rozdělí trojúhelník na dva trojúhelníky "
           "se stejným obsahem, v rovnoramenném trojúhelníku je výška na základnu zároveň těžnicí.",
           "Thaletova věta: z bodu kružnice vidíme průměr AB pod pravým úhlem. Střed kružnice opsané pravoúhlému trojúhelníku leží uprostřed "
           "přepony, kružnice vepsaná má střed v průsečíku os úhlů. Středový úhel je dvakrát větší než obvodový úhel nad stejným obloukem.",
           "Trojúhelník existuje, jen když je každá strana kratší než součet zbývajících dvou (rovnost nestačí). "
           "Při počítání se stupni a minutami pamatujte, že 1° = 60′, ne 100′."])

# ---------------------------------------------------------------- Řešený příklad
x = F(180 - 20, 4)
T.example("V trojúhelníku ABC je úhel β o 20° větší než úhel α a úhel γ je dvakrát větší než úhel α. Vypočtěte velikosti všech tří úhlů.",
          ["Velikost úhlu α označíme x. Pak β = x + 20° a γ = 2x.",
           "Součet úhlů v trojúhelníku je 180°: x + (x + 20°) + 2x = 180°.",
           "4x + 20° = 180°, 4x = 160°, x = 40°.",
           "α = 40°, β = 60°, γ = 80°. Zkouška: 40° + 60° + 80° = 180°."],
          "α = 40°, β = 60°, γ = 80°",
          x == 40 and x + (x + 20) + 2 * x == 180 and (x, x + 20, 2 * x) == (40, 60, 80))

# ---------------------------------------------------------------- Základ
svg, g = obr_protinaji()
beta, gama = 180 - 54, 54
T.task(1, "Přímky p a q se protínají v bodě O. Úhel α má velikost 54°. Vypočtěte velikost úhlu β, který je vedlejší k úhlu α, "
          "a velikost úhlu γ, který je vrcholový k úhlu α.", "β = 126°, γ = 54°",
       ["Vedlejší úhly dávají dohromady 180°: β = 180° − 54° = 126°.",
        "Vrcholové úhly jsou stejně velké: γ = α = 54°.",
        "Kontrola: γ a β jsou také vedlejší, 54° + 126° = 180°."],
       same(g["alfa"], 54) and same(g["beta"], beta) and same(g["gama"], gama) and beta + gama == 180,
       figure=svg, space=2)

svg, g = obr_rovnobezky()
beta, gama = 112, 180 - 112
T.task(1, "Přímky a, b jsou rovnoběžné, přímka c je protíná. Úhel α má velikost 112°. Vypočtěte velikost úhlu β, který je s úhlem α "
          "střídavý, a velikost úhlu γ, který je vedlejší k úhlu β.", "β = 112°, γ = 68°",
       ["Střídavé úhly u rovnoběžek jsou stejné: β = α = 112°.",
        "Vedlejší úhly dávají dohromady 180°: γ = 180° − 112° = 68°.",
        "Kontrola: γ je souhlasný s úhlem vedlejším k α, ten má také 180° − 112° = 68°."],
       same(g["alfa"], 112) and same(g["beta"], beta) and same(g["gama"], gama) and beta + gama == 180,
       figure=svg, space=2)

a3 = 180 - 38 - 52
T.task(1, "Dva úhly trojúhelníku mají velikosti 38° a 52°. Vypočtěte velikost třetího úhlu a rozhodněte, zda je trojúhelník ostroúhlý, "
          "pravoúhlý, nebo tupoúhlý.", "90°, trojúhelník je pravoúhlý",
       ["Součet úhlů v trojúhelníku je 180°: 180° − 38° − 52° = 90°.",
        "Jeden z úhlů je pravý, trojúhelník je proto pravoúhlý."],
       a3 == 90 and 38 + 52 == 90, space=1)

svg, g = obr_rovnoramenny()
zaklad = (180 - 40) / 2
T.task(1, "V rovnoramenném trojúhelníku ABC se základnou AB má úhel při vrcholu C velikost 40°. Vypočtěte velikosti úhlů α a β při základně.",
       "α = β = 70°",
       ["Úhly při základně mají dohromady 180° − 40° = 140°.",
        "V rovnoramenném trojúhelníku jsou oba stejné: 140° : 2 = 70°.",
        "Zkouška: 70° + 70° + 40° = 180°."],
       same(g["C"], 40) and same(g["A"], zaklad) and same(g["B"], zaklad) and zaklad == 70 and 2 * zaklad + 40 == 180,
       figure=svg, space=2)

T.task(1, "Převeďte: a) 2° 15′ na minuty, b) 200′ na stupně a minuty, c) 3,5° na stupně a minuty.",
       "a) 135′, b) 3° 20′, c) 3° 30′",
       ["Platí 1° = 60′.", "a) 2 · 60′ + 15′ = 135′.",
        "b) 200′ : 60′ = 3, zbytek 20′, tedy 3° 20′.", "c) 0,5° = 30′, tedy 3,5° = 3° 30′."],
       2 * 60 + 15 == 135 and divmod(200, 60) == (3, 20) and divmod(F(7, 2) * 60, 60) == (3, 30), space=2)

# ---------------------------------------------------------------- Jako u zkoušky
opts = ["75°", "105°", "110°", "145°", "255°"]
gam = 180 - 35 - 70
vnejsi = 180 - gam
T.task(2, "V trojúhelníku ABC mají úhly při vrcholech A a B velikosti 35° a 70°. Jak velký je vnější úhel při vrcholu C?", "B (105°)",
       ["Vnitřní úhel při vrcholu C: γ = 180° − 35° − 70° = 75°.",
        "Vnější úhel je vedlejší k vnitřnímu: 180° − 75° = 105°.",
        "Rychleji: vnější úhel je součet dvou nepřilehlých vnitřních úhlů, 35° + 70° = 105°.",
        "Chybné možnosti: 75° je vnitřní úhel, 110° = 180° − 70°, 145° = 180° − 35°, 255° = 360° − 105°."],
       vnejsi == 105 == 35 + 70 and [o for o in opts if int(o[:-1]) == vnejsi] == ["105°"] and opts[1] == "105°"
       and 110 == 180 - 70 and 145 == 180 - 35 and 255 == 360 - 105,
       kind="choice", options=opts, space=1)

opts = ["6 cm", "8 cm", "12 cm", "18 cm", "19 cm"]
ok = [o for o in opts if 7 + int(o.split()[0]) > 12 and 12 + 7 > int(o.split()[0]) and 12 + int(o.split()[0]) > 7]
T.task(2, "Dvě strany trojúhelníku mají délky 7 cm a 12 cm. Která z uvedených délek nemůže být délkou třetí strany?", "E (19 cm)",
       ["Třetí strana c musí splnit trojúhelníkovou nerovnost: 7 + c > 12, 12 + c > 7 a 7 + 12 > c.",
        "Z toho c > 5 cm a zároveň c < 19 cm.",
        "Délka 19 cm se rovná součtu 7 + 12, takový trojúhelník by se zploštil na úsečku. Ostatní délky leží mezi 5 cm a 19 cm."],
       [o for o in opts if o not in ok] == ["19 cm"] and opts[4] == "19 cm",
       kind="choice", options=opts, space=1)

dil = F(180, 4 + 5)
T.task(2, "Dva vedlejší úhly jsou v poměru 4 : 5. Vypočtěte jejich velikosti. Uveďte celý postup.", "80° a 100°",
       ["Vedlejší úhly mají dohromady 180°. Poměr 4 : 5 znamená 4 + 5 = 9 stejných dílů.",
        "Jeden díl: 180° : 9 = 20°.",
        "Menší úhel: 4 · 20° = 80°, větší úhel: 5 · 20° = 100°.",
        "Zkouška: 80° + 100° = 180° a 80 : 100 = 4 : 5."],
       dil == 20 and 4 * dil == 80 and 5 * dil == 100 and 4 * dil + 5 * dil == 180, space=4)

x = F(180, 5)
T.task(2, "Úhel při vrcholu rovnoramenného trojúhelníku je třikrát větší než úhel při jeho základně. Vypočtěte velikosti všech tří úhlů "
          "tohoto trojúhelníku. Uveďte celý postup.", "36°, 36°, 108°",
       ["Úhel při základně označíme x, druhý úhel při základně má také x, úhel při vrcholu je 3x.",
        "x + x + 3x = 180°, 5x = 180°, x = 36°.",
        "Úhly mají velikosti 36°, 36° a 3 · 36° = 108°.",
        "Zkouška: 36° + 36° + 108° = 180°."],
       x == 36 and 3 * x == 108 and x + x + 3 * x == 180, space=4)

svg, g = obr_rovnobezka_C()
T.task(2, "Přímka p prochází vrcholem C trojúhelníku ABC a je rovnoběžná se stranou AB. Úhly vyznačené v obrázku mezi přímkou p "
          "a stranami AC a BC mají velikosti 47° a 58°. Vypočtěte velikosti vnitřních úhlů α, β a γ trojúhelníku ABC.", "α = 47°, β = 58°, γ = 75°",
       ["Úhel 47° a úhel α jsou střídavé úhly u rovnoběžek p a AB, proto α = 47°.",
        "Stejně úhel 58° a úhel β jsou střídavé, proto β = 58°.",
        "γ = 180° − 47° − 58° = 75°.",
        "Kontrola: u vrcholu C leží vedle sebe 47°, 75° a 58° na přímce p, dohromady 180°."],
       same(g["alfa"], 47) and same(g["beta"], 58) and same(g["gama"], 180 - 47 - 58) and 47 + 75 + 58 == 180,
       figure=svg, space=3)

# 48° 35′ + 27° 40′; 180° − 124° 18′; 75° 20′ : 2 (vše v minutách)
s_a = (48 * 60 + 35) + (27 * 60 + 40)
s_b = 180 * 60 - (124 * 60 + 18)
s_c = (75 * 60 + 20) // 2
T.task(2, "Vypočtěte a výsledek zapište ve stupních a minutách: a) 48° 35′ + 27° 40′, b) velikost úhlu vedlejšího k úhlu 124° 18′, "
          "c) polovina úhlu 75° 20′.", "a) 76° 15′, b) 55° 42′, c) 37° 40′",
       ["a) 48° + 27° = 75° a 35′ + 40′ = 75′ = 1° 15′, celkem 76° 15′.",
        "b) 180° − 124° 18′ = 179° 60′ − 124° 18′ = 55° 42′.",
        "c) 75° 20′ = 4 520′, polovina je 2 260′ = 37° 40′ (nebo 75° 20′ = 74° 80′, polovina 37° 40′)."],
       divmod(s_a, 60) == (76, 15) and divmod(s_b, 60) == (55, 42) and (75 * 60 + 20) % 2 == 0 and divmod(s_c, 60) == (37, 40)
       and 74 * 60 + 80 == 75 * 60 + 20, space=3)

# yesno: kružnice opsaná/vepsaná, těžnice. Kontrola na konkrétních trojúhelnících (Fraction).
# 1) pravoúhlý (0,0),(6,0),(0,8): střed přepony (3,4) je stejně daleko od všech vrcholů
Sx, Sy = F(3), F(4)
op = {(Sx - x0) ** 2 + (Sy - y0) ** 2 for x0, y0 in ((0, 0), (6, 0), (0, 8))} == {25}
# 2) těžnice trojúhelníku A(0,0), B(8,0), C(2,5) dělí na části o stejném obsahu
A_, B_, C_, S_ = (F(0), F(0)), (F(8), F(0)), (F(2), F(5)), (F(4), F(0))
tez = shoelace(A_, S_, C_) == shoelace(S_, B_, C_) and shoelace(A_, B_, C_) == 20
# 3) pravoúhlý 3-4-5 s vrcholy (0,0),(4,0),(0,3): střed vepsané kružnice (1,1), průsečík výšek je vrchol pravého úhlu (0,0)
vep = (F(1), F(1))
vzd = [abs(vep[1]), abs(vep[0]), abs(3 * vep[0] + 4 * vep[1] - 12) / 5]
T.task(2, "Platí tato tvrzení o trojúhelníku?", "ANO, ANO, NE",
       ["Podle Thaletovy věty leží vrchol pravého úhlu na kružnici s průměrem přepona, střed kružnice opsané je tedy střed přepony. Platí.",
        "Obě části mají stejně dlouhou základnu (těžnice půlí stranu) a stejnou výšku z vrcholu. Platí.",
        "Střed vepsané kružnice leží v průsečíku os úhlů, protože má stejnou vzdálenost od všech stran. "
        "Průsečík výšek tuto vlastnost obecně nemá, například v pravoúhlém trojúhelníku je to vrchol pravého úhlu. Neplatí."],
       op and tez and vzd == [1, 1, 1] and vep != (0, 0), kind="yesno",
       options=["Střed kružnice opsané pravoúhlému trojúhelníku leží uprostřed jeho přepony.",
                "Těžnice rozdělí trojúhelník na dva trojúhelníky se stejným obsahem.",
                "Střed kružnice vepsané trojúhelníku je průsečíkem jeho výšek."], space=1)

# ---------------------------------------------------------------- Náročnější
svg, g = obr_thales()
A_, B_, C_, S_ = g["A"], g["B"], g["C"], g["S"]
st = [same(ang(B_, A_, C_), 65), same(ang(C_, A_, B_), 90), same(ang(S_, C_, B_), 70)]
T.task(3, "Body A, B, C leží na kružnici se středem S, úsečka AB je průměr kružnice. Úhel CAB má velikost 35°. Platí tato tvrzení?",
       "NE, ANO, ANO",
       ["Úhel ACB je pravý podle Thaletovy věty. Platí.",
        "Úhel CBA = 90° − 35° = 55°, ne 65°. Neplatí.",
        "Trojúhelník SAC je rovnoramenný (SA = SC jsou poloměry), úhel ACS = 35° a úhel ASC = 180° − 2 · 35° = 110°.",
        "Úhel CSB je vedlejší k úhlu ASC: 180° − 110° = 70°. Platí. (Středový úhel je dvakrát větší než obvodový 35°.)"],
       st == [False, True, True] and same(ang(B_, A_, C_), 55) and 180 - (180 - 2 * 35) == 70, kind="yesno",
       options=["Úhel CBA má velikost 65°.", "Úhel ACB je pravý.", "Úhel CSB má velikost 70°."], figure=svg, space=1)

hodn = [x for x in range(1, 40) if x + 5 > 9 and 5 + 9 > x and 9 + x > 5]
T.task(3, "Dvě strany trojúhelníku mají délky 5 cm a 9 cm. Délka třetí strany je v centimetrech celé číslo. "
          "Kolik různých délek třetí strany je možných?", "9 délek (od 5 cm do 13 cm)",
       ["Trojúhelníková nerovnost: x + 5 > 9, tedy x > 4, a 5 + 9 > x, tedy x < 14. Nerovnost 9 + x > 5 platí vždy.",
        "Celá čísla větší než 4 a menší než 14 jsou 5, 6, …, 13.",
        "Počet: 13 − 5 + 1 = 9. Délky 4 cm a 14 cm nejsou možné, protože by vznikla úsečka."],
       hodn == list(range(5, 14)) and len(hodn) == 9, space=3)

svg, g = obr_vyska_teznice()
al = 28
acs = al
acd = 90 - al
T.task(3, "V pravoúhlém trojúhelníku ABC s pravým úhlem při vrcholu C má úhel při vrcholu A velikost 28°. Bod D je pata výšky z vrcholu C "
          "na přeponu AB, bod S je střed přepony AB. Vypočtěte velikost úhlu DCS, který je v obrázku označen x.", "34°",
       ["Podle Thaletovy věty leží C na kružnici s průměrem AB a středem S, proto SC = SA.",
        "Trojúhelník ASC je rovnoramenný se základnou AC, takže úhel ACS = úhel CAS = 28°.",
        "V pravoúhlém trojúhelníku ADC je úhel ACD = 90° − 28° = 62°.",
        "Úhel DCS = úhel ACD − úhel ACS = 62° − 28° = 34°."],
       same(g["x"], acd - acs) and acd - acs == 34 and same(ang(g["C"], g["A"], g["S"]), acs) and same(ang(g["C"], g["A"], g["D"]), acd),
       figure=svg, space=3)

svg, g = obr_ctverec_trojuhelnik()
T.task(3, "Ve čtverci ABCD leží rovnostranný trojúhelník ABE (viz obrázek). Vypočtěte velikost úhlu DEC, který je v obrázku označen x.", "150°",
       ["Trojúhelník ABE je rovnostranný, proto AE = AB = AD a úhel BAE = 60°.",
        "Úhel DAE = 90° − 60° = 30° a trojúhelník ADE je rovnoramenný se základnou DE (AD = AE).",
        "Úhel AED = (180° − 30°) : 2 = 75°, ze souměrnosti je i úhel BEC = 75°.",
        "Kolem bodu E je celý úhel 360°: x = 360° − 60° − 75° − 75° = 150°."],
       same(g["E"], 150) and (180 - (90 - 60)) / 2 == 75 and 360 - 60 - 75 - 75 == 150, figure=svg, space=3)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
svg, g = obr_vyska_trojuhelnik()
T.diagnostic("V trojúhelníku ABC má úhel při vrcholu A velikost 70° a úhel při vrcholu B velikost 50°. Bod P je pata výšky z vrcholu C "
             "na stranu AB. Vypočtěte velikosti úhlů ACP a PCB.", "ACP = 20°, PCB = 40°",
             ["Výška je kolmá k AB, trojúhelníky APC a PBC jsou pravoúhlé s pravým úhlem při P.",
              "Úhel ACP = 90° − 70° = 20°.", "Úhel PCB = 90° − 50° = 40°.",
              "Kontrola: úhel ACB = 20° + 40° = 60° = 180° − 70° − 50°."],
             same(g["ACP"], 90 - 70) and same(g["PCB"], 90 - 50) and 20 + 40 == 180 - 70 - 50, figure=svg)

opts = ["ostroúhlý", "pravoúhlý", "tupoúhlý", "rovnoramenný", "rovnostranný"]
dil = F(180, 1 + 2 + 3)
uhly = [dil, 2 * dil, 3 * dil]
T.diagnostic("Vnitřní úhly trojúhelníku jsou v poměru 1 : 2 : 3. Jaký je to trojúhelník?", "B (pravoúhlý)",
             ["1 + 2 + 3 = 6 dílů, jeden díl je 180° : 6 = 30°.",
              "Úhly mají velikosti 30°, 60° a 90°.",
              "Jeden úhel je pravý, trojúhelník je pravoúhlý. Úhly nejsou stejné, takže není rovnoramenný ani rovnostranný."],
             uhly == [30, 60, 90] and sum(uhly) == 180 and max(uhly) == 90 and len(set(uhly)) == 3,
             kind="choice", options=opts)

T.save()
