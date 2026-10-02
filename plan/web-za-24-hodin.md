# Web za 24 hodin: návrh testu (jen texty a podmínky, nic nestavět do výjimky Ondřeje)

**Korekce podle průzkumu agenta 2026-10-02 (`plan/konkurence-web-za-24-hodin.md`, `plan/postupy/web-za-24-hodin.md`), platí před textem níže:**
- Náklad testu NENÍ 0 Kč: Bazoš ve Službách stojí 49 Kč vložení a 49 Kč každé TOP (7× TOP = 392 Kč za 28 dní), test se 2× TOP = 147 Kč. Sbazar je zdarma (TOP 29 Kč). Výdaj schvaluje Ondřej (finance, jeho veto). Bazoš vyžaduje SMS ověření a mikroplatbu 1 Kč z bankovního účtu spojeného s telefonem.
- Název a IČO firmy musí být na konci inzerátu (pravidlo Bazoše, žádný z 47 konkurentů to nedělá, porušení = smazání bez vrácení poplatku).
- **Právní riziko pro Ondřejovo veto: hosting cizích webů na Vercelu.** Fair Use dovoluje na Pro komerční hostování, ale Terms čl. 11 (i) zakazuje zpřístupnit službu třetí straně. Navrhuji prodávat „provoz a správu“ bez přístupu klienta do Vercelu, plán B je export souborů ke klientovi na jeho hosting, plán C (po FAILu 14:08 zahraniční služba není překážka) je hosting klientských webů u jiné služby bez zákazu třetích stran (Cloudflare Pages, Netlify, WEDOS; ověřit podmínky a cenu, akce #15), a před spuštěním písemné potvrzení od Vercel supportu, pokud zůstane Vercel.
- Nesmí se tvrdit „bez AI“ (klamavé jednání) ani „autorská práva přejdou na vás“ (výstup AI nemusí být autorské dílo, rozsudek MS Praha 10 C 13/2023): v podmínkách jen licence k užití, v textu mluvit o výsledku, termínu a záruce.
- Cena 3 990 až 4 990 Kč je střed trhu (medián Bazoše 3 999 Kč), „24 hodin“ slibuje 7 konkurentů. Odlišení: jedna cena na první rok včetně domény, hostingu a SSL, termín s datem po podkladech, vrácení peněz, tabulka „co v ceně je a není“, náhled před zaplacením (standard trhu: platba až po schválení náhledu, náhled jen neindexovaný).
- Odhad za 72 h: P(≥1 závazná poptávka) ≈ 20 až 25 % (ne 40 %), jeden inzerát se 7× TOP dá ~0,5 zakázky měsíčně (~2 300 Kč tržeb). Samotný Bazoš/Sbazar cíl 10 000 Kč zisku měsíčně nesplní, test je levná sonda zájmu a je třeba ho prodloužit na 7 dní (0 dotazů za 72 h je jen slabé NE).

Stav: NÁVRH 2026-10-02. Verdikt kanálu Seznam je NE (nízká hledanost), proto kanál = inzertní portály s vlastní návštěvností. Stavět se začne až po „Výjimka schválená Ondřejem: sonda Web za 24 hodin, náklad 0 Kč, 72 h“ (zapsat sem i do `plan/hledanost-web-za-24-hodin.md`). Průzkum konkurence a pravidel portálů dělá agent do `plan/konkurence-web-za-24-hodin.md` a `plan/postupy/web-za-24-hodin.md`; inzerát nezveřejnit před odškrtnutým seznamem.

## Cílová skupina
- Kdo hledá: živnostník nebo majitel malé firmy (řemeslo, služby, kosmetika, doprava, účetní…), který nemá web nebo má zastaralý a nechce řešit agenturu za desítky tisíc.
- Kdo používá: jeho zákazníci (hledají kontakt, ceník, reference, mapu).
- Kdo platí: podnikatel (IČO). Prodáváme jen podnikatelům (B2B): spotřebitelská práva (14 dní, informační povinnosti B2C) se neuplatní, ověřit IČO při objednávce.
- Data: zatím žádná, to je účel testu (počet poptávek za 72 h).

## Nabídka
- **Web na jednu stránku 3 990 Kč** (úvod, služby, ceník nebo reference, kontakt s mapou a formulářem, pro mobil i PC, základ SEO, ukázkové fotky z Unsplash). **Malý web do 5 stránek 4 990 Kč.** Ceny konečné (jsme neplátce DPH).
- Hotová první verze **do 24 hodin od zaplacené zálohy a úplných podkladů**, 2 kola úprav v ceně.
- Domény klient registruje na sebe (u českého registrátora), my nastavíme propojení. Hosting v ceně prvních 12 měsíců, potom volitelně **správa 290 Kč měsíčně** (hosting, drobné změny textů do 30 minut měsíčně, výpověď kdykoli ke konci měsíce).
- Záruka: pokud web neodpovídá odsouhlasenému rozsahu a nedokážeme to opravit, vrátíme zálohu.
- Platba QR převodem: 50 % záloha, 50 % při předání. Párování přes Fio už máme (kód z `web/` a `printopia/`).

## Návrh obchodních podmínek služby (k schválení Ondřejem, právo)
1. Poskytovatel: MYPIXEL s.r.o., IČO 17617421, Příčná 1892/4, 110 00 Praha 1, neplátce DPH. Služba je určena jen podnikatelům a právnickým osobám.
2. Předmět: zhotovení a nasazení webu v rozsahu objednaného balíčku. Zadání se uzavírá e-mailovou objednávkou a zálohovou fakturou.
3. Termín: první verze do 24 hodin od připsání zálohy a doručení úplných podkladů (název, kontakty, texty nebo odpovědi na dotazník, logo, vlastní fotky). Doba čekání na klienta se do lhůty nepočítá.
4. Úpravy: dvě kola připomínek v ceně, další práce 490 Kč za započatou hodinu po předchozím odsouhlasení.
5. Podklady klienta: klient odpovídá, že má k textům, logu a fotkám práva a že jejich obsah neporušuje právo. Poskytovatel neodpovídá za správnost údajů dodaných klientem.
6. Licence: po úplném zaplacení získává klient neomezenou nevýhradní licenci k užití webu bez časového a územního omezení; šablony a knihovny třetích stran se řídí svými licencemi (např. fotky Unsplash).
7. Osobní údaje: klient je správcem údajů z formuláře na svém webu; při správě poskytovatel vystupuje jako zpracovatel podle přiložené zpracovatelské smlouvy. Web neobsahuje sledovací skripty bez souhlasu (cookie lišta jen tam, kde je potřeba).
8. Záruka a reklamace: vady odpovídající odsouhlasenému rozsahu opravíme zdarma do 14 dní od předání; nelze-li opravit, vrátíme zaplacenou cenu. Odpovědnost je omezena na výši zaplacené ceny, nevzniká za ušlý zisk.
9. Správa (volitelná): 290 Kč měsíčně, fakturace měsíčně převodem, výpověď písemně (e-mail) ke konci měsíce. Při neplacení po 14 dnech od splatnosti může být web pozastaven.
10. Rozhodné právo české, spory u soudu podle sídla poskytovatele. Znění podmínek se vkládá do objednávky.

Rizika k posouzení Ondřejem (právo, jeho veto): (a) hosting webů klientů na jeho Vercelu (Pro, komerční použití je v pořádku, ale ověřit v podmínkách Vercelu pro třetí strany; alternativa: klient má vlastní hosting, my jen předáme soubory), (b) odpovědnost za vady AI obsahu a autorská práva k textům a fotkám, (c) zpracovatelská smlouva GDPR u správy, (d) slib „do 24 hodin“ musí platit (kapacita Clauda ověřena: web na jednu stránku sestavím do hodin).

## Texty
Inzerát (Bazoš, sekce Služby; délku upravit podle pravidel portálu):

> **Web pro živnostníky a firmy za 24 hodin, od 3 990 Kč**
> Nemáte web, nebo máte starý? Připravíme vám moderní web na jednu stránku (služby, ceník, kontakty, mapa, formulář), hezký na mobilu i na počítači. První verzi uvidíte do 24 hodin od podkladů, dvě kola úprav v ceně. Cena 3 990 Kč (jedna stránka) nebo 4 990 Kč (do 5 stránek), bez DPH navíc. Doménu si registrujete na sebe, my ji nastavíme. Volitelně správa 290 Kč měsíčně. Fakturujeme jako s.r.o., platba převodem. Používáme AI a vlastní šablony, proto to stíhá rychle a levně. Napište obor a název firmy, do hodiny pošleme ukázku a cenu.
> Kontakt: e-mail, telefon (po schválení).

Blok → otázka: nadpis „Kolik a za jak dlouho?“; „Nemáte web“ „Je to pro mě?“; seznam obsahu „Co dostanu?“; „Používáme AI“ „Proč tak levně a rychle?“; „Doménu na sebe“ „Komu web patří?“; poslední věta „Co mám udělat?“.

Odpověď zákazníkovi (e-mail, do 60 minut od poptávky):

> Dobrý den, děkuji za zájem o web. Pro přesnou cenu a ukázku potřebuji: 1) název firmy a obor, 2) co nabízíte (3–6 služeb), 3) kontakty a adresu, 4) máte logo a fotky? (jinak použijeme volné fotky), 5) máte doménu, nebo ji zaregistrujeme? Do 24 hodin od zálohy a podkladů dostanete první verzi, dvě kola úprav jsou v ceně. Cena: 3 990 Kč jedna stránka, 4 990 Kč do 5 stránek (neplátci DPH, cena konečná), záloha 50 %. MYPIXEL s.r.o., IČO 17617421.

## Test (po schválení)
- Postup: 1) Ondřejovo schválení + souhlas s podmínkami, 2) ukázkový web (jedna stránka, výslovně označená jako ukázka, na webprodava.cz) do 1 hodiny, 3) inzerát na Bazoši (SMS ověření telefonem dělá Ondřej, autorizace), 4) odpovědi z e-mailu `web@mypixel.cz` do 60 minut (alias zřizuje Ondřej, autorizace), 5) vyhodnocení po 72 h.
- Úspěch: aspoň 1 závazná poptávka (konkrétní obor a požadavek, souhlas s cenou) do 7 dnů. Po 72 h bez poptávky jedna úprava (cena, text, druhý portál), po 0 dotazech za 7 dní test končí, zapsat poučení.
- Náklad: Bazoš 147 Kč (vložení + 2× TOP, strop 392 Kč), Sbazar 0 až 29 Kč; doména webprodava.cz už je. Hosting klientských webů na Vercelu viz riziko výše.
- Co od Ondřeje: „ano, test webu“ (a „Výjimka schválená Ondřejem“, protože formální verdikt je NE), schválení výdaje 147 Kč (finance), schválení podmínek a rizika Vercel čl. 11 (právo), SMS ověření telefonu a mikroplatba 1 Kč na Bazoši, alias e-mailu `web@mypixel.cz`. Nic dalšího, žádné ruční zveřejňování.
