import Script from "next/script";

/**
 * Měření návštěvnosti v Project Trackeru MYPIXEL (tracker.mypixel.cz): bez cookies, ukládají se jen denní souhrny.
 * Na localhost a *.vercel.app skript nic neposílá. Měří i chování na stránce, jen v denních součtech (bez nahrávání, bez hodnot polí).
 */
export default function TrackerScript() {
  return <Script src="https://tracker.mypixel.cz/n.js" data-site="printopia" strategy="afterInteractive" />;
}
