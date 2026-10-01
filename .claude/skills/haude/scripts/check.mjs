#!/usr/bin/env node
// Statische huisstijlcheck voor een haude-deck.
// Gebruik: node <skill>/scripts/check.mjs YYMMDD_onderwerp.html
// Exit 1 bij fouten, 0 als alleen waarschuwingen of niets.
import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const file = process.argv[2];
if (!file) { console.error('Gebruik: node check.mjs <deck.html>'); process.exit(2); }
const html = readFileSync(file, 'utf8');
const base = dirname(resolve(file));
const errors = [], warns = [];
const lineOf = idx => html.slice(0, idx).split('\n').length;

// 1. Geen hex-kleuren buiten het :root-tokenblok
const root = html.match(/:root\s*\{[\s\S]*?\}/);
const rootStart = root ? root.index : -1, rootEnd = root ? root.index + root[0].length : -1;
for (const m of html.matchAll(/#[0-9a-fA-F]{3,8}\b/g)) {
  if (m.index >= rootStart && m.index < rootEnd) continue;
  const before = html.slice(Math.max(0, m.index - 12), m.index);
  if (/href=["']$|&$|url\(["']?$/.test(before)) continue; // anker, entity, fragment
  if (/#s\d/.test(m[0])) continue;
  errors.push(`regel ${lineOf(m.index)}: hardcoded kleur ${m[0]} — gebruik var(--npuls-*) of var(--licht-*)`);
}

// 2. Elke slide precies één variant
const variants = [];
for (const m of html.matchAll(/<section\s+class="([^"]*\bslide\b[^"]*)"/g)) {
  const v = m[1].split(/\s+/).filter(c => /^s-/.test(c));
  if (v.length !== 1) errors.push(`regel ${lineOf(m.index)}: slide heeft ${v.length} variant-klassen (s-*), moet er 1 zijn`);
  variants.push(v[0] || '?');
}
if (!variants.length) errors.push('geen <section class="slide ..."> gevonden');
for (let k = 2; k < variants.length; k++)
  if (variants[k] === variants[k - 1] && variants[k] === variants[k - 2])
    warns.push(`slides ${k - 1}-${k + 1}: drie keer achter elkaar ${variants[k]} — wissel licht/verzadigd af`);

// 3. Echte Npuls-fonts, geen stand-ins
if (/fonts\.googleapis\.com/.test(html)) errors.push('Google Fonts gevonden — gebruik de echte fonts uit public/npuls/Npuls_lettertype (zit in de frame)');
if (!/General Sans/.test(html)) errors.push("@font-face voor 'General Sans' ontbreekt — start vanuit assets/frame.html");

// 4. Geen achtergebleven placeholders
for (const m of html.matchAll(/\{\{[A-Z_]+\}\}/g)) errors.push(`regel ${lineOf(m.index)}: placeholder ${m[0]} niet ingevuld`);

// 5. Lokale bestanden bestaan (scripts en commentaar niet meetellen)
const markup = html.replace(/<script[\s\S]*?<\/script>|<!--[\s\S]*?-->/g, m => ' '.repeat(m.length));
for (const m of markup.matchAll(/(?:\ssrc=["']|url\(["']?)(?!https?:|data:|#)([^"')]+)/g)) {
  const p = resolve(base, decodeURI(m[1]));
  if (!existsSync(p)) errors.push(`regel ${lineOf(m.index)}: bestand bestaat niet: ${m[1]}`);
}

// 6. Minimaal 3 primaire Npuls-kleuren zichtbaar (buiten zwart/wit)
const body = html.slice(html.indexOf('<body'));
const prim = ['blauw', 'geel', 'roze', 'groen', 'oranje'].filter(c =>
  new RegExp(`\\bs-${c}\\b|\\b(card|ico|node)\\s+${c}\\b|--npuls-${c}`).test(body));
if (prim.length < 3) errors.push(`maar ${prim.length} primaire kleuren gebruikt (${prim.join(', ') || 'geen'}) — minimaal 3`);

// 7. Zwart is nooit een achtergrond (vormgever-npuls-huisstijl)
for (const m of body.matchAll(/background(?:-color)?\s*:\s*var\(--npuls-zwart\)|\bs-zwart\b|\bcard\s+zwart\b/g))
  errors.push(`zwarte achtergrond gevonden (${m[0]}) — zwart is alleen voor tekst; gebruik s-blauw voor een donker accent`);

// 8. Logo-jpg heeft een roze achtergrond: alleen op s-roze
for (const m of body.matchAll(/<section\s+class="([^"]*)"[\s\S]*?<\/section>/g))
  if (/npuls_logo\.jpg/.test(m[0]) && !/\bs-roze\b/.test(m[1]))
    errors.push(`npuls_logo.jpg staat op een ${m[1].match(/s-\w+/)?.[0]}-slide — het logo heeft een roze vlak, zet het op s-roze`);

for (const w of warns) console.log('WAARSCHUWING  ' + w);
for (const e of errors) console.log('FOUT          ' + e);
console.log(`\n${variants.length} slides · varianten: ${variants.join(' ')}`);
console.log(`primaire kleuren: ${prim.join(', ')}`);
console.log(errors.length ? `\n✗ ${errors.length} fout(en)` : '\n✓ huisstijlcheck geslaagd');
process.exit(errors.length ? 1 : 0);
