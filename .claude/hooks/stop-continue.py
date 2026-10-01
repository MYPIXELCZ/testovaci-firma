#!/usr/bin/env python3
# Pojistka z FAILS.md (2026-10-01 01:19): před ukončením tahu se jednou zastavit a ověřit,
# že je naplánovaná hodinová připomínka (do 2026-10-01 04:12 5min) a že nezbývá neblokovaná práce. Druhý pokus o stop už projde.
import json
import sys

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)
print(json.dumps({
    "decision": "block",
    "reason": ("Kontrola před koncem tahu (FAILS.md): 1) Je naplánovaný send_later za 1 hodinu? Pokud ne, naplánuj ho (delay_minutes 60). "
               "2) Zbývá neblokovaná práce s perspektivou (i když od Ondřeje chybí informace)? Pokud ano, pokračuj v ní. "
               "Tah ukonči jen tehdy, když je připomínka naplánovaná a vše ostatní čeká na Ondřeje."),
}, ensure_ascii=False))
