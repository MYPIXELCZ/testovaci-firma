#!/usr/bin/env python3
"""Definice testovací kampaně Sklik pro printopia.cz (test poptávky, plan/prijimacky.md oddíl 4).

    python3 printopia/marketing/sklik.py   → ověří délky textů a vypíše kampaň jako JSON

Kampaň se zakládá přes API Sklik (api.sklik.cz/drak), až bude token a web online.

Cílová skupina (FAILS.md 2026-10-01 01:09): hledají hlavně deváťáci, používají deváťáci, PLATÍ RODIČE.
Inzeráty proto mluví k rodičům; žák, který klikne, může na webu stránku poslat rodičům.
"""
import json

URL = "https://printopia.cz/?utm_source=sklik"
DAILY_BUDGET_CZK = 30          # minimum Skliku; 50 Kč vydrží asi 2 dny, 400 Kč asi 13 dní
MAX_CPC_CZK = 6                # nad 6 Kč za proklik test podle plánu neprojde

# Frázová shoda: dotazy s přímým zájmem o procvičování matematiky na přijímačky (z našeptávačů 2026-10-01).
KEYWORDS = [
    "příprava na přijímačky matematika", "přijímačky matematika procvičování", "přijímačky matematika příklady",
    "přijímačky zlomky", "přijímačky slovní úlohy", "přijímačky matematika pdf", "sbírka úloh přijímačky",
    "procvičování na přijímačky", "příprava na přijímací zkoušky matematika", "přijímačky 9 třída matematika",
    "přijímačky rovnice", "přijímačky procenta",
]
# Vylučujeme dotazy, kde náš produkt nepomůže (jiný typ zkoušky, jiný předmět, řešení konkrétních testů).
NEGATIVE = ["maturita", "vš", "vysoká", "osmileté", "osmiletá", "5 třída", "7 třída", "angličtina", "čeština",
            "řešení 2025", "řešení 2024", "řešení 2026", "výsledky", "termín", "policejní", "zdravotnick"]

HEADLINES = ["Pro rodiče deváťáků", "Přijímačky: matika po tématech", "Ukázka zdarma ke stažení",
             "Úlohy k tisku s postupem", "Procvičí přesně slabá témata"]
DESCRIPTIONS = [
    "Pro rodiče deváťáků: úlohy k tisku na přijímačky z matiky, u každé postup řešení.",
    "Dítěti nejdou zlomky? Stáhněte si zdarma ukázku 8 úloh s postupem a vyzkoušejte to.",
]

# Pojistka: inzerát musí oslovit plátce (rodiče), ne jen dítě.
assert any("rodič" in t.lower() for t in HEADLINES[:1] + DESCRIPTIONS), "Inzeráty musí oslovit rodiče (plátce)"
for h in HEADLINES:
    assert len(h) <= 30, (h, len(h))
for d in DESCRIPTIONS:
    assert len(d) <= 90, (d, len(d))

print(json.dumps({"url": URL, "dailyBudgetCzk": DAILY_BUDGET_CZK, "maxCpcCzk": MAX_CPC_CZK, "keywords": KEYWORDS,
                  "negative": NEGATIVE, "headlines": HEADLINES, "descriptions": DESCRIPTIONS},
                 ensure_ascii=False, indent=1))
