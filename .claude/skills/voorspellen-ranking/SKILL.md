---
name: voorspellen-ranking
description: Bouw risicoscore-modellen (bipartite ranking) die individuen sorteren van hoog naar laag risico, voor situaties met beperkte capaciteit waarin je de top-N selecteert — bijv. een uitnodigingsregel voor studenten met uitvalrisico, prioriteringslijsten, triage, "wie moeten we als eerste benaderen". Gebruik deze skill altijd bij woorden als uitnodigingsregel, risicoscore, risicoprioritering, top-N, ranking op uitval/churn/risico, learning to rank met binaire labels — óók als de gebruiker het "classificatie" noemt maar het doel een gesorteerde lijst is. De ranking-benadering is methodologisch onderbouwd in Eegdeman et al. (2022) en wordt in de praktijk toegepast in de uitnodigingsregel van cedanl; daar blijkt dat sorteren op risicoscore bij beperkte capaciteit betere selecties oplevert dan classificatie met een vaste beslisgrens.
---

# Prediction: bipartite ranking (risk score / uitnodigingsregel)

Goal: no hard yes/no labels, but a **score per individual** to sort from high to low risk. The model is good when the true positives (e.g. dropouts) are at the top — not when every individual prediction is "right" or "wrong". Evaluated on ranking quality (AUC, precision@k), not on accuracy. Classic classification optimises a decision boundary at 0.5 and ignores the ordering within groups; for a list with limited capacity (invite the top-N) you specifically want that ordering right. Based on cedanl/Uitnodigingsregel (Eegdeman et al., 2022). Related terms: learning to rank, AUC optimization. The user is non-technical: address them in Dutch and keep explanations in plain language.

## Workflow

When the user invokes `/voorspellen-ranking [optional: file path or target variable]`:

## Step 0 — Check: is this not time-series forecasting?

If the question is how a count or percentage develops **over time** (e.g. "how much dropout do we expect next year"), that is forecasting, not ranking of individuals — say so and do not use this skill. This skill is for: sorting individuals by risk now.

## Step 1 — Intake (always ask first, do not assume)

1. **What is the capacity (N or k)?** How many people can be invited/handled? Needed for precision@k. Unknown: report at multiple k's (e.g. 5%, 10%, 20% of the population).
2. **Interpretable or black box?**
   - Interpretable = explainable why someone scores high (e.g. Lasso, logistic regression, Random Forest). Often required for decisions about students.
   - Black box allowed = often better ranking (e.g. Gradient Boosting, XGBoost, SVM). 
3. **Automatically fine-tune settings or use default settings?** (ask this in plain language, not with terms like hyperparameters, AUC or grids)
   - Default = fast, fine first version.
   - Fine-tune = the model tries many combinations of settings and picks the best. Takes a lot longer.
   - Internal, do not put to the user: tune on scoring="roc_auc" (ranking, not accuracy); use the local grids from `references/hyperparameters.md` by default; only if the user themselves mentions the CEDA benchmark or comparability between settings, the CEDA grids.
4. **Test and compare multiple models, or follow one recommendation?** (ask in plain language)
   - Compare = the cedanl/uitnodigingsregel-benchmark approach: Random Forest, Lasso, SVM, Gradient Boosting, XGBoost side by side, one table.
   - Recommendation = llm assess the case and recommend one algorithm with a short rationale. Weigh: number of rows and features, prevalence of the positive class, expected non-linearity, and the interpretability requirement from question 2. Do not hardcode a fixed default. cedanl benchmark results may serve as context, not as an automatic answer.

## Step 2 — Data

- Binary target column (e.g. `Dropout` 0/1). Continuous target → skill `/voorspellen-continu`.
- If the data is not yet prepared, first follow the skill `/voorspellen-dataprep` (overview, leakage check, missings, encoding, split).
- Split 80/20 stratified (random_state=42) before preprocessing; everything in a Pipeline (no leakage). If years are available: prefer training on earlier years and testing on the most recent year (like config.yaml in the benchmark: training_years vs dropout_year) — this resembles real use.
- Impute missings (median/mode), one-hot with handle_unknown="ignore", StandardScaler only for Lasso, logistic regression and SVM.
- Class imbalance is normal here and not a problem: ranking uses the whole score distribution; do not oversample unless explicitly requested.

## Step 3 — Producing the score

Two common routes (cedanl/Uitnodigingsregel uses both):
- **Classifier with `predict_proba`**: use the probability of the positive class as the score (LogReg, RF classifier, GB, XGBoost, SVC with probability=True).
- **Regressor on the 0/1 label**: e.g. Lasso or RandomForestRegressor on the Dropout column; the continuous prediction is the score.

**Never** use `predict()` with the 0.5 threshold as the final result. The output is always: score → sort descending → rank.

When tuning: **scoring="roc_auc"** (for the regressor route: a custom AUC scorer on the scores). Search method per `references/hyperparameters.md`; do not ask the user.

## Step 4 — Evaluation and reporting

Evaluate on the test set purely on ranking quality:
- **AUC (ROC-AUC)**: probability that a random positive ranks above a random negative. 0.5 = random.
- **Precision@k**: of the top-k on the list, what share is truly positive.
- **Recall@k**: what share of all positives is in the top-k.
- **Precision/recall curve across all thresholds** (like compute_dynamic_evaluation in cedanl/Uitnodigingsregel): cumulative per rank, from highest score to lowest.
- Baseline: random ranking (precision@k = prevalence).

Do not report accuracy and do not report a confusion matrix at threshold 0.5; briefly explain why if the user asks.

For a benchmark: one table with AUC and precision@k per algorithm, sort by AUC, name the winner and whether the difference matters at the relevant k.

Deliver: (1) a sorted list with scores and rank (top-N marked), (2) a summary in plain Dutch, (3) reproducible code, (4) a joblib model on request. For decisions about people, state that the list is a prioritisation aid, not a judgement per individual.

## Important

- For top-N selection under limited capacity; hard yes/no per individual → `/voorspellen-classificatie`, continuous outcome → `/voorspellen-continu`.
- Data not yet prepared? First `/voorspellen-dataprep`.
- **Never** use `predict()` with the 0.5 threshold as the final result; output is always score → sort → rank.
- Do not report accuracy or a confusion matrix; evaluate on ranking (AUC, precision@k).
- Intake (Step 1) always ask first — do not assume; do not hardcode a fixed default algorithm.
- For decisions about people: the list is a prioritisation aid, not a judgement per individual.
- The user is non-technical: all output and questions to the user are in Dutch; explain choices in plain language, no jargon.
