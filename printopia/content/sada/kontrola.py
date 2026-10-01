#!/usr/bin/env python3
"""Kontrola obsahu celé sady (po vygenerování JSON ze všech témat). Skončí chybou, když něco nesedí.

    python3 printopia/content/sada/kontrola.py

Správnost výsledků ověřují `check` u každé úlohy při generování. Tady se hlídá celek a typografie:
12 témat po sobě, počty úloh, 2 úlohy do úvodního testu na téma, žádné duplicity v celé sadě,
česká typografie (uvozovky, minus, výpustka), „oficiální“ jen v záporném smyslu, žádné odkazy na CERMAT úlohy.
"""
import json
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "src" / "content" / "sada"
files = sorted(DIR.glob("[0-9][0-9]-*.json"))
topics = [json.loads(f.read_text(encoding="utf-8")) for f in files]
errors = []

if [t["num"] for t in topics] != list(range(1, 13)):
    errors.append(f"Témata mají být 1–12 po sobě, jsou: {[t['num'] for t in topics]}")
seen = {}
for t in topics:
    n = len(t["tasks"])
    if not 14 <= n <= 18:
        errors.append(f"{t['slug']}: {n} úloh (má být 14–18)")
    if len(t["diagnostic"]) != 2:
        errors.append(f"{t['slug']}: úvodní test má {len(t['diagnostic'])} úloh (má být 2)")
    # U ano/ne a výběru je zadání text + možnosti (stejný úvod „Platí tato tvrzení?“ je v pořádku).
    texts = [t["example"]["text"]] + [x["text"] + "|" + "|".join(x.get("options") or []) for x in t["tasks"] + t["diagnostic"]]
    for x in texts:
        if x in seen:
            errors.append(f"Duplicitní zadání v {t['slug']} a {seen[x]}: {x[:60]}")
        seen[x] = t["slug"]
    blob = json.dumps(t, ensure_ascii=False)
    for rx, msg in [(r'"[^"\\]{2,60}"(?=[ ,.;:)])', None)]:
        pass
    strings = []

    def walk(o):
        if isinstance(o, str):
            strings.append(o)
        elif isinstance(o, list):
            for i in o:
                walk(i)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k != "figure":
                    walk(v)
    walk(t)
    for s in strings:
        low = s.lower()
        if re.search(r"(?<=\w) - (?=\w)", s) and not re.search(r"\d - \d", s):
            errors.append(f"{t['slug']}: spojovník místo pomlčky/minusu: {s[:70]}")
        if re.search(r"\d - \d", s):
            errors.append(f"{t['slug']}: minus píšeme „−“ (U+2212), ne „-“: {s[:70]}")
        if "..." in s or '"' in s or "  " in s:
            errors.append(f"{t['slug']}: typografie (… „“ jedna mezera): {s[:70]}")
        if "oficiální" in low and not re.search(r"ne(ní|jde|ní)[^.]{0,30}oficiální|není oficiální|nejde o oficiální|oficiální (testy|materiál|zdroj)", low):
            errors.append(f"{t['slug']}: „oficiální“ jen v záporném smyslu: {s[:70]}")
        if re.search(r"cermat", low) and not re.search(r"(nejde|není|nepochází|ne)[^.]{0,60}cermat|cermat[^.]{0,60}(zdarma|minulých let)|(testy|test) cermat|cermat (test|testy)", low):
            errors.append(f"{t['slug']}: zmínka o CERMAT zkontrolovat: {s[:70]}")
    for x in t["tasks"]:
        if x["kind"] == "choice" and x["answer"][0] not in "ABCDE":
            errors.append(f"{t['slug']}: neplatná odpověď u výběru: {x['text'][:50]}")
        if not x["answer"].strip():
            errors.append(f"{t['slug']}: prázdná odpověď: {x['text'][:50]}")

total = sum(len(t["tasks"]) for t in topics)
if errors:
    print("KONTROLA SADY: CHYBY\n- " + "\n- ".join(errors[:60]))
    sys.exit(1)
print(f"KONTROLA SADY: OK ({len(topics)} témat, {total} úloh na listech, {2 * len(topics)} v úvodním testu)")
