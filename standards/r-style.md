# CEDA R Style Guide

R coding standards for cedanl repositories. Based on the [Tidyverse style guide](https://style.tidyverse.org/) with CEDA-specific conventions.

## Ecosystem

### Tidyverse dialect

Write R in the tidyverse dialect. Tidyverse packages share a consistent design philosophy for data manipulation, which makes code predictable and composable.

- Use `|>` (base pipe) for pipelines
- Prefer tidyverse functions over base R equivalents when they improve readability (e.g., `str_detect()` over `grepl()`, `read_csv()` over `read.csv()`)
- Use tidymodels for modeling workflows
- Use ggplot2 for visualization

### Preferred packages

| Domain | Package | Notes |
|--------|---------|-------|
| Data manipulation | dplyr, tidyr | Core pipeline |
| String operations | stringr | Consistent `str_` prefix |
| Date/time | lubridate | Readable date manipulation |
| Reading data | readr, arrow | `read_csv()`, `read_parquet()` |
| Modeling | tidymodels (parsnip, recipes, workflows, yardstick) | Unified modeling interface |
| Plotting | ggplot2 | With ragg for rendering |
| Tables | flextable, gtsummary | For reports |
| Reports | quarto | `.qmd` templates |
| Interactive | shiny | App interface |
| CLI messages | cli | For user-facing messages |
| Error handling | rlang | `rlang::abort()` over `stop()` |
| File paths | fs | Cross-platform path handling |
| Iteration | purrr | Functional iteration (`map()`, `walk()`) |
| Data cleaning | janitor | `clean_names()`, `tabyl()` |

See [Principles §11](principles.md#11-dependency-selection) for general dependency selection criteria.

## Package Structure

Every R repo is an R package. See [Project Structure](project-structure.md) for full directory layouts per repo type.

### Function files

- One primary function per file, with helpers below it
- File name matches the main function: `transform_data.R` contains `transform_data()`
- User-facing (exported) functions at the top of the file
- Helper functions below, ordered hierarchically

### main.R

The entry point that orchestrates the pipeline:

```r
## Load the package
devtools::load_all()

## Configuration
opleidingsnaam <- "Informatica"
opleidingsvorm <- "VT"

## Run pipeline
metadata <- read_metadata()
programs <- transform_data(metadata, opleidingsnaam, opleidingsvorm)
results <- run_analysis(programs)
render_report(results)
```

`main.R` is NOT part of the package — it's a script that uses the package.

### Shiny app (interactive mode)

The Shiny app lives **inside** the package at `inst/app/`. This follows the standard CRAN pattern used by packages like [esquisse](https://cran.r-project.org/package=esquisse), [radiant](https://cran.r-project.org/package=radiant), and [DALEX](https://cran.r-project.org/package=DALEX).

```r
# R/run_app.R
#' Launch the interactive application
#'
#' @param ... Arguments passed to [shiny::runApp()].
#' @export
run_app <- function(...) {
  if (!requireNamespace("shiny", quietly = TRUE)) {
    rlang::abort("Package {.pkg shiny} needed. Install: install.packages('shiny')")
  }
  app_dir <- system.file("app", package = "nfwa")
  shiny::runApp(app_dir, ...)
}
```

Key conventions:
- App code in `inst/app/app.R` — wraps package functions with a UI
- Launch function in `R/run_app.R` — uses `system.file()` to locate the app
- `shiny` in `Suggests:` (not `Imports:`) — package works without Shiny installed
- `config.yml` in `inst/app/` for local data paths
- App contains NO business logic — only UI and calls to package functions

## Syntax

### Assignment and pipes

```r
# Good
students <- students_raw |>
  filter(INS_Studiejaar == 2024) |>
  select(INS_Studentnummer, INS_Opleidingsnaam)

# Bad
students = students_raw %>%
  filter(INS_Studiejaar == 2024) %>%
  select(INS_Studentnummer, INS_Opleidingsnaam)
```

- Use `<-` for assignment, not `=`
- Use `|>` (base pipe), not `%>%` (magrittr pipe)
- Left-hand assignment only (`x <- value`, not `value -> x`)
- Put the source object and first pipe on the same line

### Spacing

```r
# Good
height <- (feet * 12) + inches
df$z
x <- 1:10

# Bad
height<-feet*12+inches
df $ z
x <- 1 : 10
```

- Spaces around binary operators: `==`, `<-`, `+`, `-`, `*`, `/`, `|>`
- No spaces around unary operators: `:`, `::`, `$`, `@`, `[`, `[[`
- Extra alignment spaces are fine for readability with `<-`

### Braces and code blocks

```r
# Good
if (debug) {
  show(x)
}

# Bad
if(debug){
  show(x)
}
```

- `{` at end of line, after a space
- `}` on its own line
- Space before `(` in control flow (`if (`, `for (`), but not in function calls (`mean(x)`)

### Function definitions

```r
# Good: explicit return, named arguments
calculate_retention <- function(df,
                                year = 2024,
                                min_credits = 0,
                                include_masters = FALSE) {
  df <- df |>
    filter(INS_Studiejaar == year)

  return(df)
}

# Bad: implicit return, no named arguments
f <- function(d, y, m, i) {
  d |> filter(INS_Studiejaar == y)
}
```

- Use explicit `return()` statements
- Name arguments explicitly when calling functions with more than 2 arguments
- Put each argument on its own line when the signature is long
- Sensible defaults for optional arguments

### Line length and structure

- Maximum line length: 100 characters
- Avoid blank lines within a pipe chain
- One blank line between code blocks
- Two blank lines before a new section

## Naming
- Functions in `snake_case`, English
- Start with a verb: `transform_data()`, `create_plot()`, `add_ses()`, `get_fairness_conclusions()`
- Exception: Shiny modules use `camelCase` (Shiny convention)
- Variable names descriptive, immediately understandable, snake case
- Column names: see [Data Conventions](data-conventions.md) (preserve source names)

## Documentation

### Roxygen2 for all exported functions

```r
#' Transform raw enrollment data for analysis
#'
#' Combines enrollment and grade data, adds SES and APCG indicators,
#' creates missing-value indicators, and imputes missing numerics.
#'
#' @param metadata Named list from [read_metadata()].
#' @param opleidingsnaam Character. Name of the program.
#' @param opleidingsvorm Character. Program form ("VT", "DT", or "DU").
#'
#' @return A data frame with transformed and imputed data.
#'
#' @importFrom dplyr mutate across select
#' @export
transform_data <- function(metadata, opleidingsnaam, opleidingsvorm) {
```

- First line: short description (one sentence)
- Body: what the function does, in more detail
- `@param`: every parameter documented
- `@return`: what comes back
- `@importFrom`: explicit namespace imports
- `@export`: for user-facing functions

### Comments in scripts

```r
# Good: explains WHY
# Filter to first-year students only — retention is only meaningful for year 1
df <- df |>
  filter(INS_Studiejaar == 1)

# Bad: explains WHAT (obvious from the code)
# Filter the dataframe
df <- df |>
  filter(INS_Studiejaar == 1)
```

- Comments are directive and explain the **why**
- Use `##` (double hash) for comments, not `#`
- Avoid commented-out code — delete it (git remembers)
- Use `## TODO:` for temporary code that needs attention

## Error Handling

```r
# Good: cli for messages, rlang for errors
cli::cli_alert_info("Processing {.val {nrow(df)}} students")
if (nrow(df) == 0) rlang::abort("No students found for {opleidingsnaam}")

# Bad: base R
message(paste("Processing", nrow(df), "students"))
if (nrow(df) == 0) stop("No students found")
```

- Use `cli` package for informational messages
- Use `rlang::abort()` / `rlang::warn()` / `rlang::inform()` for conditions
- Guard clauses at function start for input validation

## Testing

```r
test_that("transform_data returns expected columns", {
  result <- transform_data(test_metadata, "Test", "VT")
  expect_s3_class(result, "data.frame")
  expect_true("retentie" %in% names(result))
})
```

- Use testthat (>= 3.0)
- Test file mirrors source file: `R/transform_data.R` → `tests/testthat/test-transform_data.R`
- Test expected outputs, edge cases, and error conditions
- Include small test fixtures in `tests/testthat/fixtures/`

## Dependency Management

- Use `renv` for reproducible environments
- After adding packages: `renv::snapshot()`
- On clone: `renv::restore()`
- Keep `renv.lock` in version control
- Don't commit the `renv/` library directory
