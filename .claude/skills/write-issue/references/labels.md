# De labelindeling — categorieën, condities en uitbreiden

Zes categorieën, één kleur per categorie. Een label zegt dus twee dingen tegelijk: wat het
betekent, en aan welke as het hangt — dat laatste zie je aan de kleur, zonder te lezen.

**De namen, kleuren en beschrijvingen staan in `labels.yml`, hiernaast.** Dat bestand is de
machine-bron: `.github/workflows/sync-labels.yml` in `cedanl/.github` leest het en duwt de set
wekelijks naar alle cedanl-repos. Dit document draagt de indeling en de regels; het herhaalt
de lijst niet, want twee lijsten lopen uit elkaar. Wat er nú in een repo staat:
`gh label list --repo cedanl/<repo>`.

Bewerk altijd het origineel in `cedanl/.github`. Een kopie van deze skill in een andere repo
draagt `labels.yml` mee, maar daar draait geen sync — daar is het dood gewicht.

## De indeling

| Categorie | Kleur | Wanneer | Waarden |
|---|---|---|---|
| **soort** | blauw | altijd één | `intern` · `impact` · `tech` · `core` |
| **intern** | groen | alleen bij `intern` | `project` · `skills` · `way-of-working` |
| **impact** | magenta | alleen bij `impact` | `bijeenkomst` · `presentatie` · `publicatie` · `adoptie` |
| **tech** | paars | alleen bij `tech` | `gui` · `sdp` · `object-store` · `research-cloud` |
| **werk** | turquoise | alleen bij `core` | `data` · `ml` · `governance` · `visuals` · `chat` |
| **aspect** | grijs | bij elk soort, optioneel | `docs` · `ux` |
| **inhoud** | oranje | meestal bij `impact` of `core` | `instroom` · `studiesucces` · `arbeidsmarkt` · `flexibilisering` |
| **status** | geel | zelden | `needs-shaping` |

De soort bepaalt welke tweede categorie in beeld komt. Bij `impact` komt daar meestal ook
`inhoud` bij: de vorm (een bijeenkomst) en het onderwerp (studiesucces) zijn twee verschillende
vragen.

**`aspect` staat los van de soort**, en dat is het verschil met `werk`. De werk-labels zijn
gebieden uit onze eigen indeling — data, ml, governance, visuals, chat. `docs` en `ux` zijn
dat niet: je documenteert een ml-pipeline, je ontwerpt de interactie van een chattool, je
schrijft docs bij een sdp-deployment. Ze hangen dus aan elk soort en aan elk gebied, en niet
onder één ervan. Vandaar een eigen as met een neutrale kleur.

## Twee paren die op elkaar lijken

**`gui` versus `ux`.** `gui` is een technisch oppervlak, net als `sdp` en `object-store`: er
is een app of dashboard in het spel. `ux` is een aspect: flow, formulering, wat de gebruiker
begrijpt. Een issue "bouw de configuratie-editor" is `tech` + `gui`; een issue "vereenvoudig
de synthesizer-keuze" is `core` + `ux`. Werk dat allebei is, krijgt allebei — dat is
informatie, geen dubbeling.

**`docs` versus `publicatie`.** `docs` beschrijft iets wat wij bouwen, voor wie het gebruikt
(README, mkdocs, dataspec) en is een aspect van dat werk. `publicatie` is het werk zelf: iets
dat naar buiten gaat en een publiek heeft (blog, artikel, rapport). Twee verschillende lezers,
twee verschillende assen.

**Alles is optioneel, ook de soort.** De indeling is een suggestie die het kiezen makkelijker
maakt, geen invulplicht. Geen passend label is een geldige uitkomst; een verkeerd label is
duurder dan geen label, want er wordt op gefilterd.

## Wat géén label is

| Wel op het CEDA Board, niet als label | Waarom |
|---|---|
| Priority (High/Medium/Low) | Bestaand veld op het board, net als Iteration |
| Iteration | Bestaand veld |
| Status / On Hold | Bestaande Status-opties op het board |
| Type (Bug/Task/Pitch) | GitHub issue type, geen label |

Zie je nog `high-priority`, `low-priority` of `on-hold` op oude issues: dat is de oude
werkwijze, niet iets om te kopiëren.

## Uitbreiden

Een nieuw label mag, maar hangt aan een bestaande categorie — anders groeit de lijst en
verdwijnt de betekenis van de kleur.

1. **Welke categorie?** Past het in geen enkele, dan is het waarschijnlijk geen label maar een
   boardveld, een issue type, of iets dat in de body hoort.
2. **Toets op bestaand gebruik.** Zoek eerst of het al informeel bestaat:
   ```bash
   gh search issues --owner cedanl --limit 200 --state open --json labels --jq '.[].labels[].name' | sort | uniq -c | sort -rn
   ```
   Eén issue is geen label. Een terugkerend thema over meerdere repo's wel.
3. **Neem de kleur van de categorie over**, letterlijk dezelfde hex.
4. **Schrijf de beschrijving als `Categorie: betekenis`**, zoals de bestaande.
5. **Voeg toe aan `labels.yml`** hiernaast, in de juiste sectie, en open een PR. De sync doet de
   rest; wachten hoeft niet, `gh label create` mag lokaal vooruitlopen.

Repo-specifieke labels (`radboud`, `UVA`, `wayfinder:*`) staan hier bewust buiten: die horen
in de repo zelf en niet in de org-brede lijst.

## Let op: de sync verwijdert nooit

`sync-labels.yml` draait `gh label create --force`: aanmaken en bijwerken, nooit weggooien.
Een label uit `labels.yml` halen laat 'm in elke repo staan, inclusief op de issues die 'm al
dragen. Echt opruimen is een aparte actie (`gh label delete` per repo) en haalt het label van
bestaande issues af — dus alleen bewust, nooit en passant.
