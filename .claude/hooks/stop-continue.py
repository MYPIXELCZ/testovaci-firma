#!/usr/bin/env python3
# Pojistka z FAILS.md (2026-10-01 01:19): před ukončením tahu se jednou zastavit a ověřit,
# že je naplánovaná hodinová připomínka (do 2026-10-01 04:12 5min) a že nezbývá neblokovaná práce. Druhý pokus o stop už projde.
import json
import os
import sys

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)

# Hodinové kontroly patří JEN hlavní session „TESTOVACÍ FIRMA“ (FAILS.md 2026-10-01 17:02). Jiné chaty v repozitáři hook ignoruje.
main = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main-session.txt")
ids = [l.strip() for l in open(main, encoding="utf-8") if l.strip() and not l.startswith("#")] if os.path.exists(main) else []
remote = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "")
if not any(i == data.get("session_id") or (remote and remote.endswith(i)) for i in ids):
    sys.exit(0)
# Další krok z plan/akce.md (první řádek ve stavu „další“ nebo „research“): čekání na nepravděpodobné není práce (FAILS.md 2026-10-01 17:17).
nxt = ""
akce = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plan", "akce.md")
if os.path.exists(akce):
    for line in open(akce, encoding="utf-8"):
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) >= 5 and cols[3] in ("další", "research"):
            nxt = f" Další krok z plan/akce.md: #{cols[0]} {cols[1]}: {cols[4]}"
            break
print(json.dumps({
    "decision": "block",
    "reason": ("Kontrola před koncem tahu (FAILS.md): 1) Je naplánovaný send_later za 1 hodinu? Pokud ne, naplánuj ho (delay_minutes 60). "
               "2) Zbývá neblokovaná práce s perspektivou (i když od Ondřeje chybí informace)? Pokud ano, pokračuj v ní. "
               "3) Spustil jsi v tomto probuzení `python3 tools/stav.py` a zareagoval na VŠECHNY ALERTY (ne jen na aktuální akci)? Má firma business s verdiktem ANO/ANO, jinak posunul jsi kandidáta z plan/alternativy.md? "
               "4) Čekáš na událost, která nastane v následujících hodinách/dnech s pravděpodobností pod ~20 %? To není čekání, ale chybějící akce: udělej další krok z plan/akce.md nebo ji doplň." + nxt + " "
               "Tah ukonči jen tehdy, když je připomínka naplánovaná a vše ostatní čeká na Ondřeje."),
}, ensure_ascii=False))
