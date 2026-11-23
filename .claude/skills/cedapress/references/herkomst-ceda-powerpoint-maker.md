# Edwins ceda-powerpoint-maker in cedapress

Edwin maakte de skill `ceda-powerpoint-maker` 0.2.0. Hier staat wat we ervan overnemen, waarom, en wat nog open is (stand 2026-11-23).

## Taakverdeling

De officiële Npuls-potx (via `vormgever-npuls-huisstijl` en de release `npuls-assets`) is het kader voor HTML én pptx en gaat voor.

| | Vast (vormgever, `npuls-assets`; Edwin wijzigt dit niet) | Flexibel (Edwin beheert `ontwerper-powerpoint` en `ontwerper-slides-html`) |
|---|---|---|
| Wat | potx-layouts, kleuren, fonts, logo's, vormen, illustraties, tokens | componenten, slidepatronen, drempels, kleurkeuze per slide, deckstructuur |
| Grens | | alleen binnen de potx-layouts en de tokens |

Ontbreekt er een asset (bijvoorbeeld iconen)? Dan komt die via een nieuwe assetrelease, niet via een eigen bestand in een deck of een skill.

## Wat Edwin aanleverde

- **Ontwerprichtlijnen** (`ontwerprichtlijnen.md`), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl. Erin staan formaat, raster, typografie, kleurcombinaties, tekst en toon, iconen en grafieken.
- **Bouwscript** `npuls_deck.py`: 656 regels Python op python-pptx. Het bevat:
  - huisstijlconstanten: kleuren, fonts en een raster in inches;
  - een tekstcheck `_past` die waarschuwt als tekst niet past;
  - ongeveer 15 componenten, zoals label-pil, tweekleurige titel, kaart met icoontegel, stappen, kerncijfer, citaat, heldenkaart en native grafiek;
  - deckfuncties: opening, deel-slide, inhoudsslide, afsluiting en een teller.
- **Eigen template** `npuls-template.pptx` (10 × 5,625 in) met 12 layouts, zoals "Deel roze" en "Inhoud lgeel".
- **Assets:** 21 PNG-iconen en 7 PNG-illustraties met een vaste achtergrondkleur.
- **Werkwijze:** eerst uitvragen (publiek, doel, lengte, bron), dan een slideplan laten bevestigen, bouwen, en daarna visueel controleren.

## Wat we overnemen

| Onderdeel | Waar | Status |
|---|---|---|
| Ontwerprichtlijnen | `ontwerper-powerpoint` (OPP-15..29) en `ontwerper-slides-html` (OSH-17..26); bij een conflict met onze oude regels gaan Edwins regels voor | PR #129 |
| Vragenronde en slideplan | werkwijze in `cedapress/SKILL.md`; het slideplan komt in `bron.md` | PR #129 |
| Componenten (label-pil, tweekleurige titel, icoontegel, stapkolom, kerncijfer naast lead, heldenkaart, notitiebalk, inzichtregel, lijstkaart, pillenkaart, tekstcheck) | overgezet naar de pptx-renderer (potx-engine) en naar het HTML-frame van cedapress | PR #129 |
| Iconen | in `npuls-assets` als SVG (`iconen/<naam>.svg`) | wacht op de licentiecheck; de renderer ondersteunt ze al en meldt een ontbrekend icoon als waarschuwing |

## Wat we niet overnemen, en waarom

- **Zijn template als basis.** cedapress bouwt op de officiële Npuls-potx uit de assetrelease. Met een eigen template lopen we uit de pas zodra Npuls de potx bijwerkt. Zijn layouts en maten zetten we om naar de potx (13,33 × 7,5 in, dus alles 4/3 groter).
- **Zijn bouwscript als motor.** Het script kent geen `bron.md`, geen hash en geen vastgezette assetversie. Die drie zijn nodig om HTML en PowerPoint uit één bron te maken. Ombouwen kost naar schatting 5 à 8 dagen, tegen 2 à 3 dagen om zijn componenten over te zetten.
- **PNG-illustraties.** Die zitten al als SVG in het assetpakket. Met de ingebakken achtergrond staan ze als blok op een andere kleur.

## Hoe we vergeleken

We bouwden hetzelfde deck van 8 slides over de Uitnodigingsregel met beide bouwers en renderden het via PowerPoint.

| | Edwin | cedapress |
|---|---|---|
| Uiterlijk | strakker, met label-pil, tweekleurige titel en icoontegels | goed, maar de kaartenslide is half leeg |
| Officiële potx | nee | ja |
| Bewerkbaar | 7 placeholders en 42 losse tekstvakken | 24 placeholders en 15 tekstvakken |
| Fout zonder waarschuwing | woorden afgebroken midden in het woord; illustratie als blok | illustratie over de kaarttekst; dubbele aslabels in de grafiek |
| Past bij bron.md en release | nee | ja |

## Nog open, vragen aan Edwin

1. Waar komen de 21 iconen vandaan, en onder welke licentie vallen ze? Tot dat vaststaat zitten er geen iconen in cedapress; de icoontegel toont zonder icoon een waarschuwing.
2. Klopt de omzetting van pt naar px voor HTML? OSH-05 houdt minimaal 18 px aan.

## Besloten door Aslam (2026-11-23)

- **Vaste CEDA-slides (ceda, team, contact) zijn optioneel.** Ze vormen één blok vóór de afsluiter; de auteur kiest per deck (`vaste-slides: ja` of `nee` in de bron). Waarschuwingen over ontbrekende of verkeerd geplaatste vaste slides zijn vervallen.
- **Zwart nooit als vlak.** `npuls-zwart` is uit `allowed_combinations` in `design-tokens.json` geschrapt als achtergrond. `npuls.css` veranderde daardoor niet, dus er is geen nieuwe assetrelease nodig.
- **Taakverdeling** zoals hierboven: potx en tokens vast, componenten en patronen flexibel.
