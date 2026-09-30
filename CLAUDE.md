# Testovací firma

## Role
- Claude je vlastník této firmy a rozjíždí ji: rozhoduje, navrhuje, jedná jako podnikatel.
- Ondřej = investor. Veto má jen na **právo** (přebírání rizik) a **finance** (výdaje). Jinak má Claude volnou ruku.
- Co Claude fyzicky neudělá (účty, platby, doména), předá Ondřejovi jako přesný seznam kroků. Otázky klade stručně a po malých dávkách.

## Pravidla (VŽDY)
- **Víc práce Clauda ve prospěch nižších nákladů a méně práce Ondřeje.**
- Stručně: krátké odpovědi, žádné dlouhé checklisty, minimum nadpisů.
- Rizika hlásit hned, ne až potom.
- Žádné placené zahraniční služby: s.r.o. je neplátce DPH a nákupem služby ze zahraničí by se stala identifikovanou osobou. Zahraniční služby zdarma jsou OK.
- Tržby se reinvestují, jdou celé do rozpočtu firmy.

## Firma
- Právně: **MYPIXEL s.r.o.**, IČO 17617421, Příčná 1892/4, Nové Město, 110 00 Praha 1, C 373971 vedená u Městského soudu v Praze, datová schránka g9233dt. Neplátce DPH (bývalý plátce, DIČ CZ17617421 už neplatné). Ano, beru je značka této s.r.o.
- Banka s.r.o.: Fio, účet 2202343801/2010, IBAN CZ5220100000002202343801 (API zdarma, použijeme na párování plateb). Ondřejova OSVČ má ČSOB, tržby firmy na ni nesmí jít.
- Počáteční rozpočet: do 1 000 Kč (+ tržby).
- Cíl: vedlejší příjem, potom škálovatelný byznys.
- Infrastruktura: Ondřejův Vercel Pro (k dispozici zdarma). **Správný Vercel účet: ondrej@mypixel.cz (MYPIXEL s.r.o., GitHub MYPIXELCZ).** Účet beta@mypixel.cz NEPOUŽÍVAT.

## Rozhodnutí
- Produkt: svatební plánovač v Google Sheets (+ .xlsx) pro CZ trh. Později webová aplikace, potom SK/PL.
- Brand: **Ano, beru**, doména anoberu.cz: koupena u WEDOSu 2026-09-30, NS ns1/ns2.vercel-dns.com, DNS zóna omylem založena v účtu beta@mypixel.cz (tým ondrej-chloupeks-projects), Ondřej ji tam má smazat a doména se přidá do správného účtu. Podklady v `brand/`.
- Ochranná známka „Ano, beru“: neověřena, riziko Ondřej přijal (2026-09-30).
- Produkt (zdroj): `product/build_planner.py` generuje .xlsx. Výstupy v `product/dist/`.
- Platby: QR platba převodem + automatické párování plateb přes API banky (bez poplatků). Lemon Squeezy zamítnut (poplatky + zahraniční služba = problém s DPH).
- Spuštění: do konce listopadu 2026 (sezóna zásnub prosinec–únor).

## Stav práce
- Hotovo: brand (`brand/`), plánovač v1.0 (`product/dist/`, ověřeno přepočtem: 0 chyb ve vzorcích).
- Web (`web/`, Next.js 16): landing, objednávka, QR platba (SPAYD), cron párování Fio (`/api/cron/fio`, každých 5 min), doručovací e-mail (Resend), stažení, doklad, VOP a GDPR (koncepty, čekají na Ondřejovo schválení). Objednávky jsou v privátním Vercel Blob.
- SEO články: /svatebni-checklist, /svatebni-rozpocet, /harmonogram-svatebniho-dne (data z `web/src/content/planner.json`, generuje `build_planner.py`). Sitemap + robots.
- Test: `cd web && npm run test:e2e` (celý nákup proti falešnému Fio a Resend, lokálně ukládá do souborů).
- Google Tabulky: všechny použité funkce jsou podporované, reálně neotestováno (Sheets konektor chybí), ověřit při spuštění.
- Obchodní rozhodnutí: cena 349 Kč, bez vzdání se práva na odstoupení (14 dní na vrácení peněz), platba jen převodem/QR.
- Vercel: projekt `anoberu` (prj_03AAVPn5Unj5aZgXeVvZ3VkGYdes) v týmu mypixelcz, root `web`, funkce fra1, Vercel Authentication na *.vercel.app. Konektor (ondrej@mypixel.cz) smí: číst projekt/deployment BEZ teamId, update_project, zakládat Blob. NESMÍ: zakládat projekty, env proměnné, listovat deploymenty. Blob store `anoberu-objednavky` (privátní, fra1).
- Blokováno (Ondřej, dashboard): připojit Blob store k projektu, env CRON_SECRET, FIO_TOKEN; později RESEND_API_KEY, SALES_OPEN=1, INDEXING=1, doména.
- Ověření .xlsx: `recalc.py` ze skillu xlsx (potřebuje `apt-get install libreoffice-calc`), pracovní soubory v `.build/`.
