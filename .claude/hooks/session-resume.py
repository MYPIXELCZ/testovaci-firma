#!/usr/bin/env python3
# Pojistka z FAILS.md 2026-10-02 14:46: po kompresi chatu nebo novém startu hlavní session vložit do kontextu průběžný stav,
# aby se neztratila nit. Vypíše plan/stav-session.md (stdout SessionStart hooku se přidá do kontextu).
import json
import os
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# jen hlavní session (jiné chaty v repozitáři ignorovat), stejně jako Stop hook
main = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main-session.txt")
ids = [l.strip() for l in open(main, encoding="utf-8") if l.strip() and not l.startswith("#")] if os.path.exists(main) else []
remote = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "")
if ids and not any(i == data.get("session_id") or (remote and remote.endswith(i)) for i in ids):
    sys.exit(0)
path = os.path.join(root, "plan", "stav-session.md")
if os.path.exists(path):
    print("OBNOVENÍ NITI (hook session-resume): přečti nejdřív tento průběžný stav, potom CLAUDE.md a FAILS.md, a pokračuj od bodu „Další kroky“. Nic z toho neodpovídej Ondřejovi, jen naváž.\n")
    print(open(path, encoding="utf-8").read())
