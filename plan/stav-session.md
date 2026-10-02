# Stav hlavní session (průběžný zápis, aby se po kompresi chatu neztratila nit)

Aktualizováno: 2026-10-02 15:05 Praha. Aktualizovat po každém významném kroku (nový pokyn Ondřeje, start nebo konec agenta, rozhodnutí, commit). Po kompresi nebo novém startu session ho přečíst jako první (vkládá ho hook `session-resume.py`), pak CLAUDE.md a FAILS.md.

## Kdo a kde
Hlavní session „TESTOVACÍ FIRMA“ (CCR `session_01N4ZDnfkuU5cm6b5gWA3X3Y`), větev `claude/hopeful-hamilton-n1pbnk` (push nasazuje do Vercel týmu MYPIXELCZ). Hodinová rutina `trig_01JwSBqqYubWBAPLvW1ZK1Te` (:25) a jednorázová připomínka `trig_01HsG7157SouDk5eMtpHKrbB` (15:28 Praha); po každém probuzení nová `send_later` za 60 minut. Ondřej píše česky, krátce; odpovědi jen s informační hodnotou.

## Cíl a pravidla (podrobně CLAUDE.md)
Cíl A: zisk ≥ 10 000 Kč měsíčně hned nebo doložená cesta do ~6 měsíců (dnes nezáporný), nebo B: pasivně, náklad ≤ ⅓ tržeb. Preference: automatizovaný produkt, pak 3D tisk, pak zakázkový web/systém/e-shop. Zahraniční placené služby povoleny (výdaj schvaluje Ondřej). Rozpočet zbývá ~700 Kč. Pravidla z FAILů dnes: verdikt/ověřitelnost, stav všech akcí (`tools/stav.py`), portfolio gate, zpětná platnost, normy přistávacího webu a zákaz „AI vzhledu“, modely se nemíchají (dávky), Vercel jen MYPIXELCZ, poradce ne přikyvovač (`plan/rozhodnuti.md`), podíl na trhu (SABLONA 2b), schopnost místo minulosti (2a), prezentace jako proměnná (2c).

## Stav businessů
Printopia a anoberu: verdikt NE/NE, pasivně, nic nepřepracovávat. Zboží.cz sonda běží (pozice 32 a 45; přeměřit 2026-10-03, vyhodnotit 2026-10-04). Sklik kredit ≈ 124 Kč bez DPH, 0 kliků. Doporučení Skliku: jen „dynamický retargeting návštěvníků Seznamu“ zvážit (akce #20 po 10-04). Web za 24 hodin: jen levná sonda zájmu, verdikt NE/NE, šance 20–25 %, riziko Vercel Terms čl. 11, Bazoš 147 Kč.

## Rozhodnutí #13 (hotovo 15:0x na Opus 5.5, `plan/rozhodnuti-business.md`)
Jeden business „Dílna na poptávky“ (K1 úkol + K2 balíček 2 990 Kč + K3 projekt 15–60 tis.), sonda odpověďmi na poptávky, varianty V1–V4, akce #21; Bazoš test zrušen; K4 jen krok 0 (DataForSEO), K6 po datech, K5 NE. Šance na A ≈ 25 % (výhrada zapsána v dokumentu).

## Čeká na Ondřeje
1. „ano, sonda poptávek“. 2. Shoptet (reCAPTCHA): 🥇 odesílá on (≈ 1 min na kus, ≈ 25 měsíčně), 🥈 vynechat, 🥉 e-mail na veřejný kontakt (nedoporučeno). 3. Podmínky služby (připravím). 4. Webtrh Premium 465 Kč, jen pokud nutné. 5. E-mail dílny čitelný přes Gmail konektor, registrace zkušebního Shoptetu. 6. Search Console printopia.cz (nepotvrzeno). 7. Přepnout zpět na Sonnet 5.5 (požádáno 15:0x).

## Agenti
Neběží žádný.

## Další kroky (pořadí, dávka Sonnet)
1. Po „přepnuto zpět“: `plan/model.txt` přepsat na „sonnet aktivní“. 2. Ověření 2a: Playwright na cizí HTTPS (README: NSS store nastaven), kdo smí odpovídat na Shoptet poptávky, Webtrh Premium (nutnost, cena, období), placený kontakt u ePoptávky a Poptavky.cz. 3. Tři vzorové odpovědi na živé poptávky s kusem řešení. 4. Podmínky služby dílny (rozšířit `plan/web-za-24-hodin.md`). 5. `plan/sonda-poptavky.csv` a sekce v `tools/stav.py`. 6. #14 stránka dílny až po schválení (vyšší model). 7. Zboží.cz přeměřit 10-03, vyhodnotit 10-04; #19, #20. 8. Každé probuzení: `python3 tools/stav.py`.
