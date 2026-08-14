---
name: create-skill
description: Bouwt een nieuwe CEDA Claude skill — zoekt eerst of er al een generieke bestaat, toetst de herkomst, classificeert en valideert. Gebruik wanneer iemand een skill wil aanmaken voor cedanl, een proces wil codificeren als skill, of een bestaande wil herzien. LET OP — alleen classificeren zonder te schrijven hoort bij `skills-ontology`; alleen de PR openen bij `branch-pr`.
allowed-tools: Read Write Edit Grep Glob Bash AskUserQuestion Skill
compatibility: Requires python3, git and the gh CLI; npx and the claude CLI for the search step
metadata:
  ceda-id: ceda.create-skill
  ceda-version: "2.0.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: extended
  ceda-upstream: superpowers:writing-skills
  ceda-source: self
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Create Skill

Bouwt een nieuwe skill voor `cedanl/.github` volgens de skills-ontologie: eerst zoeken of
iemand hem al geschreven heeft, dan toetsen of de inhoud echt ergens vandaan komt, en pas
daarna schrijven. Output is een gevalideerde skilldirectory plus een PR.

De classificatie-kennis zit in de reference-skill `skills-ontology`. Laad die zodra je
twijfelt over type, subtype of een van de vijf assen. Het veld-voor-veld schema staat in
`references/frontmatter-schema.md` — lees dat altijd voor stap 5.

## Workflow

When the user invokes `/create-skill [optional: beschrijving]`:

### 1. Extern eerst — bestaat dit al?

Schrijf niks tot deze stap klaar is. Een bestaande skill die werkt is beter dan een eigen
skill die hetzelfde doet.

Er zijn **twee gescheiden vindplaatsen**. Ze indexeren elkaar niet, dus zoek in allebei.

**1. Het skills.sh-register** — losse skills (GitHub-repo's met een `SKILL.md`), bruikbaar
door ~20 verschillende agents:

```bash
npx skills find "<onderwerp>"                      # interactief zoeken in het register
npx skills find "<onderwerp>" --owner anthropics   # scope op één GitHub-eigenaar
npx skills add -l <owner>/<repo>                   # toon wat er in een repo zit, installeer niks
```

**2. Claude Code-plugins** — die leveren skills, commands, hooks en subagents in één pakket en
staan *niet* in het skills.sh-register. Zoek in deze vaste lijst, in deze volgorde:

| Bron | Wat erin zit |
|---|---|
| `anthropics/skills` | de referentiecollectie van Anthropic, inclusief `skill-creator` |
| `obra/superpowers` | proceswerk: brainstorming, TDD, systematisch debuggen, plannen |
| `vercel-labs/agent-skills` | webontwikkeling en frontend |
| `anthropics/claude-code` (official marketplace) | wat er met Claude Code zelf meekomt |

```bash
npx skills add -l anthropics/skills            # inhoud van een repo bekijken zonder installeren
claude plugin install <plugin>@<marketplace>   # pas ná akkoord van de gebruiker
```

**Kijk niet naar wat er lokaal geïnstalleerd staat.** `claude plugin marketplace list` en
`claude plugin list` lezen de machine van deze gebruiker; een collega heeft iets anders, en de
uitkomst van deze stap moet voor iedereen hetzelfde zijn. Groeit de lijst hierboven, dan
verandert hij hier — niet per laptop. (In een devcontainer met een vastgelegde set is
lokaal kijken wél reproduceerbaar; die hebben we nog niet.)

Vind je niets, dan nog één handmatige ronde: de leaderboard op https://skills.sh/ en
`gh search code --filename SKILL.md "<term>"`.

Drie uitkomsten:

| Uitkomst | `origin` | Actie |
|---|---|---|
| Bestaande skill dekt het | `external` | Installeer 'm, vul `allowed-tools` in, stop hier. Meld wat je installeerde. |
| Bestaande skill komt in de buurt | `extended` | Neem 'm over als basis, noteer `upstream:`, en scherp 'm aan met wat bij ons anders is |
| Niets vergelijkbaars | `own` | Ga door |

Meld expliciet wat je gezocht hebt en wat je vond. `own` terwijl er een bekende generieke
variant bestaat, is een beslissing die zichtbaar hoort te zijn.

### 2. Wat hebben we zelf al?

```bash
ls .claude/skills/
grep -h "^description:" .claude/skills/*/SKILL.md
```

Lees de SKILL.md van de meest vergelijkbare skill als referentie voor structuur en toon.

Kan een bestaande skill uitgebreid worden in plaats van een nieuwe? Stel dat voor en stop
hier. Twee skills die elkaar half overlappen kosten meer dan één skill die iets breder is:
meer context, meer descriptions die om activatie concurreren, en het risico dat ze elkaar
tegenspreken.

### 3. Herkomst-gate

> Waar komt de inhoud van deze skill vandaan?

Deze stap is blokkerend. Een skill die een model uit algemene kennis verzint levert generieke
instructies op ("ga zorgvuldig om met fouten"). Bij onderwijsdata — DUO-leveringen,
1CHO-definities, SIS-eigenaardigheden — heeft het model weinig achtergrond, dus is verzonnen
inhoud slecht herkenbaar als verzonnen.

Geldige bronnen:

- een sessie waarin de taak daadwerkelijk is uitgevoerd, mét de correcties van de gebruiker
- interne documentatie, runbooks, standaarden in `standards/` of `docs/`
- leveranciers- of upstream-documentatie (SURF, DUO, Anthropic, een library)
- code-review-commentaar en issue-discussies
- git-historie van fixes — die laat zien wat er echt misging
- een expert die het in dit gesprek vertelt

Is er geen bron, dan is het antwoord niet "dan schrijven we het maar op". Zeg dit:

> Er is nog geen materiaal om deze skill op te baseren. Doe de taak één keer echt — ik loop
> mee en noteer je correcties — en daarna destilleren we daar de skill uit. Anders krijg je
> een skill die klinkt als kennis maar het niet is.

Leg het antwoord vast in `source:`. Vier vormen, en het verschil zit in wie erbij kan:

| Vorm | Voorbeeld | Consequentie |
|---|---|---|
| `self` | `source: self` | De skill *is* de bron. Dan mag dezelfde inhoud nergens anders staan, en hij hoort op `scope: org` met wijziging via review. |
| pad in de repo | `source: docs/ceda-python.md` | Bij wijziging van dat bestand hoort de skill mee te bewegen. |
| publieke url | `source: https://servicedesk.surf.nl/…` | Iedereen kan 'm nalezen; de skill mag samenvatten en doorverwijzen. |
| `intern:` + vindplaats | `source: intern:GitLab wiki npuls/ceda` | Achter inlog. |

Bij `intern:` geldt een extra eis: **de skill moet zelfstandig leesbaar zijn.** Wie de skill
laadt, kan de bron misschien niet openen — een verwijzing is dan geen bron maar een
doodlopende weg. Schrijf de substantie uit in de skill zelf en gebruik `intern:` alleen om
vast te leggen waar het origineel staat, zodat je bij drift weet wat je moet checken. En
kopieer geen inloggegevens, tokens of persoonsgegevens mee — die horen in een
secrets-store, niet in een skill.

### 4. Interview

Twee soorten vragen, en ze gaan verschillend.

**Vrije tekst** — deze kun je niet voorkauwen. Stel ze in de chat en wacht op antwoord:

1. **Naam** — kebab-case, gelijk aan de directorynaam.
2. **Doel** — wat doet de skill in één zin, en wat is de concrete output?
3. **Triggers** — 2-3 berichten die een gebruiker echt zou typen om dit te krijgen. Laat
   hem typen zoals hij het zou typen; vraag niet om vertalingen.
4. **Anti-trigger** — een geval waarin deze skill juist *niet* moet vuren, en welke skill dan
   wél. Dit wordt de exclusion-clause; zonder dit antwoord is stap 6 giswerk.

**Keuzevragen** — stel deze via het keuzemenu (`AskUserQuestion`), niet als open vraag. Ze
hebben een vaste set antwoorden en een verdedigbare default, dus een menu is sneller en
levert bruikbaardere antwoorden dan "wat wil je hier?". Maximaal vier per aanroep, dus twee
rondes:

| Ronde | Vraag | Opties |
|---|---|---|
| 1 | Wat voor ding is dit? | stappenreeks die je uitvoert (`workflow`) · kennis die je volgende actie stuurt (`reference` + `knowledge`) · toon/stijl/doelgroep (`reference` + `presentation`) · data of tools via een protocol (`connector`) |
| 1 | Waar geldt het? | alle CEDA-repo's (`org`) · alleen dit project (`project`) |
| 1 | Waaraan zie je dat het gelukt is? | een commando met een drempel (`measurable`) · een checklist die iemand nakijkt (`observable`) · niets meetbaars (`none`, vraagt motivatie) |
| 2 | Wat mag de skill aanraken? | alleen lezen (`Read, Grep, Glob`) · lezen + schrijven (`+ Write, Edit`) · ook commando's draaien (`+ Bash`) · maatwerk |

Zet in elke optie kort wat de keuze *doet*, niet alleen het label — de gebruiker kent de
ontologie niet. Bij twijfel over `type`: laad `skills-ontology`.

### 5. Classificeer en vul de frontmatter

Lees nu `references/frontmatter-schema.md`. Bepaal de kernvelden expliciet met de gebruiker,
vul de afgeleide velden zelf in en meld ze in de draft.

De kernvraag voor `type`: **bevat het een stappenreeks of beslislogica?**

- Ja → `workflow`
- Nee, injecteert kennis/regels/stijl → `reference` (+ `subtype: knowledge | presentation`)
- Levert data of tools via een protocol → `connector`

De oude CEDA-indeling Actie / Review / Generatie / Wizard is geen `type` meer maar een
vormtip *binnen* `type: workflow`; het oude type "Kennis" heet nu `type: reference` met
`subtype: knowledge`. Gebruik die woorden niet meer in nieuwe skills.

Twijfel je of het één skill of twee is, pas dan de splitsen-toets toe: haal de
organisatiespecifieke kennis eruit en zet 'm apart. Blijft er een zinnige stappenreeks over,
dan splitsen — de workflow wordt draagbaar, de reference wisselbaar. Valt de sequentie uit
elkaar, dan laten staan.

### 6. Schrijf de description en los de overlap op

Lees `references/description-schrijven.md`.

De description is het enige veld dat activeert. Schrijf 'm in de derde persoon, met de
letterlijke triggerwoorden uit vraag 3 en een exclusion-clause uit vraag 4.

De lengte hangt aan `ceda-activation`, niet aan het spec-plafond: bij `command` of `chained`
≤400 tekens — die skill wordt aangeroepen, dus de description is een herkenningsteken. Bij
`ambient` mag het volle budget van 1024. Mechaniek hoort er nooit in: paden, repo- en
bestandsnamen, vlaggen, het interne schema. Toets: verandert het zonder dat de trigger
verandert, dan staat het in de body.

**Taal: volg de gebruiker, vertaal niet uit principe.** Schrijf de description in de taal
waarin de triggers gesteld zijn. Twee varianten neem je alleen op als het team het onderwerp
echt in twee talen benoemt — `issue`/`melding`, `deployen`/`uitrollen`. Een verzonnen Engelse
vertaling naast elke Nederlandse term kost budget en vuurt nergens op. Voor de body geldt
hetzelfde: een `extended` skill houdt de taal van z'n upstream (meestal Engels), een
CEDA-eigen skill mag gewoon Nederlands zijn. Meng niet binnen één bestand.

Vergelijk daarna de nieuwe description met alle bestaande. Bij overlappende triggerwoorden
pas je **beide** descriptions aan — de nieuwe én de bestaande — in dezelfde PR. Meld dat
expliciet aan de gebruiker; het is een wijziging aan een skill waar hij niet om vroeg.

### 7. Draft de body

Begin met het skelet — `assets/skelet-workflow.md` of `assets/skelet-reference.md` — en kies
daarna de vorm bij het onderwerp met `references/vorm-patronen.md`. Dat menu bevat per patroon
(symptoom-tabel, beslisboom, architectuur-schets, benoemde gotcha-kop, gebundelde bestanden)
de vraag wanneer het z'n plek verdient, plus de skill in de collectie die het al goed doet.
**Neem geen sectie op omdat het skelet 'm noemt** — een lege of ceremoniële kop kost context
en levert niets.

Regels die het verschil maken:

- **Voeg toe wat de agent niet weet.** Geen uitleg over wat een PDF of een migratie is —
  wel de conventie, de valkuil en het commando dat hier geldt.
- **Gotcha's staan in SKILL.md zelf**, en krijgen een kop die het feit noemt
  (`## Let op: '+' wordt '_' in OCI-tags`), geen anonieme bulletlijst. Nooit conditioneel
  laden: een gotcha is per definitie iets waarvan je niet weet dat je het nodig hebt, dus
  "lees dit als je tegen X aanloopt" werkt niet — X herkennen ís het probleem.
- **Eén default, geen menu.** Kies de aanpak en noem het alternatief in één bijzin.
- **Prescriptief waar het breekt, vrij waar het kan.** Geef bij een dwingende stap de reden
  mee; de reden laat het model generaliseren naar gevallen die je niet voorzag.
- **Procedure boven antwoord.** Leer de aanpak voor een klasse problemen, niet de uitkomst
  van één geval.
- **Onder de 500 regels / 5.000 tokens.** Dat betaal je élke keer dat de skill vuurt. Wat je
  zelden nodig hebt gaat naar `references/`, `assets/` of `scripts/`, met de laadconditie in
  een `## Gebundelde bestanden`-sectie onderaan de body — niet in de frontmatter, want daar
  leest de agent 'm niet. Eén hop diep.
- **Taal**: volg de skill waar je op aansluit; een `extended` skill houdt de taal van z'n
  upstream. User-facing tekst in het Nederlands.

### 8. Valideer

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills/<naam>
```

Los elke `✗` op en draai opnieuw tot de exit code 0 is. Waarschuwingen (`!`) mag je laten
staan met een reden; noem ze in de draft. Deze validator dekt zowel de spec-regels (naam,
descriptionlengte, toegestane frontmatter-velden) als de CEDA-regels. Heb je `skills-ref`
geïnstalleerd, draai dan ook `skills-ref validate ./.claude/skills/<naam>` — dat is de
referentie-implementatie van de spec.

Draai daarna de collectie-brede check om te zien of je de activatie van iets anders hebt
verslechterd:

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills
```

Bestaande skills die nog geen CEDA-metadata dragen komen langs als `LEGACY` — dat is verwacht
en niet jouw probleem in deze PR.

### 9. Toon de draft en wacht op akkoord

Presenteer:

1. de volledige SKILL.md
2. de lijst gebundelde bestanden met hun laadconditie
3. de wijzigingen aan **bestaande** descriptions, apart benoemd
4. de validator-output

> Klopt dit? Zeg wat je wil aanpassen, of geef akkoord om te schrijven.

Verwerk feedback en herhaal tot akkoord.

### 10. Schrijf en open de PR

```bash
mkdir -p .claude/skills/<naam>
```

Schrijf de bestanden, draai de validator nog één keer, en roep dan `/branch-pr` aan voor de
branch en de PR. De PR-body noemt in elk geval: type en origin, de `source`, welke bestaande
descriptions zijn meegewijzigd en waarom, en de validator-output.

Rapporteer tot slot:

> **Skill aangemaakt:** `.claude/skills/<naam>/` — PR #<nr>
>
> Volgende stappen:
> 1. Test of de skill vuurt op je eigen triggerzinnen uit een verse sessie
> 2. Draai de skill één keer op een echte taak en voeg elke correctie die je moest geven toe
>    aan de gotchas — dat is de goedkoopste manier om 'm te verbeteren

## Let op: de frontmatter is niet vrij

De spec kent zes velden — `name`, `description`, `license`, `compatibility`, `metadata`,
`allowed-tools` — en verder niets. Alle CEDA-velden staan onder `metadata:` met een
`ceda-`-prefix, als **strings** (quote het versienummer). `allowed-tools` is een
spatie-gescheiden string, geen YAML-lijst. Zet je iets op topniveau, dan faalt de skill op
`skills-ref validate` en negeren andere agents het.

Er is geen `bundles:`-veld. Een laadconditie in de frontmatter zou ook niets doen: de agent
leest de body.

## Andere gotcha's

- **De bestaande skills dragen alleen spec-velden.** De validator meldt ze als `LEGACY`.
  Migreer ze niet en passant mee in een skill-PR; dat is een eigen traject
  (`cedanl/.github#49`, en de spec-fouten in `#59`).
- **`gh` moet buiten de sandbox draaien** in deze omgeving, en `unset GITHUB_TOKEN` voor
  `gh pr`-commando's — zie `branch-pr`.
- **`ceda-binding: hard` zonder hook bestaat niet.** Wil de gebruiker "dit moet altijd", vraag
  dan waar de hook komt. Zonder hook is het `default` plus een expliciete reden waarom
  afwijken hier misgaat — en die reden is wat het model laat generaliseren.
- **Baseline-evaluatie is nu goedkoop.** `claude plugin eval --ablation with-without <naam>`
  draait testgevallen mét en zonder de skill en rapporteert de delta. Dat beantwoordt de vraag
  die verificatie niet kan stellen — een overbodige skill haalt al z'n checks. Nog niet
  verplicht in deze workflow (zie `cedanl/.github#49`), wel de moeite bij twijfel of een skill
  iets toevoegt.

## Verificatie

`ceda-verifies: measurable` — de skill is klaar als

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills/<naam>
```

exit code 0 geeft, en de collectie-brede run geen nieuwe overlap-waarschuwing oplevert die er
voor deze PR niet was.

## Gebundelde bestanden

- `references/frontmatter-schema.md` — lees altijd, voor stap 5: de zes spec-velden en de
  `ceda-*`-sleutels met hun beslisregels
- `references/description-schrijven.md` — lees bij stap 6, of zodra je een overlap tussen
  descriptions moet oplossen
- `references/vorm-patronen.md` — lees bij stap 7, voor de keuze welke secties de skill krijgt
- `assets/skelet-workflow.md` — kopieer bij `ceda-type: workflow` of `connector`
- `assets/skelet-reference.md` — kopieer bij `ceda-type: reference`
- `scripts/validate-skill.py <pad>` — draaien, niet lezen: valideert één skill of de hele
  collectie tegen de spec en de ontologie

## Important

- Schrijf org-scope skills naar `.claude/skills/<naam>/` in `cedanl/.github`. Alleen bij
  `scope: project` schrijf je in de projectrepo zelf.
- Genereer nooit een skill die automatisch deployt, publiceert of force-pusht zonder
  expliciete bevestigingsstap in de gegenereerde skill.
- Deze skill maakt en herziet skills. Voor het *beoordelen* van een skill-PR van iemand
  anders, het opruimen van duplicaten of het auditen van een externe skill bestaan nog geen
  workflows — zie `docs/skill-gaps.md`, Gap 6.
