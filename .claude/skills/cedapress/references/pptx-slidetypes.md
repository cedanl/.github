<!-- Overgenomen uit powerclaude/references/slidetypes.md; paden naar het Npuls-assetpakket. -->
# Slidetypes en varianten

Een deck is een JS-module met `export default { bron, title, author, slides: [...] }`; `bron` is de hash van
`bron.md` (`parse_bron.py bron.md --hash`), `build.mjs` faalt als die niet klopt. Elke slide is
een object met `type`, optioneel `variant`, de velden hieronder en `notes` (sprekersnotities).

In elk tekstveld maakt `**woorden**` die woorden vet (kopfont) in de accentkleur van de variant.
`\n` is een nieuwe regel. Illustraties: bestandsnaam zonder `.svg` (bv. `team-rond-idee`) uit
`illustraties/` in het Npuls-assetpakket; wat erop staat: `references/html-assets.md`. Oude namen
(`kennisdeling`, `Lamp`, de nummers uit pakket 0.1.0, …) worden nog vertaald, maar alleen als er een tegenhanger in het pakket is.

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
De standaard is `roze`: de originele Npuls-titelslide (`slides-preview/slide01.png`, roze met zwart logo linksboven en
oranje bogen rechtsonder; logo en bogen zitten in de achtergrond). Alleen tekst erbij: `title` (groot, oranje, het titelvak
is verbreed zodat een korte titel op één regel blijft), `lede` (oranje, één zin) en twee metaregels in Cooper: `kicker`
(bv. `CEDA · mbo-instellingen`) en `sub` (bv. de datum). De HTML-titelslide (`lay-titel`) is hier gelijk aan. `illustration` mag, `agenda`, `tagline` en `deco` worden op
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
`title`, `image` (pad vanaf de map waar je bouwt, PNG/JPEG, bv. `presentaties/YYMMDD_onderwerp/img/...`), `caption`,
`text` (optioneel, kolom rechts), `alt`.

### `video` — video die in PowerPoint afspeelt
Zelfde opbouw als `image`: `title`, `video` (pad naar een `.mp4`, H.264), `caption`, `text` (optioneel), `alt`.
Het stilstaande beeld tot je op afspelen klikt is `poster` (PNG); zonder `poster` haalt `build.mjs` het beeld
op `posterAt` seconden (standaard 1) uit de video met ffmpeg. De video zit in het bestand: reken op de grootte
van de mp4 erbij. Speelt niet af in de PDF of in Google Slides; daar zie je alleen de poster. Geen `.webm`:
PowerPoint op Windows speelt die niet betrouwbaar af.

### `ceda` — vaste CEDA-introslide (optioneel)
Geen velden. "Wie is CEDA": titel, subtitel en drie punten over wat CEDA doet, links op wit; rechts het roze vlak met het Npuls-logo (template-layout Partnerslide; oude engine: `slides-preview/slide16.png`). Tekst is woordelijk gelijk aan de HTML-frame en `clidev`. Plaats: eerste van het optionele blok `ceda` → `team` → `contact` vóór de afsluiter. Bewust zonder links.

### `team` — vaste teamslide (optioneel)
Alleen `text` (optioneel). "Wie zijn wij": groepsfoto van het CEDA-team (env `CEDA_TEAMFOTO`, anders `ceda/teamfoto.png` in het assetpakket, anders `img/team-groep.png` in de deckmap; zie `teamfoto` in `renderers/lib/npuls-assets.mjs`) met rechts
de projecten (standaard: Instroomprognose en Staat van de Onderwijsinstelling), zoals in de DAIR-decks. Plaats: direct na `ceda`.

### `contact` — vaste afsluitslide (optioneel)
Geen velden. "Blijf in contact" met drie klikbare kaarten: GitHub (`github.com/cedanl`), Community (`edu.nl/7b4yg`) en e-mail (`ceda@surf.nl`), op `slides-preview/slide01.png`. Sluit het blok vaste slides af; blijft in beeld tijdens de vragen. Alleen de Einddia volgt nog.

### `closing` — afsluiting (optioneel, vóór `contact`)
`title` (default "Vragen?"), `question` (Cooper), `text`, `contact` (alleen als bekend; nooit
verzinnen), `points: [{ tag?, text }]` + `pointsTitle` **of** `illustration`. Op `roze` komt
het Npuls-logo rechtsonder.

## Componenten uit ceda-powerpoint-maker (potx-engine)

Alleen in de potx-engine. Maten van Edwin (10 in breed) zijn met 4/3 omgerekend naar de potx (13,33 in); layouts en kleuren blijven die van de potx.

**Op elke inhoudsslide** (`cards`, `stats`, `list`, `table`, `chart`, `image`, `steps`, `lead`, `insight`, `lists`, `hero`):
- `label`: label-pil linksboven, 1 tot 3 woorden (OPP-18), kleur = accent van de slide.
- `title` met `**accentdeel**`: neutraal deel zwart, accentdeel in de accentkleur. Accent volgt de achtergrond: `wit` en `licht-blauw` blauw, `licht-groen` groen, `licht-oranje` en `licht-geel` oranje (OPP-20). Max ~45 tekens.
- `intro`: korte regel (16 pt) onder de titel; de inhoud schuift mee naar beneden.
- `note`: notitiebalk onderaan (`cards`, `steps`, `lead`, `insight`, `lists`): tekst of `{ text, bold, icon, color }`.
- `icon` op een item (`cards`, `insight`, `lists`, `note`): icoontegel, afgeronde tegel in een paletkleur (tegelparen OPP-22: blauw/geel, geel/blauw, groen/roze, oranje/zwart, roze/blauw) met het icoon uit `iconen/<naam>.svg` van het assetpakket. Zit er geen iconenset in het pakket (nu nog niet), dan blijft de tegel leeg en volgt een waarschuwing; er worden geen eigen iconen meegeleverd.

| Type | Velden | Edwins patroon |
|---|---|---|
| `steps` | `items: [{ title, text }]` (3 tot 4) | stapkolom (P7): verticale stap-kaarten met cirkel |
| `lead` | `lead`, `figures: [{ value, label }]` (1 tot 2), optioneel `items` (stappen rechts, 3 tot 4) en `eyebrow` | kernzin met kerncijfer(s) (P1) |
| `hero` | `eyebrow`, `text` (Cooper), `illustration`, `color` (standaard groen) | heldenkaart (P4) |
| `insight` | `rows: [{ icon, key, text, tag }]` (3 tot 5) | inzichtregels (P3) |
| `lists` | `groups: [{ title, icon, items, style: 'list' \| 'pills', columns }]` (2 tot 3 kaarten, 3 tot 5 items) | lijstkaart en pillenkaart (P8, P13) |

`cards`: een item met `icon` krijgt een icoontegel; een item met `illustration` krijgt een eigen blok boven de titel, zodat de tekst er nooit overheen loopt. Volle kaartkleuren (blauw, groen, oranje) max. 2 per slide (OPP-21): geef de rest `color: 'wit'`.

**Controles in de build** (waarschuwingen): tekst past niet (inkorten, niet verkleinen), woord breekt midden in het woord (langste woord breder dan het vak), illustratie overlapt tekst, meer dan 60 woorden (OPP-02), tekst kleiner dan 15 pt (body) of 12 pt (label) is niet mogelijk: kleinere groottes worden opgetrokken, past het dan niet, dan volgt de waarschuwing.

## Template-engine (standaard)

`build.mjs` bouwt op `pptx/Npuls_powerpoint-template.potx` uit het Npuls-assetpakket. Elk type krijgt een layout uit de template:

| Type | Layout in de template |
|---|---|
| `title` | Titeldia (roze, standaard); `variant: 'blauw'` of `'oranje'` → Titeldia 3. `kicker` en `sub` op eigen regels |
| `section` | Sectiescheider op de master van de variant: `blauw`, `oranje`, `geel` of `roze` (`groen` bestaat niet → blauw). `number` komt klein bovenaan |
| `split` | Tekst en afbeelding 1 (illustratie rechts) of 2 (`side: 'left'`); `image` mag in plaats van `illustration` |
| `list` | Tot 4 items zonder `footer`: Stappen (golf links, vakken rechts; `illustration` per item wordt het icoon). Meer: rijen op Alleen titel |
| `quote` | Quote (op `roze` de roze master): openingsteken, citaat in Cooper links, bron direct eronder, het blok in het optische midden; `illustration` groot rechts. Gelijk aan de HTML (`lay-quote`) |
| `closing` | Sectiescheider (standaard roze): `title` klein bovenaan, `question` groot |
| `ceda` | Partnerslide (wit met rechts het roze Npuls-vlak) |
| `team` | Alleen titel (licht-blauw): groepsfoto 3:2 op de marge, bijgesneden met afgeronde hoeken, projecten ernaast in het midden (eerste regel Cooper, namen in de accentkleur). Gelijk aan de HTML |
| `contact` | Titeldia roze (logo en bogen uit de template), gecentreerd met drie witte kaarten en klikbare links, gelijk aan de oude engine; daarna volgt automatisch de **Einddia** (Npuls-logo met "Onderwijs **bewegen.**" eronder, OPP-28). `einddia: false` op het deck zet die uit |
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
