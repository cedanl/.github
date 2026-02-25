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
| `_cat` | Categorized/binned numeric | `INS_Hoogste_vooropleiding_soort_cat` |
| `_code` | Numeric code for a string value | `INS_Vooropleiding_voor_HO_code` |
| `_date` | Date field | `DEM_Leeftijd_peildatum_1_oktober_date` |
| `_origineel` | Original value before transformation | `INS_Datum_diploma_origineel` |
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

### Input data from DUO

DUO fixed-width ASCII files typically use:
- Encoding: Latin1 (ISO 8859-1)
- Fixed-width fields defined in accompanying `.txt` metadata files

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
5. **Data dictionaries** - in both machine-readable format (csv) and human-readable format (for instance, quarto-based html)

Place this documentation in:
- `app/metadata/` directory (for lookup tables and variable definitions)
- Code comments (for transformation logic)
- `README.md` or `CLAUDE.md` (for high-level overview)
