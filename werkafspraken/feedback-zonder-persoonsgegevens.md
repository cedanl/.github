# Feedback zonder persoonsgegevens

**Niveau:** Verplicht · **Eigenaar:** [@Tomeriko96](https://github.com/Tomeriko96) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Ingezonden feedback (uit een app, enquête of sessie) gaat nooit met persoonsgegevens naar GitHub, ook niet naar een private repo. Je haalt ze weg voordat de data in een repo komt.

## Waarom

- **Eenmaal gepusht, blijft het staan.** Een commit leeft voort in de git-history, in forks en in kloons. Een bestand verwijderen haalt de data daar niet weg.
- **Private is geen vrijbrief.** Repo's kunnen later publiek worden of breder gedeeld worden. De toegang is dan niet meer wat de inzender verwachtte.
- **Mensen gaven feedback, geen gegevens.** Wie een mening deelt, rekent niet op een e-mailadres of naam in ons archief.

## In de praktijk

- **Wat telt als persoonsgegeven:** e-mailadressen, namen, gebruikersnamen, telefoonnummers en ID's waarmee je naar een persoon kunt terugzoeken (bijvoorbeeld een account- of werkboek-ID). Vrije tekst kan dit allemaal bevatten, ook in een toelichting of een contactveld.
- **Haal het eruit bij de bron.** Filter terwijl je de data ophaalt, zodat er nooit een ongefilterd bestand op schijf of in je werkmap staat.
- **Laat identificerende kolommen weg** in plaats van ze te vervangen door een placeholder. Een kolom vol `[verwijderd]` voegt niets toe.
- **Lees de vrije tekst zelf door.** Een zoekactie op `@` vindt geen namen onder een compliment. Controleer ook op telefoonnummers.
- **Beperk de periode en omgeving** tot wat je nodig hebt, bijvoorbeeld één omgeving en vanaf een datum. Wat je niet ophaalt, kan niet lekken.
- **Is het toch gepusht?** Meld het direct bij de eigenaar. Een commit terugdraaien is niet genoeg; de history moet worden herschreven en de eigenaar beslist of de inzenders een melding krijgen.
- Welke velden gevoelig zijn staat in de [data-conventies](https://github.com/cedanl/.github/blob/main/standards/data-conventions.md) (veld `sensitive`).

## Achtergrond

- [Data-conventies](https://github.com/cedanl/.github/blob/main/standards/data-conventions.md) — het veld `sensitive` voor persoonsgegevens.

## Afwijken

Feedback met persoonsgegevens op GitHub zetten kan alleen met toestemming van de inzenders én akkoord van [@Tomeriko96](https://github.com/Tomeriko96) en [@CorneeldH](https://github.com/CorneeldH). Meld de afwijking bij de eigenaar.
