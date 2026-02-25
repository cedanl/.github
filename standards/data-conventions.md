# CEDA Data Conventions

Standards for data handling, naming, formats, and privacy across all cedanl repositories.

## Column Naming

### Preserve source names

Keep the original column names from data sources and variables much as possible. This ensures traceability and makes it easy for domain experts to recognize fields.

### New variables

When creating derived or computed variables, follow the naming conventions of the source data. In addition:

- Names should be descriptive and immediately understandable, when in doubt longer is better than short.
- Use underscores as separators

### Suffix conventions for derived variables

| Suffix | Meaning | Example |
|--------|---------|---------|
| `_cat` | Categorized/binned numeric | `hoogste_vooropleiding_soort_cat` |
| `_code` | Numeric code for a string value | `vooropleiding_voor_ho_code` |
| `_date` | Date field | `leeftijd_peildatum_1_oktober_date` |
| `_scaled` | Standardized/normalized | `INS_Score_scaled` |

### Character rules

- No diacritics (no accents, umlauts, or special characters) in column names
- No spaces — use underscores
- Letters, digits, and underscores only
- descriptive case, object, statement style.

## File Formats

### Internal data (between pipeline steps)

Use **Parquet** for all intermediate data files within a repository. Parquet is:
- Fast to read/write
- Compact (compressed)
- Type-preserving (no string-to-factor issues)
- Language-agnostic (works in R and Python)

### Output data (for consumers)

Provide both formats:
- **Parquet** — for programmatic consumption by other repos
- **CSV** — for users who need to open data in Excel or other tools

### CSV conventions

- Delimiter: `;` (semicolon) — standard for Dutch data, avoids conflicts with comma in decimal numbers
- Encoding: UTF-8 for output files
- Quote all text fields that might contain delimiters

Always convert to UTF-8 during the ingestion step.

## Data Directory Structure

```
data/
  01-raw/          # Source files, never modified
  02-prepared/     # Cleaned, decoded, intermediate Parquet files
  03-output/       # Final output: Parquet + CSV
```

- `01-raw/`: Place input files here. These are read-only — never overwrite source data.
- `02-prepared/`: Intermediate results between pipeline steps. Parquet format.
- `03-output/`: Final deliverables. Always both Parquet and CSV.

All data directories are in `.gitignore`. Include synthetic demo/subfolders datasets where possible (in `data/`) for exploratory use.

## Privacy and Sensitive Data

### Rules

- **Never commit** personal data (BSN, names, addresses) to git
- **Auto-anonymize** BSN and other identifiers in the ingestion step
- Sensitive fields are removed or hashed before data leaves `02-prepared/`
- Document which fields are considered sensitive in `metadata/` or the README

### Data classification

| Level | Description | Handling |
|-------|-------------|----------|
| Public | Aggregated statistics, published data | Can be in repo (demo data) |
| Internal | Anonymized individual records | In `.gitignore`, share via secure channels |
| Sensitive | Contains BSN, names, or other PII | Must be anonymized before any processing output |

## Documentation of Data Assumptions

Every repo that processes data should document:

1. **Expected input format** — which fields, types, and sources
2. **Transformation logic** — what changes and why (in code comments or metadata)
3. **Known data quality issues** — missing values, known errors, workarounds
4. **Output schema** — what the final output looks like

Place this documentation in:
- `metadata/` directory (for lookup tables and variable definitions)
- Code comments (for transformation logic)
- `README.md` or `CLAUDE.md` (for high-level overview)

## Data Dictionaries

Every repo that processes or produces data **must** include a data dictionary for its output datasets. Maintain two formats: machine-readable and human-readable.

### Machine-readable: `data_dictionary.csv`

A `;`-delimited CSV file (UTF-8) in the repo's metadata directory (see [Project Structure](project-structure.md) for exact location per language).

| Kolom | Verplicht | Beschrijving |
|-------|-----------|-------------|
| `dataset` | ja | Naam van de output dataset (bijv. `instroom_2024`) |
| `column_name` | ja | Kolomnaam zoals in de data |
| `description` | ja | Korte beschrijving van de variabele |
| `type` | ja | Datatype: `character`, `integer`, `double`, `date`, `boolean` |
| `source` | ja | Herkomst: bronsysteem of `derived` voor berekende variabelen |
| `example` | nee | Voorbeeldwaarde |
| `allowed_values` | nee | Toegestane waarden of bereik (bijv. `1-5`, `MBO;HBO;WO`) |
| `sensitive` | nee | `true` als het veld persoonsgegevens bevat |

### Human-readable: rendered documentation

Generate a readable version from `data_dictionary.csv`, for example:

- **Quarto** rendered to HTML (recommended — fits existing CEDA workflow)
- **R**: `DT::datatable()` or `gt::gt()` in a Quarto vignette
- **Python**: table in a Streamlit app page

### Location

The data dictionary lives alongside other metadata files, following existing package conventions:

- **R repos**: `inst/metadata/data_dictionary.csv` (installed with the package)
- **Python repos**: `src/metadata/data_dictionary.csv` (accessible via `importlib.resources`)

The human-readable version can be a vignette (R) or a page in the app (Shiny/Streamlit).

### Maintenance

- Update the data dictionary when columns are added, removed, or renamed
