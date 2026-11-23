#!/usr/bin/env node
// Statische check voor een cedapress-HTML-deck: huisstijl (overgenomen uit clanna), bron-hash en ontwerpregels
// (ids uit ontwerper-slides-html/references/regels.md).
// Gebruik: node <cedapress>/renderers/html/check.mjs presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html [--stempel]
//   --stempel  zet eerst de hash van de huidige bron.md in de HTML. Alleen doen nadat de HTML met de bron is bijgewerkt.
// Exit 1 bij fouten, 0 als alleen waarschuwingen of niets.
import { readFileSync, existsSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { bronHash, bronNaast } from '../lib/bron.mjs';

const file = process.argv.slice(2).find((a) => !a.startsWith('--'));
if (!file) { console.error('Gebruik: node check.mjs <deck.html> [--stempel]'); process.exit(2); }
const bron = bronNaast(file);
if (process.argv.includes('--stempel') && bron) {
  const h = bronHash(bron);
  const src = readFileSync(file, 'utf8');
  const out = /<meta name="cedapress-bron"[^>]*>/.test(src)
    ? src.replace(/<meta name="cedapress-bron"[^>]*>/, `<meta name="cedapress-bron" content="${h}">`)
    : src.replace(/<head>/, `<head>
<meta name="cedapress-bron" content="${h}">`);
  writeFileSync(file, out);
  console.log(`gestempeld: ${h}`);
}
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

// 2. Elke slide precies één variant (s-deel = lichte kleur van het deel, vereist data-deel)
const variants = [];
for (const m of html.matchAll(/<section\b[^>]*\bclass="([^"]*\bslide\b[^"]*)"[^>]*>/g)) {
  const v = m[1].split(/\s+/).filter(c => /^s-/.test(c));
  if (v.length !== 1) errors.push(`regel ${lineOf(m.index)}: slide heeft ${v.length} variant-klassen (s-*), moet er 1 zijn`);
  if (v[0] === 's-deel' && !/\bdata-deel="[^"]+"/.test(m[0])) errors.push(`regel ${lineOf(m.index)}: s-deel zonder data-deel="…" — geef het deel een naam`);
  variants.push(v[0] || '?');
}
if (!variants.length) errors.push('geen <section class="slide ..."> gevonden');
const delen = new Set([...html.matchAll(/<section\b[^>]*\bdata-deel="([^"]+)"/g)].map(m => m[1]));
if (delen.size === 1) warns.push(`maar één deel (${[...delen][0]}) — delen zijn bedoeld voor 3 à 5 hoofdstukken`);
if (delen.size > 5) warns.push(`${delen.size} delen — de navigatie past er maximaal 5 netjes`);
for (let k = 2; k < variants.length; k++)
  if (variants[k] !== 's-deel' && variants[k] === variants[k - 1] && variants[k] === variants[k - 2])
    warns.push(`slides ${k - 1}-${k + 1}: drie keer achter elkaar ${variants[k]} — wissel licht/verzadigd af`);

// 3. Echte Npuls-fonts, geen stand-ins
if (/fonts\.googleapis\.com/.test(html)) errors.push('Google Fonts gevonden — de echte fonts komen uit het assetpakket (npuls/web/npuls.css, zit in de frame)');
if (!/General Sans/.test(html)) errors.push("'General Sans' ontbreekt — start vanuit renderers/html/frame.html");
if (!/<link[^>]+href=["']npuls\/web\/npuls\.css["']/.test(html)) errors.push('link naar npuls/web/npuls.css ontbreekt — start vanuit renderers/html/frame.html');
if (/public\/npuls\//.test(html)) errors.push('pad public/npuls/ gevonden — assets komen uit het pakket via npuls/ (prepare.mjs)');

// 4. Geen achtergebleven placeholders
for (const m of html.matchAll(/\{\{[A-Z_]+\}\}/g)) errors.push(`regel ${lineOf(m.index)}: placeholder ${m[0]} niet ingevuld`);

// 5. Lokale bestanden bestaan (scripts en commentaar niet meetellen)
const markup = html.replace(/<script[\s\S]*?<\/script>|<!--[\s\S]*?-->/g, m => ' '.repeat(m.length));
if (!existsSync(resolve(base, 'npuls'))) errors.push('map npuls/ naast het deck ontbreekt — draai renderers/html/prepare.mjs <deckmap>');
for (const m of markup.matchAll(/(?:\ssrc=["']|url\(["']?|<link[^>]+href=["'])(?!https?:|data:|#|mailto:)([^"')]+)/g)) {
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
  if (/npuls_logo\.jpg|npuls-logo-roze\.jpg/.test(m[0]) && !/\bs-roze\b/.test(m[1]))
    errors.push(`npuls-logo-roze.jpg staat op een ${m[1].match(/s-\w+/)?.[0]}-slide — het logo heeft een roze vlak, zet het op s-roze`);

// 9. Vaste CEDA-slides (gelijk in HTML en pptx)
for (const [t, naam] of [['Wie is CEDA', '"Wie is CEDA"'], ['Wie zijn wij', '"Wie zijn wij"'], ['Blijf in contact', '"Blijf in contact"']])
  if (!body.includes(t)) warns.push(`vaste CEDA-slide ${naam} ontbreekt — alleen weglaten als de gebruiker dat expliciet vroeg`);

// 10. Bron-markdown is de single source of truth: HTML moet de hash van de huidige bron.md dragen
const meta = html.match(/<meta name="cedapress-bron" content="([^"]*)"/);
if (!bron) errors.push('bron.md ontbreekt naast het deck — elk deck heeft een bron-markdown (verplicht)');
else if (!meta || !/^sha256:/.test(meta[1])) errors.push('meta cedapress-bron ontbreekt — HTML is niet uit bron.md gegenereerd (prepare.mjs, of --stempel na bijwerken)');
else if (meta[1] !== bronHash(bron)) errors.push(`HTML loopt achter op bron.md (HTML ${meta[1]}, bron ${bronHash(bron)}) — werk de HTML bij uit de bron en draai check met --stempel`);

// 11. Ontwerpregels (ontwerper-slides-html/references/regels.md). TODO(Edwin): drempels vaststellen.
const sections = [...body.matchAll(/<section([^>]*)>([\s\S]*?)<\/section>/g)];
const zichtbaar = (h) => h.replace(/<!--[\s\S]*?-->|<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<svg[\s\S]*?<\/svg>/g, ' ')
  .replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;|&#\d+;/g, ' ');
const vast = /Wie is CEDA|Wie zijn wij|Blijf in contact|lay-eind/;
sections.forEach(([all, attrs, inner], k) => {
  const n = k + 1;
  if (vast.test(all)) return;
  const woorden = zichtbaar(inner).split(/\s+/).filter((w) => /[\p{L}\d]/u.test(w)).length;
  if (woorden > 90) errors.push(`slide ${n}: ${woorden} woorden zichtbaar [OSH-02] — splitsen`);
  else if (woorden > 60) warns.push(`slide ${n}: ${woorden} woorden zichtbaar [OSH-02] — richtlijn max 60`);
  const h2 = (inner.match(/<h2/g) || []).length;
  if (h2 > 1) errors.push(`slide ${n}: ${h2} koppen (h2) [OSH-01] — één boodschap per slide`);
  const kop = inner.match(/<h[12][^>]*>([\s\S]*?)<\/h[12]>/);
  if (kop) { const kw = zichtbaar(kop[1]).split(/\s+/).filter(Boolean).length; if (kw > 12) warns.push(`slide ${n}: kop van ${kw} woorden [OSH-03] — max 12`); }
  for (const ul of inner.matchAll(/<(ul|ol)[^>]*>([\s\S]*?)<\/>/g)) {
    const li = (ul[2].match(/<li/g) || []).length;
    if (li > 5) warns.push(`slide ${n}: lijst met ${li} punten [OSH-04] — max 5`);
  }
  for (const img of inner.matchAll(/<img[^>]*>/g)) if (!/alt=/.test(img[0])) errors.push(`slide ${n}: afbeelding zonder alt [OSH-06] — alt="" voor decoratie`);
});
const fancy = html.match(/<meta name="cedapress-fancy" content="([ABC])"/)?.[1];
if (!fancy) warns.push('meta cedapress-fancy (A, B of C) ontbreekt [OSH-10]');
else {
  const anim = (body.match(/data-(a|count|draw|pop|grow)/g) || []).length;
  const illus = (body.match(/npuls\/illustraties\//g) || []).length;
  const bogen = (body.match(/class="deco bogen"/g) || []).length;
  if (fancy === 'A' && anim) errors.push(`fancy A (sober) met ${anim} extra animatie(s) data-* [OSH-10]`);
  if (fancy !== 'A' && bogen < 2) warns.push(`fancy ${fancy}: bogen rechtsonder op ${bogen} slide(s) [OSH-11] — huisstijl+ vraagt ze terugkerend`);
  if (fancy === 'C' && illus < 3) warns.push(`fancy C (rijk) met ${illus} illustratie(s) [OSH-12] — minstens 3`);
}

for (const w of warns) console.log('WAARSCHUWING  ' + w);
for (const e of errors) console.log('FOUT          ' + e);
console.log(`\n${variants.length} slides · varianten: ${variants.join(' ')}`);
if (delen.size) console.log(`delen: ${[...delen].join(' · ')}`);
console.log(`primaire kleuren: ${prim.join(', ')}`);
console.log(errors.length ? `\n✗ ${errors.length} fout(en)` : '\n✓ huisstijlcheck geslaagd');
process.exit(errors.length ? 1 : 0);
