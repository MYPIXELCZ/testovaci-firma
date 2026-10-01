#!/usr/bin/env python3
"""Zakládá a řídí kampaň ze sklik.py přes API Sklik Drak. Idempotentní: existující kampaň nezakládá znovu.

    SKLIK_TOKEN=… python3 printopia/marketing/sklik_api.py [--status | --pause | --resume | --report | --rebuild | --sitelinks | --ads | --stats]

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
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://api.sklik.cz/drak/json/v5/"
CAMPAIGN_PREFIX = "Printopia – prodej přijímačky"  # Sklik nepustí ani název odstraněné kampaně, proto při přestavbě přibude čas
CAMPAIGN = f"{CAMPAIGN_PREFIX} {datetime.now(ZoneInfo('Europe/Prague')):%Y-%m-%d %H:%M}"
OLD_CAMPAIGN = "Printopia – test přijímačky"  # první verze (kredit 0, nikdy nespuštěná), při založení nové se odstraní

changing = not {"--status", "--pause", "--report", "--ads", "--stats"} & set(sys.argv)
if changing:
    postupy = Path(__file__).resolve().parents[2] / "plan/postupy/sklik.md"
    text = postupy.read_text(encoding="utf-8") if postupy.exists() else ""
    if "## Kontrolní seznam" not in text or "- [ ]" in text:
        raise SystemExit(f"Nejdřív {postupy}: celý kontrolní seznam odškrtnutý (- [x]).")

    vol = Path(__file__).resolve().parents[2] / "plan/hledanost-printopia.md"  # FAILS.md 2026-10-01 17:00: bez absolutní hledanosti se kampaň nemění
    vt = vol.read_text(encoding="utf-8") if vol.exists() else ""
    if "## Kapacita trhu" not in vt or "(doplnit" in vt.split("## Kapacita trhu")[1]:
        raise SystemExit(f"Nejdřív {vol}: absolutní hledanost a vyplněná kapacita trhu (plan/hledanost.py).")

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



def attach_sitelinks(camp_id):
    """Odkazy a Popisky jsou v účtu sdílené (stejné jméno a URL nejde vytvořit dvakrát), proto se použijí už existující."""
    have = {(x["name"], x.get("url") or ""): x["id"] for x in call("sitelinks.list", user).get("sitelinks", []) if not x.get("deleted")}
    wanted = [(n, u) for n, u in spec["sitelinks"]] + [(c, "") for c in spec["callouts"]]
    missing = [(n, u) for n, u in wanted if (n, u) not in have]
    if missing:
        made = call("sitelinks.create", user, [{"name": n, **({"url": u} if u else {})} for n, u in missing])
        have.update(dict(zip(missing, made["ids"])))
    ids = [have[w] for w in wanted]
    call("sitelinks.campaign.set", user, [{"id": camp_id, "sitelinkIds": ids}])
    return len(ids)


session = call("client.loginByToken", os.environ["SKLIK_TOKEN"])["session"]
user = {"session": session}
info = call("client.get", user)["user"]
print("kredit:", info.get("walletCredit", 0) / 100, "Kč")

camps = call("campaigns.list", user, {"isDeleted": False}, {"limit": 100, "offset": 0, "displayColumns": [
    "id", "name", "status", "type", "deleted", "budget.dayBudget", "excludedSearchServices", "actualClicks"]}).get("campaigns", [])
existing = next((c for c in camps if c.get("name", "").startswith(CAMPAIGN_PREFIX) and not c.get("deleted")), None)
if existing and "--rebuild" in sys.argv:
    call("campaigns.remove", user, [existing["id"]])  # jen označí jako odstraněnou; kredit se nespotřebuje
    print("odstraněna pro přestavbu:", existing["id"])
    camps, existing = [c for c in camps if c is not existing], None
if existing:
    print("kampaň existuje:", existing["id"], existing.get("status"))
    if "--pause" in sys.argv or "--resume" in sys.argv:
        status = "suspend" if "--pause" in sys.argv else "active"
        call("campaigns.update", user, [{"id": existing["id"], "type": "fulltext", "status": status}])
        print("nový stav:", status)
    if "--sitelinks" in sys.argv:
        print("odkazy a popisky přiřazeny:", attach_sitelinks(existing["id"]))
    if "--ads" in sys.argv:  # stav schválení reklam (adStatus nastavuje Sklik)
        ads = call("ads.list", user, {"campaign": {"ids": [existing["id"]]}, "isDeleted": False},
                   {"offset": 0, "limit": 100, "displayColumns": ["id", "adStatus", "creative1"]}).get("ads", [])
        for a in ads:
            print(f"  reklama {a['id']}: {a.get('adStatus')} – {a.get('creative1')}")
    if "--stats" in sys.argv:  # zobrazení, kliky a útrata dnes (stav schválení `adStatus` Sklik nevysvětluje, spolehlivý signál jsou až zobrazení)
        day = datetime.now(ZoneInfo("Europe/Prague")).strftime("%Y-%m-%d")
        rid = call("campaigns.createReport", user, {"dateFrom": day, "dateTo": day}, {"statGranularity": "total", "includeCurrentDayStats": True})["reportId"]
        rows = call("campaigns.readReport", user, rid, {"offset": 0, "limit": 100, "allowEmptyStatistics": True,
                                                       "displayColumns": ["id", "impressions", "clicks", "totalMoney"]})["report"]
        names = {c["id"]: c["name"] for c in camps}  # jen neodstraněné kampaně (vyhledávání i Nákupy/Zboží.cz)
        for r in rows:
            if r["id"] in names:
                st = r["stats"][0]
                print(f"dnes {names[r['id']][:40]}: zobrazení {st['impressions']}, kliky {st['clicks']}, útrata {st['totalMoney'] / 100} Kč")
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

old = next((c for c in camps if c.get("name") == OLD_CAMPAIGN and not c.get("deleted")), None)
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
    gid = call("groups.create", user, [{"campaignId": camp_id, "name": name, "cpc": g.get("cpc", spec["maxCpcCzk"]) * 100}])["groupIds"][0]
    kw = call("keywords.create", user, [{"groupId": gid, "name": k, "matchType": "phrase"} for k in g["keywords"]])
    ads = call("ads.create", user, [{
        "groupId": gid, "adType": "eta", "headline1": a["h"][0], "headline2": a["h"][1], "headline3": a["h"][2],
        "description": a["d"][0], "description2": a["d"][1], "path1": a["path"][0], "path2": a["path"][1],
        "finalUrl": spec["url"],
    } for a in g["ads"]])
    out["groups"][name] = {"groupId": gid, "keywords": len(kw.get("positiveKeywordIds", [])), "ads": ads.get("adIds")}

out["sitelinks"] = attach_sitelinks(camp_id)
print(json.dumps(out, ensure_ascii=False))
print("Kampaň je POZASTAVENÁ. Spuštění: sklik_api.py --resume (až budou reklamy schválené, kredit připsaný a web nasazený).")
