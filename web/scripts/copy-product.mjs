// Zkopíruje prodejní verzi plánovače z product/dist do web/private (mimo public, stahuje se jen po zaplacení).
// Kopie je i v gitu, takže build funguje i při nasazení samotné složky web/ (bez product/).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";

const name = "svatebni-planovac-anoberu.xlsx";
const src = new URL(`../../product/dist/${name}`, import.meta.url);
const dst = new URL(`../private/${name}`, import.meta.url);
mkdirSync(new URL("../private/", import.meta.url), { recursive: true });
if (existsSync(src)) {
  copyFileSync(src, dst);
  console.log(`private/${name} aktualizován z product/dist`);
} else if (existsSync(dst)) {
  console.log(`private/${name} použit z gitu`);
} else {
  throw new Error(`Chybí ${name}: ani product/dist, ani web/private`);
}
