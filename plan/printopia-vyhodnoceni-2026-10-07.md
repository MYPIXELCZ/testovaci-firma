# Printopia: vyhodnocení k 2026-10-07 (první skutečná tržba)

**Fakta (stats API, Fio, `/api/health`):** 2026-10-07 přišla na Fio platba 349 Kč (VS 8261007767), objednávka zdroj `sklik`, zaplacená; cron spároval, e-mail (Resend) i Fio v pořádku. Je to první skutečná tržba firmy (dříve jen testovací 1 Kč).
**Čísla týdne 2026-10-01 až 07:** Sklik fulltext 28 zobrazení, 6 prokliků, útrata 15,19 Kč, kredit 113,26 Kč; návštěvy ze Skliku 9 až 14 podle zdroje (serverové), 1 objednávka; z úvodu klik na „koupit“ 8,8 %; formulář `/koupit` 3 start, 2 odeslání. Zboží.cz: kampaň Nákupy 0 zobrazení, nabídka není na stranách 1 až 3 u „přijímačky matematika“ ani „matematika 9 třída přijímačky“.
**Závěry:**
1. Konverze 1 objednávka ze 6 prokliků je jedno pozorování (95 % interval zhruba 0,4 až 64 %), nic nedokazuje; cena objednávky z reklamy 15 Kč. Rozhodnutí o škálování až od ≈ 190 návštěv ze Skliku (jinak nerozliším 2 % a 5 %).
2. Zboží.cz sonda je neúspěšná (0 zobrazení po 6 dnech); kampaň „Nákupy: Printopia“ nechat běžet za 0 Kč, další investici ne (Heureka zrušena, min. dobití 499 Kč).
3. Verdikt `plan/verdikt.py` zůstává NE/NE (Seznam: „cermat testy“ ø 1,1 až 1,4 tis. hledání, špička 4,1 tis., ≈ 123 prokliků ve špičce při CTR 3 %). Pro cíl B (zisk ≥ 2 000 Kč měsíčně, ≥ 6 objednávek) by při konverzi 3 až 8 % stačilo ≈ 75 až 200 prokliků měsíčně, což je v sezóně (listopad až duben) na hraně možné, mimo ni ne. Zatím jen sbírat data, bez dalších výdajů (kredit 113 Kč vystačí).
4. Právo/finance: tržba 349 Kč (neplátce DPH, bez DPH); účetně jde do rozpočtu firmy (reinvestice).
