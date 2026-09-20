# Skill Bouwmodel

Het CEDA-model om skills, commands, hooks en connectors te classificeren. Het bouwmodel beschrijft *hoe een individuele skill is gebouwd*, los van hoe skills zich tot het CEDA-werk verhouden.

**Canonieke bron:** `.claude/skills/skills-ontology/SKILL.md` — wijzigingen aan het model landen daar via review. Dit document is een navigatiepunt; de inhoud staat in de skill, niet hier.

**Gerelateerde kaarten:**
- [`ceda-werklandkaart.md`](ceda-werklandkaart.md) — het CEDA-werk zelf: keten en dwarslagen
- [`skills-landkaart.md`](skills-landkaart.md) — welke skills er zijn, waar ze hangen, waar de gaten zitten

---

## Wat het bouwmodel bevat

Het model geeft antwoord op drie vragen bij elk ding dat in de harness belandt:

**1. Wat voor ding is het?**

| Laag | Bevat | Voorbeeld |
|---|---|---|
| workflow | stappenreeks / beslislogica | `ship`, `create-skill`, `etl-pipeline` |
| reference | kennis, regels, stijl, persona — geen sequentie | `skills-ontology`, `npuls-huisstijl`, `check-style` |
| connector | data of tools via een protocol | MCP-servers |

**2. Hoe gedraagt het zich?**

Vijf assen per ding: activation (wat triggert het), binding (hoe dwingend), scope (org of project), execution (inline of geïsoleerd), tools (welke mag het aanraken).

**3. Waar komt het vandaan?**

Twee velden: `origin` (wie schreef dit artefact — own / extended / external) en `source` (waar staat de bron van waarheid buiten de skill).

---

## Waarom "bouwmodel" en niet "ontologie"

"Ontologie" belooft een begrippenstelsel over het domein — welke processen bestaan, hoe skills tot het CEDA-werk verhouden. Dit document levert dat niet: het classificeert één skill op technische assen. Dat is een bouw- en classificatiemodel, geen domeinontologie.

De domeinontologie leeft in de werklandkaart en de skills-landkaart samen.

---

## Volledig model

Lees `.claude/skills/skills-ontology/SKILL.md` voor:

- de drie lagen met definitie en gotcha's
- de vijf assen met beslisregels
- het frontmatter-schema (velden, types, verplicht/optioneel)
- description-eisen en de twee vormen van exclusion-clause
- progressive disclosure (drie laadniveaus)
- verificatie vs. evaluatie
- patronen: splitsen, chaining, één info / meerdere doelgroepen
- gotchas en bekende misverstanden

De rationale (waarom deze indeling, welke alternatieven zijn afgevallen) staat in `.claude/skills/skills-ontology/references/rationale.md`.
