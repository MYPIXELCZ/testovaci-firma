#!/usr/bin/env python3
# Pojistka z FAILS.md (2026-10-01 01:19): před ukončením tahu se jednou zastavit a ověřit,
# že je naplánovaná 5min připomínka a že nezbývá neblokovaná práce. Druhý pokus o stop už projde.
import json
import sys

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)
print(json.dumps({
    "decision": "block",
    "reason": ("Kontrola před koncem tahu (FAILS.md): 1) Je naplánovaný send_later za 5 min? Pokud ne, naplánuj ho. "
               "2) Zbývá neblokovaná práce s perspektivou (i když od Ondřeje chybí informace)? Pokud ano, pokračuj v ní. "
               "Tah ukonči jen tehdy, když je připomínka naplánovaná a vše ostatní čeká na Ondřeje."),
}, ensure_ascii=False))
