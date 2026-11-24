# Ontwikkelstack en tooling

Bij CEDA bouwen wij informatieproducten die onderwijsinstellingen in het mbo, hbo en wo veilig op hun eigen machine kunnen draaien. Onze ontwikkelstack is daarom gekozen op drie eisen: **lokaal uitvoerbaar zonder cloudverplichting**, **reproduceerbaar tussen instellingen** en **goed leesbaar voor zowel datawetenschappers als ontwikkelaars**.

Op deze pagina lees je uit welke lagen onze stack bestaat en waarom wij deze hulpmiddelen inzetten.

## Overzicht per laag

| Laag | Python-ecosysteem | R-ecosysteem | Waarom deze keuze? |
| :--- | :--- | :--- | :--- |
| **Taal & pakketvorm** | Python (>= 3.13) met `src/`-pakketopbouw | R met standaard pakketstructuur (`DESCRIPTION`, `R/`) | Elke analyse is installeerbaar, testbaar en herbruikbaar buiten losse notebooks. |
| **Omgeving & pakketbeheer** | `uv` (`pyproject.toml` + `uv.lock`) | `renv` (`renv.lock`) | Vastgepinde versies voorkomen "werkt wel op mijn laptop"-problemen. |
| **Dataverwerking** | `Polars` (en `pandas` voor uitwisseling) | `tidyverse` (`dplyr`, `tidyr`, `readr`, `arrow`) | Leesbare datapijplijnen en snelle verwerking van grote onderwijsbestanden. |
| **Opslagformaten** | Parquet (tussenstappen) + `;`-CSV (einduitvoer) | Parquet (tussenstappen) + `;`-CSV (einduitvoer) | Parquet bewaart datatypen tussen R en Python; puntkomma-CSV opent direct goed in Excel. |
| **Codekwaliteit & tests** | `ruff` (lint + opmaak) en `pytest` | `air` (opmaak), `roxygen2` en `testthat` | Eenduidige opmaak en automatische controles bij elke wijziging. |
| **Interactieve schil** | `Streamlit` (of Shiny voor Python) | `Shiny` | Collega's bij instellingen gebruiken modellen via een scherm zonder zelf code aan te passen. |
| **Rapportage & docs** | `Quarto` en `MkDocs Material` | `Quarto` | Reproduceerbare rapporten en doorzoekbare technische documentatie vanuit Markdown. |

## Ontwikkelomgeving en containers

Niet elke instelling heeft dezelfde rechten of lokale installaties op werkplekken. Daarom werken we met **devcontainers** (op basis van Docker of Podman):

- **Direct starten:** wie een project opent in VS Code, Positron of GitHub Codespaces krijgt direct de juiste versie van Python, R, systeemafhankelijkheden en hulpmiddelen.
- **Lokale dataverwerking:** de container draait lokaal bij de instelling, zodat gevoelige onderwijsdata de eigen omgeving niet hoeft te verlaten.
- Zie voor de gedetailleerde afspraken binnen het kernteam ook de werkafspraak [Devcontainer](../werkafspraken/devcontainer.md).

## Automatisering, CI en documentatie

- **GitHub Actions:** controleert bij pull requests automatisch code-opmaak, tests en documentatieopbouw voordat wijzigingen landen op `main`.
- **MkDocs Material:** bouwt dit ontwikkelaarshandboek en pakketdocumentatie rechtstreeks vanuit Markdown-bestanden in versiebeheer.
- **Slidev in Npuls-huisstijl:** presentaties schrijven we als Markdown in git, zodat huisstijl en inhoud gescheiden blijven; zie de werkafspraak [Presentaties](../werkafspraken/presentaties.md).

## AI-ondersteund ontwikkelen en herleidbaarheid

Waar AI-hulpmiddelen meeschrijven aan code of documentatie gelden twee vaste waarborgen:

1. **Vaste projectcontext (`CLAUDE.md`):** elke repository verwijst naar onze [ontwikkelstandaarden](../standards/principles.md), zodat gegenereerde code direct dezelfde pakketopbouw, naamgeving en teststructuur volgt.
2. **Sessie-vastlegging met Entire (binnen CEDA):** in het kernteam legt Entire prompts en sessiecontext vast naast commits, zonder persoonsgegevens; zie de [handleiding Entire CLI](../guides/entire-cli.md).

!!! warning "Geen echte studentgegevens in ontwikkeltools"
    Ontwikkelen, testen en werken met AI-hulpmiddelen doen wij uitsluitend op open onderwijsdata of synthetische demodata. Echte instellingsbestanden blijven lokaal en staan altijd in `.gitignore`.
