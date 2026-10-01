// Slidetypes voor powerclaude. Elke functie tekent één slide uit een spec-object.
// Maten in inches op 13.333 × 7.5 (16:9). Alle kleuren via tokens.mjs.
import { ALLOWED, C, CARD, CHART_ORDER, FONT, GRIJS, VARIANTS, hex } from './tokens.mjs';
import { imageSize } from './assets.mjs';

export const W = 13.333;
export const H = 7.5;
const M = 0.6; // buitenmarge
const CW = W - 2 * M; // contentbreedte

// ---------- tekst ----------

// Gemiddelde tekenbreedte in em per font; bewust iets ruim, zodat een
// terugval naar een ander font ook nog past.
const EM = { [FONT.body]: 0.53, [FONT.head]: 0.56, [FONT.quote]: 0.5 };

// `**vet**` → kopfont in de accentkleur. Geeft pptxgenjs-runs terug.
function runs(text, base, accent) {
  const out = [];
  String(text).split('\n').forEach((line, li, lines) => {
    const parts = line.split(/\*\*(.+?)\*\*/g);
    parts.forEach((p, i) => {
      if (!p) return;
      const strong = i % 2 === 1;
      out.push({ text: p, options: strong ? { fontFace: FONT.head, color: accent ?? base.color } : {} });
    });
    if (li < lines.length - 1) {
      if (out.length) out[out.length - 1].options.breakLine = true;
      else out.push({ text: '', options: { breakLine: true } });
    }
  });
  return out.length ? out : [{ text: '', options: {} }];
}

function plain(text) {
  return String(text).replace(/\*\*(.+?)\*\*/g, '$1');
}

// Geschatte hoogte (inches) van tekst op een gegeven breedte en grootte.
export function textHeight(text, { w, size, font = FONT.body, line = 1.18 }) {
  const charsPerLine = Math.max(1, Math.floor((w * 72) / (size * (EM[font] ?? 0.53))));
  const lines = plain(text).split('\n').reduce((n, p) => n + Math.max(1, Math.ceil((p.length * 1.06) / charsPerLine)), 0);
  return (lines * size * line) / 72;
}

// Schat de benodigde hoogte en verklein het font tot `min` als het niet past.
export function fit(text, { w, h, size, font = FONT.body, min, line = 1.18 }) {
  const floor = min ?? Math.max(10, Math.round(size * 0.75));
  for (let s = size; s >= floor; s--) {
    if (textHeight(text, { w, size: s, font, line }) <= h) return { size: s, ok: true };
  }
  return { size: floor, ok: false };
}

export class Canvas {
  constructor(pptx, slide, variant, ctx) {
    this.pptx = pptx;
    this.slide = slide;
    this.v = VARIANTS[variant];
    this.variant = variant;
    this.ctx = ctx; // { warn, n, illu: Map, dots }
  }

  text(text, o) {
    if (text == null || text === '') return;
    const font = o.font ?? FONT.body;
    const r = fit(text, { w: o.w, h: o.h, size: o.size, font, min: o.min });
    if (!r.ok) this.ctx.warn(`tekst past niet (${o.w.toFixed(1)}×${o.h.toFixed(1)} in, ${r.size}pt): "${plain(text).slice(0, 50)}…" → inkorten of splitsen`);
    const color = hex(o.color);
    this.slide.addText(runs(text, { color }, o.accent ? hex(o.accent) : undefined), {
      x: o.x, y: o.y, w: o.w, h: o.h,
      fontFace: font, fontSize: r.size, color,
      align: o.align ?? 'left', valign: o.valign ?? 'top',
      margin: 0, italic: o.italic ?? false, bold: false,
      charSpacing: o.spacing, lineSpacingMultiple: o.line ?? 1.05,
      paraSpaceAfter: o.paraSpace ?? 0,
    });
  }

  label(text, o) {
    // Kleine kapitalen-labels zoals "WAT JE DOET".
    this.text(String(text).toUpperCase(), { ...o, font: FONT.head, size: o.size ?? 11, spacing: 3, min: 8 });
  }

  box(o) {
    const radius = o.r ?? 0.28;
    this.slide.addShape(radius ? this.pptx.ShapeType.roundRect : this.pptx.ShapeType.rect, {
      x: o.x, y: o.y, w: o.w, h: o.h,
      fill: { color: hex(o.fill) },
      line: { type: 'none' },
      rectRadius: radius ? Math.min(radius / Math.min(o.w, o.h), 0.5) : undefined,
    });
  }

  pill(text, o) {
    this.box({ x: o.x, y: o.y, w: o.w, h: o.h, fill: o.fill, r: o.h / 2 });
    this.text(text, { x: o.x + 0.1, y: o.y, w: o.w - 0.2, h: o.h, size: o.size ?? 13, color: o.color, font: FONT.head, align: 'center', valign: 'middle', min: 8 });
  }

  circle(o) {
    this.slide.addShape(this.pptx.ShapeType.ellipse, {
      x: o.x, y: o.y, w: o.d, h: o.d,
      fill: o.fill ? { color: hex(o.fill) } : { type: 'none' },
      line: o.stroke ? { color: hex(o.stroke), width: o.width ?? 3 } : { type: 'none' },
    });
  }

  badge(text, o) {
    this.circle({ x: o.x, y: o.y, d: o.d, fill: o.fill });
    this.text(text, { x: o.x, y: o.y, w: o.d, h: o.d, size: o.size ?? Math.round(o.d * 34), color: o.color, font: FONT.head, align: 'center', valign: 'middle', min: 10 });
  }

  // Beeldmerk rechtsboven (of op een eigen plek), getekend als vector-stippen.
  mark(o = {}) {
    const dots = this.ctx.dots;
    if (!dots) return;
    const s = o.size ?? 0.7;
    const x0 = o.x ?? W - M - s;
    const y0 = o.y ?? 0.42;
    const color = hex(o.color ?? this.v.mark);
    for (const d of dots) {
      this.slide.addShape(this.pptx.ShapeType.ellipse, {
        x: x0 + (d.cx - d.r) * s, y: y0 + (d.cy - d.r) * s, w: 2 * d.r * s, h: 2 * d.r * s,
        fill: { color }, line: { type: 'none' },
      });
    }
  }

  title(text, o = {}) {
    this.text(text, { x: M, y: o.y ?? 0.45, w: o.w ?? CW - 1.1, h: o.h ?? 0.85, size: o.size ?? 34, color: o.color ?? this.v.title, font: FONT.head, valign: 'middle', min: 24 });
  }

  illustration(name, o) {
    const png = this.ctx.illu.get(name);
    if (!png) return this.ctx.warn(`illustratie "${name}" niet gevonden`);
    const s = Math.min(o.w, o.h);
    this.slide.addImage({ path: png, x: o.x + (o.w - s) / 2, y: o.y + (o.h - s) / 2, w: s, h: s, altText: o.alt ?? '' });
  }

  // Decoratie in vector: golven (pulse curve), ringen, starburst of chevrons.
  deco(kind, o) {
    const [c1, c2 = c1] = (o.colors ?? this.v.deco).map(hex);
    const S = this.pptx.ShapeType;
    if (kind === 'golven') {
      const wave = (dy, color) => this.slide.addShape(S.custGeom, {
        x: o.x, y: o.y + dy, w: o.w, h: o.h * 0.7,
        line: { color, width: o.width ?? 9 }, fill: { type: 'none' },
        points: [
          { x: 0, y: o.h * 0.6 },
          { x: o.w * 0.5, y: o.h * 0.45, curve: { type: 'cubic', x1: o.w * 0.15, y1: o.h * -0.1, x2: o.w * 0.3, y2: o.h * 0.1 } },
          { x: o.w, y: 0.02, curve: { type: 'cubic', x1: o.w * 0.7, y1: o.h * 0.8, x2: o.w * 0.85, y2: o.h * 0.5 } },
        ],
      });
      wave(0, c1);
      wave(o.h * 0.3, c2);
    } else if (kind === 'ringen') {
      const d = Math.min(o.w, o.h);
      [1, 0.78, 0.56, 0.34].forEach((f, i) => this.circle({ x: o.x + (d - d * f) / 2, y: o.y + (d - d * f) / 2, d: d * f, stroke: i % 2 ? (o.colors?.[1] ?? this.v.deco[1] ?? this.v.deco[0]) : (o.colors?.[0] ?? this.v.deco[0]), width: 4.5 }));
      this.circle({ x: o.x + d * 0.43, y: o.y + d * 0.43, d: d * 0.14, fill: o.colors?.[0] ?? this.v.deco[0] });
    } else if (kind === 'starburst') {
      const d = Math.min(o.w, o.h);
      const cx = o.x + d / 2, cy = o.y + d / 2;
      for (let k = 0; k < 8; k++) {
        const a = (k * Math.PI) / 4;
        const r1 = d * 0.22, r2 = d * 0.5;
        const x1 = cx + r1 * Math.cos(a), y1 = cy + r1 * Math.sin(a);
        const x2 = cx + r2 * Math.cos(a), y2 = cy + r2 * Math.sin(a);
        this.slide.addShape(S.line, {
          x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
          flipH: (x2 - x1) * (y2 - y1) < 0, line: { color: c1, width: 6, lineCap: 'round' },
        });
      }
      this.slide.addShape(S.ellipse, { x: cx - d * 0.12, y: cy - d * 0.12, w: d * 0.24, h: d * 0.24, fill: { color: c2 }, line: { type: 'none' } });
    } else if (kind === 'chevrons') {
      for (let k = 0; k < 3; k++) this.slide.addShape(S.chevron, { x: o.x + k * o.h * 0.75, y: o.y, w: o.h * 0.6, h: o.h, fill: { color: k % 2 ? c2 : c1 }, line: { type: 'none' } });
    }
  }

  // Tekst/vlak op een verzadigde achtergrond moet in allowed_combinations staan.
  // Op lichte (secondary) achtergronden mag elk verzadigd vlak.
  checkPair(bg, fg, where) {
    const light = bg === 'wit' || bg.startsWith('licht-');
    if (fg === bg || (!light && !ALLOWED[bg]?.includes(fg))) this.ctx.warn(`${fg} op ${bg} (${where}) is geen toegestane Npuls-combinatie`);
  }
}

function cardColors(cv, items) {
  return items.map((it, i) => it.color ?? cv.v.cards[i % cv.v.cards.length]);
}

function footer(cv, s, y) {
  if (s.footer) cv.text(s.footer, { x: M, y, w: CW, h: 0.5, size: 18, color: cv.v.text, accent: cv.v.accent, min: 12 });
  if (s.footnote) cv.text(s.footnote, { x: M, y: H - 0.62, w: CW, h: 0.3, size: 11, color: cv.v.bg === 'blauw' ? 'roze' : cv.v.title, min: 9 });
}

// ---------- slidetypes ----------

export const LAYOUTS = {
  // Openingsslide: kicker-pill, grote titel, lede in Cooper, rechts agenda of illustratie.
  title(cv, s) {
    const v = cv.v;
    cv.mark({ x: M, y: 0.5, size: 0.8 });
    if (s.kicker) cv.pill(s.kicker, { x: 1.65, y: 0.68, w: Math.min(4.6, 0.6 + s.kicker.length * 0.12), h: 0.44, fill: v.accent, color: CARD[v.accent].big, size: 13 });
    const right = s.agenda?.length || s.illustration;
    const tw = right ? 7.4 : CW;
    cv.text(s.title, { x: M, y: 1.85, w: tw, h: 2.0, size: 46, color: v.title, font: FONT.head, valign: 'bottom', min: 32 });
    cv.text(s.lede, { x: M, y: 4.0, w: tw, h: 0.6, size: 22, color: v.quote, font: FONT.quote, min: 16 });
    cv.text(s.sub, { x: M, y: 4.7, w: tw, h: 0.45, size: 16, color: v.text, min: 12 });
    if (s.agenda?.length) {
      const n = Math.min(s.agenda.length, 4);
      const gap = n > 3 ? 1.35 : 1.7;
      const y0 = 1.3;
      const cols = [...new Set([v.accent, ...v.cards])];
      for (let i = 0; i < n; i++) {
        const y = y0 + i * gap;
        if (i < n - 1) cv.slide.addShape(cv.pptx.ShapeType.line, { x: 9.4, y: y + 1.0, w: 0, h: gap - 1.0, line: { color: hex(v.text), width: 1.5, dashType: 'dash' } });
        const fill = cols[i % cols.length];
        cv.badge(String(i + 1), { x: 8.9, y, d: 1.0, fill, color: CARD[fill].big, size: 28 });
        cv.text(s.agenda[i], { x: 10.2, y, w: 2.55, h: 1.0, size: 20, color: v.title, font: FONT.head, valign: 'middle', min: 13 });
      }
    } else if (s.illustration) {
      cv.illustration(s.illustration, { x: 8.4, y: 1.2, w: 4.3, h: 4.3 });
    }
    if (s.deco !== false) cv.deco('golven', { x: M, y: 5.75, w: 4.4, h: 1.5 });
    if (s.tagline) cv.text(s.tagline, { x: 8.7, y: 6.72, w: 4.0, h: 0.4, size: 14, color: v.accent, font: FONT.head, align: 'right' });
  },

  // Sectie of kernboodschap: één grote bewering, optioneel nummer en toelichting.
  section(cv, s) {
    const v = cv.v;
    cv.mark();
    if (s.number) cv.badge(String(s.number), { x: M, y: 1.4, d: 1.1, fill: v.accent, color: CARD[v.accent].big, size: 32 });
    cv.text(s.title, { x: M, y: 2.7, w: 8.6, h: 2.0, size: 48, color: v.title, font: FONT.head, valign: 'bottom', min: 32 });
    cv.text(s.text, { x: M, y: 4.95, w: 8.2, h: 1.4, size: 22, color: v.quote, font: FONT.quote, min: 15 });
    if (s.illustration) cv.illustration(s.illustration, { x: 9.3, y: 2.0, w: 3.6, h: 3.6 });
    else if (s.deco !== false) cv.deco(s.deco ?? 'ringen', { x: 9.6, y: 2.3, w: 3.0, h: 3.0 });
    footer(cv, { footnote: s.footnote }, 0);
  },

  // Kerncijfers: 2-4 gekleurde tegels met cijfer, label en uitleg.
  stats(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    let y = 1.45;
    if (s.lede) {
      const lh = Math.min(0.95, textHeight(s.lede, { w: 11.2, size: 21, font: FONT.quote }) + 0.05);
      cv.text(s.lede, { x: M, y, w: 11.2, h: lh, size: 21, color: v.quote, font: FONT.quote, min: 15 });
      y += lh + 0.35;
    }
    const items = s.items.slice(0, 4);
    const cols = cardColors(cv, items);
    const gap = 0.24;
    const cw = (CW - gap * (items.length - 1)) / items.length;
    const maxH = s.callout ? (s.lede ? 2.7 : 3.4) : (s.lede ? 3.4 : 4.4);
    const textH = Math.max(...items.map((it) => (it.text ? textHeight(it.text, { w: cw - 0.6, size: 14 }) : 0)));
    const ch = Math.min(maxH, Math.max(2.6, 2.05 + textH + 0.25));
    items.forEach((it, i) => {
      const x = M + i * (cw + gap);
      const c = cols[i];
      const r = CARD[c];
      cv.checkPair(v.bg, c, 'kaart');
      cv.box({ x, y, w: cw, h: ch, fill: c });
      cv.text(String(it.value), { x: x + 0.3, y: y + 0.25, w: cw - 0.6, h: 1.1, size: 64, color: r.big, font: FONT.head, valign: 'middle', min: 36 });
      cv.text(it.label, { x: x + 0.3, y: y + 1.4, w: cw - 0.6, h: 0.45, size: 19, color: r.title, font: FONT.head, min: 13 });
      cv.text(it.text, { x: x + 0.3, y: y + 1.85, w: cw - 0.6, h: ch - 2.0, size: 14, color: r.text, min: 10 });
    });
    y += ch + 0.3;
    if (s.callout) {
      cv.box({ x: M, y, w: CW, h: 0.85, fill: 'wit', r: 0.2 });
      cv.text(s.callout, { x: M + 0.35, y, w: CW - 0.7, h: 0.85, size: 16, color: 'zwart', accent: 'blauw', valign: 'middle', min: 11 });
    }
    footer(cv, { footnote: s.footnote }, 0);
  },

  // Kaarten in kolommen (2-4): badge, pill, kop, ondertitel, gelabelde secties.
  // `arrows: true` zet chevrons tussen de kaarten (proces/stappen).
  cards(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const items = s.items.slice(0, 4);
    const cols = cardColors(cv, items);
    const gap = s.arrows ? 0.5 : 0.3;
    const cw = (CW - gap * (items.length - 1)) / items.length;
    const y = 1.5;
    // Rijen (kop, titel, secties) krijgen over alle kaarten dezelfde hoogte,
    // zodat labels naast elkaar uitlijnen; de kaart is zo hoog als de inhoud.
    const iw = cw - 0.6;
    const ts = items.length > 3 ? 20 : 24;
    const headH = items.some((it) => it.badge || s.numbered || it.tag) ? 0.85 : 0;
    const titleH = Math.max(0.4, ...items.map((it) => textHeight(it.title, { w: iw, size: ts, font: FONT.head }))) + 0.12;
    const subH = items.some((it) => it.sub) ? 0.5 : 0;
    const secsOf = (it) => it.sections ?? (it.text ? [{ text: it.text }] : []);
    const nSec = Math.max(...items.map((it) => secsOf(it).length));
    let secH = Array.from({ length: nSec }, (_, k) => Math.max(...items.map((it) => {
      const sec = secsOf(it)[k];
      if (!sec) return 0;
      return (sec.label ? 0.38 : 0) + textHeight(sec.text, { w: iw, size: 15, font: sec.strong ? FONT.head : FONT.body }) + 0.25;
    })));
    const maxH = s.footer ? 4.55 : 5.05;
    const fixed = 0.3 + headH + titleH + subH + 0.15;
    const natural = fixed + secH.reduce((a, b) => a + b, 0);
    if (natural > maxH) secH = secH.map((h) => h * (maxH - fixed) / (natural - fixed));
    const ch = Math.min(maxH, Math.max(2.8, natural));
    items.forEach((it, i) => {
      const x = M + i * (cw + gap);
      const c = cols[i];
      const r = CARD[c];
      cv.checkPair(v.bg, c, 'kaart');
      cv.box({ x, y, w: cw, h: ch, fill: c });
      let iy = y + 0.3;
      const badge = it.badge ?? (s.numbered ? String(i + 1) : null);
      if (badge) cv.badge(badge, { x: x + 0.3, y: iy, d: 0.6, fill: r.pillBg, color: r.pillFg, size: 20 });
      if (it.tag) cv.pill(it.tag, { x: x + (badge ? 1.05 : 0.3), y: iy + 0.08, w: cw - (badge ? 1.35 : 0.6), h: 0.44, fill: r.pillBg, color: r.pillFg, size: 12 });
      iy += headH;
      if (it.illustration) { cv.illustration(it.illustration, { x: x + cw - 1.3, y: y + 0.2, w: 1.1, h: 1.1 }); }
      cv.text(it.title, { x: x + 0.3, y: iy, w: iw, h: titleH - 0.15, size: ts, color: r.title, font: FONT.head, min: 14 });
      iy += titleH;
      if (it.sub) cv.text(it.sub, { x: x + 0.3, y: iy, w: iw, h: 0.4, size: 14, color: r.text, font: FONT.quote, min: 10 });
      iy += subH + 0.15;
      secsOf(it).forEach((sec, k) => {
        let sy = iy;
        if (sec.label) { cv.label(sec.label, { x: x + 0.3, y: sy, w: iw, h: 0.3, color: r.label }); sy += 0.38; }
        cv.text(sec.text, { x: x + 0.3, y: sy, w: iw, h: secH[k] - (sy - iy) - 0.15, size: 15, color: r.text, font: sec.strong ? FONT.head : FONT.body, min: 10 });
        iy += secH[k];
      });
      if (s.arrows && i < items.length - 1) {
        cv.slide.addShape(cv.pptx.ShapeType.chevron, { x: x + cw + 0.12, y: y + ch / 2 - 0.3, w: 0.26, h: 0.6, fill: { color: hex(v.title) }, line: { type: 'none' } });
      }
    });
    footer(cv, s, y + ch + 0.2);
  },

  // Tekst naast een Npuls-illustratie.
  split(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const left = s.side === 'left';
    const tx = left ? 6.2 : M;
    const ix = left ? M : 8.2;
    const tw = 6.9 - (left ? 0.3 : 0);
    let y = 1.6;
    if (s.lede) {
      const lh = Math.min(1.2, textHeight(s.lede, { w: tw, size: 22, font: FONT.quote }) + 0.05);
      cv.text(s.lede, { x: tx, y, w: tw, h: lh, size: 22, color: v.quote, font: FONT.quote, min: 15 });
      y += lh + 0.4;
    }
    if (s.bullets?.length) {
      const per = Math.min(1.0, (6.6 - y) / s.bullets.length);
      s.bullets.forEach((b, i) => {
        const by = y + i * per;
        const fill = v.cards[i % v.cards.length];
        cv.circle({ x: tx, y: by + 0.12, d: 0.22, fill });
        cv.text(b, { x: tx + 0.45, y: by, w: tw - 0.45, h: per - 0.12, size: 19, color: v.text, accent: v.accent, min: 12 });
      });
    } else if (s.text) {
      cv.text(s.text, { x: tx, y, w: tw, h: 6.6 - y, size: 19, color: v.text, accent: v.accent, min: 12, paraSpace: 8 });
    }
    if (s.illustration) cv.illustration(s.illustration, { x: ix, y: 1.4, w: 4.6, h: 4.9, alt: s.alt });
    footer(cv, { footnote: s.footnote }, 0);
  },

  // Rijen met kop, toelichting en statuspill (planning, open punten, randvoorwaarden).
  list(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const rows = s.items.slice(0, 7);
    const y0 = 1.55;
    const avail = (s.footer ? 5.0 : 5.5);
    const rh = Math.min(0.95, avail / rows.length - 0.1);
    const card = v.bg === 'blauw' ? 'roze' : 'wit';
    if (card === 'wit' && !v.bg.startsWith('licht') && v.bg !== 'roze') cv.ctx.warn(`list op ${v.bg}: kies een lichte variant of roze`);
    rows.forEach((it, i) => {
      const y = y0 + i * (rh + 0.1);
      cv.box({ x: M, y, w: CW, h: rh, fill: card, r: 0.14 });
      cv.text(it.title, { x: M + 0.3, y: y + 0.06, w: 4.2, h: rh - 0.12, size: 16, color: 'zwart', font: FONT.head, valign: 'middle', min: 10 });
      cv.text(it.text, { x: M + 4.6, y: y + 0.06, w: it.status ? 5.0 : 7.3, h: rh - 0.12, size: 14, color: 'zwart', valign: 'middle', min: 9 });
      if (it.status) {
        const sc = it.color ?? 'blauw';
        const fg = CARD[sc]?.text === 'zwart' ? 'zwart' : (sc === 'blauw' ? 'roze' : CARD[sc]?.text ?? 'zwart');
        cv.pill(it.status, { x: M + CW - 1.95, y: y + rh / 2 - 0.18, w: 1.7, h: 0.36, fill: sc, color: fg, size: 11 });
      }
    });
    footer(cv, s, y0 + rows.length * (rh + 0.1) + 0.15);
  },

  // Tabel in Npuls-stijl: blauwe kopregel, afwisselend wit en licht.
  table(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const head = s.columns.map((c) => ({ text: c, options: { bold: false, fontFace: FONT.head, color: hex('roze'), fill: { color: hex('blauw') } } }));
    const body = s.rows.map((r, i) => r.map((cell) => ({ text: String(cell), options: { fill: { color: hex(i % 2 ? (v.bg === 'wit' ? 'licht-blauw' : 'wit') : (v.bg === 'wit' ? 'wit' : 'licht-roze')) }, color: hex('zwart') } })));
    const fs = s.rows.length > 8 ? 12 : 14;
    cv.slide.addTable([head, ...body], {
      x: M, y: 1.55, w: CW, colW: s.widths ? s.widths.map((f) => f * CW) : undefined,
      fontFace: FONT.body, fontSize: fs, margin: [5, 8, 5, 8], valign: 'middle',
      border: { type: 'solid', pt: 0.75, color: hex(v.bg === 'blauw' ? 'blauw' : 'roze') },
      autoPage: false,
    });
    if (s.rows.length > 10) cv.ctx.warn('tabel met meer dan 10 rijen: splitsen of samenvatten');
    footer(cv, s, 6.5);
  },

  // Native PowerPoint-grafiek (bewerkbaar) in de Npuls-volgorde, met optionele conclusie rechts.
  chart(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const P = cv.pptx;
    const kind = { bar: P.ChartType.bar, line: P.ChartType.line, pie: P.ChartType.pie, doughnut: P.ChartType.doughnut }[s.chart ?? 'bar'];
    const data = s.series.map((se) => ({ name: se.name, labels: s.labels, values: se.values }));
    const side = s.takeaway ? 4.0 : 0;
    const panel = v.bg.startsWith('licht') || v.bg === 'wit' ? null : 'wit';
    const x = M, y = 1.5, w = CW - side - (side ? 0.3 : 0), h = 5.0;
    if (panel) cv.box({ x, y, w, h, fill: panel, r: 0.2 });
    const axis = hex('zwart');
    const colors = (s.colors ?? (s.chart === 'pie' || s.chart === 'doughnut' ? CHART_ORDER : CHART_ORDER.slice(0, s.series.length))).map(hex);
    cv.slide.addChart(kind, data, {
      x: x + 0.2, y: y + 0.2, w: w - 0.4, h: h - 0.4,
      barDir: s.horizontal ? 'bar' : 'col', barGrouping: s.stacked ? 'stacked' : 'clustered',
      chartColors: colors, lineSize: 3, lineDataSymbolSize: 8,
      catAxisLabelFontFace: FONT.body, valAxisLabelFontFace: FONT.body, catAxisLabelColor: axis, valAxisLabelColor: axis,
      catAxisLabelFontSize: 13, valAxisLabelFontSize: 12,
      valGridLine: { color: 'DDDDDD', size: 0.75 }, catGridLine: { style: 'none' },
      showLegend: s.series.length > 1 || s.chart === 'pie' || s.chart === 'doughnut', legendPos: 'b', legendFontFace: FONT.body, legendFontSize: 13, legendColor: axis,
      showValue: s.values ?? true, dataLabelFontFace: FONT.head, dataLabelFontSize: 12, dataLabelColor: axis,
      dataLabelFormatCode: s.format ?? '#,##0', valAxisLabelFormatCode: s.format ?? '#,##0',
      showTitle: false,
    });
    if (s.takeaway) {
      const tx = M + CW - side;
      const th = Math.min(h, 1.2 + textHeight(s.takeaway, { w: side - 0.6, size: 20, font: FONT.head }));
      cv.box({ x: tx, y, w: side, h: th, fill: v.cards[0] });
      const r = CARD[v.cards[0]];
      cv.label(s.takeawayLabel ?? 'Wat valt op', { x: tx + 0.3, y: y + 0.35, w: side - 0.6, h: 0.3, color: r.label });
      cv.text(s.takeaway, { x: tx + 0.3, y: y + 0.8, w: side - 0.6, h: th - 1.0, size: 20, color: r.title, font: FONT.head, min: 13 });
      if (s.illustration) cv.illustration(s.illustration, { x: tx + 0.4, y: y + th + 0.2, w: side - 0.8, h: h - th - 0.2 });
    }
    footer(cv, { footnote: s.footnote ?? (s.source ? `Bron: ${s.source}` : undefined) }, 0);
  },

  // Citaat in Cooper Light.
  quote(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.text('“', { x: M, y: 0.6, w: 1.5, h: 2.1, size: 120, color: v.accent, font: FONT.quote });
    cv.text(s.text, { x: 1.4, y: 1.9, w: s.illustration ? 7.4 : 10.4, h: 3.4, size: 36, color: v.quote === 'zwart' ? v.title : v.quote, font: FONT.quote, min: 22 });
    cv.text(s.by, { x: 1.4, y: 5.5, w: 7.5, h: 0.5, size: 18, color: v.text, font: FONT.head });
    if (s.illustration) cv.illustration(s.illustration, { x: 9.2, y: 1.7, w: 3.5, h: 3.5 });
  },

  // Schermafbeelding of foto, passend geschaald, met onderschrift.
  image(cv, s) {
    const v = cv.v;
    cv.mark();
    cv.title(s.title);
    const side = s.text ? 4.1 : 0;
    const box = { x: M, y: 1.5, w: CW - side - (side ? 0.3 : 0), h: s.caption ? 4.75 : 5.2 };
    const { w: iw, h: ih } = imageSize(s.image);
    const scale = Math.min(box.w / iw, box.h / ih);
    const w = iw * scale, h = ih * scale;
    cv.slide.addImage({ path: s.image, x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w, h, altText: s.alt ?? s.caption ?? '' });
    if (s.caption) cv.text(s.caption, { x: M, y: box.y + box.h + 0.15, w: box.w, h: 0.4, size: 13, color: v.text, align: 'center', min: 10 });
    if (s.text) {
      const tx = M + CW - side;
      cv.text(s.text, { x: tx, y: 1.6, w: side, h: 4.9, size: 18, color: v.text, accent: v.accent, min: 12, paraSpace: 8 });
    }
    footer(cv, { footnote: s.footnote }, 0);
  },

  // Vaste CEDA-introslide ("Wie is CEDA"), woordelijk gelijk aan clidev/_template.md.
  // Direct na de titel/agenda; bewust zonder links (die staan op `contact`).
  ceda(cv) {
    cv.slide.background = { path: 'public/npuls/powerpoint_slides/Slide16.PNG' };
    const w = W / 2 - M - 0.5;
    cv.label('Wie is CEDA', { x: M + 0.2, y: 1.75, w, h: 0.35, color: 'oranje', size: 13 });
    cv.text('Centre of Educational Data Analytics', { x: M + 0.2, y: 2.15, w, h: 1.3, size: 32, color: 'blauw', font: FONT.head, min: 24 });
    cv.text('Eén team binnen Npuls. Van ruwe data tot AI-toepassing, open source.', { x: M + 0.2, y: 3.5, w, h: 0.9, size: 18, color: 'zwart', font: FONT.quote, min: 14 });
    ['Data, analytics en generatieve AI in één keten', 'Altijd in co-creatie met mbo, hbo en wo', 'Open source, voor elke instelling'].forEach((b, i) => {
      const y = 4.6 + i * 0.55;
      cv.circle({ x: M + 0.2, y: y + 0.12, d: 0.17, fill: ['blauw', 'oranje', 'groen'][i] });
      cv.text(b, { x: M + 0.55, y, w: w - 0.35, h: 0.55, size: 16, color: 'zwart', min: 12 });
    });
  },

  // Vaste afsluitslide ("Blijf in contact") met de CEDA-links, woordelijk gelijk aan
  // clidev/_template.md. Altijd de allerlaatste slide; de kaarten zijn klikbaar.
  contact(cv) {
    cv.slide.background = { path: 'public/npuls/powerpoint_slides/Slide1.PNG' };
    cv.label('Tot slot', { x: M, y: 1.75, w: CW, h: 0.35, color: 'oranje', size: 13, align: 'center' });
    cv.text('Blijf in contact', { x: M, y: 2.15, w: CW, h: 0.95, size: 44, color: 'blauw', font: FONT.head, align: 'center' });
    cv.text('Vragen, feedback of zin om mee te bouwen? We horen graag van je.', { x: 2.5, y: 3.15, w: W - 5, h: 0.5, size: 18, color: 'zwart', align: 'center' });
    const links = [
      ['GitHub', 'github.com/cedanl', 'blauw', 'roze', 'https://github.com/cedanl'],
      ['Community', 'community.npuls.nl/groups/data-ai', 'groen', 'zwart', 'https://community.npuls.nl/groups/data-ai'],
      ['Email', 'ceda@surf.nl', 'oranje', 'zwart', 'mailto:ceda@surf.nl'],
    ];
    const cw = 3.5, gap = 0.3, x0 = (W - (3 * cw + 2 * gap)) / 2;
    links.forEach(([tag, label, c, fg, url], i) => {
      const x = x0 + i * (cw + gap);
      cv.box({ x, y: 4.0, w: cw, h: 1.35, fill: 'wit', r: 0.2 });
      cv.pill(tag, { x: x + (cw - 1.6) / 2, y: 4.22, w: 1.6, h: 0.4, fill: c, color: fg, size: 12 });
      cv.slide.addText(label, {
        x: x + 0.15, y: 4.78, w: cw - 0.3, h: 0.4, margin: 0, align: 'center',
        fontFace: FONT.body, fontSize: 14, color: hex('zwart'), hyperlink: { url },
      });
    });
  },

  // Afsluiting: vraag in Cooper, optioneel punten/contact. Logo alleen op roze.
  closing(cv, s) {
    const v = cv.v;
    const logo = v.bg === 'roze' && s.logo !== false;
    if (!logo) cv.mark();
    cv.title(s.title ?? 'Vragen?');
    const hasRight = s.points?.length || s.illustration;
    const lw = hasRight ? 5.6 : 9.5;
    const qh = Math.min(2.6, textHeight(s.question, { w: lw, size: 40, font: FONT.quote }) + 0.1);
    cv.text(s.question, { x: M, y: 1.8, w: lw, h: qh, size: 40, color: v.quote, font: FONT.quote, min: 24 });
    let ty = 1.8 + qh + 0.35;
    if (s.text) { cv.text(s.text, { x: M, y: ty, w: lw, h: 0.9, size: 18, color: v.text, font: FONT.head, min: 11 }); ty += 1.0; }
    if (s.contact) cv.text(s.contact, { x: M, y: ty, w: lw, h: 0.45, size: 16, color: v.accent, font: FONT.head, min: 11 });
    if (s.points?.length) {
      const x = 7.0, w = W - M - x;
      if (s.pointsTitle) cv.text(s.pointsTitle, { x, y: 1.75, w, h: 0.5, size: 22, color: v.title, font: FONT.head });
      const card = v.cards[v.cards.length - 1];
      const r = CARD[card];
      const ph = Math.min(1.5, (4.6 / s.points.length) - 0.15);
      s.points.forEach((p, i) => {
        const y = 2.45 + i * (ph + 0.15);
        cv.box({ x, y, w, h: ph, fill: card, r: 0.25 });
        if (p.tag) cv.pill(p.tag, { x: x + 0.3, y: y + 0.22, w: 1.5, h: 0.38, fill: r.pillBg, color: r.pillFg, size: 11 });
        cv.text(p.text, { x: x + 0.3, y: y + (p.tag ? 0.7 : 0.2), w: w - 0.6, h: ph - (p.tag ? 0.85 : 0.4), size: 15, color: r.text, min: 10 });
      });
    } else if (s.illustration) {
      cv.illustration(s.illustration, { x: 8.0, y: 1.6, w: 4.6, h: 4.6 });
    }
    if (logo) cv.slide.addImage({ path: 'public/npuls/npuls_logo.jpg', x: W - M - 1.3, y: H - M - 1.3, w: 1.3, h: 1.3, altText: 'Npuls' });
    else if (s.deco !== false && !hasRight) cv.deco('ringen', { x: 9.6, y: 3.6, w: 2.8, h: 2.8 });
    else if (s.deco !== false) cv.deco('ringen', { x: M + 0.05, y: 5.6, w: 1.5, h: 1.5 });
  },
};

export const TYPES = Object.keys(LAYOUTS);
export { C };
export const FOOT_GRIJS = GRIJS;
