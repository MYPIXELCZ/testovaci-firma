#!/usr/bin/env python3
"""Jeden přehled výsledků VŠECH akcí z plan/akce.md (FAILS.md 2026-10-02 13:32: nesmí se sledovat jen aktuální akce).

    python3 tools/stav.py

Tokeny: env SKLIK_TOKEN, STATS_KEY_PRINTOPIA, STATS_KEY_ANOBERU, jinak soubory .sklik_token, .stats_key, .stats_key_anoberu ve scratchpadu.
Každá akce v plan/akce.md, která není `zamítnuto`/`hotovo`, musí mít v posledním sloupci značku [stav:<sekce>] a sekce musí tady existovat,
jinak skript hlásí CHYBÍ SLEDOVÁNÍ. Nová akce = nový řádek v akce.md se značkou + nová sekce zde.
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALERTS: list[str] = []


def secret(env, fname):
    if os.environ.get(env):
        return os.environ[env]
    for p in glob.glob(f"/tmp/claude-*/**/scratchpad/{fname}", recursive=True):
        return Path(p).read_text().strip()
    return None


def http(url, headers=None, ua=None):
    req = urllib.request.Request(url, headers={**(headers or {}), **({"User-Agent": ua} if ua else {})})
    try:
        return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        return f"CHYBA {e}"


API = "https://api.sklik.cz/drak/json/v5/"


def sklik_call(method, *params):
    req = urllib.request.Request(API + method, data=json.dumps(params).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def sklik():
    print("\n## sklik: vyhledávání, skupina Testy a Nákupy (Zboží.cz)")
    token = secret("SKLIK_TOKEN", ".sklik_token")
    if not token:
        print("  CHYBÍ SKLIK_TOKEN"); return
    u = {"session": sklik_call("client.loginByToken", token)["session"]}
    credit = sklik_call("client.get", u)["user"].get("walletCredit", 0) / 100
    print(f"  kredit {credit} Kč")
    if credit < 82:
        ALERTS.append(f"Sklik: kredit klesl na {credit} Kč (útrata)")
    camps = {c["id"]: c for c in sklik_call("campaigns.list", u, {"isDeleted": False}, {"limit": 50, "offset": 0, "displayColumns": ["id", "name", "status", "type", "budget.dayBudget"]}).get("campaigns", [])}
    frm, to = (date.today() - timedelta(days=7)).isoformat(), date.today().isoformat()

    def report(kind, cols):
        r = sklik_call(f"{kind}.createReport", u, {"dateFrom": frm, "dateTo": to}, {"statGranularity": "daily", "includeCurrentDayStats": True})
        if r.get("status") != 200:
            print(f"  {kind}: {r.get('statusMessage')}"); return []
        return sklik_call(f"{kind}.readReport", u, r["reportId"], {"offset": 0, "limit": 300, "allowEmptyStatistics": True, "displayColumns": cols}).get("report", [])

    for kind, cols in (("campaigns", ["id", "name", "impressions", "clicks", "totalMoney"]), ("groups", ["id", "name", "impressions", "clicks", "totalMoney"]),
                       ("keywords", ["id", "name", "impressions", "clicks", "totalMoney"])):
        print(f"  {kind} (posledních 7 dní, jen s aktivitou):")
        for r in report(kind, cols):
            days = [(s["date"], s.get("impressions", 0), s.get("clicks", 0), s.get("totalMoney", 0)) for s in r.get("stats", []) if s.get("date")]
            imp, clk, money = sum(d[1] for d in days), sum(d[2] for d in days), sum(d[3] for d in days)
            if kind == "campaigns" and r["id"] not in camps:
                continue
            if imp or clk or kind == "campaigns":
                c = camps.get(r["id"], {})
                extra = f" [{c.get('type')}, {c.get('status')}, {c.get('budget', {}).get('dayBudget', 0) / 100:.0f} Kč/den]" if kind == "campaigns" else ""
                print(f"    {r.get('name', '')[:44]}{extra}: zobrazení {imp}, kliky {clk}, útrata {money / 100:.2f} Kč, po dnech {[(d[0], d[1], d[2]) for d in days]}")
            if clk:
                ALERTS.append(f"Sklik {kind}: {r.get('name')} má {clk} kliků")
            if kind == "campaigns" and imp:
                ALERTS.append(f"Sklik: {r.get('name')} má {imp} zobrazení za 7 dní")


def site(name, url, env, fname):
    print(f"\n## {name}")
    key = secret(env, fname)
    code = http(url + "/")[:5]
    print(f"  web: {'OK' if not code.startswith('CHYBA') else code}")
    d = json.loads(http(url + "/api/stats", {"x-stats-key": key or ""}) or "{}")
    orders = d.get("orders", {})
    print(f"  objednávky {json.dumps(orders, ensure_ascii=False)}")
    server = d.get("server", {})
    if server:
        print(f"  návštěvy podle zdroje {server.get('visits')}, po dnech {server.get('visitsByDay')}, klik na Koupit {server.get('buyClicks')}, leady {server.get('leads')}")
    print(f"  anketa {json.dumps(d.get('feedback'), ensure_ascii=False)}")
    created = orders.get("created", 0)
    created = sum(created.values()) if isinstance(created, dict) else created
    if created:
        ALERTS.append(f"{name}: {created} vytvořených objednávek")
    if server.get("leads"):
        ALERTS.append(f"{name}: {server['leads']} leadů")
    if any(k != "direct" and v for k, v in (server.get("visits") or {}).items()):
        ALERTS.append(f"{name}: návštěvy z jiného zdroje než přímo: {server['visits']}")
    return d


def zbozi():
    print("\n## zbozi: nabídka Printopie na Zboží.cz")
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15"
    for q in ("matematika 9 třída přijímačky", "přijímačky matematika"):
        found = None
        for page in (1, 2, 3):
            url = "https://www.zbozi.cz/hledej/?q=" + urllib.parse.quote(q) + ("" if page == 1 else f"&strana={page}")
            names = list(dict.fromkeys(re.findall(r'"name":"([^"]{5,120})"', http(url, ua=ua).replace("&quot;", '"'))))
            hit = [i for i, n in enumerate(names) if "Printopia" in n]
            if hit:
                found = (page, hit[0] + 1)
                break
        print(f"  „{q}“: {'strana %d, pořadí %d' % found if found else 'nenalezeno na stranách 1 až 3'}")


def seo():
    print("\n## seo: organická návštěvnost (zdroj v sekcích výše: návštěvy mimo `sklik`/`zbozi` = přímé nebo organické)")


def portfolio():
    print("\n## portfolio: má firma aspoň jeden business s verdiktem ANO/ANO? (plan/verdikt.py)")
    ok = []
    for f in sorted((ROOT / "plan").glob("hledanost-*.md")):
        t = f.read_text(encoding="utf-8")
        if "## Verdikt (automaticky)" not in t or f.stem.startswith("hledanost-alt-") or f.stem in ("hledanost-kandidati-2026-10-01",):
            continue
        ov = re.search(r"Ověřitelnost do \d+ dnů: \*\*(\w+)", t)
        ds = re.search(r"Dostatečný prodej: \*\*(\w+)", t)
        ex = "Výjimka schválená Ondřejem" in t
        print(f"  {f.stem[10:]}: ověřitelné {ov and ov.group(1)}, dostatečný prodej {ds and ds.group(1)}{', VÝJIMKA' if ex else ''}")
        if ov and ds and ov.group(1) == "ANO" and ds.group(1) == "ANO":
            ok.append(f.stem)
    alt = ROOT / "plan/alternativy.md"
    print(f"  alternativy: {'plan/alternativy.md existuje' if alt.exists() else 'CHYBÍ plan/alternativy.md'}")
    if not ok:
        ALERTS.append("portfolio: žádný business nemá verdikt ANO/ANO, hledat alternativu (plan/alternativy.md), posunout kandidáta o krok")


SECTIONS = {"sklik", "zbozi", "seo", "printopia", "anoberu", "portfolio"}  # názvy sekcí výše, značka [stav:<název>] v plan/akce.md
print("# Stav všech akcí", date.today())
sklik()
site("printopia", "https://printopia.cz", "STATS_KEY_PRINTOPIA", ".stats_key")
site("anoberu", "https://anoberu.cz", "STATS_KEY_ANOBERU", ".stats_key_anoberu")
zbozi()
seo()
portfolio()

print("\n## pokrytí akcí plan/akce.md")
for line in (ROOT / "plan/akce.md").read_text(encoding="utf-8").splitlines():
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cols) >= 5 and cols[0].isdigit() and not cols[3].startswith(("zamítnuto", "hotovo")):
        tags = re.findall(r"\[stav:([\w-]+)\]", cols[4])
        if not tags or any(t not in SECTIONS for t in tags):
            print(f"  CHYBÍ SLEDOVÁNÍ: akce #{cols[0]} ({cols[1][:40]}) nemá značku [stav:<sekce>] se sekcí ve tools/stav.py")
            ALERTS.append(f"akce #{cols[0]} nemá sledování")
        else:
            print(f"  akce #{cols[0]}: sleduje {', '.join(tags)}")

print("\n## ALERTY (nové věci, na které reagovat)")
print("\n".join(f"  - {a}" for a in ALERTS) if ALERTS else "  žádné")
sys.exit(1 if any("sledování" in a for a in ALERTS) else 0)
