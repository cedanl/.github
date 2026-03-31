---
name: write-issue-cowork
description: Writing and maintaining GitHub issues and pull requests for cedanl repositories from Cowork. Uses the GitHub MCP connector (issue_write tool) as a wrapper around the cedanl issue templates. Use when creating new issues, editing issue titles/bodies, or cleaning up issue metadata from within a Cowork session.
---

# Write GitHub Issues (Cowork)

Wrapper rond de GitHub MCP connector die zorgt dat issues het juiste formaat krijgen op basis van de cedanl ISSUE_TEMPLATE bestanden.

**Vereiste:** De GitHub MCP connector moet verbonden zijn (Settings → Connectors).

---

## Workflow

### 1. Bepaal issue type

| Input bevat | Type |
|---|---|
| Bug, fout, error, kapot | Bug |
| Groot werk, meerdere dagen, architectuur, evaluatie, business case, roadmap | Pitch |
| Al het andere | Task |

Twijfel? Kies Pitch als het werk meer dan 2 dagen duurt.

### 2. Bouw de body op basis van het template

Vul in wat je weet vanuit de gebruikersinput; laat secties leeg (maar behoud de koppen) als er geen info voor is.

### 3. Roep issue_write aan

Gebruik altijd list_issue_types(owner="cedanl") om het juiste type op te halen voor je de issue aanmaakt.



Rapporteer de html_url uit de response aan de gebruiker.

---

## Labels (verplicht)

Elk issue krijgt minimaal een label. Bron: cedanl/.github/.github/labels.yml

### Domein labels

| Label | Beschrijving |
|---|---|
| instroom | Instroomprognose MBO |
| uitval | Uitval analyses |
| tech | Technische verbeteringen |
| project | Project organisatie |

### Status labels

| Label | Beschrijving |
|---|---|
| needs-shaping | Pitch die nog gevormd moet worden |

**Keuzelogica:**
- Pitch over project organisatie / iteratie planning -> project
- Pitch over inhoudelijk werk (instroom, uitval, tech) -> kies het bijpassende domein label + eventueel needs-shaping
- Task die bij een pitch hoort -> zelfde label als de pitch
- Bug -> tech

---

## Geldige type waarden

Gebruik altijd list_issue_types(owner="cedanl") voor actuele waarden. Bekende waarden:

| Naam | Gebruik |
|---|---|
| Pitch | Shape Up pitch voor groter werk |
| Task | Taak of werk unit |
| Bug | Bug of probleem |

---

## Body Templates

### Bug

### Beschrijving

**Wat gaat er mis?**
...

**Stappen om te reproduceren:**
1. ...

**Screenshots / Logs (optioneel):**
...

### Task

### Beschrijving

Wat moet er gedaan worden?

### Acceptatiecriteria

- [ ] ...
- [ ] ...

### Pitch

### Problem / Opportunity

Wat is het echte probleem? Voor wie? Evidence, voorbeelden, context.

### Appetite (timebox)

Small (1-2 dagen) | Medium (3-4 dagen) | Large (5-6 dagen)

### Solution

High-level aanpak, misschien enkele key elements.

### Risks / Rabbit holes

Welke valkuilen moeten we vermijden?

### No-Gos

Wat doen we expliciet NIET in deze versie?

### Gevalideerd met

@

### Sparring partner

@

---

## Bekende repositories

| Repo | Gebruik |
|---|---|
| project_algemeen | Algemene CEDA projecttaken |
| 1cho | 1CHO gerelateerde issues |

---

## Titel richtlijnen

- Specifiek en beschrijvend
- Sentence case
- Geen prefixes zoals [FEATURE] of [BUG] - gebruik labels

---

## Overige afspraken

- CEDA Board: https://github.com/orgs/cedanl/projects/2
- Blank issues zijn uitgeschakeld - gebruik altijd een template body
- Link gerelateerde issues met #issue-number
- Gebruik @username voor validatie en sparring partners in pitches
- Nooit Generated with Claude Code in issues zetten
