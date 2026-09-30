# FAILS

Chyby nahlášené Ondřejem ("FAIL: ..."). Každá má příčinu a pojistku, aby se neopakovala.

## 2026-09-30 21:57 UTC
- **Hlášení:** počítal si s marketingovými kanály, které musím obsluhovat já.
- **Příčina:** Marketing (FB skupiny, Pinterest) jsem navrhl podle toho, co funguje, a nezkontroloval, kdo ho bude obsluhovat. Dohoda „Ondřej jen autorizuje a schvaluje“ nebyla zapsaná v paměti.
- **Pojistka:** Pravidlo v CLAUDE.md (Role): Ondřej dělá JEN autorizaci a schvalování. Nové pravidlo „Test kroku pro Ondřeje“: před každým návrhem nebo plánem u každého jeho kroku ověřit, že jde o přihlášení/ověření/souhlas. Jinak krok převezmu, nebo kanál vyřadím. FB příspěvky a piny jsou vyřazené jako kanál.

## 2026-09-30 22:00 UTC
- **Hlášení:** vytvářel jsi produt/službu, která je sezónní a sezóny právě není
- **Příčina:** Produkt jsem vybíral podle toho, co umím vyrobit od A do Z, a podle velikosti trhu. Neověřil jsem, kdy bude první tržba. Sezónu zásnub (prosinec–únor) jsem bral jako termín spuštění, ne jako riziko, že se první 2–3 měsíce nic neprodá.
- **Pojistka:** Pravidlo v CLAUDE.md (Rozhodnutí): u každého nového produktu nebo služby předem ověřit sezónnost poptávky vůči dnešnímu datu a odhadnout, kdy přijde první tržba. Přednost mají produkty s poptávkou teď nebo po celý rok. Sezónní produkt mimo sezónu jen s výslovným zdůvodněním a jako vedlejší, nikdy jediný.

## 2026-09-30 22:09 UTC
- **Hlášení:** neděláš research toho, zda je po dané službě/produktu poptávka
- **Příčina:** Produkty jsem vybíral podle úsudku („velký trh“, „celoroční“), ne podle dat. Neměl jsem povinný krok, který by vyžadoval doložit poptávku čísly a zdroji dřív, než začnu stavět nebo žádat o peníze.
- **Pojistka:** Povinná šablona `plan/SABLONA.md`: poptávka s čísly a zdroji, konkurence, ekonomika, test poptávky s kritériem pokračovat/zastavit. Pravidlo v CLAUDE.md: bez vyplněných oddílů 1–4 nic nestavím (déle než pár hodin) a Ondřej nic nekupuje.

## 2026-10-01 00:24 (Praha)
- **Hlášení:** používej pražské časy
- **Příčina:** Nástroje (logy Vercelu, plánovač připomínek, kontejner) běží v UTC a já časy Ondřejovi přepisoval bez převodu.
- **Pojistka:** Pravidlo v CLAUDE.md: Ondřejovi vždy pražský čas (Europe/Prague). Hook `.claude/hooks/prague-time.sh` přidá ke každé zprávě aktuální pražský čas a posun proti UTC, takže převod mám vždy před očima. FAIL záznamy se píšou v pražském čase.

## 2026-10-01 01:09 (Praha)
- **Hlášení:** když děláš reklamu nebo design webu/reklamy jakýchkoli materiálů, ověř pro jakou cílovou skupinu to děláš (například teď je to pro děti, ale jsou děti ti, co to budou kupovat?)
- **Příčina:** Cílovou skupinu jsem nerozlišil na tři role: kdo hledá, kdo používá a kdo platí. U přijímaček hledají hlavně deváťáci (14–15 let), používají je deváťáci, ale platí rodiče. Klíčová slova v Skliku by přiváděla hlavně děti, které nezaplatí. Formulář navíc mohl sbírat e-maily od dětí mladších 15 let bez souhlasu rodičů (GDPR, v ČR hranice 15 let).
- **Pojistka:** Šablona plánu má povinný oddíl „Cílová skupina“: kdo hledá, kdo používá, kdo platí, pro koho je který materiál, omezení u nezletilých. Pravidlo v CLAUDE.md: každá reklama, web a materiál má v hlavičce uvedenou cílovou skupinu. Printopia: inzeráty mluví k rodičům, formulář vyžaduje „jsem rodič, nebo je mi aspoň 15 let“, žák může stránku poslat rodičům. Kontrola v kódu: `sklik.py` spadne, když inzeráty neoslovují rodiče; e2e ověřuje potvrzení věku ve formuláři.
