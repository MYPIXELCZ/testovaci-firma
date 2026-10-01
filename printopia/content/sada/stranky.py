#!/usr/bin/env python3
"""Tematické SEO stránky zdarma z ověřených úloh sady → src/content/temata/{slug}.json.

    python3 printopia/content/sada/stranky.py   (po vygenerování JSON ze všech témat)

Z každého tématu bere jen úlohy bez obrázku a bez výběru (aby stačil text), max. 6 (zbytek zůstává v placené sadě).
Cílová skupina: stránku hledá žák nebo rodič, příklady řeší žák; prodejní sdělení míří na dospělé (odkaz na sadu dole).
"""
import json
from pathlib import Path

SADA = Path(__file__).resolve().parents[2] / "src" / "content" / "sada"
OUT = Path(__file__).resolve().parents[2] / "src" / "content" / "temata"
LEVELS = {1: "Základ", 2: "Jako u zkoušky", 3: "Náročnější"}

PAGES = {
    "vyrazy": ("vyrazy-prijimacky", "Výrazy a mnohočleny na přijímačky: příklady s postupem řešení",
               "Výrazy a mnohočleny na přijímačky: příklady s postupem",
               "úprava výrazů, roznásobení, vzorce (a ± b)² a a² − b², vytýkání a dosazení",
               "Úprava výrazů je v přijímačkách z matematiky v úloze 3, kde se jedna část píše s postupem a každá chyba stojí bod."),
    "umernost": ("pomer-a-umernost-prijimacky", "Poměr, úměrnost, pohyb a práce na přijímačky: příklady s postupem",
                 "Poměr a úměrnost na přijímačky: příklady s postupem",
                 "poměr, trojčlenka, měřítko, rychlost a společná práce",
                 "Poměr, úměrnost, rychlost a společná práce se v přijímačkách objevují v krátkých úlohách i uvnitř slovních úloh."),
    "grafy": ("grafy-a-prumer-prijimacky", "Grafy, tabulky a průměr na přijímačky: příklady s postupem",
              "Grafy, tabulky a průměr na přijímačky: příklady s postupem",
              "čtení z grafů, aritmetický průměr, medián a souřadnice bodů",
              "Úloha 11 u přijímaček je svazek tří tvrzení ANO/NE ke grafu nebo tabulce. Procvičte si práci s daty."),
    "uhly": ("uhly-a-trojuhelniky-prijimacky", "Úhly a trojúhelníky na přijímačky: příklady s postupem řešení",
             "Úhly a trojúhelníky na přijímačky: příklady s postupem",
             "vedlejší, vrcholové a střídavé úhly, součet úhlů a rovnoramenný trojúhelník",
             "Úhly se v přijímačkách počítají v geometrických úlohách i ve výběru z možností A–E. Pomůže pečlivý náčrt."),
    "obsahy": ("obsahy-a-pythagorova-veta-prijimacky", "Obvody, obsahy, kruh a Pythagorova věta na přijímačky: příklady",
               "Obvody, obsahy a Pythagorova věta na přijímačky: příklady",
               "obvod a obsah rovinných útvarů, kruh a Pythagorova věta",
               "Obvody a obsahy patří k nejčastějším geometrickým úlohám. U zkoušky je u kruhu uvedené π, ostatní vzorce znát musíte."),
    "telesa": ("telesa-objem-povrch-prijimacky", "Tělesa, objem a povrch na přijímačky: příklady s postupem řešení",
               "Tělesa: objem a povrch na přijímačky, příklady s postupem",
               "objem a povrch krychle, kvádru, hranolu a válce, převody jednotek a hladina vody",
               "Tělesa jsou skoro v každém testu a úspěšnost je jen kolem 28 %. Žáci si pletou povrch s pláštěm a chybují v jednotkách."),
    "konstrukce": ("konstrukcni-ulohy-prijimacky", "Konstrukční úlohy na přijímačky: příklady s postupem řešení",
                   "Konstrukční úlohy na přijímačky: příklady s postupem",
                   "konstrukce trojúhelníků a čtyřúhelníků, osa úsečky a úhlu, množiny bodů",
                   "Konstrukce jsou za 5 až 6 bodů z 50, ale úspěšnost je kolem 24 % a třetina žáků je vůbec nezkusí. Přitom stačí základní kroky."),
    "vzory": ("uslovne-ulohy-vzory-prijimacky", "Úsudek a vzory na přijímačky: nestandardní úlohy s postupem",
              "Úsudek a vzory na přijímačky: nestandardní úlohy s postupem",
              "číselné řady, vzory z obrazců, logické úlohy a kombinatorika",
              "Poslední úloha testu bývá nestandardní a řeší ji jen asi 14 % žáků. Zkuste si, jak se k takovým úlohám přistupuje."),
}
# slug stránky u vzorů zní lépe jako „vzory-a-usudek-prijimacky“
PAGES["vzory"] = ("vzory-a-usudek-prijimacky",) + PAGES["vzory"][1:]


def pick(tasks):
    ok = [t for t in tasks if t["kind"] in ("open", "construct") and not t.get("figure") and not t.get("options")]
    chosen = []
    for level, n in ((1, 2), (2, 3), (3, 1)):
        chosen += [t for t in ok if t["level"] == level][:n]
    rest = [t for t in ok if t not in chosen]
    chosen += rest[: max(0, 6 - len(chosen))]
    return chosen[:6]


OUT.mkdir(parents=True, exist_ok=True)
made = []
for f in sorted(SADA.glob("[0-9][0-9]-*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    if d["slug"] not in PAGES:
        continue
    slug, title, h1, what, lead = PAGES[d["slug"]]
    tasks = pick(d["tasks"])
    if len(tasks) < 4:
        print(f"{slug}: jen {len(tasks)} vhodných úloh, stránka se nevytvoří")
        continue
    page = {
        "slug": slug, "title": title, "h1": h1,
        "description": f"{len(tasks)} příkladů ve stylu přijímaček z matematiky ({what}). S postupem řešení krok za krokem.",
        "lead": f"{lead} Tady je {len(tasks)} příkladů z naší sady. Nejdřív počítejte sami, postup si rozbalte až potom.",
        "tips": d["tips"][:4],
        "tasks": [{"topic": LEVELS[t["level"]], "text": t["text"], "answer": t["answer"], "steps": t["steps"]} for t in tasks],
    }
    (OUT / f"{slug}.json").write_text(json.dumps(page, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    made.append(slug)
    print(slug, len(tasks), "úloh")

# index.ts: všechny stránky v jednom seznamu
existing = sorted(p.stem for p in OUT.glob("*.json"))
lines = [f'import t{i} from "./{s}.json";' for i, s in enumerate(existing)]
lines += ["", "export type Topic = typeof t0;", "",
          "// Tematické stránky s příklady (generují content/temata.py a content/sada/stranky.py).",
          "// Zlomky mají vlastní stránku s ukázkou ke stažení.",
          "const ALL: Topic[] = [" + ", ".join(f"t{i}" for i in range(len(existing))) + "];",
          "export const TOPICS: Record<string, Topic> = Object.fromEntries(ALL.map((t) => [t.slug, t]));", ""]
(OUT / "index.ts").write_text("\n".join(lines), encoding="utf-8")
print("index.ts:", len(existing), "stránek")
