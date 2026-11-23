#!/usr/bin/env node
// Zet een deckmap klaar voor de HTML-renderer:
//   - map `npuls` naast het deck = junction (Windows) of symlink naar het Npuls-assetpakket (versie uit assets.lock)
//   - .gitignore in de deckmap: npuls, exports/ en de teamfoto niet in git (assets uit het pakket, exports naar SharePoint)
//   - CEDA-teamfoto (env CEDA_TEAMFOTO of ceda/teamfoto.png uit het pakket) naar img/team-groep.png
//   - zonder deck-HTML: kopieer frame.html als <mapnaam>.html en vul {{BRON_HASH}} in
// Gebruik: node <cedapress>/renderers/html/prepare.mjs presentaties/YYMMDD_onderwerp
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { npulsAssetsDir, npulsPaths } from '../lib/npuls-assets.mjs';
import { bronHash } from '../lib/bron.mjs';

const dir = process.argv[2];
if (!dir || !existsSync(dir)) { console.error('Gebruik: node prepare.mjs <deckmap>'); process.exit(2); }
const deckDir = resolve(dir);
let assets;
try { assets = npulsAssetsDir(); } catch (e) { console.error(`FOUT  ${e.message}`); process.exit(2); }

const link = join(deckDir, 'npuls');
if (existsSync(link) || (() => { try { return lstatSync(link).isSymbolicLink(); } catch { return false; } })()) {
  if (!lstatSync(link).isSymbolicLink()) { console.error(`FOUT  ${link} bestaat en is geen link — weghalen of hernoemen`); process.exit(2); }
  rmSync(link, { recursive: false, force: true });
}
symlinkSync(assets, link, process.platform === 'win32' ? 'junction' : 'dir');
console.log(`✓ npuls → ${assets}`);

const gi = join(deckDir, '.gitignore');
const want = ['npuls', 'exports/', 'img/team-groep.png'];
const have = existsSync(gi) ? readFileSync(gi, 'utf8').split(/\r?\n/) : [];
const add = want.filter((w) => !have.includes(w));
if (add.length) writeFileSync(gi, [...have.filter(Boolean), ...add].join('\n') + '\n');

const team = join(deckDir, 'img', 'team-groep.png');
if (!existsSync(team)) {
  const bron = npulsPaths().teamfoto;
  if (bron && existsSync(bron)) {
    mkdirSync(dirname(team), { recursive: true });
    copyFileSync(bron, team);
    console.log('✓ teamfoto → img/team-groep.png');
  } else console.log('WAARSCHUWING  geen teamfoto: zet CEDA_TEAMFOTO of leg img/team-groep.png neer ("Wie zijn wij")');
}

const name = basename(deckDir);
const html = join(deckDir, `${name}.html`);
const bron = join(deckDir, 'bron.md');
if (!existsSync(bron)) { console.error(`FOUT  ${bron} ontbreekt — schrijf eerst de bron-markdown (verplicht)`); process.exit(1); }
if (!existsSync(html)) {
  copyFileSync(join(dirname(fileURLToPath(import.meta.url)), 'frame.html'), html);
  const fancy = (readFileSync(bron, 'utf8').match(/^fancy:\s*([ABC])\b/m) || [, 'B'])[1];
  writeFileSync(html, readFileSync(html, 'utf8').replace('{{BRON_HASH}}', bronHash(bron)).replace('{{FANCY}}', fancy));
  console.log(`✓ frame gekopieerd → ${html}`);
}
console.log(`bron-hash: ${bronHash(bron)}`);
