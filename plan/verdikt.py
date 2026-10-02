#!/usr/bin/env python3
"""Automatický verdikt před stavbou (FAILS.md 2026-10-02 13:31): jde to ověřit do 3 dnů a bude prodej dostatečný?

    python3 plan/verdikt.py <projekt> --cena 349 [--konv 0.01] [--konv-overeni X] [--ctr 0.03] [--cil 10000] [--dny 3] [--rozpocet 0] [--jine-kliky-mesicne 0] [--naklad-mesicne 0] [--jine-cpc N] [--rust-mesicne 0] [--horizont 6] [--trh-objednavek-mesicne N] [--podil-max 0.03] [--pasivni]

Čte `plan/hledanost-<projekt>.md` (tabulka „Cílové dotazy“ ze `plan/hledanost.py`) a do téhož souboru zapíše oddíl „## Verdikt (automaticky)“.
- Ověřitelnost: kolik návštěv se do `--dny` dnů dá reálně získat (hledání × CTR × dny/30 + jiné kliky) proti tomu, kolik jich je potřeba,
  aby aspoň jedna objednávka přišla s pravděpodobností ≥ 60 % při předpokládané konverzi (≈ 92 návštěv při 1 %).
- Dostatečný prodej (Ondřej 2026-10-02 13:46: 3 000 Kč měsíčně není cíl): měsíční ZISK při dnešní hledanosti (ø 2 měs., sezóna se nepočítá) musí dosáhnout
  A) škálovatelný business: průměrný zisk ≥ `--cil` (výchozí 10 000 Kč měsíčně; kolísání mezi měsíci je v pořádku) a cesta k desítkám tisíc, NEBO
  B) plně pasivní business (`--pasivni`: po spuštění žádná práce Clauda ani Ondřeje, vše automaticky): náklady ≤ ⅓ tržeb a zisk ≥ 2 000 Kč měsíčně (např. tržby 3 000, náklad 1 000, zisk 2 000).
  Zisk NEMUSÍ dosáhnout cíle hned (Ondřej 2026-10-02 14:13: nemusí to být první měsíc, perspektiva musí být dlouhodobě): při `--rust-mesicne g` (měsíční růst návštěv/zakázek, max. 0,30) a `--horizont N` (max. 6 měsíců) stačí, aby projektovaný zisk
  zisk × (1+g)^N dosáhl cíle a zisk dnes nebyl záporný. Růst musí mít v `plan/hledanost-<projekt>.md` řádek „Odůvodnění růstu: <čím se bude zvyšovat, s čísly>“, jinak se nepočítá.
  Zisk = tržby − náklady; náklady = klikání placené reklamy (kliky × cena kliku) + `--naklad-mesicne` (ostatní měsíční náklady v Kč).
`--konv-overeni` = podíl návštěv, který stačí jako signál poptávky při ověření (u služeb závazná poptávka s cenou, např. 0,05), jinak platí `--konv`.
`--rozpocet` = Kč, které se v okně ověření smí utratit za dokoupené kliky (cena kliku z tabulky); `--jine-kliky-mesicne` = trvale dostupné kliky mimo hledání (placená reklama jinde): rozpočet / cena kliku. Bez nich počítá jen hledání ze Skliku (Seznam).
Konverze 1 % a CTR 3 % jsou konzervativní předpoklady, ne měření. Cíle (10 000 Kč zisku / pasivně 2 000 Kč zisku při nákladu ≤ ⅓ tržeb) stanovil Ondřej 2026-10-02.
Výjimku z verdiktu smí zapsat jen Ondřej řádkem „Výjimka schválená Ondřejem: <důvod> (<datum>)“.
"""
import math
import re
import sys
from pathlib import Path

args = sys.argv[1:]
project = args[0]
opt = {"--cena": None, "--konv": 0.01, "--konv-overeni": None, "--ctr": 0.03, "--cil": 10000, "--dny": 3, "--rozpocet": 0, "--jine-kliky-mesicne": 0, "--naklad-mesicne": 0, "--jine-cpc": None, "--rust-mesicne": 0, "--horizont": 6, "--trh-objednavek-mesicne": None, "--podil-max": 0.03}
pasivni = "--pasivni" in args
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
jine_cpc = cpc if opt["--jine-cpc"] is None else opt["--jine-cpc"]  # cena kliku mimo Sklik (např. 0 u inzertního portálu, náklady pak do --naklad-mesicne)
naklad = avg * ctr * cpc + jine * jine_cpc + opt["--naklad-mesicne"]
zisk = monthly_avg - naklad
zisk_peak = monthly_peak - (peak * ctr * cpc + jine * jine_cpc + opt["--naklad-mesicne"])
rust = min(opt["--rust-mesicne"], 0.30)
horizont = min(opt["--horizont"], 6)
rust_ok = rust > 0 and re.search(r"Odůvodnění růstu:\s*\S", text) is not None
zisk_h = zisk * (1 + rust) ** horizont if rust_ok else zisk
if opt["--rust-mesicne"] > 0 and not rust_ok:
    print("POZOR: růst se nepočítá, v hledanost souboru chybí řádek „Odůvodnění růstu: …“")
if pasivni:
    ok_sales = monthly_avg > 0 and naklad <= monthly_avg / 3 and zisk >= 2000
    kriterium = "pasivní (náklady ≤ ⅓ tržeb a zisk ≥ 2 000 Kč měsíčně, bez práce po spuštění)"
else:
    ok_sales = zisk >= cil or (rust_ok and zisk >= 0 and zisk_h >= cil)
    kriterium = f"škálovatelný (zisk ≥ {cil:.0f} Kč měsíčně hned" + (f", nebo při odůvodněném růstu {rust * 100:.0f} % měsíčně do {horizont:.0f} měsíců" if rust_ok else ", růst nezadán nebo neodůvodněn") + ", cesta k desítkám tisíc)"
ok_verify = reach >= need
# Ukousnutelný podíl (Ondřej 2026-10-02 14:38: v každém businessu je konkurence, která drží trh; ptát se, zda si realisticky ukousneme kus)
trh = opt["--trh-objednavek-mesicne"]
potreba_obj = (2000 if pasivni else cil) / cena if cena else 0
podil = potreba_obj / trh if trh else None
podil_max = opt["--podil-max"]
ok_share = podil is not None and podil <= podil_max
verdict = f"""## Verdikt (automaticky)
Předpoklady (ne měření): cena {cena:.0f} Kč, konverze na platbu {konv * 100:.1f} %, na signál poptávky při ověření {konv_o * 100:.1f} %, CTR {ctr * 100:.0f} %, cíl zisku {cil:.0f} Kč měsíčně, okno {dny:.0f} dny, rozpočet na dokoupené kliky {rozpocet:.0f} Kč při ø {cpc:.1f} Kč za klik, jiné kliky {jine:.0f} měsíčně. Hledání je jen Seznam (Sklik).
- Ověřitelnost do {dny:.0f} dnů: **{"ANO" if ok_verify else "NE"}**. Dosažitelných návštěv {reach:.1f} (z toho dokoupených {bought:.1f}), potřeba {need} (aspoň jeden signál poptávky s pravděpodobností 60 %).
- Dostatečný prodej: **{"ANO" if ok_sales else "NE"}**. Kritérium: {kriterium}. Tržby měsíčně při dnešní hledanosti {monthly_avg:.0f} Kč, náklady {naklad:.0f} Kč, zisk {zisk:.0f} Kč (ve špičce zisk {zisk_peak:.0f} Kč){f", projektovaný za {horizont:.0f} měs. při růstu {rust * 100:.0f} % měsíčně {zisk_h:.0f} Kč" if rust_ok else ""}.
- Ukousnutelný podíl: **{("ANO" if ok_share else "NE") if podil is not None else "NEOVĚŘENO"}**. {f"Pro cíl je třeba {potreba_obj:.1f} objednávek měsíčně z dosažitelných {trh:.0f}, tj. podíl {podil * 100:.1f} % (realistický strop pro nováčka do 6 měsíců {podil_max * 100:.0f} %)." if podil is not None else "Chybí `--trh-objednavek-mesicne` (kolik nákupních rozhodnutí měsíčně je v dosažitelném trhu); doplnit podle plan/SABLONA.md oddíl 2b."}
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
sys.exit(0 if ok_verify and ok_sales else 1)  # podíl na trhu se vypisuje a hlídá `plan/kontrola-spusteni.py`
