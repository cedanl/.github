---
name: dedup-skills
description: Ruimt overlappende skills op in een collectie — draait de collectie-brede validator voor de detectie, beslist per paar tussen samenvoegen, deprecaten of houden-met-scherpere-descriptions, en voert het deprecatiepad uit inclusief de kopieën die via `npx skills add` in andere repo's staan. Gebruik wanneer iemand zegt dat twee skills hetzelfde doen, vraagt of een skill weg kan, "dubbele skills", "overlappende skills", "skills opruimen", "dedup", "deprecaten" of "welke skills kunnen weg" noemt, of wanneer de validator overlap-waarschuwingen geeft. LET OP — gaat het om één nieuwe skill in een PR, gebruik dan `review-skill`; om een skill schrijven of herzien, `create-skill`; om de vraag wat voor soort skill iets is, `skills-ontology`. Niet voor dubbele *code* — daarvoor zijn `simplify-ceda` en `de-hardcode`.
allowed-tools: Read Grep Glob Bash Write Edit AskUserQuestion
compatibility: Requires python3, git and the gh CLI; the claude CLI for the ablation step
metadata:
  ceda-id: ceda.dedup-skills
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: self
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Skills ontdubbelen

Ruimt overlap op in `.claude/skills/`. De detectie doet de validator; deze skill draagt het
oordeel en het pad. Dat pad is het echte werk: een org-skill is via `npx skills add` naar
andere repo's **gekopieerd**, dus hem hier weghalen laat hem daar gewoon staan en gewoon
triggeren.

Lees eerst `references/deprecatiepad.md`. Zonder dat is "we halen hem weg" een halve actie.

## Workflow

When the user invokes `/dedup-skills [optional: twee skillnamen]`:

### 1. Detectie komt uit de validator, niet uit een leesronde

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills
```

Wat hij oplevert, neem je over als vastgesteld — er is geen oordeel voor nodig en dus ook
geen model:

| Signaal | Betekenis |
|---|---|
| `✗ name … wordt door meerdere directories geclaimd` | twee kopieën van één identiteit — ga naar uitkomst **samenvoegen** |
| `! overlappende triggerwoorden met X … geen exclusion-clause` | kandidaatpaar, gedeelde woorden staan erbij |

Herleid een waarschuwing nooit met de hand. Ga je hem tegenspreken, doe dat met bewijs uit
stap 2, niet met een indruk bij het lezen.

Aanvullend, en dit vindt de validator niet: dezelfde bronwaarheid op meerdere plekken.

```bash
/usr/bin/grep -rl "<hexcode of norm of pad>" .claude/skills/
```

Dubbele bronwaarheid is een *ander* probleem dan dubbele triggers — daar hoort geen skill te
verdwijnen, maar een verwijzing te komen. Zie stap 3, uitkomst C.

### 2. Bewijs per paar, met `diff` en niet met indruk

Per kandidaatpaar precies deze drie:

```bash
diff <(sed -n '/^description:/p' A/SKILL.md) <(sed -n '/^description:/p' B/SKILL.md)
diff A/SKILL.md B/SKILL.md | wc -l
ls -R A B
```

Wat je zoekt: identieke of bijna-identieke descriptions (dan gooit het model een muntje op),
en welke van de twee de bundels heeft (dat is bijna altijd de doorontwikkelde).

Zoek daarna wie er naar de kandidaten verwijst — dit vergeten kost je een gebroken skill:

```bash
/usr/bin/grep -rn "A\|B" .claude/skills/ --include=SKILL.md --include=*.md
```

### 3. Beslis per paar: drie uitkomsten

| Uitkomst | Wanneer | Actie |
|---|---|---|
| **A. Samenvoegen** | zelfde artefact, één is verder ontwikkeld | de rijkste versie blijft, de ander gaat het deprecatiepad in, verwijzingen mee |
| **B. Parametriseren** | zelfde taak, ander oppervlak of andere doelgroep | één skill, het verschil wordt een argument of een bestand in `references/` |
| **C. Houden, descriptions repareren** | de skills zijn echt verschillend, alleen de triggerruimte overlapt | geen bestand raken; **beide** descriptions krijgen een exclusion-clause, in dezelfde PR |

C is de meest voorkomende uitkomst en de goedkoopste. Grijp niet naar A omdat twee skills op
elkaar lijken — kijk of ze een *ander besluit* nemen bij dezelfde input.

Zit het verschil alleen in de doelgroep of de persona, dan is dat B: content DRY, doelgroep
als argument.

### 4. Voor je iets overbodig verklaart: meet het

> Zonder baseline is "deze skill is overbodig" een mening.

```bash
claude plugin eval --ablation with-without <naam>
```

Dat draait testgevallen mét en zonder de skill en rapporteert de delta. Verplicht bij uitkomst
A en B als de kandidaat om andere redenen dan een letterlijke kloon verdwijnt. **Overslaan mag
alleen bij een aantoonbare kloon** — zelfde `name` in de frontmatter, of descriptions die
byte-identiek zijn. Sla je hem over, zet dan in de PR *waarom* het een kloon is.

Geeft de ablation geen meetbaar verschil, dan is dat het argument. Geeft hij wél verschil, dan
is de skill niet overbodig en zit je in uitkomst C.

### 5. Het deprecatiepad

Lees `references/deprecatiepad.md` en volg het. In het kort: een verwijderde skill blijft
bestaan in elke repo die hem ooit gekopieerd heeft, dus verwijderen is stap drie van vier en
niet stap één.

### 6. Toon het plan en wacht op akkoord

Eén tabel — kandidaat, uitkomst, bewijs, ablation-uitslag — plus de verwijzingen die
meeveranderen en de repo's waar een kopie staat. Daarna:

> Klopt dit? Zeg wat je wil aanpassen, of geef akkoord om uit te voeren.

Voer niets uit voor akkoord. Geen `git rm`, geen `git mv`, geen issue.

### 7. Uitvoeren, in aparte PR's per uitkomst

Klonen (A) · parametriseren (B) · descriptions (C) zijn drie verschillende soorten risico en
drie verschillende reviewers. Eén PR die ze mengt wordt niet gereviewd maar doorgeklikt.

Roep per PR `/branch-pr` aan. Noem in de body: het bewijs per paar, de ablation-uitslag, en de
issues die openstaan voor de kopieën elders.

## Let op: verwijderen bereikt de kopieën niet

`npx skills add cedanl/.github` **kopieert** naar `<repo>/.claude/skills/`. Er is geen
koppeling terug: geen versie, geen lockfile, geen update-commando dat verdwenen skills opruimt.
Wat je hier weghaalt blijft daar staan, in de versie van het moment van kopiëren, en blijft
triggeren.

Gevolg voor de volgorde: eerst zichtbaar maken dat de skill vervangen is, dán pas weghalen.
Een tombstone die niemand ophaalt helpt niet, maar een skill die stil verdwijnt helpt ook
niet — het verschil is dat je bij de eerste weet wie je moet aanschrijven.

## Let op: geen nieuw metadata-veld voor deprecatie

De verleiding is een `ceda-deprecated: true` toe te voegen. Doe dat niet. Geen enkele agent
leest het (de spec kent het niet, en de agent leest de body), en we hebben nog niet één keer
meegemaakt wat er in de praktijk misgaat. Het tombstone-patroon uit
`references/deprecatiepad.md` gebruikt uitsluitend velden die al bestaan: de `description`
draagt de doorverwijzing, want dat is het enige veld dat activeert.

## Verificatie

`ceda-verifies: measurable` — klaar als:

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills
```

1. minder fouten dan voor de ronde, en geen nieuwe,
2. geen enkele `name … wordt door meerdere directories geclaimd` meer,
3. voor elk paar dat als C is afgedaan: aan **beide** kanten een exclusion-clause, dus de
   waarschuwing is aan beide kanten weg,
4. en per gedeprecateerde skill een openstaand issue op elke repo waar een kopie staat.

Punt 4 is niet machinaal te checken; die hoort in de PR-body als lijstje met issuenummers.

## Gebundelde bestanden

- `references/deprecatiepad.md` — lees vóór stap 5, en vóór je iets voorstelt dat een skill
  laat verdwijnen: de vier stappen, het tombstone-patroon en het commando om kopieën in de
  org te vinden

## Important

- **Detecteren is niet het probleem, begrenzen wel.** De validator vindt de paren al. De
  waarde van deze skill zit in stap 3 t/m 5 — er is geen ronde nodig waarin je alle
  descriptions nog eens naast elkaar legt.
- Nooit automatisch samenvoegen of verwijderen. Elk voorstel gaat langs een mens, ook als de
  ablation nul verschil geeft.
- Verwijzingen uit andere skills verhuizen mee in dezelfde PR. Een skill die naar een
  verdwenen skill wijst is erger dan het duplicaat.
- Deze skill oordeelt over een **collectie**. Gaat het om één skill in een PR, dan is dat
  `review-skill`; gaat het om de vraag of een skill überhaupt moet bestaan vóór hij geschreven
  is, dan is dat stap 1 en 2 van `create-skill`.
