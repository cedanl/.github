# Npuls-assets in een HTML-deck (assetpakket)

Alle paden zijn **relatief vanaf de deckmap**; `npuls/` is de link naar het Npuls-assetpakket die `renderers/html/prepare.mjs` aanmaakt (niet in git, versie uit `assets.lock`). Spaties in bestandsnamen als `%20` schrijven.

## Fonts — zitten al in de frame

`npuls/web/npuls.css` (de frame linkt die al) laadt General Sans via Fontshare, met Plus Jakarta Sans als vervanger. Cooper Light zit niet in het pakket (licentie): alleen zichtbaar als hij lokaal geïnstalleerd is; anders Georgia. Zie `fonts.md` in het pakket.

## Logo

`npuls/logos/npuls-logo-roze.jpg` — 200×200, beeldmerk + woordmerk op een **roze vlak** (≈ `--npuls-roze`). Daarom alleen op `s-roze`-slides (check.mjs dwingt dit af). De frame zet het al op de afsluitslide.

## Illustraties

`npuls/illustraties/illustratie-NN.svg` — 26 isometrische Npuls-illustraties uit de officiële potx (pakket 0.1.0),
zwarte contour, vlakken in het Npuls-palet. De potx geeft ze geen namen; beschrijving hieronder (visueel, 2026-11-19).
De oude namen uit `public/npuls/powerpoint_illustrations` bestaan niet meer; de pptx-renderer vertaalt ze nog
(`ILLU_ALIAS` in `renderers/pptx/lib/assets.mjs`), de HTML niet.

```html
<img class="illu" src="npuls/illustraties/illustratie-07.svg" alt="">
<img class="illu-sm" src="npuls/illustraties/illustratie-19.svg" alt="">
```

| Thema | Nummer (wat staat erop; oude naam) |
|---|---|
| Data, AI, tech | 01 laptop + dashboards + telefoon (learninganalystics) · 02 brein + AI-chip (kunstmatigeintelligentie) · 03 AI-chip (chip) · 04 atoom (Connecties) · 05 brein + tandwiel (brains) · 06 servers (data) · 15 VR-bril (vr) · 20 kubussen-netwerk (netwerk) · 26 filmstrook (video) |
| Scherm | 13 laptop met videogesprek · 17 pc met toetsenbord (pc) |
| Mensen | 16 presentator bij scherm (present) · 18 persoon + munten + rekenmachine (Financien/bestuurder) · 22 persoon achter toetsenbord + lamp (onderwijsprofessional) |
| Samen, delen | 07 groep rond lamp (kennisdeling) · 10 handdruk (hands) · 11 gesprek met tekstballonnen (gesprek) · 14 mensen in een kring + lamp (samenwerken) |
| Onderwijs | 08 boeken (books) · 12 afstudeerhoed (hat) · 21 schoolgebouw met boom |
| Idee, inzicht | 19 lamp met stralen (light) · 23 locatiepin (locatie) · 24 verrekijker |
| Planning, erkenning | 09 kalender (events) · 25 cadeau |

Vormtaal (sterren, pijlen, golven, tegels, bogen) staat in `npuls/vormen/` (o.a. `bogen.svg`, `golf-oranje.svg`,
`tegel-*.svg`, `npuls-logo.svg`, `cc-by-sa.svg`), niet in `illustraties/`.

**Kiezen:** één illustratie per slide, als beeld naast tekst (`split`) of klein in een kaart (`illu-sm`). Niet als achtergrond, niet naast een decoratieve `.deco` op dezelfde plek.

## Wat níét gebruiken

- `npuls/slides-preview/slideNN.png` — voorbeelden van de pptx-layouts, geen achtergronden; botsen met de slide-varianten hier.
- `npuls/web/sprite.svg` via `<use href="npuls/web/sprite.svg#…">`: Chrome blokkeert externe `<use>` bij `file://`. Bogen zet de frame daarom inline; iconen via Font Awesome.
- Verzonnen logo's of een nagetekend beeldmerk.
