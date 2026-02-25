# CEDA Project Structure

How cedanl repositories are organized, by type and language.

## Repository Types

### Type 1: Ingestion Repository

Transforms raw data sources (DUO fixed-width files, CSVs, APIs) into clean, research-ready formats. Other repos depend on ingestion repo output.


### Type 2: Analysis / Use-Case Repository

Focuses on analysis (and therefore includes specific preparation). Produces data enriched with predictions, analytical results, reports, and visualizations.

### Type 3: Template Repository

Starting points for new projects. Contains devcontainer configurations, boilerplate, and example code.

### Type 4: Integration / Dashboard Repository *(future)*

Combines outputs from multiple repos into unified "management" interfaces or dashboards. Runs on SURF Developer Platform. This needs to be explored further.

---

## Shared Standards (All Repos)

### Required files

| File | Purpose |
|------|---------|
| `README.md` | What the repo does, how to install, how to run |
| `LICENSE` | MIT license |
| `.gitignore` | Language-appropriate ignores + data files |
| `CLAUDE.md` | AI assistant context, references org standards |
| `.devcontainer/` | Reproducible dev environment |

### README richtlijnen

De README is het visitekaartje van het project — gericht op **relevantie en gebruiksinstructies**, niet op technische repo-structuur.

**Taal:** Nederlands. Code, variabelenamen en technische termen mogen in het Engels.

**Opbouw:**

1. **Titel en korte beschrijving** — één zin die uitlegt wat het project doet en voor wie
2. **Visueel voorbeeld** — screenshot, GIF of diagram dat het eindresultaat toont (dashboard, rapport, tabel). Niet decoratief maar functioneel: het moet duidelijk maken wat het project oplevert
3. **Relevantie / context** — waarom dit project bestaat, welk probleem het oplost, wie de doelgroep is
4. **Snel starten** — stappen om het project te installeren en te draaien (dependencies, data, commando's)
5. **Data** — welke input nodig is, waar output terechtkomt, verwijzing naar data dictionary
6. **Contact / bijdragen** — wie verantwoordelijk is, hoe bij te dragen

**Wat niet in de README hoort:**
- Gedetailleerde projectstructuur (directory tree) → verplaats naar `CLAUDE.md` of `docs/`
- Technische architectuurdocumentatie → verplaats naar `docs/architecture.md`
- Uitgebreide API-documentatie → verplaats naar `docs/` of gegenereerde docs

### Data directories

See [Data Conventions](data-conventions.md) for full details on data directory structure, file formats, and naming.

In short: `data/01-raw/`, `data/02-prepared/`, `data/03-output/` with numbered prefixes per pipeline step. Data directories are in `.gitignore`, but each numbered folder has a `/demo` subfolder with synthetic data committed to git — making the repo a standalone working product.

### CLAUDE.md template

Every repo should have a `CLAUDE.md` that includes:

```markdown
# Project Name

## Overview
Brief description of what this repo does and which pipeline stage it covers.

## Standards
Follow CEDA technical standards: https://github.com/cedanl/.github/tree/main/standards/README.md

## Tech Stack
Language, key packages, tooling.

## Project Structure
Directory layout with brief descriptions.

## How to Run
Commands to install dependencies and run the pipeline / app.

## Data
Input/output formats, where data comes from, privacy notes.
```

---

## Type 1: Ingestion Repository

### R Variant

```
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
├── R/                          # Package functions
│   ├── ingest_source.R         # Read raw files
│   ├── decode_fields.R         # Parse fixed-width, apply metadata
│   ├── validate_data.R         # Quality checks
│   └── export_data.R           # Write Parquet + CSV output
├── inst/
│   ├── app/                    # Shiny app for interactive mode
│   │    ├── app.R
│   │    └── config.yml         # Fixed config for local data paths
│   └── metadata/               # Add additional mapping tables / reference data
├── data/
│   ├── 01-raw/
│   ├── 02-prepared/
│   └── 03-output/
├── man/                        # Auto-generated roxygen2 docs
├── tests/
│   └── testthat/
├── main.R                      # Pipeline orchestration script
├── DESCRIPTION
├── NAMESPACE
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
└── renv.lock
```

**Key conventions:**
- Functions in `R/` are the package — named as `verb_object.R`
- `main.R` sources the package and runs the pipeline end-to-end
- Shiny app in `inst/app/` wraps package functions with a UI
- `config.yml` in the app defines local data paths — users only need to set paths once
- `renv` manages dependencies

### Python Variant

```
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
├── src/
│   └── project_name/           # Package (pip-installable)
│       ├── __init__.py
│       ├── ingest.py           # Read raw files
│       ├── decode.py           # Parse and transform
│       ├── validate.py         # Quality checks
│       ├── export.py           # Write Parquet + CSV output
│       └── metadata/           # Mapping tables, reference data (inside package)
│           ├── __init__.py
│           └── field_definitions.csv
├── app/                        # Streamlit app for interactive mode
│   ├── main.py                 # Streamlit entrypoint
│   ├── pages/                  # Multi-page app
│   └── config.toml             # Fixed config for local data paths
├── .streamlit/
│   └── config.toml             # Streamlit settings
├── data/
│   ├── 01-raw/
│   ├── 02-prepared/
│   └── 03-output/
├── tests/
├── pyproject.toml              # Package definition + uv config
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
└── uv.lock
```

**Key conventions:**
- Package code lives in `src/project_name/` — installable via `uv pip install -e .`
- Metadata (mapping tables, field definitions) lives **inside** the package at `src/project_name/metadata/` — accessible via `importlib.resources`
- `app/main.py` is the Streamlit entrypoint — wraps package functions
- `uv` for dependency management, `ruff` for linting/formatting
- `config.toml` in the app defines local data paths

---

## Type 2: Analysis / Use-Case Repository

### R Variant

```
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── R/                          # Package functions
│   ├── prepare_data.R          # Load and merge input data
│   ├── transform_data.R        # Feature engineering, enrichment
│   ├── run_analysis.R          # Core analysis / modeling
│   ├── create_plots.R          # Visualization functions
│   └── render_report.R         # Report generation
├── inst/
│   ├── app/                    # Shiny app for interactive mode
│   │   ├── app.R
│   │   └── config.yml
│   ├── metadata/
│   └── templates/              # Report templates (Quarto/Rmd)
├── metadata/                   # Lookup tables, variable definitions
├── data/
│   ├── 01-raw/                 # Input from ingestion repos
│   ├── 02-prepared/
│   └── 03-output/
├── man/
├── tests/
│   └── testthat/
├── vignettes/                  # Usage documentation
├── main.R                      # Pipeline orchestration
├── DESCRIPTION
├── NAMESPACE
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
└── renv.lock
```

**Key conventions:**
- Input data comes from ingestion repos (placed in `data/01-raw/`)
- `metadata/` holds lookup tables, variable definitions, configuration
- Report templates (Quarto `.qmd` or Rmarkdown) live in `inst/templates/`
- Shiny app lets users select parameters and run the analysis interactively

### Python Variant

```
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── prepare.py          # Load and merge input data
│       ├── transform.py        # Feature engineering
│       ├── analyze.py          # Core analysis / modeling
│       ├── visualize.py        # Plotting functions
│       ├── export.py           # Output generation
│       └── metadata/           # Lookup tables, variable definitions (inside package)
│           ├── __init__.py
│           ├── variabelen.csv
│           └── levels.csv
├── app/                        # Streamlit app
│   ├── main.py
│   ├── pages/
│   └── config.toml
├── .streamlit/
│   └── config.toml
├── data/
│   ├── 01-raw/
│   ├── 02-prepared/
│   └── 03-output/
├── tests/
├── pyproject.toml
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
└── uv.lock
```

**Key conventions:**
- Same package + app pattern as ingestion repos
- Metadata (lookup tables, variable definitions) lives **inside** the package at `src/project_name/metadata/` — accessible via `importlib.resources`
- Streamlit app lets users configure analysis parameters and view results

---

## Type 3: Template Repository

Templates provide starting points. They contain the earlier discussed directories.
