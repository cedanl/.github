# Ontwikkelstandaarden

Welkom bij de technische standaarden van [CEDA](https://github.com/cedanl). Deze documenten leggen vast hoe wij onze R- en Python-pakketten voor onderwijsdata-analyse opbouwen, naamgeven, testen en documenteren.

Zo blijft code uit verschillende instellingen herkenbaar, herbruikbaar en direct lokaal uitvoerbaar.

## Overzicht van de standaarden

Lees eerst de ontwikkelprincipes en pak daarna het onderdeel dat past bij jouw taak of programmeertaal:

- **[Ontwikkelprincipes](principles.md)** — de twaalf vaste uitgangspunten voor al onze code in R en Python.
- **[Projectstructuur](project-structure.md)** — vaste mappenopbouw per type repository, inclusief eisen aan `README.md` en `CLAUDE.md`.
- **[Dataconventies](data-conventions.md)** — kolomnamen, bestandsformaten (Parquet en CSV), datamappen, privacy en `data_dictionary.csv`.
- **[Python-stijlgids](python-style.md)** — afspraken voor Python-pakketten met `uv`, `ruff`, `polars`, `pytest` en Streamlit.
- **[R-stijlgids](r-style.md)** — afspraken voor R-pakketten in het tidyverse-dialect met `renv`, `air`, `testthat` en Shiny.
- **[Migratie vanuit Cookiecutter](migration-cookiecutter.md)** — stappenplan om bestaande analyseprojecten om te zetten naar de CEDA-pakketstandaard.

## Hoe gebruik je deze standaarden?

### Voor ontwikkelaars bij instellingen en in het CEDA-team

Gebruik deze richtlijnen wanneer je een nieuw pakket opzet, een bestaande tool opschaalt of een pull request beoordeelt. Bestaande repositories groeien stapsgewijs naar deze standaard toe; nog niet elke oudere repository voldoet al op elk punt.

Zoek je een overzicht van de inhoudelijke producten die CEDA samen met instellingen ontwikkelt? Bekijk dan het actuele projectoverzicht op de [CEDA-community](https://edu.nl/twt84).

### Gebruik met AI-assistenten (`CLAUDE.md`)

Elke CEDA-repository verwijst vanuit `CLAUDE.md` naar deze standaarden, zodat ook AI-hulpmiddelen direct dezelfde structuur en stijl volgen:

```markdown
## Standaarden
Volg de technische standaarden van CEDA: https://cedanl.github.io/.github/standards/
```

In het CEDA-kernteam zijn deze standaarden daarnaast beschikbaar als interactieve commando's (zoals `/init-repo`, `/check-style` en `/migrate-cookiecutter`) binnen onze gedeelde ontwikkelcontainer.
