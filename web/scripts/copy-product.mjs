// Zkopíruje prodejní verzi plánovače z product/dist do web/private (mimo public, stahuje se jen po zaplacení).
import { copyFileSync, mkdirSync } from "node:fs";

const name = "svatebni-planovac-anoberu.xlsx";
mkdirSync(new URL("../private/", import.meta.url), { recursive: true });
copyFileSync(new URL(`../../product/dist/${name}`, import.meta.url), new URL(`../private/${name}`, import.meta.url));
console.log(`private/${name} připraven`);
