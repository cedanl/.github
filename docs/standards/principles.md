# Ontwikkelprincipes

Deze twaalf kernprincipes gelden voor alle repositories binnen `cedanl`, ongeacht of je in R of in Python werkt.

## 1. Pakket eerst

Elke repository is een volwaardig softwarepakket, ook wanneer er een interactief dashboard bij zit.

- **R:** volledige pakketstructuur (`DESCRIPTION`, `NAMESPACE`, `R/`, `man/`, `tests/`).
- **Python:** installeerbaar pakket met `pyproject.toml` en een `src/`-indeling.

**Waarom:** een pakket dwingt een heldere structuur af, maakt automatische tests mogelijk, legt afhankelijkheden vast en maakt functies herbruikbaar tussen projecten.

## 2. Interactieve modus

Elke repository bevat een laagdrempelige applicatie-interface (Shiny voor R, Streamlit voor Python) met een vaste configuratie voor lokale databestanden. Dat zorgt voor drie voordelen:

- Collega's bij instellingen kunnen de oplossing direct gebruiken zonder programmeerkennis.
- Ontwikkelaars kunnen uitkomsten van de pijplijn snel visueel controleren.
- Elke CEDA-oplossing voelt op dezelfde manier aan.

De applicatie roept alleen functies uit het pakket aan en bevat zelf géén reken- of bedrijfslogica.

## 3. Klaar voor devcontainers

Elke repository bevat een `.devcontainer/`-configuratie voor een reproduceerbare ontwikkelomgeving. Iedereen moet in drie stappen aan de slag kunnen:

1. Kloon de repository.
2. Open het project in VS Code, Positron of GitHub Codespaces.
3. Werk direct in een omgeving waarin alle pakketten en hulpmiddelen klaarstaan.

Dit maakt zowel lokaal testen zonder installatiegedoe als geautomatiseerd testen eenvoudig.

## 4. Scheiding van verantwoordelijkheden

Elk script of onderdeel doet één duidelijk afgebakende taak. We ordenen dataverwerking langs vaste stappen:

```text
inlezen > voorbereiden > transformeren > analyseren > visualiseren > exporteren
```

Niet elke repository doorloopt alle stappen. Bij complexe brondata met meerdere toepassingen heeft een losse inlees-repository grote voordelen. Binnen één repository geldt altijd:

- Herbruikbare functies staan in het pakket (`R/` of `src/`).
- Scripts die de pijplijn aansturen (`main.R` of `main.py`) staan los van de functiedefinities.
- Configuratie staat los van de programmalogica.

## 5. Functioneel programmeren

Schrijf zuivere functies en schakel ze aan elkaar:

- Geef functies expliciete invoer en uitvoer mee.
- Gebruik pijplijnen (`|>` in R, methodeketens in Python) voor datatransformaties.
- Vermijd neveneffecten in kernfuncties; houd lezen en schrijven van bestanden aan de randen van je pijplijn.

## 6. Leesbaarheid voorop

Schrijf code voor mensen om te begrijpen, niet om de laatste milliseconde snelheid te winnen:

- Gebruik leesbare, gangbare bouwstenen (`tidyverse` in R, `Polars` of `pandas` in Python).
- Kies duidelijke, beschrijvende functienamen boven cryptische afkortingen.
- Gebruik bekende pakketten met een heldere API.
- Optimaliseer pas voor snelheid wanneer metingen laten zien waar een echt knelpunt zit.

## 7. Het rechte pad (guard clauses)

Beperk inspringniveaus. De hoofdlogica staat zo ver mogelijk links, terwijl randgevallen bovenaan een functie direct worden afgevangen:

- Gebruik vroege controles (*guard clauses*) in plaats van diep geneste `if`/`else`-blokken.
- Kies `purrr::map()` of lijstbegrip (*list comprehensions*) boven handmatige lussen met tellervariabelen.
- Eindigt een `if`-blok met een foutmelding of `return()`, laat `else` dan weg.

```r
## Goed: vroege controle bovenaan de functie
get_data <- function(config) {
  if (!valid_config(config)) rlang::abort("Ongeldige configuratie")
  if (!can_connect()) rlang::abort("Geen verbinding mogelijk")

  data <- fetch_data(config)
  return(clean_data(data))
}

## Vermijden: onnodig diep genest
get_data <- function(config) {
  if (valid_config(config)) {
    if (can_connect()) {
      data <- fetch_data(config)
      return(clean_data(data))
    }
  }
}
```

## 8. Zelfdocumenterende code

Goede naamgeving is de beste documentatie. Maak de bedoeling van elk onderdeel zichtbaar in de naam:

- Functienamen bestaan uit `werkwoord_onderwerp` (zoals `transform_enrollment_data` of `create_fairness_plot`).
- Variabelenamen volgen herkenbare bronconventies; zie [Dataconventies](data-conventions.md).
- Commentaar legt uit **waarom** iets gebeurt, niet **wat** de code zichtbaar al doet.
- Gebruik expliciete `return()`-aanroepen in R en type-annotaties in Python.

## 9. Uitbreidbaarheid

Schrijf code die eenvoudig aan te passen is voor een volgende instelling of onderwijssector:

- Geef functies logische standaardwaarden mee voor optionele parameters.
- Haal vaste drempelwaarden en bestandspaden uit de code naar configuratiebestanden.
- Maak eerst de aanpassing eenvoudig, en voer daarna de eenvoudige aanpassing door.

## 10. Stapsgewijs opschonen (refactoring)

Goede code ontstaat in slagen:

1. Bouw eerst een werkende oplossing.
2. Trek herbruikbare onderdelen naar pakketfuncties met tests.
3. Laat collega's en gebruikers bij instellingen de uitkomsten toetsen.
4. Schoon de code op aan de hand van hun terugkoppeling.

Doordat onze patronen hier vastliggen, verschuift dit steeds vaker naar *prefactoring*: vanaf het begin overzichtelijke code schrijven.

## 11. Keuze van afhankelijkheden

Stel jezelf vier vragen voordat je een extra pakket toevoegt:

- **Wordt het pakket actief onderhouden?** Controleer recente releases en openstaande problemen.
- **Wie beheert het?** Geef de voorkeur aan gevestigde gemeenschappen (zoals Posit, rOpenSci of breed gedragen Python-projecten) boven eenmansprojecten.
- **Is het echt nodig?** Elke extra afhankelijkheid vergroot de onderhoudslast; voor vijf regels logica volstaat een eigen hulpfunctie.
- **Past het in ons ecosysteem?** Raadpleeg de voorkeurspakketten in de [Python-stijlgids](python-style.md) en [R-stijlgids](r-style.md).

## 12. Codebeoordeling

Elke wijziging wordt vóór samenvoegen beoordeeld via een pull request. Bij een review letten we op:

- Aansluiting op deze ontwikkelprincipes.
- Inhoudelijke juistheid en afhandeling van randgevallen.
- Leesbaarheid en naamgeving.
- Aanwezigheid van automatische tests.
