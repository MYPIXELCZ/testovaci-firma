# Stav hlavní session (průběžný zápis, aby se po kompresi chatu neztratila nit)

Aktualizováno: 2026-10-02 15:20 Praha. Aktualizovat po každém významném kroku (nový pokyn Ondřeje, start nebo konec agenta, rozhodnutí, commit). Po kompresi nebo novém startu session ho přečíst jako první (vkládá ho hook `session-resume.py`), pak CLAUDE.md a FAILS.md.

## Kdo a kde
Hlavní session „TESTOVACÍ FIRMA“ (CCR `session_01N4ZDnfkuU5cm6b5gWA3X3Y`), větev `claude/hopeful-hamilton-n1pbnk` (push nasazuje do Vercel týmu MYPIXELCZ). Hodinová rutina `trig_01JwSBqqYubWBAPLvW1ZK1Te` (:25) a jednorázová připomínka `trig_01HsG7157SouDk5eMtpHKrbB` (15:28 Praha); po každém probuzení nová `send_later` za 60 minut. Ondřej píše česky, krátce; odpovědi jen s informační hodnotou.

## Cíl a pravidla (podrobně CLAUDE.md)
Cíl A: zisk ≥ 10 000 Kč měsíčně hned nebo doložená cesta do ~6 měsíců (dnes nezáporný), nebo B: pasivně, náklad ≤ ⅓ tržeb. Preference: automatizovaný produkt, pak 3D tisk, pak zakázkový web/systém/e-shop. Zahraniční placené služby povoleny (výdaj schvaluje Ondřej). Rozpočet zbývá ~700 Kč. Pravidla z FAILů dnes: verdikt/ověřitelnost, stav všech akcí (`tools/stav.py`), portfolio gate, zpětná platnost, normy přistávacího webu a zákaz „AI vzhledu“, modely se nemíchají (dávky), Vercel jen MYPIXELCZ, poradce ne přikyvovač (`plan/rozhodnuti.md`), podíl na trhu (SABLONA 2b), schopnost místo minulosti (2a), prezentace jako proměnná (2c).

## Stav businessů
Printopia a anoberu: verdikt NE/NE, pasivně, nic nepřepracovávat. Zboží.cz sonda běží (pozice 32 a 45; přeměřit 2026-10-03, vyhodnotit 2026-10-04). Sklik kredit ≈ 124 Kč bez DPH, 0 kliků. Doporučení Skliku: jen „dynamický retargeting návštěvníků Seznamu“ zvážit (akce #20 po 10-04). Web za 24 hodin: jen levná sonda zájmu, verdikt NE/NE, šance 20–25 %, riziko Vercel Terms čl. 11, Bazoš 147 Kč.

## Revize #13 (15:09–15:20, Ondřej sdělil nové fakty)
Ondřej má živé: mypixel.cz (MYPIXEL s.r.o., WordPress weby od 14 800 Kč, 85+ webů, 5,0 z 24 Google recenzí), webprodava.cz (jeho nabídka webů, provozovatel Ing. Ondřej Chloupek), ReviewBoost SaaS (reviewboost.cz, MYPIXEL s.r.o., 690 Kč/měs) a platí ePoptávku 500 Kč/měs. **Nechce poptávkové portály (duplicita)** → „Dílna na poptávky“ (#21) a stránka na webprodava.cz (#14) zrušeny, třída „web pro malé firmy“ duplikuje jeho byznys. Domény v CLAUDE.md nebyly volné (opraveno). Model: Sonnet 5.5 aktivní (`plan/model.txt`), agenti neběží. Portfolio gate: žádný business s ANO/ANO.

## Kandidáti teď
1. ReviewBoost jako business testovací firmy (#22): Seznam jen „google recenze“ 137/měs, bez Google dat nevím; čeká na Ondřejovu odpověď (je to jeho oddělený projekt? zákazníci?) a DataForSEO. 2. K4 digitální produkty Etsy (#23, pasivní, B ≈ 30 %, A ≈ 10 %): krok 0 DataForSEO. 3. K6 Shoptet doplněk po datech (nemáme zdroj dat bez portálů, nízká priorita). K5 3D tisk NE pro A.

## Čeká na Ondřeje
1. Rozhodnutí o směru: 🥇 ReviewBoost jako business testovací firmy (marketing, růst), 🥈 K4 Etsy, 🥉 nic nového. 2. Autorizace účtu DataForSEO (1 USD zdarma, bez karty; pro ReviewBoost i K4). 3. Oprava IČ v patičce mypixel.cz (17664578 patří Glow Wrapp s.r.o., správně 17617421); tvrzení „+47 recenzí v průměru“ na reviewboost.cz musí mít data (jinak klamavé, § 6b zákona 40/1995). 4. Search Console printopia.cz (nepotvrzeno).

## Další kroky (dávka Sonnet)
1. Po Ondřejově odpovědi: akce #22 nebo #23. 2. Zboží.cz přeměřit 10-03, vyhodnotit 10-04; #19, #20. 3. Každé probuzení: `python3 tools/stav.py`; send_later 60 min (trig_01HsG7157SouDk5eMtpHKrbB 15:28 Praha čeká).
