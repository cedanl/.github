---
name: voorspellen-dataprep
description: Bereid een dataset voor op voorspelmodellen (regressie, classificatie of risicoranking). Gebruik deze skill altijd als eerste stap wanneer de gebruiker data wil klaarmaken, opschonen of controleren voor een voorspelling — bijv. "maak mijn CSV klaar voor het model", "check of deze data bruikbaar is", "voorspel X op basis van dit bestand" — en ook wanneer een van de skills voorspellen-continu, voorspellen-classificatie of voorspellen-ranking wordt gebruikt en de data nog niet is voorbereid.
---

# Datapreparatie voor voorspelmodellen

Doel: van ruwe data naar een schone train/test-opzet waarmee de skills `/voorspellen-continu`, `/voorspellen-classificatie` en `/voorspellen-ranking` direct verder kunnen. Alles gebeurt in een sklearn Pipeline/ColumnTransformer zodat er geen leakage is en de stappen herdraaibaar zijn. De gebruiker is niet technisch: leg elke keuze in één zin gewone taal uit en vraag alleen wat echt nodig is.

## Workflow

When the user invokes `/voorspellen-dataprep [optioneel: bestandspad]`:

## Stap 1 — Inlezen en overzicht

- Lees het bestand in en toon: aantal rijen, aantal kolommen, per kolom het type en het percentage missende waarden.
- Bevestig met de gebruiker welke kolom de doelvariabele is (wat voorspeld moet worden) als dat niet al duidelijk is.

## Stap 2 — Routekeuze

Bepaal het doeltype en benoem de vervolgskill:
- Continu getal → `/voorspellen-continu`
- Categorie, harde ja/nee-beslissing per individu → `/voorspellen-classificatie`
- Binair label, maar het doel is sorteren op risico en top-N selecteren → `/voorspellen-ranking`
- Rijen zijn tijdstippen en het doel is de toekomst over de tijd voorspellen → tijdreeks-forecasting; meld dat deze skills daar niet voor zijn.

## Stap 3 — Opschonen

- Verwijder rijen waar de doelvariabele zelf ontbreekt (die zijn onbruikbaar voor trainen; meld hoeveel).
- Verwijder exacte duplicaatrijen (meld hoeveel).
- Verwijder ID-achtige kolommen (uniek per rij: studentnummer, e-mail) en constante kolommen. Benoem welke.
- Fix datatypes (getallen die als tekst staan, datums parsen).

## Stap 4 — Leakage-check (belangrijkste stap)

Loop de kolommen langs op informatie die de uitkomst verraadt of pas ná het voorspelmoment ontstaat (bijv. "uitschrijfdatum" bij het voorspellen van uitval, eindcijfer bij het voorspellen van slagen). Leg de gebruiker in gewone taal voor welke kolommen verdacht zijn en vraag bevestiging om ze te verwijderen. Dit kan niet volledig automatisch: de gebruiker weet wat wanneer bekend is.

## Stap 5 — Missende waarden

- Kolommen met > 50% missend: voorstellen te verwijderen (met de gebruiker afstemmen).
- Overige: SimpleImputer in de pipeline — mediaan voor numeriek, meest voorkomende waarde of aparte categorie "onbekend" voor categorisch. Meld wat je deed.

## Stap 6 — Categorische kolommen

- One-hot encoding met handle_unknown="ignore".
- Hoge cardinaliteit (> ~20 categorieën): groepeer zeldzame categorieën (< ~1% van de rijen) samen tot "overig" vóór het encoden.

## Stap 7 — Train/test-split

Altijd vóór het fitten van imputer/encoder/scaler:
- Standaard: 80/20, random_state=42; stratified op de doelkolom bij classificatie en ranking.
- Data over meerdere jaren/cohorten: splits op tijd (train op eerdere jaren, test op het laatste jaar) — dat lijkt op echt gebruik.

## Stap 8 — Scaling

StandardScaler in de pipeline, alleen toegepast voor lineaire modellen en SVM (de vervolgskill bepaalt dit). Boommodellen hebben het niet nodig.

## Stap 9 — Oplevering

- Een ColumnTransformer/Pipeline die alle bovenstaande stappen bevat, plus X_train, X_test, y_train, y_test.
- Kort rapport in gewone taal: wat is verwijderd, wat is geïmputeerd, hoe is gesplitst, klassenbalans (bij binaire doelen), en eventuele zorgen (weinig rijen, scheve verdeling, verdachte kolommen).
- Ga daarna door met de passende voorspel-skill uit Stap 2.

## Important

- Altijd eerste stap vóór `/voorspellen-continu`, `/voorspellen-classificatie` of `/voorspellen-ranking` als de data nog niet is voorbereid.
- Splits altijd vóór het fitten van imputer/encoder/scaler — anders lekt testinformatie in de training.
- De leakage-check (Stap 4) is de belangrijkste stap en kan niet volledig automatisch: vraag de gebruiker altijd om bevestiging voor je kolommen verwijdert.
- De gebruiker is niet technisch: leg elke keuze in één zin gewone taal uit; geen jargon zonder uitleg.
- Alleen cedanl-gebruik: rij-gebaseerde voorspelling, geen tijdreeks-forecasting.
