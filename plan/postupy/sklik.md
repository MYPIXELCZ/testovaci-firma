# Sklik: postupy, chyby a audit kampaně Printopia

Cílová skupina (kampaň Printopia): hledá deváťák i rodič (poměr měří test), používá deváťák, **platí rodič**. Inzeráty mluví k rodiči a nikdy přímo nevyzývají dítě ke koupi ani k přemlouvání rodičů (zákon 634/1992 Sb., příloha č. 2 písm. e; UCPD příloha I bod 28).
Zpracováno 2026-10-01. Platí pro každou další kampaň v Skliku: před založením projít **Kontrolní seznam**.

## Zdroje
Všechny navštíveny 2026-10-01.
1. Shody klíčových slov (VS): https://napoveda.sklik.cz/cileni/klicova-slova/shody-klicovych-slov-vs/
2. Vylučující slova (VS): https://napoveda.sklik.cz/cileni/klicova-slova/vylucujici-slova/
3. Nástroje pro práci s dotazy: https://napoveda.sklik.cz/cileni/klicova-slova/nastroje-pro-praci-s-dotazy/
4. Rozpočet kampaně (poměr 100 : 1, optimalizace rozpočtu): https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/rozpocet-kampane/
5. Nastavení kampaní (celkový rozpočet, platnost): https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/
6. Časové plánování: https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/casove-planovani/
7. Cílení na zařízení: https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/cileni-na-zarizeni/
8. Způsob střídání reklam: https://napoveda.sklik.cz/kampane-a-sestavy/nastaveni-kampane/zpusob-stridani-reklam/
9. Pravidla reklam (obecná): https://napoveda.sklik.cz/pravidla/
10. Pravidla textové reklamy: https://napoveda.sklik.cz/pravidla/textova-reklama/
11. Nejčastější důvody zamítnutí: https://napoveda.sklik.cz/nejcastejsi-duvody-zamitnuti-pro-vsechny-reklamni-formaty/
12. Textové reklamy a doporučení k psaní: https://napoveda.sklik.cz/reklamy/textove-inzeraty/ , https://napoveda.sklik.cz/reklamy/textove-inzeraty/doporuceni-pro-psani-uspesnych-textovych-inzeratu/
13. Odkazy (sitelinky) a Popisky: https://napoveda.sklik.cz/reklamy/textove-inzeraty/odkazy-sitelinky/ , https://napoveda.sklik.cz/reklamy/textove-inzeraty/popisky/
14. Sklik check list (před spuštěním, 7, 14, 30 dní): https://napoveda.sklik.cz/checklist/
15. Konverzní kód a parametr consent: https://napoveda.sklik.cz/merici-skripty/konverzni-kod/
16. Modelované konverze: https://napoveda.sklik.cz/mereni-uspesnosti/konverze/modelovane-konverze/
17. Cookieless check list: https://napoveda.sklik.cz/cookieless-check-list/
18. Automatické tagování a dynamické proměnné: https://napoveda.sklik.cz/mereni-uspesnosti/sledovaci-url/automaticke-tagovani-cilovych-url/ , https://napoveda.sklik.cz/mereni-uspesnosti/sledovaci-url/dynamicke-promenne/
19. Kde se zobrazují textové reklamy: https://napoveda.sklik.cz/zaciname-inzerovat/vyhledavaci-sit/
20. Kvalita a řazení reklam: https://napoveda.sklik.cz/mereni-uspesnosti/sloupec-kvalita/ , https://napoveda.sklik.cz/reklamy/textove-inzeraty/razeni-inzeratu/
21. Sklik API Drak: https://api.sklik.cz/drak/campaigns.create.html , https://api.sklik.cz/drak/ads.create.html , https://api.sklik.cz/drak/keywords.create.html , https://api.sklik.cz/drak/sitelinks.create.html
22. Blog Seznam: Nejčastější chyby v Sklik účtech (06/2022): https://blog.seznam.cz/2022/06/jake-jsou-nejcastejsi-chyby-v-sklik-uctech/
23. Effectix: Zásady pro nastavení účtu Sklik (11/2021): https://www.effectix.com/zasady-pro-kvalitni-nastaveni-uctu-sklik/
24. PPC Profits: Deset mýtů a chyb (03/2015): https://www.ppcprofits.cz/blog/deset-nejcastejsich-mytu-chyb-pri-sprave-ppc-kampani
25. Optimalizovaný web: 7 největších chyb v PPC (02/2017): https://www.optimalizovany-web.cz/7-nejvetsich-chyb-v-ppc-kampanich/
26. Zaklik: Omezený rozpočet (aktualizace 01/2023): https://www.zaklik.cz/strategie/omezeny-rozpocet/
27. Jiří Franěk: 44 chyb v PPC: https://jirifranek.cz/ppc-chyby/
28. Zákon o ochraně spotřebitele, příloha č. 2 písm. e: https://www.zakonyprolidi.cz/cs/1992-634
29. GDPR čl. 7 odst. 4 (podmiňování souhlasu): https://eur-lex.europa.eu/legal-content/CS/TXT/?uri=CELEX:32016R0679
30. Našeptávač Seznamu (reálné dotazy, `_count` = relativní četnost): `https://suggest.seznam.cz/fulltext/cs?phrase=…&count=15`, 35 frází staženo 2026-10-01. Návrhy bez `_count` jsou strojově doplněné (např. „… brno“, „… cermat“), berou se jen jako náznak.

## Čeho se vyvarovat
- **Spoléhat na to, že frázová shoda je úzká.** V Skliku frázová shoda ignoruje pád, tvar i diakritiku, nezáleží na pořadí slov, slova se mohou přidat zleva, zprava i doprostřed a reklama se může zobrazit i na synonyma (zdroj 1). Bez vylučujících slov chytá skoro všechno, co obsahuje naše slova.
- **Chybějící nebo špatně zadaná vylučující slova.** Vylučující slova diakritiku **nikdy** neodstraňují, Sklik proto doporučuje zadávat je s diakritikou i bez ní (zdroj 2). Volná vylučující shoda slovo skloňuje, ale jen skutečné slovo: kmen typu „zdravotnick“ nic nevyloučí. Víceslovné volné vylučující slovo vyloučí jen dotazy, které obsahují všechna jeho slova (zdroj 2).
- **Vylučovat jen naslepo, nebo naopak příliš agresivně.** Seznam je potřeba stavět z reálných dotazů a pak z reportu vyhledávacích dotazů (zdroje 3, 14, 22).
- **Nepracovat s reportem dotazů.** Kontrolovat ho do 7 dnů a pak pravidelně (zdroj 14, 25).
- **Mnoho slov v jedné sestavě.** Sestavy mají být tematicky úzké, do zhruba 10 slov (zdroje 22, 23, 24).
- **Jediná nebo dvě stejné reklamy v sestavě.** Doporučení: 2–4 (Sklik check list), Effectix: 3 (zdroje 14, 22, 23).
- **Chybí rozšíření.** Bez Odkazů a Popisků je reklama menší a má nižší CTR (zdroje 13, 22).
- **Neměřit.** „Kdo neměří, sype peníze z okna“: bez měření nejde poznat, který dotaz přivádí kupující (zdroje 24, 25, 27).
- **Všechno posílat na úvodní stránku, i když existuje relevantnější.** Vstupní stránka má odpovídat dotazu (zdroje 14, 24, 27).
- **Slib „zdarma“ s podmínkou.** Ceny, slevy a „zdarma“ musí být pravdivé, uvedené na cílové stránce a **nepodmíněné** (zdroj 9).
- **Porušení formálních pravidel textu.** Vykřičník v titulcích, VELKÁ písmena (ZDARMA), chybějící diakritika, rovné uvozovky, emotikony, chybějící mezera za interpunkcí, výzva „klikněte zde“, zmínka o konkurenci, nadměrné opakování slov (zdroje 9, 10, 21: diagnostika `words_more_than_three_times_in_all_text`).
- **Cílová stránka bez údajů o provozovateli nebo bez zásad ochrany osobních údajů**, nefunkční URL (404), cíl přímo na PDF nebo automatické stahování souboru, nezavíratelné vyskakovací okno (zdroje 9, 11).
- **Denní rozpočet malý vůči CPC.** Sklik doporučuje denní rozpočet : max. CPC = 100 : 1. Při nižším poměru se reklama zobrazí jen na část dotazů a může dojít k přečerpání rozpočtu (zdroj 4). Řešení při pevném rozpočtu je nižší CPC, ne vypínání reklamy na půl dne (zdroj 26).
- **Celkový rozpočet nižší než denní.** Hrozí přečerpání a kredit v mínusu (zdroj 5).
- **Míchat vyhledávací a obsahovou síť v jedné kampani** (zdroje 25, 27). Naše kampaň typu `fulltext` je jen vyhledávací.
- **Zapnout automatické tagování při ručně zadaných UTM.** Sklik pak ručně zadané UTM přepíše svými hodnotami, takže `utm_source=sklik` by se změnilo na `seznam` (zdroj 18).

## Jak na to při malém rozpočtu
**Typy shody.** Volná shoda v Skliku navíc spouští „automatizovaný výdej“ na dotazy vybrané podle textu reklamy (zdroj 1), proto ji s rozpočtem 400 Kč nepoužívat. Frázová shoda stačí, protože sama pokrývá tvary, diakritiku i pořadí slov. Přesná shoda u víceslovného slova diakritiku ignoruje, ale neskloňuje se (zdroj 1). Sestavy jen s přesnou shodou se nezobrazují v Seznam Asistentovi. Frázové a volné ano a Asistenta nelze vyloučit (zdroj 19). Nezadávat duplicitní slova: ve frázové shodě je „procvičování na přijímačky“ nadmnožinou „přijímačky matematika procvičování“.

**Vylučující slova.** Na úrovni kampaně (platí pro všechny sestavy), ve volné shodě, každé slovo s diakritikou i bez ní (zdroj 2). Zdroj: našeptávač teď, report dotazů po spuštění. Slova, která mohou být i relevantní (např. „cermat“, „testy“), nevylučovat hned. Sledovat je v reportu dotazů a vyloučit, když přinášejí prokliky bez kliknutí na „Koupit“.

**Struktura.** Jedna kampaň = jeden denní rozpočet. Sestavy rozpočet nedělí, jen zvyšují relevanci, takže dvě až tři tematické sestavy v jedné kampani rozpočet nerozdrobí. Více kampaní s rozpočtem 30 Kč by ho rozdrobilo (min. 30 Kč na kampaň, zdroj 4).

**Reklamy.** 2–4 na sestavu, klíčové slovo v titulku, výhoda, výzva k akci, cena (zdroje 12, 14). Pole: titulky 30 znaků, popisek 90, dvě Cesty po 15 znacích, Cesty smějí mít diakritiku (zdroj 12). Slovo z dotazu ve viditelné URL zvyšuje relevanci (zdroj 12). Střídání reklam ponechat „weighted“ (podle CTR), dokud se neměří konverze (zdroje 14, 21).

**Rozšíření.** Odkazy: text max. 25 znaků, každý na jinou URL (stejná URL se zobrazí jen jednou), zobrazí se 2–6 Odkazů. Popisky: max. 25 znaků, zadat alespoň 4, zobrazí se max. 4 (zdroj 13). Proklik na Odkaz stojí stejně jako na reklamu. V API: `sitelinks.create`, a když chybí `url`, vznikne Popisek (zdroje 13, 21). Jak je přiřadit ke kampani, ověřit v dokumentaci Draku.

**Čas a zařízení.** Úpravy dělat až podle dat, ne odhadem (zdroj 14: „Úprava nabídek dle výkonu“). Časové plánování vypíná optimalizaci denního rozpočtu, která jinak rozkládá výdej přes celý den (zdroje 4, 6). Bez dat ho proto nezapínat. Zařízení: multiplikátor −100 % až +300 %, jen podle výkonu (zdroj 7). 80 % návštěvníků Seznamu chodí z mobilu (zdroj 19).

**CPC.** Ve stejné aukci rozhoduje max. CPC a koeficient kvality (relevance slova k dotazu, CTR), vyšší CTR znamená nižší skutečnou cenu (zdroj 20). Při omezeném rozpočtu snížit CPC, aby kampaň běžela celý den a prokliky byly levnější (zdroje 4, 26). Po 7 dnech zkontrolovat ztracená zobrazení (rozpočet / pořadí) a sloupec Kvalita 1–10 (zdroje 4, 14, 20).

**Schvalování a zamítnutí.** Nejčastější důvody: chybí údaje o provozovateli na webu (IČO, adresa, e-mail), neověřitelná nebo podmíněná cena či „zdarma“, nefunkční URL, obsah reklamy neodpovídá stránce, atypická zkratka, text bez smyslu, formální chyby (zdroje 9, 10, 11). Po spuštění zkontrolovat zamítnuté reklamy (zdroj 14). Podpora Skliku odpovídá do 2 hodin (zdroj 11).

**Měření konverzí, retargeting, cookies.** Konverzní i retargetingový kód má povinný parametr `consent`. Bez souhlasu (0) Seznam zpracuje hit anonymně a použije ho jen k modelování (zdroj 15). Modelování potřebuje aspoň jednotky konverzí a prokliků denně, u malých účtů je přínos malý (zdroj 16). Kód s `consent: 0` se může spouštět i bez cookie lišty, kódem se souhlasem (1) až po souhlasu (zdroj 17). Retargeting potřebuje souhlas s cookies, tedy cookie lištu (zdroje 15, 17). Alternativa bez cookies, kterou už máme: vlastní anonymní trychtýř a do cílové URL dynamické proměnné `{keywordId}`, `{creative}`, `{network}` (zdroj 18). Tak jde trychtýř rozdělit po klíčových slovech a reklamách bez osobních údajů.

**Jak dlouho a s kolika kliky vyhodnocovat.** Sklik check list: den 1 schválení, do 7 dnů report dotazů, vylučující slova, mírné úpravy CPC a omezený rozpočet, do 14 dnů nulová zobrazení, slova s nízkým CTR a A/B test reklam, od 30 dnů pravidelný report (zdroj 14). Statistika (vlastní výpočet, Wilsonův 95% interval): 4 kliknutí na „Koupit“ z 80 návštěv (5 %) znamenají interval 2,0–12,2 %, 1 z 80 interval 0,2–6,7 %. **Při 80 návštěvách nejde spolehlivě rozlišit 2 % od 5 %.** K tomu je potřeba zhruba 190 návštěv (jednostranný test, α = 0,05, síla 80 %). A/B test dvou reklam při desítkách prokliků nic neprokáže, Sklik je beztak střídá sám („bayesovský bandita“, zdroj 8).

## Kontrolní seznam
Každý bod se ověřuje příkazem, výstupem API nebo pohledem do reportu. Před spuštěním:
- [ ] Cílová skupina je v hlavičce `sklik.py` a aspoň jeden titulek nebo popisek každé reklamy oslovuje plátce. Ověří `assert` v `sklik.py`.
- [ ] Žádný text nevyzývá dítě ke koupi ani k přemlouvání rodičů. Ověří ruční čtení textů a `assert` (zakázaná slova „kup si“, „řekni rodičům“, „přemluv“).
- [ ] Texty mají správnou délku (titulek ≤ 30, popisek ≤ 90, Cesta ≤ 15, Odkaz a Popisek ≤ 25) a nemají vykřičník v titulku, VELKÁ slova, rovné uvozovky ani slovo víc než 3× (`assert` v `sklik.py`).
- [ ] Každá cena, „zdarma“ a datum v reklamě jsou pravdivé, na cílové stránce a nepodmíněné. Ověří `curl` cílové URL a hledání stejného textu.
- [ ] Cílová URL vrací 200, je to webová stránka (ne PDF), má provozovatele (IČO, adresa, e-mail) a odkaz na zásady ochrany osobních údajů (`curl`, grep „IČO“, „Ochrana osobních údajů“).
- [ ] Kampaň je typu `fulltext` (bez obsahové sítě) a ve sledovaných službách nejsou Sbazar, Sauto a Zboží (`campaigns.list` → `excludedSearchServices`).
- [ ] Denní rozpočet ≥ 30 Kč, celkový rozpočet (je-li) ≥ denní a kredit v účtu je známý (`client.get`).
- [ ] Žádná volná shoda; frázová nebo přesná shoda, bez duplicit, ve frázové shodě žádné slovo není nadmnožinou jiného (skript).
- [ ] Vylučující slova: každé slovo s diakritikou má i variantu bez ní, žádné není kmen bez koncovky (skript), seznam vychází z dotazů v našeptávači.
- [ ] 2–4 reklamy v každé sestavě, klíčové slovo nebo jeho téma je v titulku, Cesty jsou vyplněné.
- [ ] Aspoň 4 Popisky a 4 Odkazy na různé URL, všechny s `utm_source=sklik`.
- [ ] Automatické tagování je vypnuté (`autotagging.get`), nebo měření počítá i `utm_source=seznam`.
- [ ] Měření: v URL je `utm_source=sklik&utm_term={keywordId}&utm_content={creative}`, trychtýř je ukládá a `vyhodnoceni.py` sčítá Sklik ze všech stránek, ne jen z úvodu.
- [ ] Je předem zapsané kritérium vyhodnocení i s počtem návštěv potřebným pro rozhodnutí (`plan/<projekt>.md`, oddíl 4).

Po spuštění: den 1 všechny reklamy schválené (`ads.list` stav), do 3 dnů zobrazení > 0 u sestav, den 7 projitý report dotazů a doplněná vylučující slova, zkontrolované ztracené zobrazení z rozpočtu a pořadí, den 14 slova s nulou zobrazení a slova s nízkým CTR.

## Audit naší kampaně
Stav podle `printopia/marketing/sklik.py` a `sklik_api.py` (kampaň 7984059, sestava 176751820). Živá kampaň nebyla ověřována přes API.

| Bod | Stav | Návrh |
|---|---|---|
| Cílová skupina, oslovení rodiče | OK (hlavička, `assert`, „Pro rodiče deváťáků“, „Dítěti nejdou zlomky?“) | Rozšířit `assert` na každou reklamu zvlášť (inzerát 2 má rodiče jen v popisku) a přidat zakázané výzvy dětem. |
| Typ kampaně, síť | OK (`fulltext`, jen vyhledávání) | Vyloučit Sbazar, Sauto a Zboží přes `excludedSearchServices` (ID z `campaigns.listSearchServices`). |
| Typ shody | OK (frázová, žádná volná) | Frázová shoda v Skliku je široká (tvary, pořadí, synonyma), proto jsou klíčová vylučující slova. |
| Duplicitní slova | Chybí kontrola | „přijímačky matematika procvičování“ je pokrytá slovem „procvičování na přijímačky“, vyřadit. |
| Hledanost slov | Riziko | Seznam u našich frází ukazuje velmi nízkou četnost („přijímačky matematika“ 5, „příklady z matematiky přijímačky“ 6). Skutečně hledané: „příprava na přijímací zkoušky“ 107, „příprava na přijímací zkoušky na střední školu“ 65, „státní přijímačky z matematiky“ 25, „pracovní sešit přijímačky 2027“ 5. Přidat „příprava na přijímací zkoušky na střední školu“, „státní přijímačky z matematiky“ a „pracovní sešit přijímačky“ (rodiče, nákupní úmysl). Po 3 dnech zkontrolovat slova s nulou zobrazení. |
| Struktura | 1 sestava, 12 slov, 2 reklamy | Dvě sestavy ve stejné kampani: A „Příprava (rodiče)“ (příprava…, procvičování…, sbírka…, pracovní sešit…, pdf), B „Témata“ (zlomky, procenta, rovnice, slovní úlohy, příklady). Rozpočet se nedělí. |
| Vylučující slova | Nedostatečné | Opravit chyby (viz níže) a doplnit podle reálných dotazů. |
| Texty reklam | Částečně OK | „Ukázka zdarma ke stažení“ a „Stáhněte si zdarma ukázku 8 úloh“ jsou podmíněné e-mailem a **povinným** souhlasem s upozorněním. To odporuje pravidlu Skliku („zdarma“ musí být nepodmíněné) a láká hledače věcí zdarma, což zkresluje test nákupu. „Pro rodiče deváťáků“ je v inzerátu 1 dvakrát (titulek i popisek). Chybí cena, Cesty a třetí reklama. |
| Rozšíření | Chybí | 4 Popisky a 4–5 Odkazů (níže). |
| Rozpočet a CPC | 30 Kč/den, 6 Kč = poměr 5 : 1 (doporučeno 100 : 1) | Reklama se ukáže jen na část dotazů. Pokud po 3 dnech hlásí ztracená zobrazení z rozpočtu a pozice je dobrá, snížit CPC na 4 Kč: ze 400 Kč pak vyjde asi 100 prokliků místo asi 67. Celkový rozpočet nenastavovat pod denní. |
| Čas, zařízení, region | Výchozí (celý den, všechna zařízení, celá ČR) | OK, produkt je celostátní. Upravovat až podle reportu (zařízení, hodina) po zhruba 50 proklicích. |
| Měření | Částečně | `utm_source=sklik` funguje jen při vypnutém autotaggingu. `vyhodnoceni.py` počítá jen `home:sklik`, takže prokliky přes Odkazy na tematické stránky by se nezapočítaly. Přidat `&utm_term={keywordId}&utm_content={creative}`, ukládat v trychtýři a vyhodnocovat po slovech a reklamách. Konverzní kód Skliku teď nenasazovat: při našem objemu nic nepřidá a vložení skriptu třetí strany by vyžadovalo úpravu zásad (právo = Ondřej). |
| Vstupní stránka | OK (200, 0,6 s, provozovatel a IČO v patičce, zásady ochrany osobních údajů, mobil) | Tlačítko „Koupit sadu za 349 Kč“ vede na produkt, který vyjde až 15. 11. Datum je jen v FAQ. Uvést „vychází 15. 11.“ i u tlačítka, jinak hrozí výtka, že je stránka klamavá (zdroj 9). **Právní riziko pro Ondřeje:** stažení ukázky vyžaduje souhlas se zasíláním upozornění, takže jde o podmiňování souhlasu (GDPR čl. 7 odst. 4). Bezpečnější je udělat souhlas nepovinný. |
| Kritérium vyhodnocení | Slabé | 80 prokliků nerozliší 2 % od 5 % (viz výše, potřeba je asi 190). Do vyhodnocení brát i návštěvy z vyhledávání a pro rozhodnutí kombinovat klik na „Koupit“, e-maily rodičů a anketu. Výsledek při 80 proklicích brát jen jako orientační. |

**Oprava stávajících vylučujících slov:** „zdravotnick“ → „zdravotnická“, „zdravotnicka“ (kmen nic nevyloučí). Ke každému slovu s diakritikou přidat variantu bez ní: „vysoka“, „osmilete“, „trida“ (jako „5 trida“, „7 trida“), „cestina“, „anglictina“, „reseni 2026“, „vysledky“, „termin“, „policejni“. „řešení 2024“ a „řešení 2025“ nahradit samotnými roky „2024“ a „2025“, které pokryjí i „cermat testy 2024 ke stažení“ a „testy na přijímací zkoušky 2025“.

**Doplnit (volná vylučující shoda, každé slovo podložené dotazem z našeptávače 2026-10-01):**
```python
NEGATIVE_ADD = [
  # jiná zkouška, škola nebo ročník („příprava na přijímačky na víceleté gymnázium“, „7.třída“, „přijímačky na vysoké školy 2027“)
  "maturitní", "maturitni", "vs", "vysoke", "víceleté", "vicelete", "šestileté", "sestilete", "8leté", "8lete",
  "6leté", "6lete", "5.třída", "7.třída", "zdravotnická", "zdravotnicka",
  # jiný předmět („přijímačky český jazyk 2027“, „testy z čj na přijímačky“)
  "český jazyk", "cesky jazyk", "čj", "cj", "jazyk",
  # úřední informace, ne příprava („přijímací zkoušky na střední školy 2027 termíny“ 64, „kdy budou přijímací zkoušky“)
  "termin", "kdy", "přihláška", "prihlaska", "vysledky",
  # staré testy a klíče („cermat testy z minulých let“, „cermat testy 2024 ke stažení“)
  "2024", "2025", "klíč", "klic",
  # kurzy a doučování na místě („doučování na přijímačky brno“ 29, „příprava na přijímačky brno“ 18)
  "doučování", "doucovani", "kurz", "lektor", "brno", "praha", "plzeň", "plzen", "ostrava", "olomouc", "kladno",
  "pardubice", "hradec", "budějovice", "budejovice", "mělník", "melnik",
  # zdarma, online a akce jiných („přijímačky pdf zdarma“, „přijímačky online“ 18, „přijímačky nanečisto 2027“ 45, „prijimacky.blesk.cz“ 36)
  "zdarma", "online", "nanečisto", "nanecisto", "nečisto", "necisto", "scio", "blesk", "taktik", "pohoda", "robin", "youtube",
]
# SLEDOVAT v reportu dotazů, nevylučovat hned (mohou být i rodiče): "cermat", "testy", "pdf", "ke stažení", "k vytištění", "2026"
```
„2026“ zatím nevylučovat: část lidí tím myslí školní rok 2026/27.

**Návrh textů (délky ověřené):**
- Sestava A, reklama 1: T1 „Přijímačky: matika po tématech“, T2 „Pro rodiče deváťáků“, T3 „Postup u každé úlohy“, P1 „Úlohy k tisku na jednotnou přijímací zkoušku, u každé postup řešení krok za krokem.“, P2 „Sada 12 témat za 349 Kč vychází 15. 11. Příklady s postupem si projděte zdarma.“ (na úvodu jsou zdarma bez podmínky 2 úlohy a odkazy na tematické stránky), Cesty „přijímačky“ / „matematika“.
- Sestava A, reklama 2: T1 „Příprava na přijímačky: matika“, T2 „Víte, co dítěti nejde?“, T3 „Sada 12 témat za 349 Kč“, P1 „Úvodní test ukáže slabá témata, plán rozvrhne přípravu do zkoušky 12. dubna.“
- Sestava B: T1 „Zlomky, procenta, rovnice“, T2 „Přijímačky z matiky s postupem“, P1 „Pro rodiče deváťáků: příklady po tématech k tisku, u každé úlohy postup řešení.“
- Popisky: „Postup u každé úlohy“, „PDF k tisku“, „14 dní na vrácení peněz“, „Bez předplatného“, „Jednorázově 349 Kč“.
- Odkazy: „Zlomky na přijímačky“ → /zlomky-prijimacky, „Procenta na přijímačky“ → /procenta-prijimacky, „Rovnice na přijímačky“ → /rovnice-prijimacky, „Slovní úlohy“ → /slovni-ulohy-prijimacky, „Jak se připravit“ → /jak-se-pripravit-na-prijimacky (všechny s `?utm_source=sklik`; předtím upravit `vyhodnoceni.py`).

Nic z toho není nasazené: kód kampaně ani živá kampaň se neměnily.
