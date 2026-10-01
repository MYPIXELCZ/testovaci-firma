#!/usr/bin/env python3
"""Definice kampaně Sklik pro printopia.cz (prodej sady, plan/prijimacky.md oddíl 4).

    python3 printopia/marketing/sklik.py   → ověří texty a vypíše kampaň jako JSON

Postupy a kontrolní seznam: plan/postupy/sklik.md (všechny body musí být odškrtnuté, hlídá sklik_api.py).
Cílová skupina (FAILS.md 2026-10-01 01:09): hledají hlavně deváťáci, používají deváťáci, PLATÍ RODIČE.
Inzeráty proto mluví k rodičům a nikdy nevyzývají dítě ke koupi (UCPD příloha I bod 28).
Pojistky níže jsou `assert`y: skript spadne, když texty porušují pravidla Skliku nebo naše.
"""
import json
import re
import unicodedata

BASE = "https://printopia.cz"
# Měření bez cookies: utm_source pozná kanál, {keywordId} a {creative} doplní Sklik (rozpad po slovech a reklamách).
UTM = "utm_source=sklik&utm_term={keywordId}&utm_content={creative}"
URL = f"{BASE}/?{UTM}"
DAILY_BUDGET_CZK = 30          # minimum Skliku
MAX_CPC_CZK = 5                # při ceně sady 349 Kč a konverzi kolem 1 % je dražší klik ztráta
EXCLUDED_SEARCH_SERVICES = [4]  # Encyklopedie.Seznam.cz (1 = Seznam.cz, 8 = partnerské vyhledávače ponecháno)

# Frázová shoda (ignoruje pády a diakritiku, pořadí slov je volné): dotazy z našeptávače Seznamu 2026-10-01.
GROUPS = {
    "Příprava (rodiče)": {
        "keywords": [
            "příprava na přijímací zkoušky matematika", "příprava na přijímací zkoušky na střední školu",
            "příprava na přijímačky matematika", "státní přijímačky z matematiky", "sbírka úloh přijímačky",
            "pracovní sešit přijímačky", "procvičování na přijímačky", "přijímačky 9 třída matematika",
        ],
        "ads": [
            {"h": ["Přijímačky: matika po tématech", "Pro rodiče deváťáků", "Postup u každé úlohy"],
             "d": ["Sada 12 témat k tisku za 349 Kč: úlohy s postupem řešení a plán do zkoušky.",
                   "Zaplatíte převodem, soubory ke stažení máte hned po zaplacení. 14 dní na vrácení peněz."],
             "path": ["přijímačky", "matematika"]},
            {"h": ["Víte, co dítěti nejde?", "Úvodní test + plán do zkoušky", "Sada 12 témat za 349 Kč"],
             "d": ["Úvodní test ukáže slabá témata, plán rozvrhne přípravu do zkoušky 12. dubna 2027.",
                   "Pro rodiče deváťáků: 12 témat k tisku, u každé úlohy postup řešení krok za krokem."],
             "path": ["příprava", "slabá témata"]},
        ],
    },
    "Témata": {
        "keywords": [
            "přijímačky zlomky", "přijímačky procenta", "přijímačky rovnice", "přijímačky slovní úlohy",
            "přijímačky matematika příklady", "přijímačky konstrukční úlohy", "přijímačky geometrie",
        ],
        "ads": [
            {"h": ["Zlomky, procenta, rovnice", "Přijímačky z matiky s postupem", "Sada 12 témat za 349 Kč"],
             "d": ["Pro rodiče deváťáků: příklady po tématech k tisku, u každé úlohy postup řešení.",
                   "Konstrukce, geometrie, slovní úlohy i grafy. Příklady si projdete na webu předem."],
             "path": ["přijímačky", "příklady"]},
            {"h": ["Slovní úlohy na přijímačky", "Úlohy k tisku s postupem", "Sada 12 témat za 349 Kč"],
             "d": ["Slovní úlohy, zlomky, procenta, konstrukce: každé téma zvlášť, s postupem řešení.",
                   "Pro rodiče deváťáků. Jednorázově 349 Kč, bez předplatného, 14 dní na vrácení peněz."],
             "path": ["slovní úlohy", "matematika"]},
        ],
    },
}

# Vylučující slova (volná negativní shoda na úrovni kampaně). Každé slovo s diakritikou dostane i variantu bez ní.
# Základ: dotazy z našeptávače, kde náš produkt nepomůže. „cermat“, „testy“, „pdf“ jen sledovat v reportu dotazů.
_NEGATIVE = [
    "maturita", "maturitní", "vš", "vysoká", "vysoké", "osmileté", "osmiletá", "víceleté", "šestileté", "6leté", "8leté",
    "5.třída", "7.třída", "5 třída", "7 třída", "policejní", "zdravotnická", "angličtina", "čeština", "jazyk", "čj",
    "výsledky", "termín", "přihláška", "2024", "2025", "klíč", "doučování", "kurz", "lektor", "zdarma", "online",
    "nanečisto", "nečisto", "scio", "blesk", "taktik", "robin", "youtube",
    "brno", "praha", "plzeň", "ostrava", "olomouc", "kladno", "pardubice", "hradec", "budějovice", "mělník",
]


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


NEGATIVE = sorted({v for w in _NEGATIVE for v in (w, fold(w))})

SITELINKS = [  # Odkazy (text ≤ 25 znaků, každý na jinou URL)
    ("Zlomky na přijímačky", f"{BASE}/zlomky-prijimacky?utm_source=sklik"),
    ("Procenta na přijímačky", f"{BASE}/procenta-prijimacky?utm_source=sklik"),
    ("Rovnice na přijímačky", f"{BASE}/rovnice-prijimacky?utm_source=sklik"),
    ("Slovní úlohy", f"{BASE}/slovni-ulohy-prijimacky?utm_source=sklik"),
    ("Jak se připravit", f"{BASE}/jak-se-pripravit-na-prijimacky?utm_source=sklik"),
]
CALLOUTS = ["Postup u každé úlohy", "Soubory k tisku", "14 dní na vrácení peněz", "Bez předplatného"]  # Popisky (≤ 25)

# --------------------------------------------------------------------------- pojistky
FORBIDDEN = ["kup si", "kupte si", "řekni rodičům", "řekněte rodičům", "přemluv", "nech si koupit"]
ALLOWED_CAPS: set[str] = set()  # Sklik varuje před 2+ po sobě jdoucími velkými písmeny (PDF, QR), proto je v textech reklam nepoužíváme
all_text = []
for name, g in GROUPS.items():
    assert 2 <= len(g["ads"]) <= 4, f"{name}: 2–4 reklamy v sestavě"
    for ad in g["ads"]:
        assert len(ad["h"]) == 3 and len(ad["d"]) == 2 and len(ad["path"]) == 2
        for h in ad["h"]:
            assert len(h) <= 30, (h, len(h))
            assert "!" not in h, f"vykřičník v titulku: {h}"
        for d in ad["d"]:
            assert len(d) <= 90, (d, len(d))
        for p in ad["path"]:
            assert len(p) <= 15, (p, len(p))
        all_text += ad["h"] + ad["d"]
        # Plátce (rodič) je osloven v titulku 1–2 nebo popisku 1, kde se reklama zobrazí jistě.
        assert any("rodič" in t.lower() for t in [ad["h"][0], ad["h"][1], ad["d"][0], ad["d"][1]]) or "dítěti" in ad["h"][0], (
            f"Reklama musí oslovit rodiče (plátce): {ad['h'][0]}")
for t in all_text:
    low = t.lower()
    assert not any(f in low for f in FORBIDDEN), f"Výzva dítěti ke koupi: {t}"
    assert '"' not in t and "'" not in t, f"Rovné uvozovky: {t}"
    for w in re.findall(r"\b[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{3,}\b", t):
        assert w in ALLOWED_CAPS, f"Slovo velkými písmeny: {w} v {t}"
for c in CALLOUTS:
    assert not re.search(r"[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{2,}", c), f"Velká písmena v Popisku: {c}"
for s, _ in SITELINKS:
    assert len(s) <= 25, (s, len(s))
assert len({u for _, u in SITELINKS}) == len(SITELINKS), "Odkazy musí mít každý jinou URL"
assert len(CALLOUTS) >= 4 and all(len(c) <= 25 for c in CALLOUTS), "Aspoň 4 Popisky do 25 znaků"
assert all("utm_source=sklik" in u for _, u in SITELINKS) and "utm_source=sklik" in URL

STOP = {"na", "z", "do", "a", "s", "o", "pro"}
kws = [(g, k) for g, d in GROUPS.items() for k in d["keywords"]]
words = [(k, {w for w in fold(k).lower().split() if w not in STOP}) for _, k in kws]
assert len({k for k, _ in words}) == len(words), "Duplicitní klíčová slova"
for a, wa in words:
    for b, wb in words:
        assert a == b or not wa < wb, f"Frázová shoda: „{b}“ je nadmnožinou „{a}“, vyřadit"
assert all(len(k.split()) <= 8 for _, k in kws), "Klíčové slovo má max. 8 slov"
for w in _NEGATIVE:  # vylučující slovo nesmí zabít vlastní klíčové slovo
    assert not any(fold(w) in fold(k).lower().split() for _, k in kws), f"Vylučující slovo „{w}“ je v klíčovém slově"

print(json.dumps({"url": URL, "dailyBudgetCzk": DAILY_BUDGET_CZK, "maxCpcCzk": MAX_CPC_CZK,
                  "excludedSearchServices": EXCLUDED_SEARCH_SERVICES, "groups": GROUPS, "negative": NEGATIVE,
                  "sitelinks": SITELINKS, "callouts": CALLOUTS}, ensure_ascii=False, indent=1))
