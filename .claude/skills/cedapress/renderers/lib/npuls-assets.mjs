// Npuls-assetpakket vinden voor cedapress (HTML- en pptx-renderer).
//
// Eén bron: het versioned assetpakket van vormgever-npuls-huisstijl. De versie staat op één plek:
// cedapress/assets.lock. Volgorde:
//   1. env NPULS_ASSETS_DIR (override, bv. een lokale checkout van het pakket)
//   2. python <vormgever>/scripts/npuls_assets.py ensure --version <lock>  → laatste regel stdout = cachepad
// Nooit meer assets uit de presentatierepo of uit de skillmap van vormgever-npuls-huisstijl.
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
export const SKILL_DIR = resolve(HERE, '..', '..');

export function lockedVersion() {
  const lock = readFileSync(join(SKILL_DIR, 'assets.lock'), 'utf8');
  const m = lock.match(/^npuls-assets\s*==\s*([0-9][\w.+-]*)\s*$/m);
  if (!m) throw new Error(`assets.lock: geen regel "npuls-assets==<versie>" in ${join(SKILL_DIR, 'assets.lock')}`);
  return m[1];
}

function helperScript() {
  const rel = ['vormgever-npuls-huisstijl', 'scripts', 'npuls_assets.py'];
  return [
    resolve(SKILL_DIR, '..', ...rel),
    join(homedir(), '.claude', 'skills', ...rel),
    join(homedir(), '.agents', 'skills', ...rel),
    join(homedir(), 'Projects', '.github', '.claude', 'skills', ...rel),
  ].find((p) => existsSync(p));
}

let cached;
/** Absoluut pad naar de root van het assetpakket (bevat manifest.json, pptx/, logos/, ...). */
export function npulsAssetsDir() {
  if (cached) return cached;
  const env = process.env.NPULS_ASSETS_DIR;
  if (env) {
    if (!existsSync(env)) throw new Error(`NPULS_ASSETS_DIR=${env} bestaat niet`);
    return (cached = resolve(env));
  }
  const version = lockedVersion();
  const helper = helperScript();
  if (!helper) throw new Error('vormgever-npuls-huisstijl/scripts/npuls_assets.py niet gevonden — installeer vormgever-npuls-huisstijl of zet NPULS_ASSETS_DIR');
  const py = process.platform === 'win32' ? 'python' : 'python3';
  const r = spawnSync(py, [helper, 'ensure', '--version', version], { encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
  if (r.error || r.status !== 0) throw new Error(`npuls_assets.py ensure --version ${version} faalde:\n${r.stderr || r.error?.message || ''}`);
  const dir = r.stdout.trim().split(/\r?\n/).pop().trim();
  if (!existsSync(dir)) throw new Error(`npuls_assets.py gaf "${dir}", maar dat pad bestaat niet`);
  return (cached = resolve(dir));
}

/** Vaste paden in het pakket (0.1.0). Fonts en de CEDA-teamfoto zitten er bewust niet in: zie fonts en teamfoto. */
export function npulsPaths(root = npulsAssetsDir()) {
  return {
    root,
    manifest: join(root, 'manifest.json'),
    template: join(root, 'pptx', 'Npuls_powerpoint-template.potx'),
    logos: join(root, 'logos'),
    logoJpg: join(root, 'logos', 'npuls-logo-roze.jpg'),
    vormen: join(root, 'vormen'),
    illustraties: join(root, 'illustraties'),   // illustratie-NN.svg (26, uit de potx)
    slidesPreview: join(root, 'slides-preview'), // slideNN.png, zelfde volgorde als de oude SlideN.PNG
    css: join(root, 'web', 'npuls.css'),
    sprite: join(root, 'web', 'sprite.svg'),
    // Fonts zitten niet in het pakket (licenties, zie fonts.md): web via CDN in npuls.css, voor PowerPoint
    // lokaal uit de Npuls-communicatiekit. Map met de .otf/.ttf: env NPULS_FONTS_DIR.
    fonts: process.env.NPULS_FONTS_DIR || '',
    // CEDA-teamfoto ("Wie zijn wij") is geen Npuls-asset. TODO(Aslam): vaste plek kiezen (CEDA-assets/huisstijlplus).
    // Nu: env CEDA_TEAMFOTO, anders img/team-groep.png in de deckmap.
    teamfoto: process.env.CEDA_TEAMFOTO || '',
  };
}
