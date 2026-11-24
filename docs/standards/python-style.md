---
icon: lucide/code-xml
---

# Python-stijlgids

Deze stijlgids beschrijft hoe wij Python-code schrijven in CEDA-repositories. We bouwen voort op PEP 8 met vaste keuzes voor onderwijsdata-analyse.

## Ecosysteem

### Vaste ontwikkeltools

| Hulpmiddel | Doel |
| :--- | :--- |
| `uv` | Pakket- en omgevingsbeheer (vervangt losse `pip`-, `venv`- en `pyenv`-stappen). |
| `ruff` | Linting én automatische code-opmaak (vervangt `flake8`, `black` en `isort`). |
| `pytest` | Automatische tests. |
| `quarto` | Reproduceerbare rapportages en documentatie. |

### Voorkeurspakketten

| Domein | Pakket | Toelichting |
| :--- | :--- | :--- |
| Dataframes (standaard) | `polars` | Snel, zuinig met geheugen en een consistente keten-API. |
| Dataframes (uitwisseling) | `pandas` | Wanneer een gekoppeld pakket (zoals `scikit-learn`) daarom vraagt. |
| Data opschonen | `pyjanitor` | Handige hulpfuncties zoals `clean_names()`. |
| Visualisatie (interactief) | `plotly` | Interactieve grafieken in dashboards. |
| Visualisatie (statisch) | `matplotlib`, `seaborn` | Vaste figuren voor rapporten. |
| Modelleren | `scikit-learn` | Classificatie, regressie en evaluatie. |
| Webapplicatie | `streamlit` | Interactieve schil voor gebruikers bij instellingen. |
| Opdrachtregel (CLI) | `typer`, `rich` | Duidelijke commando's en voortgangsweergave in de terminal. |
| Bestandsformaten | `pyarrow`, `fastexcel` | Inlezen en wegschrijven van Parquet en Excel. |
| Configuratie | `tomllib`, `pyyaml` | Uitlezen van TOML- en YAML-configuratie. |

Zie ook [Ontwikkelprincipes §11](principles.md#11-keuze-van-afhankelijkheden) voor het afwegen van nieuwe afhankelijkheden.

## Pakketopbouw

Elke Python-repository is een installeerbaar pakket onder `src/`. Zie [Projectstructuur](project-structure.md) voor de volledige mappenboom.

### `pyproject.toml`

`pyproject.toml` is de enige bron voor pakketmetadata, afhankelijkheden en tool-instellingen:

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Heldere beschrijving in één zin"
requires-python = ">=3.13"
dependencies = [
    "polars>=1.0",
    "streamlit>=1.40",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
]

[tool.uv]
cache-dir = "./.uv_cache"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Metadata binnen het pakket uitlezen

Referentietabellen en het datawoordenboek staan in `src/project_name/metadata/` (met een eigen `__init__.py`), zodat ze altijd met het pakket meereizen:

```python
from importlib.resources import files
import polars as pl


def load_variable_definitions() -> pl.DataFrame:
    """Laad variabelendefinities vanuit de pakketmetadata."""
    path = files("project_name.metadata") / "variabelen.csv"
    return pl.read_csv(str(path), separator=";")
```

### `main.py` (startpunt van de pijplijn)

```python
"""Startpunt voor de datapijplijn van project-name."""
from project_name.analyze import run_analysis
from project_name.export import export_results
from project_name.prepare import prepare_data
from project_name.transform import transform_data


def main() -> None:
    df = prepare_data("data/01-raw/")
    df = transform_data(df)
    results = run_analysis(df)
    export_results(results, "data/03-output/")


if __name__ == "__main__":
    main()
```

## Schrijfstijl en syntaxis

### Type-annotaties

Voorzie alle functieparameters en retourwaarden van type-annotaties:

```python
# Goed
def transform_data(
    df: pl.DataFrame,
    target_year: int,
    min_credits: int = 0,
    include_masters: bool = False,
) -> pl.DataFrame:
    ...

# Vermijden
def transform_data(df, target_year, min_credits=0, include_masters=False):
    ...
```

- Gebruik moderne unie-notatie (`str | None` in plaats van `Optional[str]`).
- Gebruik kleine letters voor collectietypen (`list[str]`, `dict[str, int]`).
- Annoteer lokale variabelen alleen waar dat echt verduidelijkt.

### Docstrings

Schrijf docstrings in Google-stijl:

```python
def process_chunk(
    positions: list[tuple[int, int]],
    chunk: list[str],
) -> list[str]:
    """Zet regels met vaste kolombreedtes om naar puntkomma-gescheiden tekst.

    Args:
        positions: Lijst met (start, eind)-posities per veld.
        chunk: Invoerregels om te verwerken.

    Returns:
        Lijst met puntkomma-gescheiden regels.
    """
```

### Databewerking met Polars

Geef de voorkeur aan Polars met overzichtelijke methodeketens tussen haakjes:

```python
students = (
    df.filter(pl.col("INS_Studiejaar") >= 2020)
    .select(["INS_Studentnummer", "INS_Opleidingsnaam", "retentie"])
    .with_columns(
        pl.col("retentie").cast(pl.Int8).alias("retentie_int"),
    )
)

# Zet alleen op de grens naar een ander pakket om naar pandas
students_pd = students.to_pandas()
```

### Naamgeving en imports

- Functies en variabelen in `snake_case`, klassen in `PascalCase`, constanten in `UPPER_SNAKE_CASE`.
- Laat functienamen beginnen met een werkwoord (`prepare_data()`, `validate_schema()`, `export_results()`).
- Gebruik altijd `pathlib.Path` in plaats van losse tekenreeks-paden of `os.path`.
- Laat `ruff` de volgorde van imports bewaken (standaardbibliotheek, externe pakketten, eigen pakket).

### Foutafhandeling en configuratie

Valideer invoer aan het begin van een functie en geef specifieke foutmeldingen terug:

```python
import tomllib
from pathlib import Path
import polars as pl


def load_config(config_path: Path = Path("app/config.toml")) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Configuratiebestand ontbreekt: {config_path}")
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def load_input_data(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Invoerbestand niet gevonden: {path}")
    if path.suffix not in (".csv", ".parquet"):
        raise ValueError(f"Niet-ondersteund bestandsformaat: {path.suffix}")

    return pl.read_csv(path, separator=";")
```

## Automatisch testen

Spiegel de opbouw van `src/` onder `tests/` (`src/project_name/transform.py` krijgt `tests/test_transform.py`) en voer tests uit met `uv run pytest`:

```python
import polars as pl
import pytest
from project_name.transform import transform_data


@pytest.fixture
def sample_data() -> pl.DataFrame:
    return pl.DataFrame({
        "INS_Studiejaar": [2025, 2026, 2026],
        "INS_Studentnummer": ["001", "002", "003"],
        "retentie": [1, 0, 1],
    })


def test_transform_filters_by_year(sample_data: pl.DataFrame) -> None:
    result = transform_data(sample_data, target_year=2026)
    assert result.height == 2


def test_transform_raises_on_empty() -> None:
    empty = pl.DataFrame({"INS_Studiejaar": [], "retentie": []})
    with pytest.raises(ValueError, match="Geen data"):
        transform_data(empty, target_year=2026)
```

## Interactieve applicatie (`app/`)

De Streamlit- of Shiny-voor-Python-app staat **buiten** `src/` in een eigen map `app/`:

- Zowel `streamlit run` als `shiny run` verwacht een bestandspad als startpunt.
- De app bevat **geen** rekenlogica en roept uitsluitend functies uit `src/project_name/` aan.
- Lokale bestandspaden staan in `app/config.toml`.

## Beheer van afhankelijkheden

- Leg pakketten vast in `pyproject.toml` en commit altijd `uv.lock` én `.python-version`.
- Zet `.uv_cache/` in `.gitignore`.
