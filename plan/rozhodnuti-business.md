# Rozhodnutí o novém businessu (#13, 2026-10-02 15:0x Praha, vyšší model)

> **REVIZE 2026-10-02 15:12: celé rozhodnutí níže je ZRUŠENO.** Ondřej mi sdělil, že 1) má živý web mypixel.cz (MYPIXEL s.r.o., WordPress weby od 14 800 Kč, 85+ webů, 5,0 z 24 Google recenzí, sólo) a webprodava.cz (nabídka webů, Ing. Ondřej Chloupek), 2) už platí ePoptávku 500 Kč měsíčně a poptávkové portály tohoto typu nechce (duplicita). Sonda „Dílna na poptávky“ (#21) i stránka dílny na webprodava.cz (#14) jsou zrušeny; webové služby jsou duplicitní s jeho vlastním byznysem. Ponechávám jako záznam analýzy (čísla trhu poptávek platí). Aktuální stav: `plan/stav-session.md` a akce #22, #23.

Podklady: `plan/alternativy-2026-10-02.md` (data, konkurence, dodatky o podílu a prezentaci), `plan/hledanost-alt2-*.md` (verdikty), `plan/postupy/zahranicni-sluzby.md`, `plan/konkurence-web-za-24-hodin.md`. Čísla, která tu nejsou změřená, jsou označená jako odhad.

## Rozhodnutí
**Jeden business, ne tři: „Dílna na poptávky“.** K1 (úkol za pevnou cenu), K2 (měsíční balíček 2 990 Kč) a K3 (projekt 15 až 60 tis. Kč) mají stejný kanál (veřejné poptávky, kde zadavatel sám chce nabídku), stejnou dodávku (Claude) i stejnou nejistotu (míra výhry nové firmy). Testuji je jednou sondou s třemi úrovněmi nabídky; podle poptávky se zvolí úroveň, podle segmentu varianta prezentace.
- Verdikt K1+K2: ANO/ANO (`plan/hledanost-alt2-poptavky.md`, na hraně 5,1 vs. 5). Sonda nic nestaví, jen odpovídá, proto výjimka z verdiktu není potřeba ani pro K3 (ten bez výjimky nesmí jen samostatné stavění nebo reklamu).
- **Samostatný test „Web za 24 hodin“ na Bazoši ruším** (Bazoš je tržiště prodávajících: 59 inzerátů webů, 0 „poptávám web“, medián 62 zobrazení za celou dobu inzerátu). Nabídka webu přechází do K3 odpovědí, ušetří se 147 Kč.
- Business je typ A (vyžaduje práci Clauda), ne pasivní. Ondřej podle varianty Shoptetu níže 0 až ≈ 25 minut měsíčně.

## Pořadí (konečné)
| # | Kandidát | 2a Umím to? | 2b Ukousnutelný podíl | Šance na A do 6 měs. (odhad) | Rozhodnutí |
|---|---|---|---|---|---|
| 1 | Dílna na poptávky (K1+K2+K3) | ano, kromě telefonu; tři věci ověřit do 24 h (níže) | potřeba výhra ≈ 3 až 5 % z ≈ 45 poptávek měsíčně; bez dokladu se bere 1 % = NEOVĚŘENO, změří sonda | ≈ 25 % | **sonda hned po schválení** |
| 2 | K4 digitální produkty pro svět (Etsy) | ano (šablony ověřené přepočtem, angličtina); Etsy API pro inzeráty ověřit | B = 9 prodejů měsíčně ≈ 11 % prodejů jednoho zavedeného konkurenta; neověřeno | A ≈ 10 %, B ≈ 30 % | jen krok 0 (Google a Etsy objem, ≈ 0 Kč); sonda až z prvních tržeb č. 1 |
| 3 | K6 doplněk pro Shoptet | ano (kód), schválení Shoptetu neznámé | ≈ 29 platících z 48 410 e-shopů, blokuje vítěz bere vše a schválení | ≈ 5 % | po 2 až 4 týdnech dat z č. 1 (opakované požadavky ≥ 5×) |
| 4 | K5 3D tisk katalogově | ano (STL parametricky, ověřeno), tisk Ondřej | marže 20 až 50 Kč na hodinu tisku, ne konkurence | ≈ 5 % | NE pro A; jen s konkrétním výrobkem s vyšší marží |
| – | Upwork/Fiverr jako druhý kanál č. 1 | ano, ale nabídku musí odeslat člověk; Upwork ≈ 1,5 až 2,5 USD za nabídku | trh o řády větší, výhra nového profilu ≈ 1 až 3 % (odhad) | – | až po ověření dodávky a výhry v č. 1 |
| – | K7 hlídač zakázek, K8 hlídání partnerů, K9 zakázky malého rozsahu, K10 chatbot | ano | blokuje kanál nebo zdarma alternativa, ne konkurence | < 5 % | zamítnuto (důvody v `plan/alternativy-2026-10-02.md`) |

## 1. Dílna na poptávky: podrobně
**2a Schopnost.** Konkrétní odpověď s návrhem řešení, cenou a termínem: ano. Importy a migrace (Excel, XML, Websnadno, WebCzech, Wix → Shoptet): ano, převod skriptem do formátu importu Shoptetu, starý web se dá stáhnout přes proxy. Úpravy vzhledu a funkcí (HTML, CSS, JS v „Editaci kódu“), slevy, dárky, poukazy: ano jako kód; použití v administraci zákazníka potřebuje prohlížeč z kontejneru. Weby a e-shopy K3: ano (Next.js, QR platby a Fio z našich projektů, hosting Netlify). Napojení Pohoda, Premiér, Baselinker: jen tam, kde jde o soubory nebo zdokumentované API. **Neumím: telefonovat a chodit na schůzky** (slabina hlavně u K3) a garantovat odpověď mimo běh hodinové rutiny. Kapacita: středně ≈ 25 až 35 hodin práce Clauda měsíčně; strop jsou limity Ondřejova předplatného (riziko dostupnosti, ne náklad firmy).
Ověřit do 24 h (dávka Sonnet, 0 Kč): (a) Playwright otevře cizí HTTPS administraci (README uvádí nastavený NSS store, dříve chyba certifikátu); plán B: zákazník vloží kód podle návodu; (b) vzorový import a úprava na zkušebním e-shopu Shoptet (30 dní zdarma, registraci autorizuje Ondřej); (c) kdo smí odpovídat na poptávky Shoptetu (jen partneři, nebo kdokoli přes formulář) a zda je Webtrh Premium pro odpovědi nutné, za kolik a na jak dlouho.

**2b Trh, výhody, nika, podíl.** Trh: ≈ 45 použitelných poptávek měsíčně (Shoptet ≈ 25, Webtrh ≈ 11, ePoptávka ≈ 6, Poptavky.cz ≈ 3; u ePoptávky a Poptavky.cz ověřit, zda kontakt není placený), z toho ≈ 12 s rozpočtem ≥ 15 tis. Kč. Koncentrace: 776 partnerů Shoptetu, zavedené agentury (Sniper Design 600+ klientů, Webotvůrci 1 500+ instalací), freelanceři 500 až 550 Kč za hodinu.
Výhody s důkazem: 1) pevná cena předem místo hodinové sazby (ceník janat-epromo.cz 500 až 550 Kč/h); 2) balíček 2 990 Kč měsíčně proti 10 500 Kč za 20 h freelancera (tamtéž); 3) hotový kus řešení už v odpovědi (vzorek převedeného importu, návrh kódu, náhled první obrazovky webu u K3), což konkurence s hodinovou sazbou zdarma nedělá (důkaz: připravím pro 3 živé poptávky v dávce Sonnet); 4) malé úkoly platí zákazník až po předání (riziko nese firma, částky do ≈ 6 000 Kč); 5) odpověď do 2 hodin v pracovní dny (doloží měření v sondě).
Úzká nika: **převody dat a migrace na Shoptet za pevnou cenu do 48 hodin** (objektivně ověřitelný výsledek, malá vizuální složka, konkurence ji účtuje hodinově). Bereme i ostatní poptávky, které AI zvládne.
Podíl: A do 6 měsíců vyžaduje výhru ≈ 3 % (když 25 % vyhraných přejde na balíček) až ≈ 5 % (když jen 10 %), tj. 1,5 až 2,5 zakázky z ≈ 45 měsíčně plus kumulace balíčků. Bez dokladu platí 1 %, tedy ukousnutelnost je NEOVĚŘENÁ a rozhodne sonda. K3 je jen přidaný potenciál (0,18 zakázky měsíčně při výhře 1,5 % ≈ 5 400 Kč v průměru).

**2c Prezentace (každá odpověď nese značku varianty).**
- V1 „Technik na zavolanou“: majitel e-shopu s jednorázovým problémem, „nechci platit agenturu a týden čekat“; pevná cena předem, hotovo do 24 až 48 h, platba po předání; kotva freelancer 500 až 550 Kč/h; konkurence freelanceři a partneři Shoptetu.
- V2 „Měsíční balíček úprav“: e-shop, který úpravy potřebuje pořád; 2 990 Kč měsíčně, pevný rozsah, výpověď kdykoli; kotva 10 500 Kč za 20 h; nabízí se v každé odpovědi jako druhá možnost.
- V3 „Rychlé ruce pro agentury“: agentury a freelanceři, kteří nestíhají (poptávky na Webtrhu od kolegů); pevná cena za úkol, předání s dokumentací, bez kontaktu s jejich klientem.
- V4 (K3) „Nový web nebo e-shop s náhledem předem“: firma bez webu nebo se zastaralým, rozpočet ≥ 15 tis.; náhled první obrazovky v odpovědi, platba 50 % po schválení náhledu; kotva agentura 50 až 250 tis., freelancer 15 až 50 tis.; slabina bez hovoru, proto komunikace písemně uvedená předem.
Poctivost ve všech: otevřeně „pracujeme s AI, výsledek kontrolujeme“, nová firma, pilotní cena a záruka, žádné reference ani počty klientů, které nemáme. Ukázky jen jako „ukázkový projekt“.

**3 Ekonomika.** Náklad sondy 0 až 465 Kč (Webtrh), hosting náhledů Netlify Free 0 Kč, doména webprodava.cz už je. Střední scénář (výhra 5 % u Shoptetu a 3 % u Webtrhu, odhad): ≈ 2,6 úkolu měsíčně × 3 500 Kč, k tomu balíčky ≈ 3 po 6 měsících, celkem ≈ 15 až 25 tis. Kč tržeb v 6. měsíci. Pesimistický (výhra 1 až 2 %): ≈ 2 až 5 tis. Kč, A nevyjde.

**4 Test.**
- Do 72 h od schválení: ≥ 20 odpovědí na živé poptávky (Shoptet backlog, Webtrh, ePoptávka), každá na míru s kusem řešení a značkou varianty. Pokračovat: ≥ 2 reakce zadavatele (dotaz, žádost o upřesnění nebo cenu). Zastavit nebo změnit variantu: 0 reakcí z 20.
- Do 28 dní (≥ 40 odpovědí): **pokračovat k A** při ≥ 2 zaplacených zakázkách (výhra ≈ 5 %) nebo 1 zakázce a 1 balíčku; **prodloužit o 28 dní** při 1 zakázce; **zastavit jako kandidáta A** při 0 zaplacených, zapsat `plan/dilna-vyhodnoceni.md`.
- Měření: tabulka `plan/sonda-poptavky.csv` (datum, portál, kategorie, rozpočet, varianta, čas odpovědi, reakce, výsledek, částka, důvod ne), sekce v `tools/stav.py`, odmítnutí se ptají na důvod (cena, AI, reference, termín).
- Přistávací stránka (#14, upravený rozsah): stránka dílny na webprodava.cz (nabídka, ceny, jak pracujeme s AI, firma v patičce), aby odkaz v odpovědích budil důvěru. Stavět až po schválení sondy, návrh na vyšším modelu; prvních 72 h se odpovídá i bez ní.

## Co schvaluje Ondřej
1. **„ano, sonda poptávek“** (start; Bazoš test se ruší).
2. **Shoptet poptávky** (formulář má reCAPTCHA, kterou neobcházím): 🥇 odpovědi připravím a ty je jen vložíš a odešleš (≈ 1 minuta na kus, ≈ 25 měsíčně); je to ruční práce mimo tvou roli, ale bez Shoptetu klesne trh na ≈ 20 poptávek měsíčně a A přes tento kanál do 6 měsíců téměř nevyjde. 🥈 Shoptet vynechat (0 minut, šance na A ≈ 10 %). 🥉 Psát na veřejný e-mail e-shopu (nedoporučuji: šedá zóna zákona 480/2004 § 7 a podmínek Shoptetu).
3. **Obchodní podmínky služby** (právo): rozšířím návrh v `plan/web-za-24-hodin.md` o úkoly, balíček a projekty (B2B, odpovědnost do výše ceny, zpracovatelská smlouva GDPR při přístupu do administrace, otevřené uvedení AI) a pošlu ke schválení.
4. **Webtrh Premium 465 Kč** (finance), jen pokud ověřím, že bez něj odpovídat nejde.
5. Autorizace: e-mailová adresa dílny (např. web@mypixel.cz), kterou čtu a z níž odesílám přes Gmail konektor, a registrace zkušebního e-shopu Shoptet.

## Výhrada (jednou)
I nejlepší kandidát má podle mě šanci na A do 6 měsíců jen ≈ 25 %. Hlavní rizika: nová firma bez hodnocení a bez telefonu, chyba v cizím e-shopu (pověst a odpovědnost), závislost na limitech předplatného. Proto malá sonda s jasným zastavením, ne investice.

## Další kroky (dávka Sonnet po přepnutí zpět)
1. Ověření 2a (a) až (c), 2. tři vzorové odpovědi na živé poptávky s kusem řešení, 3. podmínky služby k bodu 3, 4. `plan/sonda-poptavky.csv` a sekce v `tools/stav.py`, 5. K4 krok 0 až po autorizaci účtu DataForSEO (tamtéž levně ověřit Google objem klíčových dotazů Printopie, jen jako informace, bez přepracování).
