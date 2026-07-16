---
name: voorspellen-classificatie
description: Bouw voorspelmodellen voor categorische uitkomsten (ja/nee of meerdere klassen) waar per individu een correcte voorspelling telt — bijv. "voorspel of een student uitvalt", "classificeer aanvragen als goedgekeurd/afgekeurd", "predict churn yes/no". Gebruik deze skill bij elke classificatietaak. LET OP — als het doel is een lijst te sorteren op risico en de top-N te selecteren (beperkte capaciteit, uitnodigingslijst, prioritering), gebruik dan de skill voorspellen-ranking in plaats van deze.
---

# Prediction: classification

Goal: predict a class per row (dropout yes/no, category A/B/C). Evaluated on the quality of individual predictions. The user is non-technical: address them in Dutch and keep explanations in plain language.

## Workflow

When the user invokes `/voorspellen-classificatie [optional: file path or target variable]`:

## Step 0 — Check: is this actually classification?

Two checks before you start:
1. **Ranking?** For a binary target, always ask first: is this about **hard yes/no decisions per individual**, or about **sorting by risk and selecting the top-N** (e.g. who to invite under limited capacity)? In the second case: use the skill `/voorspellen-ranking`. Classic classification optimises a decision boundary at 0.5 and ignores the ordering within groups; for prioritisation lists that is the wrong optimisation.
2. **Time series?** Is this about predicting future events over time where rows are timestamps (e.g. "will there be a peak next month")? Then this is forecasting, not row-based classification — say so and use a forecasting approach. For data across multiple years (panel data): split on time (train on earlier years, test on the most recent year) instead of random.

## Step 1 — Intake (always ask first, do not assume)

Ask these in plain Dutch. Skip a question only if the answer is already in the conversation.

1. **Interpretable or black box?**
   - Interpretable = you can explain why (logistic regression, Lasso-logistic, small decision tree).
   - Black box allowed = often more accurate (Random Forest, Gradient Boosting, XGBoost, SVM). No deep learning.
2. **Automatically fine-tune settings or use default settings?** (ask this in plain language, not with terms like hyperparameters or cross-validation)
   - Default = fast, fine first version.
   - Fine-tune = the model tries many combinations of settings and picks the best. Takes longer. Technical detail: see `references/hyperparameters.md`.
3. **Benchmark multiple algorithms or one recommendation?**
   - Benchmark = train all suitable algorithms, one comparison table (the cedanl/uitnodigingsregel-benchmark approach: RF, Lasso/LogReg, SVM, Gradient Boosting, XGBoost).
   - Recommendation = assess the case yourself and recommend one algorithm with a short rationale. Weigh: number of rows (logistic regression strong with little data; boosting with lots of data), class balance, many categorical features (trees), expected non-linearity, and the interpretability requirement from question 1. Do not hardcode a fixed default.

## Step 2 — Data

If the data is not yet prepared, first follow the skill `/voorspellen-dataprep` (overview, leakage check, missings, encoding, split). Core, also if that skill is unavailable:
- Split 80/20 stratified on the target column (random_state=42) before preprocessing; everything in an sklearn Pipeline (no leakage).
- Impute missings (median/mode), one-hot with handle_unknown="ignore", StandardScaler only for logistic regression and SVM.
- Check class balance. For a skewed distribution (< ~20% minority class): report it, use class_weight="balanced" where possible and do not rely on accuracy.

## Step 3 — Algorithms

| Algorithm | Interpretable | Scaling |
|---|---|---|
| Logistic regression | yes | yes |
| Small decision tree | yes | no |
| Random Forest | no | no |
| Gradient Boosting | no | no |
| XGBoost | no | no |
| SVM (rbf, probability=True) | no | yes |

No neural networks / deep learning.

When tuning: use the grids from `references/hyperparameters.md` (scoring: "f1" or "roc_auc" for imbalance). Choose the search method yourself (it is described in that file); do not bother the user with it.

## Step 4 — Evaluation and reporting

Report on the test set: accuracy, precision, recall, F1 (per class for multiclass), confusion matrix, and ROC-AUC for a binary outcome. Give a baseline (majority class) for context.

For a benchmark: one table, sort by F1 (or AUC for imbalance), name the winner.

For interpretable models: show coefficients/odds ratios. For ensembles: feature importances, with the caveat that this is not causality.

Deliver: (1) a summary in plain Dutch, (2) reproducible code, (3) a joblib model on request.

## Important

- Goal is to sort by risk and select the top-N? Use `/voorspellen-ranking`, not this skill.
- Data not yet prepared? First `/voorspellen-dataprep`.
- Intake (Step 1) always ask first — do not assume; do not hardcode a fixed default algorithm.
- No neural networks / deep learning.
- Always split before preprocessing, everything in an sklearn Pipeline (no leakage).
- The user is non-technical: all output and questions to the user are in Dutch; explain choices in plain language, no jargon.
