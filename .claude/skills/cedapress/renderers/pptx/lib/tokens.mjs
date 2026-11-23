// Npuls-palet, kleurrollen en toegestane combinaties als PowerPoint-hex (zonder #), met korte namen (blauw, licht-geel).
// Alles komt uit vormgever-npuls-huisstijl/references/design-tokens.json: hier staat geen enkele kleurtabel meer.
// De vorm van de exports (C, ALLOWED, VARIANTS, CARD, ICON_FG, TILE_ON, BADGE_FG, CHART_ORDER) is gelijk gebleven.
import { colorTable, loadTokensOrExit, short } from '../../lib/design-tokens.mjs';

const T = loadTokensOrExit();
const S = short;
const real = (o) => Object.entries(o).filter(([k]) => !k.startsWith('_'));
const map = (o, f = S) => Object.fromEntries(real(o).map(([k, v]) => [S(k), f(v)]));

export const C = map(colorTable(T), (v) => v.replace('#', '').toUpperCase());

// Neutraal grijs alleen voor voetnoten op lichte vlakken (design-tokens: neutrals).
export const GRIJS = T.neutrals['grijs-600'].replace('#', '').toUpperCase();

// allowed_combinations: achtergrond naar toegestane voorgrond.
export const ALLOWED = Object.fromEntries(T.colors.allowed_combinations.map((c) => [S(c.background), c.with.map(S)]));

// Slide-varianten: achtergrond + vaste rollen (slide_roles). Elke rol is een toegestane voorgrond.
// cards = kaartkleuren die op deze achtergrond mogen. accent2 = openingsteken van een citaat; highlight = markering achter het
// accentdeel van de titel (alleen waar het accent als tekst te weinig contrast haalt), anders null.
export const VARIANTS = map(T.slide_roles, (r) => ({
  title: S(r.title), text: S(r.text), accent: S(r.accent), accent2: S(r.accent_2), quote: S(r.quote), mark: S(r.marker),
  highlight: r.title_highlight ? S(r.title_highlight) : null, cards: r.cards.map(S), deco: r.deco.map(S),
}));
for (const [bg, v] of Object.entries(VARIANTS)) v.bg = bg;

// Tekstrollen per kaartkleur: groot (kerncijfer/badge), kop, tekst, label, pil.
export const CARD = map(T.card_roles, (r) => ({
  big: S(r.big), title: S(r.title), text: S(r.text), label: S(r.label), pillBg: S(r.pill_bg), pillFg: S(r.pill_fg),
}));

// Icoontegel: tegelkleur naar kleur van het icoon. Tegelkleur op een kaart: nooit gelijk aan de kaartkleur.
export const ICON_FG = map(T.tile_pairs.icon_fg);
export const TILE_ON = map(T.tile_pairs.on_card);
export const TILE_CYCLE = T.tile_pairs.cycle.map(S);
// Tekst op een gekleurde pil of cirkel (label-pil, stapnummer): alleen toegestane combinaties.
export const BADGE_FG = map(T.badge_fg);
// Zachte tint bij een accentkleur (kaarten en rijen op een witte slide) en standaardkleur van de heldenkaart.
export const TINT = map(T.tints);
export const HERO_DEFAULT = S(T.component_defaults.hero);

// Grafiekreeksen in de volgorde uit data_visualization.categorical_order (zwart is nooit een vlak).
export const CHART_ORDER = T.data_visualization.categorical_order.map(S).filter((c) => c !== 'zwart');

// Echte Npuls-fonts. De semibold is in Windows een eigen familie: gebruik die
// naam i.p.v. bold:true op "General Sans" (anders tekent PowerPoint een nep-vet).
export const FONT = {
  body: 'General Sans',
  head: 'General Sans Semibold',
  quote: 'Cooper Lt BT',
};

export const hex = (name) => {
  const v = C[name];
  if (!v) throw new Error(`Onbekende Npuls-kleur "${name}". Kies uit: ${Object.keys(C).join(', ')}`);
  return v;
};

/** Controleert of de tokens zelf kloppen: elke kleurrol verwijst naar een bestaande kleur en elke voorgrond op een
 *  verzadigde achtergrond is een toegestane combinatie. Geeft een lijst met fouten (leeg = goed). */
export function checkTokens() {
  const errs = [];
  const known = (name, where) => { if (!C[name]) errs.push(`design-tokens.json: ${where} gebruikt kleur "${name}" die niet in colors staat`); };
  const light = (bg) => bg === 'wit' || bg.startsWith('licht-');
  for (const [bg, v] of Object.entries(VARIANTS)) {
    if (!C[bg]) errs.push(`design-tokens.json: slide_roles.${bg} is geen kleur uit colors`);
    for (const role of ['title', 'text', 'accent', 'accent2', 'quote', 'mark', 'highlight']) if (v[role]) known(v[role], `slide_roles.${bg}.${role}`);
    for (const c of [...v.cards, ...v.deco]) known(c, `slide_roles.${bg}.cards/deco`);
    if (!light(bg)) {
      for (const role of ['title', 'text', 'accent', 'quote']) {
        if (v[role] !== bg && !ALLOWED[bg]?.includes(v[role])) errs.push(`design-tokens.json: slide_roles.${bg}.${role} = ${v[role]} is geen toegestane combinatie (allowed_combinations)`);
      }
    }
  }
  for (const [c, r] of Object.entries(CARD)) for (const [role, name] of Object.entries(r)) known(name, `card_roles.${c}.${role}`);
  for (const [group, o] of Object.entries({ icon_fg: ICON_FG, on_card: TILE_ON, badge_fg: BADGE_FG })) {
    for (const [k, v] of Object.entries(o)) { known(k, group); known(v, `${group}.${k}`); }
  }
  for (const c of [...TILE_CYCLE, ...CHART_ORDER]) known(c, 'tile_pairs.cycle/data_visualization');
  for (const [bg, fgs] of Object.entries(ALLOWED)) { known(bg, 'allowed_combinations'); fgs.forEach((f) => known(f, `allowed_combinations.${bg}`)); }
  return errs;
}
