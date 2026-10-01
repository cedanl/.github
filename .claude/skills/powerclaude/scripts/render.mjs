#!/usr/bin/env node
// Rendert een .pptx naar PNG's (en optioneel PDF) om visueel te controleren.
//
//   node <skill>/scripts/render.mjs exports/<naam>/<naam>.pptx [--pdf]
//
// Windows: via PowerPoint (COM) — toont precies wat de ontvanger ziet.
// macOS/Linux of zonder PowerPoint: via LibreOffice (soffice) + pdftoppm.
// PNG's komen in exports/<naam>/qa/slide-NN.png.
import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync, renameSync, rmSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';

const file = process.argv[2];
const wantPdf = process.argv.includes('--pdf');
if (!file || !existsSync(file)) {
  console.error('Gebruik: node <skill>/scripts/render.mjs exports/<naam>/<naam>.pptx [--pdf]');
  process.exit(2);
}
const abs = resolve(file);
const qa = join(dirname(abs), 'qa');
rmSync(qa, { recursive: true, force: true });
mkdirSync(qa, { recursive: true });
const pdf = abs.replace(/\.pptx$/i, '.pdf');

function viaPowerPoint() {
  const ps = `
$ErrorActionPreference = 'Stop'
$pp = New-Object -ComObject PowerPoint.Application
$p = $pp.Presentations.Open('${abs}', $true, $false, $false)
$i = 1
foreach ($s in $p.Slides) { $s.Export(('${qa}\\slide-{0:D2}.png' -f $i), 'PNG', 1600, 900); $i++ }
${wantPdf ? `$p.SaveAs('${pdf}', 32)` : ''}
$p.Close()
`;
  const r = spawnSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', ps], { encoding: 'utf8' });
  return r.status === 0;
}

function viaLibreOffice() {
  const soffice = ['soffice', 'libreoffice', '/Applications/LibreOffice.app/Contents/MacOS/soffice']
    .find((b) => spawnSync(b, ['--version']).status === 0);
  if (!soffice) return false;
  execFileSync(soffice, ['--headless', '--convert-to', 'pdf', '--outdir', dirname(abs), abs], { stdio: 'ignore' });
  if (spawnSync('pdftoppm', ['-v']).error) {
    console.error('pdftoppm (poppler) ontbreekt: PDF staat klaar, PNG\'s niet.');
    return true;
  }
  execFileSync('pdftoppm', ['-png', '-scale-to-x', '1600', '-scale-to-y', '900', pdf, join(qa, 'slide')]);
  for (const f of readdirSync(qa)) {
    const m = f.match(/slide-0*(\d+)\.png/);
    if (m) renameSync(join(qa, f), join(qa, `slide-${m[1].padStart(2, '0')}.png`));
  }
  if (!wantPdf) rmSync(pdf, { force: true });
  return true;
}

const ok = (process.platform === 'win32' && viaPowerPoint()) || viaLibreOffice();
if (!ok) {
  console.error('FOUT  geen renderer: installeer PowerPoint (Windows) of LibreOffice + poppler.');
  process.exit(2);
}
const pngs = readdirSync(qa).filter((f) => f.endsWith('.png')).sort();
console.log(`OK  ${pngs.length} slides → ${qa}`);
if (wantPdf && existsSync(pdf)) console.log(`OK  PDF → ${pdf}`);
console.log(`Bekijk elke PNG met Read voordat je "klaar" meldt (${basename(abs)}).`);
