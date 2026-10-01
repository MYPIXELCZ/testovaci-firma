#!/usr/bin/env python3
"""Zakládá a řídí kampaň ze sklik.py přes API Sklik Drak. Idempotentní: existující kampaň nezakládá znovu.

    SKLIK_TOKEN=… python3 printopia/marketing/sklik_api.py [--status | --pause | --resume | --report]

Bez parametru založí kampaň POZASTAVENOU (spustí ji až --resume po schválení reklam, dobití kreditu a nasazení webu).
Token je jen v env (Vercel projekt printopia, SKLIK_TOKEN), nikdy v repozitáři.
Pojistka (FAILS.md 2026-10-01 02:22): kampaň se zakládá a spouští jen podle nastudovaných postupů,
plan/postupy/sklik.md musí mít celý kontrolní seznam odškrtnutý.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.sklik.cz/drak/json/v5/"
CAMPAIGN = "Printopia – prodej přijímačky"
OLD_CAMPAIGN = "Printopia – test přijímačky"  # první verze (kredit 0, nikdy nespuštěná), při založení nové se odstraní

changing = not {"--status", "--pause", "--report"} & set(sys.argv)
if changing:
    postupy = Path(__file__).resolve().parents[2] / "plan/postupy/sklik.md"
    text = postupy.read_text(encoding="utf-8") if postupy.exists() else ""
    if "## Kontrolní seznam" not in text or "- [ ]" in text:
        raise SystemExit(f"Nejdřív {postupy}: celý kontrolní seznam odškrtnutý (- [x]).")

spec = json.loads(subprocess.run([sys.executable, str(Path(__file__).with_name("sklik.py"))],
                                 check=True, capture_output=True, text=True).stdout)


def call(method, *params):
    req = urllib.request.Request(API + method, data=json.dumps(params).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(4):  # síť občas spadne uprostřed spojení; opakovat je bezpečné jen u čtení a přihlášení
        try:
            res = json.load(urllib.request.urlopen(req, timeout=30))
            break
        except OSError:
            if attempt == 3 or method.endswith((".create", ".set", ".remove")):
                raise
            time.sleep(2 ** attempt)
    if res.get("status") not in (200, 206):
        raise SystemExit(f"{method}: {res.get('status')} {res.get('statusMessage')} {res.get('diagnostics')}")
    if res.get("diagnostics"):
        print(f"  {method}: diagnostika {res['diagnostics']}")
    return res


session = call("client.loginByToken", os.environ["SKLIK_TOKEN"])["session"]
user = {"session": session}
info = call("client.get", user)["user"]
print("kredit:", info.get("walletCredit", 0) / 100, "Kč")

camps = call("campaigns.list", user, {}, {"limit": 100, "offset": 0}).get("campaigns", [])
existing = next((c for c in camps if c.get("name") == CAMPAIGN and c.get("status") != "removed"), None)
if existing:
    print("kampaň existuje:", existing["id"], existing.get("status"))
    if "--pause" in sys.argv or "--resume" in sys.argv:
        status = "suspend" if "--pause" in sys.argv else "active"
        call("campaigns.update", user, [{"id": existing["id"], "type": "fulltext", "status": status}])
        print("nový stav:", status)
    if "--report" in sys.argv:
        print(json.dumps(existing, ensure_ascii=False))
    sys.exit(0)
if not changing:
    print("kampaň zatím neexistuje")
    sys.exit(0)

# Autotagging přepisuje utm_source, měření by se rozbilo.
try:
    tag = call("autotagging.get", user)
    print("autotagging:", {k: v for k, v in tag.items() if k not in ("session", "status", "statusMessage")})
except SystemExit as e:
    print("autotagging nelze zjistit:", e)

old = next((c for c in camps if c.get("name") == OLD_CAMPAIGN and c.get("status") != "removed"), None)
if old:
    call("campaigns.remove", user, [old["id"]])
    print("stará kampaň odstraněna:", old["id"])

camp_id = call("campaigns.create", user, [{
    "name": CAMPAIGN, "type": "fulltext", "dayBudget": spec["dailyBudgetCzk"] * 100, "status": "suspend",
    "excludedSearchServices": spec["excludedSearchServices"],
    "negativeKeywords": [{"name": n, "matchType": "negativeBroad"} for n in spec["negative"]],
}])["campaignIds"][0]
out = {"campaignId": camp_id, "groups": {}}
for name, g in spec["groups"].items():
    gid = call("groups.create", user, [{"campaignId": camp_id, "name": name, "cpc": spec["maxCpcCzk"] * 100}])["groupIds"][0]
    kw = call("keywords.create", user, [{"groupId": gid, "name": k, "matchType": "phrase"} for k in g["keywords"]])
    ads = call("ads.create", user, [{
        "groupId": gid, "adType": "eta", "headline1": a["h"][0], "headline2": a["h"][1], "headline3": a["h"][2],
        "description": a["d"][0], "description2": a["d"][1], "path1": a["path"][0], "path2": a["path"][1],
        "finalUrl": spec["url"],
    } for a in g["ads"]])
    out["groups"][name] = {"groupId": gid, "keywords": len(kw.get("positiveKeywordIds", [])), "ads": ads.get("adIds")}

links = call("sitelinks.create", user, [{"name": n, "url": u} for n, u in spec["sitelinks"]] + [{"name": c} for c in spec["callouts"]])
call("sitelinks.campaign.set", user, [{"id": camp_id, "sitelinkIds": links["ids"]}])
out["sitelinks"] = len(links["ids"])
print(json.dumps(out, ensure_ascii=False))
print("Kampaň je POZASTAVENÁ. Spuštění: sklik_api.py --resume (až budou reklamy schválené, kredit připsaný a web nasazený).")
