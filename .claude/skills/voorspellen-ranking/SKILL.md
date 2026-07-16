---
name: voorspellen-ranking
description: Bouw risicoscore-modellen (bipartite ranking) die individuen sorteren van hoog naar laag risico, voor situaties met beperkte capaciteit waarin je de top-N selecteert — bijv. een uitnodigingsregel voor studenten met uitvalrisico, prioriteringslijsten, triage, "wie moeten we als eerste benaderen". Gebruik deze skill altijd bij woorden als uitnodigingsregel, risicoscore, risicoprioritering, top-N, ranking op uitval/churn/risico, learning to rank met binaire labels — óók als de gebruiker het "classificatie" noemt maar het doel een gesorteerde lijst is. De ranking-benadering is methodologisch onderbouwd in Eegdeman et al. (2022) en wordt in de praktijk toegepast in de uitnodigingsregel van cedanl; daar blijkt dat sorteren op risicoscore bij beperkte capaciteit betere selecties oplevert dan classificatie met een vaste beslisgrens.
---

# Voorspellen: bipartite ranking (risicoscore / uitnodigingsregel)

Doel: geen harde ja/nee-labels, maar een **score per individu** waarmee je sorteert van hoog naar laag risico. Het model is goed als de echte positieven (bijv. uitvallers) bovenaan staan — niet als elke individuele voorspelling "goed" of "fout" is. Evaluatie op rangorde-kwaliteit (AUC, precision@k), niet op accuracy. Klassieke classificatie optimaliseert een beslisgrens bij 0,5 en negeert de volgorde binnen de groepen; voor een lijst met beperkte capaciteit (top-N uitnodigen) wil je juist die volgorde goed hebben. Gebaseerd op cedanl/Uitnodigingsregel (Eegdeman et al., 2022). Verwante termen: learning to rank, AUC optimization.

## Workflow

When the user invokes `/voorspellen-ranking [optioneel: bestandspad of doelvariabele]`:

## Stap 0 — Check: is dit geen tijdreeks-forecasting?

Als de vraag is hoe een aantal of percentage zich **over de tijd** ontwikkelt (bijv. "hoeveel uitval verwachten we volgend jaar"), is dat forecasting, geen ranking van individuen — meld dat en gebruik deze skill niet. Deze skill is voor: individuen nu sorteren op risico.

## Stap 1 — Intake (altijd eerst vragen, niet zelf aannemen)

1. **Wat is de capaciteit (N of k)?** Hoeveel mensen kunnen er uitgenodigd/behandeld worden? Nodig voor precision@k. Onbekend: rapporteer bij meerdere k's (bijv. 5%, 10%, 20% van de populatie).
2. **Interpreteerbaar of black box?**
   - Interpreteerbaar = uitlegbaar waarom iemand hoog scoort (Lasso, logistische regressie). Vaak vereist bij besluiten over studenten.
   - Black box mag = vaak betere rangorde (Random Forest, Gradient Boosting, XGBoost, SVM). Geen deep learning.
3. **Instellingen automatisch fijnslijpen of standaardinstellingen?** (vraag het in deze gewone taal, niet met termen als hyperparameters, AUC of grids)
   - Standaard = snel, prima eerste versie.
   - Fijnslijpen = het model probeert veel combinaties van instellingen uit en kiest de beste. Duurt langer.
   - Intern, niet aan de gebruiker voorleggen: tune op scoring="roc_auc" (rangorde, niet accuracy); gebruik standaard de lokale grids uit `references/hyperparameters.md`; alleen als de gebruiker zelf CEDA, de benchmark of vergelijkbaarheid tussen instellingen noemt, de CEDA-grids.
4. **Meerdere modellen testen en vergelijken, of één aanbeveling volgen?** (in gewone taal vragen)
   - Vergelijken = aanpak van cedanl/uitnodigingsregel-benchmark: Random Forest, Lasso, SVM, Gradient Boosting, XGBoost naast elkaar, één tabel.
   - Aanbeveling = beoordeel zelf de case en beveel één algoritme aan met korte motivering. Weeg mee: aantal rijen en features, prevalentie van de positieve klasse, verwachte niet-lineariteit, en de interpretatie-eis uit vraag 2. Geen vaste default hardcoden. Benchmarkresultaten van cedanl mogen als context dienen, niet als automatisch antwoord.

## Stap 2 — Data

- Binaire doelkolom (bijv. `Dropout` 0/1). Continue doelvariabele → skill `/voorspellen-continu`.
- Is de data nog niet voorbereid, volg dan eerst de skill `/voorspellen-dataprep` (overzicht, leakage-check, missings, encoding, split).
- Splits 80/20 stratified (random_state=42) vóór preprocessing; alles in een Pipeline (geen leakage). Als er jaren beschikbaar zijn: liever trainen op eerdere jaren en testen op het laatste jaar (zoals config.yaml in de benchmark: training_years vs dropout_year) — dat lijkt op echt gebruik.
- Missings imputeren (mediaan/modus), one-hot met handle_unknown="ignore", StandardScaler alleen voor Lasso, logistische regressie en SVM.
- Klassenonbalans is hier normaal en geen probleem: ranking gebruikt de hele scoreverdeling; niet oversamplen tenzij expliciet gevraagd.

## Stap 3 — Score maken

Twee gangbare routes (cedanl/Uitnodigingsregel gebruikt beide):
- **Classifier met `predict_proba`**: gebruik de kans op de positieve klasse als score (LogReg, RF-classifier, GB, XGBoost, SVC met probability=True).
- **Regressor op het 0/1-label**: bijv. Lasso of RandomForestRegressor op de Dropout-kolom; de continue voorspelling is de score.

Gebruik **nooit** `predict()` met de 0,5-drempel als eindresultaat. De output is altijd: score → sorteren aflopend → rang.

Bij tunen: **scoring="roc_auc"** (bij regressor-route: custom AUC-scorer op de scores). Zoekmethode volgens `references/hyperparameters.md`; niet aan de gebruiker vragen.

## Stap 4 — Evaluatie en rapportage

Evalueer op de testset uitsluitend op rangorde-kwaliteit:
- **AUC (ROC-AUC)**: kans dat een willekeurige positieve boven een willekeurige negatieve staat. 0,5 = random.
- **Precision@k**: van de top-k op de lijst, welk aandeel is echt positief.
- **Recall@k**: welk aandeel van alle positieven zit in de top-k.
- **Precision/recall-curve over alle drempels** (zoals compute_dynamic_evaluation in cedanl/Uitnodigingsregel): cumulatief per rang, van hoogste score naar laagste.
- Baseline: random ranking (precision@k = prevalentie).

Rapporteer géén accuracy en géén confusion matrix bij drempel 0,5; leg kort uit waarom als de gebruiker erom vraagt.

Bij benchmark: één tabel met AUC en precision@k per algoritme, sorteer op AUC, benoem de winnaar en of het verschil bij de relevante k iets uitmaakt.

Lever op: (1) gesorteerde lijst met scores en rang (top-N gemarkeerd), (2) samenvatting in gewone taal, (3) herdraaibare code, (4) joblib-model op verzoek. Vermeld bij besluiten over personen dat de lijst een prioriteringshulp is, geen oordeel per individu.

## Important

- Voor top-N selectie bij beperkte capaciteit; harde ja/nee per individu → `/voorspellen-classificatie`, continue uitkomst → `/voorspellen-continu`.
- Data nog niet voorbereid? Eerst `/voorspellen-dataprep`.
- Gebruik **nooit** `predict()` met de 0,5-drempel als eindresultaat; output is altijd score → sorteren → rang.
- Rapporteer géén accuracy of confusion matrix; evalueer op rangorde (AUC, precision@k).
- Intake (Stap 1) altijd eerst vragen — niet zelf aannemen; geen vast default-algoritme hardcoden.
- Geen neurale netwerken / deep learning.
- Bij besluiten over personen: de lijst is een prioriteringshulp, geen oordeel per individu.
