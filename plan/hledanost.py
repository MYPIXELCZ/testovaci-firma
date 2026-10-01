#!/usr/bin/env python3
"""Absolutní hledanost dotazů ze Skliku (keywords.suggest.stats), povinná před stavbou projektu (FAILS.md 2026-10-01 17:00).

    SKLIK_TOKEN=… python3 plan/hledanost.py <projekt> "dotaz 1" "dotaz 2" … [--navrhy "základ" …]

Zapíše plan/hledanost-<projekt>.md: tabulka dotazů (průměr 2 posledních měsíců = číslo ve Skliku, špička z 12 měsíců, ø CPC),
součty a prázdný oddíl „## Kapacita trhu“, který musí autor vyplnit (hledanost × CTR × konverze × cena vs. cíl).
`--navrhy` přidá souvisejících až 100 dotazů ke každému základu (keywords.suggest) a ukáže nejsilnější.
Pozor: čísla jsou jen ze Seznamu (Google v Skliku není), 0 znamená „pod prahem“. Kontrola `plan/kontrola-spusteni.py` bez vyplněné kapacity neprojde.
"""
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.sklik.cz/drak/json/v5/"


def call(method, *params):
    req = urllib.request.Request(API + method, data=json.dumps(params).encode(), headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=60))
    if res.get("status") != 200:
        raise SystemExit(f"{method}: {res.get('status')} {res.get('statusMessage')}")
    return res


args = sys.argv[1:]
project, rest = args[0], args[1:]
seeds = []
if "--navrhy" in rest:
    i = rest.index("--navrhy")
    rest, seeds = rest[:i], rest[i + 1:]
queries = list(dict.fromkeys(rest))
user = {"session": call("client.loginByToken", os.environ["SKLIK_TOKEN"])["session"]}
stats = {}


def keep(query, avg, series_raw, cpc_halers):
    series = [t["searchCount"] for t in series_raw][:-1]  # poslední (běžný) měsíc je neúplný
    months = [t["timePeriod"] for t in series_raw][:-1]
    peak = max(series) if series else 0
    stats[query] = (avg, peak, months[series.index(peak)] if series else "-", cpc_halers / 100)


suggested = []
for seed in seeds:
    for x in call("keywords.suggest", user, seed, {"limit": 100}).get("suggestions", []):
        suggested.append(x["query"])
        keep(x["query"], x.get("avgSearchCount", 0), x.get("searchCountInTime", []), x.get("cpc", 0))
suggested = [q for q in dict.fromkeys(suggested) if q not in queries]
todo = [q for q in queries if q not in stats]
for i in range(0, len(todo), 100):
    for x in call("keywords.suggest.stats", user, todo[i:i + 100]).get("stats", []):
        keep(x["query"], x.get("avgSearchCount", 0), x.get("searchCountInTime", []), x.get("avgCpc", 0))


def table(rows):
    out = ["| dotaz | ø 2 měs. | špička 12 měs. | měsíc špičky | ø CPC Kč |", "|---|---:|---:|---|---:|"]
    for q in rows:
        a, p, m, c = stats.get(q, (0, 0, "-", 0))
        out.append(f"| {q} | {a} | {p} | {m} | {c:.1f} |")
    return "\n".join(out)


mine = sorted(queries, key=lambda q: -stats.get(q, (0,))[0])
best = sorted(suggested, key=lambda q: -stats.get(q, (0, 0))[1])[:30]
text = f"""# Hledanost: {project}

Zdroj: Sklik API `keywords.suggest.stats` (jen Seznam; ø 2 měs. je číslo, které ukazuje Sklik, špička = nejvyšší měsíc z posledních 12), staženo {date.today()}. Nula znamená „pod prahem“.

## Cílové dotazy
{table(mine)}

Součet ø 2 měs.: {sum(stats.get(q, (0,))[0] for q in queries)} / měs., součet špiček: {sum(stats.get(q, (0, 0))[1] for q in queries)} / měs.
"""
if best:
    text += f"\n## Nejsilnější související dotazy (podle špičky, z návrhů Skliku)\n{table(best)}\n"
text += "\n## Kapacita trhu\n(doplnit: hledanost × CTR 2–5 % × konverze × cena vs. cíl projektu, závěr stavět / nestavět / nejdřív sonda)\n"
out = Path(__file__).with_name(f"hledanost-{project}.md")
if out.exists() and "## Kapacita trhu" in out.read_text(encoding="utf-8") and "(doplnit" not in out.read_text(encoding="utf-8").split("## Kapacita trhu")[1]:
    keep = out.read_text(encoding="utf-8").split("## Kapacita trhu")[1]  # už vyplněný závěr nepřepisovat
    text = text.split("\n## Kapacita trhu")[0] + "\n## Kapacita trhu" + keep
out.write_text(text, encoding="utf-8")
print(f"zapsáno {out}")
print(table(mine[:12]))
