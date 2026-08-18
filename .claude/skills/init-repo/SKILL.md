---
name: init-repo
description: Initialize a new cedanl repository with the correct CEDA project structure. Use when starting a new project, creating a new repo, or scaffolding a repository. LET OP — voor een repo die al bestaat en alleen de projectinstructies mist is er `cedafy-claude-md`.
---

# Initialize CEDA Repository

Scaffold a new cedanl repository following CEDA technical standards.

## Workflow

When the user invokes `/init-repo [optional: project name]`:

## Starter .devcontainer templates

For every new repo, a minimal .devcontainer folder is created for Python and R:

| Question | Options |
|----------|---------|
| Project name? | snake_case name (e.g., `instroomprognose_mbo`) |
| Repository type? | 1: Ingestion, 2: Analysis/Use-Case, 3: Template |
| Language? | R, Python |
| One-line description? | Free text |

**.devcontainer/Dockerfile**
```
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m vscode
USER vscode
WORKDIR /workspace
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:${PATH}"
```

**.devcontainer/devcontainer.json**
```
{
  "name": "python-uv-dev",
  "build": { "dockerfile": "Dockerfile" },
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "anthropic.claude-code",
    "n4eth.ty-type-checker"
  ],
  "postCreateCommand": "uv sync && uv pip install ty",
  "forwardPorts": [8501],
  "remoteUser": "vscode",
  "settings": {
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
  }
}
```

### R

**.devcontainer/Dockerfile**
```
FROM rocker/tidyverse:latest
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    curl \
    vim \
    git \
    build-essential \
    cmake \
    libnode-dev \
    libffi-dev \
    zlib1g-dev \
    libgit2-dev \
    && rm -rf /var/lib/apt/lists/*
USER rstudio
WORKDIR /workspace
```

**.devcontainer/devcontainer.json**
```
{
  "name": "R Dev Container",
  "build": { "dockerfile": "Dockerfile" },
  "remoteUser": "rstudio",
  "settings": {},
  "extensions": [ "REditorSupport.r" ],
  "postCreateCommand": "Rscript -e 'install.packages(c(\"devtools\", \"usethis\", \"pak\", \"renv\"), repos=\"https://cran.rstudio.com/\")'"
}
```


project-name/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
├── data/
│   ├── 01-raw/
│   │   └── demo/
│   ├── 02-prepared/
│   │   └── demo/
│   └── 03-output/
│       └── demo/
├── CLAUDE.md
├── README.md
├── LICENSE
└── .gitignore
```

#### R repos additionally get:

```
├── R/                          # Package functions
├── inst/
│   ├── app/
│   │   ├── app.R
│   │   └── config.yml
│   └── metadata/
├── man/
├── tests/
│   └── testthat/
├── main.R
├── DESCRIPTION
├── NAMESPACE
└── renv.lock
```

#### Python repos additionally get:

```
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── metadata/
│           └── __init__.py
├── app/
│   ├── main.py
│   └── config.toml
├── .streamlit/
│   └── config.toml
├── tests/
├── pyproject.toml
├── .python-version
└── uv.lock
```

### 4. Generate file contents

#### CLAUDE.md

Do not write this one by hand. Fetch the org baseline and fill in its `<...>` slots:

```bash
gh api repos/cedanl/.github/contents/werkafspraken/_claude-md-template.md --jq .content | base64 -d
```

Fill the slots from the answers in step 1 and the structure you just generated: one line on
what this is, the stack and package manager, and the run/test/lint commands for the chosen
language. Leave the `## Valkuilen` section empty — it grows per repository, on evidence.

Do **not** add a module map, an architecture description, or code style rules. Claude reads
those from the code itself, style is a linter's job, and every line in this file is loaded in
every session — a longer file means a file that gets half ignored.

An existing repository that does not have this baseline yet is a job for `/cedafy-claude-md`,
not for this skill.

#### README.md

```markdown
# [Project Name]

[description]

## Installation

[language-specific install instructions]

## Usage

[how to run the pipeline and the interactive app]

## Development

[devcontainer instructions, how to run tests]

## License

MIT
```

#### .gitignore

Generate language-appropriate ignores:
- R: `.Rproj.user`, `renv/library/`, `data/01-raw/*`, `data/02-prepared/*`, `data/03-output/*`, `!data/*/demo/`
- Python: `__pycache__/`, `.venv/`, `.uv_cache/`, `data/01-raw/*`, `data/02-prepared/*`, `data/03-output/*`, `!data/*/demo/`

#### LICENSE

MIT license with current year and "cedanl" as copyright holder.

#### .devcontainer/devcontainer.json

- R: use `ghcr.io/rocker-org/devcontainer/r-ver` image with R extensions
- Python: use `mcr.microsoft.com/devcontainers/python` image with Python extensions

#### R-specific files

- **DESCRIPTION**: package metadata with `Imports:` and `Suggests:` (shiny in Suggests)
- **NAMESPACE**: empty, to be generated by roxygen2
- **main.R**: `devtools::load_all()` + pipeline skeleton
- **R/run_app.R**: `run_app()` function using `system.file("app", package = "...")`
- **inst/app/app.R**: minimal Shiny app skeleton calling package functions
- **inst/app/config.yml**: paths to data directories

#### Python-specific files

- **pyproject.toml**: full config with `[project]`, `[tool.uv]`, `[tool.ruff]`, `[tool.pytest]`, `[tool.ty]` (type hints via ty)
- **src/project_name/__init__.py**: package docstring + version
- **app/main.py**: minimal Streamlit app skeleton calling package functions
- **app/config.toml**: paths to data directories
- **.python-version**: `3.13`

### 5. Type-specific starter functions

#### Type 1 (Ingestion)

Create skeleton functions:
- R: `R/ingest_source.R`, `R/decode_fields.R`, `R/validate_data.R`, `R/export_data.R`
- Python: `src/project_name/ingest.py`, `decode.py`, `validate.py`, `export.py`

#### Type 2 (Analysis)

Create skeleton functions:
- R: `R/prepare_data.R`, `R/transform_data.R`, `R/run_analysis.R`, `R/create_plots.R`
- Python: `src/project_name/prepare.py`, `transform.py`, `analyze.py`, `visualize.py`, `export.py`

### 6. Initialize tooling

- R: `renv::init()` if R is available
- Python: `uv init`, `uv sync`, and `uv pip install ty` if uv is available (ty is used for checking and generating type hints, see https://github.com/n4eth/ty)
- Git: `git init` if not already a git repo

### 7. Report result

Show the created structure and suggest next steps:

```
## Created: [project-name]

**Type:** [Ingestion/Analysis] | **Language:** [R/Python]

[tree output of created structure]

### Next steps
1. Add your data to `data/01-raw/` (and demo data to `data/01-raw/demo/`)
2. Implement the skeleton functions in [R/ or src/]
3. Configure data paths in [config file]
4. Run `/check-style` when ready to verify standards compliance
```

## Important

- Always create demo subdirectories in each data folder
- Data directories are gitignored except `/demo` subfolders
- The interactive app (Shiny/Streamlit) should contain NO business logic
- Follow naming conventions from the relevant style guide
- Reference `/check-style` for post-creation validation
