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

- **Automatisch aan.** De `claude`-functie in de container kijkt naar de origin van de repo. Staat daar `cedanl/` of `surf-internal/npuls/ceda/` in, dan schakelt hij Entire in en zet hij de checkpoint-remote en -opslag goed. Dat gebeurt bij elke start van `claude`.
- **Checkpoints gaan naar de centrale repo.** Alle sessiedata wordt gesynchroniseerd naar `cedanl/entire-checkpoints` bij `git push`. Zo heeft iedereen toegang tot dezelfde sessiegeschiedenis, zonder dat de projectrepos vol session-data raken.
- **Eén branch, geen losse refs.** Entire kan checkpoints opslaan als losse git-refs (`refs/entire/checkpoints/…`) of op een gedeelde branch. Refs zie je niet in de branchlijst op GitHub. Wij kiezen de branch `entire/checkpoints/v1`, zodat alles op één plek zichtbaar is. Checkpoints van vóór deze keuze (ID's van 26 tekens) staan als kopie op die branch, maar `entire checkpoint explain` leest ze alleen via de refs.
- **Niet in persoonlijke repos.** Entire activeert alleen in repos van `cedanl` of de CEDA-groep op GitLab. In je eigen forks of persoonlijke projecten gebeurt er niets.
- **Wat komt erin en wie leest mee.** Een checkpoint bevat het hele transcript: je prompts, tool-uitvoer en de bestanden die de agent las. Iedereen met toegang tot `cedanl/entire-checkpoints` kan dat lezen, ook collega's die er zelf niet naar schrijven. Laad dus geen data met persoonsgegevens in een sessie en lees de afspraak [Feedback zonder persoonsgegevens](feedback-zonder-persoonsgegevens.md).
- **Controleer de status.** Twijfel je of Entire aan staat? Draai `entire status` — die toont de huidige configuratie en of er een sessie loopt.
- **Configuratie niet zelf aanpassen.** De configuratie staat lokaal per repo in `.entire/` (niet gecommit) en wordt door de `claude`-functie gezet. Pas die niet met de hand aan — dan loopt jouw omgeving uit de pas met de rest van het team. Gaat er iets mis met een gedeelde branch (bijvoorbeeld een botsende push), draai dan `entire doctor`.

## Achtergrond

- [Entire.io documentatie](https://docs.entire.io) — de officiële docs met installatie, commando's en concepten.
- [entireio/cli](https://github.com/entireio/cli) — de bron van de CLI, open source (MIT, Go).
- [cedanl/entire-checkpoints](https://github.com/cedanl/entire-checkpoints) — de centrale repo waar alle checkpoints naartoe gaan.
- [dev-dots #3](https://github.com/cedanl/dev-dots/issues/3) — de origin story van de agentic coding omgeving.
- [Guide: Entire CLI](../guides/entire-cli.md) — uitgebreide technische handleiding met installatie, gebruik en troubleshooting.

## Afwijken

Wil je Entire in een niet-CEDA repo gebruiken, de configuratie aanpassen of niet meedoen? Dat loopt via [@Tomeriko96](https://github.com/Tomeriko96), met akkoord van [@CorneeldH](https://github.com/CorneeldH). Let op: `entire disable` helpt niet blijvend, want `claude` zet Entire bij de volgende start weer aan.
