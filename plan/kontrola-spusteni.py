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
# Vercel (FAILS.md 2026-10-02 14:17): web se nasazuje jen do týmu MYPIXELCZ.
if not re.search(r"Vercel tým:\s*MYPIXELCZ\s*\(team_fNHd0fCTFAA6MuEnT4BlEeWu\)", text):
    missing.append("plán: řádek „Vercel tým: MYPIXELCZ (team_fNHd0fCTFAA6MuEnT4BlEeWu)“ po ověření `get_project` (plan/postupy/vercel-nasazeni.md)")
design = plan.with_name("design-" + plan.name)
if not design.exists() or not re.search(r"## Konkurence|## Rozbor", design.read_text(encoding="utf-8")):
    missing.append(f"design průzkum {design} (rozbor konkurence, prvky, vizuální směr)")
elif not re.search(r"## Texty", design.read_text(encoding="utf-8")):
    missing.append(f"{design}: oddíl „## Texty“ (každý blok webu → na jakou otázku cílové skupiny odpovídá)")
if design.exists():
    # Přistávací web (FAILS.md 2026-10-02 13:50 a 13:53): nezávislá revize vzhledu se skóre ≥ 8/10 a čistá `tools/landing-kontrola.mjs`.
    dt = design.read_text(encoding="utf-8")
    rev = re.search(r"## Revize vzhledu(.*?)(\n## |\Z)", dt, re.S)
    sc = re.search(r"Skóre:\s*(\d+(?:[.,]\d+)?)\s*/\s*10", rev.group(1)) if rev else None
    if not rev or not sc or float(sc.group(1).replace(",", ".")) < 8:
        missing.append(f"{design}: oddíl „## Revize vzhledu“ se řádkem „Skóre: N/10“ (N ≥ 8) od nezávislého recenzenta (screenshoty PC 1440 + mobil 390, rubrika z plan/postupy/pristavaci-web.md, kritérium „nepůsobí jako vygenerované AI“)")
    elif not re.search(r"landing-kontrola:\s*OK", rev.group(1)):
        missing.append(f"{design}: v oddílu „## Revize vzhledu“ řádek „landing-kontrola: OK (datum)“ po úspěšném `node tools/landing-kontrola.mjs <URL>`")
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
# Verdikt (FAILS.md 2026-10-02 13:31): ověřitelné do 3 dnů a dostatečný prodej, jinak jen s výjimkou schválenou Ondřejem.
if vol is not None:
    vt = vol.read_text(encoding="utf-8")
    ov = re.search(r"Ověřitelnost do \d+ dnů: \*\*(\w+)", vt)
    ds = re.search(r"Dostatečný prodej: \*\*(\w+)", vt)
    if not (ov and ds):
        missing.append(f"{vol}: oddíl „## Verdikt (automaticky)“ (`python3 plan/verdikt.py <projekt> --cena …`)")
    elif (ov.group(1), ds.group(1)) != ("ANO", "ANO") and "Výjimka schválená Ondřejem:" not in vt:
        missing.append(f"{vol}: verdikt {ov.group(1)}/{ds.group(1)} (ověřitelné do 3 dnů / dostatečný prodej), bez řádku „Výjimka schválená Ondřejem: …“ se nespouští")
if missing:
    sys.exit("CHYBÍ před spuštěním:\n- " + "\n- ".join(missing))
print("OK: plán i aplikace mají metriky a vyhodnocení.")
