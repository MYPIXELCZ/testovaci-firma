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
- Banka s.r.o.: Fio (API zdarma, použijeme na párování plateb). Ondřejova OSVČ má ČSOB, tržby firmy na ni nesmí jít.
- Počáteční rozpočet: do 1 000 Kč (+ tržby).
- Cíl: vedlejší příjem, potom škálovatelný byznys.
- Infrastruktura: Ondřejův Vercel Pro (k dispozici zdarma).

## Rozhodnutí
- Produkt: svatební plánovač v Google Sheets (+ .xlsx) pro CZ trh. Později webová aplikace, potom SK/PL.
- Brand: **Ano, beru**, doména anoberu.cz: schválena 2026-09-30, koupí ji Ondřej u CZ registrátora na s.r.o., NS přesměruje na Vercel. Podklady v `brand/`.
- Ochranná známka „Ano, beru“: neověřena, riziko Ondřej přijal (2026-09-30).
- Produkt (zdroj): `product/build_planner.py` generuje .xlsx. Výstupy v `product/dist/`.
- Platby: QR platba převodem + automatické párování plateb přes API banky (bez poplatků). Lemon Squeezy zamítnut (poplatky + zahraniční služba = problém s DPH).
- Spuštění: do konce listopadu 2026 (sezóna zásnub prosinec–únor).

## Stav práce
- Hotovo: brand (`brand/`), plánovač v1.0 (`product/dist/`, ověřeno přepočtem: 0 chyb ve vzorcích).
- Další: prodejní web na Vercelu, objednávky, QR platby + párování přes Fio API, automatické doručení a doklad.
- Ověření .xlsx: `recalc.py` ze skillu xlsx (potřebuje `apt-get install libreoffice-calc`), pracovní soubory v `.build/`.
