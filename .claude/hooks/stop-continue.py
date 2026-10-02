#!/usr/bin/env python3
# Pojistka z FAILS.md (2026-10-01 01:19): před ukončením tahu se jednou zastavit a ověřit připomínku a neblokovanou práci.
# Zkráceno 2026-10-02 14:50 kvůli tokenům (text se opakuje na konci každého tahu); podrobnosti v CLAUDE.md.
import json
import os
import sys
import time

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)

here = os.path.dirname(os.path.abspath(__file__))
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(here))
# Hodinové kontroly patří JEN hlavní session „TESTOVACÍ FIRMA“ (FAILS.md 2026-10-01 17:02).
main = os.path.join(here, "main-session.txt")
ids = [l.strip() for l in open(main, encoding="utf-8") if l.strip() and not l.startswith("#")] if os.path.exists(main) else []
remote = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "")
if not any(i == data.get("session_id") or (remote and remote.endswith(i)) for i in ids):
    sys.exit(0)

nxt = ""
akce = os.path.join(root, "plan", "akce.md")
if os.path.exists(akce):
    for line in open(akce, encoding="utf-8"):
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) >= 5 and cols[3] in ("další", "research"):
            nxt = f" Další krok: #{cols[0]} {cols[1][:90]}."
            break
state = os.path.join(root, "plan", "stav-session.md")
stale = ""
if not os.path.exists(state):
    stale = " Chybí plan/stav-session.md, založ ho."
else:
    age = (time.time() - os.path.getmtime(state)) / 60
    if age > 40:
        stale = f" plan/stav-session.md je starý {age:.0f} min: aktualizuj a commitni."
print(json.dumps({
    "decision": "block",
    "reason": ("Konec tahu (bez výčtu Ondřejovi, jen nové věci, žádost o něj, rizika). Ověř: "
               "`python3 tools/stav.py` puštěn a ALERTY vyřízeny; neblokovaná práce pokračuje; nečekáš na událost s P<20 %; "
               "modely se nemíchají (ListAgents před žádostí o přepnutí); nový pokyn Ondřeje posouzen kriticky (výhrada jednou, veto platí, `plan/rozhodnuti.md`); "
               "Vercel jen tým MYPIXELCZ; stav v plan/stav-session.md." + stale + nxt),
}, ensure_ascii=False))
