---
name: cedapress
description: Gebruik wanneer iemand een presentatie, deck of slides wil in Npuls/CEDA-huisstijl — een HTML-deck, html-presentatie, show-deck, kick-off of keynote, een PowerPoint of pptx die collega's zelf aanpassen, een deck voor een opdrachtgever, of beide vormen uit één bron — of een bestaand deck wil bijwerken, exporteren naar pdf/pptx of wijzigingen uit een gedeelde pptx wil terughalen. Ook bij "/cedapress" en de oude namen "/clanna" en "/powerclaude". LET OP — een Slidev-presentatie is `clidev`; een Marp-deck is `build-marp-deck`.
allowed-tools: Read Write Edit Bash Glob Grep
compatibility: Requires node, python 3 en git. pptx-route ook python-pptx en PowerPoint (Windows) of LibreOffice. Npuls-assets via het versioned pakket van vormgever-npuls-huisstijl. playwright-chromium en pptxgenjs eenmalig via npm install in de renderers-map.
metadata:
  ceda-id: ceda.cedapress
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: "cedanl/clidev-presentaties#15 en #16; vervangt clanna 0.5.1 (frame van Janna Berkhout) en powerclaude 0.3.0"
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# cedapress — presentaties uit één bron

Eén **bron-markdown** per deck; daaruit maakt cedapress een HTML-deck, een pptx op de officiële Npuls-template,
of beide. Vervangt `clanna` (HTML) en `powerclaude` (pptx); hun renderers en checks zitten hier, gedrag gelijk.

```
bron.md  →  HTML-deck       (git, projectrepo)
   ↑     →  pptx / pdf      (SharePoint; projectrepo-README linkt)
   └──── tekst en notes uit een bewerkte pptx (terugschrijven)
```

`<cp>` = de map van deze skill ("Base directory"). **Vereist:** laad `vormgever-npuls-huisstijl` (palet,
combinaties, vormtaal) en per vorm `ontwerper-slides-html` en/of `ontwerper-powerpoint` (ontwerpregels).

**Met dank aan Janna Berkhout (KIS):** de HTML-frame (engine, slide-varianten, componenten, ritme) komt uit haar
deck *"Welk open-source model kan mijn LLM-wiki het beste onderhouden?"*, via clanna. "clanna" blijft triggerwoord.

## Vaste regels

| Regel | Waarom |
|---|---|
| **`bron.md` is altijd verplicht** en wordt eerst geschreven; HTML en pptx komen er altijd uit | Eén waarheid. HTML of pptx nooit los bewerken; pptx-wijzigingen via terugschrijven |
| HTML draagt `<meta name="cedapress-bron">`, deck-spec draagt `bron:` = hash van `bron.md` | `check.mjs` en `build.mjs` falen als de output achterloopt op de bron |
| Npuls-assets alleen uit het assetpakket, versie in `assets.lock` | Eén bron; nooit meer `public/npuls` uit clidev-presentaties |
| Deck in de **projectrepo**: `presentaties/YYMMDD_onderwerp/` | Deck staat bij het project; README-sectie "Presentaties" linkt |
| Binaire exports (pdf, pptx, gebundelde html) niet in git → SharePoint | Repo blijft klein; exports zijn altijd opnieuw te maken |
| Vaste CEDA-slides aan: titel → Wie is CEDA → Wie zijn wij → inhoud → Blijf in contact → Einddia | Tekst ligt vast; alleen weglaten op expliciet verzoek |
| Zakelijk, geen opvulling; elke bewering en elk cijfer tegen de bron getoetst vóór export | Geen LLM-fluff (sectiescheiders zonder inhoud, wervende ledes); tekst volgens `npuls-schrijfwijzer` |
| Niet "klaar" melden zonder check, qa/render en alle screenshots bekeken | Overloop, botsingen en lege vlakken zie je niet in de broncode |

## Werkwijze

### 1. Vaste vragen — in één bericht, vraag alleen wat ontbreekt

1. **Voor wie** (publiek, setting, duur)
2. **Kernboodschap** in één zin
3. **Vorm:** html, pptx of beide
4. **Fancy:** A sober, B huisstijl+ (standaard), C rijk — zie de ontwerper-skills
5. **Project** — bepaalt de repo. Bekende projecten: Uitnodigingsregel, Instroomprognose, Sectorale
   informatievoorziening, Samenwijzer, SkillsRadar, NKO, Open-onderwijsdata-chat, MCP en EduGenAI,
   Instellingsdata-chat, Synthetische data.

Plus: bronnen (lees ze zelf), spreker, datum. Een gevraagd aantal slides telt inhoudsslides.

### 2. Projectrepo vinden

Zoek lokaal (`~/Projects/<repo>`, naam lijkt op het project) en anders `gh repo list cedanl --topic project`.
Niets gevonden of twijfel → vraag de gebruiker waar het deck moet komen. Maak `presentaties/YYMMDD_onderwerp/`.

### 3. Eén rondje inhoud aanscherpen

Leg de verhaallijn voor in max ~8 regels (titel per slide als bewering + kernboodschap). Vraag één keer om
reactie; verwerk die. Ontbreekt een cijfer → vragen, nooit verzinnen.

### 4. Bron-markdown schrijven

Formaat: `references/bronformaat.md`. Schrijf `bron.md`, valideer:

```bash
python <cp>/scripts/parse_bron.py presentaties/YYMMDD_onderwerp/bron.md --check
python <cp>/scripts/parse_bron.py presentaties/YYMMDD_onderwerp/bron.md --vorm html   # of pptx: JSON per slide
```

### 5. Ontwerp toetsen

Lees `ontwerper-slides-html` / `ontwerper-powerpoint` en hun `references/regels.md` voor het gekozen
fancy-niveau. Pas de bron aan als een slide de regels niet haalt (te veel tekst → splitsen of naar Notes).

### 6. Renderen

Eenmalig: `npm install --prefix <cp>/renderers` (playwright-chromium, pptxgenjs). Assets: de renderers roepen
`vormgever-npuls-huisstijl/scripts/npuls_assets.py ensure` aan met de versie uit `assets.lock`; override met
env `NPULS_ASSETS_DIR`. Niet in het pakket: fonts (licentie; web via CDN in `npuls.css`, pptx via env
`NPULS_FONTS_DIR` naar de communicatiekit) en de CEDA-teamfoto (env `CEDA_TEAMFOTO` of `img/team-groep.png` in de deckmap).

**HTML** — componenten en slide-varianten: `references/html-componenten.md`; assets en illustraties:
`references/html-assets.md`.

```bash
node <cp>/renderers/html/prepare.mjs presentaties/YYMMDD_onderwerp   # npuls-link, .gitignore, frame + bron-hash
```

Vul `YYMMDD_onderwerp.html` uit de bron: `{{…}}`-placeholders, inhoudsslides op `<!-- INHOUD -->`, notes als
HTML-commentaar boven de `<section>`, `::: html`-blokken als animatie/interactie. Raak `<style>` en `<script>`
niet aan. Bron later gewijzigd → HTML bijwerken, daarna `check.mjs … --stempel`.

**pptx** — slidetypes en velden: `references/pptx-slidetypes.md`. Start van
`<cp>/renderers/pptx/voorbeeld.deck.mjs` → `YYMMDD_onderwerp.deck.mjs` in de deckmap, met `bron:` =
`parse_bron.py bron.md --hash`. Fonts: `node <cp>/renderers/pptx/install-fonts.mjs --check` (installeren na akkoord).

### 7. Controleren — verplicht

```bash
node <cp>/renderers/html/check.mjs presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html   # huisstijl + bron-hash + ontwerpregels
node <cp>/renderers/html/qa.mjs    presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html   # screenshots 1920×1080 + 1366×768
node <cp>/renderers/pptx/build.mjs presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.deck.mjs   # spec-checks + bouw
node <cp>/renderers/pptx/render.mjs presentaties/YYMMDD_onderwerp/exports/YYMMDD_onderwerp.pptx
```

FOUT → oplossen (in de bron, dan output bijwerken). WAARSCHUWING met id (`[OSH-02]`) → regel opzoeken en
oplossen of bewust laten staan en melden. Bekijk **elke** screenshot/PNG met Read. Audit: elk cijfer en elke
bewering tegen de bronnen.

### 8. Exporteren en opslaan

```bash
node <cp>/renderers/html/bundle.mjs presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html   # exports/…html, één bestand
node <cp>/renderers/html/qa.mjs     presentaties/YYMMDD_onderwerp/YYMMDD_onderwerp.html --pdf
node <cp>/renderers/pptx/render.mjs presentaties/YYMMDD_onderwerp/exports/YYMMDD_onderwerp.pptx --pdf
```

- **In git** (projectrepo): `bron.md`, de HTML, de deck-spec, `*.pptx.meta.json`, `img/`. Niet: `npuls`, `exports/`.
- **SharePoint:** pdf, pptx, gebundelde html, per jaar en project (lokale OneDrive-sync; vraag het pad als het
  onbekend is). Upload via Graph API is nog niet beschikbaar.
- **README** van de projectrepo, sectie `## Presentaties` (aanmaken als die ontbreekt): één regel
  `- YYMMDD — titel — [bron](presentaties/YYMMDD_onderwerp/) · [pdf/pptx](<SharePoint-link>)`.
- Commit alleen als de gebruiker dat vraagt.

Meld: deckmap, uitkomst van check/qa/build/render, exports en waar ze staan. Bij pptx: ontvangers zonder
Npuls-fonts zien Calibri; stuur de PDF mee.

### 9. Bijwerken en terugschrijven

- Inhoud wijzigen = eerst `bron.md`, dan HTML/spec bijwerken en opnieuw checken.
- Bestaande pptx die in PowerPoint is bewerkt: `python <cp>/scripts/terugschrijven.py <deckmap> <pptx>` toont
  wat er in tekst en notes verschilt; na akkoord in `bron.md` verwerken, commit "wijziging uit pptx", opnieuw renderen.
- Een pptx van buiten cedapress (geen meta, geen bron) klein aanpassen: `python <cp>/renderers/pptx/edit.py`
  (dump, replace, beeldmerk, media, kloon, importeer, verplaatst, verwijder; zie de docstring). Wil de gebruiker
  dat deck verder onderhouden → eerst een `bron.md` uit `edit.py dump --notes` maken.

## Bestanden

- `assets.lock` — enige plek met de versie van het Npuls-assetpakket
- `references/bronformaat.md` — lees altijd vóór je `bron.md` schrijft
- `references/html-componenten.md`, `references/html-assets.md` — lees bij de HTML-route
- `references/pptx-slidetypes.md` — lees bij de pptx-route
- `scripts/parse_bron.py` — draaien: valideren, splitsen per vorm, hash; test: `python -m unittest <cp>/scripts/test_parse_bron.py`
- `scripts/test_parse_bron.py` — tests van de parser
- `scripts/terugschrijven.py` — draaien: pptx → verschillen met de bron (skelet, zie TODO in het bestand)
- `renderers/html/` — `frame.html`, `prepare.mjs`, `check.mjs`, `qa.mjs`, `bundle.mjs` (uit clanna)
- `renderers/pptx/` — `build.mjs`, `build_potx.py`, `render.mjs`, `edit.py`, `install-fonts.mjs`, `lib/`, `voorbeeld.deck.mjs` (uit powerclaude)
- `renderers/lib/` — assetpakket vinden (`npuls-assets.mjs`, `npuls_assets_path.py`), bron-hash (`bron.mjs`), node-afhankelijkheden (`deps.mjs`)
- `examples/261119_voorbeeld/` — klein voorbeelddeck (bron + HTML) om de renderers te testen

## Veelgemaakte fouten

| Symptoom | Oplossing |
|---|---|
| `HTML loopt achter op bron.md` | HTML bijwerken uit de bron, dan `check.mjs … --stempel` |
| `deck-spec loopt achter op bron.md` | Spec bijwerken, `bron:` op de nieuwe hash zetten |
| `map npuls/ naast het deck ontbreekt` / koppen in systeemfont | `prepare.mjs <deckmap>` draaien; controleer `NPULS_ASSETS_DIR` of het assetpakket |
| `playwright-chromium niet gevonden` | `npm install --prefix <cp>/renderers` |
| Calibri of dubbele woorden in de pptx-PNG's | Fonts niet geïnstalleerd: `install-fonts.mjs`, PowerPoint herstarten |
| Inhoud onder de navigatiebalk op 1366×768 | Minder tekst, `g4` → `g3`, of splitsen (in de bron) |
| Render faalt op macOS/Linux | LibreOffice en poppler (`pdftoppm`) installeren |
