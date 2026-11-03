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
De standaard is `roze`: de originele Npuls-titelslide (`Slide1.PNG`, roze met zwart logo linksboven en
oranje bogen rechtsonder; logo en bogen zitten in de achtergrond). Alleen tekst erbij: `title` (blauw),
`lede` (Cooper, één zin), en één kleine regel die `kicker` en `sub` samenvoegt (bv.
`CEDA · DAIR-bijeenkomst · 120 minuten`). `illustration` mag, `agenda`, `tagline` en `deco` worden op
roze niet getoond (waarschuwing): zet het programma in een tijdlijn.
Wil je toch de blauwe titelslide (blauw met bogen, wit logo, kicker-pill, agenda genummerd rechts of
`illustration`, `tagline`, `deco: false` zet de golven uit), geef dan `variant: 'blauw'`. `npuls: false` zet
de Npuls-achtergrond uit.

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
`rows: [{ label, items }]` (max 2) in plaats van `items` zet twee rijen kaarten onder elkaar, elk met een
label erboven (bv. stappen en valkuilen); houd de kaarttekst dan kort. `callout` zet een grote witte balk
onder de kaarten voor een oproep of kernboodschap (gebruik `**Kop:** tekst`).

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

### `timeline` — programma of planning op schaal
`title`, `blocks: [{ minutes, title, text?, tag?, color?, start? }]` (2-8), `legend: [{ color, label }]`,
`total` (optioneel, anders de som), `footnote`. De breedte van elk blok volgt de duur; de tijden erboven
worden opgeteld. `tag` is een kleine pill onder het blok (bijvoorbeeld een skill of spreker),
`color` een Npuls-kleur (default: de kaartkleuren van de variant). Blokken onder ~0,9 inch breed geven een waarschuwing.

### `quote` — citaat
`text`, `by`, `illustration` (optioneel). Beste op `blauw`.

### `image` — schermafbeelding of foto
`title`, `image` (pad vanaf de projectroot, PNG/JPEG, bv. `public/shots/...`), `caption`,
`text` (optioneel, kolom rechts), `alt`.

### `video` — video die in PowerPoint afspeelt
Zelfde opbouw als `image`: `title`, `video` (pad naar een `.mp4`, H.264), `caption`, `text` (optioneel), `alt`.
Het stilstaande beeld tot je op afspelen klikt is `poster` (PNG); zonder `poster` haalt `build.mjs` het beeld
op `posterAt` seconden (standaard 1) uit de video met ffmpeg. De video zit in het bestand: reken op de grootte
van de mp4 erbij. Speelt niet af in de PDF of in Google Slides; daar zie je alleen de poster. Geen `.webm`:
PowerPoint op Windows speelt die niet betrouwbaar af.

### `ceda` — vaste CEDA-introslide
Geen velden. "Wie is CEDA": titel, subtitel en drie punten over wat CEDA doet, links op wit; rechts het roze vlak met het Npuls-logo (template-layout Partnerslide; oude engine: `Slide16.PNG`). Tekst is woordelijk gelijk aan `clidev`/`_template.md`. Plaats: direct na de titel (of agenda). Bewust zonder links.

### `team` — vaste teamslide
Alleen `text` (optioneel). "Wie zijn wij": groepsfoto van het CEDA-team (`public/shots/team/groep.png`) met rechts
de projecten (standaard: Instroomprognose en Staat van de Onderwijsinstelling), zoals in de DAIR-decks. Plaats: direct na `ceda`.

### `contact` — vaste afsluitslide
Geen velden. "Blijf in contact" met drie klikbare kaarten: GitHub (`github.com/cedanl`), Community (`edu.nl/7b4yg`) en e-mail (`ceda@surf.nl`), op `Slide1.PNG`. Altijd de allerlaatste slide; blijft in beeld tijdens de vragen.

### `closing` — afsluiting (optioneel, vóór `contact`)
`title` (default "Vragen?"), `question` (Cooper), `text`, `contact` (alleen als bekend; nooit
verzinnen), `points: [{ tag?, text }]` + `pointsTitle` **of** `illustration`. Op `roze` komt
het Npuls-logo rechtsonder.

## Template-engine (standaard)

`build.mjs` bouwt op `public/npuls/Npuls_powerpoint-template.potx`. Elk type krijgt een layout uit de template:

| Type | Layout in de template |
|---|---|
| `title` | Titeldia (roze, standaard); `variant: 'blauw'` of `'oranje'` → Titeldia 3. `kicker` en `sub` op eigen regels |
| `section` | Sectiescheider op de master van de variant: `blauw`, `oranje`, `geel` of `roze` (`groen` bestaat niet → blauw). `number` komt klein bovenaan |
| `split` | Tekst en afbeelding 1 (illustratie rechts) of 2 (`side: 'left'`); `image` mag in plaats van `illustration` |
| `list` | Tot 4 items zonder `footer`: Stappen (golf links, vakken rechts; `illustration` per item wordt het icoon). Meer: rijen op Alleen titel |
| `quote` | Quote (op `roze` de roze master) |
| `closing` | Sectiescheider (standaard roze): `title` klein bovenaan, `question` groot |
| `ceda` | Partnerslide (wit met rechts het roze Npuls-vlak) |
| `team` | Alleen titel, groepsfoto met tekst rechts (licht-blauw) |
| `contact` | Titeldia roze (logo en bogen uit de template), gecentreerd met drie witte kaarten en klikbare links, gelijk aan de oude engine; daarna volgt automatisch de **Einddia** (Npuls-logo). `einddia: false` op het deck zet die uit |
| `cards`, `stats`, `chart`, `table`, `timeline`, `image` | Alleen titel, met de inhoud getekend als vormen, grafiek of tabel |

Verschillen met de oude engine:
- Inhoudsslides zijn standaard **wit**, zoals in de template. Een andere variant wordt de achtergrond van die slide (Opmaak achtergrond); de layout blijft die van de template.
- Titels staan in de titel-placeholder (40pt, zwart op wit en licht). Te lang → automatisch kleiner, met een waarschuwing.
- `image` kan een `link` krijgen: klikken op de afbeelding opent die URL.
- Geen eigen beeldmerk of golven: logo en vormtaal komen uit de template.

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
