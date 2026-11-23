# Npuls-assets

Versioned pakket met officiele Npuls-assets (PowerPoint, HTML-decks, webpagina's). Wordt als GitHub-release uitgebracht op `cedanl/.github` onder tag `npuls-assets-vX.Y.Z`.

## Inhoud en herkomst

| Map of bestand | Wat | Bron |
|---|---|---|
| `pptx/Npuls_powerpoint-template.potx` | PowerPoint-template | Npuls-communicatiekit |
| `illustraties/` | 26 illustraties (SVG), `illustratie-NN.svg` | potx slide 18 en 19 (leesvolgorde); herkomst per bestand in `illustraties-mapping.json` |
| `vormen/` | Vormen en tegels (SVG), o.a. `bogen.svg` | Npuls-communicatiekit; identiek aan de graphics in de slideLayouts van de potx |
| `logos/` | Logo's en beeldmerken (PNG), logo op roze (JPG) | Npuls-communicatiekit |
| `slides-preview/` | PNG-previews van de templateslides | uit het template |
| `web/` | Voor HTML: `npuls.css`, `sprite.svg`, geoptimaliseerde `vormen/` en `logos/` | `npuls.css` gegenereerd uit `design-tokens.json` (`scripts/gen_npuls_css.py`, niet met de hand bewerken); rest afgeleid van bovenstaande |
| `fonts.md` | Lettertypen en licenties (geen losse fontbestanden; de potx heeft ze ingesloten) | |
| `manifest.json` | Versie en alle bestanden met sha256 | gegenereerd |

De potx-illustraties hebben geen betekenisvolle namen (shapes heten "Graphic NN"), vandaar de nummering.

## Gebruiken en pinnen

Pin altijd een vaste versie. De helper in de skill `vormgever-npuls-huisstijl` haalt het pakket op en cachet het in `~/.cache/ceda/npuls-assets/<versie>/`:

```bash
python .claude/skills/vormgever-npuls-huisstijl/scripts/npuls_assets.py ensure --version 0.1.0
python .claude/skills/vormgever-npuls-huisstijl/scripts/npuls_assets.py path web/npuls.css
```

Handmatig: `https://github.com/cedanl/.github/releases/download/npuls-assets-v0.1.0/npuls-assets-0.1.0.zip`.

## Uitbrengen

1. Pas bestanden aan, verhoog `VERSION` en vul `CHANGELOG.md`.
2. Draai `scripts/build-npuls-assets.sh` lokaal om te controleren.
3. Push tag `npuls-assets-vX.Y.Z`: de workflow `npuls-assets-release.yml` bouwt de zip en maakt de release.

Wie brengt uit: nog te bepalen (TBD).
