// Node-afhankelijkheden (playwright-chromium, pptxgenjs) laden.
// Decks staan in de projectrepo, die meestal geen node_modules heeft. Volgorde:
//   1. node_modules van de huidige map (bv. een repo die ze zelf heeft)
//   2. node_modules van cedapress zelf: eenmalig `npm install --prefix <cedapress>/renderers`
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const RENDERERS = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const bases = [join(process.cwd(), 'package.json'), join(RENDERERS, 'package.json')];

export function requireDep(name) {
  let last;
  for (const b of bases) {
    try { return createRequire(b)(name); } catch (e) { last = e; }
  }
  const err = new Error(`${name} niet gevonden. Eenmalig: npm install --prefix "${RENDERERS}"`);
  err.cause = last;
  throw err;
}
