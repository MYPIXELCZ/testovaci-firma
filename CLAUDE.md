# Testovací firma

## Role
- Claude je vlastník této firmy a rozjíždí ji: rozhoduje, navrhuje, jedná jako podnikatel.
- Ondřej = investor. Veto má jen na **právo** (přebírání rizik) a **finance** (výdaje). Jinak má Claude volnou ruku.
- Co Claude fyzicky neudělá (účty, platby, doména), předá Ondřejovi jako přesný seznam kroků. Otázky klade stručně a po malých dávkách.

## Pravidla (VŽDY)
- **Nečekat na Ondřeje.** Jeho kroky shrnout jednou a stručně, pak hned pokračovat ve všem, co jimi není blokované. Nikdy nekončit práci jen proto, že něco čeká na něj.
- **Nezastavovat se:** běží trvalá hodinová připomínka (Routine `trig_01JwSBqqYubWBAPLvW1ZK1Te`, každou hodinu v :25 do této session). Při každém spuštění: kontrola stavu, navázat na Ondřejovy kroky, jinak další neblokovaná práce. Vypnout jen na Ondřejův pokyn (update_trigger enabled=false).
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
- Web (`web/`, Next.js 16): landing, objednávka, QR platba (SPAYD), cron párování Fio (`/api/cron/fio`, každých 5 min), doručovací e-mail (Resend), stažení, doklad, VOP a GDPR (schváleny Ondřejem 2026-09-30). Objednávky jsou v privátním Vercel Blob.
- SEO články: /svatebni-checklist, /svatebni-rozpocet, /harmonogram-svatebniho-dne, /seznam-hostu-na-svatbu, /zasedaci-poradek-svatba (seznam v `web/src/content/articles.ts`) (data z `web/src/content/planner.json`, generuje `build_planner.py`). Sitemap + robots.
- Test: `cd web && npm run test:e2e` (celý nákup proti falešnému Fio a Resend, lokálně ukládá do souborů).
- Google Tabulky: všechny použité funkce jsou podporované, reálně neotestováno (Sheets konektor chybí), ověřit při spuštění.
- Testovací režim: objednávka přes *.vercel.app (chráněno Vercel Authentication) = 1 Kč, projde i s vypnutým prodejem, doklad označen jako testovací. Cron páruje vždy.
- Marketing: `marketing/prispevky.md` (FB skupiny, jen otevřeně za značku), piny `marketing/piny/` (generuje `render.mjs`), checklist k tisku `web/public/ke-stazeni/svatebni-checklist-anoberu.pdf` (generuje `marketing/checklist-pdf/render.mjs`).
- Obchodní rozhodnutí: cena 349 Kč, bez vzdání se práva na odstoupení (14 dní na vrácení peněz), platba jen převodem/QR.
- Vercel: projekt `anoberu` (prj_03AAVPn5Unj5aZgXeVvZ3VkGYdes) v týmu mypixelcz (team_fNHd0fCTFAA6MuEnT4BlEeWu), root `web`, funkce fra1, Vercel Authentication na *.vercel.app. Konektor má plný přístup k projektu (po rozšíření autorizace). Blob `anoberu-orders` (privátní, fra1, připojený). Nepoužitý prázdný store `anoberu-objednavky` (store_PzJcBM5ask99PXx1) smazat. Env: BLOB_READ_WRITE_TOKEN, CRON_SECRET, SITE_URL. Diagnostika: /api/health (na anoberu.cz jen ok/nok). web_fetch_vercel_url na *.vercel.app končí na SSO; automation bypass zamítnut bezpečnostním pravidlem, neobcházet. Tajemství (FIO_TOKEN, RESEND_API_KEY) buď env, nebo privátní úložiště přes https://anoberu-mypixelcz.vercel.app/nastaveni (jen pro přihlášené do Vercelu). Build se přeskočí, když se nezměnil `web/`.
- FIO_TOKEN uložen přes /nastaveni a ověřen u banky (2026-09-30). RESEND_API_KEY uložen (jen odesílání). Doménu anoberu.cz v Resendu (EU) založil Ondřej; DNS záznamy zadává na WEDOSu.
- DNS zůstává na WEDOSu (konektor nesmí zapisovat DNS záznamy ve Vercelu). Ondřej zadává: A @ 76.76.21.21, CNAME www → cname.vercel-dns.com, Resend TXT resend._domainkey, CNAME rsend/send, TXT _dmarc. Při spuštění: SALES_OPEN=1, INDEXING=1.
- Ověření .xlsx: `recalc.py` ze skillu xlsx (potřebuje `apt-get install libreoffice-calc`), pracovní soubory v `.build/`.
