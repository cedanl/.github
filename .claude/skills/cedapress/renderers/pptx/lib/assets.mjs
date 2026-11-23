// Npuls-assets uit het versioned assetpakket (zie ../../lib/npuls-assets.mjs): illustraties (SVG → PNG), beeldmerk, logo.
import { existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { requireDep } from '../../lib/deps.mjs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { npulsPaths } from '../../lib/npuls-assets.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
let NP;
try { NP = npulsPaths(); } catch (e) { console.error(`FOUT  Npuls-assetpakket niet beschikbaar: ${e.message}`); process.exit(2); }
export const NPULS = NP;
export const ILLU_DIR = NP.illustraties;
export const LOGO = NP.logoJpg;
// Logo's en beeldmerk komen uit logos/ van het assetpakket.
export const SKILL_ASSETS = NP.logos;
// Volledige horizontale logo (stippenring + woordmerk), transparant. Wit voor blauwe vlakken, zwart voor lichte.
export const LOGO_HORIZONTAAL = { wit: join(SKILL_ASSETS, 'npuls-logo-horizontaal-wit.png'), zwart: join(SKILL_ASSETS, 'npuls-logo-horizontaal-zwart.png') };
// Echte titelachtergrond (blauw met de bogen) uit de Npuls-powerpointsjabloon.
export const TITEL_ACHTERGROND = join(NP.slidesPreview, 'slide15.png');
// Standaard Npuls-titelslide: roze, zwart logo linksboven, oranje bogen rechtsonder (logo en bogen zitten in de afbeelding).
export const TITEL_ROZE = join(NP.slidesPreview, 'slide01.png');

// pptxgenjs en playwright: uit de huidige map of uit cedapress/renderers/node_modules.
export const projectRequire = requireDep;

// Oude namen (public/npuls/powerpoint_illustrations) → nummer in het assetpakket, zodat oude deck-specs blijven werken.
// Visueel gekoppeld op 2026-11-19; namen zonder tegenhanger in het pakket staan er niet in.
export const ILLU_ALIAS = {
  learninganalystics: 1, kunstmatigeintelligentie: 2, chip: 3, Connecties: 4, brains: 5, data: 6, Servers: 6,
  kennisdeling: 7, books: 8, events: 9, hands: 10, gesprek: 11, hat: 12, 'Laptop met beeld': 13, Combineren: 14,
  vr: 15, present: 16, pc: 17, Financien: 18, bestuurder: 18, light: 19, Lamp: 19, netwerk: 20,
  'Gebouw blauw met boom': 21, schoolgebouwen: 21, onderwijsprofessional: 22, locatie: 23, verrekijker: 24,
  cadeau: 25, video: 26,
};
export function illustrationPath(name) {
  const base = String(name).replace(/\.svg$/i, '');
  const nr = /^\d+$/.test(base) ? Number(base) : ILLU_ALIAS[base];
  const file = nr ? `illustratie-${String(nr).padStart(2, '0')}.svg` : `${base}.svg`;
  return join(ILLU_DIR, file);
}

// Rasteriseer SVG-illustraties eenmalig naar PNG: SVG in PowerPoint werkt pas
// vanaf 2019/365 en niet in alle viewers (Keynote, oudere Office, previews).
export async function rasterize(svgPaths, outDir, px = 1200) {
  const todo = [];
  const out = new Map();
  mkdirSync(outDir, { recursive: true });
  for (const p of svgPaths) {
    const png = join(outDir, p.split(/[\\/]/).pop().replace(/\.svg$/i, '.png'));
    out.set(p, png);
    if (!existsSync(png) || statSync(png).mtimeMs < statSync(p).mtimeMs) todo.push([p, png]);
  }
  if (!todo.length) return out;
  const { chromium } = projectRequire('playwright-chromium');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: px, height: px }, deviceScaleFactor: 1 });
  for (const [svg, png] of todo) {
    const src = readFileSync(svg, 'utf8');
    await page.setContent(
      `<html><body style="margin:0;background:transparent">` +
      `<img id="i" style="width:${px}px;height:${px}px;object-fit:contain" src="data:image/svg+xml;base64,${Buffer.from(src).toString('base64')}">` +
      `</body></html>`
    );
    await page.waitForFunction(() => document.getElementById('i').complete);
    await page.locator('#i').screenshot({ path: png, omitBackground: true });
  }
  await browser.close();
  return out;
}

// Echt Npuls-beeldmerk (stippenring): de stippen staan genormaliseerd in logos/beeldmerk-ring.json van het
// assetpakket. Wordt als losse vector-cirkels getekend, zodat de kleur per variant klopt.
export function beeldmerkDots() {
  const ring = join(SKILL_ASSETS, 'beeldmerk-ring.json');
  return existsSync(ring) ? JSON.parse(readFileSync(ring, 'utf8')) : null;
}

// Afmetingen van PNG/JPEG lezen, voor schermafbeeldingen die passend moeten schalen.
export function imageSize(path) {
  const b = readFileSync(path);
  if (b.readUInt32BE(0) === 0x89504e47) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  if (b[0] === 0xff && b[1] === 0xd8) {
    let i = 2;
    while (i < b.length) {
      const marker = b[i + 1];
      const len = b.readUInt16BE(i + 2);
      if (marker >= 0xc0 && marker <= 0xc3) return { w: b.readUInt16BE(i + 7), h: b.readUInt16BE(i + 5) };
      i += 2 + len;
    }
  }
  throw new Error(`Kan afmetingen van ${path} niet lezen (alleen PNG/JPEG).`);
}
