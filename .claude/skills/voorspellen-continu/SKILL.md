---
name: voorspellen-continu
description: Bouw voorspelmodellen voor continue (numerieke) doelvariabelen zoals cijfers, studiepunten, aantallen of bedragen. Gebruik deze skill altijd wanneer de gebruiker een getal wil voorspellen op basis van data (regressie), ook als het woord "regressie" niet valt — bijv. "voorspel het eindcijfer", "schat het aantal EC", "predict grade/score/amount". NIET gebruiken voor ja/nee-uitkomsten (classificatie) of het rangschikken op risico (ranking).
---

# Voorspellen: continue doelvariabele (regressie)

Doel: een model dat een getal voorspelt per rij (student, klant, ...). Evaluatie op afwijking tussen voorspelling en werkelijkheid.

## Workflow

When the user invokes `/voorspellen-continu [optioneel: bestandspad of doelvariabele]`:

## Stap 0 — Check: is dit geen tijdreeks-forecasting?

Als het doel is **toekomstige waarden over de tijd** te voorspellen (instroom volgend jaar, omzet per maand, bezetting per week) en de rijen zijn tijdstippen in plaats van individuen, dan is dit tijdreeks-forecasting, geen rij-gebaseerde regressie. Meld dat aan de gebruiker en gebruik deze skill dan niet: een random 80/20-split lekt dan toekomst in de training en de metrics worden misleidend. Gebruik een forecasting-aanpak (lag-features + temporele split, of een forecasting-skill als die beschikbaar is). Twijfelgeval (paneldata: individuen gevolgd over jaren): rij-gebaseerd modelleren mag, maar splits dan op tijd (train op eerdere jaren, test op het laatste jaar).

## Stap 1 — Intake (altijd eerst vragen, niet zelf aannemen)

Stel deze drie vragen aan de gebruiker voordat je gaat modelleren. Kort en in gewone taal. Sla vragen alleen over als het antwoord al in het gesprek staat.

1. **Interpreteerbaar of black box?**
   - Interpreteerbaar = je kunt uitleggen waarom het model iets voorspelt (Lasso, lineaire regressie, kleine beslisboom). Nodig als resultaten verantwoord moeten worden aan bijv. examencommissie of studenten.
   - Black box mag = vaak nauwkeuriger (Random Forest, Gradient Boosting, XGBoost, SVR). Geen deep learning.
2. **Instellingen automatisch fijnslijpen of standaardinstellingen?** (vraag het in deze gewone taal, niet met termen als hyperparameters of cross-validatie)
   - Standaard = snel, meestal prima als eerste versie.
   - Fijnslijpen = het model probeert veel combinaties van instellingen uit en kiest de beste. Duurt langer, vaak iets betere scores. Technisch: zie `references/hyperparameters.md`.
3. **Meerdere algoritmes benchmarken of één aanbeveling?**
   - Benchmark = train alle passende algoritmes, vergelijk in één tabel.
   - Aanbeveling = beoordeel zelf de case en beveel één algoritme aan met korte motivering. Weeg mee: aantal rijen (SVR traag en linear vaak beter bij < ~500 rijen; boosting wint meestal bij veel data), aantal features vs rijen, veel categorische features (bomen), verwachte niet-lineariteit, en de interpretatie-eis uit vraag 1. Geen vaste default hardcoden.

## Stap 2 — Data

Is de data nog niet voorbereid, volg dan eerst de skill `/voorspellen-dataprep` (overzicht, leakage-check, missings, encoding, split). Kern, ook als die skill niet beschikbaar is:
- Doelkolom moet numeriek en continu zijn. Binair (0/1)? Verwijs naar `/voorspellen-classificatie` of `/voorspellen-ranking`.
- Splits 80/20 (random_state=42) vóór alle preprocessing; alles in een sklearn Pipeline (geen leakage).
- Missings imputeren (mediaan/modus), one-hot met handle_unknown="ignore", StandardScaler alleen voor Lasso/lineair/SVR.

## Stap 3 — Algoritmes

Kies uit (afhankelijk van intake-antwoord 1):

| Algoritme | Interpreteerbaar | Scaling |
|---|---|---|
| Lasso | ja | ja |
| Lineaire regressie (Ridge/ElasticNet) | ja | ja |
| Kleine beslisboom | ja | nee |
| Random Forest Regressor | nee | nee |
| Gradient Boosting Regressor | nee | nee |
| XGBoost Regressor | nee | nee |
| SVR | nee | ja |

Geen neurale netwerken / deep learning gebruiken.

Bij tunen: gebruik de grids uit `references/hyperparameters.md`. De zoekmethode kies je zelf (staat in dat bestand); val de gebruiker er niet mee lastig.

## Stap 4 — Evaluatie en rapportage

Rapporteer op de testset: RMSE, MAE, R². Geef ook een baseline (voorspel altijd het gemiddelde) zodat de scores context hebben.

Bij benchmark: één vergelijkingstabel, sorteer op RMSE, benoem de winnaar en of het verschil praktisch relevant is.

Bij interpreteerbare modellen: toon coëfficiënten (Lasso: welke features vallen weg). Bij boom-ensembles: feature importances, met de kanttekening dat dit richtinggevend is, geen causaliteit.

Lever op: (1) korte samenvatting in gewone taal, (2) code die de gebruiker kan herdraaien, (3) opgeslagen model (joblib) als daarom gevraagd wordt.

## Important

- Alleen voor continue (numerieke) doelvariabelen. Ja/nee → `/voorspellen-classificatie`; sorteren op risico → `/voorspellen-ranking`.
- Tijdreeks-forecasting (rijen = tijdstippen)? Niet deze skill; meld het en splits op tijd.
- Data nog niet voorbereid? Eerst `/voorspellen-dataprep`.
- Intake (Stap 1) altijd eerst vragen — niet zelf aannemen; geen vast default-algoritme hardcoden.
- Geen neurale netwerken / deep learning.
- Splits altijd vóór preprocessing, alles in een sklearn Pipeline (geen leakage).
- De gebruiker is niet technisch: leg keuzes uit in gewone taal, zonder jargon.
