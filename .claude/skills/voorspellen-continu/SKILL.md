---
name: voorspellen-continu
description: Bouw voorspelmodellen voor continue (numerieke) doelvariabelen zoals cijfers, studiepunten, aantallen of bedragen. Gebruik deze skill altijd wanneer de gebruiker een getal wil voorspellen op basis van data (regressie), ook als het woord "regressie" niet valt — bijv. "voorspel het eindcijfer", "schat het aantal EC", "predict grade/score/amount". NIET gebruiken voor ja/nee-uitkomsten (classificatie) of het rangschikken op risico (ranking).
---

# Prediction: continuous target (regression)

Goal: a model that predicts a number per row (student, customer, ...). Evaluated on the deviation between prediction and reality. The user is non-technical: address them in Dutch and keep explanations in plain language.

## Workflow

When the user invokes `/voorspellen-continu [optional: file path or target variable]`:

## Step 0 — Check: is this not time-series forecasting?

If the goal is to predict **future values over time** (enrolment next year, revenue per month, occupancy per week) and the rows are timestamps instead of individuals, then this is time-series forecasting, not row-based regression. Tell the user and do not use this skill: a random 80/20 split then leaks the future into training and the metrics become misleading. Use a forecasting approach (lag features + temporal split, or a forecasting skill if available). Edge case (panel data: individuals followed across years): row-based modelling is allowed, but split on time then (train on earlier years, test on the most recent year).

## Step 1 — Intake (always ask first, do not assume)

Ask the user these three questions before modelling. Short and in plain Dutch. Skip a question only if the answer is already in the conversation.

1. **Interpretable or black box?**
   - Interpretable = you can explain why the model predicts something (e.g. Lasso, linear regression, small decision tree, Random Forest). Needed when results must be justified to e.g. an exam board or students.
   - Black box allowed = often more accurate (e.g. Gradient Boosting, XGBoost, SVR). 
2. **Automatically fine-tune settings or use default settings?** (ask this in plain language, not with terms like hyperparameters or cross-validation)
   - Default = fast, usually fine as a first version.
   - Fine-tune = the model tries many combinations of settings and picks the best. Takes a lot longer, often slightly better scores. Technical detail: see `references/hyperparameters.md`.
3. **Benchmark multiple algorithms or one recommendation?**
   - Benchmark = train all suitable algorithms, compare in one table.
   - Recommendation = llm assess the case and recommend one algorithm with a short rationale. Weigh: number of rows (SVR slow and linear often better at < ~500 rows; boosting usually wins with lots of data), features vs rows, many categorical features (trees), expected non-linearity, and the interpretability requirement from question 1. Do not hardcode a fixed default.

## Step 2 — Data

If the data is not yet prepared, first follow the skill `/voorspellen-dataprep` (overview, leakage check, missings, encoding, split). Core, also if that skill is unavailable:
- The target column must be numeric and continuous. Binary (0/1)? Refer to `/voorspellen-classificatie` or `/voorspellen-ranking`.
- Split 80/20 (random_state=42) before all preprocessing; everything in an sklearn Pipeline (no leakage).
- Impute missings (median/mode), one-hot with handle_unknown="ignore", StandardScaler only for Lasso/linear/SVR.

## Step 3 — Algorithms

Choose from (depending on intake answer 1):

| Algorithm | Interpretable | Scaling |
|---|---|---|
| Lasso | yes | yes |
| Linear regression (Ridge/ElasticNet) | yes | yes |
| Small decision tree | yes | no |
| Random Forest Regressor | yes | no |
| Gradient Boosting Regressor | no | no |
| XGBoost Regressor | no | no |
| SVR | no | yes |


When tuning: use the grids from `references/hyperparameters.md`. Choose the search method yourself (it is described in that file); do not bother the user with it.

## Step 4 — Evaluation and reporting

Report on the test set: RMSE, MAE, R². Also give a baseline (always predict the mean) so the scores have context.

For a benchmark: one comparison table, sort by RMSE, name the winner and whether the difference is practically relevant.

For interpretable models: show coefficients (Lasso: which features drop out). For tree ensembles: feature importances, with the caveat that this is indicative, not causality.

Deliver: (1) a short summary in plain Dutch, (2) code the user can re-run, (3) a saved model (joblib) if requested.

## Important

- Only for continuous (numeric) targets. Yes/no → `/voorspellen-classificatie`; sorting by risk → `/voorspellen-ranking`.
- Time-series forecasting (rows = timestamps)? Not this skill; say so and split on time.
- Data not yet prepared? First `/voorspellen-dataprep`.
- Intake (Step 1) always ask first — do not assume; do not hardcode a fixed default algorithm.
- Always split before preprocessing, everything in an sklearn Pipeline (no leakage).
- The user is non-technical: all output and questions to the user are in Dutch; explain choices in plain language, no jargon.
