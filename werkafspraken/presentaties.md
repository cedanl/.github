# Presentaties

**Niveau:** Verplicht · **Eigenaar:** [@EdwinLieftink](https://github.com/EdwinLieftink) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Wat je namens CEDA presenteert maak je met Slidev in [clidev-presentaties](https://github.com/cedanl/clidev-presentaties), in de Npuls-huisstijl.

## Waarom

- **De huisstijl zit in `style.css`**, niet in jouw kopie van een deck. Eén aanpassing werkt door in alle presentaties.
- **Decks staan in git.** Ze zijn terug te vinden, te hergebruiken en te reviewen zoals code.
- **Tekst-diff in plaats van een binair bestand.** Je ziet wat er tussen twee versies is veranderd.
- **Slides naast de rest van het werk.** Een sprint review of webinar bouw je met dezelfde tooling als waarin je werkt.

## In de praktijk

**Naamgeving.** `YYMMDD_onderwerp_naam.md`, bijvoorbeeld `260311_leeranalytics_mbo.md`. Underscores tussen de woorden, twee à drie woorden — geen halve zin in de bestandsnaam.

**Presenteren met twee schermen.** Je wilt je notities zien zonder dat het publiek ze ziet. Dat gaat via twee browservensters op dezelfde dev-server:

1. Start de presentatie: `npx slidev <bestand>.md --open`.
2. Venster 1 is de gewone weergave. Sleep dat naar de beamer en zet het fullscreen met `f`. Dit ziet het publiek.
3. Open een tweede venster in presenter-mode: klik de presenter-knop in het navigatiepaneel (verschijnt als je linksonder in beeld hovert), of zet `/presenter` achter de URL. Dit venster houd je op je laptop.
4. Je ziet nu notities, de volgende slide en een timer. Doorklikken in presenter-mode synct het beamer-venster automatisch — je hoeft niets dubbel te doen.

**Notities.** Zet ze als HTML-comment onderaan een slide:

```markdown
# Mijn slide

Inhoud

<!-- Dit is een notitie, zichtbaar in presenter-mode -->
```

Alleen een comment aan het *einde* van een slide telt als notitie.

**Klikken vanaf je telefoon.** Start met `--remote` en open de URL op je toestel. Handig als je niet aan je laptop vastgeplakt wilt staan.

**Delen achteraf.** `npx slidev export <bestand>.md` maakt een PDF. Moet het per se PowerPoint zijn: `npx slidev export <bestand>.md --format pptx`.

**Assets.** Screenshots en afbeeldingen voor een deck komen in `public/presentations/YYMMDD_onderwerp_naam/`.

**Vastgelopen?** Gebruik `/clidev` — die skill zet het project op, kiest het juiste template en kent de huisstijlcomponenten.

## Achtergrond

- [Slidev — Presenter Mode](https://sli.dev/guide/ui#presenter-mode) — de officiële uitleg van het twee-vensters-model.
- [Slidev — Remote Access](https://sli.dev/features/remote-access) — waarom `--remote` bestaat en waar je op moet letten als je het aanzet.
- [Npuls huisstijl-skill](https://github.com/cedanl/.github/tree/main/.claude/skills/npuls-huisstijl) — de bron voor kleuren, typografie en vormentaal; `style.css` in clidev-presentaties is daar de uitwerking van.

## Afwijken

Een deck dat je samen met externen of Npuls-collega's maakt, hoeft niet per se in Slidev — dat loopt in overleg met [@EdwinLieftink](https://github.com/EdwinLieftink).
