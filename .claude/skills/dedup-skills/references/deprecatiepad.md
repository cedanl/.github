# Het deprecatiepad — een skill laten verdwijnen uit een gekopieerde collectie

`npx skills add cedanl/.github` kopieert `.claude/skills/` naar de doelrepo. Er blijft niets
achter dat terugwijst: geen versie, geen lockfile, geen commando dat verdwenen skills opruimt.
Een `git rm` hier verandert daar dus niets. De kopie blijft staan, in de vorm van het moment
van kopiëren, en blijft triggeren.

Daarom vier stappen, in deze volgorde. Stap 3 is het verwijderen, en dat is expres niet stap 1.

## 1. De vervanger staat er eerst

De skill die de taak overneemt is gemerged en gevalideerd vóór de oude iets wordt aangedaan.
Bij een merge waarbij de rijkste versie de naam van de armste overneemt (`git mv B A`),
betekent dat: eerst A vervangen door de inhoud van B, valideren, mergen. Pas dan verdwijnt de
directory B.

Nooit een gat tussen weg en vervangen. Iemand die in dat gat `npx skills add` draait, houdt
niets over.

## 2. Tombstone, één iteratie lang

De directory blijft bestaan; `SKILL.md` wordt vervangen door een doorverwijzing. Alleen
bestaande velden — geen `ceda-deprecated`, dat leest niemand.

```markdown
---
name: ui-designer
description: Vervangen door `ontwerper-digitaal-product`. Deze skill doet niets meer. Gebruik wanneer je hier per ongeluk terechtkomt via een oude verwijzing of een oude kopie van de collectie — laad dan `ontwerper-digitaal-product`. LET OP — deze skill bevat geen inhoud; alles staat in `ontwerper-digitaal-product`.
allowed-tools: Read
metadata:
  ceda-id: ceda.ui-designer
  ceda-version: "2.0.0"
  ceda-type: reference
  ceda-subtype: knowledge
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: self
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: none
---

# ui-designer is vervangen

Deze skill is samengevoegd met `ontwerper-digitaal-product` (PR #NN, iteratie NN). De inhoud
staat daar, met de ISGVO-bundels die hier ontbraken.

Kom je hier via een oude kopie van de collectie: draai `npx skills add cedanl/.github`
opnieuw in die repo.

`ceda-verifies: none` — een tombstone voert niets uit, dus er is niets te verifiëren.
```

Waarom de description de doorverwijzing draagt en niet de body: de description is het enige
veld dat activeert. Vuurt de oude skill nog ergens, dan moet die ene regel al genoeg zijn.

Waarom een tombstone en niet direct weg: een skill die stil verdwijnt geeft een repo die
opnieuw synct een gat zonder uitleg. Een tombstone geeft die repo een aanwijzing, en geeft jou
één iteratie om stap 3 af te maken.

## 3. Zoek de kopieën en schrijf ze aan

De tombstone bereikt alleen repo's die opnieuw synchroniseren. De rest moet je opzoeken.

```bash
gh search code "name: <skillnaam>" --owner cedanl --filename SKILL.md
gh search code "<skillnaam>" --owner cedanl --filename SKILL.md   # ook verwijzingen
```

Per repo met een treffer één issue: welke skill vervalt, wat ervoor in de plaats komt, en het
commando om te syncen. Verzamel de issuenummers — die horen in de PR-body van de
opruimactie, want dat is het enige bewijs dat stap 3 gedaan is.

Staat de kopie in een repo buiten `cedanl`, dan houdt het op bij een melding in het kanaal
waar de collectie aangekondigd wordt. Dat is een bekende beperking, geen reden om stap 2 over
te slaan.

## 4. Volgende iteratie: tombstone weg

Zet dat in het issue van stap 3, niet in een `TODO` in de code. Een tombstone die blijft
staan is een lege skill die description-budget kost in elke sessie.

## Wat dit pad níet oplost

- **Een kopie die gewijzigd is.** Als iemand de skill lokaal heeft aangepast, is syncen geen
  optie meer en is het issue een gesprek, geen instructie.
- **Repo's die nooit reageren.** De kopie blijft daar bestaan. Wat je wint is dat je weet
  wáár, in plaats van dat aan te nemen.
- **Skills die via een plugin of marketplace verspreid zijn** in plaats van via
  `npx skills add`. Dan geldt het update-mechanisme van die marketplace, en dit pad niet.
