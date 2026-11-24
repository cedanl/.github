# Entire — AI-sessies vastleggen

**Niveau:** Experiment · **Eigenaar:** [@Tomeriko96](https://github.com/Tomeriko96) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Je werkt met Entire in alle CEDA-repos: de GitHub-org `cedanl` en de GitLab-groep `surf-internal/npuls/ceda` (git.sdp.surf.nl). De devcontainer activeert het automatisch bij het starten van Claude Code. Checkpoints gaan van beide platforms naar dezelfde private GitHub-repo `cedanl/entire-checkpoints`, op de branch `entire/checkpoints/v1`.

## Waarom

- **Herleidbaarheid.** Elke codeverandering is te herleiden naar de prompt die hem veroorzaakte — geen "wie heeft dit geschreven?" maar "welke sessie heeft dit opgeleverd?".
- **Sessies hervatten.** Als een collega is gestopt of een sessie crasht, pak je precies daar weer op waar het ophield.
- **Audit trail.** Voor projecten waar traceerbaarheid van AI-werk belangrijk is, liggen de prompts, tool-calls en transcripts vast naast de commits.
- **Geen extra handeling.** Het draait mee in de container, je hoeft niks te installeren of te onthouden.

## In de praktijk

- **Automatisch aan.** De `claude`-functie in de container draait `entire-setup`. Dat zet Entire aan voor de repo waar je staat én voor elke repo direct onder `/workspaces/dev-dots`, voor elke repo met `cedanl/` of `surf-internal/npuls/ceda/` in de origin. Het maakt dus niet uit of je Claude in de projectmap of in de root start. Dat geldt vanaf [dev-dots#49](https://github.com/cedanl/dev-dots/pull/49); een oudere container zet Entire alleen aan in de map waar je `claude` start.
- **Zonder container, op je Mac.** Werk je in de Code-tab van de Claude-app op macOS, dan zet je Entire zelf aan met dezelfde checkpoint-remote. De stappen staan in de guide onder [Op je eigen Mac met Claude Desktop](../guides/entire-cli.md#op-je-eigen-mac-met-claude-desktop). In de Chat-tab werkt Entire niet.
- **Checkpoints gaan naar de centrale repo.** Alle sessiedata wordt gesynchroniseerd naar `cedanl/entire-checkpoints` bij `git push`. Zo heeft iedereen toegang tot dezelfde sessiegeschiedenis, zonder dat de projectrepos vol session-data raken.
- **Eén branch, geen losse refs.** Entire kan checkpoints opslaan als losse git-refs (`refs/entire/checkpoints/…`) of op een gedeelde branch. Refs zie je niet in de branchlijst op GitHub. Wij kiezen de branch `entire/checkpoints/v1`, zodat alles op één plek zichtbaar is. Checkpoints van vóór deze keuze (ID's van 26 tekens) staan als kopie op die branch, maar `entire checkpoint explain` leest ze alleen via de refs.
- **Niet in persoonlijke repos.** Entire activeert alleen in repos van `cedanl` of de CEDA-groep op GitLab. In je eigen forks of persoonlijke projecten gebeurt er niets.
- **Wat komt erin en wie leest mee.** Een checkpoint bevat het hele transcript: je prompts, tool-uitvoer en de bestanden die de agent las. Iedereen met toegang tot `cedanl/entire-checkpoints` kan dat lezen, ook collega's die er zelf niet naar schrijven. Laad dus geen data met persoonsgegevens in een sessie en lees de afspraak [Feedback zonder persoonsgegevens](feedback-zonder-persoonsgegevens.md).
- **Controleer de status.** Twijfel je of Entire aan staat? Draai `entire status` — die toont de huidige configuratie en of er een sessie loopt.
- **Configuratie niet zelf aanpassen.** De configuratie staat lokaal per repo in `.entire/` (niet gecommit) en wordt door de `claude`-functie gezet. Pas die niet met de hand aan — dan loopt jouw omgeving uit de pas met de rest van het team. Controleer of het klopt met `entire-setup --check`. Gaat er iets mis met een gedeelde branch (bijvoorbeeld een botsende push), draai dan `entire doctor`.

## Laat je agent het regelen

Vraag je je agent om Entire te installeren of aan te zetten, geef dan deze tekst. Die werkt vanuit elke map, ook in een oudere container, en laat de agent zelf controleren of het klopt.

````text
Zet Entire aan voor mijn CEDA-repo's en controleer dat het werkt.

1. Draai `entire-setup`. Bestaat dat commando niet (oudere container), draai dan voor elke
   repo die ik gebruik met origin `cedanl/` of `surf-internal/npuls/ceda/`:
     entire enable -y --agent claude-code
     entire configure --checkpoint-backend branch --checkpoint-remote github:cedanl/entire-checkpoints
   Staat `.entire/settings.json` in git, voeg dan `--local` toe aan `entire configure`.
   Zet `/.entire/` en `/.claude/settings.local.json` in `.git/info/exclude`.
2. Controleer met `entire-setup --check` (of `entire status` per repo). Elke CEDA-repo moet
   "Enabled" tonen met `cedanl/entire-checkpoints` als checkpoint-remote.
3. Toon de volledige uitvoer van stap 1 en 2. Gaat er iets mis, noem dan de repo en de
   foutmelding. Verzin geen omweg.

Niet doen: `.entire/` of `.claude/settings.local.json` committen; `entire disable`,
`entire clean` of `entire doctor --force` draaien; een andere Entire-versie installeren;
Entire aanzetten in repo's die geen CEDA-repo zijn.
````

**Controleer het achteraf.** Laat de agent een kleine wijziging committen en `git log -1 --format=%B` tonen. Daar hoort een regel `Entire-Checkpoint: …` in te staan. Ontbreekt die, dan staat het niet goed.

### De beste instellingen

| Instelling | Waarde | Waarom |
|------------|--------|--------|
| Checkpoint-remote | `github:cedanl/entire-checkpoints` | Eén plek voor het hele team, ook voor repo's op GitLab. |
| Opslag | `git-branch` (`entire/checkpoints/v1`) | Alles zichtbaar op één branch, in plaats van losse refs. |
| Agent | `claude-code` | De hooks voor Claude Code. |
| Waar de config staat | lokaal per repo (`.entire/` in `.git/info/exclude`) | Niets in de projectrepo's committen. Staat `.entire/settings.json` al in git, pas dan alleen `settings.local.json` aan. |
| Versie | gepind in de Dockerfile van dev-dots (`ENTIRE_VERSION`) | Iedereen dezelfde CLI. |
| Waar je start | maakt niet uit | `entire-setup` loopt alle repo's onder de workspace-root langs. |

## Achtergrond

- [Entire.io documentatie](https://docs.entire.io) — de officiële docs met installatie, commando's en concepten.
- [entireio/cli](https://github.com/entireio/cli) — de bron van de CLI, open source (MIT, Go).
- [cedanl/entire-checkpoints](https://github.com/cedanl/entire-checkpoints) — de centrale repo waar alle checkpoints naartoe gaan.
- [dev-dots #3](https://github.com/cedanl/dev-dots/issues/3) — de origin story van de agentic coding omgeving.
- [Guide: Entire CLI](../guides/entire-cli.md) — uitgebreide technische handleiding met installatie, gebruik en troubleshooting.

## Afwijken

Wil je Entire in een niet-CEDA repo gebruiken, de configuratie aanpassen of niet meedoen? Dat loopt via [@Tomeriko96](https://github.com/Tomeriko96), met akkoord van [@CorneeldH](https://github.com/CorneeldH). Voor jezelf uitzetten kan direct: `git config devdots.entire false` (alleen die repo) of `export DEVDOTS_ENTIRE=0` (alle repo's). `entire disable` helpt niet blijvend, want `claude` zet Entire bij de volgende start weer aan. Bij de eerste keer in een repo toont de container een melding met deze opties.
