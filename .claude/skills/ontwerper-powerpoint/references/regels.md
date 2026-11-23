# Toetsbare ontwerpregels — PowerPoint-decks

Vaste structuur per regel: **id · regel · meetbaar criterium · fancy-niveau · getoetst door**.
`ernst`: FOUT blokkeert export, WAARSCHUWING moet bekeken worden. Niveau "alle" = A, B en C.

<!-- TODO(Edwin): drempels en ontbrekende regels vanuit ontwerp/communicatie. Pas bij wijziging ook
     cedapress/renderers/pptx/build.mjs (blok "spec controleren") aan. Status: eerste versie CEDA, 2026-11-19. -->

| id | Regel | Meetbaar criterium | Fancy | Getoetst door | Ernst |
|---|---|---|---|---|---|
| OPP-01 | Eén boodschap per slide | elke inhoudsslide heeft een `title` | alle | build.mjs | FOUT |
| OPP-02 | Weinig tekst | zichtbare woorden per slide ≤ 70 (richtlijn), waarschuwing boven 90 | alle | build.mjs | W |
| OPP-03 | Tekst past | geen "tekst past niet"-melding van de template-engine | alle | build_potx.py | W (oplossen) |
| OPP-04 | Notes overal | elke slide heeft `notes` | alle | build.mjs | W |
| OPP-05 | Leesbaar | body ≥ 14 pt, koppen ≥ 24 pt na passend maken | alle | build_potx.py (minimum per tekstvak) | W |
| OPP-06 | Alt-tekst | `image`/`video` hebben `alt` | alle | handmatig (TODO in build.mjs) | W |
| OPP-07 | Kleuren | alleen Npuls-kleurnamen, geen hex; ≥ 3 primaire kleuren zichtbaar | alle | build.mjs | F / W |
| OPP-08 | Ritme | niet 2× achter elkaar dezelfde verzadigde variant | alle | build.mjs | W |
| OPP-09 | Vaste slides | `ceda` na titel, `team` na `ceda`, eindigen met `contact` | alle | build.mjs | W |
| OPP-10 | Sober is sober | fancy A: alleen wit/licht, ≤ 1 illustratie per slide, geen video | A | handmatig (TODO) | W |
| OPP-11 | Beeld | fancy B/C: ≥ 2 Npuls-illustraties in het deck | B, C | build.mjs | W |
| OPP-12 | Visueel gecontroleerd | elke gerenderde PNG bekeken; geen overloop of botsing | alle | render.mjs + handmatig | F |
| OPP-13 | Feiten kloppen | elk cijfer terug te vinden in de bronnen van `bron.md` | alle | handmatig (audit vóór export) | F |
| OPP-14 | Banner/hero-patroon | Banner/hero-patroon zoals npuls.nl: effen vlak in één huisstijlkleur (blauw, groen, oranje of roze), daarop één illustratie, eventueel met een dunne witte cirkellijn erachter. Kant-en-klaar voorbeeld: `tegels/` in het assetpakket. Lijnpictogrammen in `tegels/tegel-themas.svg` zijn het officiële Npuls-alternatief voor icoontjes. | B, C | handmatig | W |
