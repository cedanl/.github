# Modelkaart — sjabloon

Beknopte eindsamenvatting bij elke modelleer-sessie. Doel: iemand anders (of jij
over drie maanden) begrijpt wat het model doet, hoe goed het is, en wanneer je de
output níét moet vertrouwen — zonder de code te lezen.

```yaml
taak: <regressie | classificatie | tijdreeks-forecast>
target: <wat wordt voorspeld> op <voorspelmoment: welke info is dan bekend>
data:
  bron: <ML-ready output van data-cleaner / pad>
  omvang: <n rijen, periode, granulariteit>
features:
  gebruikt: [..]                 # eventueel top-N + verwijzing naar volledige lijst
  herkomst_check: <bevestig: geen feature met toekomstinfo / target-afgeleide>
model:
  type: <baseline + gekozen model>
  hyperparameters: {..}
validatie:
  opzet: <random | gestratificeerd | tijd | groep> — <waarom deze>
  testset: <hoe apart gehouden, één keer gebruikt: ja/nee>
resultaten:
  primaire_metriek: <naam> = <waarde ± spreiding>
  baseline: <naam> = <waarde>     # het model MOET dit verslaan
  secundair: {..}
  faalgevallen: <waar/voor welk segment presteert het slecht>
interpretatie:
  top_features: [..]              # getoetst aan de hypotheses uit EDA
  onverwacht: <iets dat op leakage of een fout kan wijzen>
beperkingen_en_vertrouwen:
  - <concrete situatie waarin de output kritisch beoordeeld moet worden>
  - <distributie-shift / segment met weinig data / score dicht bij baseline>
openstaande_vragen:
  - <gevraagd + antwoord, of nog open>
reproduceerbaarheid:
  seed: <..>
  stack: <libraries + versies indien relevant>
```

## Minimale kwaliteitspoort vóór je oplevert

- [ ] Baseline aanwezig en het model verslaat het meetbaar.
- [ ] Validatie-opzet past bij de datastructuur (tijd/groep waar nodig).
- [ ] Testset exact één keer gebruikt.
- [ ] Preprocessing binnen de CV-fold gefit (geen CV-leakage).
- [ ] Primaire metriek bewust gekozen en tegen baseline afgezet.
- [ ] Onzekerheid + faalgevallen benoemd, niet alleen gemiddelde.
- [ ] "Wanneer niet vertrouwen" expliciet ingevuld.
