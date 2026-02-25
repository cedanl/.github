# Migration: Cookiecutter Data Science to CEDA Package Standard

Guide for migrating existing repos (e.g., Uitnodigingsregel, studentprognose) from cookiecutter data science layout to the CEDA package standard.

## Key Differences

| Cookiecutter | CEDA Package Standard | Why |
|---|---|---|
| `module/` or `scripts/` (loose files) | `src/project_name/` (installable package) | Reusable across repos, testable, proper imports |
| `data/raw/`, `data/interim/`, `data/processed/` | `data/01-raw/`, `data/02-prepared/`, `data/03-output/` | Numbered prefixes show pipeline order, consistent across repos |
| No interactive interface | `app/` with Streamlit | Non-programmers can use the tool |
| `Makefile` for orchestration | `main.py` + `Makefile` (optional) | Keep Makefile if useful, but `main.py` is the primary entrypoint |
| Config in loose files | `config.toml` in `app/` + metadata inside package | Config for app separately, reference data travels with the package |
| No devcontainer | `.devcontainer/` | Reproducible environment for all contributors |

## What to Keep from Cookiecutter

- Numbered data stages (already a similar concept)
- Separation of notebooks from source code
- `Makefile` as optional convenience (for CLI shortcuts like `make test`, `make lint`)

## Migration Steps

1. Move `module/` or `scripts/` code into `src/project_name/` with proper `__init__.py`
2. Add `[project]` section to `pyproject.toml` if not already a proper package
3. Move metadata/config files into `src/project_name/metadata/`
4. Add `app/` with Streamlit wrapper
5. Add `.devcontainer/`
6. Rename data directories to numbered scheme
7. Add demo data in `data/XX-stage/demo/` subfolders
