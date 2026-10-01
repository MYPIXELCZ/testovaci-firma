"""Společný formát tematických listů sady (pracovní listy k tisku na přijímačky z matematiky).

Každý tematický soubor content/sada/NN_slug.py vytvoří Topic, přidá řešený příklad a úlohy a zavolá save().
Každá úloha nese `check`: výraz, který výsledek (a ideálně i mezikroky) ověří výpočtem (fractions.Fraction,
math). Když neplatí, skript spadne a list se nevygeneruje. Úlohy jsou vlastní, ve stylu jednotné přijímací
zkoušky, nikdy ne převzaté z testů CERMAT.

Zápis v textech: zlomek „a/b“ (vysází se nad sebou), násobení „·“, dělení „:“, minus „−“, desetinná čárka,
mezery v tisících („12 500“), jednotky s mezerou („5 cm“, „cm²“, „cm³“).
"""
import json
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "src" / "content" / "sada"
LEVELS = {1: "Základ", 2: "Jako u zkoušky", 3: "Náročnější"}
KINDS = {"open": "otevřená úloha", "choice": "výběr z možností", "yesno": "ano/ne", "construct": "konstrukční úloha"}


def fr(x) -> str:
    """Číslo pro sazbu: zlomek „7/12“, celé číslo bez jmenovatele, desetinné s čárkou."""
    x = F(x)
    s = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return s.replace("-", "−")


def dec(x, places=2) -> str:
    """Desetinné číslo s čárkou a bez zbytečných nul: 2.50 → „2,5“."""
    s = f"{float(x):.{places}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


class Topic:
    def __init__(self, num: int, slug: str, title: str, intro: str, tips: list[str]):
        self.data = {"num": num, "slug": slug, "title": title, "intro": intro, "tips": tips, "example": None, "tasks": [],
                     "diagnostic": []}

    def example(self, text: str, steps: list[str], answer: str, check: bool):
        """Řešený příklad na začátek listu: ukáže postup, než žák začne sám."""
        assert check, f"[{self.data['slug']}] Řešený příklad neověřen: {text}"
        self.data["example"] = {"text": text, "steps": steps, "answer": answer}

    def task(self, level: int, text: str, answer: str, steps: list[str], check: bool,
             kind: str = "open", options: list[str] | None = None, figure: str | None = None, space: int = 3):
        """level 1–3, kind: open/choice/yesno/construct; options = 5 možností A–E u choice (answer = „C“ apod.),
        u yesno = výroky (answer = „ANO, NE, ANO“). figure = SVG obrázek (volitelně). space = řádky na počítání (1–8)."""
        slug = self.data["slug"]
        assert check, f"[{slug}] Úloha neověřena: {text}"
        assert level in LEVELS and kind in KINDS, f"[{slug}] Neplatná úroveň/typ: {text}"
        assert steps and all(s.strip() for s in steps), f"[{slug}] Chybí postup: {text}"
        if kind == "choice":
            assert options and len(options) == 5 and answer[:1] in "ABCDE", f"[{slug}] Výběr potřebuje 5 možností a písmeno: {text}"
            assert len(set(options)) == 5, f"[{slug}] Možnosti se opakují: {text}"
        if kind == "yesno":
            assert options and len(options) == len(answer.split(",")), f"[{slug}] Ano/ne: počet výroků a odpovědí nesedí: {text}"
        assert text not in [t["text"] for t in self.data["tasks"]], f"[{slug}] Duplicitní úloha: {text}"
        self.data["tasks"].append({"level": level, "kind": kind, "text": text, "options": options, "answer": answer,
                                   "steps": steps, "figure": figure, "space": space})

    def diagnostic(self, text: str, answer: str, steps: list[str], check: bool, kind: str = "open",
                   options: list[str] | None = None, figure: str | None = None):
        """Dvě úlohy tématu do úvodního testu (jiné než na listu, úroveň „jako u zkoušky“). Podle nich rodič pozná,
        jestli téma procvičit."""
        slug = self.data["slug"]
        assert check, f"[{slug}] Úloha úvodního testu neověřena: {text}"
        assert kind in ("open", "choice"), f"[{slug}] Úvodní test: jen open/choice"
        if kind == "choice":
            assert options and len(options) == 5 and answer[:1] in "ABCDE", f"[{slug}] Výběr potřebuje 5 možností a písmeno: {text}"
        assert text not in [t["text"] for t in self.data["tasks"]], f"[{slug}] Úloha testu je stejná jako na listu: {text}"
        self.data["diagnostic"].append({"kind": kind, "text": text, "options": options, "answer": answer, "steps": steps, "figure": figure})

    def save(self):
        d = self.data
        assert d["example"], f"[{d['slug']}] Chybí řešený příklad"
        n = len(d["tasks"])
        assert 12 <= n <= 18, f"[{d['slug']}] Počet úloh {n}, má být 12–18"
        levels = [t["level"] for t in d["tasks"]]
        assert levels == sorted(levels), f"[{d['slug']}] Úlohy mají jít od základu po náročnější"
        assert all(levels.count(l) >= 3 for l in LEVELS), f"[{d['slug']}] Každá úroveň potřebuje aspoň 3 úlohy"
        assert any(t["kind"] != "open" for t in d["tasks"]), f"[{d['slug']}] Přidej i uzavřené úlohy jako u zkoušky"
        assert len(d["diagnostic"]) == 2, f"[{d['slug']}] Úvodní test potřebuje právě 2 úlohy tématu"
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{d['num']:02d}-{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{d['num']:02d} {d['slug']}: {n} úloh ověřeno")
