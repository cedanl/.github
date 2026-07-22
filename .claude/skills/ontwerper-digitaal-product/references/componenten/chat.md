# Chat / conversational interface

Lees dit bestand zodra je zelf besluit een chatinterface te gebruiken — als patroon voor persoonlijke berichten (direct messaging) óf als AI/bot-conversatie. Chat is als interface zo oud als de command line; combineer je 'm met bot-logica, dan gelden extra regels bovenop de generieke interactieregels.

## Twee varianten, niet hetzelfde

- **Direct messaging / inbox** — gebruiker communiceert privé met andere mensen of groepen. Typisch drie schermen: **Inbox** (ontvangen berichten), **Outbox/Sent**, **Nieuw bericht** (invoerformulier + verzendknop) (ui-patterns.com).
- **AI/bot-conversatie** — gebruiker communiceert met een systeem, niet een mens. Onderscheid hierbinnen: **customer-service bots** (vervangen een deel van menselijke supportagenten) en **interaction bots** (extra interactiekanaal voor taken, bv. bestellen, offerte aanvragen) (NN/g). De meeste regels hieronder gelden voor deze variant.

## Anatomie

- **Berichtenlijst** — bubbels in een scrollbare thread. Positie (links/rechts) en kleur onderscheiden afzender. Overweeg een derde visuele stijl voor systeemberichten (statusupdates, bevestigingen) naast gebruiker/bot.
- **Invoerveld + verzendtrigger** — Enter om te verzenden, Shift+Enter voor een nieuwe regel (gangbare conventie).
- **Quick replies / knoppen náást vrije tekst** — beide mechanismen moeten samen bestaan, niet als vervanging van elkaar.
- **Typing-indicator en tijdstempel** — geven aan dat het systeem verwerkt, en geven een referentiepunt bij het terugkijken van het gesprek.
- **Foutstatus** — beantwoordt altijd: wat gebeurde er, waarom, wat kan de gebruiker nu doen.

## Wanneer gebruiken (en wanneer niet)

- Gebruik chat wanneer de taak zich leent voor sequentiële, natuurlijke-taal-interactie, of wanneer gebruikers privé met individuen/groepen willen communiceren.
- **Bouw geen chatbot als een goed ontworpen website of app de taak al oplost.** NN/g: chatbots repliceren vaak functionaliteit die al bestaat, tonen maar weinig informatie tegelijk, en gebruikers ontdekken het kanaal vaak niet eens. Investeer liever in de bestaande flow, tenzij de bot een aantoonbaar voordeel biedt (snelheid, 24/7 beschikbaarheid, minder informatie-overload).
- **Houd de scope smal.** Bouw voor een beperkt aantal simpele, welomschreven taken. Complexiteit wordt slecht gehanteerd in het beperkte chatkanaal — vertel de gebruiker vooraf expliciet wat de bot wél en niet kan, anders ontstaan valse verwachtingen (NN/g).

## Interactie & structuur

- **Bied altijd zowel vrije tekst als knoppen/quick-replies aan.** Gebruikers klagen wanneer typen verplicht is voor iets dat ook een knop had kunnen zijn (bv. een datum), en voelen zich beperkt wanneer vrije tekst volledig ontbreekt (NN/g-onderzoek).
- **Bouw flexibiliteit in de lineaire flow.** Lineaire scripts werken zolang gebruikers "binnen de lijntjes" blijven, maar zodra ze afwijken (typefout, ander woord, van gedachten veranderen) lopen bots vaak vast en dwingen de gebruiker om opnieuw te beginnen. Ondersteun context-behoud tussen taken (adres niet twee keer vragen), tussentijds bijstellen ("maak dat 12 personen") en terug-/vooruitspringen zonder alles te verliezen.
- **Eén idee per bericht.** Splits lange antwoorden in meerdere kortere, opeenvolgende berichten in plaats van alles in één blok te persen.
- **Toon typing-indicators en, bij AI, streaming tekst tijdens verwerking.** Een pauze zonder signaal voelt in een gesprek aan als sociale stilte, niet als "systeem is bezig" — dit is een functioneel signaal, geen decoratie. Voeg bij AI-antwoorden een stopknop toe om een stream te kunnen onderbreken.
- **Benoem vertraging expliciet.** Bij taken die tijd kosten (zoeken, tool-aanroepen) toon een concrete status ("Zoekt in je documenten...") in plaats van een generieke spinner.
- **Quick replies werken het best bij gestructureerde flows** (intake, kwalificatievragen); laat vrije tekst beschikbaar voor momenten die nuance vereisen.

## Toegankelijkheid & vertrouwen (AI-specifiek)

- **Wees vooraf duidelijk dat het een bot is, geen mens.** Gebruikers waarderen die transparantie en passen er hun taalgebruik (directer, minder beleefdheidsformules) en verwachtingen op aan (NN/g).
- **Vermijd antropomorfe taal** ("Ik dacht na over je probleem…") — dit overschat in de ogen van de gebruiker wat het systeem kan. Gebruik neutrale, feitelijke formuleringen ("Dit antwoord is gebaseerd op: [bron]") (NN/g, Explainable AI).
- **Erken onbegrip eerlijk en bied een uitweg.** Een bot die toegeeft het niet te begrijpen en doorverwijst naar een mens, telefoonnummer of ander kanaal wordt beter gewaardeerd dan een zelfverzekerd fout antwoord.
- **Bronvermeldingen:** stijl ze zichtbaar anders dan de hoofdtekst, plaats ze direct naast de bewering die ze onderbouwen, gebruik betekenisvolle labels (publicatienaam/titel, niet het woord "Bron"). Gebruikers klikken zelden door om te verifiëren — een citaat wekt dus schijnzekerheid zodra het niet klopt, dus verifieer zelf de juistheid vóór je ze toont.
- **Disclaimers zichtbaar bij het invoerveld**, niet in een footer of achter een info-icoon. Heldere, actiegerichte taal ("Controleer antwoorden altijd") in plaats van vage taal ("Alleen ter referentie").
- **Wees terughoudend met stap-voor-stap "redeneer"-uitleg** die zekerheid suggereert — dit is vaak een achteraf gegenereerde rationalisatie, geen getrouwe weergave van het onderliggende proces. Gebruik in plaats daarvan bronvermelding en een eerlijke beschrijving van beperkingen.

## States

- Verzonden / ontvangen
- Typend / verwerkend (indicator)
- Streaming (tokens verschijnen progressief in plaats van in één keer)
- Onderbroken stream — toon wat al gegenereerd was, met een duidelijke "onvolledig"-indicator en een retry-optie
- Fout — onderscheid begripsfouten ("dat begreep ik niet") van technische fouten ("er ging iets mis"); allebei met een concreet vervolgpad
- Leeg (nieuw gesprek, geen berichten)

## Veelgemaakte fouten

- Vrije tekst volledig blokkeren zodat de bot aanvoelt als een website met stap-knoppen in plaats van een gesprek — of omgekeerd, alles verplicht laten typen terwijl een knop voor de hand ligt.
- Een chatbot bouwen voor taken die de bestaande site/app al goed oplost.
- Niet transparant zijn over het feit dat het geen mens is.
- Context niet vasthouden tussen vragen binnen hetzelfde gesprek (adres, voorkeuren opnieuw laten invoeren).
- Generieke spinners bij lange wachttijden in plaats van benoemde voortgangsstatussen.
- Bronvermeldingen tonen alsof ze geverifieerd zijn terwijl ze gehallucineerd of onduidelijk zijn.
- Een persoonlijkheid of toon beloven die het systeem niet kan volhouden door het hele gesprek — dit ondermijnt vertrouwen meer dan gewoon zakelijk blijven.
- Carrousels gebruiken om lange resultatenlijsten te tonen — bots hebben beperkte weergaveruimte; bij veel treffers is sorteren/filteren nodig, niet nóg een scrollend element.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele en micro-interactie-inspiratie (bubbel-animaties, kleurgebruik, lay-out) kan een galerij zoals collectui.com/designs/chat-layout-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de bruikbaarheids- en vertrouwensregels hierboven wegen zwaarder dan een visuele trend.

## Bronnen

- ui-patterns.com — [Chat / Direct Messaging](https://ui-patterns.com/patterns/direct-messaging)
- NN/g — [The User Experience of Chatbots](https://www.nngroup.com/articles/chatbots/)
- NN/g — [Explainable AI in Chat Interfaces](https://www.nngroup.com/articles/explainable-ai/)
- NN/g — [Noncommand User Interfaces](https://www.nngroup.com/articles/noncommand/) (achtergrond: waarom conversatie-interfaces zonder starre commandosyntax werken, en welke verantwoordelijkheid dat bij het systeem legt)
- Medium (Writika Bhaskar) — [Rethinking UX Heuristics for Chatbots: A Conversational Lens on NN/g's Classic Principles](https://medium.com/@WritikaB/rethinking-ux-heuristics-for-chatbots-a-conversational-lens-on-nn-gs-classic-principles-a3c4d5c4c9a6)
- Lovable — [How to Build a Chatbot UI: Design Guide](https://lovable.dev/guides/how-to-build-a-chatbot-ui)
- CollectUI — [Chat Layout UI Design Inspiration](https://collectui.com/designs/chat-layout-ui-design-inspiration) (visuele inspiratie)
