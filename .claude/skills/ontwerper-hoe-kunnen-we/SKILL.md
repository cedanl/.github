---
name: hoe-kunnen-we
description: "Genereer 'Hoe kunnen we...'-vragen (How Might We) uit bestaande centrale inzichten binnen het onderwijsdomein (mbo/hbo/wo). Zet een centraal inzicht volgens het WIE/WIL/WANT/MAAR-stramien om in een set ontwerpvragen die breed genoeg zijn voor uiteenlopende oplossingen en smal genoeg om een brainstorm te starten, en toetst elke vraag expliciet op te breed/te smal. Gebruik deze skill altijd wanneer de gebruiker een centraal inzicht, insight statement, empathy map-uitkomst of jobs-to-be-done aanlevert en daar ontwerpvragen, ontwerpkansen of brainstormvragen uit wil halen. Trigger ook bij zinnen als \"How Might We\", \"HMW\", \"hoe kunnen we\", \"centraal inzicht\", \"centrale inzichten\", \"maak hier ontwerpvragen van\", \"vertaal dit inzicht naar een designvraag\", \"waar moeten we op brainstormen\", \"herformuleer dit inzicht als vraag\", of wanneer iemand een inzicht in de vorm 'X wil Y want Z maar W' deelt. Levert de HMW-set in de chat plus een .md-bestand op."
---

# Hoe kunnen we (How Might We)

Elk probleem is een ontwerpkans. Een centraal inzicht beschrijft een spanning: iemand wil iets, om een
reden, maar iets zit in de weg. Een "Hoe kunnen we..."-vraag draait die spanning om naar een
uitnodiging om te ontwerpen — het veronderstelt dat er een oplossing bestaat, zonder die oplossing
al voor te schrijven.

Jouw rol: **je genereert de HMW-vragen zelf** op basis van de aangeleverde centrale inzichten. Je
begeleidt geen workshop — je levert de set, inclusief je eigen kalibratie-oordeel per vraag.

Deze skill werkt in het onderwijsdomein (mbo/hbo/wo): studenten, docenten, opleidingsmanagers,
data-analisten, instellingsbestuur, examencommissies, decanen, studieloopbaanbegeleiders.

---

## Voordat je begint

Deze skill start bij een **bestaand centraal inzicht**. Je genereert centrale inzichten niet zelf — die komen uit
de centrale-inzichten-skill of van de gebruiker.

Een centraal inzicht volgt dit stramien:

- **WIE** — de persoon uit de empathy map
- **WIL** — de activiteit
- **WANT** — het doel, de onderliggende reden
- **MAAR** — de restrictie, het obstakel

> *Centraal inzicht: **Marie** (wie) wil **lekker snel boodschappen doen** (wil), **want** ze wil meer
> tijd overhouden voor leuke dingen met het gezin, **maar** met kleine kinderen winkelen is
> tijdrovend en stressvol.*

**Ontbreekt er een onderdeel?** Vraag het kort na — één ronde, niet meer. Zonder MAAR is er geen
spanning om op te ontwerpen; zonder WANT wordt de HMW oppervlakkig (je ontwerpt dan op de
activiteit in plaats van op de behoefte). WIE en WIL kun je desnoods plausibel invullen en als
aanname markeren.

Krijg je meerdere centrale inzichten tegelijk? Behandel ze afzonderlijk — elk inzicht krijgt zijn eigen set.

---

## De methode

### Stap 1 — Ontleed het inzicht

Benoem per inzicht expliciet de vier onderdelen. Dit lijkt overbodig maar bepaalt de kwaliteit van
alles wat volgt: de MAAR levert de spanning, de WANT levert de richting. Een HMW die alleen op de
WIL leunt, produceert voorspelbare vragen.

Kijk ook naar het **niveau** van het obstakel. Zit de MAAR in het proces, in de vaardigheid van de
persoon, in het systeem eromheen, of in de emotie? Datzelfde inzicht levert per niveau een andere
soort HMW op.

### Stap 2 — Genereer HMW's vanuit meerdere hoeken

Herformuleer het inzicht als vraag door "Hoe kunnen we..." ervoor te zetten. Eén inzicht levert
meerdere goede vragen op — dat is de bedoeling, niet een teken van besluiteloosheid.

Genereer **5 tot 8 HMW's per inzicht**, verdeeld over verschillende invalshoeken. Gebruik deze
hoeken als generator, niet als checklist die je krampachtig volmaakt:

| Hoek | Vraagvorm | Voorbeeld |
|---|---|---|
| **Verwijder het obstakel** | Hoe kunnen we het obstakel wegnemen? | Hoe kunnen we boodschappen doen zonder wachttijd? |
| **Draai het obstakel om** | Hoe kunnen we het obstakel juist een voordeel maken? | Hoe kunnen we van winkelen met kinderen iets leuks maken? |
| **Verplaats de last** | Hoe kunnen we het obstakel bij iemand of iets anders leggen? | Hoe kunnen we de winkel het werk laten doen? |
| **Verander het moment** | Hoe kunnen we het op een ander tijdstip of plek laten gebeuren? | Hoe kunnen we boodschappen doen buiten de drukte om? |
| **Verander de rol** | Hoe kunnen we de persoon een andere rol geven? | Hoe kunnen we kinderen mede-boodschapper maken? |
| **Ga naar de diepere behoefte** | Hoe kunnen we de WANT bereiken zonder de WIL? | Hoe kunnen we gezinnen meer vrije tijd geven? |
| **Analogie uit een ander domein** | Wie lost dit elders al op? | Hoe kunnen we boodschappen doen zo vlot maken als afhalen? |

Formuleer vanuit de **persoon**, niet vanuit de organisatie: "Hoe kunnen we een student helpen om..."
in plaats van "Hoe kunnen we de instelling laten...". De organisatie is de uitvoerder, niet het
onderwerp.

Vermijd oplossingswoorden in de vraag zelf. Zodra er "app", "dashboard", "portal", "chatbot" of
"training" in staat, heb je het antwoord al ingevuld en heb je een brainstorm van één idee.

### Stap 3 — Kalibreer elke HMW zelf

Dit is de kern van de skill: je levert geen ongefilterde lijst, maar een beoordeelde set.

Toets elke gegenereerde HMW op twee kanten:

**Te breed** — de vraag zou net zo goed over een compleet ander inzicht kunnen gaan. Je kunt hem
beantwoorden zonder de WIE, WIL of MAAR te kennen. Er is geen aanknopingspunt om te beginnen.

> *Hoe kunnen we mensen helpen te ontstressen?* → te breed. Geen persoon, geen context, geen
> obstakel. Waar begin je?

**Te smal** — de vraag bevat de oplossing al. Er is precies één antwoord mogelijk, of het antwoord
is een concreet product/kanaal. De brainstorm is klaar voordat hij begint.

> *Hoe kunnen we Marie een app geven waarmee zij de drukte in de supermarkt kan zien?* → te smal.
> "App" en "drukte zien" zijn al ontwerpbeslissingen.

De **praktische toets**: zou deze vraag minstens 5 wezenlijk verschillende ideeën opleveren in een
brainstorm van 15 minuten? Minder dan 3 → te smal. Meer dan 20 maar allemaal willekeurig → te breed.

**Wat je doet met de uitkomst:**

- **Goed** → houden, opnemen in de set.
- **Te breed** → herschrijf smaller door de MAAR of de WIE terug te brengen. Geef de herschreven
  versie, niet alleen het oordeel.
- **Te smal** → herschrijf breder door het oplossingswoord te vervangen door het onderliggende
  doel. Geef ook hier de herschreven versie.

Neem in de output ook **1 à 2 afgewezen varianten** op met de reden. Dat is leerzaam: de gebruiker
ziet waarom een vraag niet werkt en kan zelf beter kalibreren. Het maakt je oordeel ook
controleerbaar in plaats van een black box.

### Stap 4 — Kies de startvraag

Wijs één HMW aan als **startpunt voor de brainstorm** en leg in één of twee zinnen uit waarom.
Meestal is dat de vraag die de MAAR het directst aanpakt zonder een oplossingsrichting op te
leggen. Een lijst zonder prioriteit laat de gebruiker met het werk zitten.

---

## Output

Lever twee dingen: het antwoord in de chat én een `.md`-bestand in `/mnt/user-data/outputs/`
met de naam `hmw-<kort-onderwerp>.md`. Beide bevatten dezelfde structuur.

Gebruik dit template:

```markdown
# Hoe kunnen we — <onderwerp>

## Centraal inzicht
> <het inzicht, letterlijk>

**WIE** <persoon> · **WIL** <activiteit> · **WANT** <doel> · **MAAR** <obstakel>

*Aannames:* <alleen als je iets zelf hebt ingevuld; anders weglaten>

## Startvraag
**Hoe kunnen we <...>?**
<één of twee zinnen waarom deze het beste startpunt is>

## Hoe kunnen we-vragen

| # | Hoe kunnen we... | Hoek | Kalibratie |
|---|---|---|---|
| 1 | <vraag> | <hoek> | Goed |
| 2 | <vraag> | <hoek> | Verbreed vanaf te smal |
| ... | | | |

## Afgewezen varianten

- ~~<vraag>~~ — **te breed**: <reden>. Herschreven als #<n>.
- ~~<vraag>~~ — **te smal**: <reden>. Herschreven als #<n>.

## Volgende stap
<één zin: wat de gebruiker hierna doet — brainstorm, inzicht aanscherpen, of meer centrale inzichten nodig>
```

Bij meerdere centrale inzichten: één bestand, per inzicht een eigen sectie met dezelfde opbouw.

Houd de chatweergave compact — de tabel plus de startvraag volstaan. Verwijs voor het volledige
overzicht naar het bestand.

---

## Voorbeeld

**Centraal inzicht:** *Sanne, tweedejaars mbo-student Zorg, wil weten of ze op koers ligt voor haar
diploma, want ze wil niet aan het eind van het jaar voor verrassingen komen te staan, maar de
studievoortgangsinformatie is verspreid over verschillende systemen en pas achteraf zichtbaar.*

**Startvraag:** Hoe kunnen we een mbo-student op elk moment laten voelen of ze op koers ligt?

*Waarom:* raakt de MAAR (informatie komt te laat) én de WANT (geen verrassingen) zonder een kanaal
of systeem voor te schrijven.

| # | Hoe kunnen we... | Hoek | Kalibratie |
|---|---|---|---|
| 1 | ...een mbo-student op elk moment laten voelen of ze op koers ligt? | Verwijder obstakel | Goed |
| 2 | ...voortgang zichtbaar maken op momenten dat een student er iets mee kan? | Verander het moment | Goed |
| 3 | ...een student zelf haar voortgang laten bijhouden zonder extra werk? | Verander de rol | Goed |
| 4 | ...de opleiding het signaal laten geven in plaats van de student het te laten zoeken? | Verplaats de last | Goed |
| 5 | ...onzekerheid over studievoortgang omzetten in richting? | Draai om | Goed |
| 6 | ...een student hetzelfde vertrouwen geven dat een pakketrace geeft? | Analogie | Verbreed vanaf te smal |

**Afgewezen varianten:**

- ~~Hoe kunnen we studenten helpen minder stress te ervaren?~~ — **te breed**: geldt voor elk
  studentinzicht, geen aanknopingspunt bij voortgang of systemen. Herschreven als #5.
- ~~Hoe kunnen we Sanne een dashboard geven met haar behaalde studiepunten?~~ — **te smal**:
  "dashboard" en "studiepunten" zijn al ontwerpkeuzes. Herschreven als #1.

---

## Aandachtspunten

**De HMW is geen samenvatting van het inzicht.** Wie het inzicht simpelweg omdraait
("Hoe kunnen we ervoor zorgen dat Sanne weet of ze op koers ligt?") krijgt een vraag die correct
maar bloedeloos is. De hoeken uit stap 2 bestaan om daaraan te ontsnappen.

**Blijf weg van jargon uit het beleidsdomein.** "Hoe kunnen we de studiesuccesratio verhogen?" is
een KPI, geen ontwerpvraag. Vertaal terug naar wat iemand ervaart.

**Onderwijscontext maakt sommige obstakels structureel.** Roosters, examenreglementen,
AVG-beperkingen en systeemlandschappen zijn vaak niet weg te ontwerpen. Dat is geen reden om ze te
negeren — juist een HMW die het obstakel omdraait ("hoe kunnen we van de privacybeperking een
vertrouwensvoordeel maken?") levert de interessantste ideeën op.

**Twijfel je of een vraag te smal is?** Bedenk drie oplossingen. Lijken ze allemaal op elkaar, dan
is hij te smal.
