---
name: powerclaude
description: Gebruik wanneer iemand een PowerPoint (.pptx) wil in Npuls/CEDA-huisstijl — een powerpoint, pptx-deck, presentatie die collega's zelf moeten kunnen aanpassen, een deck voor een externe partij of opdrachtgever, of slides om in Teams/SharePoint te delen. Ook bij "/powerclaude". LET OP — een Slidev-presentatie of standaard reviewdeck is `clidev`; een los HTML-bestand, show-deck of Mentimeter-deck is `clanna`; een Marp-deck is `build-marp-deck`.
allowed-tools: Read Write Edit Bash Glob Grep
compatibility: Requires node and git; draait in de root van cedanl/clidev-presentaties (Npuls-assets, pptxgenjs en playwright-chromium via npm install). Renderen voor controle via PowerPoint (Windows) of LibreOffice.
metadata:
  ceda-id: ceda.powerclaude
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: "cedanl/clidev-presentaties workshop-voorstel-RAD_fb_CdH.pptx (gemaakt met Claude desktop + vormgever-npuls-huisstijl)"
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# powerclaude — PowerPoint met Claude

Een echte, bewerkbare `.pptx` in Npuls-huisstijl. Jij schrijft alleen de **inhoud** als deck-spec
(een JS-bestand met slides); `build.mjs` tekent elke slide uit vaste layouts met de echte
Npuls-fonts, het palet, het beeldmerk en de illustraties. Zo ziet elk deck er hetzelfde uit en
blijft alles in PowerPoint aanpasbaar (tekstvakken, vormen, native grafieken en tabellen).

**REQUIRED BACKGROUND:** laad `vormgever-npuls-huisstijl` voor kleuren, combinaties, typografie
en vormtaal. `powerclaude` voegt alleen het PowerPoint-deel toe.

**Waar powerclaude bewust afwijkt van vormgever-npuls-huisstijl:**

| vormgever zegt | powerclaude doet | Reden |
|---|---|---|
| Plus Jakarta Sans als digitale vervanger | Echte General Sans, General Sans Semibold en Cooper Lt BT | PowerPoint gebruikt geïnstalleerde fonts; `install-fonts.mjs` zet ze erop |
| Font Awesome-iconen | Npuls-illustraties en vector-vormtaal | Webfonts werken niet in PowerPoint |
| Design tokens niet hardcoden | Palet staat in `scripts/lib/tokens.mjs` | De geïnstalleerde vormgever-kopie mist `references/`; `build.mjs` controleert tegen `design-tokens.json` als die er is |

**Welke skill?** Slidev/reviewdeck → `clidev`. Eén HTML-bestand dat moet opvallen → `clanna`.
Iets wat anderen in PowerPoint openen, aanpassen of doorsturen → `powerclaude`.

## Werkwijze

`<skill>` = de map van deze skill (staat bovenaan als "Base directory").

### 1. Project vinden en klaarzetten

Het deck moet vanuit de root van `clidev-presentaties` gebouwd worden (fonts, illustraties, logo).

```bash
find ~ -maxdepth 6 -type d -name Npuls_lettertype -path "*public/npuls*" -not -path "*/node_modules/*" 2>/dev/null | sed 's#/public/npuls/Npuls_lettertype##' | head -3
```

Niets gevonden → vraag waar het mag komen en `git clone https://github.com/cedanl/clidev-presentaties.git <pad>`.
Ontbreekt `node_modules/pptxgenjs` → `npm install` (of `npm install -D pptxgenjs`).

Fonts controleren — zonder deze fonts rendert PowerPoint in Calibri/Cooper Black, kloppen de
tekstmaten niet en zie je in de controle-PNG's verdubbelde woorden:

```bash
node <skill>/scripts/install-fonts.mjs --check
```

Ontbreken ze → vraag of je ze mag installeren (per gebruiker, geen beheerrechten), dan
`node <skill>/scripts/install-fonts.mjs`.

### 2. Briefing

Je hebt nodig — vraag wat ontbreekt, in één bericht:

1. **Titel**
2. **Aanleiding** — waarom deze presentatie, 1-2 zinnen
3. **Bronnen** — mappen/bestanden met de inhoud; lees die zelf
4. **Publiek, toon en duur**
5. **Spreker, team, datum**

Een gevraagd aantal slides telt **inhoudsslides**; titel en afsluiting komen erbij.
Geen aantal → ~1 inhoudsslide per 2 minuten.

### 3. Deck-spec schrijven

```bash
cp <skill>/assets/voorbeeld.deck.mjs YYMMDD_onderwerp.deck.mjs
```

Lees `references/slidetypes.md` (alle types, velden en varianten) en vervang de inhoud.
Het voorbeeld toont elk type één keer; houd alleen wat je nodig hebt.

- Eerste slide `title`, laatste `closing`.
- Eén boodschap per slide; de titel is een bewering ("Uitval daalt na jaar 1"), geen onderwerp.
- Varianten afwisselen: lichte inhoudsslides, één verzadigde slide per kernboodschap.
- Per slide max ~70 woorden zichtbare tekst. Meer → splitsen.
- Minstens twee Npuls-illustraties in het deck.
- `notes` op elke slide: wat de spreker zegt, niet wat er al staat.
- Getallen alleen uit de bronnen; nooit verzinnen. Ontbreekt een cijfer → vraag het.

### 4. Bouwen en controleren — verplicht, in deze volgorde

```bash
node <skill>/scripts/build.mjs YYMMDD_onderwerp.deck.mjs     # → exports/<naam>/<naam>.pptx
node <skill>/scripts/render.mjs exports/<naam>/<naam>.pptx   # → exports/<naam>/qa/slide-NN.png
```

- **FOUT** → oplossen en opnieuw bouwen.
- **WAARSCHUWING** "tekst past niet" → inkorten of splitsen; niet negeren. Combinatie-waarschuwing → andere kaartkleur of variant.
- Bekijk daarna **elke** PNG met Read. Let op: tekst die over een rand loopt, lege vlakken,
  te volle kaarten, een illustratie die botst. Pas de spec aan en bouw opnieuw.

### 5. Opleveren

```bash
node <skill>/scripts/render.mjs exports/<naam>/<naam>.pptx --pdf   # + exports/<naam>/<naam>.pdf
```

Meld: pad van de spec, de `.pptx`, de PDF, en de uitkomst van build en render.
Zeg erbij: **ontvangers zonder Npuls-fonts zien Calibri** — stuur hun de PDF, of laat ze de
fonts uit `public/npuls/Npuls_lettertype/` installeren. Aanpassen gaat in de spec (opnieuw
bouwen); kleine tekstwijzigingen mogen ook direct in PowerPoint.

## Vaste regels

| Regel | Waarom |
|---|---|
| Altijd via `build.mjs` en een deck-spec; geen eigen pptxgenjs/python-pptx-code | Eigen layouts = elk deck ziet er anders uit en de checks lopen niet |
| Koppen in `General Sans Semibold`, nooit `bold: true` op General Sans | De semibold is in Windows een eigen familie; vet zetten geeft een nep-vet |
| Cooper alleen voor lede, citaat en afsluitvraag | vormgever-regel: Cooper voor introducties/quotes |
| Zwart is nooit een slide- of kaartachtergrond | vormgever-regel |
| Logo (`npuls_logo.jpg`) alleen op een `roze` closing | Het jpg heeft een roze vlak |
| Geen hex-kleuren in de spec; alleen Npuls-kleurnamen | `build.mjs` faalt op onbekende kleuren |
| Niet "klaar" melden zonder build + render + alle PNG's bekeken | Overloop en botsingen zie je niet in de spec |

## Veelgemaakte fouten

| Symptoom | Oplossing |
|---|---|
| Calibri, Cooper Black of dubbele woorden in de PNG's | Fonts niet geïnstalleerd: `install-fonts.mjs`, PowerPoint herstarten, opnieuw renderen |
| `public/npuls/powerpoint_illustrations niet gevonden` | Niet vanuit de projectroot gedraaid |
| `pptxgenjs ontbreekt` | `npm install -D pptxgenjs` in de projectroot |
| Kaarttekst loopt uit de kaart | Minder tekst per sectie, of 4 → 3 kaarten |
| Twee blauwe kaarten naast elkaar op roze | Roze heeft drie kaartkleuren; gebruik 3 items of zet `color` per item |
| Render faalt op macOS/Linux | Installeer LibreOffice en poppler (`pdftoppm`) |

## Gebundelde bestanden

- `references/slidetypes.md` — lees altijd voordat je de spec schrijft: types, velden, varianten
- `assets/voorbeeld.deck.mjs` — startpunt; kopiëren naar de projectroot en invullen
- `scripts/build.mjs <spec>` — draaien, niet lezen: valideert de spec en bouwt de .pptx
- `scripts/render.mjs <pptx> [--pdf]` — draaien: PNG's per slide (en PDF) voor de controle
- `scripts/install-fonts.mjs [--check]` — draaien: Npuls-fonts per gebruiker installeren of controleren
- `scripts/lib/tokens.mjs` — lees alleen als je het palet of de kaartkleuren moet aanpassen
- `scripts/lib/layouts.mjs` — lees alleen als een slidetype ontbreekt en je er een wilt toevoegen
- `scripts/lib/assets.mjs` — lees alleen bij problemen met illustraties of het beeldmerk
