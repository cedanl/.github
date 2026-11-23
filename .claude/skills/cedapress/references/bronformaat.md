# Bron-markdown (`bron.md`)

Eén `bron.md` per deck is de **single source of truth**. Altijd verplicht: cedapress schrijft hem eerst,
HTML en pptx worden er altijd uit gemaakt. Nooit HTML of pptx los bewerken zonder dat de bron mee verandert;
wijzigingen in een gedeelde pptx komen via `scripts/terugschrijven.py` terug. Formaat uit pitch
cedanl/clidev-presentaties#16. Parser en validatie: `python <cedapress>/scripts/parse_bron.py bron.md --check`.

## Plaats

```
<projectrepo>/presentaties/YYMMDD_onderwerp/
  bron.md                              # inhoud (git)
  YYMMDD_onderwerp.html                # HTML-deck, draagt de bron-hash (git)
  YYMMDD_onderwerp.deck.mjs            # pptx-deckspec, draagt de bron-hash (git)
  YYMMDD_onderwerp.pptx.meta.json      # hash van de geëxporteerde pptx, voor terugschrijven (git)
  img/                                 # eigen afbeeldingen, los (git)
  npuls  -> assetpakket                # link, niet in git (prepare.mjs)
  exports/                             # pdf, pptx, gebundelde html: niet in git, naar SharePoint
```

De README van de projectrepo krijgt onder `## Presentaties` één regel per deck met de link naar de map
en naar de export op SharePoint.

## Opbouw

```markdown
---
titel: Uitval in het eerste jaar
project: Instroomprognose
publiek: bestuurders mbo, 15 minuten
kernboodschap: Uitval zit vooral in jaar 1 en is per sector anders
vorm: beide            # html | pptx | beide
fancy: B               # A sober | B huisstijl+ | C rijk (ontwerper-skills)
duur: 15               # minuten; ~1 inhoudsslide per 2 minuten
spreker: Naam
datum: 2026-11-19
vaste-slides: ja       # Wie is CEDA, Wie zijn wij, Blijf in contact; nee alleen op expliciet verzoek
bronnen: pad/of/url, pad2
---

## Slide 1 — Uitval in het eerste jaar
type: stats
Tekst op de slide: 1 op de 4 studenten stopt in jaar 1.
Notes: Benadruk dat dit landelijk is, niet per instelling.

::: html
Teller loopt op van 0 naar 25%; klik toont uitsplitsing per sector.
:::
::: pptx
Statische grafiek; uitsplitsing op volgende slide.
:::

## Slide 2 — Uitsplitsing per sector
alleen: pptx
Tabel mbo / hbo / wo.
Notes: In HTML zit dit achter de klik op slide 1.
```

## Regels

| Element | Betekenis |
|---|---|
| `## ` | Nieuwe slide. `Slide N — ` ervoor mag, de rest is de **titel** (een bewering, geen onderwerp). |
| Sleutels direct onder de kop | `type` (pptx-slidetype of HTML-component), `alleen`, `variant`, `layout`, `deel`. Alleen deze namen. |
| Tekst | Wat op de slide staat, in markdown. Gedeeld door beide vormen. |
| `Notes:` | Sprekersnotities, tot de volgende slide of het volgende blok. Elke slide heeft notes. |
| `::: html` … `:::` | Alleen voor HTML: animatie, timer, interactie, Mentimeter. |
| `::: pptx` … `:::` | Alleen voor pptx: statische variant, ander slidetype. |
| Geen blok | Slide is in beide vormen gelijk. |
| `alleen: html` / `alleen: pptx` | Slide bestaat in één vorm. |

Vaste CEDA-slides (titel, Wie is CEDA, Wie zijn wij, Blijf in contact, Einddia) staan **niet** in de bron:
de renderers zetten ze erin (`vaste-slides: ja`). Alleen de projectenlijst op "Wie zijn wij" mag in de
frontmatter: `team-projecten: Instroomprognose, Staat van de Onderwijsinstelling`.

## Hash

`parse_bron.py bron.md --hash` geeft `sha256:<16 hex>` over de tekst (BOM weg, `\r\n` → `\n`); gelijk aan
`renderers/lib/bron.mjs`. De HTML draagt hem in `<meta name="cedapress-bron">`, de deck-spec in `bron:`.
`check.mjs` en `build.mjs` falen als die niet gelijk is aan de huidige `bron.md`. Na het bijwerken van de
HTML uit een gewijzigde bron: `check.mjs <deck.html> --stempel`; in de deck-spec de nieuwe hash zetten.
Stempel alleen nadat de inhoud echt is bijgewerkt.

## Terugschrijven uit pptx

1. Bij export schrijft `build.mjs` `<naam>.pptx.meta.json` met de hash van de pptx en van de bron.
2. Is de pptx op SharePoint bewerkt (andere hash): `python <cedapress>/scripts/terugschrijven.py <deckmap> <pptx>`.
3. Toon de verschillen (tekst en notes) aan de gebruiker; verwerk na akkoord in `bron.md`, commit
   "wijziging uit pptx", maak HTML en exports opnieuw. Opmaak uit PowerPoint komt niet terug.
