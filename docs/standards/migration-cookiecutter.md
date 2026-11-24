# Migratie vanuit Cookiecutter

Veel oudere data-science-projecten zijn opgezet met de klassieke *Cookiecutter Data Science*-indeling. Deze gids laat zien hoe je zo'n project stapsgewijs omzet naar de CEDA-pakketstandaard.

## Belangrijkste verschillen

| Cookiecutter-opzet | CEDA-pakketstandaard | Waarom deze keuze? |
| :--- | :--- | :--- |
| Losse scripts in `module/` of `scripts/` | Installeerbaar pakket in `src/project_name/` (of `R/`) | Herbruikbaar, goed testbaar en schone imports zonder pad-trucs. |
| `data/raw/`, `data/interim/`, `data/processed/` | `data/01-raw/`, `data/02-prepared/`, `data/03-output/` | Genummerde mappen tonen direct de volgorde van de pijplijn. |
| Geen gebruikersinterface | `app/` (Streamlit) of `inst/app/` (Shiny) | Ook collega's zonder programmeerkennis kunnen met de analyse werken. |
| Aanroep alleen via `Makefile` | `main.py` of `main.R` als vast startpunt (`Makefile` optioneel) | Duidelijk startpunt in elke editor en op elk besturingssysteem. |
| Losse configuratiebestanden | `config.toml` / `config.yml` bij de app + metadata in het pakket | Lokale paden gescheiden van referentietabellen die met het pakket meereizen. |
| Handmatige lokale installatie | `.devcontainer/` | Reproduceerbare ontwikkelomgeving voor iedere bijdrager. |

## Wat blijft behouden?

- De scheiding tussen verkenningsnotebooks en productiecode.
- Het werken met gescheiden datastappen (alleen met vaste nummering).
- Een optionele `Makefile` voor handige snelkoppelingen zoals `make test` of `make lint`.

## Stappenplan voor migratie

1. **Verplaats broncode naar het pakket:** zet losse modules uit `module/` of `scripts/` om naar functies in `src/project_name/` (met `__init__.py`) of `R/`.
2. **Maak het pakket installeerbaar:** voeg een volledige `[project]`-sectie toe aan `pyproject.toml` (of werk `DESCRIPTION` en `NAMESPACE` bij in R).
3. **Bundel referentiedata:** verplaats opzoektabellen en het datawoordenboek naar `src/project_name/metadata/` of `inst/metadata/`.
4. **Voeg de dunne applicatielaag toe:** maak `app/` (Streamlit) of `inst/app/` (Shiny) aan die uitsluitend pakketfuncties aanroept.
5. **Voeg `.devcontainer/` toe:** zorg dat nieuwe ontwikkelaars het project direct in een container kunnen openen.
6. **Hernoem de datamappen:** stap over op `data/01-raw/`, `data/02-prepared/` en `data/03-output/` en controleer `.gitignore`.
7. **Voeg synthetische demodata toe:** plaats voorbeelddata in `demo/`-submappen zodat iedereen de pijplijn direct kan testen zonder echte studentgegevens.
