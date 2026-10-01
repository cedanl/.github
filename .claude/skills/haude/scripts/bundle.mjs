#!/usr/bin/env node
// Maakt van een haude-deck één deelbaar bestand: fonts, logo en illustraties uit
// public/ worden als data-URI ingebakken. Font Awesome en Mentimeter blijven online.
// Gebruik: node <skill>/scripts/bundle.mjs YYMMDD_onderwerp.html [uit.html]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve, basename, extname, join } from 'node:path';

const file = process.argv[2];
if (!file) { console.error('Gebruik: node bundle.mjs <deck.html> [uit.html]'); process.exit(2); }
const name = basename(file, '.html');
const outFile = resolve(process.argv[3] || join('exports', name, `${name}.html`));
const base = dirname(resolve(file));
const mime = { '.otf': 'font/otf', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp' };

let n = 0, bytes = 0;
const html = readFileSync(file, 'utf8').replace(
  /(\ssrc=["']|url\(["']?)(?!https?:|data:|#)([^"')\s][^"')]*)/g,
  (all, pre, path) => {
    const p = resolve(base, decodeURI(path));
    const type = mime[extname(p).toLowerCase()];
    if (!type || !existsSync(p)) return all;
    const buf = readFileSync(p); n++; bytes += buf.length;
    return `${pre}data:${type};base64,${buf.toString('base64')}`;
  });

mkdirSync(dirname(outFile), { recursive: true });
writeFileSync(outFile, html);
console.log(`✓ ${n} bestanden ingebakken (${(bytes / 1024).toFixed(0)} kB) → ${outFile}`);
