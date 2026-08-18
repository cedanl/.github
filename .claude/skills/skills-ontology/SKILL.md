---
name: skills-ontology
description: Draagt het CEDA-model om skills, commands, hooks en connectors te classificeren — drie lagen (workflow, reference, connector), vijf assen (activation, binding, scope, execution, tools), het frontmatter-schema en de regels voor descriptions, progressive disclosure en verificatie. Gebruik wanneer iemand vraagt wat voor soort skill iets is, of iets een skill/hook/connector/command moet zijn, wat een veld in de frontmatter betekent, of een skill gesplitst moet worden, waarom een skill niet triggert, of "skills ontologie", "skill type", "skill classificeren", "skill taxonomy" noemt. LET OP — moet er daadwerkelijk een skill geschreven, herzien of gevalideerd worden, gebruik dan `create-skill`; die laadt deze kennis zelf.
allowed-tools: Read Grep Glob
metadata:
  ceda-id: ceda.skills-ontology
  ceda-version: "1.0.0"
  ceda-type: reference
  ceda-subtype: knowledge
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: self
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Skills Ontology CEDA

Het model waarmee CEDA skills classificeert — en waarmee je voorspelt *wanneer* elk ding
laadt. Deze skill **is** de bron: er is geen document ernaast, en dat is met opzet, want twee
bronnen voor hetzelfde model geven precies de drift die dit model elders bestrijdt.

## Wanneer dit geldt

Reference-skill, geen procedure. Laadt wanneer je iets moet indelen, benoemen of beoordelen
in het skill-landschap: is dit een skill of een hook, welk `type`, hoort dit gesplitst,
waarom vuurt deze skill niet, wat betekent dit frontmatter-veld.

## De kernvraag

Niks activeert zichzelf (op chaining na); de trigger komt altijd van buiten. Het verschil zit
in de *inhoud*. Vraag bij elk ding: **bevat het een stappenreeks of beslislogica?**

| Laag | Bevat | Voorbeeld |
|---|---|---|
| **workflow** | stappenreeks / beslislogica | `ship`, `simplify-ceda`, `create-skill` |
| **reference** | kennis, regels, stijl, persona — geen sequentie | R/Python-conventies, brandbook, doelgroep-toon |
| **connector** | data of tools via een protocol | MCP-connector, REST API |

Er is geen apart handelend "agent"-object. Er is Claude die een workflow volgt. Spawnt die
subagents, dan is dat nog steeds Claude-die-instructies-volgt — dat verschil zit op de
execution-as.

### Reference: twee subtypes

Scheidslijn is één vraag: verandert dit *wat* Claude weet, of *hoe* Claude formuleert?

| `subtype` | Bevat | Voorbeeld |
|---|---|---|
| `knowledge` | wat waar is over domein, org of code | conventies, glossary, wie-is-wie |
| `presentation` | hoe de output eruitziet: toon, jargon, lengte, format | `kort`, `caveman`, `bestuurder`, `docent` |

Zo delen professionals dezelfde `knowledge` en onderscheiden ze zich op `presentation`.

Wat géén subtype is: een conventie (dat is `knowledge` met een waarde op de binding-as), een
meegeleverd bestand (dat is verpakking, zie de bundle-sectie), een doelgroep (dat is een parameter
in de skill, geen typenaam).

## De vijf assen

Elk ding krijgt een waarde op elke as. Assen voorkomen oneindige rijen types.

**Activation — wat triggert het?** `ambient` (model beslist op relevantie) · `command` (mens
typt `/naam`) · `hook` (runtime-event) · `scheduled` (cron/headless) · `chained` (andere
workflow roept aan). Command en hook zijn dus geen types maar punten op deze as.

**Binding — hoe hard?** `hard` (niet onderhandelbaar) · `default` (normale werkwijze, mag van
afgeweken) · `suggestie` (hint). Binding is een eigenschap van een *paar*, niet van één
object: de reference draagt de norm, de rationale en het meetcommando; de hook draagt de
afdwinging; de evaluatie draagt de uitkomst. Praktische regel: `binding: hard` is alleen
geldig als er een `activation: hook`-tegenhanger bestaat — anders is het `default` met een
mooie titel. **Fragiel is niet hard**: "draai exact deze migratiesequentie" hoort dwingend
geformuleerd, maar krijgt `default` plus een expliciete reden waaróm afwijken hier misgaat.

**Scope — waar staat het werk?** `org` (gedeeld via `cedanl/.github`) · `project` (quirk van
dít project). Conflictregel: lokaler wint. `user` staat *niet* op deze as — dat gaat over wie
het doet, niet waar het werk staat. User-voorkeuren componeren als laag en dragen uitsluitend
`subtype: presentation`, nooit `knowledge`. Botsen ze toch, dan wint een knowledge-norm met
`binding: hard`.

**Execution — hoe draait het?** `inline` (hoofdcontext) · `isolated` (subagent met eigen
venster) · `deterministic` (script of hook, geen model in de lus). `isolated` is niet gratis:
kies het als de output *comprimeert*, niet als de hoofdcontext het resultaat integraal nodig
heeft.

**Tools — wat mag het aanraken?** `allowed-tools` is voorafgaande toestemming, geen sandbox.
Review-skill → `Read, Grep, Glob`. Documentatiegenerator → `Read, Write`. Deploy → `Bash` met
een nauwe matcher. Dit is ook de plek waar `origin: external` een prijskaartje krijgt: een
overgenomen skill draait met de rechten die jij toestaat, niet die de auteur wenste.

## Herkomst en bron

Twee verschillende vragen, allebei een veld:

| Veld | Antwoordt | Verwijst naar |
|---|---|---|
| `origin` | wie schreef dit *skill-artefact* — `external` / `extended` / `own` | een **skill** (via `upstream:` bij `extended`) |
| `source` | waar staat de bron van waarheid *buiten* de skill | een **document**: pad, url of `self` |

Ze zijn orthogonaal: een `own` skill kan een externe bron hebben, een `extended` skill kan
`source: self` zijn.

De waarde van `origin` zit in `extended` — dat dwingt je de bron te benoemen, waarmee
periodiek bijwerken mogelijk wordt. En `own` wordt een signaal: staat er `own` terwijl er een
bekende generieke variant bestaat, dan is dat een beslissing die zichzelf zichtbaar maakt.
Werkvolgorde is dus **extern eerst, opinioneren als tweede stap**.

`source` nooit leeg laten: leeg betekent tegelijk "geen bron" en "nog niet ingevuld", en een
validator kan die twee niet onderscheiden. `self` is een expliciete claim, met consequentie:
dan mag dezelfde inhoud nergens anders staan — geen wiki, geen README-sectie — en de skill
hoort op `scope: org` met wijziging via review. Het duplicaat `vormgever-npuls-huisstijl` /
`-2` is precies de failure mode die hiermee wordt afgevangen.

## Waar dit alles in de frontmatter landt

De Agent Skills-specificatie kent **zes** velden en verder niets: `name`, `description`,
`license`, `compatibility`, `metadata`, `allowed-tools`. Eigen velden horen onder `metadata:`,
een map van string naar string, met een prefix tegen botsingen. Bij ons dus `ceda-type`,
`ceda-subtype`, `ceda-origin`, `ceda-upstream`, `ceda-source`, `ceda-activation`,
`ceda-binding`, `ceda-execution`, `ceda-scope`, `ceda-verifies`, `ceda-id`, `ceda-version`.

Drie dingen waar mensen op struikelen:

- `name` moet 1-64 tekens zijn, alleen `a-z`, `0-9` en losse streepjes, en **gelijk aan de
  directorynaam**. Underscores zijn ongeldig.
- `allowed-tools` is een spatie-gescheiden **string**, geen YAML-lijst: `Read Grep Glob`.
- Een CEDA-veld op topniveau is off-spec en wordt door andere agents genegeerd.

Het volledige schema met beslisregels staat in
`.claude/skills/create-skill/references/frontmatter-schema.md`; `validate-skill.py` in
diezelfde skill controleert het.

## De description: het enige veld dat activeert

Alle assen hierboven *beschrijven* een skill. Precies één veld laat hem afgaan. De
description staat bij elke sessie in de systeemprompt, van álle skills tegelijk; de rest van
de skill bestaat op dat moment nog niet. Een uitstekende skill met een vage description vuurt
nooit.

Vijf eisen: derde persoon met de woorden die de gebruiker letterlijk typt (productnamen,
systeemnamen, foutmeldingen — ook "als hij alleen output plakt zonder vraag") · een
exclusion-clause · max 1024 tekens, hard begrensd door de spec · geschreven in de taal waarin
de triggers gesteld worden, zonder verzonnen vertalingen ernaast · niet tijdsgebonden. Bij
twijfel iets te opdringerig formuleren; onder-triggeren is vaker het probleem.

**De exclusion-clause heeft twee vormen**, en de tweede wordt het vaakst vergeten:

- **verwijzend** — een andere skill hoort hier te vuren: "gaat het om sorteren en top-N,
  gebruik `voorspellen-ranking`".
- **begrenzend** — géén skill hoort hier te vuren, want buiten dit domein gelden de aannames
  niet: "niet voor Helm of Flux buiten SDP; zonder Harbor en een GitLab-SDP-pipeline kloppen
  deze conventies niet". Toets: kan iemand met een *vergelijkbaar maar ander* systeem deze
  skill per ongeluk binnenhalen? Dan hoort deze vorm erin.

De clause is onderhoudswerk: voeg je een skill toe die overlapt met een bestaande, dan hoort
de description van de *bestaande* skill in dezelfde PR mee te veranderen.

## Progressive disclosure: drie laadniveaus

| Niveau | Wat laadt | Wanneer |
|---|---|---|
| 1 | `name` + `description` van elke skill | altijd, elke sessie |
| 2 | de body van `SKILL.md` | zodra de skill triggert |
| 3 | gebundelde bestanden (`references/`, `scripts/`, `assets/`) | alleen op instructie uit niveau 2 |

Richtlijn: `SKILL.md` onder de 500 regels / 5.000 tokens. Elke bundle draagt een
laadconditie — "lees `references/api-errors.md` als de API iets anders dan 200 teruggeeft"
werkt, "zie references/ voor details" niet. Graaf ondiep houden: één hop vanaf `SKILL.md`.

Die conditie hoort **in de body**, in een `## Gebundelde bestanden`-sectie. De spec kent geen
frontmatter-veld voor bundles, en het zou ook niet helpen: de agent leest de body, niet de
metadata. Een bestand dat nergens in de body genoemd wordt, laadt nooit.

Een gebundeld script kost alleen z'n *output* aan context, niet z'n broncode. Verzint het
model bij herhaald gebruik telkens dezelfde hulplogica, dan is dat het signaal om het één
keer te schrijven en te bundelen.

## Verificatie versus evaluatie

| | Meet | Wanneer | Onderwerp |
|---|---|---|---|
| `verifies:` | is het werk goed | elke run | het artefact |
| baseline-eval | is de skill beter dan géén skill | bij schrijven of wijzigen | de skill |
| evaluatie | helpt de skill iemand | over de tijd | het gebruik |

`verifies: measurable` = een commando plus een drempel (feitelijk werk). `verifies:
observable` = een checklist van wat waar moet zijn na afloop, beoordeeld door mens of
subagent (expressief werk: sparren, brainstorm, vormgeven). `none` mag, maar alleen met
motivatie in de skill zelf. De skill draagt de norm en de meetmethode; de gemeten uitkomst
hoort er niet in — die gaat naar de evaluatie, buiten de skill, omdat org-skills naar elke
repo gekópieerd worden en een waarneming naast een kopie nooit terugkomt bij de bron.

## Patronen

**Splitsen — workflow los van reference.** Haal de organisatiespecifieke kennis eruit en zet
'm in een reference. Blijft er een zinnige stappenreeks over → splitsen; de workflow wordt
draagbaar, de reference wisselbaar. Valt de sequentie uit elkaar → laten staan, de stappen
zélf zijn organisatiespecifiek. Splitsen kost ook iets: te smal gesneden skills dwingen er
meerdere tegelijk te laden, met meer context en meer descriptions die concurreren.

**Chaining — houd het generieke schoon, laat het specifieke aan de rand hangen.** Eén
richting (generiek → specifiek, anders cycli) en begrensde diepte. Edges wonen niet in de
skill maar in CLAUDE.md of een manifest: je bezit de frontmatter van een externe skill niet,
en "A draait na B" is een lokale compositiebeslissing.

**Eén info, meerdere doelgroepen.** Content in één canonieke knowledge-reference; per
doelgroep een presentation-reference (toon, jargon, zorgen, lengte); een workflow "render
voor doelgroep X" met de doelgroep als argument. Content DRY, doelgroep-versies afgeleid in
plaats van opgeslagen.

**Diagnose: kennis die een procedure is.** Bij troubleshooting valt de scheiding tussen
workflow en reference weg — de kennis *is* "in situatie X doe Y". Dat blijft `reference` +
`knowledge`, geen nieuw subtype, maar wel een erkende vorm: oriëntatie mét instructie →
mentaal model → benoemde valkuilen → de dubbelzinnige gevallen (zelfde symptoom, tegengestelde
actie) → conventies → symptoom-tabel → gebundelde bestanden → recap. Twee dingen daaruit
gelden overal: een kop noemt het feit en niet de categorie, en een symptoom-tabel
(`symptoom | oorzaak | eerste actie`) is de dichtste vorm die er is. Voorbeelden:
`surf-sdp-helm-flux`, `sdp-secrets-management`.

**Taste is geen laag.** Judgment is een *kwaliteit* van een workflow (wanneer stoppen, wat
"goed" is) of van een reference (welke default) — geen eigen rij.

## Verbinden met projecten

Drie inhaakpunten per repo: de marketplace (gedeelde skills in elke sessie), `repo/.claude/`
(project-scoped, gedeeld via git) en `repo/CLAUDE.md` (de altijd-aan laag die de rest
dirigeert). Wél in CLAUDE.md: projectfeiten die niet te raden zijn, *pointers* naar
conventies, afwijkingen van de default. Niet in CLAUDE.md: de inhoud van standaarden of
workflows — CLAUDE.md dirigeert, dupliceert niet.

## Gotchas

- **De bestaande CEDA-skills dragen alleen `name` en `description`.** Het schema hierboven is
  vastgesteld maar nog niet uitgerold; ga er niet van uit dat een willekeurige skill deze
  velden heeft.
- **"Kennis" is oude terminologie.** Skills van vóór dit model gebruiken de types Actie /
  Review / Generatie / Wizard / Kennis. Vertaal: de eerste vier zijn `type: workflow`,
  "Kennis" is `type: reference` + `subtype: knowledge`.
- **Perez' woordkeus verschilt van de onze.** In dat artikel heet onze workflow-skill een
  *agent* en is *skill* gereserveerd voor wat wij reference noemen. Structureel hetzelfde
  model, andere labels.

## Gebundelde bestanden

- `references/rationale.md` — lees wanneer je het model wil wijzigen, of wanneer een regel
  hierboven arbitrair aanvoelt: waarom deze indeling, welke alternatieven zijn afgevallen, en
  de bronnen

## Important

- **Deze skill is de bron** (`ceda-source: self`). Wijzigingen aan het model landen hier, via
  review; zet dezelfde inhoud niet ook in een document of een wiki, want dan is de drift
  terug. De openstaande stappen om het model op de collectie toe te passen staan in
  `cedanl/.github#49`.
- Deze skill classificeert en legt uit. Voor het schrijven, herzien of valideren van een
  skill: `create-skill`.
