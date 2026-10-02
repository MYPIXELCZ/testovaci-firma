#!/usr/bin/env python3
"""Automatický verdikt před stavbou (FAILS.md 2026-10-02 13:31): jde to ověřit do 3 dnů a bude prodej dostatečný?

    python3 plan/verdikt.py <projekt> --cena 349 [--konv 0.01] [--konv-overeni X] [--ctr 0.03] [--cil 3000] [--dny 3] [--rozpocet 0] [--jine-kliky-mesicne 0]

Čte `plan/hledanost-<projekt>.md` (tabulka „Cílové dotazy“ ze `plan/hledanost.py`) a do téhož souboru zapíše oddíl „## Verdikt (automaticky)“.
- Ověřitelnost: kolik návštěv se do `--dny` dnů dá reálně získat (hledání × CTR × dny/30 + jiné kliky) proti tomu, kolik jich je potřeba,
  aby aspoň jedna objednávka přišla s pravděpodobností ≥ 60 % při předpokládané konverzi (≈ 92 návštěv při 1 %).
- Dostatečný prodej: měsíční tržby při dnešní hledanosti (ø 2 měs., sezóna se nepočítá) proti cíli `--cil` Kč měsíčně.
`--konv-overeni` = podíl návštěv, který stačí jako signál poptávky při ověření (u služeb závazná poptávka s cenou, např. 0,05), jinak platí `--konv`.
`--rozpocet` = Kč, které se v okně ověření smí utratit za dokoupené kliky (cena kliku z tabulky); `--jine-kliky-mesicne` = trvale dostupné kliky mimo hledání (placená reklama jinde): rozpočet / cena kliku. Bez nich počítá jen hledání ze Skliku (Seznam).
Konverze 1 % a CTR 3 % jsou konzervativní předpoklady, ne měření. Cíl 3 000 Kč měsíčně je minimum pro „vedlejší příjem“, Ondřej ho může změnit.
Výjimku z verdiktu smí zapsat jen Ondřej řádkem „Výjimka schválená Ondřejem: <důvod> (<datum>)“.
"""
import math
import re
import sys
from pathlib import Path

args = sys.argv[1:]
project = args[0]
opt = {"--cena": None, "--konv": 0.01, "--konv-overeni": None, "--ctr": 0.03, "--cil": 3000, "--dny": 3, "--rozpocet": 0, "--jine-kliky-mesicne": 0}
for i, a in enumerate(args):
    if a in opt:
        opt[a] = float(args[i + 1])
if opt["--cena"] is None:
    raise SystemExit("Chybí --cena (cena produktu v Kč).")
cena, konv, ctr, cil, dny, jine = (opt[k] for k in ("--cena", "--konv", "--ctr", "--cil", "--dny", "--jine-kliky-mesicne"))
konv_o = opt["--konv-overeni"] or konv
rozpocet = opt["--rozpocet"]

path = Path(__file__).with_name(f"hledanost-{project}.md")
text = path.read_text(encoding="utf-8")
section = text.split("## Cílové dotazy")[1].split("\n## ")[0]
avg = peak = 0
cpc_w = cpc_n = 0
for line in section.splitlines():
    m = re.match(r"\| .+? \| (\d+) \| (\d+) \| \S+ \| ([\d.]+) \|", line)
    if m:
        avg += int(m.group(1))
        peak += int(m.group(2))
        if float(m.group(3)) > 0 and int(m.group(1)) > 0:
            cpc_w += float(m.group(3)) * int(m.group(1))
            cpc_n += int(m.group(1))
cpc = cpc_w / cpc_n if cpc_n else 5.0  # ø cena kliku vážená hledaností, jinak 5 Kč

need = math.ceil(math.log(0.4) / math.log(1 - konv_o))  # návštěv pro ≥ 60 % šanci aspoň na jeden signál poptávky
bought = rozpocet / cpc if cpc else 0
reach = avg * ctr * dny / 30 + jine * dny / 30 + bought
monthly_avg = (avg * ctr + jine) * konv * cena
monthly_peak = (peak * ctr + jine) * konv * cena
ok_verify = reach >= need
ok_sales = monthly_avg >= cil
verdict = f"""## Verdikt (automaticky)
Předpoklady (ne měření): cena {cena:.0f} Kč, konverze na platbu {konv * 100:.1f} %, na signál poptávky při ověření {konv_o * 100:.1f} %, CTR {ctr * 100:.0f} %, cíl {cil:.0f} Kč měsíčně, okno {dny:.0f} dny, rozpočet na dokoupené kliky {rozpocet:.0f} Kč při ø {cpc:.1f} Kč za klik, jiné kliky {jine:.0f} měsíčně. Hledání je jen Seznam (Sklik).
- Ověřitelnost do {dny:.0f} dnů: **{"ANO" if ok_verify else "NE"}**. Dosažitelných návštěv {reach:.1f} (z toho dokoupených {bought:.1f}), potřeba {need} (aspoň jeden signál poptávky s pravděpodobností 60 %).
- Dostatečný prodej: **{"ANO" if ok_sales else "NE"}**. Tržby měsíčně při dnešní hledanosti {monthly_avg:.0f} Kč (ve špičce {monthly_peak:.0f} Kč) proti cíli {cil:.0f} Kč.
- Závěr: **{"stavět smí" if ok_verify and ok_sales else "NESTAVĚT a nespouštět bez výjimky schválené Ondřejem"}**.
"""
if "## Verdikt (automaticky)" in text:
    head, rest = text.split("## Verdikt (automaticky)", 1)
    tail = "\n## " + rest.split("\n## ", 1)[1] if "\n## " in rest else ""
    text = head.rstrip("\n") + "\n\n" + verdict + tail
else:
    marker = "\n## Kapacita trhu"
    text = text.replace(marker, "\n" + verdict + marker, 1) if marker in text else text.rstrip("\n") + "\n\n" + verdict
path.write_text(text, encoding="utf-8")
print(verdict)
sys.exit(0 if ok_verify and ok_sales else 1)
