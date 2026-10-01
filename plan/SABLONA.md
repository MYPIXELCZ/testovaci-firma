# Plán produktu: <název>

Povinná šablona (pojistka z FAILS.md). Bez vyplněných oddílů 1–4 se nestaví nic, co trvá déle než pár hodin,
a Ondřej nekupuje nic (doména, reklama). Každé tvrzení o poptávce musí mít zdroj (odkaz, nástroj, datum).

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
