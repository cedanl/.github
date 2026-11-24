# R-stijlgids

Deze stijlgids beschrijft hoe wij R-code schrijven binnen `cedanl`. We volgen de [Tidyverse style guide](https://style.tidyverse.org/), aangevuld met vaste afspraken voor CEDA-pakketten.

## Ecosysteem

### Tidyverse-dialect

We schrijven R in het tidyverse-dialect zodat datapijplijnen voorspelbaar en goed leesbaar blijven:

- Gebruik de ingebouwde R-pijp `|>` (niet `%>%`).
- Geef de voorkeur aan tidyverse-functies wanneer die leesbaarder zijn (`str_detect()` boven `grepl()`, `read_csv()` boven `read.csv()`).
- Gebruik `tidymodels` voor voorspelmodellen en `ggplot2` voor grafieken.

### Voorkeurspakketten

| Domein | Pakket | Toelichting |
| :--- | :--- | :--- |
| Databewerking | `dplyr`, `tidyr` | Kern van de datapijplijn. |
| Tekstbewerking | `stringr` | Consistente `str_`-functies. |
| Datum en tijd | `lubridate` | Leesbare datumberekeningen. |
| Inlezen en opslaan | `readr`, `arrow` | `read_csv()` en `read_parquet()`. |
| Modelleren | `tidymodels` | Eenduidige workflow voor recepten, modellen en evaluatie. |
| Grafieken | `ggplot2`, `ragg` | Heldere visualisaties met scherpe weergave. |
| Tabellen en rapporten | `flextable`, `gtsummary`, `quarto` | Reproduceerbare rapportages in `.qmd`. |
| Interactieve app | `shiny` | Gebruikersschil voor instellingen. |
| Meldingen en fouten | `cli`, `rlang` | `cli_alert_info()` en `rlang::abort()` in plaats van `stop()`. |
| Paden en herhaling | `fs`, `purrr`, `janitor` | Platformonafhankelijke paden, `map()` en `clean_names()`. |

Zie [Ontwikkelprincipes §11](principles.md#11-keuze-van-afhankelijkheden) voor het afwegen van extra pakketten.

## Pakketopbouw

Elke R-repository is een volwaardig R-pakket. Zie [Projectstructuur](project-structure.md) voor de volledige mappenindeling.

### Functiebestanden in `R/`

- Zet één hoofdfunctie per bestand met eventuele hulpfuncties daaronder.
- Laat de bestandsnaam aansluiten op de hoofdfunctie (`R/transform_data.R` bevat `transform_data()`).

### `main.R`

`main.R` staat in de hoofdmap van de repository (buiten `R/`) en stuurt de volledige pijplijn aan:

```r
## Laad het lokale pakket
devtools::load_all()

## Configuratie
opleidingsnaam <- "Informatica"
opleidingsvorm <- "VT"

## Voer de pijplijn uit
metadata <- read_metadata()
programs <- transform_data(metadata, opleidingsnaam, opleidingsvorm)
results <- run_analysis(programs)
render_report(results)
```

### Shiny-applicatie (`inst/app/`)

In R staat de Shiny-app **binnen** het pakket onder `inst/app/`, met een opstartfunctie in `R/run_app.R`:

```r
#' Start de interactieve applicatie
#'
#' @param ... Argumenten doorgegeven aan [shiny::runApp()].
#' @export
run_app <- function(...) {
  if (!requireNamespace("shiny", quietly = TRUE)) {
    rlang::abort("Pakket {.pkg shiny} is nodig. Installeer met install.packages('shiny').")
  }
  app_dir <- system.file("app", package = "mijnpakket")
  shiny::runApp(app_dir, ...)
}
```

- Zet `shiny` onder `Suggests:` in `DESCRIPTION`, zodat het pakket ook zonder Shiny bruikbaar blijft.
- Houd `inst/app/app.R` vrij van rekenlogica; roep alleen pakketfuncties aan.

## Schrijfstijl en syntaxis

### Toekenning en pijpen

```r
## Goed
students <- students_raw |>
  filter(INS_Studiejaar == 2026) |>
  select(INS_Studentnummer, INS_Opleidingsnaam)

## Vermijden
students = students_raw %>%
  filter(INS_Studiejaar == 2026) %>%
  select(INS_Studentnummer, INS_Opleidingsnaam)
```

- Gebruik `<-` voor toekenning en `|>` voor pijplijnen.
- Houd de regelbreedte op maximaal 100 tekens.

### Functiedefinities

Gebruik expliciete `return()`-aanroepen, logische standaardwaarden en benoem argumenten bij aanroepen met meer dan twee parameters:

```r
calculate_retention <- function(df,
                                year = 2026,
                                min_credits = 0,
                                include_masters = FALSE) {
  df <- df |>
    filter(INS_Studiejaar == year)

  return(df)
}
```

### Naamgeving

- Functies en variabelen in `snake_case`, startend met een werkwoord (`transform_data()`, `create_plot()`).
- Uitzondering: Shiny-modules volgen de gangbare `camelCase`-conventie van Shiny.
- Kolomnamen volgen onze [Dataconventies](data-conventions.md).

## Documentatie en commentaar

Documenteer elke geëxporteerde functie met `roxygen2` (`@param`, `@return`, `@importFrom`, `@export`). Gebruik in scripts dubbele hekjes (`##`) voor commentaar dat uitlegt **waarom** een keuze is gemaakt, en verwijder uitgecommentarieerde code.

## Foutafhandeling en testen

Gebruik `cli` voor meldingen en `rlang::abort()` voor foutcondities:

```r
cli::cli_alert_info("{.val {nrow(df)}} inschrijvingen worden verwerkt")
if (nrow(df) == 0) {
  rlang::abort("Geen inschrijvingen gevonden voor {opleidingsnaam}")
}
```

Test elke functie met `testthat` (>= 3.0) in `tests/testthat/test-<functienaam>.R`, inclusief kleine synthetische testbestanden onder `tests/testthat/fixtures/`.

## Automatische opmaak en versiebeheer

Gebruik [air](https://posit-dev.github.io/air/) om R-bestanden automatisch en eenduidig op te maken:

```bash
air format .
air format --check .
```

Beheer pakketversies met `renv`: leg versies vast in `renv.lock` met `renv::snapshot()`, herstel ze met `renv::restore()` en zet de lokale map `renv/library/` in `.gitignore`.
