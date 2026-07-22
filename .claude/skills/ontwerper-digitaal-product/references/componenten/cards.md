# Card

Lees dit bestand zodra je zelf besluit een kaart-layout (card) te gebruiken om content te groeperen. Een card is een container voor een paar korte, gerelateerde stukjes informatie — visueel vergelijkbaar met een speelkaart, bedoeld als gelinkte, korte representatie van één conceptuele eenheid (NN/g).

## Anatomie

- **Titel** — de samenvatting; in één oogopslag duidelijk waar de card over gaat.
- **Secundaire tekst/subtitel** (optioneel) — extra context; wordt soms overgeslagen tijdens het scannen, houd 'm kort.
- **Tertiaire tekst** (optioneel) — niet-essentiële extra info; bewaar zichtbare hiërarchie tussen alle drie de tekstniveaus.
- **Media** — meestal één hero-afbeelding, illustratie of video.
- **Call-to-action** — expliciete knop/link, of de hele card is klikbaar met een affordance-icoon (chevron, pijl).
- **Tags/labels/status** — bv. "Nieuw", "Live", "Meest gewaardeerd".
- **Visuele signifiers**: rand, achtergrondkleur die afwijkt van de onderliggende canvas, afgeronde hoeken, lichte drop shadow. Dit "common regions"-principe groepeert content sterker dan alleen nabijheid (proximity) kan — items die verder uit elkaar staan, worden toch als groep gezien zodra ze binnen dezelfde rand/achtergrond vallen (NN/g).

## Wanneer gebruiken (en wanneer niet)

Gebruik cards voor:
- **Heterogene verzamelingen** — content van wisselend type en lengte (afbeeldingen, tekst, video door elkaar), waarbij niet elk item dezelfde velden hoeft te hebben.
- **Browsen, niet zoeken.** Cards zijn beter geschikt wanneer gebruikers rondkijken dan wanneer ze gericht naar één item zoeken.
- **Streams/feeds** (nieuwsoverzicht), **discovery-interfaces** (content die zichzelf onthult), **workflow-tools** (één taak = één kaart, zoals Trello), **dashboards** met uiteenlopende content-typen.

Gebruik geen cards (kies een lijst of grid) wanneer:
- **De content homogeen is** — een lijst van vergelijkbare producten, of een fotogalerij. Een standaard lijst-/gridweergave scant beter en kost minder ruimte.
- **Strikte volgorde/ranking belangrijk is.** Cards onderbenadrukken hiërarchie; gebruikers kunnen moeilijk zien wat belangrijker is dan wat anders.
- **Gebruikers items direct moeten vergelijken.** Oogonderzoek (NN/g) laat zien dat mensen bij cards herhaaldelijk heen-en-weer kijken tussen items omdat de layout niet voorspelbaar is — een lijst met vaste, consistente posities per veld (bv. prijs altijd rechtsonder) ondersteunt vergelijken veel beter.
- **Gebruikers naar een specifiek item zoeken.** Cards zijn minder scanbaar dan lijsten omdat de positie van elementen per kaart kan verschillen, en ze nemen meer ruimte in, dus je toont er minder tegelijk (meer beroep op kortetermijngeheugen).

## Interactie & structuur

- **"One card, one concept."** Een card mag meerdere elementen bevatten, maar die horen allemaal bij hetzelfde onderwerp.
- **Maak bij voorkeur de hele card klikbaar**, niet alleen een los element — een groter klikgebied verbetert bruikbaarheid op zowel touch als muis (Fitts' wet).
- **Bepaal scrolrichting vooraf en houd 'm consistent**: alleen horizontaal óf alleen verticaal, niet beide. Content die de maximale hoogte/breedte overschrijdt wordt getrunceerd (niet gescrold binnen de card), maar kan uitklapbaar zijn.
- **Cards binnen één set zijn uniform**; cards in verschillende sets hoeven dat niet te zijn — varieer gerust in vorm (rond, rechthoekig) tussen sets om het interessant te houden.
- **Definieer expliciet de edge cases** vóór je het ontwerp overdraagt: hoe ziet het eruit met maar 1-2 cards, hoeveel cards per rij, in welke volgorde worden ze gesorteerd, welk deel is klikbaar, wat gebeurt er bij hover.

## Toegankelijkheid

- Alt-tekst voor media en links, en een logische taborde binnen de card.
- Laat gebruikers tussen cards in een set kunnen springen zonder door elk los element te moeten tabben.
- Klikgebieden groot genoeg: minimaal 44×44px (iOS-richtlijn) / 48dp (Android-richtlijn) — vergelijkbaar met de aanraakdoel-eis uit het ISGVO-model.
- Bij lokalisatie: houd rekening met tekenlengte en leesbaarheid — sommige talen (bv. Chinees) nemen per teken meer ruimte in dan Latijnse schriften, andere juist minder; test of je titel/tekstniveaus dat verschil aankunnen.

## Visueel

- **Afgeronde hoeken + lichte drop shadow** laten de card op een fysieke kaart lijken en signaleren diepte/klikbaarheid.
- **Genereuze witruimte** rond elke card — elke card is een eigen mini-ontwerp en heeft ruimte nodig om gezien en begrepen te worden.
- **De afbeelding is koning.** Investeer in een sterke hero-afbeelding; houd tekst in eenvoudige, goed leesbare typefaces (bv. sans-serif, normaal gewicht) voor maximale scanbaarheid.
- **Bouw duidelijke hiërarchie**: belangrijkste content bovenaan, typografie voor nadruk, dividers voor onderdelen die duidelijker gescheiden moeten worden.
- **Beperk de inhoud tot het essentiële** — een card is een entry point naar meer details, niet de plek voor de volledige details zelf. Voor elk gegevenspunt: is dit noodzakelijk, of kan het weg?

## Veelgemaakte fouten

- **Visuele overload**: te veel informatie of acties in één card proppen. Maak een lijst van alle databronnen en schrap wat niet essentieel is.
- Cards gebruiken voor een verzameling **homogene items** (vergelijkbare producten, fotogalerij) waar een lijst of grid beter scant.
- Cards gebruiken wanneer **strikte ranking/volgorde** gecommuniceerd moet worden.
- Cards gebruiken voor content die **direct vergeleken** moet worden.
- **Edge cases niet ontworpen**: tekst-overflow, beeldschaling, hoe het eruitziet met slechts één of twee cards, lage-kwaliteit of ontbrekende afbeeldingen.
- Slechts een deel van de card klikbaar maken zonder dat duidelijk is welk deel — of de hele card klikbaar maken zonder dat te signaleren (shadow/hover-animatie ontbreekt).

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele en micro-interactie-inspiratie (kleurgebruik, schaduwdiepte, hover-animaties) kan een galerij zoals collectui.com/designs/card-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de bruikbaarheidsregels hierboven (NN/g, ui-patterns.com) wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Cards: UI-Component Definition](https://www.nngroup.com/articles/cards-component/)
- ui-patterns.com — [Cards](https://ui-patterns.com/patterns/cards)
- UX Collective — [Designing Cards for Beginners](https://uxdesign.cc/designing-cards-for-beginners-9ed9454d27f6)
- CollectUI — [Card UI Design Inspiration](https://collectui.com/designs/card-ui-design-inspiration) (visuele inspiratie)
