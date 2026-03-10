# CEDA Development Principles

Core principles that apply to all cedanl repositories, regardless of language (R or Python).

## 1. Package-First Development

Every repository is a proper package — even when it also has an interactive interface.

- **R**: Full R package structure (DESCRIPTION, NAMESPACE, R/, man/, tests/)
- **Python**: Proper package with `pyproject.toml` and `src/` layout

Why: Packages enforce structure, enable testing, manage dependencies explicitly, and make code reusable across projects.

## 2. Interactive Mode

Every repo includes a simple app interface (Shiny for R, Streamlit for Python) with configuration fixed for local data. This enables:

- Immediate use without programming knowledge
- Quick validation of pipeline results during development
- A consistent way to interact with any CEDA tool

The app wraps the package functions — it does not contain business logic itself.

## 3. Devcontainer-Ready

All repos include a `.devcontainer/` configuration for reproducible development environments. Any contributor should be able to:

1. Clone the repo
2. Open in VS Code / GitHub Codespaces
3. Have a working environment with all dependencies

This also enables running the interactive interface without local setup and automatic testing in VMs.

## 4. Separation of Concerns

Each script or module does one thing. Code is organized into clear pipeline stages:

```
ingest > prepare > transform > analyze > visualize > export
```

Not all repos use all stages. For complex raw data with several use cases, a speficic ingestion repo has benefits (1CijferHO). For one model there might be several use cases with own visualization needs.

Within a repo:

- Reusable functions live in the package (R/ or src/)
- Pipeline orchestration scripts are separate from function definitions
- Configuration is separate from logic

## 5. Functional Programming

Write functions. Compose them.

- Prefer pure functions with explicit inputs and outputs
- Use pipe operators (`|>` in R, method chaining in Python) for data transformation chains
- Avoid side effects in core functions — keep I/O at the boundaries
- Functions can take and return other functions (higher-order functions like decorators)

## 6. Interpretability First

Write code for humans to read, not for computers to execute fast.

- Use high-level, readable constructs (tidyverse in R, Polars/Pandas in Python)
- Prefer clear, descriptive function names over terse ones
- Choose well-known packages with intuitive APIs over raw performance
- Only optimize for algorithmic efficiency when profiling shows a bottleneck

## 7. Happy Path

Minimize indentation levels. The main logic should run at the lowest indentation possible.

- Use guard clauses and early returns instead of deeply nested if/else
- Prefer `purrr::map()` / list comprehensions over explicit for-loops with index tracking
- An if-block that ends with `stop()` or `return()` does not need an `else`

```r
# Good: guard clause
get_data <- function(config) {
  if (!valid_config(config)) stop("Invalid config")
  if (!can_connect()) stop("Cannot connect")

  data <- fetch_data(config)
  clean_data(data)
}

# Bad: nested
get_data <- function(config) {
  if (valid_config(config)) {
    if (can_connect()) {
      data <- fetch_data(config)
      clean_data(data)
    }
  }
}
```

## 8. Self-Documenting Code

Names are documentation. Make the intent of every object explicit through its name.

- Function names: verb + object (`transform_enrollment_data`, `create_fairness_plot`)
- Variable names: descriptive, following source conventions (see [Data Conventions](data-conventions.md))
- Comments explain **why**, not **what** — the code shows what happens

Use explicit `return()` statements in R. Use type hints in Python.

## 9. Extensibility

Write code that is easy to modify and extend.

- Functions with sensible defaults and optional arguments
- Extract hard-coded values into configuration
- *"For each desired change, make the change easy (warning: this may be hard), then make the easy change"* — Kent Beck

## 10. Refactoring as Practice

Code improves through iteration:

1. Write working code (possibly messy)
2. Extract reusable parts into package functions
3. Let colleagues (and users!) validate the code
4. Refactor based on feedback

Over time, this becomes **prefactoring**: writing cleaner code from the start because the patterns are written down for AI-coding toolings and internalized for humans.

## 11. Dependency Selection

Before adding a new dependency, evaluate:

- **Actively maintained?** Check the last commit date.
- **Who maintains it?** Prefer Posit/RStudio, rOpenSci, or established Python organizations over individual repos.
- **Neccesary?** Every additional dependency is also a possible weakness. Internal functions might be better.
- **Ecosystem fit?** See the specifik R and python standards for preferred packages.

## 12. Code Review

All new code is (automatically) reviewed before merge. Reviews check for:

- Adherence to these principles
- Correctness and edge cases
- Readability and naming
- Test coverage
