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
CAMPAIGN_NAME = "Printopia – prodej přijímačky"
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
CAMPAIGN = next((c["id"] for c in call("campaigns.list", user, {}, {"limit": 100, "offset": 0}).get("campaigns", [])
                 if c.get("name") == CAMPAIGN_NAME and c.get("status") != "removed"), None)
if CAMPAIGN is None:
    sys.exit("Kampaň zatím neexistuje (sklik_api.py).")
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
by_src = web["funnel"]["bySrc"]
# Návštěvy ze Skliku ze všech stránek (úvod, témata, objednávka), ne jen z úvodu.
sk_views = sum(v.get("view", 0) for k, v in by_src.items() if k.endswith(":sklik"))
sk_home = by_src.get("home:sklik", {})
orders = web.get("orders", {"created": {}, "paid": {}, "revenue": 0})
clicks, spend = st["clicks"], st["totalMoney"] / 100
print(f"# Vyhodnocení Printopia ({since} až {today})\n")
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
print(f"- návštěvy ze Skliku (všechny stránky) {sk_views}, celkem úvod {home.get('view', 0)}")
for k in ["t10", "t30", "scroll50", "cta_sample", "cta_buy", "pdf_download", "form_start", "form_submit"]:
    print(f"  - úvod {k}: {home.get(k, 0)} (ze Skliku {sk_home.get(k, 0)})")
print(f"- e-maily na tipy: {web['server']['leads']}, role: {web['server']['leadsByRole']}")
print(f"- objednávky: vytvořeno {sum(orders['created'].values())}, zaplaceno {sum(orders['paid'].values())}, tržba {orders['revenue']} Kč, "
      f"podle zdroje {orders['paid']}")
print(f"- anketa: {web['feedback']}")
print("\n## Závěry")
for f in web["findings"]:
    print(f"- {f}")
paid = sum(orders["paid"].values())
visits = sk_views or clicks
if paid:
    print(f"- {paid} zaplacených objednávek, {orders['revenue']} Kč; cena za objednávku z reklamy {spend / max(1, orders['paid'].get('sklik', 0)):.0f} Kč.")
if visits >= 190:
    sk_orders = orders["created"].get("sklik", 0)
    print(f"- Rozhodnutí při {visits} návštěvách ze Skliku: objednávek ze Skliku {sk_orders}, zaplacených {orders['paid'].get('sklik', 0)} → "
          + ("POKRAČOVAT (platící zákazníci jsou)" if paid else "PRODLOUŽIT jen SEO / ZASTAVIT reklamu, pokud nikdo neobjednal"))
else:
    print(f"- Zatím {visits} návštěv ze Skliku, rozhodnutí až od cca 190 (při 80 nejde rozlišit 2 % od 5 %), výsledek jen orientační.")
