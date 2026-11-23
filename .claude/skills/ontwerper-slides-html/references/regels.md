# Toetsbare ontwerpregels — HTML-decks

Vaste structuur per regel: **id · regel · meetbaar criterium · fancy-niveau · getoetst door**.
`ernst`: FOUT blokkeert export, WAARSCHUWING moet bekeken worden. Niveau "alle" = A, B en C.

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl. Alleen het deel dat los staat van het medium is overgenomen (OSH-17 en hoger, plus aangepaste OSH-02, 03, 04, 08, 13, 14, 16). Kleuren en lettertypen staan in `vormgever-npuls-huisstijl` (`design-tokens.json`) en worden met hun tokennaam genoemd.

<!-- Pas bij wijziging van een drempel ook cedapress/renderers/html/check.mjs (blok "11. Ontwerpregels") aan. -->

| id | Regel | Meetbaar criterium | Fancy | Getoetst door | Ernst |
|---|---|---|---|---|---|
| OSH-01 | Eén boodschap per slide | ≤ 1 `h2` per inhoudsslide | alle | check.mjs | FOUT |
| OSH-02 | Weinig tekst | zichtbare woorden per inhoudsslide ≤ 50 (richtlijn), waarschuwing boven 50, fout boven 90; notes en vaste slides tellen niet; kaarttitel 1 tot 4 woorden, kaarttekst ≤ 20 woorden (niet geautomatiseerd) | alle | check.mjs | W / F |
| OSH-03 | Kop is een korte bewering | kop ≤ 12 woorden en ≤ ± 45 tekens, formule uit OSH-17 | alle | check.mjs (lengte); bewering: handmatig | W |
| OSH-04 | Korte lijsten | 3 tot 5 punten per `ul`/`ol` | alle | check.mjs | W |
| OSH-05 | Leesbaar op de beamer | kleinste gerenderde tekst ≥ 18 px op 1920×1080; niets onder de navigatie of buiten beeld | alle | qa.mjs (overflow); minimale grootte: TODO | F |
| OSH-06 | Alt-tekst | elke `img` heeft een `alt`-attribuut (`alt=""` = decoratie) | alle | check.mjs | FOUT |
| OSH-07 | Inhoud nooit alleen via animatie | met animatie uit (qa/PDF) is alle inhoud zichtbaar | alle | qa.mjs (screenshots zonder animatie) + handmatig | F |
| OSH-08 | Kleurcombinaties | alleen slide-varianten `s-*`; geen hex buiten `:root`; elke slide toont minstens 3 primaire kleuren; `npuls-zwart` nooit als vlak of achtergrond | alle | check.mjs (huisstijl) | FOUT |
| OSH-09 | Duur past | inhoudsslides ≈ `duur` / 2 (± 30 %) | alle | handmatig (TODO in check) | W |
| OSH-10 | Sober is sober | fancy A: geen `data-a/-count/-draw/-pop/-grow` | A | check.mjs | FOUT |
| OSH-11 | Huisstijl+ herkenbaar | fancy B/C: bogen rechtsonder op ≥ 2 slides; Npuls-logo linksboven op titel en contact (frame) | B, C | check.mjs (bogen) | W |
| OSH-12 | Rijk is beeldend | fancy C: ≥ 3 Npuls-illustraties | C | check.mjs | W |
| OSH-13 | Ritme | niet 2× achter elkaar dezelfde variant of achtergrondtint; ongeveer de helft van de inhoudsslides wit | alle | check.mjs (huisstijl) | W |
| OSH-14 | Verhaallijn | > 8 inhoudsslides → max. 4 delen (`data-deel`), elk met 2 tot 4 inhoudsslides | alle | check.mjs (aantal delen) | W |
| OSH-15 | Feiten kloppen | elk cijfer en elke bewering terug te vinden in de bronnen van `bron.md` | alle | handmatig (audit vóór export) | F |
| OSH-16 | Banner/hero-patroon | Banner/hero-patroon zoals npuls.nl: effen vlak in één huisstijlkleur (blauw, groen, oranje of roze), daarop één illustratie met een ingebakken achtergrond in dezelfde kleur (zie OSH-22), eventueel met een dunne witte cirkellijn erachter. Kant-en-klaar voorbeeld: `tegels/` in het assetpakket. Lijnpictogrammen in `tegels/tegel-themas.svg` zijn het officiële Npuls-alternatief voor icoontjes. | B, C | handmatig | W |
| OSH-17 | Titelformule | neutraal deel + accentdeel in kleur ("Wat levert het **op?**"), zinshoofdletter, geen punt, op één regel | alle | handmatig | W |
| OSH-18 | Label | 1 tot 3 woorden in KAPITALEN die de functie van de slide noemen (AANLEIDING, KERNVRAAG, RESULTATEN, OPROEP); zelfde kleur als het accentdeel van de titel | alle | handmatig | W |
| OSH-19 | Kleurcombinaties | alleen `allowed_combinations` uit de tokens (nooit geel op groen of groen op blauw); accent volgt de achtergrond: wit en `licht-blauw` geven `npuls-blauw`, `licht-groen` geeft `npuls-groen`, `licht-oranje` en `licht-geel` geven `npuls-oranje`; op roze en groen is de titel zwart met accent blauw (roze) of roze (groen); op groen en oranje is het accentdeel een roze markering achter zwarte tekst (roze als tekst haalt daar maar ca. 2,2:1); de inhoud staat in het optische midden onder de titel (40 % van de vrije ruimte erboven, 60 % eronder); oranje op `licht-oranje` haalt ca. 2,5:1 en is alleen voor het titelaccent en groot display (kerncijfer), nooit voor kleine tekst; een volle kaartkleur max. 1 tot 2 per slide | alle | handmatig (TODO check.mjs) | F |
| OSH-20 | Typografische hiërarchie | van groot naar klein: deck-/deeltitel, slidetitel, lead, kaarttitel, tekst, label; `General Sans` voor alles, `Cooper Light` alleen voor intro's, citaten, de grote vraag en de afsluiter; kerncijfer vet in `npuls-oranje` | alle | handmatig | W |
| OSH-21 | Iconen | altijd in een afgeronde tegel in een paletkleur, nooit los; tegelparen blauw/geel, geel/blauw, groen/roze, oranje/zwart, roze/blauw, afwisselen binnen één slide | alle | handmatig | W |
| OSH-22 | Illustraties | één illustratie per slide, alleen op een vlak in dezelfde kleur als de ingebakken achtergrond; geen stockfoto's tenzij aangeleverd, geen foto's van publieke personen | alle | handmatig | W |
| OSH-23 | Vormentaal | afgeronde rechthoeken, cirkels, pillen; geen schaduwen, geen verlopen, geen randen | alle | handmatig | W |
| OSH-24 | Deckstructuur | opening → delen (kleurvolgorde `npuls-roze` → `npuls-oranje` → `npuls-groen` → `npuls-blauw`) → oproep/vervolg → optioneel blok vaste CEDA-slides (Wie is CEDA, Wie zijn wij, Blijf in contact; de auteur kiest met `vaste-slides: ja` of `nee` in `bron.md`) → afsluiting "Onderwijs **bewegen.**" met CC BY-SA 4.0 en naamsvermelding | alle | handmatig | W |
| OSH-25 | Tekst en toon | Nederlands, B1, actief en uitnodigend, korte zinnen (`npuls-schrijfwijzer`); bronnen en voorbehoud in de notes, met markering wat afgeleid is | alle | handmatig | W |
| OSH-26 | Grafieken | kleurvolgorde blauw, oranje, groen, geel, roze (één reeks = blauw); altijd een kaart of titel die zegt wat opvalt | alle | handmatig | W |

## Nog open

- **OSH-05:** minimale lettergrootte blijft 18 px op 1920×1080. Edwins waarden (9 pt label, 11,5 pt body op een dia van 10 inch, omgerekend naar potx 12 en 15 pt) gelden voor pptx en worden niet omgerekend naar een schermgrootte. Edwin moet de HTML-ondergrens bevestigen (TODO(Edwin)).
- **Nog niet geautomatiseerd in check.mjs:** OSH-08 (3 primaire kleuren is er wel), OSH-13, OSH-14 (aantal delen is er wel), OSH-17 tot OSH-26 (formule, label, kleurcombinaties, iconen, illustraties).
- **Iconen:** HTML gebruikt Font Awesome (tokens); de pptx wacht op een iconenset in het assetpakket (herkomst en licentie van Edwins set onbekend).
