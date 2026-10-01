#!/usr/bin/env python3
"""Téma 5: Procenta. Vlastní úlohy ve stylu jednotné přijímací zkoušky (formát v _lib.py, vzor 01_zlomky.py)."""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import Topic, dec  # noqa: E402


def cz(x) -> str:
    """Číslo pro odpověď: celé s mezerou v tisících („12 500“), jinak desetinné s čárkou."""
    x = F(x)
    if x.denominator == 1:
        return f"{x.numerator:,}".replace(",", " ").replace("-", "−")
    return dec(x, 4)


T = Topic(5, "procenta", "Procenta",
          "Procenta patří k nejbodovanějším tématům zkoušky: úloha 15 s přiřazováním bývá procentová a procenta se vracejí "
          "také ve výběru A–E i ve slovních úlohách. Rozhoduje, zda správně určíte základ, tedy to, k čemu se procenta vztahují.",
          ["Nejdřív určete základ (100 %): je to původní hodnota nebo celek, ke kterému se část či změna vztahuje. "
           "Při dvou změnách po sobě je základem druhé změny už hodnota po první změně.",
           "Procenta převádějte na desetinná čísla: 35 % = 0,35, 5 % = 0,05, 125 % = 1,25. Část z celku se pak počítá násobením, "
           "celek (základ) dělením: je-li 15 % rovno 90, je 1 % rovno 90 : 15 = 6 a 100 % je 600.",
           "Zdražení o 20 % znamená násobit číslem 1,2, zlevnění o 20 % číslem 0,8. Opakované změny se násobí, nesčítají: "
           "dvě zdražení o 20 % dají 1,2 · 1,2 = 1,44, tedy zdražení o 44 %, ne o 40 %. Zdražení a zlevnění o stejné procento se "
           "neruší, protože každá změna má jiný základ: po zlevnění o 20 % vrátí cenu zpět až zdražení o 25 %.",
           "Otázky „o kolik procent je A větší než B“ a „o kolik procent je B menší než A“ mají různé výsledky, protože základem je "
           "pokaždé jiné číslo: to, s čím porovnáváme (v otázce stojí za slovem „než“).",
           "Jednoduchý úrok za rok = jistina · roční úroková sazba. Za část roku se násobí zlomkem roku (3 měsíce = 3/12 roku). "
           "Promile (‰) je tisícina: 1 ‰ = 0,001 = 0,1 %.",
           "Koncentrace roztoku nebo směsi je podíl hmotnosti složky a hmotnosti celého roztoku (směsi). Při přidání vody se množství rozpuštěné látky "
           "nemění, mění se jen hmotnost celku."])

# ---------------------------------------------------------------- Řešený příklad
T.example("Sportovní boty stály 2 000 Kč. Obchod je nejdřív zdražil o 20 % a potom zlevnil o 20 % z nové ceny. "
          "Kolik boty nyní stojí a jak se jejich cena změnila oproti původní ceně?",
          ["Zdražení o 20 %: cena je 120 % původní, tedy 2 000 · 1,2 = 2 400 Kč.",
           "Zlevnění o 20 % z nové ceny: zbývá 80 % ze 2 400 Kč, tedy 2 400 · 0,8 = 1 920 Kč.",
           "Změna oproti původní ceně: 2 000 − 1 920 = 80 Kč a 80 : 2 000 = 0,04 = 4 %.",
           "Cena je o 4 % nižší než původní a nevrátila se na 2 000 Kč: druhá změna se počítá z vyššího základu (2 400 Kč)."],
          "1 920 Kč, cena je o 4 % nižší než původní",
          2000 * F(120, 100) == 2400 and 2400 * F(80, 100) == 1920 and F(1920, 2000) == F(96, 100)
          and 2000 - 1920 == 80 and F(80, 2000) == F(4, 100))

# ---------------------------------------------------------------- Základ
r = F(35, 100) * 240
T.task(1, "Kolik korun je 35 % z 240 Kč?", f"{cz(r)} Kč",
       ["35 % = 35/100 = 0,35.", "0,35 · 240 = 84 Kč.",
        "Jinak: 10 % z 240 je 24, 30 % je 72, 5 % je 12 a dohromady 72 + 12 = 84 Kč."],
       r == 84 and F(240, 10) * 3 + F(240, 20) == 84, space=2)

r = F(18, 24) * 100
T.task(1, "Ve třídě je 24 žáků a 18 z nich jede na lyžařský kurz. Kolik procent žáků třídy jede na kurz?", f"{cz(r)} %",
       ["Podíl žáků na kurzu: 18 : 24 = 18/24 = 3/4.", "3/4 = 0,75 = 75 %.", "Zkouška: 75 % z 24 = 0,75 · 24 = 18. ✓"],
       r == 75 and F(18, 24) == F(3, 4) and F(75, 100) * 24 == 18, space=2)

r = F(90) / F(15, 100)
T.task(1, "Sleva na batoh činila 15 % z původní ceny, tedy 90 Kč. Kolik korun stál batoh před slevou?", f"{cz(r)} Kč",
       ["Původní cena je základ, tedy 100 %. Patnáct procent základu je 90 Kč.", "1 % je 90 : 15 = 6 Kč.",
        "100 % je 6 · 100 = 600 Kč.", "Zkouška: 15 % ze 600 = 0,15 · 600 = 90 Kč. ✓"],
       r == 600 and F(90, 15) == 6 and F(15, 100) * 600 == 90, space=2)

r = 120 * (1 + F(25, 100))
T.task(1, "Vstupenka do kina stála 120 Kč a zdražila o 25 %. Kolik stojí nyní?", f"{cz(r)} Kč",
       ["Po zdražení o 25 % je cena 125 % původní ceny, tedy 1,25 · původní cena.", "1,25 · 120 = 150 Kč.",
        "Jinak: 25 % ze 120 je 30 Kč a 120 + 30 = 150 Kč."],
       r == 150 and F(25, 100) * 120 == 30, space=2)

r = F(35, 1000) * 2000
T.task(1, "Mořská voda obsahuje průměrně 35 ‰ (promile) soli. Kolik gramů soli je ve 2 kg mořské vody?", f"{cz(r)} g",
       ["1 ‰ je jedna tisícina: 35 ‰ = 35/1000 = 0,035.", "2 kg = 2 000 g.", "0,035 · 2 000 = 70 g soli.",
        "Kontrola: 1 ‰ ze 2 000 g je 2 g a 35 · 2 = 70 g. ✓"],
       r == 70 and F(1, 1000) == F(1, 10) / 100 and F(1, 1000) * 2000 * 35 == 70, space=2)

# ---------------------------------------------------------------- Jako u zkoušky
r = 8000 * F(80, 100) * F(90, 100)
T.task(2, "Mobilní telefon stál 8 000 Kč. Nejdřív zlevnil o 20 %, potom byla jeho nová cena snížena ještě o 10 % (ze zlevněné ceny). "
          "Kolik stojí po obou slevách a o kolik procent původní ceny celkem zlevnil?",
       f"{cz(r)} Kč, celkem o 28 %",
       ["Po první slevě zbývá 80 % ceny: 8 000 · 0,8 = 6 400 Kč.",
        "Druhá sleva se počítá ze 6 400 Kč, zbývá 90 %: 6 400 · 0,9 = 5 760 Kč.",
        "Podíl původní ceny: 5 760 : 8 000 = 0,72 = 72 %, sleva celkem tedy 100 % − 72 % = 28 %.",
        "Pozor: sečtení 20 % + 10 % = 30 % je chyba, druhá sleva se počítá z nižší ceny."],
       r == 5760 and 8000 * F(80, 100) == 6400 and F(5760, 8000) == F(72, 100) and 100 - 72 == 28, space=3)

zari, rijen = 1600, 2000
a = F(rijen - zari, zari) * 100
b = F(rijen - zari, rijen) * 100
T.task(2, "Na školní charitativní sbírce se v září vybralo 1 600 Kč a v říjnu 2 000 Kč. "
          "a) O kolik procent více se vybralo v říjnu než v září? "
          "b) O kolik procent méně se vybralo v září než v říjnu?",
       f"a) o {cz(a)} %, b) o {cz(b)} %",
       ["Rozdíl: 2 000 − 1 600 = 400 Kč.",
        "a) Porovnáváme se zářím (stojí za slovem „než“), základem je 1 600 Kč: 400 : 1 600 = 1/4 = 25 %.",
        "b) Porovnáváme s říjnem, základem je 2 000 Kč: 400 : 2 000 = 1/5 = 20 %.",
        "Výsledky se liší, protože základ je pokaždé jiný."],
       a == 25 and b == 20 and F(400, 1600) == F(1, 4) and F(400, 2000) == F(1, 5), space=3)

r = 50000 * F(3, 100) * F(4, 12)
T.task(2, "Na spořicí účet bylo uloženo 50 000 Kč s úrokem 3 % ročně. Úrok se počítá jednoduše (bez úročení úroků) a daň "
          "z úroků nepočítejte. Kolik korun úroku vklad přinese za 4 měsíce?", f"{cz(r)} Kč",
       ["Úrok za celý rok: 3 % z 50 000 Kč = 0,03 · 50 000 = 1 500 Kč.", "4 měsíce jsou 4/12 = 1/3 roku.",
        "Úrok za 4 měsíce: 1 500 : 3 = 500 Kč."],
       r == 500 and 50000 * F(3, 100) == 1500 and F(4, 12) == F(1, 3) and F(1500, 3) == 500, space=3)

opts = {"288 Kč": 288, "300 Kč": 300, "340 Kč": 340, "380 Kč": 380, "432 Kč": 432}
T.task(2, "Po zdražení o 20 % stojí kniha 360 Kč. Kolik stála před zdražením?", "B",
       ["Původní cena je základ (100 %), po zdražení je cena 120 % základu.",
        "120 % původní ceny je 360 Kč, tedy 1 % je 360 : 120 = 3 Kč a 100 % je 300 Kč.",
        "Zkouška: 300 · 1,2 = 360. ✓",
        "Chyby: 288 Kč vyjde odečtením 20 % z nové ceny (360 · 0,8), 340 Kč a 380 Kč odečtením, resp. přičtením 20 Kč "
        "místo 20 %, 432 Kč násobením 360 · 1,2."],
       [k for k, v in opts.items() if v * F(120, 100) == 360] == ["300 Kč"] and 360 * F(80, 100) == 288
       and 360 - 20 == 340 and 360 + 20 == 380 and 360 * F(120, 100) == 432 and F(360, 120) == 3,
       kind="choice", options=list(opts), space=3)

stmts = [F(3, 2) * F(1, 2) == 1, F(20, 100) * 50 == F(50, 100) * 20, F(4, 10) == F(4, 100)]
T.task(2, "Platí tato tvrzení?", "NE, ANO, NE",
       ["Po zdražení o 50 % je cena 1,5 původní ceny, po zlevnění o 50 % z nové ceny je to 0,5 · 1,5 = 0,75 původní ceny, "
        "tedy 75 %. Cena se nevrátila, tvrzení neplatí.",
        "20 % z 50 = 0,2 · 50 = 10 a 50 % z 20 = 0,5 · 20 = 10. Tvrzení platí.",
        "0,4 = 40/100 = 40 %, ne 4 %. Tvrzení neplatí."],
       stmts == [False, True, False] and F(3, 2) * F(1, 2) == F(3, 4), kind="yesno",
       options=["Když cena stoupne o 50 % a potom klesne o 50 % z nové ceny, vrátí se na původní hodnotu.",
                "20 % z 50 je totéž jako 50 % z 20.", "Desetinné číslo 0,4 odpovídá 4 %."], space=3)

pondeli = 320
utery = pondeli * F(125, 100)
streda = utery * F(75, 100)
ctvrtek = pondeli * F(75, 100)
nabidka = [240, 300, 320, 345, 375, 400]
pismena = "".join("ABCDEF"[nabidka.index(v)] for v in (utery, streda, ctvrtek))
T.task(2, "Pekárna prodala v pondělí 320 rohlíků. V úterý prodala o 25 % více než v pondělí, ve středu o 25 % méně než v úterý "
          "a ve čtvrtek o 25 % méně než v pondělí. Přiřaďte ke každému dni (1–3) odpovídající počet prodaných rohlíků (A–F): "
          "1 – úterý, 2 – středa, 3 – čtvrtek. Nabídka: A) 240, B) 300, C) 320, D) 345, E) 375, F) 400.",
       f"1 – {pismena[0]}, 2 – {pismena[1]}, 3 – {pismena[2]}",
       ["Úterý: o 25 % více než v pondělí, tedy 1,25 · 320 = 400 rohlíků (F).",
        "Středa: o 25 % méně než v úterý, základem je úterý: 0,75 · 400 = 300 rohlíků (B).",
        "Čtvrtek: o 25 % méně než v pondělí, základem je pondělí: 0,75 · 320 = 240 rohlíků (A).",
        "Ostatní možnosti jsou typické chyby: 320 (C) vyjde, když se nárůst a pokles o 25 % „vyruší“, 345 (D) je 320 + 25 "
        "a 375 (E) je 400 − 25 (přičtení a odečtení 25 kusů místo 25 %)."],
       pismena == "FBA" and utery == 400 and streda == 300 and ctvrtek == 240 and len(set(nabidka)) == 6
       and 320 + 25 == 345 and 400 - 25 == 375, space=3)

T.task(2, "Obchod míchá směs ze 3 kg ořechů a 2 kg rozinek. a) Kolik procent hmotnosti směsi tvoří rozinky? "
          "b) Kolik kilogramů rozinek je třeba přidat, aby rozinky tvořily přesně polovinu směsi (množství ořechů se nemění)?",
       "a) 40 %, b) 1 kg",
       ["Celá směs váží 3 + 2 = 5 kg.", "a) Rozinky tvoří 2 : 5 = 2/5 = 0,4 = 40 % směsi.",
        "b) Rozinky tvoří polovinu směsi, když jich je stejně jako ořechů, tedy 3 kg. Chybí 3 − 2 = 1 kg.",
        "Zkouška: 3 kg ořechů a 3 kg rozinek, rozinky tvoří 3 : 6 = 1/2 = 50 %. ✓"],
       F(2, 5) == F(40, 100) and 3 - 2 == 1 and F(2 + 1, 3 + 2 + 1) == F(1, 2), space=3)

# ---------------------------------------------------------------- Náročnější
sul = F(6, 100) * 400
nova = sul / F(4, 100)
T.task(3, "Ve 400 g solného roztoku je 6 % soli. a) Kolik gramů soli roztok obsahuje? "
          "b) Kolik gramů čisté vody je třeba přidat, aby roztok obsahoval jen 4 % soli?",
       f"a) {cz(sul)} g, b) {cz(nova - 400)} g",
       ["a) 6 % ze 400 g: 0,06 · 400 = 24 g soli.",
        "Přidáním vody se množství soli nezmění, zůstává 24 g. Tato sůl má tvořit 4 % nového roztoku.",
        "Hmotnost nového roztoku: 24 : 0,04 = 600 g.",
        "b) Vody je třeba přidat 600 − 400 = 200 g.", "Zkouška: 24 : 600 = 0,04 = 4 %. ✓"],
       sul == 24 and nova == 600 and nova - 400 == 200 and F(24, 600) == F(4, 100), space=4)

kon = F(936) / (F(130, 100) * F(80, 100))
zisk = F(936) - kon
T.task(3, "Obchodník nakoupil zboží, zvýšil jeho nákupní cenu o 30 % a potom tuto zvýšenou cenu snížil o 20 %. Zákazník zaplatil 936 Kč. "
          "a) Jaká byla nákupní cena zboží? b) Kolik procent z nákupní ceny obchodník vydělal?",
       f"a) {cz(kon)} Kč, b) {cz(zisk / kon * 100)} %",
       ["Nákupní cena je základ x. Po zvýšení o 30 % je cena 1,3 · x, po snížení o 20 % z ní 0,8 · 1,3 · x = 1,04 · x.",
        "1,04 · x = 936, tedy x = 936 : 1,04 = 93 600 : 104 = 900 Kč (104 · 9 = 936).",
        "Zkouška: 900 · 1,3 = 1 170 a 1 170 · 0,8 = 936. ✓",
        "Výdělek: 936 − 900 = 36 Kč a 36 : 900 = 0,04 = 4 % nákupní ceny."],
       kon == 900 and F(13, 10) * F(8, 10) == F(104, 100) and 900 * F(13, 10) == 1170 and 1170 * F(8, 10) == 936
       and zisk == 36 and zisk / kon == F(4, 100) and F(93600, 104) == 900, space=5)

opts = {"10 %": 10, "20 %": 20, "21 %": 21, "110 %": 110, "121 %": 121}
T.task(3, "Délku strany čtverce zvětšíme o 10 %. O kolik procent se tím zvětší obsah čtverce?", "C",
       ["Původní strana je a, nová strana je 1,1 · a.", "Nový obsah: (1,1 · a)² = 1,21 · a², původní obsah je a².",
        "Nový obsah je 121 % původního, zvětšil se tedy o 21 %. Zkouška pro a = 10: 100 → 121.",
        "Chyby: 10 % je zvětšení strany, 20 % vznikne sečtením 10 % + 10 %, 110 % je nová délka strany a 121 % je nový obsah, ne jeho zvětšení."],
       [k for k, v in opts.items() if v == (F(11, 10) ** 2 - 1) * 100] == ["21 %"] and F(11, 10) ** 2 == F(121, 100)
       and 11 * 11 == 121,
       kind="choice", options=list(opts), space=3)

kroucek = F(60) / F(25, 100)
zaku = kroucek / F(40, 100)
T.task(3, "Do kroužku robotiky chodí 60 chlapců, což je 25 % všech chlapců školy. Chlapci tvoří 40 % všech žáků školy. "
          "Kolik žáků má škola?", f"{cz(zaku)} žáků",
       ["Do kroužku chodí 25 % = 1/4 všech chlapců, takže všech chlapců je 4 · 60 = 240.",
        "Chlapci tvoří 40 % = 2/5 všech žáků, tedy 2/5 žáků je 240.", "1/5 žáků je 240 : 2 = 120, všech žáků je 5 · 120 = 600.",
        "Zkouška: 40 % ze 600 = 240 chlapců a 25 % z 240 = 60 chlapců v kroužku. ✓"],
       kroucek == 240 and zaku == 600 and F(40, 100) * 600 == 240 and F(25, 100) * 240 == 60, space=4)

# ---------------------------------------------------------------- Úvodní test (2 úlohy tématu)
r = F(180 - 150, 150) * 100
T.diagnostic("Cena měsíční jízdenky vzrostla ze 150 Kč na 180 Kč. O kolik procent jízdenka zdražila?", f"o {cz(r)} %",
             ["Zdražení: 180 − 150 = 30 Kč.", "Základem je původní cena 150 Kč: 30 : 150 = 1/5 = 0,2 = 20 %."],
             r == 20 and F(30, 150) == F(1, 5))

opts = {"600 Kč": 600, "625 Kč": 625, "750 Kč": 750, "800 Kč": 800, "1 000 Kč": 1000}
T.diagnostic("Zboží stálo 800 Kč. Nejdřív zlevnilo o 25 %, potom zdražilo o 25 % z nové ceny. Kolik stojí nyní?", "C",
             ["Po zlevnění: 0,75 · 800 = 600 Kč.", "Po zdražení z nové ceny: 1,25 · 600 = 750 Kč.",
              "Cena se nevrátila na 800 Kč, protože druhá změna se počítá z nižšího základu."],
             [k for k, v in opts.items() if v == 800 * F(3, 4) * F(5, 4)] == ["750 Kč"] and 600 + 25 == 625
             and 800 * F(5, 4) == 1000,
             kind="choice", options=list(opts))

T.save()
