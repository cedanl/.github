# Toetsbare ontwerpregels — PowerPoint-decks

Vaste structuur per regel: **id · regel · meetbaar criterium · fancy-niveau · getoetst door**.
`ernst`: FOUT blokkeert export, WAARSCHUWING moet bekeken worden. Niveau "alle" = A, B en C.

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl.

Kleuren en lettertypen staan in `vormgever-npuls-huisstijl` (`design-tokens.json`) en worden hier met hun tokennaam genoemd (`npuls-blauw`, `licht-groen`, `General Sans`). Daar staan de hexwaarden; dit bestand herhaalt ze niet.

<!-- Open (TODO(Edwin)): zie onderaan "Nog open". Pas bij wijziging van een drempel ook
     cedapress/renderers/pptx/build.mjs (blok "spec controleren") aan. Status: Edwin verwerkt, 2026-11-23. -->

| id | Regel | Meetbaar criterium | Fancy | Getoetst door | Ernst |
|---|---|---|---|---|---|
| OPP-01 | Eén boodschap per slide | elke inhoudsslide heeft een `title` die die ene boodschap zegt | alle | build.mjs | FOUT |
| OPP-02 | Weinig tekst | zichtbare woorden per inhoudsslide ≤ 50 (richtlijn), waarschuwing boven 60; kaarttitel 1 tot 4 woorden, kaarttekst ≤ 20 woorden | alle | build.mjs (nu nog 70/90, aanpassen) | W |
| OPP-03 | Tekst past | geen "tekst past niet"-melding van de template-engine; los op door in te korten of te splitsen, niet door te verkleinen | alle | build_potx.py | W (oplossen) |
| OPP-04 | Notes overal | elke slide heeft `notes`; bronnen en voorbehoud staan daar ("Bron: ..."), met markering wat afgeleid is en niet letterlijk in de bron staat | alle | build.mjs (aanwezigheid); inhoud handmatig | W |
| OPP-05 | Leesbaar | kleinste tekst ≥ 9 pt (alleen labels, tags, eyebrows), bodytekst ≥ 11,5 pt, slidetitel 26 pt; groottes volgens de typografietabel hieronder | alle | build_potx.py (minimum per tekstvak) | W |
| OPP-06 | Alt-tekst | `image`/`video` hebben `alt` | alle | handmatig (TODO in build.mjs) | W |
| OPP-07 | Kleuren | alleen Npuls-kleurnamen (tokens), geen hex; elke slide toont minstens 3 primaire kleuren; `npuls-zwart` nooit als vlak of achtergrond, alleen voor tekst en iconen | alle | build.mjs | F / W |
| OPP-08 | Ritme | nooit twee keer dezelfde achtergrondtint achter elkaar; ongeveer de helft van de inhoudsslides wit, de rest licht (`licht-*`) | alle | build.mjs | W |
| OPP-09 | Vaste slides (optioneel) | de auteur kiest per deck (`vaste-slides: ja` of `nee` in `bron.md`). Met `ja`: één blok `ceda` → `team` → `contact` vóór de afsluiter; bij een onvolledig of verspreid blok, of een keuze die niet met de spec klopt, volgt een waarschuwing | alle | build.mjs | W |
| OPP-10 | Sober is sober | fancy A: alleen wit/licht, geen video | A | handmatig (TODO) | W |
| OPP-11 | Beeld | fancy B/C: ≥ 2 Npuls-illustraties in het deck | B, C | build.mjs | W |
| OPP-12 | Visueel gecontroleerd | elke gerenderde PNG bekeken; geen overloop of botsing | alle | render.mjs + handmatig | F |
| OPP-13 | Feiten kloppen | elk cijfer terug te vinden in de bronnen van `bron.md`; geen verzonnen cijfers, namen of citaten | alle | handmatig (audit vóór export) | F |
| OPP-14 | Banner/hero-patroon | zoals npuls.nl: effen vlak in één huisstijlkleur (`npuls-blauw`, `npuls-groen`, `npuls-oranje` of `npuls-roze`), daarop één illustratie met een ingebakken achtergrond in dezelfde kleur (zie OPP-23). Kant-en-klaar voorbeeld: `tegels/` in het assetpakket. Lijnpictogrammen in `tegels/tegel-themas.svg` zijn het officiële Npuls-alternatief voor icoontjes. | B, C | handmatig | W |
| OPP-15 | Formaat en raster | altijd 16:9, 10 × 5,625 in; marge links 0,55 in, rechts tot 9,45 in (inhoudsbreedte 8,9 in); tussenruimte kaarten 0,25 in horizontaal, 0,12 in verticaal; geen kleine tekst rechtsonder (ringen) | alle | build_potx.py / handmatig | F |
| OPP-16 | Vaste elementen uit de layout | label-pil linksboven (y 0,42), titel (y 0,80), optionele intro (y 1,36), inhoudszone y 1,70 tot 4,85 (met intro 1,85 tot 4,85), teller "nn / totaal" linksonder (y 5,20, 9 pt vet); niet zelf tekenen | alle | handmatig | W |
| OPP-17 | Titelformule | neutraal deel + accentdeel in kleur ("Wat levert het **op?**"), zinshoofdletter, geen punt, ≤ ± 45 tekens, op één regel | alle | build.mjs (lengte); rest handmatig | W |
| OPP-18 | Label-pil | 1 tot 3 woorden in KAPITALEN die de functie noemen (AANLEIDING, KERNVRAAG, WERKING, RESULTATEN, LESSEN, IN DE PRAKTIJK, OPROEP AAN DE SECTOR); mag "· naam" bevatten; zelfde kleur als het accentdeel van de titel | alle | handmatig (TODO build.mjs) | W |
| OPP-19 | Patroon en aantallen | één patroon per slide; 2 tot 4 kaarten, 3 tot 4 stappen of 3 tot 5 lijstitems; twee opeenvolgende inhoudsslides hebben niet hetzelfde patroon | alle | build.mjs (aantallen) | W |
| OPP-20 | Kleurcombinaties | alleen `allowed_combinations` uit de tokens (dus nooit geel op groen of groen op blauw); accent volgt de achtergrond: wit en `licht-blauw` geven `npuls-blauw`, `licht-groen` geeft `npuls-groen`, `licht-oranje` en `licht-geel` geven `npuls-oranje` | alle | handmatig (TODO build.mjs) | F |
| OPP-21 | Gekleurde kaarten | een volle kaartkleur (`npuls-blauw`, `npuls-groen`, `npuls-oranje`) alleen als nadruk: max. 1 tot 2 per slide, de rest wit of licht | alle | handmatig | W |
| OPP-22 | Iconen | altijd in een afgeronde icoontegel (0,42 in) in een paletkleur, nooit los; tegelparen (tegel/icoon) blauw/geel, geel/blauw, groen/roze, oranje/zwart, roze/blauw, afwisselen binnen één slide | alle | handmatig | W |
| OPP-23 | Illustraties | één illustratie per slide, alleen op een vlak in dezelfde kleur als de ingebakken achtergrond (deel-slide, heldenkaart of losse tegel); geen stockfoto's tenzij aangeleverd, geen foto's van publieke personen | alle | handmatig | W |
| OPP-24 | Vormentaal | afgeronde rechthoeken (kaarten), cirkels (stapnummers, stippen), pillen (labels); geen schaduwen, geen verlopen, geen randen | alle | handmatig | W |
| OPP-25 | Grafieken | native en bewerkbaar; kolom of staaf voor vergelijken, lijn voor trend, donut alleen voor 2 tot 4 delen van één geheel; kleurvolgorde blauw, oranje, groen, geel, roze (één reeks = blauw); altijd een kaart of titel die zegt wat opvalt; bron in notes | alle | handmatig | W |
| OPP-26 | Deckstructuur | opening (geel) → delen → oproep/vervolg of "Meer weten / Met dank aan" → optioneel blok vaste CEDA-slides (OPP-09) → afsluiting; opening: titel 54 pt vet, ondertitel 40 pt regular (vraag of belofte), 2 metaregels | alle | build.mjs | W |
| OPP-27 | Delen | elk deel: één deel-slide (pil "DEEL n", titel 40 pt, intro 18 pt Cooper, illustratie rechts) + 2 tot 4 inhoudsslides; max. 4 delen; kleurvolgorde `npuls-roze` → `npuls-oranje` → `npuls-groen` → `npuls-blauw` | alle | build.mjs | W |
| OPP-28 | Afsluiting | "Onderwijs **bewegen.**", CC BY-SA 4.0-tekst met naamsvermelding (waarop de inhoud gebaseerd is), Npuls-logo; logo en merkelementen niet wijzigen | alle | build.mjs / handmatig | F |
| OPP-29 | Tekst en toon | Nederlands, B1, actief en uitnodigend, korte zinnen (volgens `npuls-schrijfwijzer`); opening- en deeltitels kort en prikkelend | alle | handmatig | W |

## Typografie (OPP-05)

Primair `General Sans` (regular en semibold), secundair `Cooper Light` (tokens `typography`), alleen voor deel-intro's, citaten, de grote vraag in een heldenkaart, een open vraag en de afsluiter. Code: Courier New.

| Element | Grootte | Stijl |
|---|---|---|
| Openingstitel / ondertitel | 54 / 40 pt | vet / regular |
| Deel-titel | 40 pt | vet |
| Deel-intro | 18 pt | Cooper |
| Slidetitel | 26 pt | vet, accentdeel in kleur |
| Lead/kernzin | 19 pt | regular |
| Citaat | 27 pt | Cooper |
| Heldenkaart-tekst | 23 pt | Cooper |
| Kerncijfer | 44 pt | vet, `npuls-oranje` |
| Kaarttitel | 16 tot 20 pt | vet |
| Rijtekst / inzicht | 15 pt | regular |
| Kaart- en lijsttekst | 13 tot 14 pt | regular |
| Intro onder titel | 12 pt | regular |
| Toelichting in stap | 11,5 pt | regular |
| Labels, tags, eyebrows | 9 pt | vet, KAPITALEN, spatiëring |

Past het niet: tekst inkorten of over twee slides verdelen, nooit verkleinen.

## Nog open

- **build.mjs:** drempels in `renderers/pptx/build.mjs` staan nog op 70/90 woorden en 14 pt; de nieuwe waarden (OPP-02, OPP-05, OPP-15 tot OPP-28) zijn nog niet geautomatiseerd.
- **Iconen:** herkomst en licentie van Edwins iconenset zijn nog niet vastgesteld.
