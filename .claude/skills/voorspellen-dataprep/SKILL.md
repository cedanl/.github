---
name: voorspellen-dataprep
description: Bereid een dataset voor op voorspelmodellen (regressie, classificatie of risicoranking). Gebruik deze skill altijd als eerste stap wanneer de gebruiker data wil klaarmaken, opschonen of controleren voor een voorspelling — bijv. "maak mijn CSV klaar voor het model", "check of deze data bruikbaar is", "voorspel X op basis van dit bestand" — en ook wanneer een van de skills voorspellen-continu, voorspellen-classificatie of voorspellen-ranking wordt gebruikt en de data nog niet is voorbereid.
---

# Data preparation for prediction models

Goal: go from raw data to a clean train/test setup that the skills `/voorspellen-continu`, `/voorspellen-classificatie` and `/voorspellen-ranking` can continue with directly. Everything happens inside an sklearn Pipeline/ColumnTransformer so there is no leakage and the steps are reproducible. The user is non-technical: address them in Dutch, explain each choice in one plain-language sentence, and ask only what is genuinely needed.

## Workflow

When the user invokes `/voorspellen-dataprep [optional: file path]`:

## Step 1 — Load and overview

- Read the file and show: number of rows, number of columns, per column the type and the percentage of missing values.
- Confirm with the user which column is the target variable (what must be predicted) if that is not already clear.

## Step 2 — Route choice

Determine the target type and name the follow-up skill:
- Continuous number → `/voorspellen-continu`
- Category, hard yes/no decision per individual → `/voorspellen-classificatie`
- Binary label, but the goal is to sort by risk and select the top-N → `/voorspellen-ranking`
- Rows are timestamps and the goal is to predict the future over time → time-series forecasting; state that these skills are not for that.

## Step 3 — Cleaning

- Remove rows where the target variable itself is missing (unusable for training; report how many).
- Remove exact duplicate rows (report how many).
- Remove ID-like columns (unique per row: student number, email) and constant columns. Name which ones.
- Fix data types (numbers stored as text, parse dates).

## Step 4 — Leakage check (most important step)

Go through the columns for information that gives away the outcome or only comes into existence after the prediction moment (e.g. "de-registration date" when predicting dropout, final grade when predicting passing). Explain to the user in plain language which columns are suspect and ask for confirmation before removing them. This cannot be fully automated: the user knows what is known when.

## Step 5 — Missing values

- Columns with > 50% missing: propose removing them (confirm with the user).
- Others: SimpleImputer in the pipeline — median for numeric, most frequent value or a separate "onbekend" (unknown) category for categorical. Report what you did.

## Step 6 — Categorical columns

- One-hot encoding with handle_unknown="ignore".
- High cardinality (> ~20 categories): group rare categories (< ~1% of the rows) together into "overig" (other) before encoding.

## Step 7 — Train/test split

Always before fitting the imputer/encoder/scaler:
- Default: 80/20, random_state=42; stratified on the target column for classification and ranking.
- Data across multiple years/cohorts: split on time (train on earlier years, test on the most recent year) — this resembles real use.

## Step 8 — Scaling

StandardScaler in the pipeline, applied only for linear models and SVM (the follow-up skill decides this). Tree models do not need it.

## Step 9 — Delivery

- A ColumnTransformer/Pipeline containing all of the above steps, plus X_train, X_test, y_train, y_test.
- A short report in plain Dutch: what was removed, what was imputed, how it was split, class balance (for binary targets), and any concerns (few rows, skewed distribution, suspect columns).
- Then continue with the appropriate prediction skill from Step 2.

## Important

- Always the first step before `/voorspellen-continu`, `/voorspellen-classificatie` or `/voorspellen-ranking` when the data is not yet prepared.
- Always split before fitting the imputer/encoder/scaler — otherwise test information leaks into training.
- The leakage check (Step 4) is the most important step and cannot be fully automated: always ask the user for confirmation before removing columns.
- The user is non-technical: all output and questions to the user are in Dutch; explain each choice in one plain-language sentence, no jargon without explanation.
