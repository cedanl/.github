# Dataconventies

Deze afspraken zorgen voor eenduidige kolomnamen, uitwisselbare bestandsformaten en veilige omgang met onderwijsdata in alle CEDA-projecten.

## Kolomnamen

### Behoud bronnamen waar mogelijk

Houd de oorspronkelijke kolomnamen uit landelijke bronnen (zoals 1CijferHO, Studielink of DUO-bekostigingsbestanden) zoveel mogelijk aan. Zo blijven velden herleidbaar naar de brondocumentatie en direct herkenbaar voor collega's bij instellingen.

### Nieuwe en afgeleide variabelen

Maak je een berekende of afgeleide kolom aan? Sluit dan aan bij de stijl van de brondata en volg deze regels:

- Kies een beschrijvende naam die zonder uitleg te begrijpen is; liever iets langer dan onduidelijk kort.
- Gebruik alleen letters, cijfers en liggende streepjes (`_`).
- Gebruik geen spaties en geen diakritische tekens (geen trema's of accenten).

### Vaste achtervoegsels voor afgeleide kolommen

| Achtervoegsel | Betekenis | Voorbeeld |
| :--- | :--- | :--- |
| `_cat` | Ingedeelde of gecategoriseerde waarde | `hoogste_vooropleiding_soort_cat` |
| `_code` | Numerieke code bij een tekstwaarde | `vooropleiding_voor_ho_code` |
| `_datum` | Datumveld | `leeftijd_peildatum_1_oktober_datum` |
| `_norm` | Gestandaardiseerde of genormaliseerde waarde | `INS_Score_norm` |

## Bestandsformaten

### Tussenbestanden binnen een pijplijn

Gebruik **Parquet** voor alle tussenliggende bestanden in `02-prepared/`. Parquet leest en schrijft razendsnel, is compact, behoudt exacte datatypen en werkt naadloos in zowel R als Python.

### Einduitvoer voor gebruikers en vervolgstappen

Lever eindresultaten in `03-output/` altijd in twee formaten op:

- **Parquet** — voor geautomatiseerd hergebruik in vervolganalyses.
- **CSV** — voor collega's die uitkomsten willen openen in Excel, Power BI of andere hulpmiddelen.

### Afspraken voor CSV-bestanden

- **Scheidingsteken:** puntkomma (`;`) — de standaard voor Nederlandse Excel-instellingen en veilig naast komma's in decimaalgetallen.
- **Tekencodering:** altijd `UTF-8` (zet afwijkende broncoderingen al tijdens de inleesstap om naar UTF-8).
- **Tekstvelden:** plaats tekstvelden die een puntkomma kunnen bevatten tussen aanhalingstekens.

## Indeling van datamappen

```text
data/
  01-raw/          # Ongewijzigde bronbestanden (alleen-lezen)
  02-prepared/     # Opgeschoonde tussenbestanden in Parquet-formaat
  03-output/       # Eindresultaten in zowel Parquet als CSV
```

- Overschrijf nooit bestanden in `01-raw/`.
- Zet alle mappen met echte instellingsdata in `.gitignore`.
- Voeg waar mogelijk synthetische demodata toe in een `demo/`-submap, zodat iedereen de code direct kan draaien.

## Privacy en gevoelige gegevens

### Basisregels

- **Commit nooit persoonsgegevens** (zoals BSN, namen, e-mailadressen of studentnummers) naar git, ook niet naar besloten repositories.
- **Pseudonimiseer direct bij het inlezen** voordat data naar `02-prepared/` wordt geschreven.
- **Leg gevoelige velden vast** in het datawoordenboek met `sensitive = true`.
- Zie voor feedback uit apps of sessies ook de werkafspraak [Feedback zonder persoonsgegevens](../werkafspraken/feedback-zonder-persoonsgegevens.md).

### Dataclassificatie

| Niveau | Omschrijving | Omgang |
| :--- | :--- | :--- |
| **Openbaar** | Geaggregeerde statistieken, open onderwijsdata of synthetische demodata | Mag in de repository staan. |
| **Intern** | Gepseudonimiseerde gegevens op individueel niveau | Altijd in `.gitignore`; blijft op de machine van de instelling of binnen een beveiligde omgeving. |
| **Gevoelig** | Bevat BSN, naam of andere direct herleidbare persoonsgegevens | Verwijderen of hashen tijdens de allereerste inleesstap; verlaat nooit ruwe opslag. |

## Aannames en datakwaliteit vastleggen

Elke repository die data verwerkt legt vier zaken vast:

1. **Verwacht invoerformaat** — benodigde velden, datatypen en herkomst.
2. **Transformatielogica** — welke bewerkingen plaatsvinden en waarom (in codecommentaar en metadata).
3. **Bekende datakwaliteitspunten** — ontbrekende waarden, afwijkingen per studiejaar en gekozen oplossingen.
4. **Uitvoerschema** — de precieze kolommen en betekenissen van de eindtabel.

## Datawoordenboek (`data_dictionary.csv`)

Elke repository die datasets oplevert bevat een actueel datawoordenboek in zowel machineleesbare als mensleesbare vorm.

### Machineleesbaar: `data_dictionary.csv`

Een puntkomma-gescheiden UTF-8-bestand in de metadatamap van het pakket (`inst/metadata/data_dictionary.csv` in R, `src/<pakket>/metadata/data_dictionary.csv` in Python):

| Kolom | Verplicht | Beschrijving |
| :--- | :--- | :--- |
| `dataset` | ja | Naam van de uitvoertabel (bijv. `instroom_2026`). |
| `column_name` | ja | Exacte kolomnaam in de dataset. |
| `description` | ja | Heldere omschrijving van de variabele. |
| `type` | ja | Datatype: `character`, `integer`, `double`, `date` of `boolean`. |
| `source` | ja | Bronsysteem of `derived` bij afgeleide kolommen. |
| `example` | nee | Voorbeeldwaarde (nooit een echt persoonsgegeven). |
| `allowed_values` | nee | Toegestane waarden of bereik (bijv. `1-5` of `MBO;HBO;WO`). |
| `sensitive` | nee | `true` wanneer het veld persoonsgevoelige informatie raakt. |

### Mensleesbare weergave

Genereer vanuit `data_dictionary.csv` automatisch een overzichtelijke tabel in een Quarto-rapport, R-vignette (`DT::datatable()` of `gt::gt()`) of een toelichtingspagina in de Streamlit- of Shiny-app. Werk het woordenboek direct bij zodra kolommen wijzigen.
