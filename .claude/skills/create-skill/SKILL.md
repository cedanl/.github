---
name: create-skill
description: Scaffold een nieuwe CEDA Claude skill via een begeleide workflow. Gebruik wanneer iemand een nieuwe /skill wil aanmaken voor de cedanl organisatie, een bestaand proces wil codificeren als skill, of vraagt hoe je een skill bouwt.
---

# Create Skill

Begeleid de gebruiker stap voor stap bij het bouwen van een nieuwe Claude skill voor de cedanl organisatie. De skill zorgt dat het resultaat aansluit bij de CEDA-conventies en daadwerkelijk triggert wanneer dat hoort.

## Workflow

When the user invokes `/create-skill [optional: beschrijving]`:

### 1. Prior art check

Lees de bestaande skills om dubbel werk te voorkomen en referenties te hebben:

```bash
ls .claude/skills/
```

Lees ook de SKILL.md van de meest vergelijkbare skill (op basis van de beschrijving van de gebruiker) als referentie voor structuur en tone-of-voice.

Rapporteer kort wat er al bestaat en of er overlap is. Als een bestaande skill uitgebreid kan worden in plaats van een nieuwe te bouwen, stel dat voor aan de gebruiker en stop hier.

### 2. Interview

Stel de volgende vragen **in één bericht** — niet één voor één:

> **Nieuwe skill aanmaken**
>
> Beantwoord de volgende vragen zodat ik een goede SKILL.md kan genereren:
>
> 1. **Naam** — Hoe heet de skill? (kebab-case, bijv. `check-stijl` of `maak-rapport`)
> 2. **Doel** — Wat doet de skill in één zin? Wat is de concrete output?
> 3. **Trigger** — Wanneer moet Claude deze skill automatisch activeren? Noem 2-3 voorbeeldberichten van een gebruiker die deze skill zou moeten triggeren.
> 4. **Input** — Wat geeft de gebruiker mee? (bijv. een bestandspad, een naam, niets)
> 5. **Type output** — Is de output objectief (een bestand, een commit, een issue) of subjectief (een review, een advies)?

Wacht op de antwoorden van de gebruiker voor je verder gaat.

### 3. Classificeer de skill

Op basis van de antwoorden: bepaal het type skill.

| Type | Kenmerken | Aanpak |
|------|-----------|--------|
| **Actie** | Maakt iets aan of wijzigt iets (bestand, PR, issue, commit) | Workflow met bash-commando's + bevestigingsstap |
| **Review** | Beoordeelt iets (code, stijl, structuur) | Workflow met criteria-tabellen + bevindingen-format |
| **Generatie** | Produceert tekst of inhoud (notities, slides, docs) | Workflow met templates + draft → bevestig → publiceer |
| **Wizard** | Begeleidt door een proces via vragen | Workflow met interview → classificatie → uitvoer |

Noteer intern: welk type is dit? Dit bepaalt de structuur van de gegenereerde SKILL.md.

### 4. Draft de SKILL.md

Genereer een volledige `SKILL.md` op basis van de antwoorden en het type. Gebruik onderstaande conventies:

#### Frontmatter

```yaml
---
name: <kebab-case naam>
description: <één zin — begin met een werkwoord, sluit af met wanneer de skill actief is>
---
```

De `description` is het trigger-signaal waarmee Claude beslist of de skill relevant is. Schrijf hem zo dat hij matcht op de triggerberichten die de gebruiker opgaf.

#### Structuur

```markdown
# <Naam in plain language>

<2-3 zinnen: wat doet de skill, voor wie, en wat is de concrete output.>

## Workflow

When the user invokes `/<naam> [optional: ...]`:

### 1. <Eerste stap>
...

### 2. <Volgende stap>
...

## Important

- <Kritieke randvoorwaarden>
- <Wat de skill expliciet NIET doet>
```

#### Conventies

| Element | Conventie |
|---------|-----------|
| Taal van de skill body | Engels (instructies aan Claude) |
| Taal van user-facing tekst | Nederlands (wat de gebruiker ziet) |
| Bash-commando's | Altijd in een code block |
| Bevestiging bij destructieve acties | Verplicht — toon draft, vraag akkoord |
| Tabellen | Gebruik voor keuzes, classificaties, formats |
| Bevindingen-format | Gebruik kopjes per categorie + ernst-indeling |
| Verwijzingen naar andere skills | Gebruik `/skill-naam` syntax |

#### Actie-skills: bevestigingsstap

Sluit elke actie-skill af met een expliciete bevestiging:

```markdown
### N. Bevestig en voer uit

Toon een samenvatting van wat er aangemaakt/gewijzigd wordt:

> **Klaar om uit te voeren:**
> - [wat er gaat gebeuren]
>
> Doorgaan?

Wacht op akkoord van de gebruiker voor je schrijft, commit of publiceert.
```

### 5. Optimaliseer de description

De `description` in de frontmatter bepaalt of Claude de skill triggert. Controleer:

- Begint met een werkwoord (`Scaffold`, `Draft`, `Check`, `Genereer`)
- Noemt het domein of de context (`CEDA`, `cedanl`, `Npuls`)
- Sluit af met de trigger-conditie (`Gebruik wanneer...`)
- Is maximaal twee zinnen

Vergelijk de description met de triggerberichten die de gebruiker opgaf in stap 2. Als de match zwak is, pas de description aan.

### 6. Toon de draft en wacht op akkoord

Presenteer de volledige gegenereerde SKILL.md aan de gebruiker:

> **Draft SKILL.md voor `/<naam>`**
>
> ```markdown
> <volledige inhoud>
> ```
>
> Klopt dit? Zeg wat je wil aanpassen, of geef akkoord om te schrijven.

Verwerk feedback en herhaal dit totdat de gebruiker akkoord geeft.

### 7. Schrijf de skill

Zodra de gebruiker akkoord geeft:

```bash
mkdir -p .claude/skills/<naam>
```

Schrijf de definitieve SKILL.md naar `.claude/skills/<naam>/SKILL.md`.

Rapporteer:

> **Skill aangemaakt:** `.claude/skills/<naam>/SKILL.md`
>
> Volgende stappen:
> 1. Test de skill met `/create-skill` → kijk of Claude hem triggert op jouw voorbeeldberichten
> 2. Commit en push naar `cedanl/.github` zodat de skill organisatiebreed beschikbaar is
> 3. Gebruik `/write-issue` om een PR aan te maken als je dat nog niet gedaan hebt

## Important

- Schrijf altijd naar `.claude/skills/<naam>/SKILL.md` in de `cedanl/.github` repo — niet in een project-repo
- Genereer nooit een skill die automatisch deployt, publiceert of force-pusht zonder expliciete bevestiging
- Als de gebruiker een bestaand proces wil vastleggen ("ik doe altijd X als Y"), behandel dat als een Actie- of Wizard-skill — vraag door naar de concrete stappen
- Refereer naar bestaande CEDA skills als voorbeeld, niet naar externe voorbeelden
- De skill ondersteunt alleen cedanl-repos — voeg dit toe aan de `## Important` sectie van de gegenereerde skill indien relevant
