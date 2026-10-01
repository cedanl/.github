# Slidetypes en varianten

Een deck is een JS-module met `export default { title, author, slides: [...] }`. Elke slide is
een object met `type`, optioneel `variant`, de velden hieronder en `notes` (sprekersnotities).

In elk tekstveld maakt `**woorden**` die woorden vet (kopfont) in de accentkleur van de variant.
`\n` is een nieuwe regel. Illustraties: bestandsnaam zonder `.svg` uit
`public/npuls/powerpoint_illustrations/` (lijst en thema's: zie de assets-tabel in de `clanna`-skill,
of `ls public/npuls/powerpoint_illustrations`).

## Varianten (achtergrond)

| Variant | Gebruik | Kaarten krijgen |
|---|---|---|
| `blauw` | titel, sectie, citaat — de sterkste kleur | geel, roze |
| `roze` | kerncijfers, afsluiting (logo verschijnt alleen hier) | blauw, oranje, groen |
| `groen` / `oranje` / `geel` | één kernboodschap of sectie | roze (op geel: blauw, oranje) |
| `licht-geel` / `licht-blauw` / `licht-groen` / `licht-roze` | inhoudsslides met kaarten, lijsten, tabellen, grafieken | blauw, oranje, groen, geel |
| `wit` | alleen als het echt moet (Npuls is kleurrijk) | blauw, oranje, groen, geel |

Kaartkleur overschrijven: `color: 'groen'` op een item. De build waarschuwt bij een combinatie
die niet in `allowed_combinations` staat.

Default: `title` en `section` → `blauw`, de rest → `licht-geel`. Wissel lichte varianten af en
zet per kernboodschap één verzadigde slide.

## Types

### `title` — openingsslide
`kicker` (pill, bv. `'CEDA · DAIR-bijeenkomst'`), `title`, `lede` (Cooper, één zin), `sub`
(kleine regel: duur, datum, spreker), `agenda` (2-4 korte punten, genummerd rechts) **of**
`illustration`, `tagline` (optioneel, rechtsonder), `deco: false` zet de golven uit.

### `section` — kernboodschap of hoofdstuk
`number` (optioneel), `title` (bewering, max ~8 woorden), `text` (Cooper, één zin),
`illustration` of `deco: 'ringen' | 'starburst' | 'golven' | false`.

### `stats` — kerncijfers
`title`, `lede` (optioneel), `items: [{ value, label, text, color? }]` (2-4), `callout`
(witte balk, gebruik `**Kop:** tekst`), `footnote`.

### `cards` — kolommen, casussen, stappen
`title`, `items` (2-4): `{ badge?, tag?, title, sub?, sections: [{ label?, text, strong? }] | text, illustration?, color? }`.
`numbered: true` nummert de badges, `arrows: true` zet chevrons tussen de kaarten (proces).
`footer` (één zin onder de kaarten), `footnote`. Per kaart max ~35 woorden.

### `split` — tekst naast een illustratie
`title`, `lede` (optioneel), `bullets` (max 4) **of** `text`, `illustration`, `side: 'left'`
zet de illustratie links.

### `list` — rijen met status (randvoorwaarden, open punten, planning)
`title`, `items: [{ title, text, status?, color? }]` (max 7), `footer`, `footnote`.
Statuskleuren: `groen` = vast/klaar, `oranje` = open/aandacht, `blauw` = info. Nooit rood.

### `table` — echte PowerPoint-tabel
`title`, `columns`, `rows` (max ~8, bij meer: splitsen), `widths` (fracties, optioneel).

### `chart` — bewerkbare PowerPoint-grafiek
`title` (de conclusie, niet "Grafiek van X"), `chart: 'bar' | 'line' | 'pie' | 'doughnut'`,
`labels`, `series: [{ name, values }]`, `horizontal`, `stacked`, `format` (Excel-formaat, bv.
`'0"%"'` of `'#,##0'`), `takeaway` (kaart rechts), `illustration` (onder de takeaway),
`source` (voetnoot). Kleuren volgen de Npuls-volgorde blauw → oranje → groen → geel → roze.

### `quote` — citaat
`text`, `by`, `illustration` (optioneel). Beste op `blauw`.

### `image` — schermafbeelding of foto
`title`, `image` (pad vanaf de projectroot, PNG/JPEG, bv. `public/shots/...`), `caption`,
`text` (optioneel, kolom rechts), `alt`.

### `ceda` — vaste CEDA-introslide
Geen velden. "Wie is CEDA": titel, subtitel en drie punten over wat CEDA doet, op de Npuls-achtergrond met roze logovlak (`Slide16.PNG`). Tekst is woordelijk gelijk aan `clidev`/`_template.md`. Plaats: direct na de titel (of agenda). Bewust zonder links.

### `contact` — vaste afsluitslide
Geen velden. "Blijf in contact" met drie klikbare kaarten: GitHub (`github.com/cedanl`), Community (`community.npuls.nl/groups/data-ai`) en e-mail (`ceda@surf.nl`), op `Slide1.PNG`. Altijd de allerlaatste slide; blijft in beeld tijdens de vragen.

### `closing` — afsluiting (optioneel, vóór `contact`)
`title` (default "Vragen?"), `question` (Cooper), `text`, `contact` (alleen als bekend; nooit
verzinnen), `points: [{ tag?, text }]` + `pointsTitle` **of** `illustration`. Op `roze` komt
het Npuls-logo rechtsonder.

## Minimaal voorbeeld

```js
export default {
  title: 'Studiesucces in beeld',
  slides: [
    { type: 'title', kicker: 'CEDA · Thinktank', title: 'Studiesucces in beeld', lede: 'Wat de 1CHO-data ons vertelt', sub: '23 september 2026', illustration: 'learninganalystics', notes: '...' },
    { type: 'stats', variant: 'roze', title: 'Drie cijfers die opvallen', items: [{ value: '15%', label: 'uitval jaar 1', text: 'hbo, cohort 2024' }, { value: '62%', label: 'diploma in 5 jaar', text: 'alle sectoren' }, { value: '1 op 4', label: 'wisselt', text: 'binnen de instelling' }], notes: '...' },
    { type: 'ceda' },
    { type: 'closing', variant: 'blauw', question: 'Waar wil jij als eerste in duiken?', notes: '...' },
    { type: 'contact' },
  ],
};
```

Het volledige voorbeeld met elk type, inclusief `ceda` en `contact`, staat in `assets/voorbeeld.deck.mjs`.
