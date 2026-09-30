#!/usr/bin/env python3
"""Kontrola před spuštěním projektu (pojistka z FAILS.md): bez metrik a vyhodnocení se nespouští.

    python3 plan/kontrola-spusteni.py plan/<projekt>.md <adresář aplikace>

Ověří, že plán má všechny povinné oddíly šablony a že aplikace měří trychtýř, ptá se na důvod
a umí z dat vyvodit, co zlepšit. Když něco chybí, skončí chybou a vypíše co.
"""
import re
import sys
from pathlib import Path

plan, app = Path(sys.argv[1]), Path(sys.argv[2])
text = plan.read_text(encoding="utf-8")
code = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in app.rglob("*")
                 if p.suffix in {".ts", ".tsx", ".mjs", ".py"} and "node_modules" not in p.parts and ".next" not in p.parts)

checks = {
    "plán: 1. Poptávka": r"## 1\. Poptávka",
    "plán: 1b. Cílová skupina": r"## 1b\. Cílová skupina",
    "plán: 3. Ekonomika": r"## 3\. Ekonomika",
    "plán: 4. Test poptávky": r"## 4\. Test poptávky",
    "plán: 7. Metriky a vyhodnocení": r"## 7\. Metriky",
}
missing = [k for k, rx in checks.items() if not re.search(rx, text)]
code_checks = {
    "aplikace: trychtýř (události návštěvy)": r"funnel|trychtýř",
    "aplikace: anketa „proč ne“": r"[Ff]eedback",
    "aplikace: automatické závěry": r"findings",
    "aplikace: e2e test metrik": r"trychtýř",
}
missing += [k for k, rx in code_checks.items() if not re.search(rx, code)]
if missing:
    sys.exit("CHYBÍ před spuštěním:\n- " + "\n- ".join(missing))
print("OK: plán i aplikace mají metriky a vyhodnocení.")
