# Kwaliteitschecks — de vier guards in detail

Concrete checks per valkuil. Doorloop deze tijdens Stap 2 (clean laag) en Stap 3
(branch-transforms). Wat je vindt maar niet zeker weet → vraag; wat je corrigeert
→ noteer in het opschoonrapport.

## 1. Data leakage (zwaarst voor het ML-spoor)

Leakage = het model leert van informatie die op het voorspelmoment niet bestaat.
Het geeft te-mooie-om-waar validatiescores en faalt in productie.

Checks:

- **Tijdslijn-toets.** Voor elke feature: *is deze waarde bekend op het moment
  dat we voorspellen?* Zo nee → verwijderen of vervangen door een lagged versie.
- **Target-afgeleiden.** Kolommen die (deels) uit de target zijn berekend, of die
  na de target-gebeurtenis zijn ingevuld → verwijderen.
- **Verdachte correlatie.** Een feature die bijna perfect met de target
  correleert is vaak leakage, geen signaal → onderzoek de herkomst, vraag.
- **Split-hygiëne.** Fit imputers/encoders/scalers **alleen op train**, transform
  op val/test. Nooit statistieken over de hele set berekenen vóór de split.
- **Groeps-/tijd-leakage.** Bij herhaalde metingen per entiteit of tijdreeks:
  splits op entiteit/tijd, niet willekeurig, anders lekt informatie tussen
  train en test.
- **ID's & vrije tekst.** Rauwe ID's, timestamps of vrije tekst als feature
  kunnen memorization veroorzaken → bewust encoden of weglaten.

## 2. Dtypes & schema-drift

Checks:

- Dwing verwachte dtypes expliciet af; laat pandas/polars types niet raden.
- Parse datums expliciet met bekend formaat; faal bij niet-parsebare waarden i.p.v.
  ze op NaT te zetten.
- Zet categorische kolommen op `category`/enum; controleer op onverwachte niveaus.
- **Schema-drift = fail-fast:** onbekende kolom, ontbrekende verwachte kolom, of
  gewijzigd type → stop en rapporteer tegen het data-contract.
- Detecteer gemengde types binnen één kolom (getallen als string, `"1.0"` vs `1`).
- Normaliseer tekst waar nodig (trim whitespace, case, gecodeerde tekens), maar
  behoud betekenisdragende varianten — vraag bij twijfel.
- Numerieke sentinels (-999, 9999, 0-als-missing) → herken en behandel als
  missing, niet als waarde. Vraag als de betekenis onzeker is.

## 3. Missings & outliers

Checks:

- **Per kolom een expliciete strategie**, gedocumenteerd: drop, impute
  (welke methode + waarom), of flag-kolom + impute. Nooit een blinde globale
  `dropna()`/`fillna(0)`.
- Missings >~30% in een kolom → beslissing vereist een vraag: droppen, of is
  "missing" zelf een signaal (dan een expliciete indicator-kolom)?
- Imputeer split-veilig (statistiek uit train).
- **Outliers:** detecteer (IQR, z-score, of domeinranges) en **log** ze; verwijder
  of cap alleen met expliciete reden. Een outlier kan een fout óf een echt
  extreem geval zijn — vraag bij twijfel, verwijder niet stil.
- Controleer op onmogelijke waarden (negatieve leeftijd, percentage >100,
  toekomstige datum) → deze horen bij domein-invarianten in het contract.

## 4. Temporele integriteit

Voor tijdreeks-/paneldata (zoals wekelijkse snapshots):

- **Ordening bewaren.** Nooit shufflen; sorteer op tijd (en entiteit) en houd dat.
- **Duplicaten per tijdstap.** Controleer op meerdere rijen voor dezelfde
  (entiteit, periode) — vaststellen of het fout is of legitiem vóór aggregatie.
- **Consistente periodering.** Uniforme week-/maand-/jaardefinitie (let op
  ISO-week vs volgnummer, jaargrenzen). Vraag welke conventie geldt.
- **Gaten in de tijdas.** Ontbrekende periodes expliciet maken (reindexen) i.p.v.
  onzichtbaar overslaan; beslis bewust of gaten geïmputeerd of gemarkeerd worden.
- **Aggregatie-niveau.** Cumulatief vs per-periode niet door elkaar halen; bij
  optellen over tijd de granulariteit expliciet houden.
- **Lagging.** Bij features uit het verleden: shift correct zodat er geen waarde
  uit de toekomst binnenkomt (raakt ook leakage-guard).

## Snelle poort vóór je oplevert

- [ ] Elke kolom in elke output heeft een bekende dtype en betekenis.
- [ ] Geen kolom die op voorspelmoment onbekend zou zijn in de ML-output.
- [ ] Missings-strategie per kolom expliciet en gedocumenteerd.
- [ ] Encoders/scalers alleen op train gefit.
- [ ] Tijdordening en granulariteit intact; duplicaten verantwoord.
- [ ] Data-contract + opschoonrapport gegenereerd.
- [ ] Alle niet-triviale of dubbelzinnige keuzes zijn gevraagd of gerapporteerd.
