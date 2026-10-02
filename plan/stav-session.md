# Stav hlavní session (průběžný zápis, aby se po kompresi chatu neztratila nit)

Aktualizováno: 2026-10-02 14:52 Praha. Aktualizovat po každém významném kroku (nový pokyn Ondřeje, start nebo konec agenta, rozhodnutí, commit). Po kompresi nebo novém startu session ho přečíst jako první (vkládá ho hook `session-resume.py`), pak CLAUDE.md a FAILS.md.

## Kdo a kde
Hlavní session „TESTOVACÍ FIRMA“ (CCR `session_01N4ZDnfkuU5cm6b5gWA3X3Y`), větev `claude/hopeful-hamilton-n1pbnk` (push nasazuje do Vercel týmu MYPIXELCZ). Hodinová rutina `trig_01JwSBqqYubWBAPLvW1ZK1Te` (:25) a jednorázová připomínka `trig_01HsG7157SouDk5eMtpHKrbB` (15:28 Praha); po každém probuzení nová `send_later` za 60 minut. Ondřej píše česky, krátce; odpovědi jen s informační hodnotou.

## Cíl a pravidla (podrobně CLAUDE.md)
Cíl A: zisk ≥ 10 000 Kč měsíčně hned nebo doložená cesta do ~6 měsíců (dnes nezáporný), nebo B: pasivně, náklad ≤ ⅓ tržeb. Preference: automatizovaný produkt, pak 3D tisk, pak zakázkový web/systém/e-shop. Zahraniční placené služby povoleny (výdaj schvaluje Ondřej). Rozpočet zbývá ~700 Kč. Pravidla z FAILů dnes: verdikt/ověřitelnost, stav všech akcí (`tools/stav.py`), portfolio gate, zpětná platnost, normy přistávacího webu a zákaz „AI vzhledu“, modely se nemíchají (dávky), Vercel jen MYPIXELCZ, poradce ne přikyvovač (`plan/rozhodnuti.md`), podíl na trhu (SABLONA 2b), schopnost místo minulosti (2a), prezentace jako proměnná (2c).

## Stav businessů
Printopia a anoberu: verdikt NE/NE, pasivně, nic nepřepracovávat. Zboží.cz sonda běží (pozice 32 a 45; přeměřit 2026-10-03, vyhodnotit 2026-10-04). Sklik kredit ≈ 124 Kč bez DPH, 0 kliků. Doporučení Skliku: jen „dynamický retargeting návštěvníků Seznamu“ zvážit (akce #20 po 10-04). Web za 24 hodin: jen levná sonda zájmu, verdikt NE/NE, šance 20–25 %, riziko Vercel Terms čl. 11, Bazoš 147 Kč.

## Kandidáti (`plan/alternativy-2026-10-02.md`)
1. K1+K2 lovec poptávek s paušálem 2 990 Kč (verdikt ANO/ANO na hraně, varianty prezentace 1 až 3 v dodatku), 2. K3 zakázkový web/systém/e-shop, 3. K4 digitální produkty (Etsy + Lemon Squeezy; krok 0 Keywords Everywhere 280 Kč), 3D tisk NE pro A, PPC služba jen jako vrstva k K2 (Ondřej 14:28 odsouhlasil, jen pokud dojde na K1+K2).

## Čeká na Ondřeje
1. (14:55 Ondřej se ptá na cenu přepnutí: nový dialog říká, že přepnutí znovu načte celou session; doporučeno 🥇 nový chat na Opus 5.5 jen pro #13 s promptem „přečti CLAUDE.md, plan/stav-session.md, plan/alternativy-2026-10-02.md, udělej #13, zapiš do plan/rozhodnuti-business.md, commit a push, bez agentů a bez send_later“; hlavní session zůstává na Sonnetu.) Přepnutí modelu na Opus 5.5: žádost ODESLÁNA 2026-10-02 14:52 („nic neběží“, `ListAgents` prázdné). Po jeho „přepnuto“ ověřit `get_session` (`session_context.model`), zapsat `plan/model.txt` „vyšší model aktivní: <model> (<datum>)“ a dělat jen #13 (a #14 až po schválení testu); potom napsat „přepni zpět na Sonnet 5.5“. 2. Po přepnutí: konečné rozhodnutí o businessu (#13). 3. K sondě K1+K2: výjimka z verdiktu, schválení podmínek služby (rozšířit `plan/web-za-24-hodin.md`), Webtrh Premium 465 Kč, odpovědi na Shoptet poptávky (veřejný e-mail e-shopu vs. ručně Ondřej), řádek „Výjimka schválená Ondřejem“. 4. Search Console ověření printopia.cz (nepotvrzeno).

## Agenti
Neběží žádný (ListAgents 14:52). Hotovo a commitnuto: zahraniční služby #15 (`plan/postupy/zahranicni-sluzby.md`: DataForSEO pro Google hledanost ≈ 1,3 Kč/100 dotazů, Seznam jen ≈ 15 % hledání, Etsy, Netlify místo Vercelu pro klienty; Ondřej by autorizoval DataForSEO účet, Etsy, Netlify, Search Console OAuth), konkurence webu, normy přistávacího webu (`plan/postupy/pristavaci-web.md`), kandidáti (`plan/alternativy-2026-10-02.md`), PPC (`plan/alt-ppc-sluzba.md`).

## Další kroky (pořadí)
1. (hotovo) agent #15 commitnut, žádost o Opus odeslána. 2. Čekat na „přepnuto“ jen u #13 a #14, ostatní dělat dál na Sonnetu. 3. V dávce Opus: znovu pořadí kandidátů s oddíly 2a/2b/2c, doporučení; pak napsat „přepni zpět na Sonnet 5.5“. 4. Akce #19 (test správy cizího Sklik účtu), #20. 5. Návrh přistávacího webu (#14) až po Ondřejově schválení testu. 6. Každé probuzení: `python3 tools/stav.py`.
