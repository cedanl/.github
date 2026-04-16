---
name: mkdocs-setup
description: Voeg een MkDocs Material documentatiesite toe aan een cedanl Python project en configureer GitHub Pages. Gebruik wanneer iemand documentatie wil toevoegen, een docs-site wil opzetten, of vraagt hoe MkDocs werkt in cedanl repos.
---

# MkDocs Setup

Voeg een volledige MkDocs Material documentatiesite toe aan een cedanl Python project, inclusief GitHub Actions workflow en GitHub Pages configuratie. Gebaseerd op de opzet van `cedanl/1cijferho` en `cedanl/studentprognose`.

## Workflow

When the user invokes `/mkdocs-setup`:

### 1. Controleer bestaande setup

Check of MkDocs al geconfigureerd is:

```bash
ls mkdocs.yml mkdocs.yaml docs/ .github/workflows/docs.yml 2>/dev/null
```

Als `mkdocs.yml` al bestaat: lees de huidige configuratie en bied aan om deze te updaten in plaats van opnieuw te beginnen. Vraag de gebruiker wat er gewijzigd moet worden en stop hier als dat het geval is.

Stel ook vast wat de huidige repo en organisatie zijn:

```bash
gh repo view --json name,owner,description --jq '{name: .name, owner: .owner.login, description: .description}'
```

### 2. Interview — vraag 1

> Wat is de naam van de site? Dit wordt de titel in de navigatiebalk.
> (Standaard: de repo-naam in leesbare vorm, bijv. `1cijferho` → `1CijferHO`)

Wacht op antwoord.

### 3. Interview — vraag 2

> Wat is een korte beschrijving van het project? (1 zin, wordt gebruikt als `site_description` en in de browser-tab)

Wacht op antwoord.

### 4. Interview — vraag 3

> Heeft het project een `src/<package>/` layout met Python code waarvan je de API wil documenteren via docstrings?
> (ja / nee — als ja, wordt `mkdocstrings` geconfigureerd)

Wacht op antwoord.

### 5. Interview — vraag 4

> Heb je extra's nodig?
> - **Mermaid** — diagrammen in Markdown (bijv. flowcharts, sequentiediagrammen)
> - **MathJax** — wiskundige formules via LaTeX
> - **Geen van beide**

Wacht op antwoord.

### 6. Interview — vraag 5

> Welke accentkleur wil je gebruiken voor het thema?
>
> | Kleur | Voorbeeld gebruik |
> |-------|-------------------|
> | `teal` | 1CijferHO |
> | `indigo` | Studentprognose |
> | `deep purple` | — |
> | `blue` | — |
>
> (Standaard: `teal`)

Wacht op antwoord.

### 7. Genereer de bestanden

Genereer op basis van de antwoorden de volgende bestanden. Toon ze **allemaal als draft** aan de gebruiker voor het wegschrijven (zie stap 8).

---

#### `mkdocs.yml`

```yaml
site_name: <site_name>
site_description: <site_description>
site_url: https://cedanl.github.io/<repo>/
repo_url: https://github.com/cedanl/<repo>
repo_name: cedanl/<repo>
edit_uri: edit/main/docs/

docs_dir: docs
site_dir: site

theme:
  name: material
  language: nl
  logo: assets/logo.png
  favicon: assets/logo.png
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: <kleur>
      accent: <kleur>
      toggle:
        icon: material/brightness-7
        name: Donker thema
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: <kleur>
      accent: <kleur>
      toggle:
        icon: material/brightness-4
        name: Licht thema
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.tabs.link

plugins:
  - search:
      lang: nl
  # Alleen als src-layout met Python code (vraag 3 = ja):
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            docstring_style: google
            show_source: false
            show_root_heading: true
            show_symbol_type_heading: true
            members_order: source

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      # Alleen als Mermaid gewenst (vraag 4):
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.snippets:
      base_path: ["."]
  - admonition
  - pymdownx.details
  - attr_list
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - toc:
      permalink: true
  # Alleen als MathJax gewenst (vraag 4):
  - pymdownx.arithmatex:
      generic: true

# Alleen als MathJax gewenst:
extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Home: index.md
  - Aan de slag: aan-de-slag.md
  # Als src-layout (vraag 3 = ja):
  - API-referentie:
    - api/index.md
```

Pas de nav aan op basis van bestaande `.md` bestanden in `docs/` als die al bestaan.

---

#### `.github/workflows/docs.yml`

Gebruik altijd het twee-job patroon (build + deploy gescheiden), zodat PR's de docs bouwen maar niet deployen:

```yaml
name: Docs

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Install docs dependencies
        run: uv sync --group docs

      - name: Build docs
        run: uv run mkdocs build --strict

      - name: Upload Pages artifact
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

#### `pyproject.toml` — dependency group toevoegen

Voeg toe aan de bestaande `pyproject.toml` (niet vervangen — alleen de groep toevoegen):

```toml
[dependency-groups]
docs = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.26.0",  # alleen als vraag 3 = ja
    "pymdown-extensions>=10.0",
]
```

Als de repo `[project.optional-dependencies]` gebruikt in plaats van `[dependency-groups]`: gebruik dan `[project.optional-dependencies] docs = [...]` en pas het workflow-commando aan naar `uv sync --extra docs`.

---

#### `docs/` structuur aanmaken

```
docs/
├── assets/
│   └── logo.png          ← placeholder, gebruiker vervangt dit
├── index.md              ← homepage
├── aan-de-slag.md        ← getting started
└── api/
    └── index.md          ← alleen als vraag 3 = ja
```

Alleen als MathJax gewenst (vraag 4):
```
docs/javascripts/mathjax.js
```

Met als inhoud:
```javascript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};
```

---

#### Starter `docs/index.md`

```markdown
# <site_name>

<site_description>

## Snel aan de slag

Zie [Aan de slag](aan-de-slag.md) voor installatie-instructies.

## Over dit project

Dit project is onderdeel van de [CEDA](https://github.com/cedanl) organisatie.
```

### 8. Toon de draft en wacht op akkoord

Presenteer een samenvatting van alle te genereren bestanden:

> **MkDocs setup voor `<repo>`**
>
> De volgende bestanden worden aangemaakt of gewijzigd:
>
> - `mkdocs.yml` — siteconfiguratie
> - `.github/workflows/docs.yml` — build + deploy workflow
> - `pyproject.toml` — docs dependency group toegevoegd
> - `docs/index.md`, `docs/aan-de-slag.md` — starter pagina's
> - `docs/assets/` — map voor logo en andere assets
> [+ `docs/api/index.md` als vraag 3 = ja]
> [+ `docs/javascripts/mathjax.js` als MathJax gewenst]
>
> Klopt dit? Zeg wat je wil aanpassen, of geef akkoord om te schrijven.

Wacht op akkoord voor je bestanden schrijft.

### 9. Schrijf de bestanden

Schrijf alle gegenereerde bestanden naar de repo. Wijzig `pyproject.toml` via edit (voeg de dependency group toe, vervang niet de hele file).

### 10. Configureer GitHub Pages

Stel GitHub Pages in om GitHub Actions als bron te gebruiken:

```bash
# Controleer of Pages al geconfigureerd is
gh api repos/cedanl/<repo>/pages 2>/dev/null && echo "exists" || echo "new"

# Als nieuw: activeer Pages met GitHub Actions als bron
gh api repos/cedanl/<repo>/pages \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  -f "build_type=workflow"

# Als al bestaat: zet bron om naar GitHub Actions
gh api repos/cedanl/<repo>/pages \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -f "build_type=workflow"
```

### 11. Rapporteer het resultaat

> **MkDocs setup compleet voor `<repo>`**
>
> **Aangemaakt:**
> - `mkdocs.yml`
> - `.github/workflows/docs.yml`
> - `docs/index.md`, `docs/aan-de-slag.md` [+ extras]
>
> **GitHub Pages:** geconfigureerd op GitHub Actions
> **Live URL (na eerste deploy):** `https://cedanl.github.io/<repo>/`
>
> **Volgende stappen:**
> 1. Vervang `docs/assets/logo.png` met het Npuls-logo (zie `/npuls-huisstijl`)
> 2. Vul `docs/aan-de-slag.md` met installatie-instructies
> 3. Commit en push naar `main` — de workflow deployt automatisch
> 4. Controleer de live site na ~2 minuten op de URL hierboven

## Important

- Gebruik altijd het twee-job patroon voor de workflow (build + deploy gescheiden) — zo bouwen PR's ook de docs zonder te deployen, waardoor je breekbare docs eerder ziet
- Voeg `mkdocstrings` alleen toe als het project een `src/<package>/` layout heeft met Python-functies en Google-style docstrings
- Vervang nooit de volledige `pyproject.toml` — voeg alleen de `[dependency-groups] docs` sectie toe
- GitHub Pages moet op "GitHub Actions" staan als bron, niet op een branch — anders werkt `actions/deploy-pages@v4` niet
- Voor het Npuls-logo: verwijs de gebruiker naar `/npuls-huisstijl`
