# Printopia: kontrola odstoupení od smlouvy a kontaktu (2026-10-07, na dotaz Ondřeje; není právní stanovisko, právo = jeho veto)

Zdroje: nařízení vlády č. 29/2023 Sb. (vzorové poučení a vzorový formulář, příloha, platí od 18. 2. 2023, nahradilo 363/2013 Sb.; stáhnuto z zakonyprolidi.cz), Shoptet blog o odstoupení 2026 (stav „tlačítkové novely“), ČOI. Kód: `printopia/src/app/obchodni-podminky/page.tsx`, `src/lib/email.ts`, `src/app/koupit/OrderForm.tsx`.

## Co je v pořádku
- Tlačítko objednávky „Objednat s povinností platby“, souhlas s OP, údaje prodávajícího (MYPIXEL s.r.o., sídlo, IČO, rejstřík, neplátce DPH) v OP i patičce, e-mail printopia@mypixel.cz (patička, OP § 6, 7, 8, e-maily mají reply-to), odstoupení do 14 dnů od uzavření smlouvy (správný začátek lhůty u digitálního obsahu), vrácení do 14 dnů stejným způsobem, ADR u ČOI (platforma ODR EU už od 7/2025 není potřeba), vady podle § 2389a a násl., funkčnost digitálního obsahu (PDF k tisku). Výjimku pro digitální obsah (§ 1837 písm. l) nevyužíváme, takže „14 dní na vrácení peněz“ platí i po stažení (obchodní rozhodnutí).

## Mezery
1. **E-maily neobsahují poučení o právu na odstoupení ani vzorový formulář ani OP.** Web není trvalý nosič, potvrzení smlouvy s informacemi má jít na trvalém nosiči (e-mail s textem nebo přílohou PDF). Důsledek: lhůta pro odstoupení se může prodloužit až na 1 rok a 14 dní a hrozí pokuta ČOI za porušení informačních povinností.
2. **Chybí vzorový formulář pro odstoupení** (příloha NV 29/2023) a stránka s ním; OP § 6 zná jen e-mail s číslem objednávky.
3. **Tlačítková novela** (odstoupení online dvěma kliknutími, jen digitální obsah a e-shopy jsou povinné): Sněmovna schválila 2026-07-10, čeká na Senát, očekávané účinnosti leden 2027; připravit předem (online formulář + potvrzení e-mailem).
4. Telefon: nemáme. Vzorové poučení po něm žádá („telefonní číslo a adresu pro e-mail“), zákon ho ukládá jen pokud je k dispozici; e-mail jako přímý a rychlý kontakt stačí (rozsudek SDEU C‑266/19). Doporučení: jen e-mail, rozhodnutí je Ondřejovo.

## Navržená oprava (čeká na „ano“ Ondřeje, právní text)
- Stránka `/odstoupeni-od-smlouvy`: vzorové poučení (varianta „uzavření smlouvy“, digitální obsah) a vzorový formulář podle NV 29/2023, online formulář (jméno, e-mail, číslo objednávky) s druhým potvrzovacím krokem, odeslání e-mailem na printopia@mypixel.cz + potvrzení zákazníkovi.
- E-mail po objednávce (platební údaje) doplnit o: poučení, vzorový formulář, OP (PDF příloha nebo text), odkaz na stránku odstoupení; e-mail s doručením odkaz.
- OP § 6: jiné jednoznačné prohlášení (např. dopis na sídlo), odkaz na formulář a stránku, text podle vzorového poučení.
- Postup refundu: odstoupení čte Claude (e-mail), vrácení z Fio provádí Ondřej (autorizace platby); lhůta 14 dní od odstoupení.
