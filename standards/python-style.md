# CEDA Python Style Guide

Python coding standards for cedanl repositories. Based on PEP 8 with CEDA-specific conventions for educational data analytics.

## Ecosystem

### Tooling

| Tool | Purpose |
|------|---------|
| `uv` | Package and dependency management (replaces pip, venv, pyenv) |
| `ruff` | Linting AND formatting (replaces flake8, black, isort) |
| `pytest` | Testing |
| `quarto` | Reports and documentation |

### Preferred packages

| Domain | Package | Notes |
|--------|---------|-------|
| DataFrames (large) | polars | Fast, memory-efficient, consistent API |
| DataFrames (interop) | pandas | When libraries require pandas input |
| Data cleaning | pyjanitor | `clean_names()`, chaining methods |
| Visualization | plotly | Interactive plots for dashboards |
| Visualization (static) | matplotlib, seaborn | For reports |
| Modeling | scikit-learn | Classification, regression, evaluation |
| Web interface | streamlit | Interactive app mode |
| CLI | typer | When command-line interface is needed |
| Console output | rich | Progress bars, formatted output |
| File formats | pyarrow, fastexcel | Parquet and Excel I/O |
| Configuration | pyyaml, tomli | YAML/TOML config parsing |

See [Principles §11](principles.md#11-dependency-selection) for general dependency selection criteria.

## Package Structure

Every Python repo is an installable package. See [Project Structure](project-structure.md) for full directory layouts per repo type.

### pyproject.toml

Single source of truth for package metadata, dependencies, and tool configuration:

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Clear one-line description"
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

### Accessing package metadata

Metadata files (CSVs, Excel lookups) live inside the package so they travel with it:

```python
from importlib.resources import files

def load_variable_definitions():
    """Load variable definitions from package metadata."""
    path = files("project_name.metadata") / "variabelen.csv"
    return pl.read_csv(str(path), separator=";")
```

For this to work, include `metadata/` inside `src/project_name/` with an `__init__.py`.

### main.py (CLI entrypoint)

```python
"""Pipeline entrypoint for project-name."""
from project_name.prepare import prepare_data
from project_name.transform import transform_data
from project_name.analyze import run_analysis
from project_name.export import export_results


def main() -> None:
    df = prepare_data("data/01-raw/")
    df = transform_data(df)
    results = run_analysis(df)
    export_results(results, "data/03-output/")


if __name__ == "__main__":
    main()
```

## Syntax

### Type hints

Use type hints for function signatures. They serve as documentation and enable static analysis:

```python
## Good
def transform_data(
    df: pl.DataFrame,
    target_year: int,
    min_credits: int = 0,
    include_masters: bool = False,
) -> pl.DataFrame:
    ...

## Bad
def transform_data(df, target_year, min_credits=0, include_masters=False):
    ...
```

- All function parameters and return types annotated
- Use `str | None` (union syntax) over `Optional[str]`
- Use `list[str]` over `List[str]` (lowercase generics, Python 3.10+)
- Don't annotate every local variable — only where it adds clarity

### Docstrings

Use Google-style docstrings:

```python
def process_chunk(
    positions: list[tuple[int, int]],
    chunk: list[str],
) -> list[str]:
    """Process a chunk of fixed-width lines into CSV format.

    Converts fixed-width lines into semicolon-delimited strings
    based on field position definitions.

    Args:
        positions: List of (start, end) tuples defining field boundaries.
        chunk: Lines to process, as strings or bytes.

    Returns:
        List of semicolon-delimited strings, one per input line.

    Example:
        >>> process_chunk([(0, 5), (5, 10)], ["abc  def  "])
        ['abc;def']
    """
```

- First line: short summary (one sentence, imperative mood)
- Body: additional context when needed
- Args: every parameter documented
- Returns: what comes back
- Example: when the behavior isn't obvious

### Data manipulation with Polars

Prefer Polars for data operations. Its API is consistent and explicit:

```python
# Good: Polars method chaining
students = (
    df.filter(pl.col("INS_Studiejaar") >= 2020)
    .select(["INS_Studentnummer", "INS_Opleidingsnaam", "retentie"])
    .with_columns(
        pl.col("retentie").cast(pl.Int8).alias("retentie_int"),
    )
)

# When pandas is required (e.g., for scikit-learn input)
students_pd = students.to_pandas()
```

- Use method chaining with parenthesized expressions
- Explicit column selection with `pl.col()`
- Use `.alias()` for derived columns
- Convert to pandas only at the boundary where a library requires it

### When to use Pandas

- Libraries that require pandas input (scikit-learn, some plotting libraries)
- Small, simple operations where Polars overhead isn't justified
- When reading Excel files (via openpyxl/fastexcel, then convert to Polars)

### Naming

Follow PEP 8:

```python
# Good
def calculate_retention_rate(df: pl.DataFrame, year: int) -> float:
    enrollment_count = df.filter(pl.col("year") == year).height
    ...

class StudentDataPipeline:
    MAX_RETRY_COUNT = 3
    ...

# Bad
def calcRetRate(df, y):
    ec = df.filter(pl.col("year") == y).height
    ...
```

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Function names start with a verb: `prepare_data()`, `validate_schema()`, `export_results()`
- Descriptive names — when in doubt, longer is better than short

### Imports

```python
# Good: organized imports
from __future__ import annotations

import json
from pathlib import Path

import polars as pl
from loguru import logger

from project_name.prepare import prepare_data
from project_name.metadata import load_variable_definitions
```

- Standard library first, then third-party, then local (ruff handles this via `isort` rules)
- Use `from pathlib import Path` — prefer `Path` over `os.path`
- Import specific names, not entire modules (except for `polars as pl`, `pandas as pd`, `numpy as np`)

### Error handling

```python
# Good: specific errors, early validation
def load_input_data(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.suffix not in (".csv", ".parquet"):
        raise ValueError(f"Unsupported format: {path.suffix}")

    return pl.read_csv(path, separator=";")

# Bad: catch-all, no validation
def load_input_data(path):
    try:
        return pl.read_csv(str(path), separator=";")
    except Exception:
        return None
```

- Validate inputs at function boundaries (guard clauses)
- Raise specific exceptions with descriptive messages
- Never catch bare `Exception` unless re-raising

### Configuration

```python
# Good: config separate from logic
import tomllib
from pathlib import Path

def load_config(config_path: Path = Path("app/config.toml")) -> dict:
    with open(config_path, "rb") as f:
        return tomllib.load(f)

config = load_config()
input_path = Path(config["paths"]["input"])
```

- Use TOML for configuration (native Python 3.11+ support)
- Keep configuration files in `app/` (for Streamlit) or project root
- Never hardcode file paths — use config or arguments
- Use `pathlib.Path` for all path handling

## Testing

```python
# tests/test_transform.py
import polars as pl
import pytest
from project_name.transform import transform_data


@pytest.fixture
def sample_data():
    return pl.DataFrame({
        "INS_Studiejaar": [2023, 2024, 2024],
        "INS_Studentnummer": ["001", "002", "003"],
        "retentie": [1, 0, 1],
    })


def test_transform_filters_by_year(sample_data):
    result = transform_data(sample_data, target_year=2024)
    assert result.height == 2
    assert all(result["INS_Studiejaar"].to_list() == [2024, 2024])


def test_transform_raises_on_empty():
    empty = pl.DataFrame({"INS_Studiejaar": [], "retentie": []})
    with pytest.raises(ValueError, match="No data"):
        transform_data(empty, target_year=2024)
```

- Test file mirrors source: `src/project_name/transform.py` → `tests/test_transform.py`
- Use fixtures for test data
- Test expected outputs, edge cases, and error conditions
- Run with `uv run pytest`

## Interactive App (Streamlit or Shiny for Python)

The app lives **outside** the package in `app/`. This is different from R, where the app lives inside the package (`inst/app/`). The reason: both `streamlit run` and `shiny run` require a file path, not a Python module.

### Key conventions (both frameworks)

- App in `app/` directory — NOT inside `src/project_name/`
- App contains NO business logic — only UI and calls to package functions
- `config.toml` in `app/` for local data paths
- Keep the app thin — orchestration and presentation only

## Dependency Management

- `pyproject.toml` defines dependencies
- `uv.lock` locks exact versions (commit to git)
- `.python-version` pins the Python version
- Don't commit `.uv_cache/`
