# Projectstructuur

Dit overzicht laat zien hoe CEDA-repositories zijn opgebouwd per type toepassing en programmeertaal.

## Typen repositories

### Type 1: Inlees-repository (ingestion)

Zet ruwe bronbestanden (zoals DUO-bekostigingsbestanden, 1CijferHO-leveringen, CSV's of open API's) om naar schone, gevalideerde en gepseudonimiseerde datasets. Andere analysepakketten bouwen voort op deze uitvoer.

### Type 2: Analyse- en toepassingsrepository

Voert een specifieke analyse, voorspelling of benchmark uit op klaargezette data. Levert verrijkte datasets, rapportages en een bijbehorend dashboard op.

### Type 3: Sjabloonrepository (template)

Startpunt voor nieuwe projecten met een kant-en-klare pakketopzet, `.devcontainer/` en teststructuur.

### Type 4: Integratie- en dashboardrepository *(in verkenning)*

Combineert de uitvoer van meerdere pakketten in één overkoepelend overzicht, bijvoorbeeld op het SURF Developer Platform.

---

## Gedeelde afspraken voor alle repositories

### Verplichte bestanden

| Bestand | Doel |
| :--- | :--- |
| `README.md` | Korte uitleg wat het project doet, voor wie het is en hoe je het start. |
| `LICENSE` | Open-sourcelicentie (standaard MIT). |
| `.gitignore` | Taalspecifieke negeerregels plus alle mappen met echte data. |
| `CLAUDE.md` | Technische context en verwijzing naar deze standaarden voor AI-hulpmiddelen. |
| `.devcontainer/` | Reproduceerbare ontwikkelomgeving. |

### Richtlijnen voor `README.md`

De `README.md` is de voordeur van het project. Focus op **relevantie en gebruik**, niet op interne mappenbomen.

**Taal:** Nederlands. Code, functienamen en vaste technische termen mogen in het Engels staan.

**Vaste opbouw:**

1. **Titel en kernzin** — één zin die uitlegt wat het project doet en voor wie.
2. **Visueel voorbeeld** — schermafbeelding of schema van het eindresultaat (dashboard, rapport of tabel), zodat direct duidelijk is wat het oplevert.
3. **Relevantie en context** — welk vraagstuk bij instellingen lost dit op?
4. **Snel aan de slag** — concrete stappen om het project te installeren en met demodata te draaien.
5. **Data** — welke invoer nodig is, waar uitvoer verschijnt en waar het datawoordenboek staat.
6. **Achtergrond en verwijzingen** — links naar inhoudelijke toelichting of aanvullende documentatie.
7. **Contact en bijdragen** — wie aanspreekpunt is en hoe je een issue of verbetering indient.

**Wat hoort niet in de `README.md`?**

- Uitgebreide mappenbomen → zet die in `CLAUDE.md`.
- Diepgaande technische architectuur → zet die in `CLAUDE.md`, `vignettes/` of een eigen docs-map.

### Datamappen

Zie [Dataconventies](data-conventions.md) voor alle details over naamgeving en bestandsformaten.

Kort samengevat werken we met `data/01-raw/`, `data/02-prepared/` en `data/03-output/`. Echte data staat altijd in `.gitignore`. Elke genummerde map bevat wel een `/demo`-submap met synthetische voorbeelddata in git, zodat iedereen het project direct werkend kan uitproberen.

### Opzet voor `CLAUDE.md`

Elke repository bevat een `CLAUDE.md` volgens dit stramien:

```markdown
# Projectnaam

## Overzicht
Korte beschrijving van wat deze repository doet en welke pijplijnstap deze afdekt.

## Standaarden
Volg de technische standaarden van CEDA: https://cedanl.github.io/.github/standards/

## Ontwikkelstack
Programmeertaal, belangrijkste pakketten en hulpmiddelen.

## Projectstructuur
Mappenindeling met korte toelichting per map.

## Uitvoeren
Commando's om afhankelijkheden te installeren en de pijplijn, app en tests te draaien.

## Data
Invoer- en uitvoerformaten, herkomst van velden en aandachtspunten rond privacy.
```

---

## Type 1: Inlees-repository

### R-variant

```text
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
├── R/                          # Pakketfuncties
│   ├── ingest_source.R         # Ruwe bestanden inlezen
│   ├── decode_fields.R         # Vaste breedtes parsen, metadata toepassen
│   ├── validate_data.R         # Kwaliteitscontroles
│   └── export_data.R           # Parquet + CSV wegschrijven
├── inst/
│   ├── app/                    # Shiny-app voor interactief gebruik
│   │   ├── app.R
│   │   └── config.yml          # Lokale datapaden
│   └── metadata/               # Koppeltabellen, referentiedata, data_dictionary.csv
├── data/
│   ├── 01-raw/
│   ├── 02-prepared/
│   └── 03-output/
├── man/                        # Automatisch gegenereerde roxygen2-documentatie
├── tests/
│   └── testthat/
├── main.R                      # Script dat de volledige pijplijn aanstuurt
├── DESCRIPTION
├── NAMESPACE
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
└── renv.lock
```

**Belangrijkste afspraken:**

- Functies in `R/` vormen samen het pakket en heten `werkwoord_onderwerp.R`.
- `main.R` laadt het pakket en draait de pijplijn van begin tot eind.
- De Shiny-app in `inst/app/` biedt een schil rond de pakketfuncties.
- `config.yml` legt lokale datapaden vast zodat gebruikers die maar één keer instellen.
- `renv` beheert pakketversies en `air` verzorgt de code-opmaak.

### Python-variant

```text
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
├── src/
│   └── project_name/           # Installeerbaar Python-pakket
│       ├── __init__.py
│       ├── ingest.py           # Ruwe bestanden inlezen
│       ├── decode.py           # Parsen en omzetten
│       ├── validate.py         # Kwaliteitscontroles
│       ├── export.py           # Parquet + CSV wegschrijven
│       └── metadata/           # Koppeltabellen, referentiedata, data_dictionary.csv
│           ├── __init__.py
│           └── field_definitions.csv
├── app/                        # Streamlit-app voor interactief gebruik
│   ├── main.py                 # Startpunt voor Streamlit
│   ├── pages/                  # Extra pagina's
│   └── config.toml             # Lokale datapaden
├── .streamlit/
│   └── config.toml             # Streamlit-instellingen
├── data/
│   ├── 01-raw/
│   ├── 02-prepared/
│   └── 03-output/
├── tests/
├── pyproject.toml              # Pakketdefinitie + uv- en ruff-instellingen
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
└── uv.lock
```

**Belangrijkste afspraken:**

- De pakketcode staat in `src/project_name/` en is installeerbaar via `uv sync` of `uv pip install -e .`.
- Metadata (koppeltabellen en velddefinities) zit **in** het pakket onder `src/project_name/metadata/` en wordt geladen via `importlib.resources`.
- `app/main.py` is het startpunt voor Streamlit en roept alleen functies uit het pakket aan.
- `uv` beheert afhankelijkheden en `ruff` controleert en formatteert de code.

---

## Type 2: Analyse- en toepassingsrepository

### R-variant

```text
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── R/                          # Pakketfuncties
│   ├── prepare_data.R          # Invoerdata laden en koppelen
│   ├── transform_data.R        # Kenmerken afleiden en verrijken
│   ├── run_analysis.R          # Kernanalyse of model
│   ├── create_plots.R          # Visualisatiefuncties
│   └── render_report.R         # Rapportgeneratie
├── inst/
│   ├── app/                    # Shiny-app voor interactief gebruik
│   │   ├── app.R
│   │   └── config.yml
│   ├── metadata/               # Koppeltabellen, referentiedata, data_dictionary.csv
│   └── templates/              # Rapportsjablonen (Quarto .qmd)
├── data/
│   ├── 01-raw/                 # Schone invoer vanuit inlees-pakketten
│   ├── 02-prepared/
│   └── 03-output/
├── man/
├── tests/
│   └── testthat/
├── vignettes/                  # Uitgebreide gebruiksvoorbeelden
├── main.R                      # Pijplijn-aansturing
├── DESCRIPTION
├── NAMESPACE
├── CLAUDE.md
├── README.md
├── LICENSE
├── .gitignore
└── renv.lock
```

### Python-variant

```text
project-name/
├── .devcontainer/
│   └── devcontainer.json
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── prepare.py          # Invoerdata laden en koppelen
│       ├── transform.py        # Kenmerken afleiden
│       ├── analyze.py          # Kernanalyse of model
│       ├── visualize.py        # Grafiekfuncties
│       ├── export.py           # Uitvoer wegschrijven
│       └── metadata/           # Opzoektabellen, variabelen, data_dictionary.csv
│           ├── __init__.py
│           ├── variabelen.csv
│           └── levels.csv
├── app/                        # Streamlit-app
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

---

## Type 3: Sjabloonrepository

Sjabloonrepositories bevatten dezelfde basisopzet met vooraf ingevulde configuratie voor tests, linting en devcontainers, zodat nieuwe projecten direct op de standaard starten.
