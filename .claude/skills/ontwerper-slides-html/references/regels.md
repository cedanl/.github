# Toetsbare ontwerpregels — HTML-decks

Vaste structuur per regel: **id · regel · meetbaar criterium · fancy-niveau · getoetst door**.
`ernst`: FOUT blokkeert export, WAARSCHUWING moet bekeken worden. Niveau "alle" = A, B en C.

<!-- TODO(Edwin): drempels en ontbrekende regels vanuit ontwerp/communicatie. Pas bij wijziging ook
     cedapress/renderers/html/check.mjs (blok "11. Ontwerpregels") aan. Status: eerste versie CEDA, 2026-11-19. -->

| id | Regel | Meetbaar criterium | Fancy | Getoetst door | Ernst |
|---|---|---|---|---|---|
| OSH-01 | Eén boodschap per slide | ≤ 1 `h2` per inhoudsslide | alle | check.mjs | FOUT |
| OSH-02 | Weinig tekst | zichtbare woorden per inhoudsslide ≤ 60 (waarschuwing), ≤ 90 (fout); notes en vaste slides tellen niet | alle | check.mjs | W / F |
| OSH-03 | Kop is een korte bewering | kop ≤ 12 woorden | alle | check.mjs (lengte); bewering: handmatig | W |
| OSH-04 | Korte lijsten | ≤ 5 punten per `ul`/`ol` | alle | check.mjs | W |
| OSH-05 | Leesbaar op de beamer | kleinste gerenderde tekst ≥ 18 px op 1920×1080; niets onder de navigatie of buiten beeld | alle | qa.mjs (overflow); minimale grootte: TODO | F |
| OSH-06 | Alt-tekst | elke `img` heeft een `alt`-attribuut (`alt=""` = decoratie) | alle | check.mjs | FOUT |
| OSH-07 | Inhoud nooit alleen via animatie | met animatie uit (qa/PDF) is alle inhoud zichtbaar | alle | qa.mjs (screenshots zonder animatie) + handmatig | F |
| OSH-08 | Kleurcombinaties | alleen slide-varianten `s-*`; geen hex buiten `:root`; ≥ 3 primaire kleuren in het deck | alle | check.mjs (huisstijl) | FOUT |
| OSH-09 | Duur past | inhoudsslides ≈ `duur` / 2 (± 30 %) | alle | handmatig (TODO in check) | W |
| OSH-10 | Sober is sober | fancy A: geen `data-a/-count/-draw/-pop/-grow` | A | check.mjs | FOUT |
| OSH-11 | Huisstijl+ herkenbaar | fancy B/C: bogen rechtsonder op ≥ 2 slides; Npuls-logo linksboven op titel en contact (frame) | B, C | check.mjs (bogen) | W |
| OSH-12 | Rijk is beeldend | fancy C: ≥ 3 Npuls-illustraties | C | check.mjs | W |
| OSH-13 | Ritme | niet 3× achter elkaar dezelfde variant | alle | check.mjs (huisstijl) | W |
| OSH-14 | Verhaallijn | > 8 inhoudsslides → 3 à 5 delen (`data-deel`) | alle | check.mjs (aantal delen) | W |
| OSH-15 | Feiten kloppen | elk cijfer en elke bewering terug te vinden in de bronnen van `bron.md` | alle | handmatig (audit vóór export) | F |
