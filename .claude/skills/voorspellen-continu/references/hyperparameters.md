# Hyperparameter-grids (regressie)

Werkbare zoekruimtes voor algemene regressie. Zoekmethode (interne keuze, nooit aan de gebruiker vragen): GridSearchCV als de grid ≤ ~60 combinaties telt, anders RandomizedSearchCV(n_iter=50). Altijd cv=5, n_jobs=-1, random_state=42, scoring="neg_root_mean_squared_error".

```python
PARAM_GRIDS = {
    "Lasso": {  # geschaalde input; let op: passende alpha hangt af van de schaal van y
        "alpha": [0.0001, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0],
        "max_iter": [10_000],
    },
    "Ridge": {  # geschaalde input
        "alpha": [0.01, 0.1, 1, 10, 100],
    },
    "ElasticNet": {  # geschaalde input
        "alpha": [0.001, 0.01, 0.1, 0.5, 1.0],
        "l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9],
        "max_iter": [10_000],
    },
    "DecisionTree": {
        "max_depth": [2, 3, 4, 6],
        "min_samples_leaf": [3, 5, 10],
        "min_samples_split": [2, 5, 10],
    },
    "RandomForest": {
        "bootstrap": [True, False],
        "max_depth": [3, 5, 10, None],
        "max_features": ["sqrt", "log2", None],
        "min_samples_leaf": [1, 3, 5],
        "min_samples_split": [2, 5, 10],
        "n_estimators": [100, 200, 300],
    },
    "GradientBoosting": {
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5],
        "subsample": [0.8, 1.0],
        "min_samples_leaf": [1, 5, 10],
    },
    "XGBoost": {  # optioneel; sla over als xgboost niet installeerbaar is
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
        "min_child_weight": [1, 5],
    },
    "SVR": {  # geschaalde input; overslaan bij > ~10.000 rijen (te traag), tenzij de gebruiker erom vraagt
        "C": [0.1, 1, 10, 100, 1000],
        "gamma": ["scale", 0.001, 0.01, 0.1, 1],
        "kernel": ["rbf"],
        "epsilon": [0.01, 0.1, 0.5],
    },
}
```

Richtlijnen:
- Deze grids zijn vertrekpunten, geen wet. Ligt het optimum op de rand van de grid, breid die kant uit en zoek opnieuw.
- Kleine datasets (< ~1000 rijen): houd bomen ondiep (max_depth ≤ 4) en regularisatie hoog; grote datasets (> ~50k): cv=3 en n_iter=30 om rekentijd te beperken.
- Ondiepe bomen (max_depth 2–4) passen bij weinig features en weinig rijen (zoals de uitnodigingsregel-context); bij bredere datasets is dat te restrictief — vandaar de ruimere waardes hierboven.
