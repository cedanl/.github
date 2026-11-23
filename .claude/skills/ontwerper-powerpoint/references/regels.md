# Toetsbare ontwerpregels — PowerPoint-decks

Vaste structuur per regel: **id · regel · meetbaar criterium · fancy-niveau · getoetst door**.
`ernst`: FOUT blokkeert export, WAARSCHUWING moet bekeken worden. Niveau "alle" = A, B en C.

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl.

Kleuren en lettertypen staan in `vormgever-npuls-huisstijl` (`design-tokens.json`) en worden hier met hun tokennaam genoemd (`npuls-blauw`, `licht-groen`, `General Sans`). Daar staan de hexwaarden; dit bestand herhaalt ze niet.

<!-- Pas bij wijziging van een drempel ook cedapress/renderers/pptx/build.mjs (blok "spec controleren") en build_potx.py (MIN_BODY, MIN_LABEL) aan. -->

| id | Regel | Meetbaar criterium | Fancy | Getoetst door | Ernst |
|---|---|---|---|---|---|
| OPP-01 | Eén boodschap per slide | elke inhoudsslide heeft een `title` die die ene boodschap zegt | alle | build.mjs | FOUT |
| OPP-02 | Weinig tekst | zichtbare woorden per inhoudsslide ≤ 50 (richtlijn), waarschuwing boven 60 (build.mjs); kaarttitel 1 tot 4 woorden, kaarttekst ≤ 20 woorden | alle | build.mjs | W |
| OPP-03 | Tekst past | geen "tekst past niet"-melding van de template-engine; los op door in te korten of te splitsen, niet door te verkleinen | alle | build_potx.py | W (oplossen) |
| OPP-04 | Notes overal | elke slide heeft `notes`; bronnen en voorbehoud staan daar ("Bron: ..."), met markering wat afgeleid is en niet letterlijk in de bron staat | alle | build.mjs (aanwezigheid); inhoud handmatig | W |
| OPP-05 | Leesbaar | kleinste tekst ≥ 12 pt (alleen labels, tags, eyebrows), bodytekst ≥ 15 pt, slidetitel 40 pt uit de layout; groottes in potx-pt volgens de typografietabel hieronder (Edwin: 9 en 11,5 pt op 10 in) | alle | build_potx.py (minimum per tekstvak) | W |
| OPP-06 | Alt-tekst | `image`/`video` hebben `alt` | alle | handmatig (TODO in build.mjs) | W |
| OPP-07 | Kleuren | alleen Npuls-kleurnamen (tokens), geen hex; elke slide toont minstens 3 primaire kleuren; `npuls-zwart` nooit als vlak of achtergrond, alleen voor tekst en iconen | alle | build.mjs | F / W |
| OPP-08 | Ritme | nooit twee keer dezelfde achtergrondtint achter elkaar; ongeveer de helft van de inhoudsslides wit, de rest licht (`licht-*`) | alle | build.mjs | W |
| OPP-09 | Vaste slides (optioneel) | de auteur kiest per deck (`vaste-slides: ja` of `nee` in `bron.md`). Met `ja`: één blok `ceda` → `team` → `contact` vóór de afsluiter; bij een onvolledig of verspreid blok, of een keuze die niet met de spec klopt, volgt een waarschuwing | alle | build.mjs | W |
| OPP-10 | Sober is sober | fancy A: alleen wit/licht, geen video | A | handmatig (TODO) | W |
| OPP-11 | Beeld | fancy B/C: ≥ 2 Npuls-illustraties in het deck | B, C | build.mjs | W |
| OPP-12 | Visueel gecontroleerd | elke gerenderde PNG bekeken; geen overloop of botsing | alle | render.mjs + handmatig | F |
| OPP-13 | Feiten kloppen | elk cijfer terug te vinden in de bronnen van `bron.md`; geen verzonnen cijfers, namen of citaten | alle | handmatig (audit vóór export) | F |
| OPP-14 | Banner/hero-patroon | zoals npuls.nl: effen vlak in één huisstijlkleur (`npuls-blauw`, `npuls-groen`, `npuls-oranje` of `npuls-roze`), daarop één illustratie met een ingebakken achtergrond in dezelfde kleur (zie OPP-23). Kant-en-klaar voorbeeld: `tegels/` in het assetpakket. Lijnpictogrammen in `tegels/tegel-themas.svg` zijn het officiële Npuls-alternatief voor icoontjes. | B, C | handmatig | W |
| OPP-15 | Formaat en raster | altijd 16:9, potx 13,33 × 7,5 in (Edwin: 10 × 5,625 in, alles × 4/3); marge links en rechts 0,98 in uit de potx (inhoudsbreedte 11,37 in); tussenruimte kaarten ± 0,33 in horizontaal, 0,16 in verticaal; geen kleine tekst rechtsonder (ringen) | alle | build_potx.py / handmatig | F |
| OPP-16 | Vaste elementen uit de layout | label-pil linksboven (y 0,55), titel-placeholder uit de layout (y 0,99), optionele intro (y 1,66), inhoudszone y 1,85 tot 6,65 (met intro 2,35 tot 6,65); het inhoudsblok staat in het optische midden van die zone: 40 % van de vrije ruimte erboven, 60 % eronder (`OPTISCH` in build_potx.py, gelijk aan de HTML), dianummer linksonder uit de layout; niet zelf tekenen (Edwin, 10 in: pil y 0,42, titel 0,80, intro 1,36, zone 1,70 tot 4,85) | alle | handmatig | W |
| OPP-17 | Titelformule | neutraal deel + accentdeel in kleur ("Wat levert het **op?**"), zinshoofdletter, geen punt, ≤ ± 45 tekens, op één regel | alle | build.mjs (lengte); rest handmatig | W |
| OPP-18 | Label-pil | 1 tot 3 woorden in KAPITALEN die de functie noemen (AANLEIDING, KERNVRAAG, WERKING, RESULTATEN, LESSEN, IN DE PRAKTIJK, OPROEP AAN DE SECTOR); mag "· naam" bevatten; zelfde kleur als het accentdeel van de titel | alle | handmatig (TODO build.mjs) | W |
| OPP-19 | Patroon en aantallen | één patroon per slide; 2 tot 4 kaarten, 3 tot 4 stappen of 3 tot 5 lijstitems; twee opeenvolgende inhoudsslides hebben niet hetzelfde patroon | alle | build.mjs (aantallen) | W |
| OPP-20 | Kleurcombinaties | alleen `allowed_combinations` uit de tokens (dus nooit geel op groen of groen op blauw); accent volgt de achtergrond: wit en `licht-blauw` geven `npuls-blauw`, `licht-groen` geeft `npuls-groen`, `licht-oranje` en `licht-geel` geven `npuls-oranje`. Op verzadigde vlakken verschillen titel en accent altijd (anders is het accentdeel en de label-pil onzichtbaar): roze = titel zwart + accent blauw; groen = titel zwart + accent roze; blauw = titel roze + accent geel; oranje = titel zwart + accent roze; geel = titel zwart + accent blauw. Roze als tekst haalt op groen en oranje maar ca. 2,2:1: daar is het accentdeel een roze markering achter zwarte tekst (build_potx.py `MARKER`, HTML `.hl`). De label-pil heeft de accentkleur. Oranje op `licht-oranje` haalt maar ca. 2,5:1: alleen voor het titelaccent en groot display (kerncijfer), nooit voor kleine tekst | alle | build_potx.py (kleurparen per kaart en kerncijfer); rest handmatig | F |
| OPP-21 | Gekleurde kaarten | een volle kaartkleur (`npuls-blauw`, `npuls-groen`, `npuls-oranje`) alleen als nadruk: max. 1 tot 2 per slide, de rest wit of licht | alle | build_potx.py (waarschuwing bij meer dan 2 volle kaartkleuren) | W |
| OPP-22 | Iconen | altijd in een afgeronde icoontegel (0,56 in; Edwin 0,42 in op 10 in) in een paletkleur, nooit los; tegelparen (tegel/icoon) blauw/geel, geel/blauw, groen/roze, oranje/zwart, roze/blauw, afwisselen binnen één slide | alle | handmatig | W |
| OPP-23 | Illustraties | één illustratie per slide, alleen op een vlak in dezelfde kleur als de ingebakken achtergrond (deel-slide, heldenkaart of losse tegel); geen stockfoto's tenzij aangeleverd, geen foto's van publieke personen | alle | handmatig | W |
| OPP-24 | Vormentaal | afgeronde rechthoeken (kaarten), cirkels (stapnummers, stippen), pillen (labels); geen schaduwen, geen verlopen, geen randen | alle | handmatig | W |
| OPP-25 | Grafieken | native en bewerkbaar; kolom of staaf voor vergelijken, lijn voor trend, donut alleen voor 2 tot 4 delen van één geheel; kleurvolgorde blauw, oranje, groen, geel, roze (één reeks = blauw); altijd een kaart of titel die zegt wat opvalt; bron in notes | alle | handmatig | W |
| OPP-26 | Deckstructuur | opening (roze, titelslide van de potx) → delen → oproep/vervolg of "Meer weten / Met dank aan" → optioneel blok vaste CEDA-slides (OPP-09) → afsluiting; opening: titel 54 pt vet, ondertitel 40 pt regular (vraag of belofte), 2 metaregels | alle | build.mjs | W |
| OPP-27 | Delen | elk deel: één deel-slide (pil "DEEL n", titel 40 pt, intro 18 pt Cooper, illustratie rechts) + 2 tot 4 inhoudsslides; max. 4 delen; kleurvolgorde `npuls-roze` → `npuls-oranje` → `npuls-groen` → `npuls-blauw` | alle | build.mjs | W |
| OPP-28 | Afsluiting | "Onderwijs **bewegen.**", CC BY-SA 4.0-tekst met naamsvermelding (waarop de inhoud gebaseerd is), Npuls-logo; logo en merkelementen niet wijzigen | alle | build.mjs / handmatig | F |
| OPP-29 | Tekst en toon | Nederlands, B1, actief en uitnodigend, korte zinnen (volgens `npuls-schrijfwijzer`); opening- en deeltitels kort en prikkelend | alle | handmatig | W |

## Typografie (OPP-05)

Primair `General Sans` (regular en semibold), secundair `Cooper Light` (tokens `typography`), alleen voor deel-intro's, citaten, de grote vraag in een heldenkaart, een open vraag en de afsluiter. Code: Courier New.

Alle groottes staan in pt op de potx (13,33 × 7,5 in). Edwins waarden voor een dia van 10 in zijn met 4/3 omgerekend. Waar de potx-layout een eigen grootte heeft (titelslide, deel-slide, titel-placeholder), gaat de layout voor.

| Element | Grootte (potx) | Edwin op 10 in | Stijl |
|---|---|---|---|
| Openingstitel / ondertitel | volgens layout Titeldia | 54 / 40 pt | vet / regular |
| Deel-titel | volgens layout Sectiescheider | 40 pt | vet |
| Deel-intro | 24 pt | 18 pt | Cooper |
| Slidetitel | 40 pt uit de layout, krimpt tot 24 pt | 26 pt | vet, accentdeel in kleur |
| Lead/kernzin | 25 pt | 19 pt | regular |
| Citaat | 36 pt | 27 pt | Cooper |
| Heldenkaart-tekst | 31 pt | 23 pt | Cooper |
| Kerncijfer | 59 pt | 44 pt | vet, `npuls-oranje` |
| Kaarttitel | 21 tot 27 pt | 16 tot 20 pt | vet |
| Rijtekst / inzicht | 20 pt | 15 pt | regular |
| Kaart- en lijsttekst | 17 tot 19 pt | 13 tot 14 pt | regular |
| Intro onder titel | 16 pt | 12 pt | regular |
| Toelichting in stap | minimaal 15 pt | 11,5 pt | regular |
| Labels, tags, eyebrows | minimaal 12 pt | 9 pt | vet, KAPITALEN, spatiëring |

Minimum (OPP-05): bodytekst ≥ 15 pt (11,5 × 4/3 = 15,3, afgerond), labels ≥ 12 pt (9 × 4/3). `build_potx.py` trekt kleinere groottes op en waarschuwt als de tekst dan niet past. Past het niet: tekst inkorten of over twee slides verdelen, nooit verkleinen.

## Nog open

- **Iconen:** herkomst en licentie van Edwins iconenset zijn nog niet vastgesteld. De icoontegel werkt al met `iconen/<naam>.svg` uit het assetpakket; zonder set blijft de tegel leeg en volgt een waarschuwing.
- **Nog niet geautomatiseerd in build.mjs:** OPP-06 (alt-tekst), OPP-10, OPP-20 (kleurcombinaties per slide, wel per kaart), OPP-26 en OPP-27 (deckstructuur, delen).
