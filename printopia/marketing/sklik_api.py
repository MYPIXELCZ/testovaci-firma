#!/usr/bin/env python3
"""Založí testovací kampaň ze sklik.py přes API Sklik Drak. Idempotentní: existující kampaň nezakládá znovu.

    SKLIK_TOKEN=… python3 printopia/marketing/sklik_api.py [--status | --pause | --resume]

Token je jen v env (Vercel projekt printopia, SKLIK_TOKEN), nikdy v repozitáři.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.sklik.cz/drak/json/v5/"
CAMPAIGN = "Printopia – test přijímačky"
spec = json.loads(subprocess.run([sys.executable, str(Path(__file__).with_name("sklik.py"))],
                                 check=True, capture_output=True, text=True).stdout)


def call(method, *params):
    req = urllib.request.Request(API + method, data=json.dumps(params).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(4):  # síť občas spadne uprostřed spojení; opakovat je bezpečné jen u čtení a přihlášení
        try:
            res = json.load(urllib.request.urlopen(req, timeout=30))
            break
        except OSError:
            if attempt == 3 or method.endswith(".create"):
                raise
            time.sleep(2 ** attempt)
    if res.get("status") not in (200, 206):
        raise SystemExit(f"{method}: {res.get('status')} {res.get('statusMessage')} {res.get('diagnostics')}")
    return res


# Pojistka z FAILS.md: kampaň se zakládá a spouští jen podle nastudovaných postupů s odškrtnutým kontrolním seznamem.
if "--status" not in sys.argv and "--pause" not in sys.argv:
    postupy = Path(__file__).resolve().parents[2] / "plan/postupy/sklik.md"
    text = postupy.read_text(encoding="utf-8") if postupy.exists() else ""
    if "## Kontrolní seznam" not in text or "- [ ]" in text:
        raise SystemExit(f"Nejdřív {postupy}: průzkum postupů a celý kontrolní seznam odškrtnutý (- [x]).")

session = call("client.loginByToken", os.environ["SKLIK_TOKEN"])["session"]
user = {"session": session}
info = call("client.get", user)["user"]
print("kredit:", info.get("walletCredit", 0) / 100, "Kč")

existing = [c for c in call("campaigns.list", user, {}, {"limit": 100, "offset": 0}).get("campaigns", [])
            if c.get("name") == CAMPAIGN]
if existing:
    c = existing[0]
    print("kampaň existuje:", c["id"], c.get("status"), c.get("actualClicks"))
    if "--pause" in sys.argv or "--resume" in sys.argv:
        status = "suspend" if "--pause" in sys.argv else "active"
        call("campaigns.update", user, [{"id": c["id"], "type": "fulltext", "status": status}])
        print("nový stav:", status)
    sys.exit(0)
if "--status" in sys.argv:
    print("kampaň zatím neexistuje")
    sys.exit(0)

camp_id = call("campaigns.create", user, [{
    "name": CAMPAIGN, "type": "fulltext", "dayBudget": spec["dailyBudgetCzk"] * 100,
    "negativeKeywords": [{"name": n, "matchType": "negativeBroad"} for n in spec["negative"]],
}])["campaignIds"][0]
group_id = call("groups.create", user, [{"campaignId": camp_id, "name": "Matematika po tématech",
                                         "cpc": spec["maxCpcCzk"] * 100}])["groupIds"][0]
kw = call("keywords.create", user, [{"groupId": group_id, "name": k, "matchType": "phrase"} for k in spec["keywords"]])
h, d = spec["headlines"], spec["descriptions"]
ads = [
    {"groupId": group_id, "adType": "eta", "headline1": h[0], "headline2": h[1], "headline3": h[2],
     "description": d[0], "description2": d[1], "finalUrl": spec["url"]},
    {"groupId": group_id, "adType": "eta", "headline1": h[3], "headline2": h[4], "headline3": h[2],
     "description": d[1], "description2": d[0], "finalUrl": spec["url"]},
]
ad = call("ads.create", user, ads)
print(json.dumps({"campaignId": camp_id, "groupId": group_id, "keywords": len(kw.get("positiveKeywordIds", [])),
                  "ads": ad.get("adIds"), "diagnostics": [kw.get("diagnostics"), ad.get("diagnostics")]}, ensure_ascii=False))
