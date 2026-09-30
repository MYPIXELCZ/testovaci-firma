#!/usr/bin/env python3
"""Oznámí URL printopia.cz vyhledávačům (Seznam, Bing) přes IndexNow. Spustit po nasazení nových stránek."""
import json
import urllib.request

KEY = "11045f5901d96d29bb8a5588cf5115d1"  # veřejný klíč, soubor public/11045f5901d96d29bb8a5588cf5115d1.txt
URLS = ["https://printopia.cz/", "https://printopia.cz/zlomky-prijimacky", "https://printopia.cz/ochrana-osobnich-udaju"]

for endpoint in ["https://search.seznam.cz/indexnow", "https://www.bing.com/indexnow"]:
    body = json.dumps({"host": "printopia.cz", "key": KEY, "keyLocation": f"https://printopia.cz/{KEY}.txt", "urlList": URLS}).encode()
    req = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        print(endpoint, urllib.request.urlopen(req, timeout=20).status)
    except urllib.error.HTTPError as e:
        print(endpoint, e.code, e.read()[:200])
