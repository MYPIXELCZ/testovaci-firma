# Design průzkum: printopia.cz (přijímačky z matiky po tématech)

Datum: 2026-10-01. Screenshoty a osnovy stránek pořízeny automaticky (Chromium), soubory jen lokálně (autorská práva cizích webů).

## Konkurence (rozbor prodejních stránek)
| Web | Úvod (nad ohybem) | Důvěra | Publikum | CTA |
|---|---|---|---|---|
| skolapopulo.cz/videoreseni-prijimacky | Fotka dvou lektorů s testy v rukou, checklist přínosů s čísly (78 testů, krok za krokem), sleva do data | „Zakoupilo 450+ studentů“, statistiky (11 let, 36 000 studentů, 96 %) | Tyká žákovi („Udělej testy. Uděláš přijímačky.“) | Červené „Koupit videořešení“ |
| prijimacky-onlinekurzy.cz | Tmavý blok, checklist s čísly (32 h videí, 600+ úloh), ukázková lekce zdarma vpravo | Lišta „5,0 Google, 180+ recenzí“, tváře lektorů, reference rodičů i studentů | Vyká, píše pro rodiče i žáky | Zelené „Začít přípravu – od 3 990 Kč“ + „Prohlédnout lekce“ |
| to-das.cz | Barevné karty podle ročníků, urgence (obsazená místa), % přijatých | „Co oceňují rodiče“ × „Co oceňují děti“, „100% garance spokojenosti“, „S nákupem nic neriskujete“ | Obě skupiny zvlášť | Karty s odkazy |
| statniprijimacky.cz, umimematiku.cz | Informační (termíny, testy), bez prodejního úvodu | Autorita obsahu | Žáci | Slabé |

## Prvky, které prodávají (ověřeno na konkurenci)
1. Konkrétní přínosy v číslech hned v úvodu (počet úloh, témat, hodin).
2. Cena přímo v hlavním tlačítku + druhé tlačítko na ukázku zdarma.
3. Důvěra: garance vrácení peněz, kdo za tím stojí, (u nás zatím žádné recenze → nevymýšlet, nahradit transparentností a ukázkou).
4. Dvě publika: „Co oceňují rodiče“ (nemusí vysvětlovat, vědí na čem dítě je, cena) a „Co oceňují deváťáci“ (postup, papír jako u zkoušky). Bez výzvy dětem ke koupi.
5. Čas: odpočet do zkoušky (12. 4. 2027) a plán, co stihnout.
6. Srovnání ceny s alternativami (doučování 200–350 Kč/h, videořešení 7 900–9 900 Kč, kurz 3 990 Kč) se zdroji.
7. Skutečný produkt vidět (náhledy stránek PDF) a lidská fotka (Unsplash, scéna učení, ne „náš tým“).
8. FAQ, sticky CTA na mobilu.

## Vizuální směr
- Tmavě modrý úvodní blok (#1c2230) s žlutým akcentem (#f5b82e) jako tužka/zvýrazňovač, zbytek světlý papír (#fbfaf6).
- Hlavní CTA žluté s tmavým textem (kontrast, odliší se od modrých odkazů), sekundární obrysové.
- Fotky: Unsplash (licence zdarma i komerčně, bez Unsplash+): žák nad úlohami, rodič a dospívající u stolu. Access Key od Ondřeje (limit 50 dotazů/h, šetřit; náhledy z CDN se nepočítají). Fotky jsou hostované u nás (`printopia/public/foto/`), autoři v `src/content/foto.json`.
- Typografie: Fraunces (nadpisy) + Inter (text), jako doteď.

## Kontrolní seznam před nasazením
- [x] úvod: nabídka pro plátce, přínosy v číslech, cena v CTA, ukázka zdarma
- [x] náhled skutečného produktu
- [x] lidské fotky (Unsplash, Vitaly Gariev a Annie Spratt, licence Unsplash, stažení ohlášeno přes API, uvedení autora u fotky)
- [x] srovnání ceny se zdroji, záruka, kdo za tím stojí, FAQ
- [x] rodiče × deváťáci, bez výzvy dětem ke koupi
- [x] screenshoty desktop + mobil zkontrolované

## Texty
Každý blok úvodní stránky odpovídá na otázku plátce (rodiče), u karty pro deváťáky na otázku uživatele. Provozovatel jen v patičce.
- Úvod: „Pomůže to mému dítěti s tím, co mu nejde?“ → nadpis, 4 přínosy, cena v tlačítku, ukázka zdarma, jednorázově a vrácení peněz.
- Odpočet: „Stihneme to?“ → dny do zkoušky a čas na téma.
- Pro rodiče / pro deváťáky: „Zvládnu to, když neumím matiku?“ / „Co z toho mám já?“
- Dvě úlohy: „Jak vypadají úlohy a postup?“ → vyzkoušet, výsledek až po rozkliknutí.
- 12 témat: „Co přesně v sadě je?“
- Cena + záruka: „Kolik to stojí oproti doučování a co když to nesedne?“
- Ukázka PDF: „Můžu to vyzkoušet na papíře?“
- FAQ: kdy, pro koho, oficiální?, zaručíte přijetí?; anketa: proč ne.
