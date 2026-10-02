# Plán produktu: <název>

Povinná šablona (pojistka z FAILS.md). Bez vyplněných oddílů 1–4 se nestaví nic, co trvá déle než pár hodin,
a Ondřej nekupuje nic (doména, reklama). Každé tvrzení o poptávce musí mít zdroj (odkaz, nástroj, datum).

## 0. Verdikt (povinné, FAILS.md 2026-10-02): ověřitelné do 3 dnů a dostatečný prodej
`python3 plan/verdikt.py <projekt> --cena … [--konv-overeni 0.05 --rozpocet …]` zapíše do `plan/hledanost-<projekt>.md` verdikt. Bez ANO/ANO se nestaví (výjimku schvaluje jen Ondřej).

## 1. Poptávka (důkazy, ne dojmy)
- **Absolutní hledanost (povinné, FAILS.md 2026-10-01 17:00):** `SKLIK_TOKEN=… python3 plan/hledanost.py <projekt> "dotaz" … --navrhy "základ"` zapíše `plan/hledanost-<projekt>.md` (měsíční hledání, špička, CPC, nejsilnější související dotazy). Relativní Trends ani našeptávač nestačí. Do oddílu „## Kapacita trhu“ vyplnit: hledanost × CTR × konverze × cena vs. cíl projektu a závěr stavět / nestavět / nejdřív sonda. Součástí kontroly `plan/kontrola-spusteni.py`.
- Relativní signály navíc: Trends, našeptávač (co lidé zadávají).
- Kdo už to prodává a jak se mu daří (počty prodejů, recenze, ceny, tržiště).
- Sezónnost vůči dnešnímu datu a odhad, kdy přijde první tržba.

## 1b. Cílová skupina (povinné, pojistka z FAILS.md)
- Kdo HLEDÁ (zadává dotazy, kliká na reklamu), kdo POUŽÍVÁ, kdo PLATÍ. Často jsou to různí lidé.
- Pro koho je který materiál: reklama a web → plátce (a hledající, aby ho přivedl k plátci), produkt → uživatel.
- Omezení: nezletilí (GDPR souhlas v ČR od 15 let, reklama na děti), způsob platby dostupný plátci.

## 2. Konkurence a proč koupí od nás
- Konkurenční tabulka: aspoň 5 konkrétních konkurentů (odkaz, cena, počet recenzí nebo prodejů, co mají a my ne) a jak se v placených výsledcích pozicují (živé hledání na search.seznam.cz: `printopia/marketing/serp_check.py` jako vzor).
- Zdarma alternativy (šablony, aplikace, banky…) a v čem jsme lepší.

## 3. Ekonomika
- Cena, odhad ceny za proklik, konverze, cena za zákazníka (CAC) vůči ceně.

## 4. Test poptávky před stavbou
- Nejdřív nejmenší možná verze (jedna stránka, jedno téma), ne celá sada. Plná stavba až po čísle hledanosti a prvním signálu poptávky.
- Co se změří, za kolik, jak dlouho, a kritérium pokračovat / zastavit.

## 5. Role Ondřeje
- Jen autorizace a schválení (test kroku pro Ondřeje). Vypsat přesně.

## 6. Rizika (právo, finance) a co schvaluje Ondřej

## 7. Metriky a vyhodnocení (povinné před spuštěním, pojistka z FAILS.md)
- Trychtýř po krocích: zobrazení reklamy → proklik → návštěva → dočtení / čas → klik na nabídku → začátek formuláře → dokončení → nákup. Rozdělit podle zdroje a zařízení.
- Proč ne: anonymní anketa s důvody (cena, nedůvěra, jiné hledání…) a hledané dotazy z reklamy.
- Automatické závěry z dat: kde lidé odpadají a co upravit (reklama, stránka, nabídka, formulář, cena).
- Po testu zapsat `plan/<projekt>-vyhodnoceni.md`: čísla, závěr pokračovat/zastavit, co zlepšit pro další RUN.
- Kontrola: `python3 plan/kontrola-spusteni.py plan/<projekt>.md <aplikace>` musí projít.

- **Zahraniční kanály a služby (Ondřej 2026-10-02):** v kapacitě trhu, konkurenci i v kanálech posuzovat zahraniční a placené služby (Google Ads, Etsy, Gumroad, hostingy, platební brány) stejně jako české: přínos proti ceně včetně 21 % DPH (reverse charge), poplatků a administrativy. Původ služby není důvod zamítnutí.

## 2a. Schopnost (umím to?) (povinné, FAIL 2026-10-02 14:43)
Rozhodujeme podle toho, zda jsme schopni to udělat, ne zda jsme to už dělali. U každé části řešení: umím ji? Ověření do 24 h (zkouška, prototyp, dokumentace) a výsledek zapsat. „Nedělali jsme“ není důvod k NE. Chybějící reference řešit pilotem se zárukou, nikdy ne vymyšlenými referencemi (klamavé jednání).

## 2c. Prezentace pro cílovou skupinu (povinné, FAIL 2026-10-02 14:44)
Stejná služba se různým skupinám jeví jinak podle toho, jak je podána. Navrhnout 2 až 3 varianty pro různé segmenty a u každé uvést: **segment** (kdo, v jaké situaci), **jeho slovy problém** (ne naše řešení), **název a příslib**, **cenová kotva a balení** (s čím se srovná: agentura, freelancer, „udělám si sám“), **důkaz** (ukázka, záruka, pilot; nic vymyšleného), **kanál a jazyk**, **konkurence v této variantě** a **realistický podíl** (oddíl 2b). V testu každou variantu označit a vyhodnotit zvlášť; vítěze volit podle reakcí, u malých vzorků postupně, ne statisticky. Platí poctivost: jiné podání, ne jiná skutečnost.

## 2b. Konkurence a ukousnutelný podíl (povinné, FAIL 2026-10-02 14:38)
V každém businessu drží trh statisticky pár velkých hráčů. Neříkáme proto automaticky „nasycené, NE“, ptáme se, zda a čím si ukousneme kus (realisticky):
1. **Trh a koncentrace:** kolik nákupních rozhodnutí měsíčně je v dosažitelném trhu (poptávky, nové e-shopy, hledání, prodeje konkurence) a kolik z něj drží vedoucí hráči (číslo a zdroj).
2. **Naše výhody (aspoň 3 s důkazem):** cena, rychlost, balíček (např. jedna cena na rok), specializace na úzkou niku, jazyk a místo, záruka, bezrizikový test, to, co vedoucí hráč nedělá (ze `Konkurence` tabulky). Výhoda bez důkazu se nepočítá.
3. **Úzká nika:** nejmenší segment, kde můžeme být první nebo nejlepší, místo boje o celý trh.
4. **Realistický podíl:** kolik objednávek měsíčně potřebujeme (cíl ÷ cena), kolik je to procent dosažitelného trhu (`plan/verdikt.py --trh-objednavek-mesicne N`, strop pro nováčka do 6 měsíců 3 %) a čím to doložíme (srovnatelní nováčci, jejich prodeje a recenze, naše míra odpovědí z testu). Žádná čísla „z optimismu“: bez dokladu se bere podíl 1 %. U poptávkových portálů se strop 3 % nahrazuje mírou výhry u odpovědí (benchmark nebo naše měření z testu), `--podil-max` se nastaví s odůvodněním.
5. **Závěr:** ukousnutelné ANO/NE a co by to změnilo (cena, nika, kanál).
