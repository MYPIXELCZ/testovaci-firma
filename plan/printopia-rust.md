# Printopia: plán růstu (od 2026-10-07, výjimka z verdiktu schválena Ondřejem, `plan/hledanost-printopia.md`)

Cíl: z jedné objednávky týdně na pravidelný pasivní příjem (B: ≥ 6 objednávek měsíčně při nákladu ≤ ⅓ tržeb), nejlépe v sezóně listopad až duben (špička Seznamu „cermat testy“ 4,1 tis. v dubnu). Stop-loss: reklamní výdaj jen z kreditu 113 Kč a max. +300 Kč se souhlasem Ondřeje; vyhodnocení při ≈ 190 návštěvách ze Skliku nebo 2026-11-15; bez 3 objednávek zpět do pasivního režimu.

## Stav a zjištění (2026-10-07)
- 1 objednávka (349 Kč) ze Skliku; fulltext kampaň: 28 zobrazení, 6 prokliků, 15,19 Kč za týden. Skoro celý provoz dělá jediné slovo „cermat testy“ (21 zobrazení, 4 prokliky, 8,99 Kč, ø 2,25 Kč za klik), ostatních 14 slov má dohromady 8 zobrazení.
- „cermat testy“ má ø 728 hledání měsíčně (na podzim 1,1 až 1,4 tis.), my jsme měli ≈ 7 % zobrazení: nabídka max. 3 Kč byla příliš nízká.

## Páky (pořadí podle poměru přínos / cena)
1. **Sklik (HOTOVO 2026-10-07 20:4x):** skupina „Testy“ max. CPC 3 → 6 Kč, přidáno 7 frázových slov (přijímačky cermat, testy cermat, cermat testy matematika, cermat testy 2026, cermat přijímací testy, cermat testy pdf, testy na přijímačky). Vyhodnotit 2026-10-14: zobrazení, kliky, ø cena kliku, objednávky; denní limit 30 Kč a kredit 113 Kč zůstávají.
2. **Google (organicky a reklama):** Google = 78,7 % hledání, Printopia je jen na Seznamu. Krok A (Ondřej, 1 klik): v Search Console potvrdit „Ověřit“ pro printopia.cz. Krok B (já, zdarma): stránka pro záměr „cermat testy matematika“ (jak procvičovat s testy CERMATu, náš postup, odkaz na ukázku; bez kopírování úloh CERMAT), IndexNow. Krok C (Google Ads kampaň, po souhlasu s rozpočtem, např. 150 Kč týdně): vyžaduje Google Ads účet (Ondřej založil) a kartu; vytvoření kampaně buď přes API (kroky Google Cloud), nebo podle mého návodu ručně.
3. **Platba kartou (zvýšení konverze):** dnes jen QR převodem. Karta nebo Apple/Google Pay obvykle zvedne konverzi impulzivního nákupu; poplatek ≈ 2,5 % (≈ 9 Kč na objednávku). Potřebuje účet brány (Stripe nebo GoPay; autorizace Ondřej) a mou implementaci (Fio párování zůstává pro převody).
4. **Rozšíření obsahu:** „cermat testy“ hledají na matematiku i češtinu; sada z českého jazyka by rozšířila nabídku a dotazy, ale obsah nejde ověřit výpočtem jako matematika (riziko chyb), proto až po datech z bodů 1 až 3.
5. **Konverze webu:** úvod → klik „koupit“ 8,8 %; `/koupit`: 5 zobrazení, 3 začátky formuláře, 2 odeslání. Vzorek je malý, úpravy až od ≈ 190 návštěv.

## Co potřebuji od Ondřeje (jen autorizace)
1. Search Console: „Ověřit“ pro printopia.cz. 2. Souhlas s rozpočtem na Google Ads (případně pokračovat v krocích Google Cloud). 3. Účet platební brány (Stripe nebo GoPay) až po potvrzení, že chce kartu.
