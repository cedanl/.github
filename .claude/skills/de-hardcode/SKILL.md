---
name: de-hardcode
description: Find hardcoded values in a cedanl repository and move them into config, package metadata, or function parameters following CEDA standards. Use when moving a project from POC to MVP, when values are baked into scripts or the app, or when the user asks to make code configurable, flexible, or "not hardcoded".
---

# De-hardcode: Extract Hardcoded Values

> **⚠️ v0.1 — experimenteel.** Deze skill is nieuw en nog niet in de praktijk getest. Behandel de bevindingen kritisch, controleer elke wijziging, en meld wat er misgaat zodat de skill verbeterd kan worden. Voer niets blind uit.

Move hardcoded values out of scripts and the app layer into their correct home, following the CEDA principle **"Extract hard-coded values into configuration"** (Principle 9, Extensibility). This is the concrete POC → MVP step: the code keeps doing the same thing, but paths, cohorts, lookup tables and settings stop being baked in.

This skill only supports **cedanl repositories** that already roughly follow the CEDA package structure. If the repo is not a package yet (loose scripts, cookiecutter layout), say so and suggest `/migrate-cookiecutter` or `/init-repo` first — then stop. Do not restructure the repo yourself.

## The three destinations

Every hardcoded value goes to exactly one home. Sorting each value correctly is the core of this skill.

| Bucket | What it is | Destination |
|--------|-----------|-------------|
| **A — Config** | Local paths, run settings, environment-dependent values | `app/config.toml` (Python) / `inst/app/config.yml` (R) |
| **B — Reference data** | Lookup/mapping tables typed as code (code→label dicts, level labels, field definitions) | package metadata: `src/project_name/metadata/*.csv` (Python) / `inst/metadata/*.csv` (R) |
| **C — Parameter** | Values that vary per run or per caller (cohort year, threshold, filter value) | a **function parameter** with a sensible default |
| **(secrets)** | API keys, tokens, connection strings, passwords | flag only → move to `.env`, confirm `.env` is in `.gitignore` |

**How to decide A vs B vs C:**

- Is it *data that a domain expert would want to edit* (a mapping with many rows, labels, definitions)? → **B**, a CSV in `metadata/`. It is data, not a setting — it must not go in `config.toml`.
- Is it *where something lives on this machine* or a fixed run setting? → **A**, config.
- Does it *change the behaviour of the logic per run/caller* (which year, which cutoff)? → **C**, a function parameter. Often A and C combine: the function gets the parameter, and `config.toml` supplies the default that `main.py` / the app passes in. Prefer C over A when the value is logic-driven rather than environment-driven.

## Phase 1: Confirm structure and scope

Detect language and confirm CEDA layout:

```bash
ls pyproject.toml src/ app/ 2>/dev/null        # Python indicators
ls DESCRIPTION NAMESPACE R/ inst/ 2>/dev/null   # R indicators
```

- Python → config in `app/config.toml`, metadata in `src/<project>/metadata/`
- R → config in `inst/app/config.yml`, metadata in `inst/metadata/`

If neither layout is present, report that this repo needs structuring first and suggest `/migrate-cookiecutter` or `/init-repo`. Stop here.

**Never read data files.** Skip everything in `data/`, `01-raw/`, `02-prepared/`, `03-output/`, and anything in `.gitignore` / `.claudeignore`. Only inspect source: `.py`, `.R`, `.toml`, `.yml`, app files.

## Phase 2: Scan for hardcoded values

Search the source for each category. Prioritise the **app layer** — per CEDA Principle 2 the app *"wraps package functions and does not contain business logic"*, so literals or logic in `app/main.py` / `inst/app/app.R` are the highest-value findings.

Categories to hunt:

| Category | Examples | Likely bucket |
|----------|----------|---------------|
| Absolute/relative paths | `/Users/...`, `"data/raw/x.csv"`, `C:\...` | A |
| Cohort / years / dates | `== 2024`, `"2023-09-01"` | C |
| Thresholds / magic numbers | cutoffs, seeds, page sizes, `> 0.7` | C |
| Dataset / file / sheet names | `"instroom_2024.parquet"`, sheet `"Blad1"` | A or C |
| Lookup tables in code | `{"56822": "Verpleegkunde", ...}`, level→label dicts | B |
| Org / domain codes | brin, croho, sector codes as literals | B or C |
| URLs / hosts / ports / schemas | API endpoints, DB hosts | A |
| Secrets | API keys, tokens, passwords, connection strings | .env (flag) |

Useful starting greps (adjust per repo):

```bash
grep -rnE "/(Users|home|mnt|workspace)/|[A-Z]:\\\\" --include=*.py --include=*.R .
grep -rnE "\b(19|20)[0-9]{2}\b" --include=*.py --include=*.R .
grep -rnE "(api_key|token|password|secret|conn.*str)" -i --include=*.py --include=*.R .
```

## Phase 3: Report findings and wait for approval

Present findings grouped by bucket, with file:line and the proposed destination. Do not change anything yet.

> **De-hardcode bevindingen — repo `<naam>`**
>
> **Bucket A → config (`<config-bestand>`)**
> - `src/x/prepare.py:12` — `data_dir = "data/01-raw"` → `config.toml [paths] raw`
>
> **Bucket B → metadata (`<metadata-map>`)**
> - `src/x/transform.py:40-260` — inline dict `opleiding_namen` (200 regels) → `metadata/opleidingen.csv`
>
> **Bucket C → functieparameter**
> - `src/x/prepare.py:8` — `filter(cohort == 2024)` → parameter `cohort: int = 2024`
>
> **Secrets (⚠️ handmatig controleren)**
> - `src/x/ingest.py:5` — hardcoded API key → verplaats naar `.env`, check `.gitignore`
>
> Welke bevindingen wil je doorvoeren? (alles / per bucket / specifieke regels)

Wait for the user to choose before touching any file. Never move secrets silently — always confirm.

## Phase 4: Apply the extraction

For each approved finding, apply the change consistent with the standards and the existing code style:

**Bucket A — config**
- Add the key to `config.toml` / `config.yml` under a sensible section (`[paths]`, `[settings]`).
- Replace the literal with a config read that matches the repo's existing pattern (do not invent a new config loader — reuse what the repo already does).

**Bucket B — reference data**
- Write the lookup table to a `;`-delimited UTF-8 CSV in the metadata dir (per `data-conventions.md`).
- Replace the inline dict/list with a load from that file (`importlib.resources` in Python, `system.file()` in R).
- If the table describes output columns, remember the separate `data_dictionary.csv` convention — do not conflate.

**Bucket C — parameter**
- Add the value as a function argument with the current literal as the default (`def prepare_data(df, cohort: int = 2024):`).
- Thread it through callers; where a caller is `main.py` or the app, feed the default from config (A+C combined).
- Keep functions pure with explicit inputs (Principle 5) and use type hints (Python) / explicit `return()` (R).

**Secrets**
- Move to `.env`, read via the repo's existing env mechanism. Verify `.env` is gitignored. If it is not, add it. Never commit the secret.

## Phase 5: Verify

- Confirm nothing broke: run existing tests if present (`uv run pytest` / `devtools::test()`), or do a quick smoke check of the affected function.
- Format: Python `uv run ruff format . && uv run ruff check --fix .`; R `air format .`.
- Summarise what moved where, and list anything you deliberately left hardcoded (and why).

Suggest `/check-style` and `/simplify-ceda` as follow-ups — but do not run them; the user decides.

## Important

- **v0.1, untested** — always report before changing, always wait for approval, never auto-run other skills.
- Sort every value into exactly one bucket (A/B/C); a lookup table must never end up in `config.toml`.
- Reuse the repo's existing config/env mechanism — do not introduce a new one.
- Never read files in `data/` or any gitignored/`.claudeignore` directory.
- Never commit or push secrets; secrets handling is confirm-only, and CEDA has no `.env` standard yet — flag the gap if relevant.
- cedanl repositories in CEDA package structure only. If the repo is not structured yet, point to `/migrate-cookiecutter` or `/init-repo` and stop.
