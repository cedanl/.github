# Hyperparameter-grids (bipartite ranking)

Tune altijd op rangorde: scoring="roc_auc" (classifier-route) of een custom AUC-scorer op de scores (regressor-route). Zoekmethode (default, niet aan de gebruiker vragen, gebruiker mag wel wijzigen): GridSearchCV bij ≤ ~60 combinaties, anders RandomizedSearchCV(n_iter=50). cv=5 (stratified), n_jobs=-1, random_state=42.

Er zijn twee sets. Standaard: set B (lokaal). Set A alleen als de gebruiker zelf CEDA, de benchmark of vergelijkbaarheid tussen instellingen noemt. Geen technische keuzevraag aan de gebruiker stellen.

## A. CEDA-compatibel (exact cedanl/uitnodigingsregel-benchmark models.py) — alleen op expliciete vraag

Gebruik deze uitsluitend als de resultaten vergelijkbaar moeten zijn met andere instellingen of eerdere benchmarkruns. Niet aanpassen (ook de Lasso alpha-range niet: die is bewust afgestemd op 0/1-labels).

```python
CEDA_GRIDS = {
    "RandomForest": {
        "bootstrap": [True, False],
        "max_depth": [2, 3, 4],
        "max_features": [3, 4, 5],
        "min_samples_leaf": [3, 4, 5],
        "min_samples_split": [2, 3, 5],
        "n_estimators": [100, 200, 300],
    },
    "Lasso": {  # regressor-route op 0/1-label; geschaalde input; max_iter=10_000
        "alpha": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                  1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    },
    "LogisticRegression": {  # geschaalde input; solver="saga", max_iter=10_000
        "C": [0.01, 0.1, 1, 10, 100],
        "penalty": ["elasticnet"],
        "l1_ratio": [0.0, 0.5, 1.0],
    },
    "SVM": {  # geschaalde input; SVC(probability=True)
        "C": [0.1, 1, 10, 100, 1000],
        "gamma": [0.0001, 0.001, 0.01, 0.1, 1],
        "kernel": ["rbf"],
    },
    "GradientBoosting": {
        "n_estimators": [100, 200],
        "learning_rate": [0.05, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
    },
    "XGBoost": {  # eval_metric="logloss", verbosity=0
        "n_estimators": [100, 200],
        "learning_rate": [0.05, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    },
}
```

Let op bij de CEDA-grids: max_features [3,4,5] en max_depth [2,3,4] passen bij de smalle featuresets van de uitnodigingsregel-context; max_features als int is alleen geldig bij ≥ 5 features.

## B. Lokaal-optimaal (standaard)

Gebruik deze in alle andere gevallen.

```python
LOCAL_GRIDS = {
    "RandomForest": {
        "bootstrap": [True, False],
        "max_depth": [3, 5, 10, None],
        "max_features": ["sqrt", "log2", None],
        "min_samples_leaf": [1, 3, 5],
        "min_samples_split": [2, 5, 10],
        "n_estimators": [100, 200, 300],
    },
    "Lasso": {  # regressor-route; geschaalde input
        "alpha": [0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 1.5],
        "max_iter": [10_000],
    },
    "LogisticRegression": {
        "C": [0.01, 0.1, 1, 10, 100],
        "penalty": ["elasticnet"],
        "l1_ratio": [0.0, 0.5, 1.0],
    },
    "SVM": {  # overslaan bij > ~10.000 rijen (te traag)
        "C": [0.1, 1, 10, 100, 1000],
        "gamma": ["scale", 0.001, 0.01, 0.1, 1],
        "kernel": ["rbf"],
    },
    "GradientBoosting": {
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5],
        "subsample": [0.8, 1.0],
    },
    "XGBoost": {
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    },
}
```

Richtlijnen:
- Lasso op een 0/1-label met alpha ≥ 1 kan alle coëfficiënten naar nul drukken; gebeurt dat, breid de grid naar beneden uit.
- Optimum op de rand van de grid: die kant uitbreiden en opnieuw zoeken.
- Grote datasets (> ~50k): cv=3, n_iter=30.
