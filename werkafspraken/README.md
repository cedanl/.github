# CEDA Werkafspraken

Hoe we bij CEDA samenwerken: welke omgeving je gebruikt, hoe je presenteert, hoe werk het team in komt. Dit gaat over de manier van werken — voor hoe code eruitziet en repos zijn opgebouwd, zie de [standards](https://github.com/cedanl/.github/tree/main/standards).

Doelgroep is het CEDA-kernteam.

## Overzicht

| Afspraak | Niveau | Eigenaar |
|----------|--------|----------|
| [Devcontainer](https://github.com/cedanl/.github/blob/main/werkafspraken/devcontainer.md) | Verplicht | [@Tomeriko96](https://github.com/Tomeriko96) |
| [Presentaties](https://github.com/cedanl/.github/blob/main/werkafspraken/presentaties.md) | Verplicht | [@EdwinLieftink](https://github.com/EdwinLieftink) |
| [Pitches](https://github.com/cedanl/.github/blob/main/werkafspraken/pitches.md) | Verplicht | [@CorneeldH](https://github.com/CorneeldH) |
| [Gebruikersrechten](https://github.com/cedanl/.github/blob/main/werkafspraken/gebruikersrechten.md) | Verplicht | [@Tomeriko96](https://github.com/Tomeriko96) |
| [Entire](https://github.com/cedanl/.github/blob/main/werkafspraken/entire.md) | Experiment | [@Tomeriko96](https://github.com/Tomeriko96) |

## Niveaus

| Niveau | Betekenis |
|--------|-----------|
| **Verplicht** | Zo doen we het. Afwijken alleen in overleg met de eigenaar, met akkoord van de team lead. |
| **Aanbevolen** | Dit is de default. Wijk af als je een reden hebt, en laat weten waarom. |
| **Experiment** | We proberen dit uit. Doe mee en deel je ervaring — daarna besluiten we of het aanbevolen of verplicht wordt. |

## Een afspraak toevoegen of wijzigen

1. Kopieer `_template.md` naar `werkafspraken/<onderwerp>.md`, of pas een bestaand bestand aan.
2. Zet het onderwerp in de tabel hierboven en in de `nav` van `mkdocs.yml`.
3. Voeg de mirror toe onder `docs/werkafspraken/` (één `include-markdown`-blok, zie de bestaande bestanden).
4. Open een PR. Review door de eigenaar van de afspraak plus [@CorneeldH](https://github.com/CorneeldH) als team lead.

Elke afspraak heeft een genoemde eigenaar. Weet je niet zeker of iets een werkafspraak moet worden? Begin dan op niveau **Experiment** — dat is goedkoper dan een discussie over een verplichting.

## Waarom dit bestaat

Afspraken die alleen in iemands hoofd of in een Slack-draadje leven, moet elke nieuwe collega opnieuw ontdekken. Ze hier neerzetten maakt ze vindbaar, bespreekbaar en veranderbaar via een PR.
