#!/usr/bin/env python3
"""Vyhodnocení testu poptávky Printopia: reklama (Sklik) + web (/api/stats) → zpráva se závěry.

    SKLIK_TOKEN=… STATS_KEY=… python3 printopia/marketing/vyhodnoceni.py [od RRRR-MM-DD]

Odpovídá na „přišlo X lidí a nikdo nekoupil, proč?“: kde v trychtýři lidé odpadají a na jaké dotazy
se reklama ukazovala (špatný dotaz = špatní lidé). Kritéria z plan/prijimacky.md oddíl 4.
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

API = "https://api.sklik.cz/drak/json/v5/"
CAMPAIGN = 7984059
today = datetime.now(ZoneInfo("Europe/Prague")).date().isoformat()  # Sklik počítá dny v pražském čase
since = sys.argv[1] if len(sys.argv) > 1 else "2026-10-01"


def call(method, *params):
    req = urllib.request.Request(API + method, data=json.dumps(params).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def report(kind, filt, columns):
    rid = call(f"{kind}.createReport", user, {**filt, "dateFrom": since, "dateTo": today},
               {"statGranularity": "total", "includeCurrentDayStats": True})
    if rid.get("status") != 200:
        return [], rid.get("statusMessage")
    res = call(f"{kind}.readReport", user, rid["reportId"], {"offset": 0, "limit": 100, "displayColumns": columns})
    return res.get("report", []), None


user = {"session": call("client.loginByToken", os.environ["SKLIK_TOKEN"])["session"]}
camp, err1 = report("campaigns", {"ids": [CAMPAIGN]}, ["id", "name"])
queries, err2 = report("queries", {"campaign": {"ids": [CAMPAIGN]}}, ["query", "keyword.name"])
st = {k: 0 for k in ["impressions", "clicks", "totalMoney"]}
for row in camp:
    for s in row.get("stats", []):
        for k in st:
            st[k] += s.get(k, 0) or 0
web = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://printopia.cz/api/stats", headers={"x-stats-key": os.environ["STATS_KEY"]}), timeout=30))

home = web["funnel"]["byPage"].get("home", {})
sk = web["funnel"]["bySrc"].get("home:sklik", {})
clicks, spend = st["clicks"], st["totalMoney"] / 100
print(f"# Vyhodnocení testu Printopia ({since} až {today})\n")
print("## Reklama (Sklik)")
print(f"- zobrazení {st['impressions']}, prokliky {clicks}, CTR {100 * clicks / st['impressions']:.1f} %" if st["impressions"] else "- zatím žádná zobrazení")
print(f"- utraceno {spend:.0f} Kč, průměrná cena prokliku {spend / clicks:.1f} Kč" if clicks else f"- utraceno {spend:.0f} Kč")
if err1 or err2:
    print(f"- chyba reportu: {err1 or err2}")
top_q = sorted(((q.get("query"), sum(s.get("clicks", 0) or 0 for s in q.get("stats", [])),
                 sum(s.get("impressions", 0) or 0 for s in q.get("stats", []))) for q in queries), key=lambda x: -x[2])[:15]
if top_q:
    print("- hledané dotazy (dotaz: zobrazení / prokliky):")
    for q, c, i in top_q:
        print(f"  - {q}: {i} / {c}")
print("\n## Web")
print(f"- návštěvy ze Skliku {sk.get('view', 0)}, celkem úvod {home.get('view', 0)}")
for k in ["t10", "t30", "scroll50", "cta_sample", "cta_buy", "form_start", "form_submit"]:
    print(f"  - {k}: {home.get(k, 0)}")
print(f"- leady: {web['server']['leads']}, role: {web['server']['leadsByRole']}")
print(f"- anketa: {web['feedback']}")
print("\n## Závěry")
for f in web["findings"]:
    print(f"- {f}")
visits = sk.get("view", 0) or clicks
if visits >= 80:
    buy_rate = 100 * sk.get("cta_buy", 0) / visits
    ok = buy_rate >= 5 and web["server"]["leads"] >= 10 and (not clicks or spend / clicks <= 6)
    stop = buy_rate < 2 or web["server"]["leads"] < 4
    print(f"- Kritérium testu: klik na Koupit {buy_rate:.1f} % (≥ 5 %), e-maily {web['server']['leads']} (≥ 10) → "
          + ("POKRAČOVAT" if ok else "ZASTAVIT" if stop else "PRODLOUŽIT o 7 dní (jen SEO)"))
else:
    print(f"- Kritérium testu: zatím {visits} prokliků, rozhodnutí až od 80.")
