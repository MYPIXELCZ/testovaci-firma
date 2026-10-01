#!/usr/bin/env python3
"""Téma 6: Poměr a úměrnost. Vlastní úlohy ve stylu jednotné přijímací zkoušky (formát v _lib.py, vzor 01_zlomky.py)."""
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, dec  # noqa: E402


def cz(x) -> str:
    """Číslo pro odpověď: celé s mezerou v tisících („12 500“), jinak desetinné s čárkou."""
    x = F(x)
    if x.denominator == 1:
        return f"{x.numerator:,}".replace(",", " ").replace("-", "−")
    return dec(x, 4)


T = Topic(6, "umernost", "Poměr a úměrnost",
          "Poměr, úměrnost, pohyb a společná práce se v testu objevují ve většině ročníků, často jako krátká úloha "
          "na začátku nebo uvnitř slovní úlohy. Základem je poznat, zda se veličiny mění stejným směrem (přímá úměrnost), "
          "nebo opačným (nepřímá úměrnost).",
          ["Poměr 3 : 5 se krátí a rozšiřuje jako zlomek (6 : 10 je totéž). Při dělení v poměru 3 : 5 sečtěte díly (3 + 5 = 8), "
           "spočítejte jeden díl a vynásobte. Stejně se počítají směsi: poměr 2 : 3 znamená 2 díly jedné složky a 3 díly druhé.",
           "Přímá úměrnost: kolikrát víc, tolikrát víc (víc kilogramů, vyšší cena). Nepřímá úměrnost: kolikrát víc, tolikrát méně "
           "(víc pracovníků, méně dní). Před počítáním se vždy zeptejte, jestli se veličiny mění stejným, nebo opačným směrem.",
           "Trojčlenka: nejdřív spočítejte hodnotu pro jednu jednotku (1 kg, 1 pracovník), pak pro požadované množství. "
           "U nepřímé úměrnosti zůstává stálý součin, např. počet pracovníků · počet dní.",
           "Měřítko 1 : 50 000 znamená, že 1 cm na mapě je 50 000 cm = 500 m ve skutečnosti. Převádějte jednotky: 1 km = 100 000 cm. "
           "Délky se násobí měřítkem, obsahy jeho druhou mocninou.",
           "Rychlost = dráha : čas, dráha = rychlost · čas. Hlídejte jednotky: minuty převeďte na hodiny (45 min = 3/4 h). "
           "Rychlost v km/h převedete na m/s dělením 3,6, opačně násobením 3,6. "
           "Průměrná rychlost je celková dráha dělená celkovým časem, ne průměr dvou rychlostí.",
           "Společná práce: když první pracovník udělá celou práci za 6 hodin a druhý za 3 hodiny, udělají za hodinu 1/6 a 1/3 práce, "
           "společně 1/6 + 1/3 = 1/2. Celá práce je 1, takže jim zabere 1 : 1/2 = 2 hodiny."])

# ---------------------------------------------------------------- Řešený příklad
d_cm = 14 * 25000
d_km = F(d_cm, 100000)
t_h = d_km / 5
T.example("Na mapě v měřítku 1 : 25 000 je trasa dlouhá 14 cm. Turista jde stálou rychlostí 5 km/h. "
          "Za jak dlouho trasu ujde? Výsledek zapište v minutách.",
          ["Skutečná délka trasy: 14 cm · 25 000 = 350 000 cm.",
           "Převod: 1 km = 100 000 cm, takže 350 000 cm = 3,5 km.",
           "Čas = dráha : rychlost = 3,5 : 5 = 0,7 h.", "0,7 h = 0,7 · 60 = 42 minut."],
          "42 minut",
          d_cm == 350000 and d_km == F(7, 2) and t_h == F(7, 10) and t_h * 60 == 42)

# ---------------------------------------------------------------- Základ
a, b = 45, 150
g = gcd(a, b)
T.task(1, "Zapište v základním tvaru poměr 45 cm : 1,5 m.", f"{a // g} : {b // g}",
       ["Obě délky převedeme na stejnou jednotku: 1,5 m = 150 cm, poměr je 45 : 150.",
        "Zkrátíme společným dělitelem 15: 45 : 150 = 3 : 10."],
       g == 15 and (a // g, b // g) == (3, 10) and gcd(3, 10) == 1 and F(45, 150) == F(3, 10), space=2)

dil = F(1200, 3 + 5)
T.task(1, "Dva brigádníci si rozdělí odměnu 1 200 Kč v poměru odpracovaných hodin 3 : 5. Kolik korun dostane každý?",
       f"{cz(3 * dil)} Kč a {cz(5 * dil)} Kč",
       ["Dílů je dohromady 3 + 5 = 8.", "Jeden díl je 1 200 : 8 = 150 Kč.",
        "První dostane 3 · 150 = 450 Kč, druhý 5 · 150 = 750 Kč.", "Zkouška: 450 + 750 = 1 200 Kč. ✓"],
       dil == 150 and 3 * dil == 450 and 5 * dil == 750 and 3 * dil + 5 * dil == 1200 and F(450, 750) == F(3, 5), space=2)

cena_kg = F(108, 4)
r = cena_kg * 7
T.task(1, "Za 4 kg jablek zaplatíme 108 Kč. Kolik korun zaplatíme za 7 kg stejných jablek?", f"{cz(r)} Kč",
       ["Cena je přímo úměrná hmotnosti (víc kilogramů, vyšší cena).", "Cena za 1 kg: 108 : 4 = 27 Kč.", "Za 7 kg: 7 · 27 = 189 Kč."],
       cena_kg == 27 and r == 189 and F(108, 4) == F(189, 7), space=2)

r = 24 * (2 + F(1, 2))
T.task(1, "Cyklista jede stálou rychlostí 24 km/h. Jakou vzdálenost ujede za 2 hodiny a 30 minut?", f"{cz(r)} km",
       ["30 minut je 1/2 hodiny, doba jízdy je tedy 2 1/2 h = 5/2 h.", "Dráha = rychlost · čas = 24 · 5/2 = 60 km.",
        "Jinak: za 2 h ujede 48 km, za 30 min 12 km, dohromady 60 km."],
       r == 60 and 24 * 2 + 24 * F(1, 2) == 60 and 2 + F(1, 2) == F(5, 2), space=2)

opts = {"0,5 m/s": F(1, 2), "5 m/s": F(5), "18 m/s": F(18), "50 m/s": F(50), "64,8 m/s": F(648, 10)}
ms = F(18 * 1000, 3600)
T.task(1, "Kolik metrů za sekundu odpovídá rychlosti 18 km/h?", "B",
       ["1 km = 1 000 m a 1 h = 3 600 s.", "18 km/h = 18 000 m : 3 600 s = 5 m/s.",
        "Zkratka: rychlost v km/h dělíme 3,6 (18 : 3,6 = 5), opačně m/s násobíme 3,6.",
        "Možnost 64,8 vznikne násobením 3,6 místo dělení."],
       ms == 5 and [k for k, v in opts.items() if v == ms] == ["5 m/s"] and F(18) / F(36, 10) == 5 and F(18) * F(36, 10) == F(648, 10),
       kind="choice", options=list(opts), space=2)

# ---------------------------------------------------------------- Jako u zkoušky
opts = {"3 dny": F(3), "6 dní": F(6), "7 dní": F(7), "13,5 dne": F(27, 2), "36 dní": F(36)}
dni = F(4 * 9, 6)
T.task(2, "Čtyři dělníci vykopou stejným tempem příkop za 9 dní. Za kolik dní ho vykopá šest dělníků?", "B",
       ["Víc dělníků udělá práci rychleji, jde o nepřímou úměrnost: počet dělníků · počet dní zůstává stálý.",
        "4 · 9 = 36, jeden dělník by příkop kopal 36 dní.", "Šest dělníků: 36 : 6 = 6 dní.",
        "Chyby: 13,5 dne vznikne přímou úměrou (9 · 6 : 4), 36 dní je součin bez dělení, 3 dny a 7 dní odčítání dní od 9."],
       dni == 6 and [k for k, v in opts.items() if v == dni] == ["6 dní"] and F(9 * 6, 4) == F(27, 2) and 4 * 9 == 36
       and 9 - 6 == 3 and 9 - 2 == 7, kind="choice", options=list(opts), space=3)

dil = F(60, 3 + 4 + 5)
st = [3 * dil, 4 * dil, 5 * dil]
T.task(2, "Obvod trojúhelníku je 60 cm. Délky jeho stran jsou v poměru 3 : 4 : 5. Určete délky všech tří stran.",
       ", ".join(f"{cz(s)} cm" for s in st),
       ["Dílů je dohromady 3 + 4 + 5 = 12.", "Jeden díl je 60 : 12 = 5 cm.",
        "Strany: 3 · 5 = 15 cm, 4 · 5 = 20 cm, 5 · 5 = 25 cm.", "Zkouška: 15 + 20 + 25 = 60 cm. ✓"],
       dil == 5 and st == [15, 20, 25] and sum(st) == 60 and st[0] + st[1] > st[2], space=3)

cas = (12 * 60 + 10) - (9 * 60 + 40)
v = F(30) / F(cas, 60)
T.task(2, "Cyklista vyjel v 9:40 a do cíle vzdáleného 30 km dojel ve 12:10. Jakou stálou rychlostí jel?", f"{cz(v)} km/h",
       ["Doba jízdy: od 9:40 do 10:00 je 20 minut, od 10:00 do 12:00 jsou 2 hodiny a do 12:10 ještě 10 minut. "
        "Celkem 20 + 120 + 10 = 150 minut = 2 hodiny 30 minut.",
        "2 h 30 min = 2 1/2 h = 5/2 h.", "Rychlost = dráha : čas = 30 : 5/2 = 30 · 2/5 = 12 km/h.",
        "Zkouška: 12 km/h · 5/2 h = 30 km. ✓"],
       cas == 150 and F(cas, 60) == F(5, 2) and v == 12 and v * F(5, 2) == 30, space=3)

stmts = [F(12, 18) == F(2, 3), F(5 * 12, 10) == 24, 60 * F(20, 60) == 20]
T.task(2, "Platí tato tvrzení?", "ANO, NE, ANO",
       ["12 : 18 = 2 : 3, protože obě čísla vydělíme šesti. Tvrzení platí.",
        "Pracovníků je dvakrát víc, práce potrvá dvakrát kratší dobu: 12 : 2 = 6 dní, ne 24. Jde o nepřímou úměrnost. Tvrzení neplatí.",
        "20 minut je 1/3 hodiny a 60 · 1/3 = 20 km. Tvrzení platí."],
       stmts == [True, False, True] and F(5 * 12, 10) == 6, kind="yesno",
       options=["Poměr 12 : 18 je stejný jako poměr 2 : 3.",
                "Když 5 pracovníků dokončí práci za 12 dní, pak 10 pracovníků ji (stejným tempem) dokončí za 24 dní.",
                "Auto jedoucí stálou rychlostí 60 km/h ujede za 20 minut 20 km."], space=3)

za_den = F(1, 10) + F(1, 15)
dni = 1 / za_den
T.task(2, "Jeden pracovník vymaluje byt za 10 dní, druhý za 15 dní. Za kolik dní ho vymalují společně?", f"za {cz(dni)} dní",
       ["První vymaluje za den 1/10 bytu, druhý 1/15 bytu.", "Společně za den: 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 bytu.",
        "Celý byt (to je 1) vymalují za 1 : 1/6 = 6 dní.",
        "Pozor: čas není průměr časů, (10 + 15) : 2 = 12,5 dne by vyšlo víc než 10 dní, za které byt zvládne sám rychlejší pracovník."],
       za_den == F(1, 6) and dni == 6 and F(3, 30) + F(2, 30) == F(1, 6) and dni < 10, space=3)

dil = F(45, 1 + 4)
T.task(2, "Suchá zdicí směs se míchá z cementu a písku v poměru 1 : 4 (podle hmotnosti). "
          "Kolik kilogramů cementu a kolik kilogramů písku je třeba na 45 kg směsi?",
       f"{cz(dil)} kg cementu a {cz(4 * dil)} kg písku",
       ["Dílů je dohromady 1 + 4 = 5.", "Jeden díl je 45 : 5 = 9 kg.",
        "Cement tvoří 1 díl, tedy 9 kg, písek 4 díly, tedy 4 · 9 = 36 kg.", "Zkouška: 9 + 36 = 45 kg a 9 : 36 = 1 : 4. ✓"],
       dil == 9 and 4 * dil == 36 and dil + 4 * dil == 45 and F(9, 36) == F(1, 4), space=3)

sirka, vyska = 8 * 500, 5 * 500
plocha = F(sirka, 100) * F(vyska, 100)
T.task(2, "Pozemek je na plánu v měřítku 1 : 500 nakreslen jako obdélník s rozměry 8 cm a 5 cm. "
          "Jaký je jeho skutečný obsah v metrech čtverečních?", f"{cz(plocha)} m²",
       ["Skutečné rozměry: 8 cm · 500 = 4 000 cm = 40 m a 5 cm · 500 = 2 500 cm = 25 m.", "Obsah: 40 · 25 = 1 000 m².",
        "Pozor: obsah na plánu (8 · 5 = 40 cm²) se nenásobí 500, ale 500² = 250 000: "
        "40 · 250 000 = 10 000 000 cm² = 1 000 m² (1 m² = 10 000 cm²)."],
       sirka == 4000 and vyska == 2500 and plocha == 1000 and 8 * 5 * 500 ** 2 == 10_000_000
       and F(10_000_000, 10_000) == plocha, space=3)

# ---------------------------------------------------------------- Náročnější
prvni, druhy = F(1, 12), F(1, 4)
hotovo = prvni * 2
zbyva = 1 - hotovo
spolu = prvni + druhy
t_spolu = zbyva / spolu
celkem = 2 + t_spolu
T.task(3, "První pracovník vyklidí sklep za 12 hodin, druhý za 4 hodiny. Prvních 2 hodiny pracuje sám první pracovník, "
          "potom se přidá druhý. Za kolik hodin od začátku bude sklep vyklizený?", f"za {cz(celkem)} hodiny (4 hodiny 30 minut)",
       ["První vyklidí za hodinu 1/12 sklepa, druhý 1/4 sklepa.",
        "Za první 2 hodiny sám vyklidí 2 · 1/12 = 1/6 sklepa, zbývá 1 − 1/6 = 5/6.",
        "Společně vyklidí za hodinu 1/12 + 1/4 = 1/12 + 3/12 = 4/12 = 1/3 sklepa.",
        "Zbylých 5/6 vyklidí za 5/6 : 1/3 = 5/6 · 3 = 5/2 h = 2,5 h.",
        "Celkem 2 + 2,5 = 4,5 h, tedy 4 hodiny 30 minut."],
       hotovo == F(1, 6) and zbyva == F(5, 6) and spolu == F(1, 3) and t_spolu == F(5, 2) and celkem == F(9, 2)
       and F(9, 2) * 60 == 270, space=5)

prumery = {d: F(2 * d) / (F(d, 20) + F(d, 30)) for d in (1, 7, 60)}
T.task(3, "Cyklista jel z města A do města B rychlostí 20 km/h a zpátky po téže cestě rychlostí 30 km/h. "
          "Jaká byla jeho průměrná rychlost na celé cestě tam a zpět?", f"{cz(prumery[60])} km/h",
       ["Délka cesty není zadaná, zvolíme ji: 60 km (společný násobek čísel 20 a 30).",
        "Tam: 60 : 20 = 3 h, zpět: 60 : 30 = 2 h, celkem 5 h.",
        "Celá dráha je 2 · 60 = 120 km, průměrná rychlost 120 : 5 = 24 km/h.",
        "Průměr rychlostí (20 + 30) : 2 = 25 km/h je špatně: cyklista jel déle pomaleji, proto vychází méně."],
       all(p == 24 for p in prumery.values()) and F(60, 20) + F(60, 30) == 5 and F(20 + 30, 2) == 25 != 24, space=4)

nasko = 15 * 1
priblizovani = 45 - 15
t = F(nasko, priblizovani)
T.task(3, "V 8:00 vyjel z místa A cyklista rychlostí 15 km/h. V 9:00 vyjel za ním stejnou cestou motorkář rychlostí 45 km/h. "
          "V kolik hodin a v jaké vzdálenosti od místa A motorkář cyklistu dohoní?", f"v 9:30, {cz(45 * t)} km od místa A",
       ["V 9:00 je cyklista hodinu na cestě, tedy 15 · 1 = 15 km od místa A.",
        "Motorkář se k němu přibližuje rychlostí 45 − 15 = 30 km/h.",
        "Náskok 15 km dožene za 15 : 30 = 1/2 h, tedy v 9:30.",
        "Vzdálenost od A: motorkář 45 · 1/2 = 22,5 km. Zkouška: cyklista za 1,5 h urazil 15 · 1,5 = 22,5 km. ✓"],
       nasko == 15 and priblizovani == 30 and t == F(1, 2) and 45 * t == F(45, 2) and 15 * (1 + t) == 45 * t, space=5)

zasoba = 20 * 18
zbytek = zasoba - 20 * 6
dalsich = F(zbytek, 20 - 5)
T.task(3, "Zásoba krmiva vystačí 20 koním na 18 dní. Po 6 dnech se 5 koní prodá. Na kolik dalších dní vystačí zbylé krmivo "
          "zbývajícím koním?", f"na {cz(dalsich)} dní",
       ["Celá zásoba je 20 · 18 = 360 denních dávek (jedna dávka je krmivo pro jednoho koně na jeden den).",
        "Za 6 dní spotřebuje 20 koní 20 · 6 = 120 dávek, zbývá 360 − 120 = 240 dávek.",
        "Zbývajících 15 koní spotřebuje denně 15 dávek: 240 : 15 = 16 dní.",
        "Zkouška: pro 20 koní zbývá 18 − 6 = 12 dní, 12 · 20 : 15 = 16 dní. ✓"],
       zasoba == 360 and zbytek == 240 and dalsich == 16 and F((18 - 6) * 20, 15) == 16, space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
mer = F(100000, 5)
T.diagnostic("Cesta je na mapě dlouhá 5 cm a ve skutečnosti 1 km. Jaké je měřítko mapy?", f"1 : {cz(mer)}",
             ["1 km = 100 000 cm.", "100 000 : 5 = 20 000, takže 1 cm na mapě odpovídá 20 000 cm ve skutečnosti.",
              "Měřítko mapy je 1 : 20 000."],
             mer == 20000 and 5 * mer == 100000)

cas = F(150, 90)
T.diagnostic("Vlak jede stálou rychlostí 90 km/h. Jak dlouho mu trvá cesta dlouhá 150 km? Výsledek zapište v hodinách a minutách.",
             "1 hodina 40 minut",
             ["Čas = dráha : rychlost = 150 : 90 = 5/3 h.", "5/3 h = 1 2/3 h a 2/3 h = 2/3 · 60 = 40 minut.",
              "Cesta trvá 1 hodinu 40 minut."],
             cas == F(5, 3) and cas - 1 == F(2, 3) and (cas - 1) * 60 == 40)

T.save()
