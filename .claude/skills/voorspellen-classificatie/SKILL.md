---
name: voorspellen-classificatie
description: Bouw voorspelmodellen voor categorische uitkomsten (ja/nee of meerdere klassen) waar per individu een correcte voorspelling telt — bijv. "voorspel of een student uitvalt", "classificeer aanvragen als goedgekeurd/afgekeurd", "predict churn yes/no". Gebruik deze skill bij elke classificatietaak. LET OP — als het doel is een lijst te sorteren op risico en de top-N te selecteren (beperkte capaciteit, uitnodigingslijst, prioritering), gebruik dan de skill voorspellen-ranking in plaats van deze.
---

# Voorspellen: classificatie

Doel: per rij een klasse voorspellen (uitval ja/nee, categorie A/B/C). Evaluatie op de kwaliteit van individuele voorspellingen.

## Workflow

When the user invokes `/voorspellen-classificatie [optioneel: bestandspad of doelvariabele]`:

## Stap 0 — Check: is dit wel classificatie?

Twee checks voordat je begint:
1. **Ranking?** Vraag bij een binaire doelvariabele altijd eerst: gaat het om **harde ja/nee-beslissingen per individu**, of om **sorteren op risico en de top-N selecteren** (bijv. wie nodig je uit bij beperkte capaciteit)? In het tweede geval: gebruik de skill `/voorspellen-ranking`. Klassieke classificatie optimaliseert een beslisgrens bij 0,5 en negeert de volgorde binnen groepen; voor prioriteringslijsten is dat de verkeerde optimalisatie.
2. **Tijdreeks?** Gaat het om het voorspellen van toekomstige gebeurtenissen over de tijd waarbij rijen tijdstippen zijn (bijv. "wordt volgende maand een piek")? Dan is dit forecasting, geen rij-gebaseerde classificatie — meld dat en gebruik een forecasting-aanpak. Bij data over meerdere jaren (paneldata): splits op tijd (train op eerdere jaren, test op het laatste jaar) in plaats van random.

## Stap 1 — Intake (altijd eerst vragen, niet zelf aannemen)

1. **Interpreteerbaar of black box?**
   - Interpreteerbaar = uitlegbaar waarom (Logistische regressie, Lasso-logistiek, kleine beslisboom).
   - Black box mag = vaak nauwkeuriger (Random Forest, Gradient Boosting, XGBoost, SVM). Geen deep learning.
2. **Instellingen automatisch fijnslijpen of standaardinstellingen?** (vraag het in deze gewone taal, niet met termen als hyperparameters of cross-validatie)
   - Standaard = snel, prima eerste versie.
   - Fijnslijpen = het model probeert veel combinaties van instellingen uit en kiest de beste. Duurt langer. Technisch: zie `references/hyperparameters.md`.
3. **Meerdere algoritmes benchmarken of één aanbeveling?**
   - Benchmark = train alle passende algoritmes, één vergelijkingstabel (aanpak van cedanl/uitnodigingsregel-benchmark: RF, Lasso/LogReg, SVM, Gradient Boosting, XGBoost).
   - Aanbeveling = beoordeel zelf de case en beveel één algoritme aan met korte motivering. Weeg mee: aantal rijen (logistische regressie sterk bij weinig data; boosting bij veel data), klassenbalans, veel categorische features (bomen), verwachte niet-lineariteit, en de interpretatie-eis uit vraag 1. Geen vaste default hardcoden.

## Stap 2 — Data

Is de data nog niet voorbereid, volg dan eerst de skill `/voorspellen-dataprep` (overzicht, leakage-check, missings, encoding, split). Kern, ook als die skill niet beschikbaar is:
- Splits 80/20 stratified op de doelkolom (random_state=42) vóór preprocessing; alles in een sklearn Pipeline (geen leakage).
- Missings imputeren (mediaan/modus), one-hot met handle_unknown="ignore", StandardScaler alleen voor logistische regressie en SVM.
- Check klassenbalans. Bij scheve verdeling (< ~20% minderheidsklasse): rapporteer dit, gebruik class_weight="balanced" waar mogelijk en leun niet op accuracy.

## Stap 3 — Algoritmes

| Algoritme | Interpreteerbaar | Scaling |
|---|---|---|
| Logistische regressie | ja | ja |
| Kleine beslisboom | ja | nee |
| Random Forest | nee | nee |
| Gradient Boosting | nee | nee |
| XGBoost | nee | nee |
| SVM (rbf, probability=True) | nee | ja |

Geen neurale netwerken / deep learning.

Bij tunen: gebruik de grids uit `references/hyperparameters.md` (scoring: "f1" of "roc_auc" bij onbalans). De zoekmethode kies je zelf (staat in dat bestand); val de gebruiker er niet mee lastig.

## Stap 4 — Evaluatie en rapportage

Rapporteer op de testset: accuracy, precision, recall, F1 (per klasse bij multiclass), confusion matrix, en ROC-AUC bij binaire uitkomst. Geef een baseline (meerderheidsklasse) ter context.

Bij benchmark: één tabel, sorteer op F1 (of AUC bij onbalans), benoem de winnaar.

Bij interpreteerbare modellen: coëfficiënten/odds-ratio's tonen. Bij ensembles: feature importances, met kanttekening dat dit geen causaliteit is.

Lever op: (1) samenvatting in gewone taal, (2) herdraaibare code, (3) joblib-model op verzoek.

## Important

- Doel is sorteren op risico en top-N selecteren? Gebruik `/voorspellen-ranking`, niet deze skill.
- Data nog niet voorbereid? Eerst `/voorspellen-dataprep`.
- Intake (Stap 1) altijd eerst vragen — niet zelf aannemen; geen vast default-algoritme hardcoden.
- Geen neurale netwerken / deep learning.
- Splits altijd vóór preprocessing, alles in een sklearn Pipeline (geen leakage).
- De gebruiker is niet technisch: leg keuzes uit in gewone taal, zonder jargon.
