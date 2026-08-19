---
name: write-issue-cowork
description: Vervangen door `write-issue`. Deze skill doet niets meer. Gebruik wanneer je hier per ongeluk terechtkomt via een oude verwijzing of een oude kopie van de collectie — laad dan `write-issue`. LET OP — deze skill bevat geen inhoud; alles staat in `write-issue`.
allowed-tools: Read
metadata:
  ceda-id: ceda.write-issue-cowork
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

# write-issue-cowork is vervangen

Deze skill is samengevoegd met `write-issue`. Cowork is geen aparte werkwijze meer: dezelfde
interview-workflow, dezelfde issuetemplates, dezelfde labelindeling. Werk je met de
GitHub-connector in plaats van de `gh` CLI, gebruik dan dezelfde stappen en voer de aanroepen
uit met de connector-tools.

Kom je hier via een oude kopie van de collectie: draai `npx skills add cedanl/.github` opnieuw
in die repo.

`ceda-verifies: none` — geen verificatie: een tombstone voert niets uit, dus er is niets te
meten.
