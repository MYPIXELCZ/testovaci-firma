#!/usr/bin/env python3
"""Kontrola před spuštěním projektu (pojistka z FAILS.md): bez metrik, vyhodnocení a absolutní hledanosti se nespouští.

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
design = plan.with_name("design-" + plan.name)
if not design.exists() or not re.search(r"## Konkurence|## Rozbor", design.read_text(encoding="utf-8")):
    missing.append(f"design průzkum {design} (rozbor konkurence, prvky, vizuální směr)")
elif not re.search(r"## Texty", design.read_text(encoding="utf-8")):
    missing.append(f"{design}: oddíl „## Texty“ (každý blok webu → na jakou otázku cílové skupiny odpovídá)")
code_checks = {
    "aplikace: trychtýř (události návštěvy)": r"funnel|trychtýř",
    "aplikace: anketa „proč ne“": r"[Ff]eedback",
    "aplikace: automatické závěry": r"findings",
    "aplikace: e2e test metrik": r"trychtýř",
}
missing += [k for k, rx in code_checks.items() if not re.search(rx, code)]
# Nejdřív nastudovat, pak dělat: každý použitý kanál má postupy s odškrtnutým kontrolním seznamem.
for channel, marker in {"sklik": "sklik.py"}.items():
    if any(p.name == marker for p in app.rglob(marker)):
        post = plan.parent / "postupy" / f"{channel}.md"
        t = post.read_text(encoding="utf-8") if post.exists() else ""
        if "## Kontrolní seznam" not in t or "- [ ]" in t:
            missing.append(f"{post}: postupy kanálu {channel} s odškrtnutým kontrolním seznamem")
# Absolutní hledanost (FAILS.md 2026-10-01 17:00): bez čísel ze Skliku se nestaví ani nespouští.
vol = next((f for f in (plan.with_name(f"hledanost-{plan.stem}.md"), plan.with_name(f"hledanost-{app.name}.md")) if f.exists()), None)
if vol is None:
    missing.append(f"plan/hledanost-{app.name}.md: absolutní hledanost ze Skliku (`SKLIK_TOKEN=… python3 plan/hledanost.py {app.name} \"dotaz\" … --navrhy \"základ\"`)")
else:
    vt = vol.read_text(encoding="utf-8")
    cap = vt.split("## Kapacita trhu")[1] if "## Kapacita trhu" in vt else ""
    if not cap.strip() or "(doplnit" in cap:
        missing.append(f"{vol}: oddíl „## Kapacita trhu“ (hledanost × CTR × konverze × cena vs. cíl, závěr) musí být vyplněný")
if missing:
    sys.exit("CHYBÍ před spuštěním:\n- " + "\n- ".join(missing))
print("OK: plán i aplikace mají metriky a vyhodnocení.")
