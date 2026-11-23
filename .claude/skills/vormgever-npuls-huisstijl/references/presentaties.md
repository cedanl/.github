# Npuls-regels voor presentaties

**Beheer: Edwin.** De Npuls-afspraken voor decks (kleurrollen per achtergrond, tegelparen, vormentaal, grafiekvolgorde, opening en afsluiter, label-pil) staan hier en in `design-tokens.json`, en nergens anders. Edwin beheert dit bestand; de exacte kleurwaarden en rollen staan in de tokens (beheer vormgever).

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl. De algemene ontwerpregels (één boodschap, weinig tekst, leesbaarheid, ritme) staan in `ontwerper-powerpoint` en `ontwerper-slides-html`; die verwijzen voor kleur en vorm naar dit bestand. De regelnummers (OPP-xx, OSH-xx) blijven gelijk, zodat waarschuwingen in `cedapress` kloppen.

## Hoe dit werkt

- **`design-tokens.json`** is de enige bron van waarden: `slide_roles` (per achtergrond: `title`, `text`, `accent`, `accent_2`, `quote`, `marker`, `title_highlight`, `cards`, `deco`), `card_roles`, `tile_pairs`, `badge_fg`, `tints`, `component_defaults`, `colors.allowed_combinations` en `data_visualization`.
- **`cedapress`** leest alleen dit bestand en `design-tokens.json` en kopieert niets: de PowerPoint-bouwer leest de tokens via `renderers/pptx/lib/tokens.mjs`, de HTML-frame gebruikt de klassen `.s-*`, `.card.<kleur>`, `.held.<kleur>` en `.ico.<kleur>` uit `web/npuls.css`, gegenereerd uit dezelfde tokens (`scripts/gen_npuls_css.py`).
- **Een kleurafspraak wijzigen** (bijvoorbeeld de titelkleur op blauw): pas één regel in `design-tokens.json` aan, draai `bash scripts/build-npuls-assets.sh` (regenereert `npuls.css`) en maak een assetrelease; hoog daarna de pins op (`cedapress/assets.lock`, `DEFAULT_VERSION` in `scripts/npuls_assets.py`). Geen andere bestanden.
- **Een kleurrol die niet in de tokens staat** geeft een FOUT: `build.mjs` (pptx) en `check.mjs` (HTML) controleren dat elke gebruikte kleur en kleurklasse in de tokens staat.

## Kleurrollen per achtergrond (OPP-20, OSH-19)

- Alleen `allowed_combinations` uit de tokens (dus nooit geel op groen of groen op blauw).
- Het accent volgt de achtergrond: wit en `licht-blauw` geven `npuls-blauw`, `licht-groen` geeft `npuls-groen`, `licht-oranje` en `licht-geel` geven `npuls-oranje`.
- Op verzadigde vlakken verschillen titel en accent altijd (anders is het accentdeel en de label-pil onzichtbaar): roze = titel zwart + accent blauw; groen = titel zwart + accent roze; blauw = titel wit + accent geel; oranje = titel zwart + accent roze; geel = titel zwart + accent blauw. Op wit en `licht-*` volgt de titel de layout (zwart) en kleurt alleen het accentdeel.
- Roze als tekst haalt op groen en oranje maar ca. 2,2:1: daar is het accentdeel een roze markering achter zwarte tekst (token `title_highlight`).
- De label-pil heeft de accentkleur (zie Label-pil).
- Oranje op `licht-oranje` haalt maar ca. 2,5:1: alleen voor het titelaccent en groot display (kerncijfer), nooit voor kleine tekst.
- De inhoud staat in het optische midden onder de titel: 40 % van de vrije ruimte erboven, 60 % eronder.
- Een volle kaartkleur (`npuls-blauw`, `npuls-groen`, `npuls-oranje`) alleen als nadruk: max. 1 tot 2 per slide, de rest wit of licht (OPP-21).
- Getoetst door: `build_potx.py` (kleurparen per kaart en kerncijfer; waarschuwing bij meer dan 2 volle kaartkleuren), `build.mjs` en `check.mjs` (kleur of kleurrol buiten de tokens); rest handmatig.

## Tegelparen voor iconen (OPP-22, OSH-21)

Een icoon staat altijd in een afgeronde icoontegel in een paletkleur, nooit los (pptx 0,56 in; Edwin 0,42 in op 10 in). Tegelparen (tegel/icoon): blauw/geel, geel/blauw, groen/roze, oranje/zwart, roze/blauw (token `tile_pairs.icon_fg`); op een kaart nooit dezelfde tegelkleur als de kaart (`tile_pairs.on_card`). Wissel de kleurparen af binnen één slide (`tile_pairs.cycle`). Getoetst: handmatig.

## Vormentaal (OPP-24, OSH-23)

Afgeronde rechthoeken (kaarten), cirkels (stapnummers, stippen) en pillen (labels). Geen schaduwen, geen verlopen, geen randen. Getoetst: handmatig.

## Grafieken (OPP-25, OSH-26)

Kleurvolgorde blauw, oranje, groen, geel, roze (token `data_visualization.categorical_order`; één reeks = blauw). Native en bewerkbaar; altijd een kaart of titel die zegt wat opvalt. Getoetst: handmatig.

## Deckstructuur: opening, delen en afsluiter (OPP-26, OPP-27, OPP-28, OSH-24)

- **Opening (OPP-26):** roze, de titelslide van de potx; titel 54 pt vet, ondertitel 40 pt regular (vraag of belofte), 2 metaregels. Volgorde: opening, delen, oproep/vervolg of "Meer weten / Met dank aan", optioneel blok vaste CEDA-slides (OPP-09), afsluiting.
- **Delen (OPP-27):** kleurvolgorde `npuls-roze` → `npuls-oranje` → `npuls-groen` → `npuls-blauw`.
- **Afsluiter (OPP-28, OSH-24):** "Onderwijs **bewegen.**", CC BY-SA 4.0-tekst met naamsvermelding (waarop de inhoud gebaseerd is) en het Npuls-logo; logo en merkelementen niet wijzigen.
- Getoetst door: `build.mjs`, deels handmatig.

## Label-pil (OPP-18, OSH-18)

De label-pil staat linksboven, heeft de accentkleur van de slide (zelfde kleur als het accentdeel van de titel) en de tekstkleur uit `badge_fg`. Inhoud: 1 tot 3 woorden in KAPITALEN die de functie van de slide noemen (de inhoudsregel staat in de ontwerper-skill). Getoetst: handmatig (de lengte door `build.mjs`).
