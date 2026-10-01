import { PRICE, SITE_URL } from "@/lib/config";

// Produktový feed pro Zboží.cz (Seznam Nákupy), specifikace https://napoveda.sklik.cz/reklamy/xml-feed/specifikace/
// Pravidla (plan/postupy/zbozi-heureka.md): bez slov „kurz“, „e-learning“, „oficiální“, „CERMAT“, bez superlativů; cena musí být shodná s /koupit.
export const dynamic = "force-static";

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

export function GET() {
  const base = SITE_URL.replace(/\/$/, "");
  const xml = `<?xml version="1.0" encoding="utf-8"?>
<SHOP xmlns="http://www.zbozi.cz/ns/offer/1.0">
  <SHOPITEM>
    <ITEM_ID>printopia-matematika-sada</ITEM_ID>
    <PRODUCTNAME>${esc("Printopia Přijímačky z matematiky po tématech, sada PDF")}</PRODUCTNAME>
    <DESCRIPTION>${esc(
      "Sada 14 souborů PDF k vytištění: úvodní test, 12 tematických sad úloh s postupem řešení a plán procvičování. " +
        "Pro žáky 9. tříd, kteří se připravují na jednotnou přijímací zkoušku z matematiky. Digitální obsah, soubory ke stažení po zaplacení."
    )}</DESCRIPTION>
    <URL>${esc(`${base}/koupit?utm_source=zbozi&utm_medium=cpc`)}</URL>
    <PRICE_VAT>${PRICE}</PRICE_VAT>
    <DELIVERY_DATE>0</DELIVERY_DATE>
    <IMGURL>${esc(`${base}/zbozi-sada.png`)}</IMGURL>
    <CATEGORYTEXT>${esc("Kultura a zábava | Knihy | Učebnice | Přírodní vědy | Matematika")}</CATEGORYTEXT>
    <MANUFACTURER>Printopia</MANUFACTURER>
    <DELIVERY>
      <DELIVERY_ID>ONLINE</DELIVERY_ID>
      <DELIVERY_PRICE>0</DELIVERY_PRICE>
    </DELIVERY>
    <MAX_CPC_SEARCH>4</MAX_CPC_SEARCH>
    <MAX_CPC>4</MAX_CPC>
  </SHOPITEM>
</SHOP>
`;
  return new Response(xml, { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
}
