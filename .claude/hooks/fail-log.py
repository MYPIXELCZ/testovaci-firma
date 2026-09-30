#!/usr/bin/env python3
# Zpráva od Ondřeje začínající "FAIL:" se automaticky zapíše do FAILS.md
# a Claude dostane pokyn doplnit příčinu a pojistku.
import datetime, json, os, sys

data = json.load(sys.stdin)
prompt = (data.get("prompt") or "").strip()
if not prompt.upper().startswith("FAIL:"):
    sys.exit(0)

root = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(root, "FAILS.md")
if not os.path.exists(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# FAILS\n\nChyby nahlášené Ondřejem (\"FAIL: ...\"). Každá má příčinu a pojistku, aby se neopakovala.\n")
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
text = prompt[5:].strip().replace("\n", " ")
with open(path, "a", encoding="utf-8") as f:
    f.write(f"\n## {stamp}\n- **Hlášení:** {text}\n- **Příčina:** (doplnit)\n- **Pojistka:** (doplnit)\n")

print(
    "Ondřej nahlásil FAIL; zapsáno do FAILS.md. Povinně: 1) doplň do FAILS.md příčinu a pojistku "
    "(pravidlo v CLAUDE.md, test, kontrola v kódu), 2) pojistku skutečně zaveď, 3) commitni a pushni, "
    "4) Ondřejovi stručně potvrď co se změnilo."
)
