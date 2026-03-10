---
name: r-package-refactor
description: Transform R projects into proper R packages with namespaces, documentation, and best practices. Use when converting scripts to packages or improving package structure.
---

# R Package Refactoring Skill

You are an expert R package developer helping to refactor an existing R project into a proper R package structure with namespaces, functions, and proper exports.

## CEDA Standards

This skill follows the **[CEDA Technical Standards](https://github.com/cedanl/.github/tree/main/standards)**. The resulting package must conform to these standards.

**Related skills:**
- Use `/check-style` to validate code against CEDA R style standards after refactoring
- Use `/init-repo` if creating a new repo from scratch (simpler than refactoring)

**When refactoring, ensure the package follows CEDA standards for structure, style, and conventions.**

## Core Philosophy

**Functions First, Package Second**
1. Analyze existing code structure
2. Convert scripts to clean, testable functions
3. Add package infrastructure (following CEDA structure)
4. Add interactive mode (Shiny app)
5. Polish with documentation and tests

This approach is safer than "big bang" refactoring - we ensure code works before adding package complexity.

**Key Principles**:
- **Functions First, Package Second**: Ensure code works before adding package complexity
- **Incremental progress**: One phase at a time with user approval
- **Test continuously**: Verify each change works before proceeding
- **Follow CEDA standards**: Package structure, tidyverse style, interactive mode (Shiny), data conventions

See `standards/principles.md` and `standards/r-style.md` for detailed CEDA guidelines.

## Configuration

Before starting, ask the user about:
1. **Package name** (if not already chosen)
2. **Repository type** (Ingestion or Analysis - see CEDA Project Structure)
   - **Ingestion**: Transforms raw data sources into clean, research-ready formats
   - **Analysis**: Produces enriched data, predictions, reports, visualizations
3. **Documentation language** (Dutch for README, English for code/comments per CEDA standards)
4. **Current pain points** (what motivated this refactoring?)
5. **Interactive mode needed?** (Shiny app for user-friendly interface - recommended per CEDA standards)

## Phase 1: Project Discovery & Analysis

**Goal:** Understand the current codebase structure and design the transformation plan

### Step 1: Analyze Directory Structure

```r
# Discover project layout
rtk ls -R . | grep "\\.R$"
```

Identify:
- **Script directories**: Are scripts organized by stage (download, prepare, analyze)?
- **Utility functions**: Where are shared functions located?
- **Data/config**: Where is metadata, config, or reference data stored?
- **Tests**: Are there existing test scripts?
- **Documentation**: README, vignettes, or markdown docs?

### Step 2: Catalog Scripts and Dependencies

For each R script:
1. **Purpose**: What does it do?
2. **Dependencies**: What packages/functions does it use?
3. **Inputs/Outputs**: Data files? Objects? Side effects?
4. **Execution order**: Which scripts run first?

Create a visual map:
```
scripts/download/ → scripts/process/ → scripts/export/
         ↓                 ↓                 ↓
      utils/helpers.R (used by all)
```

### Step 3: Identify Function Extraction Opportunities

Look for:
- **Repeated code patterns** across scripts
- **Scripts that are really functions** (take input, return output, no side effects)
- **Utility functions** already defined in utils/ or helper files
- **Configuration loading** that should be packageized

### Step 4: Design Package Architecture

Based on analysis, propose:

**Package Name**:
- Follow R conventions: lowercase, letters/numbers/periods only
- Short (5-10 chars), memorable, descriptive
- Check availability with `available::available("pkgname")`

**File Organization** (R/ directory):

See `standards/project-structure.md` for complete CEDA project structure guidelines.

For **Ingestion repos**:
- `R/ingest_source.R` - Read raw files
- `R/decode_fields.R` - Parse fixed-width, apply metadata
- `R/validate_data.R` - Quality checks
- `R/export_data.R` - Write Parquet + CSV output
- `R/run_app.R` - Launch Shiny app function
- `R/package.R` - Package-level documentation

For **Analysis repos**:
- `R/prepare_data.R` - Load and merge input data
- `R/transform_data.R` - Feature engineering, enrichment
- `R/run_analysis.R` - Core analysis/modeling
- `R/create_plots.R` - Visualization functions
- `R/render_report.R` - Report generation
- `R/run_app.R` - Launch Shiny app function
- `R/package.R` - Package-level documentation

**Export Strategy**:
- **Exported** (@export): Main pipeline functions, utilities users need, `run_app()`
- **Internal** (@keywords internal): Helper functions, low-level details

**Directory Structure** (CEDA standard):
- `inst/app/` - Shiny app (app.R, config.yml)
- `inst/metadata/` - Mapping tables, reference data, data_dictionary.csv
- `inst/templates/` - Report templates (Quarto .qmd files)
- `data/` - Example datasets for demos
  - `data/01-raw/demo/` - Sample raw data (committed to git)
  - `data/02-prepared/demo/` - Sample processed data
  - `data/03-output/demo/` - Sample output
- `man/` - Auto-generated roxygen2 docs
- `tests/testthat/` - Unit tests
- `vignettes/` - Usage documentation
- `main.R` - Pipeline orchestration script (NOT part of package)

### Step 5: Present Analysis and Plan

Create a structured plan document showing:
1. **Current structure** (directory tree with file purposes)
2. **Proposed package structure** (R/ file organization)
3. **Script → Function mapping** (which scripts become which functions)
4. **Export plan** (what users will see)
5. **Migration strategy** (what stays, what moves, what changes)

**Wait for user approval before proceeding to Phase 2**

## Phase 2: Create Package Infrastructure

**Goal:** Set up basic package structure without breaking existing code

### Step 2.1: Initialize Package Structure

```r
# Create DESCRIPTION file
usethis::create_package("path/to/package")
```

Or manually create `DESCRIPTION`:
```
Package: pkgname
Title: One-Line Description
Version: 0.0.1
Authors@R: person("First", "Last", email = "email@example.com", role = c("aut", "cre"))
Description: Longer description of what the package does.
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
RoxygenNote: 7.3.0
Depends: R (>= 4.1.0)
Imports:
    dplyr (>= 1.1.0),
    readr,
    tidyr
```

### Step 2.2: Create R/ Directory

```r
# Create R/ if it doesn't exist
dir.create("R", showWarnings = FALSE)
```

### Step 2.3: Set Up Development Tools

```r
# Create .Rbuildignore
usethis::use_build_ignore(c("data/", "test/", "*.qmd", "*.Rproj"))

# Create NAMESPACE (will be generated by roxygen2)
# Don't edit manually - roxygen2 will manage this
```

**Verify package structure with `devtools::load_all()`**

## Phase 3: Convert Utilities to Functions

**Goal:** Transform utility scripts into clean, namespaced functions

### Step 3.1: Start with Simple Helpers

Pick the simplest utility functions first (no dependencies on other utilities).

**Example transformation:**

**Before** (`utils/helpers.R`):
```r
library(lubridate)
library(dplyr)

# Calculate academic year
academic_year <- function(date) {
  year <- year(date)
  month <- month(date)
  ifelse(month >= 9, year, year - 1)
}
```

**After** (`R/utils.R`):
```r
#' Calculate academic year from date
#' @param date Date vector
#' @return Integer vector with academic years
#' @keywords internal
academic_year <- function(date) {
  # Use explicit namespacing
  year <- lubridate::year(date)
  month <- lubridate::month(date)

  # Explicit return
  return(ifelse(month >= 9, year, year - 1))
}
```

**Key changes:**
1. ❌ Remove `library()` calls
2. ✅ Add explicit namespace: `lubridate::year()`
3. ✅ Add roxygen2 documentation header
4. ✅ Use `@keywords internal` for helpers
5. ✅ Explicit `return()` statement

### Step 3.2: Test Each Function

After converting each utility:
```r
# Load package
devtools::load_all()

# Test function
test_date <- as.Date("2024-09-01")
academic_year(test_date)  # Should return 2024
```

### Step 3.3: Handle External Dependencies

For functions using mapping tables or config:

**Before** (uses global path):
```r
lookup_table <- read.csv(paste0(Sys.getenv("REF_DATA_DIR"), "lookup.csv"))
```

**After** (uses package data):
```r
#' Load reference data from package
#' @keywords internal
load_reference_data <- function(data_name) {
  # Try package installation first
  data_path <- system.file("extdata", "reference",
                           paste0(data_name, ".csv"),
                           package = "pkgname")

  # Fallback for development
  if (data_path == "") {
    data_path <- file.path("inst", "extdata", "reference",
                          paste0(data_name, ".csv"))
  }

  return(utils::read.csv(data_path, stringsAsFactors = FALSE))
}
```

### Step 3.4: Move Reference Data to inst/

```bash
# Create inst/ directory structure
mkdir -p inst/extdata/reference
mkdir -p inst/config

# Copy reference data
cp -r data/reference/* inst/extdata/reference/
cp config.yml inst/config/
```

## Phase 4: Convert Scripts to Functions

**Goal:** Transform pipeline scripts into composable functions

### Step 4.1: Identify Script Boundaries

Each script typically does:
1. **Read** data from file
2. **Transform** data (the actual logic)
3. **Write** data to file
4. **Clean up** environment

**Only #2 (transform) becomes the function** - separate I/O from logic!

### Step 4.2: Extract Pure Logic

**Before** (`scripts/process/clean_data.R`):
```r
# READ
raw_data <- read_csv("data/raw/input.csv")

# TRANSFORM
clean_data <- raw_data %>%
  distinct() %>%
  filter(!is.na(id)) %>%
  mutate(
    date = as.Date(date, format = "%Y-%m-%d"),
    status = recode_status(status)
  )

# WRITE
write_csv(clean_data, "data/processed/output.csv")

# CLEAN
rm(raw_data, clean_data)
```

**After** (`R/data_transform.R`):
```r
#' Clean and prepare raw data
#'
#' Transforms raw data: removes duplicates, filters invalid records,
#' converts dates, and recodes status values.
#'
#' @param raw_data Data frame with raw input data
#' @param status_mapping Optional. Provide custom status mapping.
#'
#' @return Data frame with cleaned data
#' @export
clean_data <- function(raw_data, status_mapping = NULL) {
  # Load default mapping if not provided
  if (is.null(status_mapping)) {
    status_mapping <- load_mapping("status_codes")
  }

  # Transform (explicit namespacing)
  result <- raw_data %>%
    dplyr::distinct() %>%
    dplyr::filter(!is.na(id)) %>%
    dplyr::mutate(
      date = as.Date(date, format = "%Y-%m-%d"),
      status = recode_status(status, status_mapping)
    )

  return(result)
}
```

**Separate I/O wrapper** (for backward compatibility):
```r
#' @keywords internal
clean_data_file <- function(input_file, output_file) {
  raw_data <- readr::read_csv(input_file)
  result <- clean_data(raw_data)
  readr::write_csv(result, output_file)
  return(invisible(NULL))
}
```

### Step 4.3: Handle Configuration

**Before** (uses global config):
```r
config <- config::get()
year <- config$year
brin <- config$institution$brin
```

**After** (explicit parameters):
```r
#' Process data for specific period
#'
#' @param data Raw data frame
#' @param year Year for processing (default: current year)
#' @param region Geographic region code (default: "NL")
#'
#' @return Processed data
#' @export
process_data <- function(data,
                        year = as.integer(format(Sys.Date(), "%Y")),
                        region = "NL") {
  # Function body with explicit parameters
  # No global config dependency
}
```

**Create config helper** (if needed):
```r
#' Load package configuration
#' @param config_name Config name (default: "default")
#' @export
load_config <- function(config_name = "default") {
  config_path <- system.file("config", "config.yml", package = "pkgname")

  # Development fallback
  if (config_path == "") {
    config_path <- "config.yml"
  }

  return(yaml::read_yaml(config_path)[[config_name]])
}
```

### Step 4.4: Build Pipeline Function

Create a main function that orchestrates the workflow:

```r
#' Run complete data processing pipeline
#'
#' Imports, cleans, analyzes, and exports data.
#'
#' @param input_path Path to input data file or directory
#' @param year Year for processing (default: current year)
#' @param output_dir Output directory path
#'
#' @return List with processed datasets
#' @export
#'
#' @examples
#' \dontrun{
#'   results <- run_pipeline(input_path = "data/raw", year = 2024)
#' }
run_pipeline <- function(input_path,
                        year = as.integer(format(Sys.Date(), "%Y")),
                        output_dir = "data/output") {

  # Step 1: Import
  raw_data <- import_data(input_path)

  # Step 2: Clean
  clean_data <- clean_data(raw_data)

  # Step 3: Transform
  transformed_data <- transform_data(clean_data, year = year)

  # Step 4: Analyze
  analysis_results <- analyze_data(transformed_data)

  # Step 5: Export
  export_results(analysis_results, output_dir = output_dir)

  return(list(
    clean = clean_data,
    transformed = transformed_data,
    results = analysis_results
  ))
}
```

## Phase 4.5: Add Interactive Mode (Shiny App)

**Goal:** Create a Shiny app following CEDA standards for interactive use

Per CEDA standards, every repo should include an interactive interface. The app wraps package functions - it contains **NO business logic**, only UI and function calls.

### Step 4.5.1: Create Shiny App Structure

```bash
# Create app directory
mkdir -p inst/app
```

### Step 4.5.2: Create app.R

```r
## inst/app/app.R

library(shiny)
library(pkgname)  # Your package

## UI
ui <- fluidPage(
  titlePanel("Package Name - Interactive Mode"),

  sidebarLayout(
    sidebarPanel(
      ## Configuration inputs
      textInput("input_path", "Input Path:", value = "data/01-raw"),
      numericInput("year", "Year:", value = as.integer(format(Sys.Date(), "%Y"))),
      textInput("output_dir", "Output Directory:", value = "data/03-output"),
      actionButton("run", "Run Pipeline", class = "btn-primary")
    ),

    mainPanel(
      ## Results display
      tabsetPanel(
        tabPanel("Summary", verbatimTextOutput("summary")),
        tabPanel("Data Preview", tableOutput("preview")),
        tabPanel("Logs", verbatimTextOutput("logs"))
      )
    )
  )
)

## Server
server <- function(input, output, session) {
  results <- eventReactive(input$run, {
    ## Call package function - NO business logic here
    run_pipeline(
      input_path = input$input_path,
      year = input$year,
      output_dir = input$output_dir
    )
  })

  output$summary <- renderPrint({
    req(results())
    str(results())
  })

  output$preview <- renderTable({
    req(results())
    head(results()$transformed, 20)
  })
}

shinyApp(ui, server)
```

### Step 4.5.3: Create config.yml

```yaml
## inst/app/config.yml
## Fixed config for local data paths - users only need to set paths once

default:
  data_path: "data"
  output_path: "data/03-output"
  metadata_path: !expr system.file("metadata", package = "pkgname")
```

### Step 4.5.4: Create run_app() function

```r
## R/run_app.R

#' Launch the interactive Shiny application
#'
#' Opens a Shiny app that provides a user interface for the package functions.
#'
#' @param ... Arguments passed to [shiny::runApp()].
#'
#' @return Runs the Shiny app (does not return a value)
#' @export
#'
#' @examples
#' \dontrun{
#'   run_app()
#' }
run_app <- function(...) {
  ## Check if shiny is installed
  if (!requireNamespace("shiny", quietly = TRUE)) {
    rlang::abort("Package {.pkg shiny} needed. Install: install.packages('shiny')")
  }

  ## Locate app directory
  app_dir <- system.file("app", package = "pkgname")

  if (app_dir == "") {
    rlang::abort("Could not find app directory. Try devtools::load_all() first.")
  }

  ## Run the app
  shiny::runApp(app_dir, ...)
}
```

### Step 4.5.5: Update DESCRIPTION

Add `shiny` to `Suggests:` (not `Imports:`) - package works without Shiny installed:

```
Suggests:
    shiny,
    testthat (>= 3.0.0)
```

### Step 4.5.6: Test the App

```r
## Load package
devtools::load_all()

## Launch app
run_app()
```

## Phase 5: Add Documentation

**Goal:** Complete roxygen2 documentation for all functions

### Step 5.1: Documentation Template

Use this template (adapt language as needed):

```r
#' Short one-line title
#'
#' Longer description explaining what the function does,
#' when to use it, and any important details.
#'
#' @param param1 Description of first parameter
#' @param param2 Description of second parameter. Default: value
#'
#' @return Description of return value
#'
#' @export
#'
#' @examples
#' \dontrun{
#'   result <- my_function(data, param = "value")
#' }
#'
#' @seealso \code{\link{related_function}}
function_name <- function(param1, param2 = default) {
  # Function body
}
```

### Step 5.2: Language-Specific Documentation

**English example:**
```r
#' Prepare enrollment data with mapping tables
#'
#' Applies mapping tables to enrollment data to translate codes into
#' readable values.
#'
#' @param enrollments Data frame with raw enrollment data
#' @return Data frame with mapped enrollment data
#' @export
```

**Dutch example:**
```r
#' Bereid inschrijvingsgegevens voor met mappingtabellen
#'
#' Past mappingtabellen toe op inschrijvingsgegevens om codes te vertalen
#' naar leesbare waarden.
#'
#' @param enrollments Data frame met ruwe inschrijvingsgegevens
#' @return Data frame met gemapte inschrijvingsgegevens
#' @export
```

### Step 5.3: Generate Documentation

```r
# Generate man/ files from roxygen2 comments
devtools::document()

# Check for issues
devtools::check_man()

# Preview documentation
?pkgname::function_name
```

### Step 5.4: Package-Level Documentation

Create `R/package.R`:
```r
#' pkgname: Brief Package Description
#'
#' Longer description of what this package does and who it's for.
#'
#' @section Main Functions:
#' \itemize{
#'   \item \code{\link{run_pipeline}}: Run complete data pipeline
#'   \item \code{\link{clean_data}}: Clean and prepare raw data
#'   \item \code{\link{import_data}}: Import data from various sources
#' }
#'
#' @docType package
#' @name pkgname-package
#' @keywords internal
"_PACKAGE"

## usethis namespace: start
## usethis namespace: end
NULL
```

### Step 5.5: Create Data Dictionary

**CEDA requirement**: Every repo that produces data must include `inst/metadata/data_dictionary.csv`.

See `standards/data-conventions.md` for the required format and columns.

Example structure:
```csv
dataset;column_name;description;type;source;example;allowed_values;sensitive
output_2024;id;Student identifier;integer;source_system;12345;;false
output_2024;status;Current enrollment status;character;derived;active;active;inactive;withdrawn;false
```

**Create human-readable version** (optional but recommended):

```r
## vignettes/data-dictionary.qmd

---
title: "Data Dictionary"
format: html
---

```{r}
#| echo: false
library(DT)

data_dict <- readr::read_csv2(
  system.file("metadata", "data_dictionary.csv", package = "pkgname")
)

datatable(data_dict, options = list(pageLength = 50))
```
```

## Phase 6: Testing & Validation

**Goal:** Ensure package works correctly and passes R CMD check

### Step 6.1: Create Test Scripts

Use testthat (>= 3.0) following CEDA standards:

```r
## tests/testthat/test-transform_data.R
## Test file mirrors source file: R/transform_data.R

test_that("transform_data returns expected columns", {
  ## Use demo data
  test_data <- readr::read_csv("../../data/01-raw/demo/sample.csv")

  result <- transform_data(test_data)

  expect_s3_class(result, "data.frame")
  expect_true(nrow(result) > 0)
  expect_true(all(c("id", "date", "status") %in% names(result)))
})

test_that("transform_data handles missing values", {
  test_data <- data.frame(id = c(1, NA, 3), value = c(10, 20, 30))

  result <- transform_data(test_data)

  expect_equal(nrow(result), 2)  ## NA rows filtered
})
```

### Step 6.2: Format Code and Run Checks

**Format and validate with `/check-style`** (CEDA standard):
```bash
## Use the check-style skill to validate against CEDA standards
/check-style

## Or format with air manually
air format .
```

**Run R CMD check**:
```r
## Check package for issues
devtools::check()
```

Common issues and fixes:
- **Namespace warnings**: Add `@importFrom` or use `::`
- **Undocumented exports**: Add roxygen2 headers
- **Missing dependencies**: Add to DESCRIPTION Imports
- **Example errors**: Use `\dontrun{}` for examples needing data
- **Style issues**: Use `/check-style` or run `air format .`

### Step 6.3: Install and Test

```r
# Install package locally
devtools::install()

# Restart R session

# Test in clean environment
library(pkgname)
?pkgname::run_pipeline
```

### Step 6.4: Update README

Create or update `README.md` following **CEDA README guidelines** (Dutch, visual-first, relevance-focused).

See `standards/README.md` for detailed README structure. Key sections:
- One-line description (Dutch)
- Visual example (screenshot/diagram)
- Relevantie (why it exists, who it's for)
- Quick start (installation, Shiny app, pipeline usage)
- Data (input/output formats, demo data location)
- Link to CLAUDE.md for technical details

## Key Transformation Patterns

### Pattern 1: Script with File I/O → Pure Function

**Before:**
```r
data <- readr::read_csv("input.csv")
result <- transform(data)
readr::write_csv(result, "output.csv")
```

**After:**
```r
#' Transform data
#' @param data Input data frame
#' @return Transformed data frame
#' @export
transform_data <- function(data) {
  result <- transform_logic(data)
  return(result)
}
```

### Pattern 2: Global Config → Function Parameters

**Before:**
```r
config <- config::get()
process_data(data, year = config$year)
```

**After:**
```r
#' @param year Academic year (default: current year)
process_data <- function(data, year = as.integer(format(Sys.Date(), "%Y"))) {
  # Use year parameter
}
```

### Pattern 3: Environment Variables → Package Data

**Before:**
```r
lookup <- read.csv(paste0(Sys.getenv("REF_DIR"), "lookup.csv"))
```

**After:**
```r
lookup <- utils::read.csv(
  system.file("extdata", "lookup.csv", package = "pkgname")
)
```

### Pattern 4: library() Calls → Explicit Namespacing + Base Pipe

**Before:**
```r
library(dplyr)
library(readr)

result <- data %>%
  mutate(x = y + 1) %>%
  filter(x > 0)
```

**After** (CEDA R style - use `|>` base pipe):
```r
## No library() calls!

result <- data |>
  dplyr::mutate(x = y + 1) |>
  dplyr::filter(x > 0)

## Or add to roxygen2:
#' @importFrom dplyr mutate filter
```

**Note**: Use `|>` (base pipe) not `%>%` (magrittr pipe) per CEDA R Style Guide.

### Pattern 5: Sourcing Scripts → Package Functions

**Before:**
```r
source("utils/helpers.R")
source("utils/mapping.R")
result <- my_helper_function(data)
```

**After:**
```r
# Just use the function - package loading makes it available
library(pkgname)
result <- my_helper_function(data)
```

## Namespace Strategy

### What to Export (@export)

✅ **User-facing functions:**
- Main workflow functions (`run_pipeline()`)
- Data preparation functions (`prepare_enrollments()`)
- Utility functions users might need (`load_config()`)

❌ **Internal functions (@keywords internal):**
- Helper functions used only within package
- Low-level implementation details
- File I/O wrappers for backward compatibility

### Import Strategy

**Option 1: Explicit :: notation** (recommended for clarity)
```r
result <- dplyr::mutate(data, x = y)
```

**Option 2: @importFrom** (for frequently used functions)
```r
#' @importFrom dplyr mutate filter select
#' @importFrom readr read_csv write_csv
```

**Don't use:** Wholesale imports (`@import dplyr`) - makes namespace unclear

## Common Challenges & Solutions

### Challenge 1: Existing code uses library()

**Solution:** Remove all `library()` calls, use `::` or `@importFrom`

### Challenge 2: Scripts depend on file paths

**Solution:**
- Make functions accept data frames, not file paths
- Create separate I/O functions if needed
- Use `system.file()` for package data

### Challenge 3: Global configuration

**Solution:**
- Make config explicit via function parameters
- Provide sensible defaults
- Create `load_config()` helper if needed

### Challenge 4: Scripts modify global environment

**Solution:**
- Functions should only modify their own scope
- Return values instead of assigning to globals
- Remove `rm()` and `clear_environment()` calls

### Challenge 5: Breaking existing workflows

**Solution:**
- Keep backward-compatible wrapper functions
- Document migration path in README
- Provide transition period with both approaches

## Workflow Summary

1. **Phase 1: Analyze** - Understand current structure, design transformation
2. **Phase 2: Infrastructure** - Create DESCRIPTION, R/, inst/, data/ (CEDA structure)
3. **Phase 3: Utilities** - Convert helper functions first
4. **Phase 4: Scripts** - Transform pipeline scripts to functions
5. **Phase 4.5: Interactive Mode** - Add Shiny app in inst/app/
6. **Phase 5: Document** - Add complete roxygen2 documentation
7. **Phase 6: Validate** - Test, format with air, check, install
8. **Phase 6.5: Finalize** - Create CLAUDE.md, set up renv, add demo data

**CEDA Standards Checklist:**
Use `/check-style` for comprehensive validation. Key elements:
- ✅ Package structure (DESCRIPTION, NAMESPACE, R/, man/, tests/)
- ✅ Shiny app in inst/app/ with run_app() function
- ✅ Data directories and demo data
- ✅ Data dictionary in inst/metadata/
- ✅ README (Dutch) and CLAUDE.md
- ✅ Format with `air`, test with `testthat`

**Always proceed incrementally with user approval between phases!**

## Phase 6.5: Create CLAUDE.md and Setup renv

### Step 6.5.1: Create CLAUDE.md

Following CEDA standards, create `CLAUDE.md` with technical documentation:

```markdown
# Package Name

## Overview

Brief description of what this package does and which CEDA repo type it is (Ingestion or Analysis).

## Standards

Follow CEDA technical standards: https://github.com/cedanl/.github/tree/main/standards/README.md

## Tech Stack

- **Language**: R (>= 4.1.0)
- **Key packages**: dplyr, readr, tidyr, ggplot2, shiny
- **Tooling**: devtools, testthat, air (code formatting), renv (dependency management)
- **Interactive mode**: Shiny app in `inst/app/`

## Project Structure

```
pkgname/
├── R/                      # Package functions
│   ├── ingest_data.R
│   ├── transform_data.R
│   ├── run_analysis.R
│   └── run_app.R
├── inst/
│   ├── app/                # Shiny app
│   │   ├── app.R
│   │   └── config.yml
│   ├── metadata/           # Reference data, data dictionary
│   └── templates/          # Quarto report templates
├── data/
│   ├── 01-raw/demo/        # Demo raw data (committed)
│   ├── 02-prepared/demo/   # Demo processed data
│   └── 03-output/demo/     # Demo output
├── man/                    # Auto-generated docs
├── tests/testthat/         # Unit tests
├── vignettes/              # Usage docs
├── main.R                  # Pipeline script (not part of package)
├── DESCRIPTION
├── NAMESPACE
└── renv.lock
```

## How to Run

### Interactive mode (Shiny app)

```r
devtools::load_all()
run_app()
```

### Pipeline mode (script)

```r
devtools::load_all()
source("main.R")
```

## Data

**Input**: [Describe input format, sources]
- Place in `data/01-raw/`
- Demo data available in `data/01-raw/demo/`

**Output**: [Describe output format]
- Written to `data/03-output/`
- Formats: Parquet (for code) + CSV (for Excel)
- Data dictionary: `inst/metadata/data_dictionary.csv`

**Privacy**: [Note any sensitive data handling]
```

### Step 6.5.2: Setup renv for Dependency Management

**Initialize renv** (CEDA standard for reproducibility):

```r
## Install renv if needed
install.packages("renv")

## Initialize renv for this project
renv::init()

## This creates:
## - renv.lock (list of exact package versions)
## - renv/ directory (local package library)
## - .Rprofile (auto-loads renv on project open)
```

**After adding new packages**:

```r
## Update lockfile
renv::snapshot()
```

**For new users cloning the repo**:

```r
## Restore exact package versions
renv::restore()
```

**Add to .gitignore**:
```
renv/library/
renv/local/
renv/staging/
```

**Keep in git**:
- `renv.lock` ✅
- `renv/activate.R` ✅
- `.Rprofile` ✅

### Step 6.5.3: Add Demo Data

Create synthetic demo data so the package works out-of-the-box:

```r
## Create demo directories
dir.create("data/01-raw/demo", recursive = TRUE)
dir.create("data/02-prepared/demo", recursive = TRUE)
dir.create("data/03-output/demo", recursive = TRUE)

## Create synthetic sample data
demo_data <- data.frame(
  id = 1:100,
  date = seq.Date(as.Date("2024-01-01"), by = "day", length.out = 100),
  value = rnorm(100, mean = 50, sd = 10)
)

## Save to demo folder (will be committed to git)
readr::write_csv(demo_data, "data/01-raw/demo/sample_data.csv")
```

**Update .gitignore**:
```
## Ignore real data
data/01-raw/*
data/02-prepared/*
data/03-output/*

## But keep demo data
!data/**/demo/
!data/**/demo/*
```

## Starting the Skill

When invoked:
1. **Introduce CEDA standards** - Explain this refactoring follows CEDA technical standards
2. **Ask about configuration**:
   - Package name
   - Repo type (Ingestion vs Analysis)
   - Documentation language (Dutch README, English code)
   - Interactive mode needed? (Shiny app recommended)
3. **Start Phase 1: Project Discovery** - Analyze current structure
4. **Present transformation plan** - Show before/after, get user approval
5. **Execute phases incrementally** - One phase at a time with user approval
6. **Validate against CEDA standards** - Run `/check-style` to verify compliance
7. **Celebrate when complete!** 🎉

## Quick Reference: CEDA Standards

For detailed standards, see: https://github.com/cedanl/.github/tree/main/standards

**Key validation**:
- Run `/check-style` to verify R style compliance
- Use `/init-repo` for reference on proper structure
- See `standards/` directory for all documentation

**Essential elements**:
- Package structure (DESCRIPTION, NAMESPACE, R/, man/, tests/)
- Shiny app in `inst/app/` with `run_app()` function
- Data conventions (numbered directories, data dictionary)
- README in Dutch, CLAUDE.md with tech details
- Format with `air`, test with `testthat`
