# Frontmatter — spec-conform, met CEDA-metadata

De Agent Skills-specificatie kent **zes** frontmatter-velden. Meer bestaat er niet; eigen
velden horen onder `metadata:`, een map van string naar string. Alles wat wij extra willen
weten staat daar, met een `ceda-`-prefix zodat het niet botst met dat van iemand anders.

```yaml
---
name: check-style
description: <het enige veld dat activeert — zie references/description-schrijven.md>
allowed-tools: Read Grep Glob
compatibility: Requires uv and ruff      # alleen als de skill echt iets nodig heeft
metadata:
  ceda-id: ceda.check-style
  ceda-version: "1.2.0"
  ceda-type: reference                   # workflow | reference | connector
  ceda-subtype: knowledge                # alleen bij reference: knowledge | presentation
  ceda-origin: own                       # external | extended | own
  ceda-upstream: ""                      # verplicht bij origin: extended — een SKILL
  ceda-source: docs/ceda-python.md       # self | pad | url | intern:<vindplaats>
  ceda-activation: ambient               # ambient | command | hook | scheduled | chained
  ceda-binding: default                  # hard | default | suggestie
  ceda-execution: inline                 # inline | isolated | deterministic
  ceda-scope: org                        # org | project  (user is een laag, geen scope)
  ceda-verifies: measurable              # measurable | observable | none
---
```

## De zes spec-velden

| Veld | Verplicht | Regels |
|---|---|---|
| `name` | ja | 1-64 tekens, alleen `a-z`, `0-9` en `-`. Niet beginnen of eindigen met een streepje, geen dubbele streepjes, en **gelijk aan de directorynaam**. Underscores zijn ongeldig. |
| `description` | ja | 1-1024 tekens. Wat de skill doet én wanneer je 'm gebruikt, met de woorden waarop hij moet vuren. |
| `allowed-tools` | nee | Een **spatie-gescheiden string**, geen YAML-lijst: `Read Grep Glob` of `Bash(git:*) Read`. Experimenteel in de spec, maar Claude Code leest 'm. |
| `compatibility` | nee | Max 500 tekens. Wat de omgeving moet hebben: `Requires glab, kubectl and SDP tenant access`. Alleen invullen als het echt een eis is. |
| `license` | nee | Kort: een licentienaam of een verwijzing naar een meegeleverd bestand. |
| `metadata` | nee | Map van string naar string. Hier staat alles van ons. Geen geneste lijsten — waarden zijn strings, dus quote versienummers en gebruik `""` voor "niet van toepassing". |

## De CEDA-metadata

Expliciet vragen tijdens het interview:

| Sleutel | Beslisregel |
|---|---|
| `ceda-type` | Bevat het een stappenreeks of beslislogica? → `workflow`. Injecteert het kennis, regels of stijl? → `reference`. Levert het data of tools via een protocol? → `connector`. |
| `ceda-subtype` | Alleen bij reference. Verandert het *wat* Claude weet (`knowledge`) of *hoe* Claude formuleert (`presentation`)? |
| `ceda-origin` | Ongewijzigd overgenomen (`external`), externe basis die wij aanscherpen (`extended`, vereist `ceda-upstream`), of geen generiek equivalent (`own`). |
| `ceda-source` | Waar staat de bron van waarheid buiten de skill? Nooit leeg: leeg betekent tegelijk "geen bron" en "nog niet ingevuld". |
| `ceda-scope` | Alle CEDA-repo's (`org`) of alleen dit project (`project`). Lokaler wint bij conflict. |
| `ceda-verifies` | Een commando met een drempel (`measurable`), een checklist die iemand nakijkt (`observable`), of niets meetbaars (`none`, vereist motivatie in de body). |

Zelf invullen, alleen melden in de draft:

| Sleutel | Default | Wanneer afwijken |
|---|---|---|
| `ceda-id` | `ceda.<name>` | Nooit wijzigen na aanmaak; hij overleeft hernoemen. |
| `ceda-version` | `"0.1.0"` | Bump bij inhoudelijke wijziging. Quoten, anders is het geen string. |
| `ceda-activation` | `command` bij workflow, `ambient` bij reference | `hook` bij runtime-afdwinging, `scheduled` bij cron, `chained` als alleen een andere workflow hem aanroept. |
| `ceda-binding` | `default` | `hard` alleen als er echt een hook is die het tegenhoudt. |
| `ceda-execution` | `inline` | `isolated` als de output comprimeert, `deterministic` bij een script of hook zonder model in de lus. |

## Gebundelde bestanden staan in de body, niet in de frontmatter

Er is geen `bundles:`-veld in de spec, en een laadconditie in de frontmatter zou toch niets
doen: de agent leest de body, niet onze metadata. Zet ze dus in een sectie onderaan
`SKILL.md`, met per bestand de conditie waaronder het gelezen moet worden:

```markdown
## Gebundelde bestanden

- `references/gotchas.md` — lees altijd, voor je iets voorstelt
- `references/api-errors.md` — lees als de API iets anders dan 200 teruggeeft
- `scripts/hr-status.sh <release> <namespace>` — draaien, niet lezen: geeft een
  gezondheidssamenvatting in één keer
```

"Zie references/ voor details" werkt niet — dan wordt het of altijd of nooit gelezen. Eén hop
diep: een bundle die naar een bundle verwijst is een skill die zichzelf niet meer overziet.

## Wat de validator controleert

`scripts/validate-skill.py` faalt op:

- `name` buiten de spec-regels of ongelijk aan de directorynaam
- `description` leeg of boven 1024 tekens
- `allowed-tools` als YAML-lijst in plaats van een spatie-gescheiden string
- CEDA-metadata op topniveau in plaats van onder `metadata:`
- een waarde buiten de toegestane set van `ceda-type`, `-subtype`, `-origin`, `-activation`,
  `-binding`, `-execution`, `-scope`, `-verifies`
- `ceda-binding: hard` zonder `ceda-activation: hook`
- `ceda-origin: extended` zonder `ceda-upstream`
- ontbrekende `ceda-source`
- `ceda-scope: user`, of `ceda-source: self` met `ceda-scope: project`
- `ceda-subtype` op een niet-reference
- een bestand in `references/`, `assets/` of `scripts/` dat nergens in de body genoemd wordt
- `SKILL.md` boven de 500 regels zonder gebundelde bestanden
- `ceda-verifies: none` zonder motivatie in de body

Waarschuwingen: overlappende triggerwoorden zonder exclusion-clause, ontbrekende
`allowed-tools` (fout bij `ceda-origin: external`), ontbrekende `ceda-id`/`ceda-version`,
tijdsgebonden description, `ceda-source: intern:` (reviewer moet controleren of de skill
zelfstandig leesbaar is).

Draai daarnaast de referentie-validator van de spec zelf als je die hebt:
`skills-ref validate ./<skill>`.
