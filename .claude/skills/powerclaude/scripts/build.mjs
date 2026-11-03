#!/usr/bin/env node
// Bouwt een Npuls-PowerPoint uit een deck-spec.
//
// Gebruik (vanuit de clidev-presentaties projectroot):
//   node <skill>/scripts/build.mjs YYMMDD_onderwerp.deck.mjs [--engine potx|pptxgenjs]
//
// Engine potx (standaard): bouwt op de Npuls-template public/npuls/Npuls_powerpoint-template.potx
// via scripts/build_potx.py (python-pptx). Engine pptxgenjs: de eigen layouts uit lib/layouts.mjs.
// Schrijft exports/<naam>/<naam>.pptx. Exit 0 = gebouwd zonder fouten
// (waarschuwingen mogelijk), 1 = fouten in de spec, 2 = omgeving niet in orde.
import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { ILLU_DIR, beeldmerkDots, illustrationPath, projectRequire, rasterize } from './lib/assets.mjs';
import { Canvas, LAYOUTS, TEAM_IMAGE, TYPES } from './lib/layouts.mjs';
import { ALLOWED, C, CARD, CHART_ORDER, FONT, VARIANTS } from './lib/tokens.mjs';

const args = process.argv.slice(2);
const engineAt = args.indexOf('--engine');
const ENGINE = engineAt >= 0 ? args.splice(engineAt, 2)[1] : 'potx';
const TEMPLATE = 'public/npuls/Npuls_powerpoint-template.potx';
const specPath = args[0];
if (!['potx', 'pptxgenjs'].includes(ENGINE)) {
  console.error(`FOUT  onbekende engine "${ENGINE}": kies potx of pptxgenjs`);
  process.exit(2);
}
if (ENGINE === 'potx' && !existsSync(TEMPLATE)) {
  console.error(`FOUT  ${TEMPLATE} niet gevonden. Draai dit vanuit de root van clidev-presentaties (of gebruik --engine pptxgenjs).`);
  process.exit(2);
}
if (!specPath) {
  console.error('Gebruik: node <skill>/scripts/build.mjs YYMMDD_onderwerp.deck.mjs');
  process.exit(2);
}
if (!existsSync(ILLU_DIR)) {
  console.error(`FOUT  ${ILLU_DIR} niet gevonden. Draai dit vanuit de root van clidev-presentaties.`);
  process.exit(2);
}
let PptxGenJS;
if (ENGINE === 'pptxgenjs') {
  try {
    PptxGenJS = projectRequire('pptxgenjs');
  } catch {
    console.error('FOUT  pptxgenjs ontbreekt in dit project. Draai: npm install -D pptxgenjs');
    process.exit(2);
  }
}

const name = basename(specPath).replace(/\.deck\.mjs$/, '').replace(/\.mjs$/, '');
const deck = (await import(pathToFileURL(resolve(specPath)).href)).default;
const errors = [];
const warnings = [];
const err = (n, m) => errors.push(`slide ${n}: ${m}`);

// ---------- tokens in sync met vormgever-npuls-huisstijl ----------
const tokenFile = [
  resolve(import.meta.dirname, '../../vormgever-npuls-huisstijl/references/design-tokens.json'),
  join(homedir(), '.claude', 'skills', 'vormgever-npuls-huisstijl', 'references', 'design-tokens.json'),
  join(homedir(), '.agents', 'skills', 'vormgever-npuls-huisstijl', 'references', 'design-tokens.json'),
  join(homedir(), 'Projects', '.github', '.claude', 'skills', 'vormgever-npuls-huisstijl', 'references', 'design-tokens.json'),
].find((p) => existsSync(p));
if (tokenFile) {
  const t = JSON.parse(readFileSync(tokenFile, 'utf8')).colors;
  for (const [k, v] of Object.entries({ ...t.primary, ...t.secondary })) {
    const key = k.replace(/^npuls-/, '');
    if (C[key] && C[key].toUpperCase() !== v.replace('#', '').toUpperCase()) {
      errors.push(`tokens.mjs: ${key} is ${C[key]}, design-tokens.json zegt ${v} — werk tokens.mjs bij`);
    }
  }
}

// ---------- spec controleren ----------
if (!deck?.slides?.length) errors.push('deck.slides ontbreekt of is leeg');
const slides = deck?.slides ?? [];
const illus = new Set();
const used = new Set();
const SATURATED = ['blauw', 'roze', 'groen', 'oranje', 'geel'];
// Vaste CEDA-slides: inhoud ligt vast in layouts.mjs (woordelijk gelijk aan clidev).
const FIXED = {
  ceda: 'Vaste CEDA-introslide: wie CEDA is. Kort toelichten, daarna door naar de inhoud.',
  team: 'Dit is het CEDA-team. Noem kort twee projecten waar we aan werken.',
  contact: 'Vaste afsluitslide: laat deze staan tijdens de vragen, zodat iedereen de links ziet.',
};
const FIXED_FIELDS = { team: ['text'] }; // velden die een vaste slide wel mag hebben
const FIXED_VARIANT = { ceda: 'wit', team: 'licht-blauw', contact: 'roze' };

slides.forEach((s, i) => {
  const n = i + 1;
  if (!TYPES.includes(s.type)) return err(n, `onbekend type "${s.type}". Kies uit: ${TYPES.join(', ')}`);
  if (FIXED[s.type]) {
    const extra = Object.keys(s).filter((k) => !['type', 'notes', ...(FIXED_FIELDS[s.type] ?? [])].includes(k));
    if (extra.length) warnings.push(`slide ${n}: ${s.type} is een vaste slide; ${extra.join(', ')} wordt genegeerd`);
    if (s.type === 'team' && !existsSync(TEAM_IMAGE)) err(n, `teamfoto ${TEAM_IMAGE} niet gevonden`);
    s.variant = FIXED_VARIANT[s.type]; // voor de afwissel-check
    s.notes ??= FIXED[s.type];
    return;
  }
  // Op de template zijn inhoudsslides standaard wit (de witte master), net als in de Npuls-template.
  const contentDefault = ENGINE === 'potx' ? 'wit' : 'licht-geel';
  const variant = s.variant ?? (s.type === 'title' ? 'roze' : s.type === 'section' ? 'blauw' : s.type === 'closing' && ENGINE === 'potx' ? 'roze' : contentDefault);
  if (!VARIANTS[variant]) return err(n, `onbekende variant "${variant}". Kies uit: ${Object.keys(VARIANTS).join(', ')}`);
  s.variant = variant;
  used.add(VARIANTS[variant].bg);
  for (const c of VARIANTS[variant].cards) if (['cards', 'stats'].includes(s.type)) used.add(c);
  if (['stats', 'cards', 'list'].includes(s.type) && !s.items?.length && !(s.type === 'cards' && s.rows?.length)) err(n, `${s.type} heeft items (of bij cards rows) nodig`);
  if (s.type === 'timeline' && (!s.blocks?.length || s.blocks.some((b) => !(b.minutes > 0) || !b.title))) err(n, 'timeline heeft blocks nodig, elk met minutes en title');
  if (s.type === 'chart' && (!s.labels?.length || !s.series?.length)) err(n, 'chart heeft labels en series nodig');
  if (s.type === 'table' && (!s.columns?.length || !s.rows?.length)) err(n, 'table heeft columns en rows nodig');
  if (s.type === 'image' && (!s.image || !existsSync(s.image))) err(n, `afbeelding "${s.image}" niet gevonden`);
  if (s.type === 'video') {
    if (!s.video || !existsSync(s.video)) err(n, `video "${s.video}" niet gevonden`);
    else if (!/\.mp4$/i.test(s.video)) err(n, `video "${s.video}" moet een .mp4 zijn (PowerPoint speelt webm niet betrouwbaar af)`);
    if (s.poster && (!/\.png$/i.test(s.poster) || !existsSync(s.poster))) err(n, `poster "${s.poster}" niet gevonden of geen .png`);
  }
  if (s.type !== 'title' && !s.title && s.type !== 'quote') err(n, 'titel ontbreekt');
  if (variant === 'wit' && ENGINE !== 'potx') warnings.push(`slide ${n}: variant wit — Npuls is kleurrijk, kies liever een lichte variant`);
  if (i > 0 && SATURATED.includes(variant) && slides[i - 1].variant === variant && s.type !== 'closing') {
    warnings.push(`slide ${n}: twee keer achter elkaar ${variant} — wissel af`);
  }
  for (const it of [s, ...(s.items ?? []), ...(s.rows ?? []).flatMap((r) => r.items ?? [])]) {
    if (it.color && !C[it.color]) err(n, `onbekende kleur "${it.color}"`);
    if (it.illustration) {
      const p = illustrationPath(it.illustration);
      if (!existsSync(p)) err(n, `illustratie "${it.illustration}" bestaat niet in ${ILLU_DIR}`);
      else illus.add(it.illustration);
    }
  }
  if (!s.notes) warnings.push(`slide ${n}: geen sprekersnotities`);
  const words = JSON.stringify({ ...s, notes: undefined, variant: undefined, type: undefined }).replace(/"[a-zA-Z]+":/g, ' ').split(/\s+/).filter((w) => /[\p{L}\d]/u.test(w)).length;
  if (words > 90) warnings.push(`slide ${n}: ~${words} woorden zichtbaar — splitsen (richtlijn: max ~70)`);
});
if (slides[0] && slides[0].type !== 'title') warnings.push('eerste slide is geen title');
const cedaAt = slides.findIndex((s) => s.type === 'ceda');
if (cedaAt === -1) warnings.push("vaste CEDA-introslide ontbreekt: zet { type: 'ceda' } direct na de titel/agenda (alleen weglaten als de gebruiker dat vraagt)");
else if (cedaAt > 2) warnings.push(`CEDA-introslide staat op slide ${cedaAt + 1}: hoort direct na de titel/agenda`);
if (cedaAt >= 0 && slides[cedaAt + 1]?.type !== 'team') warnings.push("teamslide ontbreekt na de CEDA-introslide: zet { type: 'team' } direct na { type: 'ceda' } (alleen weglaten als de gebruiker dat vraagt)");
if (slides.length && slides.at(-1).type !== 'contact') warnings.push("laatste slide is niet de vaste afsluitslide: eindig met { type: 'contact' } (alleen weglaten als de gebruiker dat vraagt)");
for (const t of Object.keys(FIXED)) if (slides.filter((s) => s.type === t).length > 1) warnings.push(`${t} staat meer dan één keer in het deck`);
if (ENGINE === 'potx') for (const c of ['oranje', 'roze']) used.add(c); // de template zelf toont oranje bogen en roze vlakken
const primaries = [...used].filter((c) => SATURATED.includes(c));
if (primaries.length < 3) warnings.push(`maar ${primaries.length} primaire kleuren zichtbaar (${primaries.join(', ')}) — Npuls vraagt er minstens 3`);
if (illus.size < 2) warnings.push(`${illus.size} Npuls-illustratie(s) in het deck — gebruik er minstens 2`);

if (errors.length) {
  errors.forEach((e) => console.error(`FOUT  ${e}`));
  process.exit(1);
}

// ---------- bouwen ----------
const outDir = join('exports', name);
mkdirSync(outDir, { recursive: true });
const illu = await rasterize([...illus].map(illustrationPath), join(outDir, 'img'));
const illuByName = new Map([...illus].map((k) => [k, illu.get(illustrationPath(k))]));
// Video zonder poster: het beeld op `posterAt` seconden (standaard 1) wordt het stilstaande beeld.
for (const [i, s] of slides.entries()) {
  if (s.type !== 'video' || s.poster) continue;
  s.poster = join(outDir, 'img', `poster-${i + 1}.png`);
  mkdirSync(dirname(s.poster), { recursive: true });
  try {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', String(s.posterAt ?? 1), '-i', s.video, '-frames:v', '1', s.poster]);
  } catch {
    console.error(`FOUT  slide ${i + 1}: geen poster uit "${s.video}" (ffmpeg ontbreekt of faalt). Installeer ffmpeg of geef poster: 'pad.png' mee`);
    process.exit(2);
  }
}

if (ENGINE === 'potx') {
  const payload = {
    name, title: deck.title ?? name, author: deck.author ?? 'CEDA', einddia: deck.einddia ?? true,
    template: resolve(TEMPLATE), out: resolve(join(outDir, `${name}.pptx`)),
    slides, illu: Object.fromEntries([...illuByName].map(([k, v]) => [k, resolve(v)])),
    tokens: { C, VARIANTS, CARD, CHART_ORDER, FONT, ALLOWED },
  };
  const pf = join(tmpdir(), `powerclaude-${name}.json`); // tijdelijk: alleen voor build_potx.py
  writeFileSync(pf, JSON.stringify(payload, null, 1));
  const py = process.platform === 'win32' ? 'python' : 'python3';
  const r = spawnSync(py, [join(import.meta.dirname, 'build_potx.py'), pf], { encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
  if (r.error || r.status !== 0) {
    console.error(r.stdout ?? '', r.stderr ?? r.error?.message ?? '');
    if (/No module named 'pptx'/.test(r.stderr ?? '')) console.error('FOUT  python-pptx ontbreekt: pip install python-pptx');
    process.exit(r.status === 1 ? 1 : 2);
  }
  warnings.forEach((w) => console.warn(`WAARSCHUWING  ${w}`));
  process.stdout.write(r.stdout);
  process.exit(0);
}

const dots = beeldmerkDots();
if (!dots) warnings.push('beeldmerk niet gevonden (vormgever-npuls-huisstijl/assets/logos) — slides zonder beeldmerk');

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.title = deck.title ?? name;
pptx.author = deck.author ?? 'CEDA';
pptx.company = deck.company ?? 'Npuls · CEDA';
pptx.theme = { headFontFace: 'General Sans Semibold', bodyFontFace: 'General Sans' };

slides.forEach((s, i) => {
  const slide = pptx.addSlide();
  slide.background = { color: C[VARIANTS[s.variant].bg] };
  const ctx = { warn: (m) => warnings.push(`slide ${i + 1}: ${m}`), illu: illuByName, dots };
  LAYOUTS[s.type](new Canvas(pptx, slide, s.variant, ctx), s);
  if (s.notes) slide.addNotes(s.notes);
});

const file = join(outDir, `${name}.pptx`);
await pptx.writeFile({ fileName: file });
warnings.forEach((w) => console.warn(`WAARSCHUWING  ${w}`));
console.log(`OK  ${file} — ${slides.length} slides, ${warnings.length} waarschuwing(en)`);
