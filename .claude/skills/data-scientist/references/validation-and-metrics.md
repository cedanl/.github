# Validatie, metrieken & leakage-in-modellering

De vangrails die snelle iteratie betrouwbaar houden. Doorloop dit bij Stap 0
(opzet kiezen), Stap 3 (trainen) en Stap 4 (evalueren).

## Validatie-opzet kiezen (vóór je traint)

- **Random split / K-fold** — alleen als rijen onafhankelijk zijn (geen tijd,
  geen herhaalde entiteiten).
- **Gestratificeerd** — classificatie met onbalans; behoud klasseverhouding per
  fold.
- **Tijd-gebaseerd (forward chaining)** — verplicht bij tijdreeks/forecast: train
  op verleden, valideer op toekomst. Nooit random shufflen over tijd.
- **Groep-gebaseerd (GroupKFold)** — herhaalde metingen per entiteit (bv. per
  student/instelling): houd een entiteit volledig in train óf test, nooit beide,
  anders lekt informatie.
- **Test-set apart** — houd een finale testset opzij, raak die één keer aan aan
  het einde. Elke extra blik erop is test-leakage en maakt de score optimistisch.

## Leakage-in-modellering (naast de data-cleaner-checks)

- **CV-leakage:** fit imputers/encoders/scalers/feature-selectie **binnen** elke
  fold, op alleen de train-helft. Fitten op de hele set vóór CV lekt.
- **Target-leakage:** feature (deels) afgeleid van de target of pas ná het
  voorspelmoment bekend → weg.
- **Tuning-leakage:** hyperparameters afstellen op de testset. Gebruik daarvoor
  validatie/CV, niet de test.
- **Rode vlag:** score veel hoger dan plausibel, of één feature domineert
  onverwacht → stop en audit de herkomst vóór je verder itereert.

## Metriek kiezen (één primaire, bewust)

Regressie:
- **MAE** — robuust, zelfde eenheid als target, minder gevoelig voor uitschieters.
- **RMSE** — straft grote fouten zwaarder; kies als grote missers duur zijn.
- **MAPE** — relatieve fout; misleidend bij waarden dicht bij 0.

Classificatie:
- **Accuracy** — alleen bij gebalanceerde klassen; misleidend bij onbalans.
- **Precision/Recall/F1** — bij onbalans of asymmetrische kosten; kies bewust
  precision vs recall op basis van welke fout duurder is.
- **ROC-AUC / PR-AUC** — rangschikkende kwaliteit; PR-AUC beter bij sterke
  onbalans.

Vergelijk de primaire metriek **altijd tegen de baseline**. Een absoluut getal
zegt niets zonder referentiepunt.

## Onzekerheid & robuustheid

- Rapporteer spreiding over CV-folds (gemiddelde ± std), niet één getal.
- Kijk naar residuen / fouten per segment: waar faalt het model systematisch?
- Test gevoeligheid: houdt de conclusie stand bij een andere split/seed?
- Benoem distributie-shift-risico: is de test representatief voor productie?

## Wanneer het model niet te vertrouwen

- Score nauwelijks boven baseline → complexiteit voegt niets toe.
- Grote train↔val-kloof → overfitting.
- Segment met te weinig data → onbetrouwbaar daar.
- Verdachte top-feature → mogelijke leakage.
- Testset niet representatief voor de inzet-populatie.
