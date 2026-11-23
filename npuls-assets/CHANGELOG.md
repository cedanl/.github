# Changelog

## 0.1.0

Eerste uitgave: PowerPoint-template, logo's, vormen, 26 illustraties uit het template (slide 18 en 19), slide-previews en `web/` (npuls.css, vormen, logos, sprite). Geen lettertypebestanden, zie `fonts.md`.

`web/npuls.css` wordt gegenereerd uit `vormgever-npuls-huisstijl/references/design-tokens.json` (`scripts/build-npuls-assets.sh`; `--check` in de lint-workflow faalt bij afwijking). Bevat alle neutrals, `--npuls-grijs` (layoutvlak) en cedapress-aliassen (`--licht-*`, `--font-primair/-secundair`).
