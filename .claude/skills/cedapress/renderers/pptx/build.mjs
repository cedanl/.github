#!/usr/bin/env node
// Bouwt een Npuls-PowerPoint uit een deck-spec.
//
// Gebruik (vanuit de root van de presentatierepo, daar staan node_modules):
//   node <cedapress>/renderers/pptx/build.mjs decks/YYMMDD_onderwerp/YYMMDD_onderwerp.deck.mjs [--engine potx|pptxgenjs]
//
// Engine potx (standaard): bouwt op pptx/Npuls_powerpoint-template.potx uit het Npuls-assetpakket
// (versie in cedapress/assets.lock) via build_potx.py (python-pptx). Engine pptxgenjs: de eigen layouts uit lib/layouts.mjs.
// Schrijft <deckmap>/exports/<naam>.pptx. Exit 0 = gebouwd zonder fouten
// (waarschuwingen mogelijk), 1 = fouten in de spec, 2 = omgeving niet in orde.
import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { bronHash, bronNaast } from '../lib/bron.mjs';
import { ILLU_DIR, NPULS, beeldmerkDots, illustrationPath, projectRequire, rasterize } from './lib/assets.mjs';
import { Canvas, LAYOUTS, TYPES, setTeamImage } from './lib/layouts.mjs';
import { ALLOWED, BADGE_FG, C, CARD, CHART_ORDER, FONT, ICON_FG, TILE_ON, VARIANTS } from './lib/tokens.mjs';

const args = process.argv.slice(2);
const engineAt = args.indexOf('--engine');
const ENGINE = engineAt >= 0 ? args.splice(engineAt, 2)[1] : 'potx';
const TEMPLATE = NPULS.template;
const specPath = args[0];
if (!['potx', 'pptxgenjs'].includes(ENGINE)) {
  console.error(`FOUT  onbekende engine "${ENGINE}": kies potx of pptxgenjs`);
  process.exit(2);
}
if (ENGINE === 'potx' && !existsSync(TEMPLATE)) {
  console.error(`FOUT  ${TEMPLATE} niet gevonden in het Npuls-assetpakket (of gebruik --engine pptxgenjs).`);
  process.exit(2);
}
if (!specPath) {
  console.error('Gebruik: node <cedapress>/renderers/pptx/build.mjs decks/YYMMDD_onderwerp/YYMMDD_onderwerp.deck.mjs');
  process.exit(2);
}
if (!existsSync(ILLU_DIR)) {
  console.error(`FOUT  ${ILLU_DIR} niet gevonden in het Npuls-assetpakket.`);
  process.exit(2);
}
let PptxGenJS;
if (ENGINE === 'pptxgenjs') {
  try {
    PptxGenJS = projectRequire('pptxgenjs');
  } catch {
    console.error('FOUT  pptxgenjs ontbreekt. Eenmalig: npm install --prefix <cedapress>/renderers');
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
  resolve(import.meta.dirname, '../../../vormgever-npuls-huisstijl/references/design-tokens.json'),
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

// CEDA-teamfoto: env CEDA_TEAMFOTO, anders ceda/teamfoto.png in het pakket, anders img/team-groep.png in de deckmap
const TEAM_IMAGE = NPULS.teamfoto || join(dirname(resolve(specPath)), 'img', 'team-groep.png');
setTeamImage(TEAM_IMAGE);

// ---------- bron-markdown is de single source of truth ----------
const bron = bronNaast(resolve(specPath));
if (!bron) errors.push('bron.md ontbreekt naast de deck-spec — elk deck heeft een bron-markdown (verplicht)');
else if (deck?.bron !== bronHash(bron)) errors.push(`deck-spec loopt achter op bron.md (spec bron: ${deck?.bron ?? 'leeg'}, bron.md: ${bronHash(bron)}) — werk de spec bij uit de bron en zet bron: '${bronHash(bron)}'`);

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

// Typen die alleen de potx-engine kent (componenten uit Edwins ceda-powerpoint-maker, zie references/pptx-slidetypes.md).
const POTX_TYPES = ['steps', 'lead', 'hero', 'insight', 'lists'];
const ALL_TYPES = [...TYPES, ...POTX_TYPES];
// Velden zonder zichtbare tekst: tellen niet mee voor het aantal woorden (OPP-02).
const NON_TEXT = new Set(['type', 'variant', 'color', 'colors', 'illustration', 'icon', 'image', 'video', 'poster', 'alt', 'link', 'notes', 'format', 'chart', 'side', 'style', 'tile']);
const zichtbaar = (v, key = '') => (NON_TEXT.has(key) ? [] : typeof v === 'string' ? v.split(/\s+/).filter((w) => /[\p{L}\d]/u.test(w)) : Array.isArray(v) ? v.flatMap((x) => zichtbaar(x)) : v && typeof v === 'object' ? Object.entries(v).flatMap(([k, x]) => zichtbaar(x, k)) : []);
const iconen = new Set();
const noteOf = (s) => (typeof s.note === 'string' ? { text: s.note } : s.note);

slides.forEach((s, i) => {
  const n = i + 1;
  if (!ALL_TYPES.includes(s.type)) return err(n, `onbekend type "${s.type}". Kies uit: ${ALL_TYPES.join(', ')}`);
  if (POTX_TYPES.includes(s.type) && ENGINE !== 'potx') return err(n, `type "${s.type}" bestaat alleen in de potx-engine`);
  if (FIXED[s.type]) {
    const extra = Object.keys(s).filter((k) => !['type', 'notes', ...(FIXED_FIELDS[s.type] ?? [])].includes(k));
    if (extra.length) warnings.push(`slide ${n}: ${s.type} is een vaste slide; ${extra.join(', ')} wordt genegeerd`);
    if (s.type === 'team' && !existsSync(TEAM_IMAGE)) err(n, `teamfoto ${TEAM_IMAGE} niet gevonden — zet CEDA_TEAMFOTO of leg img/team-groep.png in de deckmap`);
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
  if (['stats', 'cards', 'list', 'steps', 'lead'].includes(s.type) && !s.items?.length && !s.figures?.length && !(s.type === 'cards' && s.rows?.length) && !(s.type === 'lead' && s.lead)) err(n, `${s.type} heeft items (of bij cards rows) nodig`);
  if (s.type === 'insight' && !s.rows?.length) err(n, 'insight heeft rows nodig: [{ icon, key, text, tag }]');
  if (s.type === 'lists' && !s.groups?.length) err(n, 'lists heeft groups nodig: [{ title, icon, items, style }]');
  if (s.type === 'hero' && !s.text) err(n, 'hero heeft text nodig');
  // OPP-19: aantallen per patroon
  const aantal = (what, k, lo, hi) => { if (k < lo || k > hi) warnings.push(`slide ${n}: ${k} ${what}, richtlijn ${lo} tot ${hi} [OPP-19]`); };
  if (s.type === 'cards' && s.items) aantal('kaarten', s.items.length, 2, 4);
  if (s.type === 'steps') aantal('stappen', s.items?.length ?? 0, 3, 4);
  if (s.type === 'insight') aantal('rijen', s.rows?.length ?? 0, 3, 5);
  if (s.type === 'lists') { aantal('lijstkaarten', s.groups?.length ?? 0, 2, 3); for (const g of s.groups ?? []) aantal(`items in "${g.title}"`, g.items?.length ?? 0, 3, 5); }
  if (s.label && s.label.trim().split(/\s+/).length > 3) warnings.push(`slide ${n}: label "${s.label}" heeft meer dan 3 woorden [OPP-18]`);
  if (!['title', 'section', 'closing', 'quote', 'hero'].includes(s.type) && s.title && s.title.replace(/\*\*/g, '').length > 45) warnings.push(`slide ${n}: titel van ${s.title.replace(/\*\*/g, '').length} tekens, richtlijn max 45 [OPP-17]`);
  if (s.title && ['cards', 'steps', 'lead', 'insight', 'lists', 'stats', 'hero'].includes(s.type) && s.label && !s.title.includes('**')) warnings.push(`slide ${n}: titel zonder **accentdeel** [OPP-17]`);
  const iconHere = [...(s.items ?? []), ...(s.rows ?? []).flatMap((r) => [r, ...(r.items ?? [])]), ...(s.groups ?? []), noteOf(s)].filter(Boolean);
  for (const it of iconHere) if (it.icon) iconen.add(it.icon);
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
  // OPP-02: richtlijn max 50 woorden zichtbaar per inhoudsslide, waarschuwing boven 60
  const words = ['title', 'section', 'quote', 'closing'].includes(s.type) ? 0 : zichtbaar(s).length;
  if (words > 60) warnings.push(`slide ${n}: ${words} woorden zichtbaar [OPP-02] — splitsen of naar de notes (richtlijn max 50)`);
});
if (slides[0] && slides[0].type !== 'title') warnings.push('eerste slide is geen title');
// Vaste CEDA-slides zijn optioneel (bron.md: vaste-slides: ja | nee). Zijn ze er, dan als één blok ceda → team → contact aan het eind.
const vasteTypes = Object.keys(FIXED);
const vasteAt = slides.map((s, i) => (vasteTypes.includes(s.type) ? i : -1)).filter((i) => i >= 0);
const wens = (bron ? readFileSync(bron, 'utf8') : '').match(/^vaste-slides:\s*(ja|nee)/mi)?.[1]?.toLowerCase();
if (wens === 'ja' && !vasteAt.length) warnings.push("bron.md zegt vaste-slides: ja, maar de spec heeft geen { type: 'ceda' }, 'team' en 'contact'");
if (wens === 'nee' && vasteAt.length) warnings.push('bron.md zegt vaste-slides: nee, maar de spec heeft vaste CEDA-slides — haal ze weg of zet vaste-slides: ja');
if (vasteAt.length) {
  const types = vasteAt.map((i) => slides[i].type);
  if (vasteTypes.some((t) => !types.includes(t))) warnings.push(`vaste CEDA-slides horen als blok bij elkaar: ${vasteTypes.filter((t) => !types.includes(t)).join(', ')} ontbreekt`);
  const contiguous = vasteAt.every((v, k) => k === 0 || v === vasteAt[k - 1] + 1);
  const tail = slides.length - 1 - vasteAt.at(-1); // slides ná het blok (alleen closing mag, de einddia komt automatisch)
  if (!contiguous || tail > 0) warnings.push('vaste CEDA-slides (ceda, team, contact) horen als één blok aan het eind, vóór de afsluiter');
}
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
const outDir = join(dirname(resolve(specPath)), 'exports');
mkdirSync(outDir, { recursive: true });
// Iconen komen uit het assetpakket (iconen/<naam>.svg). Zit er (nog) geen iconenset in, dan toont de icoontegel een lege tegel en volgt een waarschuwing.
const ICON_DIR = join(NPULS.root, 'iconen');
const iconPaths = new Map([...iconen].filter((k) => existsSync(join(ICON_DIR, `${k}.svg`))).map((k) => [k, join(ICON_DIR, `${k}.svg`)]));
const iconPng = iconPaths.size ? await rasterize([...iconPaths.values()], join(outDir, 'img'), 256) : new Map();
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
    name, bron: deck.bron, title: deck.title ?? name, author: deck.author ?? 'CEDA', einddia: deck.einddia ?? true,
    template: resolve(TEMPLATE), out: resolve(join(outDir, `${name}.pptx`)),
    slides, illu: Object.fromEntries([...illuByName].map(([k, v]) => [k, resolve(v)])),
    icons: Object.fromEntries([...iconPaths].map(([k, v]) => [k, resolve(iconPng.get(v))])), iconsAsked: [...iconen],
    tokens: { C, VARIANTS, CARD, CHART_ORDER, FONT, ALLOWED, ICON_FG, TILE_ON, BADGE_FG }, teamfoto: resolve(TEAM_IMAGE),
  };
  const pf = join(tmpdir(), `cedapress-${name}.json`); // tijdelijk: alleen voor build_potx.py
  writeFileSync(pf, JSON.stringify(payload, null, 1));
  const py = process.platform === 'win32' ? 'python' : 'python3';
  const r = spawnSync(py, [join(import.meta.dirname, 'build_potx.py'), pf], { encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
  if (r.error || r.status !== 0) {
    console.error(r.stdout ?? '', r.stderr ?? r.error?.message ?? '');
    if (/No module named 'pptx'/.test(r.stderr ?? '')) console.error('FOUT  python-pptx ontbreekt: pip install python-pptx');
    process.exit(r.status === 1 ? 1 : 2);
  }
  warnings.forEach((w) => console.warn(`WAARSCHUWING  ${w}`));
  // Samenvatting telt alle waarschuwingen: die van build.mjs en die van build_potx.py
  const pyWarn = (r.stdout.match(/^WAARSCHUWING /gm) ?? []).length;
  process.stdout.write(r.stdout.replace(/(\d+) waarschuwing\(en\)/, `${pyWarn + warnings.length} waarschuwing(en)`));
  process.exit(0);
}

const dots = beeldmerkDots();
if (!dots) warnings.push('beeldmerk niet gevonden (logos/beeldmerk-ring.json in het assetpakket) — slides zonder beeldmerk');

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

