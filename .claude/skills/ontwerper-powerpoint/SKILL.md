---
name: ontwerper-powerpoint
description: Ontwerpregels voor PowerPoint-decks van CEDA/Npuls — tekst per slide, verhaallijn, notes, leesbaarheid, toegankelijkheid, bewerkbaarheid, fancy-schaal A/B/C. Gebruik bij het ontwerpen of beoordelen van een pptx-deck. Niet voor het bouwen zelf (dat doet `cedapress`) en niet voor kleuren of de template (dat is `vormgever-npuls-huisstijl`).
allowed-tools: Read
metadata:
  ceda-id: ceda.ontwerper-powerpoint
  ceda-version: "0.3.0"
  ceda-type: reference
  ceda-subtype: knowledge
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: "cedanl/clidev-presentaties#15 en #16; powerclaude 0.3.0 (build-checks)"
  ceda-activation: chained
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Ontwerper — PowerPoint

Best practices voor pptx-decks op de officiële Npuls-template. `cedapress` raadpleegt deze skill vóór het
schrijven van de deck-spec en toetst met `renderers/pptx/build.mjs` (spec-checks) en `render.mjs` (beeld).
Huisstijl en template komen uit `vormgever-npuls-huisstijl`.

**Toetsbare regels:** `references/regels.md` (id, regel, meetbaar criterium, fancy-niveau, waar getoetst).

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl.

**Taakverdeling (besluit Aslam):** de officiële Npuls-potx en de tokens zijn vast (beheer: `vormgever-npuls-huisstijl` en `npuls-assets`; layouts, kleuren, fonts, logo's, vormen, illustraties). Wat in deze skill staat beheert Edwin en is flexibel (componenten, slidepatronen, drempels, kleurkeuze per slide, deckstructuur), zolang het binnen de potx-layouts en tokens blijft. Ontbrekende assets komen via een nieuwe assetrelease. Achtergrond: pitch cedanl/clidev-presentaties#16.

> Open punten staan onder "Nog open" in `references/regels.md`.

## Kern

1. **Eén boodschap per slide**, titel is een bewering. Max ~50 woorden zichtbaar; meer → splitsen of notes. Titel: neutraal deel + accentdeel, max ~45 tekens.
2. **Notes op elke slide:** wat de spreker zegt, niet wat er al staat. Een pptx wordt vaak zonder spreker gelezen;
   de notes dragen dan het verhaal.
3. **Bewerkbaar blijven:** echte tekstvakken, native tabellen en grafieken, layouts uit de template. Geen tekst in
   afbeeldingen. Collega's moeten bij "Nieuwe dia" de Npuls-layouts krijgen.
4. **Statisch denken:** wat in HTML een animatie of klik is, wordt in pptx een extra slide of een statische
   grafiek (`::: pptx`-blok in de bron). Geen PowerPoint-animaties tenzij de gebruiker erom vraagt.
5. **Leesbaar:** 16:9, body ≥ 15 pt, labels ≥ 12 pt (potx-pt; Edwin: 11,5 en 9 pt op 10 in), slidetitel 40 pt uit de layout; liever splitsen dan verkleinen.
6. **Toegankelijk:** alt-tekst bij afbeeldingen, leesvolgorde = layoutvolgorde, alleen toegestane kleurcombinaties, zwart nooit als vlak.
7. **Ontvangers zonder Npuls-fonts zien Calibri:** stuur ook de PDF.

## Fancy-schaal

| Niveau | Wat in pptx |
|---|---|
| **A sober** | Witte inhoudsslides, tekst/tabel/grafiek, hooguit één illustratie per slide |
| **B huisstijl+** (standaard) | A + verzadigde sectiescheiders, kaarten en kerncijfers, ≥ 2 illustraties in het deck |
| **C rijk** | B + video, meer illustraties, citaat- en beeldslides |

Logo linksboven en de bogen rechtsonder zitten al in de template; fancy gaat hier vooral over variatie in
slidetypes en beeld, nooit over eigen kleuren of eigen layouts.
