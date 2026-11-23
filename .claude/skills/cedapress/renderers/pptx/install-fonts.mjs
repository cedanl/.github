#!/usr/bin/env node
// Installeert de Npuls-fonts (General Sans, General Sans Semibold, Cooper Lt BT)
// voor de huidige gebruiker, zonder beheerrechten. Zonder deze fonts toont
// PowerPoint de slides in Calibri en kloppen de tekstmaten niet.
//
//   NPULS_FONTS_DIR=<map met de fontbestanden uit de Npuls-communicatiekit> node <cedapress>/renderers/pptx/install-fonts.mjs
//   (het assetpakket bevat geen fonts vanwege de licenties, zie fonts.md in het pakket)
//   node <cedapress>/renderers/pptx/install-fonts.mjs --check  (alleen controleren)
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { npulsPaths } from '../lib/npuls-assets.mjs';

const SRC = npulsPaths().fonts;
const FILES = {
  'Npuls_lettertype_generalsans_regular.otf': 'General Sans (OpenType)',
  'Npuls_lettertype_generalsans_semibold.otf': 'General Sans Semibold (OpenType)',
  'Npuls_lettertype_cooper_light_bt.ttf': 'Cooper Lt BT (TrueType)',
};
const CHECK_ONLY = process.argv.includes('--check');
if (!CHECK_ONLY && (!SRC || !existsSync(SRC))) {
  console.error('FOUT  zet NPULS_FONTS_DIR op de map met de Npuls-fonts (communicatiekit); het assetpakket bevat ze niet.');
  process.exit(2);
}

const dest = {
  win32: join(process.env.LOCALAPPDATA ?? '', 'Microsoft', 'Windows', 'Fonts'),
  darwin: join(homedir(), 'Library', 'Fonts'),
}[process.platform] ?? join(homedir(), '.local', 'share', 'fonts');

const missing = Object.keys(FILES).filter((f) => !existsSync(join(dest, f)));
if (process.argv.includes('--check')) {
  if (missing.length) { console.log(`ONTBREEKT  ${missing.join(', ')}`); process.exit(1); }
  console.log('OK  Npuls-fonts geïnstalleerd'); process.exit(0);
}

mkdirSync(dest, { recursive: true });
for (const f of missing) {
  copyFileSync(join(SRC, f), join(dest, f));
  if (process.platform === 'win32') {
    spawnSync('reg', ['add', 'HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts', '/v', FILES[f], '/t', 'REG_SZ', '/d', join(dest, f), '/f'], { stdio: 'ignore' });
  }
  console.log(`geïnstalleerd  ${f}`);
}
if (process.platform === 'linux') spawnSync('fc-cache', ['-f'], { stdio: 'ignore' });
console.log(missing.length ? 'OK  herstart PowerPoint om de fonts te zien' : 'OK  fonts stonden er al');
