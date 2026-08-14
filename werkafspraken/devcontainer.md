# Devcontainer

**Niveau:** Verplicht · **Eigenaar:** [@Tomeriko96](https://github.com/Tomeriko96) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Je ontwikkelt in een devcontainer die centraal in beheer is. De default is [cedanl/dev-dots](https://github.com/cedanl/dev-dots). Een eigen container in je eigen repo mag, in overleg met [@Tomeriko96](https://github.com/Tomeriko96).

## Waarom

- **Entire draait mee.** Onze AI-tooling is onderdeel van de omgeving, niet iets dat je er per machine bij installeert.
- **Gedeelde skills.** De org-skills uit `cedanl/.github` zitten in de container, dus iedereen werkt met dezelfde set.
- **Dezelfde versies.** uv, node, az, kubectl, helm en de rest zijn voor iedereen gelijk. "Werkt bij mij wel" is dan een echt signaal in plaats van ruis.
- **Onboarding in één handeling.** Een nieuwe collega hoeft geen dag aan installeren te besteden.

## In de praktijk

- Werkt in VS Code, Positron, de terminal en GitHub Codespaces. Kies wat je gewend bent; je hoeft niet van editor te wisselen.
- Draai na het opstarten éénmalig `onboard`. Dat regelt de authenticatie voor `gh`, `claude` en `opencode`, en zet je git-identiteit expliciet (`user.useConfigOnly true`) — commits van meerdere mensen in dezelfde container blijven daardoor uit elkaar te houden.
- Claude Code en OpenCode starten met `--dangerously-skip-permissions`, als alias ingebakken. Dat is een bewuste keuze: de container ís de sandbox. Buiten de container zet je die vlag niet aan.
- Podman werkt als je geen Docker Desktop wilt of mag draaien.
- **Iets ontbreekt of zit je in de weg?** Pas de container niet stilletjes lokaal aan — dan lost het probleem alleen voor jou op en loopt jouw omgeving weer uit de pas. Open een issue of PR op [dev-dots](https://github.com/cedanl/dev-dots/issues); dan heeft iedereen er wat aan.
- **Overweldigd door de hoeveelheid tooling?** Dat is een bekend punt en geen persoonlijk falen. Je hebt maar een handvol commando's nodig om te beginnen; de rest kom je vanzelf tegen. Voor wie nieuw is in agentic coding werken we aan een kalere variant (zie de achtergrond hieronder).

## Achtergrond

- [DevPod: Improving Developer Productivity at Uber](https://www.uber.com/nl/en/blog/devpod-improving-developer-productivity-at-uber/) — waarom centraal beheerde ontwikkelomgevingen schalen waar lokale setups uiteen gaan lopen; dit is het patroon waar dev-dots een kleine versie van is.
- [dev-dots README](https://github.com/cedanl/dev-dots) — wat er precies in de container zit en hoe je hem start.
- [dev-dots #3 — Agentic coding omgeving voor DAIR](https://github.com/cedanl/dev-dots/issues/3) — de kale instapvariant. Expliciet niet de volle container, omdat die intimiderend is voor wie het concept nog niet kent.

## Afwijken

Meld het als issue op [cedanl/dev-dots](https://github.com/cedanl/dev-dots/issues). Een eigen container in je eigen repo loopt via [@Tomeriko96](https://github.com/Tomeriko96), met akkoord van [@CorneeldH](https://github.com/CorneeldH).
