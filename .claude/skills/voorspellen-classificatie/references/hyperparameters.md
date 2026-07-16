# Hyperparameter-grids (classificatie)

Werkbare zoekruimtes voor algemene classificatie. Zoekmethode (interne keuze, nooit aan de gebruiker vragen): GridSearchCV als de grid ≤ ~60 combinaties telt, anders RandomizedSearchCV(n_iter=50). Altijd cv=5 (StratifiedKFold), n_jobs=-1, random_state=42; scoring="f1" of "roc_auc" bij onbalans, anders "accuracy" of "f1_macro" (multiclass).

```python
PARAM_GRIDS = {
    "LogisticRegression": {  # geschaalde input; solver="saga", max_iter=10_000
        "C": [0.01, 0.1, 1, 10, 100],
        "penalty": ["elasticnet"],
        "l1_ratio": [0.0, 0.5, 1.0],
        "class_weight": [None, "balanced"],
    },
    "DecisionTree": {
        "max_depth": [2, 3, 4, 6],
        "min_samples_leaf": [3, 5, 10],
        "min_samples_split": [2, 5, 10],
        "class_weight": [None, "balanced"],
    },
    "RandomForest": {
        "bootstrap": [True, False],
        "max_depth": [3, 5, 10, None],
        "max_features": ["sqrt", "log2", None],
        "min_samples_leaf": [1, 3, 5],
        "min_samples_split": [2, 5, 10],
        "n_estimators": [100, 200, 300],
        "class_weight": [None, "balanced"],
    },
    "GradientBoosting": {
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5],
        "subsample": [0.8, 1.0],
    },
    "XGBoost": {  # eval_metric="logloss", verbosity=0; optioneel, sla over als niet installeerbaar
        "n_estimators": [100, 200, 400],
        "learning_rate": [0.02, 0.05, 0.1, 0.2],
        "max_depth": [2, 3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
        # bij onbalans: "scale_pos_weight": [1, n_neg/n_pos]
    },
    "SVM": {  # geschaalde input; SVC(probability=True); overslaan bij > ~10.000 rijen (te traag)
        "C": [0.1, 1, 10, 100, 1000],
        "gamma": ["scale", 0.001, 0.01, 0.1, 1],
        "kernel": ["rbf"],
        "class_weight": [None, "balanced"],
    },
}
```

Richtlijnen:
- Grids zijn vertrekpunten. Optimum op de rand: grid die kant uitbreiden en opnieuw zoeken.
- Kleine datasets (< ~1000 rijen): ondiepe bomen (max_depth ≤ 4). Grote datasets (> ~50k): cv=3, n_iter=30.
- Wil je resultaten vergelijkbaar met cedanl/uitnodigingsregel-benchmark, gebruik dan exact de grids uit models.py van die repo (o.a. RF max_depth [2,3,4], max_features [3,4,5]).
