# Assets — vormgever-npuls-huisstijl

Kant-en-klare SVG's voor de Npuls huisstijl. Alle kleuren volgen `../references/design-tokens.json`. Gebruik deze bestanden vóór je nieuwe tekent.

## `shapes/` — de vijf kernvormen

| Bestand | Kernvorm | Betekenis |
|---------|----------|-----------|
| `pulse-curve.svg` | Pulse curve | dynamiek |
| `concentrische-ringen.svg` | Concentrische ringen | bron van impact, kenniscentrum |
| `chevron.svg` | Chevron / pijl | richting, vooruitgang |
| `starburst.svg` | Starburst | aandacht, nieuw |
| `boog.svg` | Boog / halfcirkel | verbinding, overgang |

Inzetbaar ter ondersteuning van een boodschap of decoratief als masker. Altijd in een toegestane kleurcombinatie (zie `allowed_combinations`).

## `logos/` — beeldmerk

| Bestand | Gebruik |
|---------|---------|
| `npuls_logo.jpg` | **officieel beeldmerk** met woordmerk (stippenkrans + "Npuls"), 200 × 200 px. De achtergrond van het bestand is `#F3D9DC`, vrijwel gelijk aan npuls-roze (`#F4D9DC`): gebruik het op npuls-roze (bijvoorbeeld een hero) en niet op wit |
| `beeldmerk.svg` | indicatief: pulserende stippen, donker — op lichte achtergrond |
| `beeldmerk-wit.svg` | indicatief: pulserende stippen, wit — op donkere/kleurvlak-achtergrond |

**Gebruik `npuls_logo.jpg` waar het logo zichtbaar is.** Het is het bestand uit de CEDA/Npuls-presentaties (`clidev-presentaties/public/npuls/`). Het is een JPG met roze achtergrond, geen vector en geen transparante versie; de SVG's zijn een benadering en alleen een noodoplossing. Vervang het door het bestand uit de Npuls-communicatiekit als daar een vector of transparante versie van beschikbaar is, en pas het niet zelf aan (zie licentie in `../references/merkcontext.md`). Clearspace: minimaal de hoogte van de letter "N" rondom.

## `illustrations/` — voorbeeld-illustraties

`collaboration.svg`, `data-insight.svg`, `learning.svg` — vlakke stijl met zwarte contour en paletkleuren. Bedoeld als startpunt/voorbeeld voor eigen illustraties, niet als vaste merk-assets.
