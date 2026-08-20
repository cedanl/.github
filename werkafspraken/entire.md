# Entire — AI-sessies vastleggen

**Niveau:** Experiment · **Eigenaar:** [@Tomeriko96](https://github.com/Tomeriko96) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Je werkt met Entire aan in cedanl/-repos. De devcontainer activeert het automatisch bij het starten van Claude Code. Checkpoints worden gesynchroniseerd naar `cedanl/entire-checkpoints`.

## Waarom

- **Herleidbaarheid.** Elke codeverandering is te herleiden naar de prompt die hem veroorzaakte — geen "wie heeft dit geschreven?" maar "welke sessie heeft dit opgeleverd?".
- **Sessies hervatten.** Als een collega is gestopt of een sessie crasht, pak je precies daar weer op waar het ophield.
- **Audit trail.** Voor projecten waar traceerbaarheid van AI-werk belangrijk is, liggen de prompts, tool-calls en transcripts vast naast de commits.
- **Geen extra handeling.** Het draait mee in de container, je hoeft niks te installeren of te onthouden.

## In de praktijk

- **Automatisch aan.** De `claude`-functie in de container detecteert of je in een `cedanl/`-repo zit en schakelt Entire in bij de eerste aanroep. Je ziet dit terug in het onboarding-overzicht.
- **Checkpoints gaan naar de centrale repo.** Alle sessiedata wordt gesynchroniseerd naar `cedanl/entire-checkpoints` bij `git push`. Zo heeft iedereen toegang tot dezelfde sessiegeschiedenis, zonder dat de projectrepos vol session-data raken.
- **Niet in persoonlijke repos.** Entire activeert alleen in repos met `cedanl/` als origin. In je eigen forks of persoonlijke projecten gebeurt er niets.
- **Controleer de status.** Twijfel je of Entire aan staat? Draai `entire status` — die toont de huidige configuratie en of er een sessie loopt.
- **Niet de bedoeling om aan te passen.** De Entire-configuratie zit in `.entire/settings.json` in dev-dots. Pas die niet lokaal aan — dan loopt jouw omgeving uit de pas met de rest van het team.

## Achtergrond

- [Entire.io documentatie](https://docs.entire.io) — de officiële docs met installatie, commando's en concepten.
- [entireio/cli](https://github.com/entireio/cli) — de bron van de CLI, open source (MIT, Go).
- [cedanl/entire-checkpoints](https://github.com/cedanl/entire-checkpoints) — de centrale repo waar alle checkpoints naartoe gaan.
- [dev-dots #3](https://github.com/cedanl/dev-dots/issues/3) — de origin story van de agentic coding omgeving.
- [Guide: Entire CLI](../guides/entire-cli.md) — uitgebreide technische handleiding met installatie, gebruik en troubleshooting.

## Afwijken

Wil je Entire in een niet-cedanl repo gebruiken of de configuratie aanpassen? Dat loopt via [@Tomeriko96](https://github.com/Tomeriko96), met akkoord van [@CorneeldH](https://github.com/CorneeldH).
