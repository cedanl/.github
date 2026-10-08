// Npuls-assets uit clidev-presentaties: illustraties (SVG → PNG), beeldmerk, logo.
import { existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
export const ILLU_DIR = 'public/npuls/powerpoint_illustrations';
export const LOGO = 'public/npuls/npuls_logo.jpg';
// Logo's en beeldmerk staan in de projectroot, naast de andere Npuls-assets (de skill draait alleen daar).
export const SKILL_ASSETS = 'public/npuls/logos';
// Volledige horizontale logo (stippenring + woordmerk), transparant. Wit voor blauwe vlakken, zwart voor lichte.
export const LOGO_HORIZONTAAL = { wit: join(SKILL_ASSETS, 'npuls-logo-horizontaal-wit.png'), zwart: join(SKILL_ASSETS, 'npuls-logo-horizontaal-zwart.png') };
// Echte titelachtergrond (blauw met de bogen) uit de Npuls-powerpointsjabloon.
export const TITEL_ACHTERGROND = 'public/npuls/powerpoint_slides/Slide15.PNG';

// pptxgenjs en playwright komen uit de node_modules van het project, niet uit de skill.
export const projectRequire = createRequire(join(process.cwd(), 'package.json'));

export function illustrationPath(name) {
  const file = name.endsWith('.svg') ? name : `${name}.svg`;
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

// Echt Npuls-beeldmerk (stippenring): de stippen staan genormaliseerd in assets/beeldmerk-ring.json.
// Wordt als losse vector-cirkels getekend, zodat de kleur per variant klopt. Valt terug op het
// indicatieve SVG uit vormgever-npuls-huisstijl als het bestand ontbreekt.
export function beeldmerkDots() {
  const ring = join(SKILL_ASSETS, 'beeldmerk-ring.json');
  if (existsSync(ring)) return JSON.parse(readFileSync(ring, 'utf8'));
  const candidates = [
    resolve(HERE, '../../../vormgever-npuls-huisstijl/assets/logos/beeldmerk.svg'),
    join(homedir(), '.claude', 'skills', 'vormgever-npuls-huisstijl', 'assets', 'logos', 'beeldmerk.svg'),
    join(homedir(), '.agents', 'skills', 'vormgever-npuls-huisstijl', 'assets', 'logos', 'beeldmerk.svg'),
    join(homedir(), 'Projects', '.github', '.claude', 'skills', 'vormgever-npuls-huisstijl', 'assets', 'logos', 'beeldmerk.svg'),
  ];
  const file = candidates.find((p) => existsSync(p));
  if (!file) return null;
  const svg = readFileSync(file, 'utf8');
  const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const size = vb ? Number(vb[1]) : 72;
  const dots = [...svg.matchAll(/<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"/g)]
    .map((m) => ({ cx: +m[1] / size, cy: +m[2] / size, r: +m[3] / size }));
  return dots.length ? dots : null;
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
