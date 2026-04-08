---
name: generate-slides-retro-simple
description: Genereer een compacte, inhoudelijke Slidev sprint review presentatie voor CEDA, georganiseerd per domein (instroom/uitval/tech/project) met substantiemetriek op basis van commits, functies en het CEDA Board.
---

# generate-slides-retro-simple

Genereer een compacte sprint review presentatie voor CEDA, georganiseerd per domein met focus op wat er daadwerkelijk is opgeleverd.

## Instructies

### Stap 0: Clone het clidev project

1. Zoek of het project al ergens op de machine staat:
   ```bash
   find ~ -type f -name "_template.md" 2>/dev/null | xargs -I{} dirname {} | while read dir; do
     [ -d "$dir/theme" ] && [ -d "$dir/public/npuls" ] && echo "$dir"
   done | head -3
   ```
2. Als het niet gevonden wordt, clone het:
   ```bash
   git clone https://github.com/cedanl/clidev-presentaties.git ~/clidev-presentaties
   ```
3. Installeer dependencies als `node_modules/` ontbreekt:
   ```bash
   cd <project-pad> && npm install
   ```
4. Genereer de presentatie **in deze directory** met `theme: ./theme`. Naamconventie: `YYMMDD_sprint_review_simple.md`.

### Stap 1: GitHub Token check & sprint-periode

**Token check — voer dit uit VOORDAT je data ophaalt:**
1. Controleer of `$GITHUB_TOKEN` is ingesteld (`echo $GITHUB_TOKEN`).
2. Als het NIET is ingesteld, vraag de gebruiker:
   > Je hebt een GitHub Personal Access Token nodig. Heb je er al een?
   >
   > **Zo niet, maak er een aan:**
   > 1. Ga naar https://github.com/settings/tokens
   > 2. Klik op **"Generate new token (classic)"**
   > 3. Selecteer minimaal de scopes **`repo`** en **`read:org`** en **`project`**
   > 4. Klik op **"Generate token"** en kopieer het token
   >
   > **Plak je GitHub token hier in de chat:**
3. Zodra de gebruiker het token plakt:
   ```bash
   export GITHUB_TOKEN="<geplakt-token>"
   ```
4. Verifieer:
   ```bash
   curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep login
   ```

**Iteratie-periode ophalen van CEDA Board:**

Haal de actieve iteratie op van het CEDA Board (project #2) via GraphQL:

```bash
gh api graphql -f query='
{
  organization(login: "cedanl") {
    projectV2(number: 2) {
      field(name: "Iteratie") {
        ... on ProjectV2IterationField {
          configuration {
            iterations {
              id
              title
              startDate
              duration
            }
            completedIterations {
              id
              title
              startDate
              duration
            }
          }
        }
      }
    }
  }
}
'
```

- Gebruik de huidige/meest recente iteratie om `SPRINT_START` en `SPRINT_END` te bepalen
- `SPRINT_START` = `startDate` van de iteratie
- `SPRINT_END` = `startDate` + `duration` dagen
- Het veld heet "Iteratie" (Nederlands), niet "Iteration"
- Als er geen iteratie-veld is, val terug op 2 weken eindigend op vandaag
- Toon de iteratie-titel (bijv. "Sprint 12") in de presentatie

**Repo's ophalen en filteren:**
- Haal alle repos op: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/orgs/cedanl/repos?per_page=100&type=public"`
- Werk `config.json` bij met de resultaten.
- Pre-filter: alleen repo's waar `pushed_at >= SPRINT_START`.

### Stap 2: Categorie-mapping

Elke actieve repo wordt gemapt naar 1 van 5 domeinen:

| Domein | Kleur | Repos (pattern match) |
|--------|-------|----------------------|
| **instroom** | `#1D76DB` | `*instroom*`, `*prognose*`, `student-instroom-mbo`, `dashboard-instroomprognose-mbo` |
| **uitval** | `#D93F0B` | `*1cijfer*`, `*1cho*`, `*uitval*`, `*vsv*`, `*uitnodiging*`, `no-fairness-without-awareness`, `lta-hhs-fairnessawareness`, `Assistentie`, `student-signal` |
| **tech** | `#5319E7` | `*template*`, `*devcontainer*`, `sdp-tools`, `ceda-scoop`, `maak_een_hex`, `docker_1cho` |
| **project** | `#0E8A16` | `project_algemeen`, `ceda-algemeen`, `communicatie`, `.github`, `clidev-presentaties`, `public_activities`, `centre_documentation`, `regiobijeenkomsten` |
| **overig** | `#757575` | `arbeidsmarkt-mbo`, `cbs-onderwijsdata`, `overzicht-landelijke-databronnen`, `samenwijzer`, `eencijfer`, `textanalysis` |

Fallback voor onbekende repos: `overig`.

### Stap 3: Data ophalen

Haal 4 databronnen op voor alle actieve repo's:

#### A. Commits op main

Per actieve repo:
```bash
gh api "repos/cedanl/{repo}/commits?sha=main&since={SPRINT_START}&until={SPRINT_END}&per_page=100" \
  --jq '.[] | {sha: .sha, author: .author.login, message: .commit.message, date: .commit.author.date}'
```

Verzamel per repo:
- Totaal aantal commits
- Unieke contributors (GitHub usernames)
- Avatar URL per contributor: `https://github.com/{username}.png`

#### B. CEDA Board status via GraphQL

Haal alle items op van het CEDA Board (project #2) inclusief hun status:

```bash
gh api graphql -f query='
query($cursor: String) {
  organization(login: "cedanl") {
    projectV2(number: 2) {
      items(first: 100, after: $cursor) {
        nodes {
          status: fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
            }
          }
          iteratie: fieldValueByName(name: "Iteratie") {
            ... on ProjectV2ItemFieldIterationValue {
              title
            }
          }
          content {
            ... on Issue {
              number
              title
              state
              closedAt
              url
              body
              repository {
                name
              }
              issueType {
                name
              }
              assignees(first: 5) {
                nodes {
                  login
                }
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
'
```

**Let op:** gebruik GraphQL aliases (`status:` en `iteratie:`) omdat je twee `fieldValueByName` calls nodig hebt.

Filter items op `iteratie.title == {huidige iteratie titel}` om alleen items van de actieve iteratie te tonen.

Als `hasNextPage` true is, pagineer met `after: $endCursor`.

Verzamel per board item:
- Status: Done / In Progress / Todo / On Hold
- Issue type: Pitch / Task / Bug (uit `issueType.name`)
- Repo naam (voor categorie-mapping)
- Assignees (voor avatars)
- `closedAt` (voor filtering op sprint-periode)
- `body` (voor scope-analyse bij Pitches)

#### C. Functie-metric (20-100 regels) — alleen TOEGEVOEGDE code

Per actieve repo met commits, haal de diff op:

1. Bepaal het eerste commit SHA voor de sprint:
```bash
FIRST_SHA=$(gh api "repos/cedanl/{repo}/commits?sha=main&until={SPRINT_START}&per_page=1" --jq '.[0].sha')
```

2. Haal de compare op en filter op Python/R bestanden:
```bash
gh api "repos/cedanl/{repo}/compare/{FIRST_SHA}...main" \
  --jq '.files[] | select(.filename | test("\\.(py|R|r)$")) | {filename, patch}'
```

3. Analyseer alleen de `+` regels uit elke patch (toegevoegde code):
   - **Python**: zoek naar `def ` blokken en tel regels tot het volgende `def`/`class` of dedent
   - **R**: zoek naar `<- function(` of `= function(` blokken en tel regels tot de sluitende `}`
   - Tel alleen functies van **20-100 regels**

4. Dit is een proxy voor "echte logica toegevoegd" — niet boilerplate, niet one-liners, niet monolithen.

5. Rapporteer per repo: "N functies (20-100 regels) toegevoegd"

#### D. Bestanden geraakt

Uit dezelfde compare API response:
```bash
gh api "repos/cedanl/{repo}/compare/{FIRST_SHA}...main" --jq '[.files[].filename] | length'
```

Context indicator (geen waardeoordeel):
- Breed (>20 bestanden) = feature/integratie werk
- Smal (<5 bestanden) = bugfix/refactor

### Stap 4: Metrics berekenen

1. **Opgeleverd**: Board items met Status=Done waarvan `closedAt` in de sprint-periode valt. Groepeer per type:
   - Pitches afgerond
   - Tasks afgerond
   - Bugs afgerond
   - **Ratio**: done / (done + in_progress + todo) — dit is de delivery ratio

2. **Toevoegingen**: Totaal functies 20-100 regels per domein.

3. **Scope per pitch**: Per Pitch op het board:
   - Check de issue body voor tasklists: `- [ ]` (open) en `- [x]` (done)
   - Check voor issue referenties (`#123`) in de body
   - Tel done vs totaal sub-items
   - Toont of een pitch echt af is of half

4. **Bestanden geraakt**: Totaal unieke files per domein.

### Stap 5: Genereer slides

**BELANGRIJK: Geen `<script>` of `<style>` tags in Slidev markdown slides!**
Alleen statische HTML (divs, tables, inline styles) direct in de slide markdown.

Genereer `YYMMDD_sprint_review_simple.md` in het clidev project met `theme: ./theme` in de frontmatter.

#### Slide 1 — Titel + Overzicht

"CEDA Sprint Review" + datum + sprint-periode.

5 domein-blokken naast elkaar (flex layout), elk met:
- Domeinnaam + kleur als `border-left: 4px solid {kleur}`
- Aantal commits + bestanden
- Contributor avatars (ronde `<img>` tags)

Onderaan 3 hero-getallen:
- **Opgeleverd**: done items count + ratio badge
- **Toevoegingen**: totaal functies 20-100 regels
- **Bestanden geraakt**: totaal unieke files

#### Slide 2 — Uitval & Instroom

Twee kolommen layout. Per domein:
- **Commits**: count + korte samenvatting van belangrijkste commit messages (2-3 bullets)
- **Functies 20-100r**: count + "substantieve logica toegevoegd"
- **Bestanden**: count + breed/smal indicator
- **Contributors**: avatar rij

#### Slide 3 — Tech & Project

Zelfde twee-kolommen layout als slide 2 voor de domeinen tech en project.

#### Slide 4 — Overig

Halve slide (1 kolom, max 50% breedte). Zelfde metrics als andere domeinslides.

#### Slide 5 — Scope per Pitch (Kanban)

Kanban board met 4 gelijke kolommen in deze volgorde:
1. **Todo** (rood, `#C62828`) — pitches die nog niet gestart zijn
2. **In Progress** (blauw, `#1565C0`) — pitches in uitvoering
3. **Done** (groen, `#2E7D32`) — opgeleverde pitches
4. **On Hold** (grijs, `#757575`) — geparkeerde pitches

**Alleen pitches**, geen tasks of bugs. Elke pitch als tegel met:
- Titel (aanklikbaar naar GitHub issue)
- Repo referentie + assignee avatars
- Domein-kleur als `border-left`

Alle 4 kolommen `flex: 1` (even groot).

#### Slide 6 — Toevoegingen

Tabel met per domein: commits, functies 20-100r, bestanden, scope (breed/smal), top repo.
- Totaalrij onderaan
- Leeswijzer: breed = feature/integratie, smal = bugfix/refactor
- Geen waardeoordeel, alleen context

#### Slide 7 — Afgeronde tasks

Tasks en bugs die los van een pitch zijn opgeleverd deze iteratie:
- Per item: type-badge (Task/Bug), titel, repo referentie, assignee avatar
- Aanklikbaar naar GitHub issue
- Onderaan: overzicht van open tasks deze iteratie (als context)

#### Slide 8 — Afsluiting

- "Vragen?"
- Alle contributor avatars in een grid
- Link naar github.com/cedanl

### Stap 6: Terminal summary

Naast de presentatie, print een compact markdown overzicht in de terminal:

```
## CEDA Sprint Review — {start} - {end}

### Opgeleverd: X/Y (Z%)
  Pitches: A/B | Tasks: C/D | Bugs: E/F

### Per domein
| Domein    | Commits | Functies (20-100r) | Bestanden | Contributors       |
|-----------|---------|--------------------|-----------|---------------------|
| instroom  |      12 |                  4 |        18 | @user1 @user2       |
| uitval    |       8 |                  2 |         7 | @user3              |
| tech      |      15 |                  6 |        32 | @user1 @user4       |
| project   |       3 |                  0 |         5 | @user2              |

### Scope per Pitch
- [x] Pitch A (instroom): 3/3 sub-items
- [ ] Pitch B (uitval): 1/4 sub-items
- [ ] Pitch C (tech): 2/5 sub-items
```

## Visuele componenten

### Slide layout patroon

Elke slide gebruikt achtergrond + absolute positioned content:

```html
<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;">
  <img src="/npuls/powerpoint_slides/SlideX.PNG" style="width: 100%; height: 100%; object-fit: cover;" />
</div>

<div style="position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 2rem 4rem; z-index: 1;">
  <!-- content hier -->
</div>
```

Achtergronden:
- `Slide1.PNG` — Titel (eerste en laatste slide)
- `Slide3.PNG` — Content slides
- `Slide5.PNG` — Overzicht slides (tabellen)

### Avatar

```html
<img src="https://github.com/{user}.png"
     style="width: 28px; height: 28px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-left: -6px;"
     title="{user}" />
```

### Domein-kaart

```html
<div style="background: rgba(255,255,255,0.9); border-left: 4px solid {KLEUR}; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.6rem;">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <span style="font-weight: bold; font-size: 0.85rem; color: {KLEUR};">{DOMEIN}</span>
    <span style="font-size: 0.65rem; color: #666;">{N} commits | {M} bestanden</span>
  </div>
  <p style="font-size: 0.65rem; color: #333; margin: 0.3rem 0;">{SAMENVATTING}</p>
  <div style="display: flex; gap: 0.3rem; align-items: center;">
    <!-- avatars hier -->
  </div>
</div>
```

### Delivery ratio bar

```html
<div style="display: flex; align-items: center; gap: 0.5rem;">
  <div style="flex: 1; background: #E0E0E0; border-radius: 4px; height: 12px;">
    <div style="background: #2E7D32; height: 100%; width: {PERCENTAGE}%; border-radius: 4px;"></div>
  </div>
  <span style="font-size: 0.6rem; font-weight: bold;">{DONE}/{TOTAL}</span>
</div>
```

### Type badges

```html
<!-- Pitch badge -->
<span style="background: #6A1B9A; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.55rem; font-weight: bold;">Pitch</span>
<!-- Task badge -->
<span style="background: #1565C0; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.55rem; font-weight: bold;">Task</span>
<!-- Bug badge -->
<span style="background: #C62828; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.55rem; font-weight: bold;">Bug</span>
```

### Pitch scope card

```html
<div style="background: rgba(255,255,255,0.9); border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 0.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06);">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <span style="font-weight: bold; font-size: 0.75rem;">{PITCH_TITEL}</span>
    <span style="font-size: 0.55rem; background: {STATUS_KLEUR}; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px;">{STATUS}</span>
  </div>
  <div style="font-size: 0.6rem; color: #666; margin: 0.2rem 0;">{REPO} | {DONE}/{TOTAL} sub-items</div>
  <!-- delivery ratio bar hier -->
</div>
```

### Domein kleuren

| Domein | Kleur | Licht |
|--------|-------|-------|
| instroom | `#1D76DB` | `#E3F2FD` |
| uitval | `#D93F0B` | `#FBE9E7` |
| tech | `#5319E7` | `#EDE7F6` |
| project | `#0E8A16` | `#E8F5E9` |
| overig | `#757575` | `#F5F5F5` |

## Bestanden

- `config.json` — Alle cedanl-repositories (wordt bijgewerkt bij elke run)
- `<clidev-pad>/YYMMDD_sprint_review_simple.md` — Slidev-presentatie (output)
- `<clidev-pad>/theme/` — Npuls huisstijl
- `<clidev-pad>/public/` — Afbeeldingen en logo's

## Presentatie starten

De server moet in een aparte terminal gestart worden:

```bash
cd <clidev-pad>
npx slidev YYMMDD_sprint_review_simple.md --open
```

De presentatie opent op http://localhost:3030.
