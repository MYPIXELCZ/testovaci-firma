# Stav hlavní session (průběžný zápis, aby se po kompresi chatu neztratila nit)

Aktualizováno: 2026-10-07 20:05 Praha. Aktualizovat po každém významném kroku (nový pokyn Ondřeje, start nebo konec agenta, rozhodnutí, commit). Po kompresi nebo novém startu session ho přečíst jako první (vkládá ho hook `session-resume.py`), pak CLAUDE.md a FAILS.md.

## Kdo a kde
Hlavní session „TESTOVACÍ FIRMA“ (CCR `session_01N4ZDnfkuU5cm6b5gWA3X3Y`), větev `claude/hopeful-hamilton-n1pbnk` (push nasazuje do Vercel týmu MYPIXELCZ). **Hodinová rutina `trig_01JwSBqqYubWBAPLvW1ZK1Te` je VYPNUTÁ a jednorázová připomínka smazána (Ondřej 15:36); nic neplánovat, `send_later` nepoužívat.** Termíny: Zboží.cz přeměřit 2026-10-03, vyhodnotit do 2026-10-04 (bez připomínky, jen na Ondřejovo vyzvání). Ondřej píše česky, krátce; odpovědi jen s informační hodnotou.

## Cíl a pravidla (podrobně CLAUDE.md)
Cíl A: zisk ≥ 10 000 Kč měsíčně hned nebo doložená cesta do ~6 měsíců (dnes nezáporný), nebo B: pasivně, náklad ≤ ⅓ tržeb. Preference: automatizovaný produkt, pak 3D tisk, pak zakázkový web/systém/e-shop. Zahraniční placené služby povoleny (výdaj schvaluje Ondřej). Rozpočet zbývá ~700 Kč. Pravidla z FAILů dnes: verdikt/ověřitelnost, stav všech akcí (`tools/stav.py`), portfolio gate, zpětná platnost, normy přistávacího webu a zákaz „AI vzhledu“, modely se nemíchají (dávky), Vercel jen MYPIXELCZ, poradce ne přikyvovač (`plan/rozhodnuti.md`), podíl na trhu (SABLONA 2b), schopnost místo minulosti (2a), prezentace jako proměnná (2c).

## Stav businessů
**2026-10-07 20:00: PRVNÍ SKUTEČNÁ TRŽBA, Printopia 349 Kč (Fio, zdroj Sklik), `plan/printopia-vyhodnoceni-2026-10-07.md`. Zboží.cz sonda neúspěšná (0 zobrazení). Verdikt dál NE/NE; sbírat data bez výdajů. Google Cloud krok 1 od 2026-10-02 stále čeká na Ondřejovo „hotovo“.**
Printopia a anoberu: verdikt NE/NE, pasivně, nic nepřepracovávat. Zboží.cz sonda běží (pozice 32 a 45; přeměřit 2026-10-03, vyhodnotit 2026-10-04). Sklik kredit ≈ 124 Kč bez DPH, 0 kliků. Doporučení Skliku: jen „dynamický retargeting návštěvníků Seznamu“ zvážit (akce #20 po 10-04). Web za 24 hodin: jen levná sonda zájmu, verdikt NE/NE, šance 20–25 %, riziko Vercel Terms čl. 11, Bazoš 147 Kč.

## Revize #13 (15:09–15:20, Ondřej sdělil nové fakty)
Ondřej má živé: mypixel.cz (MYPIXEL s.r.o., WordPress weby od 14 800 Kč, 85+ webů, 5,0 z 24 Google recenzí), webprodava.cz (jeho nabídka webů, provozovatel Ing. Ondřej Chloupek), ReviewBoost SaaS (reviewboost.cz, MYPIXEL s.r.o., 690 Kč/měs) a platí ePoptávku 500 Kč/měs. **Nechce poptávkové portály (duplicita)** → „Dílna na poptávky“ (#21) a stránka na webprodava.cz (#14) zrušeny, třída „web pro malé firmy“ duplikuje jeho byznys. Domény v CLAUDE.md nebyly volné (opraveno). Model: Sonnet 5.5 aktivní (`plan/model.txt`), agenti neběží. Portfolio gate: žádný business s ANO/ANO.

## Kandidáti teď
1. ReviewBoost jako business testovací firmy (#22): Seznam jen „google recenze“ 137/měs, bez Google dat nevím; čeká na Ondřejovu odpověď (je to jeho oddělený projekt? zákazníci?) a DataForSEO. 2. K4 digitální produkty Etsy (#23, pasivní, B ≈ 30 %, A ≈ 10 %): krok 0 DataForSEO. 3. K6 Shoptet doplněk po datech (nemáme zdroj dat bez portálů, nízká priorita). K5 3D tisk NE pro A.

## Agenti
Žádný neběží (agent konkurence ReviewBoostu zastaven). Připomínky žádné.

## ReviewBoost: STOP (Ondřej 15:15)
Projekt má chybu, nesmím ho využít; nic jsem v jeho repu neměnil, lokální kopii smazal. Akce #22 zamítnuta. Zbývá K4 Etsy (#23, potřebuje DataForSEO) nebo nic.

## Ondřej zvolil 🥇 (15:21): Google Ads + Keyword Planner
Seznamy dotazů jsou v `plan/keyword-planner-seznamy.md` (A Česko, B USA); Ondřej je vloží do Plánovače klíčových slov a pošle mi CSV (pásma stačí). Po obdržení: do `plan/hledanost-*.md`, přepočítat K4 a dřívější kandidáty (Google ≈ 5× Seznam), nový verdikt a rozhodnutí. Ondřej 15:23 se ptá na API: nabídnuto 🥇 API Google Ads (Cloud projekt s fakturací, zapnout Google Ads API, ověření značky, Basic access automaticky, servisní účet + JSON klíč, e-mail přidat v Google Ads jako uživatele; od 9. 9. 2026 bez developer tokenu; egress do googleads.googleapis.com funguje) nebo 🥈 ruční export. Čeká na jeho volbu; po klíči napsat `plan/hledanost_google.py` (REST generateKeywordHistoricalMetrics).

## Google Ads API krok po kroku (Ondřej 15:27: účet Google Ads založen, chce kroky jednotlivě)
Krok 1 (dán 15:27): projekt `mypixel-ads-api` v Cloud Console + fakturace + zapnout Google Ads API; čeká na „krok 1 hotovo“. Další kroky: 2) Google Auth Platform → Branding (název, e-mail podpory, doména mypixel.cz) a ověření značky; v Google Ads API Overview zkontrolovat úroveň přístupu (výchozí Explorer, stačí zkusit; „Apply for access“ na Basic, může být automaticky nebo do 10 pracovních dnů); 3) servisní účet + JSON klíč (IAM → Servisní účty); 4) e-mail servisního účtu přidat v Google Ads (Správa → Přístup a zabezpečení → uživatel Standard) a předat mi ID účtu (10 číslic) a klíč; 5) já napíšu `plan/hledanost_google.py` (REST generateKeywordHistoricalMetrics) a ověřím. Pozor: dokumentace nejasná, zda je pro REST stále potřeba hlavička developer-token; ověřit po klíči.

## DataForSEO zamítnuto (Ondřej 15:19)
K4 Etsy tím nejde ověřit; navrženo 🥇 Google Ads účet + Keyword Planner (zdarma, pásma), 🥈 jen B-sondy bez dat, 🥉 pauza hledání (Printopia a anoberu zůstávají pasivní). Čeká na jeho volbu.

## Čeká na Ondřeje
1. Rozhodnutí o směru: 🥇 ReviewBoost jako business testovací firmy (marketing, růst), 🥈 K4 Etsy, 🥉 nic nového. 2. Autorizace účtu DataForSEO (1 USD zdarma, bez karty; pro ReviewBoost i K4). 3. Oprava IČ v patičce mypixel.cz (17664578 patří Glow Wrapp s.r.o., správně 17617421); tvrzení „+47 recenzí v průměru“ na reviewboost.cz musí mít data (jinak klamavé, § 6b zákona 40/1995). 4. Search Console printopia.cz (nepotvrzeno).

## Další kroky (dávka Sonnet)
1. Po Ondřejově odpovědi: akce #22 nebo #23. 2. Zboží.cz přeměřit 10-03, vyhodnotit 10-04; #19, #20. 3. Bez hodinových probuzení: `python3 tools/stav.py` jen na žádost.
