---
name: ontwerper-slides-html
description: Ontwerpregels voor HTML-presentaties van CEDA/Npuls — tekst per slide, verhaallijn, animatie en interactie, leesbaarheid, toegankelijkheid, fancy-schaal A/B/C. Gebruik bij het ontwerpen of beoordelen van een HTML-deck of show-deck. Niet voor het bouwen zelf (dat doet `cedapress`) en niet voor kleuren of logo's (dat is `vormgever-npuls-huisstijl`).
allowed-tools: Read
metadata:
  ceda-id: ceda.ontwerper-slides-html
  ceda-version: "0.3.1"
  ceda-type: reference
  ceda-subtype: knowledge
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: "cedanl/clidev-presentaties#15 en #16; clanna 0.5.1 (leesbaarheid, ritme van het deck van Janna Berkhout)"
  ceda-activation: chained
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Ontwerper slides — HTML

Best practices voor HTML-decks. `cedapress` raadpleegt deze skill vóór het renderen en toetst daarna met
`renderers/html/check.mjs` en `qa.mjs`. Huisstijl (palet, fonts, logo, bogen) komt uit
`vormgever-npuls-huisstijl`; hier staat hoe je een goede slide maakt.

**Toetsbare regels:** `references/regels.md` (id, regel, meetbaar criterium, fancy-niveau, waar getoetst).
Het id staat in de check-meldingen, bv. `[OSH-02]`.

Regels gebaseerd op de ontwerprichtlijnen van Edwin (ceda-powerpoint-maker 0.2.0), afgeleid uit de CEDA-presentatie Uitnodigingsregel en de Npuls-huisstijl. Alleen het deel dat los staat van het medium is overgenomen.

**Rollen en beheer** (gelijk in vormgever, ontwerper-powerpoint, ontwerper-slides-html en cedapress):

| Skill | Beheer | Wat erin hoort | Wat er niet in hoort |
|---|---|---|---|
| `vormgever-npuls-huisstijl` (incl. `design-tokens.json`, `references/presentaties.md` en het assetpakket `npuls-assets`) | Edwin | alles wat Npuls-specifiek is: palet, kleurrollen per achtergrond, tegelparen, fonts, logo's, vormen, illustraties, potx, deckstructuur (roze opening, afsluiter "Onderwijs bewegen.", CC BY-SA), label-pil, grafiekvolgorde | hoe je een goede slide maakt; renderercode |
| `ontwerper-powerpoint`, `ontwerper-slides-html` | Edwin | algemene ontwerpregels voor elk deck: één boodschap per slide, max. ~50 woorden, titel als bewering, minimale lettergrootte, afwisseling, contrast. Voor kleur: kies uit de rollen van de huisstijl | hexcodes, kleurlijsten, Npuls-namen |
| `cedapress` | Aslam | orkestreren en bouwen: `bron.md`, renderers, checks, `assets.lock`. Leest de tokens en `presentaties.md`, kopieert niets | eigen kleurtabellen of Npuls-regels |

Een Npuls-afspraak wijzigen = `design-tokens.json` of `presentaties.md` aanpassen (Edwin), daarna een assetrelease en de pin in `cedapress/assets.lock` ophogen (Aslam).

**Kleur en Npuls-vorm:** hier staan alleen algemene ontwerpregels. Kies kleuren uit de rollen van de huisstijl (kleurrollen per achtergrond, tegelparen, vormentaal, grafiekvolgorde, opening en afsluiter, label-pil): `vormgever-npuls-huisstijl/references/presentaties.md` en `design-tokens.json`. Regelnummers in `references/regels.md` blijven staan en verwijzen daarheen.

> Open punten staan onder "Nog open" in `references/regels.md`. Wijzig een drempel daar én in `check.mjs`.

## Kern

1. **Eén boodschap per slide.** De kop is een bewering ("Uitval zit vooral in jaar 1"), geen onderwerp.
2. **Weinig tekst.** Max ~50 woorden zichtbaar, 3 tot 5 punten per lijst. Meer → splitsen of naar de notes.
3. **Verhaallijn:** aanleiding → kern (max 4 delen bij meer dan 8 inhoudsslides, 2 tot 4 inhoudsslides per deel) → wat vragen we → afsluitvraag.
   Licht en verzadigd afwisselen; één verzadigde slide per kernboodschap.
4. **Leesbaar van achterin de zaal:** tekst schaalt mee met de breedte; geen lage bovengrens op `font-size`.
   Lege onderhelft → grotere componenten, niet kleinere letters.
5. **Animatie en interactie alleen als ze iets uitleggen:** een cijfer dat oploopt, een stap die volgt, een
   peiling. Nooit inhoud die alleen via animatie zichtbaar wordt (PDF, print en reduced motion tonen alles stil).
6. **Toegankelijk:** alt-tekst bij elke inhoudsafbeelding (`alt=""` bij decoratie), alleen toegestane
   kleurcombinaties, toetsenbordnavigatie werkt.

## Fancy-schaal

| Niveau | Wat | Wanneer |
|---|---|---|
| **A sober** | Palet, kop + tekst, hooguit één illustratie per slide, geen extra animatie | Intern overleg, review, veel cijfers |
| **B huisstijl+** (standaard) | A + Npuls-logo linksboven, drie bogen rechtsonder terugkerend, datacomponenten, ingebouwde animaties | Externe sessies, stuurgroep |
| **C rijk** | B + meer illustraties, `data-count`/`data-draw`, interactie (klik, Mentimeter), delen-navigatie | Kick-off, keynote, community |

Fancy mag de huisstijl nooit breken: ook C blijft binnen het palet, de fonts en de vormtaal.
Het niveau staat in `bron.md` (`fancy:`) en in de HTML (`<meta name="cedapress-fancy" content="B">`).
Varianten voor A/B/C-tests (bv. een "Muhammet-versie") komen later als aparte regelsets.
