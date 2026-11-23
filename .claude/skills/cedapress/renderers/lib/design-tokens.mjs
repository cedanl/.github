// design-tokens.json van vormgever-npuls-huisstijl vinden en inlezen: de enige bron van Npuls-kleurafspraken.
// cedapress kopieert niets uit dit bestand; de renderers (pptx/lib/tokens.mjs, html/check.mjs) lezen het.
// Volgorde: env NPULS_DESIGN_TOKENS (override, bv. om een wijziging te testen), de skill naast cedapress,
// dan ~/.claude/skills, ~/.agents/skills en ~/Projects/.github.
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REL = ['vormgever-npuls-huisstijl', 'references', 'design-tokens.json'];

export function tokenFile() {
  const env = process.env.NPULS_DESIGN_TOKENS;
  if (env && !existsSync(env)) throw new Error(`NPULS_DESIGN_TOKENS=${env} bestaat niet`);
  const found = [
    process.env.NPULS_DESIGN_TOKENS,
    resolve(HERE, '..', '..', '..', ...REL),
    join(homedir(), '.claude', 'skills', ...REL),
    join(homedir(), '.agents', 'skills', ...REL),
    join(homedir(), 'Projects', '.github', '.claude', 'skills', ...REL),
  ].find((p) => p && existsSync(p));
  if (!found) throw new Error('vormgever-npuls-huisstijl/references/design-tokens.json niet gevonden: installeer vormgever-npuls-huisstijl naast cedapress');
  return found;
}

const VEREIST = ['slide_roles', 'card_roles', 'tile_pairs', 'badge_fg', 'tints', 'component_defaults'];

export function loadTokens() {
  const t = JSON.parse(readFileSync(tokenFile(), 'utf8'));
  const mist = VEREIST.filter((k) => !t[k]);
  if (mist.length) throw new Error(`vormgever-npuls-huisstijl te oud of ontbreekt: design-tokens.json mist ${mist.join(', ')}. Update de skill (npx skills add cedanl/.github)`);
  return t;
}

/** Zoals loadTokens, maar bij een fout: melding en exit 2 (omgeving niet in orde) in plaats van een stacktrace. */
export function loadTokensOrExit() {
  try {
    return loadTokens();
  } catch (e) {
    console.error(`FOUT  ${e.message.startsWith('vormgever') ? e.message : `vormgever-npuls-huisstijl te oud of ontbreekt: ${e.message}. Update de skill (npx skills add cedanl/.github)`}`);
    process.exit(2);
  }
}

/** Tokennaam zonder merkvoorvoegsel: npuls-blauw wordt blauw, licht-geel blijft licht-geel. */
export const short = (name) => String(name).replace(/^npuls-/, '');

/** Klassenaam in de HTML-frame: blauw wordt blauw, licht-blauw wordt lblauw (zelfde regel als scripts/gen_npuls_css.py). */
export const htmlName = (name) => short(name).replace(/^licht-/, 'l');

/** Alle kleuren (primair + secundair) als { 'npuls-blauw': '<hex>', ... }. */
export function colorTable(t) {
  const real = (g) => Object.fromEntries(Object.entries(g).filter(([k]) => !k.startsWith('_')));
  return { ...real(t.colors.primary), ...real(t.colors.secondary) };
}
