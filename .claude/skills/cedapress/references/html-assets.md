# Npuls-assets in een HTML-deck (assetpakket)

Alle paden zijn **relatief vanaf de deckmap**; `npuls/` is de link naar het Npuls-assetpakket die `renderers/html/prepare.mjs` aanmaakt (niet in git, versie uit `assets.lock`). Spaties in bestandsnamen als `%20` schrijven.

## Fonts — zitten al in de frame

`npuls/web/npuls.css` (de frame linkt die al) is gegenereerd uit design-tokens.json (enige bron voor kleuren; de frame bevat geen eigen hex-kleuren, `check.mjs` meldt ze als fout; `bundle.mjs` bakt de css in) en laadt General Sans via Fontshare, met Plus Jakarta Sans als vervanger. Cooper Light zit niet in het pakket (licentie): alleen zichtbaar als hij lokaal geïnstalleerd is; anders Georgia. Zie `fonts.md` in het pakket.

## Logo

`npuls/logos/npuls-logo-roze.jpg` — 200×200, beeldmerk + woordmerk op een **roze vlak** (≈ `--npuls-roze`). Daarom alleen op `s-roze`-slides (check.mjs dwingt dit af). De frame zet het al op de afsluitslide.

## Illustraties

`npuls/illustraties/<naam>.svg` — 48 Npuls-illustraties (pakket 0.2.0), zwarte contour, vlakken in het Npuls-palet.
26 komen uit de officiële potx (isometrisch, vierkant); 22 komen van npuls.nl (kaart- en sectordoel-illustraties,
andere stijl, vaak met gekleurd vlak). Herkomst per bestand: `illustraties-mapping.json` in het pakket.
De namen uit pakket 0.1.0 (`illustratie-01` t/m `illustratie-26`) bestaan niet meer; de pptx-renderer vertaalt ze nog
(`ILLU_ALIAS` en `ILLU_NUMMER` in `renderers/pptx/lib/assets.mjs`), de HTML niet.

```html
<img class="illu" src="npuls/illustraties/team-rond-idee.svg" alt="">
<img class="illu-sm" src="npuls/illustraties/gloeilamp.svg" alt="">
```

Uit de potx (oude naam uit 0.1.0 tussen haakjes):

| Thema | Naam (wat staat erop; oud nummer) |
|---|---|
| Data, AI, tech | `laptop-dashboard` (01) · `brein-ai-chip` (02) · `ai-chip` (03) · `atoom` (04) · `brein-tandwiel` (05) · `servers` (06) · `vr-bril` (15) · `netwerk-blokken` (20) · `video` (26, filmstrook) |
| Scherm | `videobellen` (13, laptop met videogesprek) · `computer` (17, pc met toetsenbord) |
| Mensen | `presentator` (16) · `financien-analyse` (18, persoon + munten + rekenmachine) · `werkplek-idee` (22, persoon achter toetsenbord + lamp) |
| Samen, delen | `team-rond-idee` (07, groep rond lamp) · `handdruk` (10) · `gesprek` (11, tekstballonnen) · `samen-idee` (14, mensen in een kring + lamp) |
| Onderwijs | `boeken` (08) · `afstudeerhoed` (12) · `schoolgebouw` (21, met boom) |
| Idee, inzicht | `gloeilamp` (19, met stralen) · `locatie` (23, locatiepin) · `verrekijker` (24) |
| Planning, erkenning | `kalender` (09) · `cadeau` (25) |

Van npuls.nl (nieuw in 0.2.0): `microcredential`, `persoon-groot-scherm`, `digitale-geletterdheid`, `wereldbol`,
`samenwerking-leveranciers`, `docentondersteuning`, `xr-bril`, `xr`, `ai-chip-geel`, `nederland-pilots`, `regelingen`,
`nederland-netwerk`, `leermaterialen-collectief`, `leermaterialen`, `onderwijsaanbod`, `onderwijsmiddelen`, `europa-ai`,
`ai-raamwerk`, `administratie`, `scan-vergrootglas`, `digitaal-toetsen`, `kit`. `europa-ai` en `ai-raamwerk` bevatten een
ingesloten raster (groter bestand). Deze stijl wijkt af van de potx-illustraties: meng ze niet op één slide.

## Tegels

`npuls/tegels/tegel-*.svg` — 10 gekleurde banner- en kaarttegels van npuls.nl (effen vlak in één huisstijlkleur met één
illustratie, soms met dunne witte cirkellijn). Kant-en-klaar voorbeeld voor het banner/hero-patroon. Kleuren: blauw
(`tegel-onderwijsmiddelen`, `tegel-toetsen-leren`, `tegel-professionalisering`, `tegel-themas`), groen
(`tegel-microcredentials`, `tegel-instelling-of-individu`), oranje (`tegel-visie-ai`, `tegel-ai`), roze
(`tegel-nederland-instellingen`) en `tegel-verhaal-npuls` (roze/oranje/blauw, met logo). `tegel-themas.svg` bevat de
officiële Npuls-lijnpictogrammen; gebruik die als alternatief voor icoontjes. Herkomst: `tegels-mapping.json`.

Vormtaal (sterren, pijlen, golven, tegels, bogen) staat in `npuls/vormen/` (o.a. `bogen.svg`, `golf-oranje.svg`,
`tegel-*.svg`, `npuls-logo.svg`, `cc-by-sa.svg`), niet in `illustraties/`.

**Kiezen:** één illustratie per slide, als beeld naast tekst (`split`) of klein in een kaart (`illu-sm`). Niet als achtergrond, niet naast een decoratieve `.deco` op dezelfde plek.

## Wat níét gebruiken

- `npuls/slides-preview/slideNN.png` — voorbeelden van de pptx-layouts, geen achtergronden; botsen met de slide-varianten hier.
- `npuls/web/sprite.svg` via `<use href="npuls/web/sprite.svg#…">`: Chrome blokkeert externe `<use>` bij `file://`. Bogen zet de frame daarom inline; iconen via Font Awesome.
- Verzonnen logo's of een nagetekend beeldmerk.
