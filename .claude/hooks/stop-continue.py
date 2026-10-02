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
# Průběžný stav proti ztrátě niky po kompresi chatu (FAILS.md 2026-10-02 14:46)
stale = ""
state = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plan", "stav-session.md")
if os.path.exists(state):
    import time
    age = (time.time() - os.path.getmtime(state)) / 60
    if age > 40:
        stale = f"0) `plan/stav-session.md` je starý {age:.0f} min: před koncem tahu ho aktualizuj (kdo čeká na Ondřeje, běžící agenti, rozhodnutí, další kroky) a commitni, ať se po kompresi chatu neztratí nit. "
else:
    stale = "0) Chybí `plan/stav-session.md`, založ ho (stav, čeká na Ondřeje, agenti, další kroky). "
print(json.dumps({
    "decision": "block",
    "reason": ("Odpověď Ondřejovi bez výčtu těchto bodů: jen co se změnilo, co potřebuješ od něj a rizika (CLAUDE.md „Stručně“). Kontrola před koncem tahu (FAILS.md): " + stale + "1) Je naplánovaný send_later za 1 hodinu? Pokud ne, naplánuj ho (delay_minutes 60). "
               "2) Zbývá neblokovaná práce s perspektivou (i když od Ondřeje chybí informace)? Pokud ano, pokračuj v ní. "
               "3) Spustil jsi v tomto probuzení `python3 tools/stav.py` a zareagoval na VŠECHNY ALERTY (ne jen na aktuální akci)? Má firma business s verdiktem ANO/ANO, jinak posunul jsi kandidáta z plan/alternativy.md? "
               "4) Čekáš na událost, která nastane v následujících hodinách/dnech s pravděpodobností pod ~20 %? To není čekání, ale chybějící akce: udělej další krok z plan/akce.md nebo ji doplň." + nxt + " "
               "5) Potřebuje některá úloha vyšší model než Sonnet 5.5 (návrh vzhledu webu, volba businessu, audit)? Modely se nemíchají: o přepnutí žádej až když `ListAgents` nic nebězí a všechny úlohy pro Sonnet jsou dodělané; v dávce vyššího modelu spouštěj agenty jen na úlohy pro něj a po úloze požádej o přepnutí zpět (CLAUDE.md „Model“). "
               "6) Hodnotil jsi nové pokyny a nápady Ondřeje kriticky? Pokud s něčím nesouhlasíš, řekni to jednou věcně s alternativou (🥇🥈🥉); když na tom Ondřej trvá, jeho veto platí a zapiš to do plan/rozhodnuti.md. "
               "7) Nasazoval jsi web nebo domény na Vercel? Smí jen tým MYPIXELCZ (team_fNHd0fCTFAA6MuEnT4BlEeWu), nikdy jiný (JOYMARK…): teamId v každém volání a get_project accountId po založení. "
               "Tah ukonči jen tehdy, když je připomínka naplánovaná a vše ostatní čeká na Ondřeje."),
}, ensure_ascii=False))
