# CLAUDE.md-baseline en sessie-lifecycle-skills

**Datum:** 2026-08-14 · **Status:** ontwerp, goedgekeurd · **Eigenaar:** [@CorneeldH](https://github.com/CorneeldH)

## Probleem

Drie dingen die nu ontbreken of botsen:

1. **Geen CEDA-brede CLAUDE.md.** Elke repo verzint z'n eigen, of heeft er geen. Werk dat elke sessie opnieuw uitgelegd moet worden.
2. **Twee momenten in het werk worden structureel gemist.** Aan het begin: isolatie in een worktree, en nadenken vóór bouwen. Aan het eind: terugkijken en de context opschonen in plaats van doorrollen met een volle context.
3. **Skill-dubbeling.** De CEDA-skill `brainstorm` is een bijna-kloon van `superpowers:brainstorming`, terwijl twee superpowers-skills die CEDA wél mist (`using-git-worktrees`, `writing-plans`) niet beschikbaar zijn voor het team — superpowers is een persoonlijke plugin, geen org-tooling.

## Uitgangspunten

Deze zijn vastgesteld tijdens de brainstorm en liggen vast.

- **Doelgroep is het CEDA-team**, niet één persoon. Alles wat we opleveren moet werken voor iemand zonder persoonlijke plugins. Distributie loopt via `cedanl/.github` → dev-dots-container.
- **Vendoren, niet dedupliceren.** `brainstorm` blijft bestaan; iemand heeft eraan gewerkt. We vullen aan wat ontbreekt.
- **Het sessie-einde wordt een CLAUDE.md-regel, geen hook.** Bewust advies in plaats van dwang, om mee te starten.
- **Claude besluit zelf dát het een eindpunt is, maar voert niets uit.** De gebruiker kiest of reflectie en `/clear` gebeuren.
- **De template gaat mee bij repo-init.** Elke repo bezit z'n eigen CLAUDE.md; geen centrale import.
- **CLAUDE.md blijft minimaal.** Alles wat maar soms relevant is, wordt een skill.

### Waarom minimaal

Uit de Claude Code-documentatie: CLAUDE.md wordt elke sessie geladen, dus alleen wat breed geldt hoort erin; domeinkennis en incidentele workflows horen in skills, die on-demand laden. "The over-specified CLAUDE.md" staat expliciet in de lijst met veelgemaakte fouten — te lang betekent dat Claude de helft negeert. De toets per regel is: *zou weglaten hiervan tot een fout leiden?*

### Waarom de sessie-lifecycle dan wél in CLAUDE.md hoort

Skills triggeren automatisch op hun `description`, gematcht tegen wat de gebruiker zegt. Dat werkt voor "maak een presentatie" of "welke grafiek past hier". Het werkt niet voor triggers die aan een *moment* hangen in plaats van aan een uiting: er is geen zin die de gebruiker uitspreekt bij "we staan op een natuurlijk eindpunt" of "dit wordt straks een commit". Die momenten hebben een instructie nodig die altijd geladen is.

Dat is de scheidslijn die dit hele ontwerp draagt:

| Trigger hangt aan | Voorbeeld | Waar het hoort |
|---|---|---|
| Een uiting van de gebruiker | "maak een marp", "welke grafiek" | skill-`description` |
| Een moment in het werk | vóór de eerste schrijfactie, na het sluiten van een issue | CLAUDE.md |

Een routingtabel voor skills in CLAUDE.md is dus niet nodig, en meestal een pleister op zwakke descriptions. De juiste reparatie daarvoor is `create-skill` + `skills-ontology`.

## Onderdeel 1: skills

### Nieuw: `worktree`

Port van `superpowers:using-git-worktrees` (MIT, © 2025 Jesse Vincent — attributie in de skill). CEDA-branchnaming (`issue-<nr>-<slug>`, `fix-<slug>`). Volgt de bestaande CEDA-skillconventie: `description` en gebruikersgerichte output in het Nederlands, instructietekst in het Engels.

Behoudt de kern van het origineel: eerst detecteren of je al geïsoleerd zit, dan het native mechanisme (`EnterWorktree`) gebruiken, en pas als laatste `git worktree add`. Die volgorde is niet cosmetisch — `git worktree add` gebruiken terwijl er een native tool is, levert worktrees op die de harness niet kent en niet opruimt.

### Nieuw: `plan`

Port van `superpowers:writing-plans`. Twee afwijkingen van het origineel:

- Schrijft naar `docs/plans/`, niet naar `docs/superpowers/plans/`.
- Koppelt aan `/write-issue` in plaats van aan een losse takenlijst, zodat werk in het CEDA-board landt.

### Aangepast: `brainstorm`

Eén sectie erbij: bij een expliciete go is de vervolgstap `/plan`. Nu eindigt de skill in een beslis-samenvatting en houdt het daar op; dat is precies het gat dat `writing-plans` bij superpowers dicht. Geen herschrijving van de rest.

### Ongemoeid

`sparren`, `ship` en `branch-pr` overlappen met superpowers-equivalenten, maar zijn CEDA-specifieker en blijven zoals ze zijn. Buiten scope.

## Onderdeel 2: de template

Bestand: `werkafspraken/_claude-md-template.md`. De `<...>`-plekken worden per repo ingevuld.

```markdown
# <Repo> — projectinstructies

<Eén zin: wat dit is.> Stack: <taal + versie, framework, package manager>.

## Commando's
- Draaien: `<commando>`
- Testen: `<commando>` — draai gericht één testbestand, niet de hele suite
- Linten: `<commando>`

## Sessie-start
- **Worktree vóór de eerste schrijfactie.** Elke wijziging die een commit wordt,
  begint met `/worktree` op een eigen branch (`issue-<nr>-<slug>`). Niet achteraf
  verplaatsen. Uitzonderingen: read-only werk, en als de gebruiker "op main" zegt.
- **Bouw je iets nieuws of verander je gedrag? Eerst `/brainstorm`.** Geen code,
  geen bestanden, geen "snelle POC" vóór een expliciete go.
- **Meerdere stappen of meerdere bestanden? Na de go `/plan`.** Is de diff in één
  zin te beschrijven, sla planning over.

## Sessie-einde
Je signaleert dit zelf — de gebruiker hoeft er niet om te vragen. Het is een
natuurlijk eindpunt als één van deze waar is:
- een issue is gesloten of een PR is geopend
- een plan is afgerond
- je bent klaar met een op zichzelf staand stuk werk en het volgende is een ander onderwerp
- je hebt jezelf twee keer op hetzelfde punt moeten corrigeren

Rol dan **niet** door naar het volgende. Zeg dat je op een natuurlijk eindpunt
staat, en bied twee dingen aan:
- `/sessie-terugblik` draaien — alleen als de gebruiker ja zegt, nooit uit jezelf
- daarna `/clear`, met het volgende commando of doel als kant-en-klare
  copy-paste-regel erbij

Zegt de gebruiker niets over terugblikken en gaat hij door? Prima, laat het los
en kom er niet op terug.

Uitzondering: een strak gekoppelde vervolgstap (repareren wat je net brak, één
taak over meerdere berichten) blijft in dezelfde sessie.

Reden: lange sessies stapelen verouderde context op → tragere, slechtere output.

## Bestandsverwijzingen
Verwijs naar een bestand altijd als aanklikbare markdown-link, relatief vanaf de
root van de workspace: `[naam](pad/naar/bestand.md)`, een regel met `#L42`. Nooit
een kaal pad tussen backticks — dat kan de gebruiker niet openen. Dit geldt net
zo goed in de chat als in markdown-bestanden. Werk je in een worktree onder
`.claude/worktrees/<naam>/`, dan hoort dat stuk in het pad.

## Bij compacteren
Bewaar altijd: de lijst gewijzigde bestanden, de testcommando's en openstaande
beslissingen.

## Skills
De CEDA-skills laden zichzelf op basis van hun description. Roep ze desnoods
expliciet aan met `/naam`. Nooit `gh issue create` — gebruik `/write-issue`.

## Valkuilen
<Per repo aanvullen zodra iets twee keer misgaat. Leeg beginnen is prima.>
```

Ingevuld is dat ongeveer 45 regels.

### Wat er bewust wél in staat ondanks "minimaal"

- **`/write-issue` in plaats van `gh issue create`** — zonder die zin doet Claude uit zichzelf `gh issue create`. Weglaten veroorzaakt een fout, dus het blijft.
- **Gericht testen** — anders draait Claude standaard de volledige suite.
- **Aanklikbare bestandsverwijzingen** — zonder die regel levert Claude kale paden tussen backticks, die de gebruiker niet kan openen. Tijdens deze brainstorm zelf misgegaan.
- **Lege valkuilen-sectie** — de plek waar het bestand per repo mag groeien, op bewijs.

### Wat er bewust níet in staat

Modulemap, architectuurbeschrijving, codestijlregels, en verwijzingen naar `standards/` en `werkafspraken/`. Die leest Claude zelf uit de code, of ze zitten al in skills. Codestijl is bovendien werk voor een linter, niet voor een taalmodel.

## Onderdeel 3: de werkafspraak

Bestand: `werkafspraken/claude-md.md`, volgens `_template.md`.

- **Niveau: Experiment.** CLAUDE.md-tekst is advies, geen garantie: het model kan het missen. Dat hoort eerlijk in de afspraak te staan, en Experiment is het niveau dat daarbij past.
- **Eigenaar:** @CorneeldH.
- Opgenomen in de tabel in `werkafspraken/README.md`, in de `nav` van `mkdocs.yml`, en met de mirror onder `docs/werkafspraken/`.

## Onderdeel 4: `cedafy-claude-md`

Skill die de template toepast op een bestaande repo. Bestaat er nog geen CLAUDE.md, dan is het invullen en klaar.

### Werking

1. **Lezen** — de template plus de bestaande `CLAUDE.md`.
2. **Repo uitlezen** — stack, package manager, en de test-, lint- en run-commando's, voor de `<...>`-plekken.
3. **Per template-punt classificeren** in drie bakken:
   - *ontbreekt* — staat niet in de huidige CLAUDE.md
   - *al gedekt* — de huidige tekst zegt hetzelfde in andere woorden
   - *tegenstrijdig* — de huidige tekst zegt iets anders
4. **Ontbrekend → direct invoegen.** Geen vraag; dat is de winst van de skill.
5. **Al gedekt → niets doen.** Geen tweede regel die hetzelfde zegt.
6. **Tegenstrijdig → `AskUserQuestion`**, per punt, met drie opties: de template volgen, de huidige regel houden, of combineren. Bij "combineren" staat de voorgestelde gecombineerde tekst in de optie zelf, zodat de keuze concreet is. Maximaal vier vragen per aanroep, dus gebatcht.
7. **Wegschrijven** — de antwoorden verwerkt, repo-eigen secties ongemoeid, plus een kort overzicht van wat is toegevoegd, wat is overgeslagen, en wat de gebruiker heeft beslist.

### Wat telt als tegenstrijdig

| Huidige CLAUDE.md | Template | Classificatie |
|---|---|---|
| "werk gewoon op main" | worktree vóór eerste schrijfactie | tegenstrijdig |
| "draai altijd de volledige suite" | gericht één testbestand | tegenstrijdig |
| "vraag altijd eerst om bevestiging" | brainstorm vóór bouwen | al gedekt |
| eigen commit-flow met extra stappen | geen tegenhanger | repo-eigen, ongemoeid |

Twijfelgeval telt als tegenstrijdig, dus wordt er gevraagd. Liever een vraag te veel dan een stilzwijgend overschreven afspraak.

### Wat de skill nooit doet

Repo-eigen secties verwijderen, of het bestand herschrijven naar de volgorde van de template. Invoegen en aanpassen, niet vervangen.

### Buiten scope

De omgekeerde richting — signaleren dat een repo-eigen regel eigenlijk in de org-template thuishoort. Dat vraagt zicht op álle CLAUDE.md's tegelijk en hoort bij repo-context-as-data, niet bij deze skill.

## Onderdeel 5: haakje in `init-repo`

`init-repo` schrijft de template naar nieuwe repos. Bestaande repos worden niet automatisch bijgewerkt; die draaien eenmalig `cedafy-claude-md`.

## Volgorde van uitvoeren

1. **`sessie-terugblik` landen.** Staat nu uncommitted in worktree `skills/lifecycle` (daar nog onder de oude naam `sessie-reflectie`). Zonder deze stap verwijst de template naar een skill die niet bestaat. Harde voorwaarde voor stap 4.
2. `worktree` en `plan` vendoren.
3. `brainstorm` uitbreiden met de `/plan`-eindstap.
4. Template, werkafspraak, `werkafspraken/README.md`-tabel, `mkdocs.yml`-nav en de `docs/`-mirror.
5. `cedafy-claude-md`.
6. Haakje in `init-repo`.

## Definition of Done

- `worktree` en `plan` bestaan als CEDA-skills en komen door de skill-validator.
- `brainstorm` verwijst bij go naar `/plan`.
- `werkafspraken/_claude-md-template.md` bestaat en is ingevuld ≤ 50 regels.
- `werkafspraken/claude-md.md` bestaat op niveau Experiment, staat in de README-tabel, in de mkdocs-nav en heeft een mirror onder `docs/werkafspraken/`.
- `cedafy-claude-md` bestaat, en is gedraaid op minstens één bestaande repo mét eigen CLAUDE.md, waarbij een tegenstrijdigheid daadwerkelijk als vraag is voorgelegd.
- `init-repo` schrijft de template naar nieuwe repos.

## No-gos

- Geen hooks in deze ronde. Het sessie-einde blijft tekst.
- Geen opruiming van `sparren`, `ship` of `branch-pr`.
- Geen superpowers-plugin org-breed installeren.
- Geen automatische uitrol over bestaande repos.
- Geen routingtabel voor skills in CLAUDE.md.
