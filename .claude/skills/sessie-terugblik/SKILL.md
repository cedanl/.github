---
name: sessie-terugblik
description: Legt vast hoe een sessie ging — vaste vragenset over de werkwijze, antwoorden in de woorden van de deelnemer. Gebruik bij "reflectie", "terugblik", "hoe ging dit", "wat ging goed", "blinde vlekken" — ook halverwege, niet alleen aan het eind. LET OP — een sprint review met slides hoort bij `generate-slides-retro-simple`; niet voor een automatische samenvatting van wat er gebeurde.
allowed-tools: Read Grep Glob Write Bash
compatibility: Requires git, python3 and the gh CLI with write access to cedanl/repo-context-as-data
metadata:
  ceda-id: ceda.sessie-terugblik
  ceda-version: "0.5.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: https://github.com/cedanl/ceda-workshop-starter/blob/main/.claude/skills/sessie-reflectie/SKILL.md
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Sessie-terugblik

Kijkt terug op **het proces, niet op het product**: hoe er gewerkt is, wat er gebruikt is, wat
goed ging en wat iemand nu pas ziet. De uitkomst is één markdownbestand in de data-repo
`cedanl/repo-context-as-data`, met een frontmatter die de terugblik aan de commits van die
sessie knoopt. Terugblikken mag op elk moment — halverwege een sessie net zo goed als aan het
eind.

De waarde zit in de antwoorden van de deelnemer, niet in jouw samenvatting van de sessie. Vul
niets voor iemand in; wat jij zag krijgt een eigen sectie.

## Workflow

Bij `/sessie-terugblik [optioneel: andere data-repo]`:

### 1. Haal de context uit git log

Beperkt houden. Deze commando's, meer niet:

```bash
git log --since="1 day ago" --pretty=format:'%h %an %s' | head -30
git log --since="1 day ago" --pretty=format:'%H' | tail -1   # eerste commit van de reeks
git log -1 --pretty=format:'%H'                              # laatste
git log --since="1 day ago" --pretty=format:'%(trailers:key=Entire-Checkpoint,valueonly)'
basename "$(git rev-parse --show-toplevel)"                   # <repo> in het pad
git remote get-url origin                                     # <owner>/<repo> in de frontmatter
```

`repo:` in de frontmatter leid je af van de **remote**, niet van de directorynaam en niet van
een aanname dat alles in `cedanl` staat — er wordt ook in andere org's en in forks gewerkt.
Geen remote? Vul dan alleen de repositorynaam in.

Hieruit komt de naam (`%an` van de eigen commits), waar aan gewerkt is, de commit-range en de
checkpoint-id's als die er zijn. Geen zoektocht door statusbestanden, planningsdocumenten of
het transcript — die zijn per project anders en de terugblik hoort niet van jouw reconstructie
af te hangen.

Geen git-repo, of geen commits vandaag? Stel dan één vraag: *"Waar heb je aan gewerkt deze
sessie?"* en gebruik dat antwoord als context. Naam uit `git config user.name`, of vraag hem.
Commit-range blijft dan leeg — dat is een geldige uitkomst, geen reden om iets te verzinnen.

### 2. Tel het verbruik

```bash
python3 .claude/skills/sessie-terugblik/scripts/sessie-tokens.py
```

Geeft YAML-regels terug die zo in de frontmatter kunnen. Vraag de gebruiker hier niets over en
laat hem geen `/cost` draaien — dat kost een beurt en levert een getal op dat niemand later
nog kan narekenen. Vindt het script geen transcript, dan geeft het nullen terug; dat is een
geldige uitkomst, geen reden om te stoppen.

### 3. Stel de vragen

Lees nu `references/vragenset.md` en volg die. Eén vraag per keer, wachten op antwoord.

Heeft de gebruiker een vraag al beantwoord in zijn openingsbericht, stel 'm dan niet opnieuw.

### 4. Bouw het bestand

Pad — de datum is de dag van de terugblik, `<repo>` de repositorynaam uit stap 1, `<naam>` in
kebab-case:

```text
data/<YYYY-MM-DD>/<repo>/sessie-terugblik-<naam>.md
```

Frontmatter, altijd deze sleutels, leeg laten kan maar weglaten niet:

```yaml
---
type: sessie-terugblik
repo: <owner>/<repo>   # uit de remote; alleen <repo> als er geen remote is
datum: <YYYY-MM-DD>
naam: <volledige naam uit git>
commits: <eerste-sha>..<laatste-sha>
commit-aantal: <n>
entire-checkpoints: []
skill-versie: "0.5.0"
<de regels uit stap 2: sessie-id, sessie-berichten, tokens-in, tokens-uit,
 tokens-cache-schrijf, tokens-cache-lees>
---
```

Daaronder de secties `## Werkwijze`, `## Gebruikt`, `## Ging goed` en `## Blinde vlekken` —
in de woorden van de deelnemer. En tot slot `## Acties` als checklist.

De regels voor `## Acties` staan in `references/vragenset.md`. Kern: acties komen uit wat er
gezegd is, nooit uit wat jij er zelf bij bedenkt.

Wil de deelnemer acties toewijzen aan iemand, verwijs dan naar `write-issue`; deze skill maakt
geen issues aan.

### 5. Toon het concept en wacht op akkoord

Laat het volledige bestand zien, inclusief pad en frontmatter. Verwerk feedback en herhaal tot
akkoord. Schrijf niets naar de data-repo voor hij akkoord geeft.

### 6. Schrijf het weg

Bestaat het pad al — tweede terugblik op dezelfde dag door dezelfde persoon — hang er dan
`-2`, `-3` aan. **Nooit overschrijven**: een terugblik is een waarneming op een moment, en een
overschreven terugblik is een verloren waarneming.

```bash
unset GITHUB_TOKEN
DATA_REPO=cedanl/repo-context-as-data          # of het argument
PAD="data/$(date +%F)/<repo>/sessie-terugblik-<naam>.md"

gh api "repos/$DATA_REPO/contents/$PAD" --jq .sha 2>/dev/null   # leeg = vrij, sha = kies -2

gh api --method PUT "repos/$DATA_REPO/contents/$PAD" \
  -f message="terugblik: <repo> — <naam>, $(date +%F)" \
  -f content="$(base64 -i <lokaal-conceptbestand> | tr -d '\n')"
```

### 7. Rapporteer

De URL van het bestand in de data-repo, en de commit-range die erin staat.

## Let op: dit koppelt op commit-SHA, niet op tekst

De frontmatter is het hele punt van dit ontwerp. Checkpoint-tooling (entire.io en wat er nog
komt) legt de machinelaag vast — prompts, tool-calls, gewijzigde regels — en hangt die aan
commits, via een 12-tekens id in een `Entire-Checkpoint`-trailer. Deze skill legt de menslaag
vast: waarom, en wat er bewust bleef liggen. Die twee zijn alleen samen te brengen als beide
naar dezelfde commits wijzen.

Dus: `commits` en `entire-checkpoints` vul je in als ze er zijn, en laat je leeg als ze er niet
zijn. Nooit benaderen, nooit "ongeveer deze periode". Een verkeerde SHA is erger dan een lege.

Wat deze skill **niet** doet: de sessie machinaal reconstrueren. Geen transcript-analyse, geen
samenvatting van tool-gebruik, geen tokens-per-stap. Die laag hoort bij de checkpoint-tooling.

Die machinale laag hoort nu bij `ceda-reflect`: correcties, toolfouten en afgewezen tool-calls
landen als `agent-observaties-*.md` in dezelfde data-repo, met dezelfde frontmatter-sleutels.
Beide bestanden wijzen naar dezelfde commits, dus ze zijn achteraf samen te brengen. Zie
`cedanl/ceda-skills-library`, `plugins/ceda-reflect/`.

## Let op: het tokengetal dekt één sessie, niet één werkdag

Het script telt het nieuwste transcript van deze werkdirectory op — dus de lopende sessie.
Heeft iemand vandaag in drie sessies aan hetzelfde project gewerkt en kijkt iemand in de
derde, dan staan alleen de tokens van die derde in de frontmatter.

Dat is geen defect, maar wel iets om niet verkeerd op te tellen bij analyse. Het veld
`sessie-id` staat er daarom bij: daarmee is achteraf vast te stellen welke sessie het was en
of er andere naast liepen.

En: verzin nooit een getal. Geen transcript = nullen, niet een schatting. Een verzonnen
verbruik in een data-repo is jarenlang terugleesbaar als feit.

## Let op: `gh api --method PUT` schrijft base64, en overschrijft stil

Twee dingen gaan hier mis:

- **De content moet base64 zijn, zonder regeleindes.** Op macOS is dat `base64 -i <bestand> | tr -d '\n'`, op Linux `base64 -w0 <bestand>`. Vergeet je `tr`, dan komt er een bestand aan dat GitHub weigert of stuk opslaat.
- **Met een `sha`-parameter overschrijft de PUT het bestaande bestand.** Geef die dus nooit mee. Krijg je `422 Invalid request — "sha" wasn't supplied`, dan bestaat het pad al: kies een suffix, niet de sha.

`gh` draait in deze omgeving buiten de sandbox, met `unset GITHUB_TOKEN` ervoor — zie
`branch-pr`.

## Let op: de data-repo is privé, en dat is geen vrijbrief

`cedanl/repo-context-as-data` is privé, dus een eerlijke terugblik mag er echt in staan. Wat er
alsnog niet in hoort:

- inhoud uit bronsystemen: studentgegevens, DUO-leveringen, tokens, wachtwoorden
- oordelen over met naam genoemde collega's — herformuleer naar het proces ("de overdracht
  liep stroef"), niet naar de persoon

Twijfel je bij een passage, laat 'm in het concept staan en vraag er expliciet naar. Niet
stilletjes weglaten — dan verdwijnt de scherpte die de terugblik waardevol maakt.

## Verificatie

`ceda-verifies: measurable` — de terugblik is weggeschreven als dit exit 0 geeft en het pad
teruggeeft dat je in stap 7 rapporteerde:

```bash
gh api "repos/cedanl/repo-context-as-data/contents/data/$(date +%F)/<repo>/sessie-terugblik-<naam>.md" --jq .path
```

En inhoudelijk: de frontmatter draagt elke sleutel uit stap 4, `commits` bevat twee volledige
SHA's of is leeg, en de vier secties staan er met de woorden van de gebruiker, niet
geparafraseerd.

## Gebundelde bestanden

- `references/vragenset.md` — lees altijd, bij stap 3: de vier vragen, waarom ze zo staan, en
  hoe je doorvraagt bij een dun antwoord
- `scripts/sessie-tokens.py` — draaien, niet lezen: telt het verbruik van de lopende sessie op
  en print het als YAML voor de frontmatter

## Important

- Deze skill stelt vragen en legt antwoorden vast. Hij lost niets op: een probleem dat uit de
  terugblik komt wordt een regel in `## Acties`, geen commit in deze sessie.
- Veronderstel geen technische kennis bij de gebruiker. Draai zelf de git-commando's, gebruik
  geen jargon in de vragen, en vraag hem nooit iets in een terminal te typen behalve `/cost`.
- Verander de vragenset niet per sessie. Terugblikken zijn alleen vergelijkbaar over de tijd als
  de vragen hetzelfde blijven; een betere vraag hoort in `references/vragenset.md`, in een PR.
- Schrijf niets naar de projectrepo — geen `reflectie.md`, geen commit daar. De terugblik leeft
  in de data-repo, naast de andere contextsnapshots van dat project.
- Raak `metadata.json` in de data-repo niet aan. Die wordt door
  `scripts/collect_repo_context.py` gegenereerd; met de hand bijwerken loopt uit de pas met de
  volgende snapshot.
