# Data-contract + opschoonrapport — sjabloon

Elke run levert deze twee artefacten op. Het contract maakt fail-fast
herhaalbaar: bij een volgende run valideer je nieuwe data ertegen en stop je bij
drift. Het rapport maakt elke opschoonbeslissing review-baar.

Lever bij voorkeur machine-leesbaar (JSON/YAML) én een korte menselijke
samenvatting. Genereer een contract per output-laag (clean, ml-ready,
dashboard-ready), want hun schema's verschillen.

## Data-contract (per output-laag)

```yaml
laag: ml-ready            # clean | ml-ready | dashboard-ready
bron: <pad/naam van de bron(nen)>
granulariteit: <wat is één rij, bv. "één instelling-week">
unieke_sleutel: [kolom_a, kolom_b]   # samen uniek; run een uniciteitscheck
rij_aantal_verwacht: <n of range>
kolommen:
  - naam: <kolomnaam>
    dtype: <int64 | float64 | category | datetime64 | bool | string>
    nullable: false
    toegestane_waarden: [..]          # voor categorieën
    range: [min, max]                 # voor numeriek
    betekenis: <één zin>
    herkomst: <bron-kolom of afleiding>   # cruciaal voor leakage-audit
invarianten:
  - "kolom_x >= 0"
  - "som(deel) == totaal per (entiteit, periode)"
  - "datum <= voorspelmoment"          # leakage-invariant
```

## Opschoonrapport

```yaml
samenvatting:
  bron_rijen: <n>
  clean_rijen: <n>
  verwijderd: <n> ( <reden per groep> )
kolom_acties:
  - kolom: <naam>
    actie: <dtype-cast | rename | drop | impute | flag | cap>
    detail: <bv. "median-impute op train (waarde=X), 42 cellen">
    reden: <waarom>
missings:
  - kolom: <naam>
    pct_voor: <..>
    strategie: <drop | impute:<methode> | flag+impute>
outliers:
  - kolom: <naam>
    methode: <IQR | zscore | domeinrange>
    aantal: <n>
    behandeling: <gelogd | capped | verwijderd>  # + reden
leakage_audit:
  verwijderde_features: [..]           # met reden per stuk
  split_strategie: <random | tijd | groep>  # en waarop
openstaande_vragen:
  - <alles wat je hebt gevraagd en het antwoord, of nog open staat>
```

## Validatie tegen het contract (volgende run)

Bij nieuwe data: laad het contract en check per output-laag:
kolomset gelijk, dtypes gelijk, nullability gerespecteerd, waarden binnen
`toegestane_waarden`/`range`, unieke sleutel uniek, alle `invarianten` waar.
Elke schending → **stop en rapporteer** (fail-fast), niet stil doorgaan.
