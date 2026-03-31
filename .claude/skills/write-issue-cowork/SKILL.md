---
name: write-issue-cowork
description: Writing and maintaining GitHub issues and pull requests for cedanl repositories from Cowork (without gh CLI). Uses the GitHub REST API via osascript (macOS curl) because the Cowork sandbox blocks outbound connections. Use when creating new issues, editing issue titles/bodies, creating PRs, or cleaning up issue metadata from within a Cowork session.
---

# Writing and maintaining GitHub issues en PRs (Cowork versie)

Deze skill gebruikt **macOS `osascript` met curl** om de GitHub REST + GraphQL API aan te roepen. De Cowork sandbox blokkeert directe outbound verbindingen naar GitHub; osascript gaat via de Mac zelf.

## Bronnen van waarheid

De ISSUE_TEMPLATE bestanden in `cedanl/.github` zijn leidend — lees ze altijd voor je een issue aanmaakt:

| Template | Type | Gebruik |
|----------|------|---------|
| `pitch.yml` | Pitch | Shape Up pitches |
| `task.yml` | Task | Losse taken |
| `bug.yml` | Bug | Bugmeldingen |

Lees een template zo:
```
osascript: do shell script "TOKEN=$(cat ~/.config/ceda/github_token) && curl -s https://api.github.com/repos/cedanl/.github/contents/.github/ISSUE_TEMPLATE/pitch.yml -H \"Authorization: Bearer $TOKEN\" -H 'Accept: application/vnd.github+json' | python3 -c \"import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())\""
```

De template bevat:
- `type:` → sla dit op als `typeName` (bijv. `Pitch`)
- `labels:` → standaard labels
- `projects:` → automatisch board (cedanl/2 = CEDA Board)
- `body:` → de velden en hun `label:` waarden → dit is de body structuur

## GitHub Token

Token staat op `~/.config/ceda/github_token`. Check geldigheid:
```
osascript: do shell script "TOKEN=$(cat ~/.config/ceda/github_token) && curl -s -o /dev/null -w '%{http_code}' -H \"Authorization: Bearer $TOKEN\" https://api.github.com/user"
```
`200` = geldig. Als er geen token is: vraag de gebruiker het via Terminal op te slaan:
```
osascript: display dialog "Sla GitHub PAT op in Terminal:\n\nread -rs T && printf '%s' \"$T\" > ~/.config/ceda/github_token" buttons {"OK", "Annuleer"} default button "OK"
```
**Nooit de token in de chat vragen.**

## Workflow

### 1. Bepaal type op basis van input

| Input | Type |
|-------|------|
| Bug, fout, broken, kapot, error | Bug |
| Groot werk, meerdere dagen, architectuur, evaluatie | Pitch |
| Al het andere | Task |

### 2. Lees de bijbehorende ISSUE_TEMPLATE

Lees `pitch.yml`, `task.yml` of `bug.yml` en gebruik de `label:` velden als secties in de body.

### 3. Bepaal labels

Gebruik de labels uit de `labels:` sleutel in de template, aangevuld met een domein-label:

| Label | Beschrijving |
|-------|--------------|
| `instroom` | Instroomprognose MBO |
| `uitval` | Uitval analyses |
| `tech` | Technische verbeteringen |
| `project` | Project organisatie |

### 4. Schrijf JSON naar ~/.config/ceda/ en POST via osascript

Schrijf altijd naar `~/.config/ceda/` — `/tmp` is alleen in de sandbox zichtbaar, niet op de Mac.

**Stap A — schrijf body naar ~/.config/ceda/issue.json:**
```
osascript: do shell script "python3 -c \"
import json
body = '''### Problem / Opportunity

[inhoud]

### Appetite (timebox)

Small (1-2 dagen)

### Solution

[inhoud]

### Risks / Rabbit holes

- [risico]

### No-Gos

- [no-go]

### Gevalideerd met

@username (moet nog)

### Sparring partner

@username'''
d = {'title': 'TITEL', 'body': body, 'labels': ['project'], 'assignees': ['USERNAME']}
open('/Users/corneeldenhartogh/.config/ceda/issue.json','w').write(json.dumps(d))
\""
```

**Stap B — POST naar GitHub REST API:**
```
osascript: do shell script "TOKEN=$(cat ~/.config/ceda/github_token) && curl -s -X POST https://api.github.com/repos/cedanl/REPO/issues -H \"Authorization: Bearer $TOKEN\" -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' -H 'Content-Type: application/json' --data-binary @/Users/corneeldenhartogh/.config/ceda/issue.json | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d['node_id'], d['html_url'])\""
```

### 5. Stel het issue type in via GraphQL

De REST API ondersteunt geen `type` — gebruik GraphQL met `issueTypeId`. Zoek eerst de type node_id op uit een bestaand issue of gebruik de bekende waarden:

| Type | node_id |
|------|---------|
| Pitch | `IT_kwDOCDg-4s4BLrPK` |
| Task | `IT_kwDOCDg-4s4BLrPF` |

```
osascript: do shell script "python3 -c \"
import json
q = {'query': 'mutation { updateIssue(input: {id: \\\\\"ISSUE_NODE_ID\\\\\", issueTypeId: \\\\\"TYPE_NODE_ID\\\\\"}) { issue { title } } }'}
open('/Users/corneeldenhartogh/.config/ceda/gql.json','w').write(json.dumps(q))
\" && TOKEN=$(cat ~/.config/ceda/github_token) && curl -s -X POST https://api.github.com/graphql -H \"Authorization: Bearer $TOKEN\" -H 'Content-Type: application/json' --data-binary @/Users/corneeldenhartogh/.config/ceda/gql.json"
```

### 6. Rapporteer het resultaat

Toon de `html_url` aan de gebruiker.

## Bekende repositories

| Repo | Gebruik |
|------|---------|
| `project_algemeen` | Algemene CEDA projecttaken |
| `1cho` | 1CHO gerelateerde issues |

## Bekende type node_ids (cedanl org)

| Type | node_id |
|------|---------|
| Pitch | `IT_kwDOCDg-4s4BLrPK` |
| Task | `IT_kwDOCDg-4s4BLrPF` |

## Dialoogvensters: altijd een sluitknop

```applescript
-- Goed ✓
display dialog "Bericht" buttons {"OK", "Annuleer"} default button "OK"

-- Fout ✗
display dialog "Bericht" buttons {"OK"} default button "OK"
```

## Important

- Lees altijd de ISSUE_TEMPLATE voor je een issue aanmaakt — dat is de bron van waarheid
- Schrijf tijdelijke bestanden naar `~/.config/ceda/`, nooit naar `/tmp`
- Nooit de GitHub token in de chat vragen
- Labels zijn case-sensitive
