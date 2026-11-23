# Changelog

## 0.3.0

- **`web/npuls.css`:** bevat nu de deckklassen `.s-*` (slide-varianten), `.card.<kleur>`, `.held.<kleur>` en `.ico.<kleur>`, gegenereerd uit `slide_roles`, `card_roles` en `tile_pairs` in de tokens. Ze stonden eerst in `cedapress/renderers/html/frame.html`. Nieuw: `.held.geel/.roze/.wit`, tekstkleur op alle kaarten, `.ico.roze` is blauw op roze (was zwart), `.s-blauw .quote` is geel. `allowed_combinations` bevat nu ook wit en de `licht-*`-tinten (nieuwe `.npuls-wit-*` en `.npuls-licht-*`-klassen).

## 0.2.1

- **Kleur:** wit op blauw is toegestaan (`allowed_combinations` in de tokens, besluit Aslam 2026-11-23). `web/npuls.css` heeft daardoor de nieuwe klasse `.npuls-blauw-wit`.
- **Kleur:** zwart staat niet meer als achtergrond in `allowed_combinations` (zwart is nooit een vlak). In `npuls.css` veranderde daardoor niets.

## 0.2.0

Let op: de illustraties uit het template hebben een nieuwe naam. Pakket 0.1.0 blijft ongewijzigd beschikbaar.

- **Hernoemd:** de 26 potx-illustraties heten niet meer `illustratie-NN.svg` maar hebben een betekenisvolle naam. De oude naam staat per bestand in `illustraties-mapping.json` (`oude_naam`). Oud naar nieuw: 01 `laptop-dashboard`, 02 `brein-ai-chip`, 03 `ai-chip`, 04 `atoom`, 05 `brein-tandwiel`, 06 `servers`, 07 `team-rond-idee`, 08 `boeken`, 09 `kalender`, 10 `handdruk`, 11 `gesprek`, 12 `afstudeerhoed`, 13 `videobellen`, 14 `samen-idee`, 15 `vr-bril`, 16 `presentator`, 17 `computer`, 18 `financien-analyse`, 19 `gloeilamp`, 20 `netwerk-blokken`, 21 `schoolgebouw`, 22 `werkplek-idee`, 23 `locatie`, 24 `verrekijker`, 25 `cadeau`, 26 `video`.
- **Nieuw in `illustraties/`:** 22 officiële SVG's van npuls.nl (kaart- en sectordoel-illustraties), herkomst per bestand in `illustraties-mapping.json`. `europa-ai.svg` en `ai-raamwerk.svg` bevatten een ingesloten raster.
- **Nieuw `tegels/`:** 10 gekleurde banner- en kaarttegels van npuls.nl, herkomst in `tegels-mapping.json`. `tegel-themas.svg` bevat de officiële lijnpictogrammen.
- **Nieuw `huisstijlgids/`:** `Npuls_huisstijlgids_2025.pdf`.
- **Nieuw `ceda/`:** `teamfoto.png` (CEDA-teamfoto). Het CEDA-logo volgt nog.
- **Bewust niet opgenomen:** het CTL-logo (programmalogo), foto's van echte mensen (Leerroutes, Communitys, Community) en duplicaten (zelfde afbeelding als een potx-illustratie, of dubbel op npuls.nl).

## 0.1.0

Eerste uitgave: PowerPoint-template, logo's, vormen, 26 illustraties uit het template (slide 18 en 19), slide-previews en `web/` (npuls.css, vormen, logos, sprite). Geen lettertypebestanden, zie `fonts.md`.

`web/npuls.css` wordt gegenereerd uit `vormgever-npuls-huisstijl/references/design-tokens.json` (`scripts/build-npuls-assets.sh`; `--check` in de lint-workflow faalt bij afwijking). Bevat alle neutrals, `--npuls-grijs` (layoutvlak) en cedapress-aliassen (`--licht-*`, `--font-primair/-secundair`).
