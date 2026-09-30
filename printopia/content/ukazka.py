#!/usr/bin/env python3
"""Ukázková sada Zlomky (přijímačky 9. třída): úlohy, postupy a ověření výsledků výpočtem.

    python3 printopia/content/ukazka.py   → printopia/src/content/ukazka.json

Každý krok postupu i výsledek se ověří přes fractions.Fraction; když nesedí, skript spadne.
Úlohy jsou vlastní (ne převzaté z testů CERMAT), jen ve stejném stylu.
"""
import json
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "content" / "ukazka.json"


def fr(x: F) -> str:
    """Zlomek pro sazbu: 7/12, celá čísla bez jmenovatele, záporná se znaménkem."""
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


TASKS = []


def task(topic, text, answer, steps, check):
    assert check, f"Ověření selhalo: {text}"
    TASKS.append({"topic": topic, "text": text, "answer": answer, "steps": steps})


# 1. Sčítání a odčítání
r = F(2, 3) + F(3, 4) - F(5, 6)
task("Sčítání a odčítání", "Vypočtěte a výsledek zapište v základním tvaru: 2/3 + 3/4 − 5/6",
     fr(r),
     ["Společný jmenovatel čísel 3, 4 a 6 je 12.",
      "2/3 = 8/12, 3/4 = 9/12, 5/6 = 10/12.",
      "8/12 + 9/12 − 10/12 = 7/12.",
      "7 a 12 nemají společného dělitele, 7/12 je v základním tvaru."],
     r == F(7, 12) and F(2, 3) == F(8, 12) and F(3, 4) == F(9, 12) and F(5, 6) == F(10, 12))

# 2. Závorka a dělení zlomkem
r = (F(3, 5) - F(1, 2)) / F(3, 10)
task("Dělení zlomkem", "Vypočtěte: (3/5 − 1/2) : 3/10",
     fr(r),
     ["Nejdřív závorka: 3/5 − 1/2 = 6/10 − 5/10 = 1/10.",
      "Dělit zlomkem znamená násobit převrácenou hodnotou: 1/10 : 3/10 = 1/10 · 10/3.",
      "1/10 · 10/3 = 10/30 = 1/3."],
     r == F(1, 3) and F(3, 5) - F(1, 2) == F(1, 10))

# 3. Složený zlomek
r = (1 + F(1, 2)) / (2 - F(1, 4))
task("Složený zlomek", "Vypočtěte složený zlomek: (1 + 1/2) / (2 − 1/4)",
     fr(r),
     ["Čitatel: 1 + 1/2 = 3/2.",
      "Jmenovatel: 2 − 1/4 = 8/4 − 1/4 = 7/4.",
      "3/2 : 7/4 = 3/2 · 4/7 = 12/14 = 6/7."],
     r == F(6, 7) and 1 + F(1, 2) == F(3, 2) and 2 - F(1, 4) == F(7, 4))

# 4. Smíšené číslo a desetinné číslo
r = F(3, 2) * F(4, 10) + F(2, 5)
task("Zlomky a desetinná čísla", "Vypočtěte: 1 1/2 · 0,4 + 2/5",
     fr(r),
     ["Převedeme na zlomky: 1 1/2 = 3/2 a 0,4 = 4/10 = 2/5.",
      "3/2 · 2/5 = 6/10 = 3/5.",
      "3/5 + 2/5 = 5/5 = 1."],
     r == 1 and F(3, 2) * F(2, 5) == F(3, 5))

# 5. Porovnání zlomků
vals = {"5/8": F(5, 8), "2/3": F(2, 3), "7/12": F(7, 12)}
order = sorted(vals, key=vals.get)
task("Porovnávání", "Seřaďte od nejmenšího: 5/8, 2/3, 7/12",
     " < ".join(order),
     ["Společný jmenovatel čísel 8, 3 a 12 je 24.",
      "5/8 = 15/24, 2/3 = 16/24, 7/12 = 14/24.",
      "14/24 < 15/24 < 16/24, tedy 7/12 < 5/8 < 2/3."],
     order == ["7/12", "5/8", "2/3"])

# 6. Slovní úloha: část ze zbytku
pages = 120 / (1 - F(1, 4) - F(1, 3) * (1 - F(1, 4)))
task("Slovní úloha", "Petr přečetl první den 1/4 knihy a druhý den 1/3 zbytku. Zbývá mu přečíst 120 stran. "
     "Kolik stran má kniha?",
     f"{pages} stran",
     ["Po prvním dni zbývají 3/4 knihy.",
      "Druhý den přečte 1/3 ze zbytku: 1/3 · 3/4 = 1/4 knihy.",
      "Zbývá 3/4 − 1/4 = 1/2 knihy, což je 120 stran.",
      "Celá kniha: 120 · 2 = 240 stran.",
      "Zkouška: 240/4 = 60, zbytek 180, 180/3 = 60, zbývá 240 − 60 − 60 = 120. ✓"],
     pages == 240 and 240 - 240 / 4 - (240 - 240 / 4) / 3 == 120)

# 7. Slovní úloha: společná práce
hours = 1 / (F(1, 6) + F(1, 3))
task("Slovní úloha", "První čerpadlo vyčerpá nádrž za 6 hodin, druhé za 3 hodiny. Za kolik hodin ji vyčerpají, "
     "když pracují současně?",
     f"{hours} hodiny",
     ["První čerpadlo vyčerpá za hodinu 1/6 nádrže, druhé 1/3 nádrže.",
      "Společně za hodinu: 1/6 + 1/3 = 1/6 + 2/6 = 3/6 = 1/2 nádrže.",
      "Celou nádrž tedy vyčerpají za 2 hodiny."],
     hours == 2)

# 8. Rovnice se zlomky
x = (F(1, 2) + F(1, 3)) / F(5, 6)
task("Rovnice se zlomky", "Řešte rovnici: 5/6 · x − 1/3 = 1/2",
     f"x = {fr(x)}",
     ["Přičteme 1/3 k oběma stranám: 5/6 · x = 1/2 + 1/3 = 3/6 + 2/6 = 5/6.",
      "Vydělíme 5/6: x = 5/6 : 5/6 = 1.",
      "Zkouška: 5/6 · 1 − 1/3 = 5/6 − 2/6 = 3/6 = 1/2. ✓"],
     x == 1 and F(5, 6) * x - F(1, 3) == F(1, 2))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"title": "Zlomky", "tasks": TASKS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT, len(TASKS), "úloh ověřeno")
