#!/usr/bin/env node
// Visuele QA voor een clanna-deck: screenshot per slide op 1920×1080 én 1366×768,
// plus automatische detectie van overflow, ontbrekende fonts/afbeeldingen en
// tekst die over decoratie valt. Optioneel PDF-export.
//
// Gebruik (vanuit de projectroot, daar staat playwright-chromium):
//   node <skill>/scripts/qa.mjs YYMMDD_onderwerp.html [--pdf] [--out exports/<naam>/qa]
// Exit 1 als er fouten zijn.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, basename, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const file = args.find(a => !a.startsWith('--'));
if (!file) { console.error('Gebruik: node qa.mjs <deck.html> [--pdf] [--out dir]'); process.exit(2); }
const name = basename(file, '.html');
const outIdx = args.indexOf('--out');
const out = resolve(outIdx > -1 ? args[outIdx + 1] : join('exports', name, 'qa'));
mkdirSync(out, { recursive: true });

// playwright uit de projectroot laden, niet uit de skill-map
const require = createRequire(join(process.cwd(), 'package.json'));
let chromium;
try { ({ chromium } = require('playwright-chromium')); }
catch { console.error('playwright-chromium niet gevonden. Draai vanuit de projectroot: npm install'); process.exit(2); }

const url = pathToFileURL(resolve(file)).href;
const viewports = [{ w: 1920, h: 1080 }, { w: 1366, h: 768 }];
const browser = await chromium.launch();
const report = { deck: file, errors: [], warnings: [], shots: [] };

for (const vp of viewports) {
  const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  if (vp.w === 1920) {
    // welk font rendert de browser écht (CDP), niet wat de CSS vraagt
    const cdp = await page.context().newCDPSession(page);
    await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
    const { root } = await cdp.send('DOM.getDocument', { depth: -1, pierce: false });
    const rendered = async sel => {
      const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: sel });
      if (!nodeId) return null;
      const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId });
      return fonts.map(f => f.familyName).join(', ');
    };
    const head = await rendered('h1') ?? await rendered('h2');
    const serif = await rendered('.lede') ?? await rendered('.pull');
    if (head !== null && !/General Sans/i.test(head)) report.errors.push(`koppen renderen in "${head}", niet in General Sans (pad naar public/npuls/Npuls_lettertype klopt niet?)`);
    if (serif !== null && !/Cooper/i.test(serif)) report.errors.push(`.lede/.pull rendert in "${serif}", niet in Cooper Light BT`);
    await cdp.detach();
  }

  const count = await page.evaluate(() => document.querySelectorAll('.slide').length);
  await page.keyboard.press('Home');
  for (let n = 1; n <= count; n++) {
    if (n > 1) await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(650); // slide-transitie + balk-animatie
    const shot = join(out, `${String(n).padStart(2, '0')}_${vp.w}x${vp.h}.png`);
    await page.screenshot({ path: shot });
    report.shots.push(shot);

    const found = await page.evaluate(() => {
      const slide = document.querySelector('.slide.active');
      const navTop = document.querySelector('.nav').getBoundingClientRect().top;
      const W = innerWidth, H = innerHeight, res = { err: [], warn: [] };
      const label = el => {
        const t = (el.innerText || el.alt || '').trim().replace(/\s+/g, ' ').slice(0, 50);
        return `<${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : ''}> "${t}"`;
      };
      const content = [...slide.querySelectorAll('*')].filter(el =>
        !el.closest('.deco') && !el.closest('svg') && el.getClientRects().length &&
        getComputedStyle(el).visibility !== 'hidden');
      // leaf-ish: elementen met eigen tekst, afbeeldingen, kaarten
      const leaves = content.filter(el =>
        el.tagName === 'IMG' || el.matches('.card,.step,.node,.chip,.menti-frame,table,.bars') ||
        [...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()));
      for (const el of leaves) {
        const r = el.getBoundingClientRect();
        if (r.bottom > navTop + 2) res.err.push(`loopt onder de navigatiebalk (${Math.round(r.bottom - navTop)}px): ${label(el)}`);
        else if (r.right > W + 1 || r.left < -1) res.err.push(`valt buiten beeld horizontaal: ${label(el)}`);
      }
      // afgekapte tekst in containers met overflow:hidden (ellipsis bewust uitgezonderd)
      for (const el of content) {
        const cs = getComputedStyle(el);
        if (cs.overflow === 'hidden' && cs.textOverflow !== 'ellipsis' && !el.matches('.bar-track,.menti-frame') &&
            el.scrollHeight > el.clientHeight + 4 && el.innerText.trim())
          res.err.push(`inhoud afgekapt (${el.scrollHeight - el.clientHeight}px): ${label(el)}`);
      }
      // kapotte afbeeldingen
      for (const img of slide.querySelectorAll('img'))
        if (!img.complete || img.naturalWidth === 0) res.err.push(`afbeelding laadt niet: ${img.getAttribute('src')}`);
      // tekst over decoratie: hit-test van de geverfde vorm (niet de bounding box)
      // onder elke tekstregel die direct op de slide-achtergrond staat
      const opaque = el => {
        for (let a = el; a && a !== slide; a = a.parentElement) {
          const bg = getComputedStyle(a).backgroundColor;
          if (bg && bg !== 'transparent' && !/rgba\(.*,\s*0\)$/.test(bg)) return true;
        }
        return false;
      };
      const st = document.createElement('style');
      st.textContent = '.deco,.deco *{pointer-events:visiblePainted!important}';
      document.head.appendChild(st);
      const texts = content.filter(el => el.matches('h1,h2,h3,p,li,.kicker,.lede,.pull') && !opaque(el));
      for (const el of texts) {
        const range = document.createRange(); range.selectNodeContents(el);
        let hits = 0, total = 0;
        for (const r of range.getClientRects()) {
          for (let k = 1; k <= 12; k++) for (const fy of [0.3, 0.7]) {
            total++;
            const x = r.left + (r.width * k) / 13, y = r.top + r.height * fy;
            if (document.elementsFromPoint(x, y).some(e => e.tagName.toLowerCase() !== 'svg' && e.closest && e.closest('.deco'))) hits++;
          }
        }
        if (total && hits / total > 0.03)
          res.warn.push(`tekst ligt over decoratie (${Math.round((100 * hits) / total)}% van de regels) — verplaats de deco of de tekst: ${label(el)}`);
      }
      st.remove();
      return res;
    });
    const tag = `slide ${n} @${vp.w}x${vp.h}`;
    for (const e of [...new Set(found.err)]) report.errors.push(`${tag}: ${e}`);
    for (const w of [...new Set(found.warn)]) report.warnings.push(`${tag}: ${w}`);
  }

  if (vp.w === 1920 && args.includes('--pdf')) {
    await page.emulateMedia({ media: 'print' });
    const pdf = resolve(join(out, '..', `${name}.pdf`));
    await page.pdf({ path: pdf, width: '1920px', height: '1080px', printBackground: true });
    report.pdf = pdf;
  }
  await page.close();
}
await browser.close();

writeFileSync(join(out, 'report.json'), JSON.stringify(report, null, 2));
for (const w of report.warnings) console.log('WAARSCHUWING  ' + w);
for (const e of report.errors) console.log('FOUT          ' + e);
console.log(`\nscreenshots: ${out} (${report.shots.length})`);
if (report.pdf) console.log(`pdf: ${report.pdf}`);
console.log(report.errors.length ? `✗ ${report.errors.length} fout(en)` : '✓ geen overflow, fonts en afbeeldingen ok');
process.exit(report.errors.length ? 1 : 0);
