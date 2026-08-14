# Waarom het model is zoals het is

De skill zelf zegt *wat* de indeling is. Dit bestand zegt *waarom*, en vooral: welke
alternatieven zijn afgevallen en waarom. Lees het als je het model wil wijzigen of als een
regel arbitrair aanvoelt — de kans is groot dat er een geval achter zit.

## Geen apart agent-object

Er is Claude die een workflow-skill volgt. Spawnt die subagents, dan is dat nog steeds
Claude-die-instructies-volgt. Een aparte laag "agent" toevoegen zou suggereren dat er een
handelend ding bestaat naast de instructies, en dat is er niet. Wat isolatie wél verandert is
*wat het ding kan* — daarom is het een as (`execution`), geen laag.

Carlos Perez hanteert dezelfde drie lagen maar andere woorden: hij noemt onze workflow-skill
een *agent* en reserveert *skill* voor wat wij reference noemen ("passive: they don't decide
when to fire"). Structureel zitten we op hetzelfde model. Zijn tier-model voor onvertrouwde
inhoud (reader / orchestrator / resolver) hebben wij niet — zie de tools-as.

## Herkomst in plaats van een domein-indeling

Workflows classificeren naar wat ze inhoudelijk doen levert een lijst die eindeloos groeit en
nooit klopt. Naar herkomst indelen levert twee dingen op die wél iets doen:

- `extended` dwingt je de bron te benoemen (`upstream:`), waarmee periodiek bijwerken mogelijk
  wordt: verandert upstream, dan weet je wat je moet heroverwegen.
- `own` wordt een signaal. Staat er `own` terwijl er een bekende generieke variant bestaat,
  dan is dat een beslissing die zichzelf zichtbaar maakt.

Of de opinionering over het domein of over de methode gaat, maakt niet uit — het is dezelfde
handeling: iets generieks lokaal aanscherpen. Daarom staat `origin` op elke skill, ook op
references.

## Binding is een eigenschap van een paar

De verleiding is om een harde norm in een skill te zetten met veel hoofdletters. Dat werkt
niet: een skill kan niets tegenhouden. Splits daarom in drieën — de reference draagt de norm,
de rationale en het meetcommando; de hook draagt de afdwinging; de evaluatie draagt de
uitkomst. De skill blijft leesbaar en beargumenteerd, de hook blijft dom en hard.

Vandaar de praktische regel: `binding: hard` is alleen geldig met een `activation: hook`
-tegenhanger. Zonder is het `default` met een mooie titel.

**Fragiel is niet hard.** Een stap kan dwingend geformuleerd moeten worden zonder dat er iets
af te dwingen valt — "draai exact deze migratiesequentie, voeg geen vlaggen toe". Dat is de
juiste toon voor een breekbare operatie, en de bronnen bevelen het expliciet aan. Zulke
stappen krijgen `binding: default` plus een expliciete reden waaróm afwijken hier misgaat. De
reden is wat het model laat generaliseren naar gevallen die je niet hebt voorzien; een kale
hoofdletter-imperatief doet dat niet.

## User is geen scope

Org en project gaan over *waar het werk staat*; user gaat over *wie het doet*. Dat zijn twee
assen, en ze in één precedentieketen persen dwingt conflicten af die er niet zijn: "schrijf
kort" (user) en "gebruik Polars" (project) raken elkaar nergens.

User-voorkeuren zijn een laag die *componeert*, geen scope-waarde die overschrijft. Daaruit
volgt de regel dat user-scope uitsluitend `presentation` draagt: is een persoonlijke voorkeur
eigenlijk een conventie, dan hoort hij bij de org of het project, niet bij de persoon. En dat
is machinaal te controleren.

Waar user en project wél botsen is altijd hetzelfde geval: presentation tegen knowledge met
`binding: hard`. Daar wint de knowledge-norm. Dat is de enige uitzondering die je hoeft te
onthouden.

## Isolatie is niet gratis

`execution: isolated` kost een extra contextvenster en een ronde heen en weer. Het verdient
zich terug als de output *comprimeert* — zeven review-agents die elk één oordeel teruggeven.
Heeft de hoofdcontext het resultaat integraal nodig, dan betaal je de isolatie zonder de
winst.

## Tools zijn een aparte as, en geen sandbox

`execution` zegt wáár iets draait, `allowed-tools` zegt wát het mag. Samen beantwoorden ze
"wat kan dit ding aanrichten". Een `isolated` subagent met schrijfrechten is gevaarlijker dan
een `inline` skill die alleen leest.

Twee redenen dat deze as bestaat. Ten eerste is `allowed-tools` — naast `name` en
`description` — het enige veld dat de coding agent zélf leest; de rest van ons schema is
inert tot de validator draait. Ten tweede is dit waar `origin: external` een prijskaartje
krijgt: een overgenomen skill draait met de rechten die jij toestaat, niet met de rechten die
de auteur wenste.

Let op wat het niet is: een voorafgaande toestemming, geen sandbox. Echte begrenzing komt uit
de permissieregels van de runtime. De lijst maakt de bedoeling zichtbaar en beperkt de schade
bij een skill die je niet zelf hebt geschreven — hij vervangt geen audit.

## Waarom `source` nooit leeg mag

Leeg betekent tegelijk "geen bron" en "nog niet ingevuld", en een validator kan die twee niet
onderscheiden. `self` is daarom een expliciete claim, met een consequentie: is de skill de
bron, dan mag dezelfde inhoud nergens anders staan — geen wiki-pagina, geen README-sectie,
geen Notion. Anders heb je de drift terug, alleen omgekeerd. Vandaar: `source: self` ⇒
org-scope, en wijzigen gaat via review.

Zonder deze verwijzing drift een reference ten opzichte van z'n bron en ontstaan er stille
varianten die niemand samenvoegt. Het duplicaat `vormgever-npuls-huisstijl` / `-2` is precies
die failure mode.

**Bewust niet toegevoegd:** een `source_checked`-datum met een validator die klaagt na N
maanden. Bij een externe url is drift niet machinaal te detecteren, dus zou je onderhoud
verzinnen dat niemand doet. Pas toevoegen als drift zich daadwerkelijk voordoet.

## Waarom verificatie twee vormen heeft

Ruwweg de helft van de CEDA-collectie is expressief (`sparren`, `brainstorm`, `vormgever`,
`write-issue`). Eén numerieke vorm daarop afdwingen levert lege KPI-blokken of verzonnen
getallen, en allebei zijn erger dan niets. De observable vorm dwingt dezelfde discipline af —
*waaraan zie ik dat dit goed ging* — zonder een getal te fingeren.

## Waarom evaluatie buiten de skill staat

Org-scope skills worden via `npx skills add cedanl/.github` **gekopieerd** naar elke repo. Een
waarneming die naast een kopie belandt, komt nooit terug bij de bron: N divergerende bestanden
en een basis die niet leert. Daarom drie stappen — observatie, destillatie *per skill over
alle repo's heen*, en een wijzigingsvoorstel op de bron-skill — en daarom zijn `ceda-id` en
`ceda-version` geen administratie maar randvoorwaarde: zonder stabiele identiteit is niet vast
te stellen dat waarnemingen uit acht repo's over dezelfde skill gaan.

Bijvangst: een waarneming die in géén enkele bestaande skill past, is de signalering van een
*ontbrekende* skill. De evaluatie is daarmee ook de lacune-detector.

## Splitsen kost ook iets

De splitsen-toets kijkt of er een zinnige stappenreeks overblijft als je de
organisatiespecifieke kennis eruit haalt. Maar te smal gesneden skills dwingen er meerdere
tegelijk te laden voor één taak: meer context, meer descriptions die om activatie
concurreren, en het risico dat twee skills elkaar tegenspreken. Bundelen is goedkoper dan
splitsen — een bundle heeft geen eigen description die meedingt.

Kandidaten om te splitsen: `simplify-ceda`, `check-style`, `write-issue`, `release-notes`,
`init-repo`. Kandidaten om te laten: `sam-uren-cowork-mac`, `sdp-onboard`,
`generate-slides-retro` — daar zijn de schermen, de flow en de veldnamen de stappen.

## Waarom chain-edges niet in de skill wonen

Een externe skill kan geen chain naar een CEDA-skill declareren: je bezit z'n frontmatter
niet. En conceptueel is "A draait na B" een lokale compositiebeslissing, geen eigenschap van A
of B. Dus horen edges in CLAUDE.md of in een org-/project-manifest. Dat houdt externe skills
ongewijzigd bruikbaar, wat de voorwaarde is voor extern-eerst.

Twee regels, anders loopt het vast: één richting (generiek → specifiek, anders cycli) en
begrensde diepte (chaint elke brede workflow er drie lokale bij, dan trekt één aanroep
stilletjes veel context binnen).

## Bronnen

- Anthropic — *Equipping agents for the real world with Agent Skills*:
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Agent Skills — *Specification*: https://agentskills.io/specification
- Agent Skills — *Skill Creation: Best Practices*:
  https://agentskills.io/skill-creation/best-practices
- Agent Skills — *Skill Creation: Evaluating Skills*:
  https://agentskills.io/skill-creation/evaluating-skills
- Carlos Perez — *Structuring Agents, Skills, and MCPs*:
  https://medium.com/intuitionmachine/structuring-agents-skills-and-mcps-best-practices-from-anthropic-9312849ccea6
- Generative Programmer — *Skill Authoring Patterns from Anthropic's Docs*:
  https://generativeprogrammer.com/p/skill-authoring-patterns-from-anthropics

Intern: `cedanl/ceda-workshop-starter` (KPI-blokken per skill, hooks voor afdwinging,
subagents voor review — bron van de binding-splitsing en de execution-as),
`docs/skill-gaps.md` (gap-analyse van de collectie tegen dit model),
`cedanl/.github#49` (openstaande stappen), `cedanl/project_algemeen#41` (kennisarchitectuur,
zelfde bronze/gold-patroon op grotere schaal).
