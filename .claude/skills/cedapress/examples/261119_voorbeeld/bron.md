---
titel: Eén bron, twee vormen
project: CEDA
publiek: CEDA-team, 10 minuten
kernboodschap: Elk deck heeft één bron-markdown; HTML en pptx komen eruit
vorm: beide
fancy: B
duur: 10
spreker: CEDA
datum: 2026-11-19
vaste-slides: ja
---

## Slide 1 — Eén bron houdt HTML en pptx gelijk
type: split
De inhoud staat één keer in bron.md. HTML en pptx worden eruit gemaakt.
Notes: Testslide voor de renderers; geen echte inhoud.

::: html
Illustratie 07 rechts, kop schuift in.
:::
::: pptx
Split met illustratie-07 rechts.
:::

## Slide 2 — De check vangt verouderde output
type: list
- HTML en deck-spec dragen de hash van de bron
- Andere hash: check en build falen
- Wijziging uit pptx: terugschrijven, daarna opnieuw maken
Notes: Laat zien dat check.mjs faalt na een bronwijziging zonder --stempel.

## Slide 3 — Wat vind jij?
alleen: html
Peiling: werkt één bron voor jouw decks?
Notes: Alleen in HTML; in pptx vervalt deze slide.
