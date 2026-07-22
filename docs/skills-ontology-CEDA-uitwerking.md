# Skills Ontology CEDA

Een model om skills en connectors te classificeren — en om te voorspellen *wanneer* elk ding laadt.

## Kernvraag: bevat het een stappenreeks?

Niks activeert zichzelf (op chaining na); de trigger komt altijd van buiten. Het verschil zit in de *inhoud*.

Vraag bij elk ding: **bevat het een stappenreeks of beslislogica?**

- Ja → workflow-skill (de stappen; Claude leest en volgt ze)
- Nee, injecteert kennis/regels/etc → reference-skill
- Levert data of tools via protocol → connector

Er is geen apart handelend "agent"-object. Er is Claude die een workflow-skill volgt. Spawnt die subagents, dan is dat nog steeds Claude-die-instructies-volgt — zie de execution-as, want isolatie verandert wél wat het ding kan.

## De drie lagen (functie)

| Laag | Bevat | Voorbeeld |
|---|---|---|
| **Workflow-skill** | stappenreeks / beslislogica | gl-reconciler, simplify-ceda, GSD |
| **Reference-skill** | kennis / regels / stijl / persona, geen sequentie | R/Python-conventies, code-voorbeelden, lettertypes, mindset (doelgroep) |
| **Connector** | data of tools via protocol | MCP-connector, REST API |

Deze drie lagen beschrijven wat er in context geladen wordt. Wat er *uit* het gebruik terugkomt — waarnemingen, meetuitkomsten, gebruikersoordelen — hoort hier niet bij; zie de evaluatie verderop.

### Workflow-skill — herkomst

Bevat de stappenreeks. Wordt van buiten getriggerd (zie activation-as); beslist alleen de *interne* volgorde zodra hij draait. De enige interne activatie is **chaining**: een workflow-skill die een sub-workflow aanroept.

**Gotcha's horen hier, niet in een losse reference.** Een gotcha is een omgevingsfeit dat een redelijke aanname tegenspreekt — "de `users`-tabel gebruikt soft deletes, dus filter op `deleted_at IS NULL`". Het is per definitie iets waarvan je niet wéét dat je het nodig hebt. Een gotcha die achter een conditie hangt ("lees `references/valkuilen.md` als je tegen X aanloopt") werkt daarom niet: X herkennen ís het probleem.

Regel: gotcha's staan in de workflow-skill zelf, of in een reference die de workflow **onvoorwaardelijk** laadt (`load: always`). Nooit conditioneel. Elke correctie die je tijdens gebruik moet geven, hoort erbij — dat is de goedkoopste manier om een skill te verbeteren.

Workflows worden niet geclassificeerd naar wat ze inhoudelijk doen, maar naar **herkomst**: waar komen ze vandaan en wat maakt ze lokaal.

| `origin` | Betekenis |
|---|---|
| `external` | generieke skill, ongewijzigd gebruikt (GSD, Superpowers) |
| `extended` | externe basis plus onze opinionering; `upstream:` verplicht |
| `own` | geen generiek equivalent; zelf geschreven |

De waarde zit in `extended`. Die dwingt je de bron te benoemen, waarmee periodiek bijwerken mogelijk wordt: verandert upstream, dan weet je wat je moet heroverwegen. En `own` wordt een signaal — staat er `own` terwijl er een bekende generieke variant bestaat, dan is dat een beslissing die zichzelf zichtbaar maakt.

Of de opinionering nu over het domein of over de methode gaat, maakt niet uit. Het is dezelfde handeling: iets generieks lokaal aanscherpen. Om die reden staat `origin` niet alleen op workflows maar op elke skill — ook een reference van een ander team kun je overnemen en aanscherpen.

**Werkvolgorde: extern eerst, opinioneren als tweede stap.** Zoek of er een generieke skill bestaat voordat je zelf schrijft. Dit hoort als verplichte eerste stap in `create-skill`; `ceda-workshop-starter` heeft er met `find-skills` al gereedschap voor.

### Reference-skill — subtypes

Passieve kennis die het model inleest wanneer relevant. Twee subtypes, en de scheidslijn is één vraag: **verandert dit ding *wat* Claude weet, of *hoe* Claude formuleert?**

| `subtype` | Bevat | Voorbeeld |
|---|---|---|
| `knowledge` | wat waar is over domein, org of code — feiten, glossary, conventies | R/Python-conventies, wie-is-wie, brandbook |
| `presentation` | hoe de output eruitziet — toon, jargon-niveau, zorgen, lengte, format | `kort`, `caveman`, `bestuurder`, `docent` |

Hiermee kunnen professionals zichzelf onderscheiden op `presentation`, terwijl ze dezelfde `knowledge` delen. Dat is het hele punt van de scheiding — zie het doelgroep-patroon verderop.

Let op wat géén subtype is. Een conventie is `knowledge` met een waarde op de binding-as, geen eigen soort. Een meegeleverd bestand (brandbook, template) is verpakking — het veld `bundles:` helpt als laadmechanise. Het is geen skill op zichzelf. Ook doelgroep-parameters horen in de skill zelf, niet in de typenaam.

#### Herkomst en bron: twee verschillende dingen

Reference-skills dragen `origin` net als workflows — een reference van een ander team dat wij aanscherpen is straks het interessante geval, en dan moet het veld er al zijn. In de praktijk staat er meestal `own`; de waarde zit in de zeldzame waarde.

Daarnaast een tweede veld, want "wie schreef dit artefact" en "waar staat de waarheid" zijn niet hetzelfde:

| Veld | Antwoordt | Verwijst naar |
|---|---|---|
| `origin` | wie schreef dit *skill-artefact* | een **skill** (via `upstream:` bij `extended`) |
| `source` | waar staat de bron van waarheid *buiten* de skill | een **document**: pad of url — of `self` |

Ze zijn orthogonaal. Een `own` skill kan een externe bron hebben (jij schrijft een reference over een textbook). Een `extended` skill van een ander team kan `source: self` zijn.

Drie soorten bron:

- **extern** (`source: https://…`) — een textbook, een leverancierspagina, upstream-documentatie.
- **intern** (`source: docs/ceda-python.md`) — een eigen document dat de skill samenvat.
- **de skill zelf** (`source: self`) — er ís geen ander document. Waarom zou je iets "normaal documenteren" als je er direct een skill van kunt maken?

**Laat het veld nooit leeg.** Leeg betekent "geen bron" én "nog niet ingevuld" tegelijk; de validator kan die twee niet uit elkaar houden. `self` is een expliciete claim.

**En die claim heeft een consequentie.** Is de skill de bron, dan mag dezelfde inhoud nergens anders staan — geen wiki-pagina, geen README-sectie, geen Notion. Anders heb je de drift terug, alleen omgekeerd. Regel: **`source: self` ⇒ org-scope, en wijzigen gaat via review.**

Zonder deze verwijzing drift een reference ten opzichte van z'n bron en ontstaan er stille varianten die niemand samenvoegt. Het duplicaat `vormgever-npuls-huisstijl` / `-2` is precies die failure mode.

Nog niet toegevoegd: een `source_checked:`-datum met een validator die klaagt na N maanden. Bij een externe url is drift immers niet machinaal te detecteren. Eerst `source` uitrollen; het veld pas erbij als drift zich daadwerkelijk voordoet — anders verzin je onderhoud dat niemand doet.

### Connector

Levert data en tools via een protocol. **MCP = het protocol, connector = het archetype dat het implementeert.** Tool usage valt hier ook onder. Een API is een connector zonder MCP-laag, die bijv. via de cli aanroepbaar is. Connectoren kunnen verschillende mogelijkheden hebben, veel connectoren lezen alleen uit (data access), maar er zijn ook connectors die het mogelijk maken om externe zaken te veranderen (write access).

---

## De vijf assen (orthogonaal, over alle lagen)

Assen voorkomen oneindige rijen. Elk ding krijgt een waarde op elke as.

### Activation — wat triggert het?

| Waarde | Trigger | Voorbeeld |
|---|---|---|
| ambient | model beslist, automatisch | reference vuurt op relevantie |
| command | mens typt `/naam` | `/dcf`, `/gsd:new` |
| hook | runtime-event | pre-commit, PreToolUse |
| scheduled | cron/headless | managed agent op cron |
| chained | andere workflow roept aan | brede workflow start lokale workflow |

Command en hook zijn geen eigen types — punten op deze as. Een command is een workflow/skill met handmatige trigger. Een hook is een constraint op het punt "afgedwongen i.p.v. geïnjecteerd".

### Binding — hoe hard?

- **hard** — niet onderhandelbaar (policy, compliance). Hoort vaak in een hook of als scheduled, niet in context.
- **default** — normale werkwijze, mag afgeweken worden. Een command kan bijv. in CLAUDE.md worden genoemd.
- **suggestie** — hint. Enkel mens die command expliciet moet typen.

Een naakte hard constraint in een skill zonder *reden* is een verkeerd geplaatste hook. Zet je 'm in een reference, geef de rationale mee.

**Binding is geen eigenschap van één object, maar van een paar.** Een knowledge-reference kan een harde, meetbare norm dragen zonder daarmee een misplaatste hook te zijn — zolang de *afdwinging* ergens anders zit. Splits het in drieën:

| Wie | Draagt |
|---|---|
| de reference-skill | de norm, de rationale, en het commando waarmee je 'm meet |
| de hook / het script | de afdwinging op een runtime-event |
| de evaluatie | de gemeten uitkomst over de tijd |

De skill blijft daarmee leesbaar en beargumenteerd, de hook blijft dom en hard.

Praktische regel: `binding: hard` is alleen geldig als er een `activation: hook`-tegenhanger bestaat. Staat die er niet, dan is het `default` met een mooie titel.

**Fragiel is niet hard.** Een stap kan dwingend geformuleerd moeten worden zonder dat er iets af te dwingen valt — "draai exact deze migratiesequentie, voeg geen vlaggen toe". Dat is de juiste toon voor een breekbare operatie, en de bronnen bevelen 'm expliciet aan. Het is alleen geen `hard`: er is geen machine die het tegenhoudt. Zulke stappen krijgen `binding: default` plus een expliciete reden waaróm afwijken hier misgaat. De reden is wat het model laat generaliseren naar gevallen die je niet hebt voorzien; een kale hoofdletter-imperatief doet dat niet.

### Scope — waar staat het werk?

- **org** — gedeeld over alle CEDA-repo's. Uitgeleverd via `cedanl/.github`.
- **project** — quirks van dít project. Gedeeld via de repo.

Conflictregel: **lokaler wint.** Project verslaat org. Org is de gedeelde default; een repo die afwijkt zegt dat lokaal, in z'n eigen CLAUDE.md. Project is daarmee een superset van org: dezelfde skills, plus projectkennis — en die projectkennis hoeft lang niet altijd een skill te zijn.

**`user` staat niet op deze as.** Org en project gaan over *waar het werk staat*; user gaat over *wie het doet*. Dat zijn twee assen, en ze in één precedentieketen persen dwingt conflicten af die er niet zijn: "schrijf kort" (user) en "gebruik Polars" (project) raken elkaar nergens.

User-voorkeuren zijn een **laag die componeert**, geen scope-waarde die overschrijft. Daaruit volgt één besliste regel:

> User-scope draagt uitsluitend `subtype: presentation`. Nooit `knowledge`.
> Is een persoonlijke voorkeur eigenlijk een conventie, dan hoort hij in org of project — niet bij de persoon.

Deze regel wordt machinaal controleerbaar: `scope: user` + `subtype: knowledge` is een fout.

Waar user en project wél botsen is altijd hetzelfde geval: presentation tegen knowledge met `binding: hard`. Daar wint de knowledge-norm. Dat is de enige uitzondering die je hoeft te onthouden.

### Execution — hoe draait het?

Contextisolatie is geen verpakking maar functie: het verandert wat een ding kán.

| Waarde | Draait als | Voorbeeld |
|---|---|---|
| **inline** | in de hoofdcontext | de meeste skills |
| **isolated** | subagent met eigen contextvenster | parallelle review-agents |
| **deterministic** | script of hook, geen model in de lus | een KPI-check, een conventie-guard |

`isolated` is niet gratis. Kies het als de output *comprimeert* — zeven review-agents die elk één oordeel teruggeven. Niet als de hoofdcontext het resultaat integraal nodig heeft; dan betaal je de isolatie zonder de winst.

Dit is ook waar de "geen agent-object"-stelling standhoudt: een subagent is nog steeds Claude-die-een-workflow-volgt, alleen met een andere executiewijze. Geen nieuwe laag, wel een aparte as.

### Tools — wat mag het aanraken?

`execution` zegt *waar* iets draait, `allowed-tools` zegt *wat het mag*. Samen beantwoorden ze de vraag "wat kan dit ding aanrichten". Ze zijn niet inwisselbaar: een `isolated` subagent met schrijfrechten op de repo is gevaarlijker dan een `inline` skill die alleen leest.

| Skill | Redelijke set |
|---|---|
| security- of stijlreview | `Read, Grep, Glob` |
| documentatiegenerator | `Read, Write` |
| deploy of migratie | `Bash` met een nauwe commandomatcher |

Twee redenen dat deze as er hoort. Ten eerste: `allowed-tools` is — naast `name` en `description` — het enige veld in ons hele schema dat de coding agent zélf leest. De rest is CEDA-metadata die pas betekenis krijgt als wij er een validator op bouwen. Ten tweede: dit is de plek waar `origin: external` een prijskaartje krijgt. Een externe skill draait met de rechten die jij toestaat, niet met de rechten die de auteur wenste.

Let op: een `allowed-tools`-lijst is een *voorafgaande toestemming*, geen sandbox. Echte begrenzing komt uit de permissieregels van de runtime. De lijst maakt de bedoeling zichtbaar en beperkt de schade bij een skill die je niet zelf hebt geschreven — hij vervangt geen audit.

---

## De description: het enige veld dat activeert

Alle assen hierboven beschrijven een skill. Precies één veld laat hem afgaan.

De description is wat de agent bij het starten van elke sessie in z'n systeemprompt krijgt — van álle skills tegelijk. De rest van de skill bestaat voor hem nog niet. De keuze "is deze skill relevant" wordt dus volledig gemaakt op één regel tekst, vóórdat er ook maar iets van de inhoud is gelezen. Een uitstekende skill met een vage description vuurt nooit; een middelmatige skill met een scherpe description doet z'n werk.

Bij 53 skills is dat geen detail meer. Overlappende descriptions maken auto-activatie onbetrouwbaar — niet doordat de verkeerde skill laadt, maar doordat er drie tegelijk laden en elkaars instructies tegenspreken.

Vier eisen:

1. **Derde persoon, met triggers.** Niet wat de skill *is* maar wanneer hij *aan moet*. Noem de woorden die een gebruiker echt typt, inclusief de Nederlandse en Engelse variant.
2. **Een exclusion-clause.** Zeg erbij wanneer je 'm *niet* gebruikt, met verwijzing naar de skill die dan wél moet vuren. Dit is de enige rem op mis-triggeren die we hebben. `voorspellen-ranking` doet dit al goed ("LET OP — als het doel is te sorteren en de top-N te selecteren, gebruik dan…"); de meeste andere niet.
3. **Binnen budget.** Circa 1024 tekens. Elke description van elke skill staat permanent in context; dit is de enige plek in het systeem waar tokens per sessie in rekening worden gebracht zonder dat de skill gebruikt wordt.
4. **Niet tijdsgebonden.** Geen "de nieuwe manier om…" — dat veroudert stil.

Bij twijfel: iets te opdringerig formuleren. Onder-triggeren is in de praktijk het vaakst het probleem, en een skill die te vaak afgaat merk je meteen.

**Consequentie voor de exclusion-clause:** die is onderhoudswerk. Voeg je een skill toe die overlapt met een bestaande, dan hoort de description van de *bestaande* skill in dezelfde PR mee te veranderen. Anders groeit de collectie en verslechtert de activatie tegelijk.

---

## Progressive disclosure: drie laadniveaus

Dit document opende met de vraag wanneer iets laadt. De assen beantwoorden dat maar half. Er zijn drie niveaus, niet twee:

| Niveau | Wat laadt | Wanneer |
|---|---|---|
| 1 | `name` + `description` van elke skill | altijd, elke sessie |
| 2 | de body van `SKILL.md` | zodra de skill triggert |
| 3 | gebundelde bestanden (`references/`, `scripts/`, `assets/`) | alleen op instructie uit niveau 2 |

De `activation`-as beschrijft de sprong van 1 naar 2. Niveau 3 is een tweede mechanisme en het is het mechanisme dat een grote skill betaalbaar maakt.

**Richtlijn:** houd `SKILL.md` onder de 500 regels / 5.000 tokens. Dat is de inhoud die je élke keer betaalt dat de skill vuurt. Alles wat je niet altijd nodig hebt, gaat naar een gebundeld bestand.

**Zeg erbij wanneer.** Een bundle zonder laadconditie wordt of altijd gelezen of nooit. "Lees `references/api-errors.md` als de API iets anders dan 200 teruggeeft" werkt; "zie references/ voor details" niet. Vandaar dat `bundles:` in het schema een conditie draagt en geen kaal pad.

**Graaf ondiep houden.** Eén hop vanaf `SKILL.md`. Een bundle die naar een bundle verwijst is een skill die zichzelf niet meer kan overzien.

**Dit is waarom splitsen werkt.** Een skill die zwaar aanvoelt heeft meestal een niveau-2 die niveau-3 werk doet. Twee uitwegen, en ze zijn verschillend: haal je organisatiespecifieke kennis eruit die *andere* workflows ook nodig hebben, dan wordt het een aparte reference-skill (zie het splitsen-patroon). Is de inhoud alleen voor deze skill relevant maar zelden nodig, dan is het een bundle — geen nieuwe skill. Bundelen is goedkoper: geen extra description die om activatie concurreert.

**Scripts zijn hetzelfde principe, scherper.** Een gebundeld script kost alleen z'n *output* aan context, niet z'n broncode. Zie je bij herhaald gebruik dat het model telkens dezelfde hulplogica opnieuw verzint, dan is dat het signaal om het één keer te schrijven en te bundelen.

---

## Verificatie: doet de skill wat hij belooft

Een skill zonder verificatie is een bewering. Verificatie zit *in* de skill en draait *tijdens* de uitvoer: het geeft Claude een manier om vast te stellen dat de stappen gelukt zijn voordat hij afrondt.

Elke skill vult `verifies:` in. Twee vormen:

| Vorm | Voor | Inhoud |
|---|---|---|
| **measurable** | feitelijk werk — code, data, infra | een commando plus een drempel; machinaal, dus ook hook-afdwingbaar |
| **observable** | expressief werk — design, communicatie, advies | een checklist van wat waar moet zijn na afloop; een mens of subagent oordeelt |

`none` mag, maar alleen met expliciete motivatie in de skill zelf.

Twee vormen omdat ruwweg de helft van de CEDA-collectie expressief is (`sparren`, `brainstorm`, `vormgever`, `write-issue`). Eén numerieke vorm daarop afdwingen levert lege KPI-blokken of verzonnen getallen, en allebei zijn erger dan niets. De observable vorm dwingt dezelfde discipline af — *waaraan zie ik dat dit goed ging* — zonder een getal te fingeren.

De skill draagt de **norm en de meetmethode**. De gemeten **uitkomst** hoort er niet in; die gaat naar de evaluatie.

---

## Frontmatter-schema

De 53 skills in `cedanl/.github` dragen op dit moment alleen `name` en `description`. Daarmee is er geen manier om te vragen "welke reference-skills hebben `binding: hard` zonder hook-tegenhanger" of "welke workflows verifiëren niks" — precies de vragen waar dedupliceren en lacune-detectie op steunen.

Voorstel voor het schema. **De volgorde is niet willekeurig:** bovenaan staan de velden die de coding agent zelf leest en waar dus vandaag al gedrag aan hangt; daaronder de CEDA-metadata, die niets doet tot wij er een validator op zetten.

```yaml
# --- door de coding agent gelezen; heeft vandaag al effect ---
name: check-style
description: ...          # het enige veld dat activeert — zie de description-sectie
allowed-tools: [Read, Grep, Glob]   # voorafgaande toestemming, geen sandbox
bundles:                  # niveau-3 bestanden, elk met een laadconditie
  - path: references/gotchas.md
    load: always
  - path: references/r-voorbeelden.md
    load: "bij R-code"

# --- CEDA-metadata; inert tot de validator draait ---
id: ceda.check-style      # stabiel; overleeft hernoemen
version: 1.2.0            # nodig om observaties over repo's te aggregeren
type: reference           # workflow | reference | connector
subtype: knowledge        # alleen bij reference: knowledge | presentation
origin: own               # external | extended | own
upstream: ~               # verplicht bij origin: extended — verwijst naar een SKILL
source: docs/ceda-python.md   # alleen bij reference: self | <pad> | <url> — een DOCUMENT
activation: ambient       # ambient | command | hook | scheduled | chained
binding: default          # hard | default | suggestie
execution: inline         # inline | isolated | deterministic
scope: org                # org | project        (user = laag, geen waarde)
verifies: measurable      # measurable | observable | none (none vereist motivatie)
```

**`source` en `bundles` zijn niet hetzelfde ding.** `source` wijst naar waar de waarheid staat en mag búiten de skill liggen — dat is de drift-vraag. `bundles` somt op welke bestanden mee worden geleverd in de skilldirectory en wanneer ze laden — dat is de context-vraag. Een skill kan `source: self` zijn en tegelijk drie bundles hebben.

`id` en `version` zijn geen administratie: zonder stabiele identiteit valt de evaluatie om, want dan is niet vast te stellen dat waarnemingen uit acht repo's over dezelfde skill gaan.

De regels uit dit document worden hiermee machinaal controleerbaar — geen smaakverschillen maar fouten:

- `binding: hard` zonder een bijbehorend `activation: hook`-object
- `origin: extended` zonder `upstream:`
- `type: reference` zonder `source:` (leeg ≠ `self`)
- `scope: user` met `subtype: knowledge`
- `source: self` met `scope: project` — is de skill de bron, dan hoort hij op org-scope
- een `bundles:`-item zonder `load:`-conditie
- `SKILL.md` boven de 500 regels zonder bundles
- een `description` zonder exclusion-clause terwijl een andere skill overlappende triggerwoorden draagt

---

## Evaluatie: levert de skill iets op voor de gebruiker

Verificatie is niet genoeg. Een skill kan elke check halen en toch het verkeerde doen: de stappen kloppen, het resultaat helpt niemand. Dat blijkt niet uit een commando, alleen uit gebruik over de tijd. Evaluatie gaat daarom over bruikbaarheid, niet over functioneren — en staat buiten de skill.

**Waarom buiten.** Org-scope skills worden via `npx skills add cedanl/.github` *gekopieerd* naar elke repo. Een waarneming die naast een kopie belandt, komt nooit terug bij de bron: N divergerende bestanden en een basis die niet leert.

Drie stappen:

1. **Observatie.** Interactie met Claude Code wordt getrackt over repo's heen. Daarnaast twee expliciete signalen: uitkomsten van de `verifies`-meting, en gerichte vragen aan de gebruiker.
2. **Destillatie.** Periodiek proces dat observaties aggregeert *per skill, over alle repo's heen* — niet per repo. Daar ontstaat pas een patroon; één waarneming in één repo is ruis.
3. **Voorstel.** Een wijzigingsvoorstel op de bron-skill in `cedanl/.github` — een PR of een suggestie, door een mens beoordeeld.

**Randvoorwaarde: skill-identiteit.** Aggregeren over repo's kan alleen als een skill stabiel identificeerbaar is — vandaar `id` en `version` in het schema. Nu staat er alleen `name`, en `name` verandert wel eens; dan is de historie stuk.

**Bijvangst:** een waarneming die in géén enkele bestaande skill past, is de signalering van een *ontbrekende* skill. Daarmee is de evaluatie ook het mechanisme achter "lacunes automatisch detecteren" in de to-do — geen opslag, maar een detector.

### Wat hier nog naast hoort: de baseline

Verificatie en evaluatie hierboven zijn twee verschillende meetmomenten, en er ontbreekt er een derde:

| | Meet | Wanneer | Onderwerp |
|---|---|---|---|
| `verifies:` | is het werk goed | elke run | het artefact |
| **eval met baseline** | **is de skill beter dan géén skill** | **bij schrijven of wijzigen** | **de skill** |
| evaluatie | helpt de skill iemand | over de tijd | het gebruik |

De middelste hebben we niet. De methode is een handvol testgevallen die je twee keer draait — mét en zonder de skill — en waarvan je de delta in pass-rate, tijd en tokens vergelijkt. Dat beantwoordt de vraag die verificatie niet kan stellen: een overbodige skill haalt al z'n checks. Bij 53 skills is dat de goedkoopste opruimtest die er is.

Uitgewerkt in `cedanl/.github#49`; eerst één keer doorlopen op een bestaande skill voordat we er iets van in `create-skill` bakken.

---

## Patronen

### Splitsen: workflow los van reference

Skills die zwaar aanvoelen zijn meestal twee dingen in één. `simplify-ceda` is niet één ding — het is `simplify` (de stappenreeks) plus `ceda-standards` (een knowledge-reference met `binding: default`) die in elkaar zijn geschoven.

Toets:

> Haal de organisatiespecifieke kennis eruit en zet 'm in een reference.
> Blijft er een zinnige stappenreeks over? → splitsen. De workflow wordt draagbaar, de reference wisselbaar.
> Valt de sequentie uit elkaar? → laten staan; de stappen zélf zijn organisatiespecifiek.

Kandidaten om te splitsen: `simplify-ceda`, `check-style`, `write-issue`, `release-notes`, `init-repo`. Kandidaten om te laten: `sam-uren-cowork-mac`, `sdp-onboard`, `generate-slides-retro` — daar zijn de schermen, de flow en de veldnamen de stappen.

**Splitsen kost ook iets**, en dat hoort in de toets. Te smal gesneden skills dwingen er meerdere tegelijk te laden voor één taak: meer context, meer descriptions die om activatie concurreren, en het risico dat twee skills elkaar tegenspreken.

### Chaining: composities

Composities in dit model volgen telkens dezelfde regel — **houd het generieke schoon, laat het specifieke aan de rand hangen:**

| Wat varieert | Invariant | Variant |
|---|---|---|
| inhoud | workflow | presentation-reference (doelgroep-patroon) |
| hardheid | reference met norm en meting | hook met afdwinging |
| volgorde | generieke workflow | lokale skill die eraan hangt |

Een brede workflow die aan het eind `simplify-ceda` aanroept, is dus geen losse feature maar de derde toepassing van hetzelfde principe.

**Waar de edges wonen.** Niet in de skill. Een externe skill kan geen chain naar een CEDA-skill declareren — je bezit z'n frontmatter niet. En conceptueel is "A draait na B" een lokale compositiebeslissing, geen eigenschap van A of B. Dus: **edges horen in CLAUDE.md of in een org-/project-manifest.** Dat is precies de dirigerende rol die CLAUDE.md verderop toebedeeld krijgt, en het houdt externe skills ongewijzigd bruikbaar — de voorwaarde voor extern-eerst.

Twee regels, anders loopt het vast:

- **Eén richting.** Generiek → specifiek. Anders cycli.
- **Diepte begrensd.** Chaint elke brede workflow er drie lokale bij, dan trekt één aanroep stilletjes veel context binnen. Declareren maakt dat zichtbaar, begrenzen houdt het hanteerbaar.

### Eén info, meerdere doelgroepen

Probleem: dezelfde info, verschillende doelgroepen of verschillende smaken. Handmatig gevoerd, versies driften. Fout: doelgroep/smaak zit verweven met content.

Voorbeeld: op moment van schrijven hebben we meerdere designer-skills die onafhankelijk van elkaar zijn, maar deels hetzelfde doen. Alleen is de smaak anders. Dat wil je niet. Je wilt voor collega's die geen smaak/voorkeur op dat gebied hebben tenminste één default expliciet, en voor collega's die een eigen voorkeur hebben dat via prompts mogelijk maken.

Fix — scheid invariant van variant in drie stukken:

1. **Content → één canonieke knowledge-reference.** Eén keer geschreven, `source: self` of een verwijzing naar het bronbestand. De workflow laadt 'm; jij plakt niks meer.
2. **Elke doelgroep → een presentation-reference.** Toon, jargon-niveau, zorgen, lengte, format.
3. **Workflow-skill "render voor doelgroep X".** Neemt knowledge + presentation → output. Doelgroep = argument (`$ARGUMENTS`, bijv. `/render docent`).

Resultaat: content DRY, doelgroep-versies afgeleid, niet opgeslagen. Wijzig de info op één plek → alle versies kloppen.

Dit generaliseert: **workflow (stappen, invariant) + presentation-reference (variant) → output.** Het is ook meteen de reden dat de subtypes op precies deze grens gesneden zijn: knowledge is wat je hergebruikt, presentation is wat je varieert.

- **Feitelijk** (finance, code) — zelfde stappen, één correct resultaat. De presentation-reference is leeg; doelgroep verandert hooguit de verpakking eromheen.
- **Expressief** (communicatie, design) — zelfde stappen, andere presentatie = een ander product. Hier is de presentation-reference essentieel: doelgroep-profiel voor tekst, brandregels (design-tokens, kleur, typografie) voor design.

### Taste is geen laag

Judgment/taste staat zelden op zichzelf. Het is een *kwaliteit* van een workflow (wanneer stoppen, wat "goed" is) of reference (welke default), niet een eigen rij. Pure-taste skills bestaan maar zijn dun.

---

## Verbinden met projecten

Drie inhaakpunten per repo:

1. **Marketplace geïnstalleerd** → gedeelde workflows/connectors in elke sessie.
2. **`repo/.claude/`** → project-scoped skills, gedeeld via git.
3. **`repo/CLAUDE.md`** → de altijd-aan laag die de rest dirigeert.

CLAUDE.md laadt *altijd*, volledig, elke sessie. Reference-skills laden on-demand. Dus:

- **Wel in CLAUDE.md**: projectfeiten die niet te raden zijn (buildcommando, testrunner), *pointers* naar conventies ("volg ceda-python-standards"), afwijkingen van de default.
- **Niet in CLAUDE.md**: de inhoud van standaarden of workflows. Die zit in de skill. CLAUDE.md dirigeert, dupliceert niet.

---

## To Do

- [ ] Deze indeling valideren
- [ ] Skills-ontologie in praktijk testen met geïsoleerd voorbeeld (design?)
- [ ] Create-skill-skill maken o.b.v. de laatste inzichten en deze indeling
- [ ] Teamwerkwijze met entire en devcontainers zodat we lacunes in skills automatisch kunnen detecteren
- [ ] Frontmatter-schema vaststellen en op de bestaande skills toepassen (`id`, `version`, `type`, `subtype`, `origin`, `upstream`, `source`, `bundles`, `activation`, `binding`, `execution`, `scope`, `verifies`)
- [ ] Validator bouwen die de regels uit dit document controleert — te beginnen met `binding: hard` zonder hook-tegenhanger en `reference` zonder `source`
- [ ] Per bestaande reference-skill de `source` vaststellen; bij `source: self` controleren of de inhoud niet elders óók staat
- [ ] Doelgroep-patroon één keer echt bouwen; de dubbele designer-skills (`vormgever-npuls-huisstijl` / `-2`) zijn de aanleiding en de testcase
- [ ] `caveman-cowork` van org- naar user-scope verplaatsen
- [ ] Eerste hook toevoegen; nu is de activation-as voor drie van de vijf waarden ongebruikt
- [ ] Descriptions langslopen op exclusion-clauses, te beginnen bij de bekende overlappen (`vormgever-*`, `generate*-slides-retro*`, `write-issue*`)
- [ ] `allowed-tools` invullen op de bestaande skills; begin bij alles met `origin: external`
- [ ] Skill-evaluatie met baseline één keer volledig doorlopen (`cedanl/.github#49`)
- [ ] `SKILL.md`-lengtes meten; wat boven de 500 regels zit opsplitsen in bundles met laadconditie

---

## Appendix: CEDA-projectlandschap

Repositorytypen binnen CEDA:

- **module repositories** — één element uit het data science proces staat centraal: data preparatie, data science, data visualisatie, data interpretatie (chatbots/reporting) of data actie (actie / integratie met andere systemen)
- **integratie repositories** — hebben we nog niet
- **tech repositories** — ondersteunende repositories met templates, standaarden, utilities, etc.
- **project repositories** — interne kennis, afspraken en communicatie

Repositories hebben tenminste 2 fases:

1. **Minimum Viable Product** — veel ruimte voor eigen invulling, doel is valideren dat het project inhoudelijk en technisch kan voldoen aan de behoefte. Mogelijk deels hard-coded of sterk beperkte functionaliteit.
2. **Production-ready** — modulair, gemakkelijk in beheer. Zowel op zichzelf te runnen, als lokaal te integreren, als te integreren op SURF-infrastructuur.

---

## Bronnen

- Anthropic — *Equipping agents for the real world with Agent Skills*: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Carlos Perez — *Structuring Agents, Skills, and MCPs*: https://medium.com/intuitionmachine/structuring-agents-skills-and-mcps-best-practices-from-anthropic-9312849ccea6
  **Let op de woordkeus.** Perez heeft ook drie lagen, maar noemt onze workflow-skill een *agent* en reserveert het woord *skill* voor wat wij een reference-skill noemen ("passive: they don't decide when to fire"). Structureel zitten we op hetzelfde model; alleen dekt zijn "agent" hier geen apart handelend object, maar de stappenreeks die Claude volgt. Zijn tier-model voor untrusted content (reader / orchestrator / resolver) is wél iets wat wij nog niet hebben — zie de `allowed-tools`-as.
- Agent Skills — *Skill Creation: Best Practices*: https://agentskills.io/skill-creation/best-practices
- Agent Skills — *Skill Creation: Evaluating Skills*: https://agentskills.io/skill-creation/evaluating-skills
- Generative Programmer — *Skill Authoring Patterns from Anthropic's Docs*: https://generativeprogrammer.com/p/skill-authoring-patterns-from-anthropics

### Interne referenties

- `cedanl/ceda-workshop-starter` — praktijkvoorbeeld met KPI-blokken per skill, hooks voor afdwinging, en subagents voor review. Bron van de binding-splitsing en de execution-as.
- `cedanl/.github/.claude/skills` — de huidige collectie (53 skills, waarvan 19 in openstaande PR's).
- `docs/skill-gaps.md` — gap-analyse van de collectie tegen deze ontologie.
- `cedanl/project_algemeen#41` — kennisarchitectuur; zelfde bronze/gold-patroon op grotere schaal.
