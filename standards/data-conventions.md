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

Place this documentation in:
- `metadata/` directory (for lookup tables and variable definitions)
- Code comments (for transformation logic)
- `README.md` or `CLAUDE.md` (for high-level overview)

## Data Dictionaries

Elk repository dat data verwerkt of produceert **moet** een data dictionary bevatten voor de output datasets. Data dictionaries worden in twee formaten bijgehouden:

### Machine-readable: `data_dictionary.csv`

Een CSV-bestand (`;`-gescheiden, UTF-8) in de `metadata/` directory met de volgende kolommen:

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

Voorbeeld:

```csv
dataset;column_name;description;type;source;example;allowed_values;sensitive
instroom_2024;INS_Studentnummer;Geanonimiseerd studentnummer;character;DUO;STU_00001;;false
instroom_2024;INS_Opleidingsnaam;Naam van de opleiding;character;DUO;Verpleegkunde;;false
instroom_2024;INS_Datum_inschrijving;Datum eerste inschrijving;date;DUO;2024-09-01;;false
instroom_2024;INS_Leeftijd_cat;Leeftijdscategorie bij inschrijving;character;derived;18-25;< 18;18-25;25+;false
```

### Human-readable: gerenderde documentatie

Genereer vanuit `data_dictionary.csv` een leesbare versie, bijvoorbeeld:

- **Quarto** → render naar HTML (aanbevolen, past bij bestaande CEDA workflow)
- **R**: `DT::datatable()` of `gt::gt()` in een Quarto document
- **Python**: `pandas` tabel in een Quarto of Streamlit pagina

Plaats het gerenderde bestand in `docs/data_dictionary.html` of maak het beschikbaar via de app.

### Locatie

```
project-name/
├── metadata/
│   └── data_dictionary.csv       # Machine-readable (verplicht)
├── docs/
│   ├── data_dictionary.qmd       # Quarto source (aanbevolen)
│   └── data_dictionary.html      # Gerenderde versie
```

### Bijhouden

- Update de data dictionary wanneer kolommen worden toegevoegd, verwijderd of hernoemd
- Verwijs vanuit de `README.md` naar de data dictionary (zie [README richtlijnen](project-structure.md))
