import Script from "next/script";

/**
 * Měření návštěvnosti v Project Trackeru MYPIXEL (tracker.mypixel.cz): bez cookies, ukládají se jen denní souhrny.
 * Na localhost a *.vercel.app skript nic neposílá. Měření chování (data-behavior) je vypnuté.
 */
export default function TrackerScript() {
  return <Script src="https://tracker.mypixel.cz/n.js" data-site="printopia" data-behavior="off" strategy="afterInteractive" />;
}
