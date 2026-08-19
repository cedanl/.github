---
name: write-issue
description: Maakt en onderhoudt GitHub issues in cedanl-repos via een interview — vraagt de gebruiker per templateveld om de inhoud en vult zelf niets in. Gebruik bij "maak een issue", "schrijf hier een issue van", een bug, task of pitch opvoeren, of het bijwerken van een titel, body of labels. LET OP — gaat het om een pull request, gebruik dan `branch-pr`; om code- of stijlcontrole vooraf, `check-style`.
allowed-tools: Read Grep Glob Bash AskUserQuestion
compatibility: Requires the gh CLI, authenticated with access to the cedanl org and its projects
metadata:
  ceda-id: ceda.write-issue
  ceda-version: "2.0.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: .github/ISSUE_TEMPLATE/
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Issues schrijven voor cedanl

Maakt een issue in een cedanl-repo op basis van wat de gebruiker zégt — niet op basis van wat
jij erbij bedenkt. De skill doet het interview, de vorm en het `gh`-werk; de inhoud komt van
de gebruiker.

## De regel: de gebruiker levert de inhoud, jij levert de vorm

Elke zin in de body heeft precies één van deze drie herkomsten:

| Herkomst | Voorbeeld |
|---|---|
| Letterlijk wat de gebruiker in dit gesprek zei | zijn beschrijving, zijn acceptatiecriterium |
| Een suggestie die hij in dit gesprek heeft aangewezen | jij bood drie criteria aan, hij koos er twee |
| Een verwijzing die je zelf hebt gezien en die hij goedkeurde | `#42`, `src/app.py:88`, een commit-sha |

Wat geen van drieën is, komt niet in de body. Een lege sectie is beter dan een ingevulde
sectie die de gebruiker niet herkent: hij moet zijn eigen issue over een week nog herkennen,
en een verzonnen reproductiestap kost een collega een middag.

Wat dat concreet betekent:

- **Optioneel templateveld zonder antwoord → laat het weg.** Niet "n.v.t.", niet een aanname,
  niet een alinea die de leegte opvult.
- **Verplicht veld zonder antwoord → vraag opnieuw.** Maak de issue niet aan zolang het
  ontbreekt.
- **"Vul maar aan met context uit de code" is geen vrijbrief.** Zoek, toon wat je vond met pad
  en regelnummer, en vraag of het erin mag. Nooit stilzwijgend samenvatten.
- **Suggesties zijn kort en meervoudig.** Bied er twee tot vier aan, zodat kiezen goedkoper is
  dan corrigeren — vier is ook het maximum dat `AskUserQuestion` toont. Een suggestie staat pas
  in de body nadat hij hem heeft aangewezen.
- **Schrijf niets mooier dan het gezegd is.** Zijn zin van één regel blijft één regel.

Zo ziet het verschil eruit:

> **Gebruiker:** "de streamlit-app crasht als je een leeg bestand upload."
>
> **Wel:** Beschrijving = die zin. Reproductiestappen = daar vraag je naar.
>
> **Niet:** drie verzonnen reproductiestappen, een alinea "verwacht gedrag", een
> omgevingstabel, of een acceptatiecriterium over foutafhandeling dat hij nooit noemde.

## Workflow

When the user invokes `/write-issue [beschrijving]`:

### 1. Repo en type

Doelrepo: die van de huidige werkmap, maar alleen als de issue daar ook over gaat. Komt het
verzoek van buiten de code — een mail, een afspraak, iets org-breeds — vraag de repo dan via
`AskUserQuestion` met je eigen voorstel als eerste optie. Raad hem niet uit de tekst.
`cedanl/project_algemeen` is de verzamelplek voor projectmatige issues die bij geen enkele
codebase horen.

Stel het type voor op basis van zijn woorden en laat het bevestigen via een keuzemenu
(`AskUserQuestion`). Voorstellen mag, kiezen doet de gebruiker.

| Type | Waarvoor | Issue type-ID (cedanl, org-breed) |
|---|---|---|
| Bug | Er gaat iets kapot dat zou moeten werken | `IT_kwDOCDg-4s4BLrPI` |
| Task | Taak, item of werkeenheid | `IT_kwDOCDg-4s4BLrPF` |
| Pitch | Shape Up-pitch voor groter werk dat afstemming vraagt | `IT_kwDOCDg-4s4BLrPK` |

Werkt een ID niet meer, haal ze dan opnieuw op:

```bash
gh api graphql -f query='{ repository(owner: "cedanl", name: "<repo>") { issueTypes(first: 10) { nodes { id name } } } }'
```

### 2. Lees de templates van de doelrepo

```bash
ls .github/ISSUE_TEMPLATE/
cat .github/ISSUE_TEMPLATE/<type>.yml
```

De velden in dat bestand zijn de waarheid — inclusief welke `required: true` zijn. Wijkt de
repo af van wat je hier verwacht, dan volg je de repo. Ontbreken de templates, val dan terug
op de vaste velden onderaan deze skill.

### 3. Interview — één veld tegelijk

Loop de templatevelden af in de volgorde van het bestand. Per veld één vraag in de chat, met
het `label` van het veld en de `placeholder` als voorbeeld. Wacht op antwoord voor je de
volgende stelt.

- Meerdere vragen in één bericht levert antwoord op de eerste en stilte op de rest. Doe het niet.
- Zegt de gebruiker "sla over": optioneel veld valt weg, verplicht veld vraag je één keer
  opnieuw — blijft het leeg, dan maak je de issue niet aan en zeg je dat.
- **De vorm van je vraag bepaalt het middel, niet de veldsoort.** Vraag je open naar tekst die
  alleen de gebruiker heeft (beschrijving, probleem), dan doe je dat in de chat. Zet je zelf
  een lijstje neer waar hij uit kiest, dan is dat een keuzelijst — ook bij een vrij-tekstveld
  als acceptatiecriteria — en hoort hij in `AskUserQuestion` met `multiSelect: true`. Anders
  moet hij jouw bullets corrigeren in plaats van aanvinken, en dat is precies het verschil dat
  deze skill wil wegnemen.
- **Grenzen van `AskUserQuestion`.** Maximaal vier opties; "Other" vangt eigen tekst, dus dat
  hoeft geen eigen optie. Houd vraag en labels kort — lange regels breken de weergave. Past je
  set daar niet in, snoei dan tot de vier die er het meest toe doen, of ga terug naar de chat.
- Gaf de gebruiker bij het aanroepen al een beschrijving mee, gebruik die dan als antwoord op
  het eerste veld en zeg dat je 'm daar hebt neergezet — herhaal de vraag niet.

### 4. Labels — leg de indeling voor

Lees `references/labels.md`. Vraag de labels in de volgorde van de indeling, met
`AskUserQuestion` en steeds "geen" als geldige optie:

1. **soort** — `intern` · `impact` · `tech` · `core`
2. de tweede categorie die daaruit volgt: `intern` → intern-labels, `impact` → impact-labels,
   `tech` → tech-labels, `core` → werk-labels
3. **aspect** — `docs` · `ux`, optioneel en los van de soort
4. **inhoud** — optioneel, meestal bij `impact` of `core`
5. **status** — alleen als het van toepassing is (`needs-shaping` bij een ongevormde pitch)

Alles is optioneel, ook de soort: de indeling maakt kiezen makkelijker, ze is geen
invulplicht. Toon per categorie de waarden die er echt zijn:

```bash
gh label list --repo cedanl/<repo>
```

Wil de gebruiker een label dat niet bestaat, verzin het niet ter plekke: vraag onder welke
categorie het hoort, en noem de route uit `references/labels.md` — toevoegen aan
`references/labels.yml` met de kleur van die categorie. Een los label buiten de indeling maakt de
kleur betekenisloos.

### 5. Assignees — wie pakt dit op

Een issue zonder eigenaar blijft liggen. Vraag de assignees expliciet, met een concreet
voorstel als eerste optie.

| Type | Minimum |
|---|---|
| Pitch | twee — shape-up werk vraagt afstemming, één persoon alleen is geen pitch |
| Task | één |
| Bug | één |

**Meestal is de gebruiker zelf de eerste assignee.** Hij brengt de issue in, dus stel hem voor
en laat hem bevestigen — dat is een suggestie die hij aanwijst, geen invulling. Uitzondering:
staat er in zijn verzoek uitdrukkelijk voor wie de issue is ("issue voor Piet en Henk"), dan
zijn dat de assignees en stel je jezelf niet als alternatief voor.

Zijn eigen handle haal je op, raad hem niet uit de accountnaam:

```bash
gh api user --jq .login
```

De rest kies je uit de echte ledenlijst, nooit uit een naam die je ergens zag staan:

```bash
gh api orgs/cedanl/members --jq '.[].login'
```

Vraag met `AskUserQuestion` en `multiSelect: true`, met de gebruiker zelf als eerste optie.
Blijft het aantal onder het minimum, vraag dan één keer door wie er nog bij hoort. Houdt hij
vol, maak de issue dan wel aan en meld in stap 9 expliciet dat hij onder het minimum blijft —
dat is zijn keuze, maar hij moet hem zien.

Assignee is iets anders dan "Gevalideerd met" en "Sparring partner" in de pitch: die twee zijn
bodyvelden waar je nooit zelf iemand invult (zie onderaan). De assignee mag je voorstellen,
mits hij bevestigt.

### 6. Boardvelden — optioneel, en alleen op verzoek

Priority en Iteration zijn velden op het CEDA Board, geen labels. Vraag ze één keer, met
"laat leeg" als eerste optie. Vul ze nooit zelf in: een prioriteit die de gebruiker niet
koos, stuurt andermans planning.

| Veld | Field-ID | Opties |
|---|---|---|
| Priority | `PVTSSF_lADOCDg-4s4BOMC2zhBPZ0s` | High · Medium · Low |
| Iteration | `PVTIF_lADOCDg-4s4BOMC2zg8-YWo` | wisselt — altijd opvragen |

```bash
gh api graphql -f query='{ organization(login:"cedanl"){ projectV2(number:2){ id
  fields(first:30){ nodes{
    ... on ProjectV2SingleSelectField { id name options { id name } }
    ... on ProjectV2IterationField { id name configuration { iterations { id title } } } } } } }'
```

Vereist project-scope: `gh auth refresh -s project`. De standaardlogin heeft
`gist, read:org, repo, workflow` en struikelt met `missing required scopes [read:project]`;
`read:project` is niet genoeg, want het iteration-veld wordt geschreven. De refresh vraagt om
browserbevestiging, dus de gebruiker moet hem zelf draaien. Lukt dat niet, meld het en laat de
velden leeg — dat blokkeert het aanmaken niet.

Iteraties duren twee weken en de ID's roteren mee, dus onthoud ze niet. Lopende en toekomstige
staan in `iterations`, afgeronde in `completedIterations`:

```bash
command gh api graphql -f query='{ node(id: "PVTIF_lADOCDg-4s4BOMC2zg8-YWo") {
  ... on ProjectV2IterationField { configuration {
    iterations { id title startDate duration }
    completedIterations { id title startDate } } } } }'
```

Zegt de gebruiker "volgende iteratie", reken dat dan uit met de `startDate`s in plaats van te
tellen vanaf een nummer dat je ergens zag staan — en laat in stap 6 zien welke iteratie en
welke datums je gekozen hebt, zodat hij de aanname kan corrigeren.

**rtk-valkuil.** Bij grote of diep geneste `gh api graphql`-output vervangt rtk het antwoord
door een schemasamenvatting (`{id: string, title: string} (3)`) in plaats van de waarden. Draai
daarom `command gh` (of `rtk proxy`) zodra je de echte veld-ID's nodig hebt. Hetzelfde geldt
voor `command grep` wanneer rtk's grep je flags niet accepteert.

### 7. Toon de volledige body en wacht op akkoord

Verplicht, ook bij een issue van drie regels. Toon titel, type, labels, assignees, boardvelden
en de body letterlijk zoals die aangemaakt wordt, en benoem apart welke regels uit een suggestie
van jou komen.

> Klopt dit? Zeg wat je wil aanpassen, of geef akkoord om aan te maken.

Geen akkoord, geen `gh issue create`.

### 8. Maak de issue aan en zet type en boardvelden

```bash
gh issue create \
  --repo cedanl/<repo> \
  --title "<titel>" \
  --label "<label1>,<label2>" \
  --assignee "<handle1>,<handle2>" \
  --project "CEDA Board" \
  --body "$(cat <<'EOF'
<geformatteerde body>
EOF
)"
```

Zet daarna het type met het ID uit stap 1:

```bash
gh api graphql -f query='{ repository(owner: "cedanl", name: "<repo>") { issue(number: <nr>) { id projectItems(first: 5) { nodes { id } } } } }'
gh api graphql -f query='mutation { updateIssue(input: { id: "<issue_node_id>", issueTypeId: "<type_id>" }) { issue { title issueType { name } } } }'
```

Koos de gebruiker in stap 6 een Priority of Iteration, zet die op het project-item:

```bash
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {
  projectId: "PVT_kwDOCDg-4s4BOMC2", itemId: "<project_item_id>",
  fieldId: "<field_id>", value: { singleSelectOptionId: "<option_id>" } }) { projectV2Item { id } } }'
```

Voor Iteration is de waarde `{ iterationId: "<iteration_id>" }`.

Staat de issue nog niet op het board — `projectItems` is leeg omdat `--project` niet aansloeg —
haal het item-ID dan op door hem alsnog toe te voegen:

```bash
command gh project item-add 2 --owner cedanl --url <issue-url> --format json
```

### 9. Rapporteer

De issue-URL, plus welke labels, welk type, welke assignees en welke boardvelden gezet zijn.
Blijft het aantal assignees onder het minimum uit stap 5, zeg dat er dan bij.

## Een bestaande issue bijwerken

Dezelfde regel, en één toevoeging: raak alleen de velden aan die de gebruiker noemt. Haal de
huidige body op (`gh issue view <nr> --repo cedanl/<repo> --json title,body,labels`), toon oud
naast nieuw, wacht op akkoord, en pas dan `gh issue edit`. Het en passant "beter maken" van
tekst waar hij niet om vroeg is precies het probleem dat deze skill oplost.

## Let op: `gh issue create` slaat de issue-templates over

De templates in `.github/ISSUE_TEMPLATE/` dragen zelf al `type:` en `projects: cedanl/2`, maar
alleen de web-UI leest ze. Via `gh` krijg je een blanco issue. Daarom neem je de velden in
stap 2 zelf over, geef je `--project "CEDA Board"` mee, en zet je het type in stap 7.

## Titels

Specifiek en beschrijvend, zinskapitaal, geen prefix als `[FEATURE]` — daar zijn labels voor.

| Goed | Slecht |
|---|---|
| `Add export functionality for enrollment data` | `Bug` |
| `Data pipeline fails when processing empty CSV files` | `Fix thing` |
| `Verbeter dagstart workflow met GitHub integratie` | `NEW FEATURE` |

## Velden per type, als de repo geen templates heeft

- **Bug** — Beschrijving (verplicht): wat gaat er mis, stappen om te reproduceren, optioneel
  screenshots/logs.
- **Task** — Beschrijving (verplicht), Acceptatiecriteria (optioneel, checkboxes, maximaal
  vier). Meer dan vier criteria betekent meestal dat er twee taken in één issue zitten.
- **Pitch** — Problem / Opportunity (verplicht), Appetite: Small (1-2 dagen) | Medium (3-4
  dagen) | Large (5-6 dagen) (verplicht), Solution, Risks / Rabbit holes, No-Gos, Gevalideerd
  met, Sparring partner (alle vijf optioneel).

Bij "Gevalideerd met" en "Sparring partner" vul je nooit zelf iemand in — anders dan bij de
assignees in stap 5, waar je de gebruiker zelf wél mag voorstellen. Handles toets je tegen de
echte ledenlijst:

```bash
gh api orgs/cedanl/members --jq '.[].login'
```

## Verificatie

`ceda-verifies: observable` — na afloop klopt dit, na te lopen door de gebruiker:

- Elke alinea in de body is terug te voeren op iets wat de gebruiker zei of aanwees.
- Geen enkel templateveld is ingevuld zonder antwoord van de gebruiker.
- De volledige body is vóór aanmaken getoond en er is akkoord gegeven.
- Elk label bestaat in de repo en past in de indeling; elke `@handle` bestaat in de org.
- De issue heeft assignees die de gebruiker aanwees — twee bij een pitch, één bij een task of
  bug — of het rapport benoemt waarom niet.
- Priority en Iteration staan alleen gevuld als de gebruiker ze koos.

## Gebundelde bestanden

- `references/labels.md` — lees bij stap 4, of zodra iemand een label wil dat niet bestaat: de
  categorieën, wat er per soort bij hoort, en hoe je de lijst uitbreidt zonder de indeling te
  slopen
- `references/labels.yml` — niet lezen om labels voor te stellen (gebruik `gh label list`);
  bewerken als er een label bij moet. Dit is de machine-bron die `sync-labels.yml` naar alle
  cedanl-repos duwt

## Important

- **Verzin niets.** Bij twijfel minder tekst, niet meer. Een issue die de gebruiker niet
  herkent is erger dan een issue die te kort is.
- **Nooit aanmaken zonder getoonde body en expliciet akkoord.**
- Alleen voor cedanl-repos; blanco issues staan uit, dus gebruik altijd een van de drie types.
- **Nooit aanmaken zonder assignee.** Wie het oppakt hoort erbij; blijft het onder het minimum,
  dan is dat een expliciete keuze van de gebruiker die je meldt.
- Priority, Iteration en Status zijn boardvelden — nooit labels. Zie je `high-priority` of
  `on-hold` op oude issues, kopieer dat niet.
- Voor pull requests: `branch-pr`.
- Zet nooit "Generated with Claude Code" in een issue, en link gerelateerd werk met
  `#issue-nummer`.
