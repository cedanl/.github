#!/usr/bin/env node
// Maakt van een cedapress-HTML-deck één deelbaar bestand: npuls/web/npuls.css (fonts blijven via CDN) en alle lokale
// afbeeldingen (assetpakket via npuls/, eigen afbeeldingen) worden ingebakken. Font Awesome, GSAP en Mentimeter blijven online.
// Gebruik: node <cedapress>/renderers/html/bundle.mjs presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html [uit.html]
// Standaard naar <deckmap>/exports/<naam>.html (niet in git; delen via SharePoint).
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve, basename, extname, join } from 'node:path';

const file = process.argv[2];
if (!file) { console.error('Gebruik: node bundle.mjs <deck.html> [uit.html]'); process.exit(2); }
const name = basename(file, '.html');
const base = dirname(resolve(file));
const outFile = resolve(process.argv[3] || join(base, 'exports', `${name}.html`));
const mime = { '.otf': 'font/otf', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp' };

let n = 0, bytes = 0;
const inline = (text, from) => text.replace(
  /(\ssrc=["']|url\(["']?)(?!https?:|data:|#)([^"')\s][^"')]*)/g,
  (all, pre, path) => {
    const p = resolve(from, decodeURI(path));
    const type = mime[extname(p).toLowerCase()];
    if (!type || !existsSync(p)) return all;
    const buf = readFileSync(p); n++; bytes += buf.length;
    return `${pre}data:${type};base64,${buf.toString('base64')}`;
  });
// lokale stylesheets (npuls/web/npuls.css) als <style> inbakken, url()'s relatief aan de css
const withCss = readFileSync(file, 'utf8').replace(
  /<link\b[^>]*rel=["']stylesheet["'][^>]*href=["'](?!https?:)([^"']+)["'][^>]*>/g,
  (all, href) => {
    const p = resolve(base, decodeURI(href));
    if (!existsSync(p)) return all;
    return `<style>/* ${href} */\n${inline(readFileSync(p, 'utf8'), dirname(p))}\n</style>`;
  });
const html = inline(withCss, base);

mkdirSync(dirname(outFile), { recursive: true });
writeFileSync(outFile, html);
console.log(`✓ ${n} bestanden ingebakken (${(bytes / 1024).toFixed(0)} kB) → ${outFile}`);
