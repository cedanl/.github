---
name: mkdocs-setup
description: Richt een MkDocs Material documentatiesite in volgens het CEDA-handboekontwerp met Npuls-palet, pil-tabbladen, rustige Markdown-startpagina en GitHub Pages-workflow. Gebruik bij "/mkdocs-setup", "maak een docs-site", "voeg MkDocs toe" of "pas MkDocs aan". LET OP — niet voor applicatie-UI buiten MkDocs; gebruik daar `vormgever-npuls-huisstijl` en voor presentaties `clidev`.
allowed-tools: Read Grep Glob Write Edit Bash AskUserQuestion
compatibility: Requires python3 and uv (and gh CLI when configuring GitHub Pages)
metadata:
  ceda-id: ceda.mkdocs-setup
  ceda-version: "1.0.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: docs/stylesheets/extra.css
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# MkDocs Setup in CEDA/Npuls-stijl

Bouwt een nieuwe MkDocs Material documentatiesite op voor een `cedanl`-repository — of trekt een bestaande MkDocs-site gelijk naar de vaste CEDA/Npuls-stijl uit `cedanl/.github`. Vraag eerst de projectgegevens uit en toon een overzicht ter akkoord voordat je bestanden wegschrijft of GitHub Pages aanpast.

## Vaste stijlelementen (niet van afwijken)

Elke CEDA MkDocs-site deelt exact dezelfde rustige opzet en Npuls-tokens (bron: `.claude/skills/vormgever-npuls-huisstijl/references/design-tokens.json`):

- **Header en navigatiebalk (`.md-header`, `.md-tabs`):** achtergrond `npuls-roze` (`#F4D9DC`) met tekst in `npuls-zwart` (`#000000`, contrast 15,8:1 WCAG AAA) en een onderrand van `2px solid #DD784B` (`npuls-oranje`).
- **Beeldmerk en favicon:** `docs/assets/logos/npuls_logo.jpg` (met `#F3D9DC`-achtergrond die naadloos wegvalt op `npuls-roze`) als `logo` en `docs/assets/logos/beeldmerk.svg` als `favicon`.
- **Pil-tabbladen en zoekbalk:** top-level tabs verticaal gecentreerd (`height: 2.6rem`), hover in `rgba(255, 255, 255, 0.65)` en actieve tab als pil in `npuls-oranje` (`#DD784B`) met vette zwarte tekst (`#000000`, 6,86:1 AA). Zoekbalk (`.md-search__form`) als witte pil (`#FFFFFF`, `border-radius: 9999px`) met blauwe hover-rand (`#3D68EC`).
- **Typografie en links:** `'General Sans', 'Plus Jakarta Sans', system-ui, sans-serif` (geladen via Google Fonts; nooit Inter). Links in de tekst in `npuls-blauw` (`#3D68EC`) met hover-markering in `licht-geel` (`#FCF5D4`). Zichtbare toetsenbordfocus (`3px solid #3D68EC`).
- **Tabellen, codeblokken en admonitions:** afgeronde tabellen (`12px` radius) met koprij (`th`) op `npuls-roze` (`#F4D9DC`) en vette zwarte tekst. Admonitions volgen de Npuls-statuskleuren zonder standaard rood buiten het palet: `info`/`note` = `npuls-blauw` (`#3D68EC` op `#D6E2FD`), `warning` = `npuls-oranje` (`#DD784B` op `#FFE4D8`), `tip`/`success` = `npuls-groen` (`#00AF81` op `#CCEEE6`).
- **Footer:** `npuls-roze` (`#F4D9DC`) met `2px solid #DD784B` bovenrand en `licht-roze` (`#FAEAEA`) balk voor copyright en vaste links naar Npuls, de CEDA-community (`edu.nl/twt84`) en `ceda@surf.nl`.
- **MkDocs Material features:** `navigation.tabs`, `navigation.tabs.sticky`, `navigation.sections`, `navigation.indexes`, `navigation.path`, `navigation.top`, `search.highlight`, `search.suggest`, `content.code.copy`, `content.code.annotate`, `content.tabs.link`, `toc.follow`.

## Workflow

When the user invokes `/mkdocs-setup [optioneel: pad of repo]`:

### 1. Inspecteer de huidige repository

Controleer wat er al aanwezig is:

```bash
ls -la mkdocs.yml mkdocs.yaml pyproject.toml docs/ .github/workflows/docs.yml 2>/dev/null || true
```

- **Bestaat `mkdocs.yml` al?** Lees de huidige `mkdocs.yml`, `docs/index.md` en eventuele `extra.css`. Stel voor om de bestaande site over te zetten naar de CEDA/Npuls-stijl met behoud van de bestaande inhoud en `nav:`.
- **Nieuwe site?** Bepaal of de repository een Python-pakket met `pyproject.toml` is of een losse documentatie-repository zonder `pyproject.toml`.

### 2. Kort interview

Stel de ontbrekende vragen in één keer via `AskUserQuestion` (geen vraag over accentkleur — het Npuls-palet ligt vast):

1. **Sitenaam en korte beschrijving** — titel in de header (bijv. `1CijferHO` of `<Repo> Documentatie`) en één zin voor `site_description`.
2. **Python API-referentie (`mkdocstrings`)** — alleen vragen als `src/<package>/` aanwezig is: wil je automatische API-documentatie op basis van Google-style docstrings?
3. **Uitbreidingen** — zijn **Mermaid**-diagrammen of **MathJax**-formules nodig, of geen van beide?

### 3. Bouw het ontwerp op vanuit de gebundelde templates

1. **`mkdocs.yml`:** neem `assets/mkdocs.yml.tpl` als basis. Vul `<site_name>`, `<site_description>` en `<repo>` in, schakel alleen de gevraagde optionele blokken (`mkdocstrings`, `include-markdown`, Mermaid of MathJax) in en zet alle navigatietitels in helder Nederlands.
2. **`docs/stylesheets/extra.css`:** kopieer `assets/extra.css` ongewijzigd naar `docs/stylesheets/extra.css`.
3. **Logo en favicon (`docs/assets/logos/`):** kopieer `npuls_logo.jpg` en `beeldmerk.svg` vanuit `.claude/skills/vormgever-npuls-huisstijl/assets/logos/` naar `docs/assets/logos/`. Is die map lokaal niet aanwezig, haal beide bestanden dan op uit `cedanl/.github` en plaats nooit een lege placeholder.
4. **Startpagina (`docs/index.md`):** gebruik `assets/index.md.tpl`. Schrijf actief Nederlands volgens de Npuls-schrijfwijzer (`je`/`wij`, geen `u`/`uw`, korte zinnen).
5. **Dependencies en `.gitignore`:**
   - Voeg `site/` toe aan `.gitignore` als die regel nog ontbreekt.
   - Heeft de repo een `pyproject.toml`? Voeg dan alleen de `docs`-groep toe (`mkdocs>=1.6.0`, `mkdocs-material>=9.5.0`, `pymdown-extensions>=10.0`, en optioneel `mkdocstrings[python]>=0.26.0` of `mkdocs-include-markdown-plugin`) zonder de rest van `pyproject.toml` te overschrijven.
6. **GitHub Actions (`.github/workflows/docs.yml`):** gebruik `assets/docs-workflow.yml.tpl` — kies Variant A voor nieuwe Python-projecten (GitHub Pages bron = `GitHub Actions`) of Variant B wanneer een bestaande repo al via een `gh-pages` branch publiceert.

### 4. Toon de draft en wacht op akkoord

Presenteer welke bestanden worden aangemaakt of bijgewerkt (inclusief de `nav:`-structuur en de gekozen workflow-variant) en wacht op expliciet akkoord vóór het schrijven of aanpassen van GitHub Pages-instellingen.

### 5. Schrijf weg, valideer lokaal en configureer optioneel GitHub Pages

1. Schrijf de goedgekeurde bestanden weg.
2. Draai direct de strikte build-controle (zie **Verificatie**) en los eventuele link- of ankerwaarschuwingen op.
3. Alleen bij Variant A én na akkoord van de gebruiker: controleer via `gh api repos/cedanl/<repo>/pages` of GitHub Pages op `build_type=workflow` staat.

## Let op: houd `docs/index.md` net zo rustig als vervolgpagina's

Maak op `docs/index.md` **geen** uitbundige landingspagina: geen custom HTML-hero, geen decoratieve kernvorm-SVG's, geen gekleurde sectiekaders, geen losse pill-knoppen of kaartengrids en géén `hide: [navigation, toc]`. Gebruik precies dezelfde rustige Markdown-opbouw als op de dieperliggende pagina's:

- Standaard `# Titel` en een korte introductie van twee zinnen.
- Duidelijke `##`-koppen met gewone Markdown-tabellen (die via `extra.css` automatisch de `npuls-roze` koprij krijgen) en de standaard inhoudsopgave rechts.
- Hooguit één rustig `!!! info`-blok onderaan voor doorverwijzing naar de CEDA-community of verwante documentatie.

## Let op: geen dark-mode toggle en nooit zwart als achtergrondvlak

Voeg geen `scheme: slate` (dark mode) of generieke Material-kleuren (`teal`, `indigo`) toe. `npuls_logo.jpg` heeft een vaste `#F3D9DC` achtergrond die gemaakt is voor de `#F4D9DC` (`npuls-roze`) header, en de Npuls-huisstijl verbiedt `#000000` als achtergrondvlak. Houd `palette` daarom altijd op één blok met `scheme: default`, `primary: custom` en `accent: custom`.

## Let op: zet bronpagina's direct in `docs/`

Zet de Markdown-pagina's zelf in `docs/` (zoals `cedanl/.github` dat sinds #126 doet) in plaats van spiegelbestanden die Markdown uit de hoofdmap insluiten. Links in een ingesloten bestand zijn geschreven vanaf de hoofdmap, maar worden opgelost vanaf de spiegelpagina in `docs/`; ze breken dan in een strikte build (zie `cedanl/.github#124`). Gebruik `include-markdown` alleen voor bestanden die echt in de hoofdmap moeten blijven (zoals `README.md` of `CHANGELOG.md`), zet daarop `rewrite-relative-urls=false` en schrijf de links in dat bestand relatief aan de spiegelpagina. Een strikte build is de toets.

## Verificatie

`ceda-verifies: measurable` — de opzet is geslaagd wanneer een strikte MkDocs-build zonder fouten of waarschuwingen eindigt (exit code `0`):

```bash
# Bij een repo met pyproject.toml:
uv run mkdocs build --strict -d /tmp/mkdocs-check && rm -rf /tmp/mkdocs-check

# Bij een losse docs-repo zonder pyproject.toml:
uv run --with mkdocs-material mkdocs build --strict -d /tmp/mkdocs-check && rm -rf /tmp/mkdocs-check
# (voeg `--with mkdocs-include-markdown-plugin` toe als de site include-markdown gebruikt)
```

## Gebundelde bestanden

- `assets/mkdocs.yml.tpl` — lees altijd bij stap 3: het canonieke `mkdocs.yml`-sjabloon met Npuls-features, plugins en extensies
- `assets/extra.css` — kopieer altijd bij stap 3 ongewijzigd naar `docs/stylesheets/extra.css`: het volledige Npuls-stylesheet voor MkDocs Material
- `assets/index.md.tpl` — lees bij stap 3 wanneer je een nieuwe `docs/index.md` opzet of een drukke startpagina terugbrengt naar de rustige Markdown-stijl
- `assets/docs-workflow.yml.tpl` — lees bij stap 3 wanneer `.github/workflows/docs.yml` wordt aangemaakt of gesplitst in `build` (`--strict`) + `deploy`

## Important

- Overschrijf nooit een volledige bestaande `pyproject.toml`; voeg uitsluitend de `docs`-dependencygroep toe.
- Zet geen uitgebreide catalogus van alle CEDA-repositories op een project- of handboeksite; verwijs voor het inhoudelijke projectoverzicht naar de CEDA-community (`https://edu.nl/twt84`).
- Push of wijzig nooit GitHub Pages-instellingen zonder voorafgaand akkoord van de gebruiker.
