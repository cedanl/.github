// Npuls-palet en de toegestane combinaties, als PowerPoint-hex (zonder #).
// Bron van waarheid: vormgever-npuls-huisstijl/references/design-tokens.json.
// build.mjs vergelijkt deze waarden met dat bestand als het gevonden wordt.

export const C = {
  oranje: 'DD784B',
  zwart: '000000',
  roze: 'F4D9DC',
  blauw: '3D68EC',
  geel: 'F4D74B',
  groen: '00AF81',
  wit: 'FFFFFF',
  'licht-groen': 'CCEEE6',
  'licht-blauw': 'D6E2FD',
  'licht-roze': 'FAEAEA',
  'licht-oranje': 'FFE4D8',
  'licht-geel': 'FCF5D4',
};

// Neutraal grijs alleen voor voetnoten op lichte vlakken (design-tokens: neutrals).
export const GRIJS = '5C5C66';

// allowed_combinations uit design-tokens.json: achtergrond → toegestane voorgrond.
// Lichte (secondary) vlakken en wit dragen zwart, blauw, groen of oranje.
export const ALLOWED = {
  blauw: ['geel', 'roze'],
  roze: ['blauw', 'groen', 'zwart', 'oranje'],
  geel: ['oranje', 'zwart', 'blauw'],
  groen: ['roze', 'zwart'],
  oranje: ['zwart', 'roze'],
  wit: ['blauw', 'zwart', 'groen', 'oranje'],
  'licht-groen': ['blauw', 'zwart', 'groen'],
  'licht-blauw': ['blauw', 'zwart'],
  'licht-roze': ['blauw', 'zwart', 'groen', 'oranje'],
  'licht-oranje': ['blauw', 'zwart', 'oranje'],
  'licht-geel': ['blauw', 'zwart', 'oranje'],
};

// Slide-varianten: achtergrond + vaste rollen. Elke rol is een toegestane voorgrond.
// cards = kaartkleuren die op deze achtergrond mogen (nooit gelijk aan de achtergrond).
export const VARIANTS = {
  blauw: { bg: 'blauw', title: 'roze', text: 'roze', accent: 'geel', quote: 'geel', mark: 'roze', cards: ['geel', 'roze'], deco: ['geel', 'roze'] },
  roze: { bg: 'roze', title: 'zwart', text: 'zwart', accent: 'blauw', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen'], deco: ['blauw', 'oranje'] },
  groen: { bg: 'groen', title: 'zwart', text: 'zwart', accent: 'roze', quote: 'zwart', mark: 'zwart', cards: ['roze'], deco: ['roze'] },
  oranje: { bg: 'oranje', title: 'zwart', text: 'zwart', accent: 'roze', quote: 'zwart', mark: 'zwart', cards: ['roze'], deco: ['roze'] },
  geel: { bg: 'geel', title: 'blauw', text: 'zwart', accent: 'oranje', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'wit'], deco: ['oranje', 'blauw'] },
  wit: { bg: 'wit', title: 'blauw', text: 'zwart', accent: 'blauw', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['blauw', 'oranje'] },
  'licht-geel': { bg: 'licht-geel', title: 'blauw', text: 'zwart', accent: 'oranje', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['oranje', 'blauw'] },
  'licht-blauw': { bg: 'licht-blauw', title: 'blauw', text: 'zwart', accent: 'blauw', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['blauw'] },
  'licht-groen': { bg: 'licht-groen', title: 'blauw', text: 'zwart', accent: 'groen', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['groen', 'blauw'] },
  'licht-oranje': { bg: 'licht-oranje', title: 'blauw', text: 'zwart', accent: 'oranje', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['oranje', 'blauw'] },
  'licht-roze': { bg: 'licht-roze', title: 'blauw', text: 'zwart', accent: 'oranje', quote: 'zwart', mark: 'zwart', cards: ['blauw', 'oranje', 'groen', 'geel'], deco: ['oranje', 'blauw'] },
};

// Tekstrollen per kaartkleur: groot (kerncijfer/badge), kop, tekst, label.
// Body-tekst op groen en oranje is zwart: roze haalt daar geen leesbaar contrast.
export const CARD = {
  blauw: { big: 'geel', title: 'roze', text: 'roze', label: 'geel', pillBg: 'geel', pillFg: 'blauw' },
  oranje: { big: 'zwart', title: 'zwart', text: 'zwart', label: 'zwart', pillBg: 'roze', pillFg: 'zwart' },
  groen: { big: 'roze', title: 'zwart', text: 'zwart', label: 'zwart', pillBg: 'roze', pillFg: 'zwart' },
  geel: { big: 'blauw', title: 'blauw', text: 'zwart', label: 'blauw', pillBg: 'blauw', pillFg: 'geel' },
  roze: { big: 'blauw', title: 'blauw', text: 'zwart', label: 'blauw', pillBg: 'blauw', pillFg: 'roze' },
  wit: { big: 'blauw', title: 'blauw', text: 'zwart', label: 'oranje', pillBg: 'blauw', pillFg: 'roze' },
};

// Accent volgt de achtergrond (OPP-20): wit en licht-blauw → blauw, licht-groen → groen, licht-oranje en licht-geel → oranje.
// Op verzadigde vlakken moeten titel en accent verschillen, anders is het accentdeel (en de label-pil, die de accentkleur draagt) onzichtbaar:
// roze: titel zwart, accent blauw · groen: titel zwart, accent roze · blauw: titel roze, accent geel · oranje: titel zwart, accent roze · geel: titel blauw, accent oranje.
// Oranje op licht-oranje haalt maar ca. 2,5:1: daar alleen voor het titelaccent en groot display (kerncijfer), nooit voor kleine tekst (OPP-20).
// Icoontegel: tegelkleur → kleur van het icoon (tegelparen uit OPP-22; zwart is nooit een vlak).
export const ICON_FG = { blauw: 'geel', geel: 'blauw', groen: 'roze', oranje: 'zwart', roze: 'blauw', wit: 'blauw' };
// Tegelkleur op een kaart: nooit gelijk aan de kaartkleur.
export const TILE_ON = { blauw: 'geel', oranje: 'roze', groen: 'roze', geel: 'blauw', roze: 'blauw' };
// Tekst op een gekleurde pil of cirkel (label-pil, stapnummer): alleen toegestane combinaties.
export const BADGE_FG = { blauw: 'roze', groen: 'zwart', oranje: 'zwart', geel: 'blauw', roze: 'blauw' };

// Grafiekreeksen in de volgorde uit data_visualization.categorical_order.
export const CHART_ORDER = ['blauw', 'oranje', 'groen', 'geel', 'roze'];

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
