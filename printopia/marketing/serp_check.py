#!/usr/bin/env python3
"""Ověří na živém Seznamu, zda se naše reklama zobrazuje na klíčových slovech kampaně (nezávisle na zpožděných statistikách Skliku).

    python3 printopia/marketing/serp_check.py [dotaz ...]    bez parametru projde všechna klíčová slova ze sklik.py

Každé hledání je zobrazení reklamy navíc (bez kliknutí nic nestojí), proto nespouštět ve smyčce.
Výsledek kolísá mezi pokusy (aukce, rozložení rozpočtu přes den), jedno chybějící zobrazení nic neznamená.
"""
import html
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15"
spec = json.loads(subprocess.run([sys.executable, str(Path(__file__).with_name("sklik.py"))], check=True, capture_output=True, text=True).stdout)
queries = sys.argv[1:] or [k for g in spec["groups"].values() for k in g["keywords"]]
shown = 0
for q in queries:
    page = subprocess.run(["curl", "-s", "-m", "25", "-A", UA, "-L", "https://search.seznam.cz/?q=" + urllib.parse.quote(q)],
                          capture_output=True).stdout.decode("utf-8", "ignore")
    page = html.unescape(page)
    ads = sorted(set(re.findall(r"printopia\.cz/[^\"]*?utm_content%3D(\d+)", page)) | set(re.findall(r"printopia\.cz/\?utm_source=sklik&utm_term=\d+&utm_content=(\d+)", page)))
    total = len(set(re.findall(r'clickData":"adurl=https?://([^/&"\\]+)', page)))
    shown += bool(ads)
    print(f"{q}: reklam celkem {total}, naše {', '.join(ads) or '-'}")
print(f"Naše reklama se ukázala u {shown} z {len(queries)} dotazů.")
