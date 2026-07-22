# Menu / navigatie

Lees dit bestand zodra je zelf besluit een navigatiemenu te ontwerpen — desktop of mobiel, tabs of hamburger. Mensen gebruiken menu's om te vinden wat ze zoeken en te begrijpen wat een site of app allemaal doet; een menu dat dat niet goed doet, is een uitvoeringskloof- én evaluatiekloof-probleem tegelijk.

## Maak navigatie zichtbaar (desktop/large screen)

- **Verberg navigatie nooit achter een hamburger-icoon op grotere schermen.** Uit het oog is uit het gedachten. Een hamburgermenu is een noodzakelijk kwaad op kleine schermen waar ruimte schaars is — op desktop, met ruimte genoeg, verbergt het onnodig de context die gebruikers vertelt wie je bent en wat je doet.
- **Plaats menu's op de verwachte locatie**: primaire navigatie in de header (of links op applicaties), utility-navigatie boven de primaire navigatie, lokale navigatie links op desktop, footer-navigatie onderaan.
- **Zorg voor voldoende contrast tussen linktekst en achtergrond** — verifieer met `scripts/contrast_checker.py` in plaats van op het oog te schatten.
- **Laat een geopend menu nooit het hele scherm bedekken op grotere schermen.** Een open menu is een tijdelijk, zwevend element bovenop de content — geen aparte pagina. Bedekt het alles, dan denken gebruikers dat ze per ongeluk naar een nieuwe pagina zijn genavigeerd.

## Communiceer de huidige locatie

- **Toon altijd waar de gebruiker zich bevindt** — via highlighting in het menu en/of breadcrumbs. Gebruikers landen vaak niet op de homepage; zonder locatie-indicatie raken ze de weg kwijt.
- **Bied lokale navigatie voor nauw verwante content** in plaats van gebruikers steeds omhoog en omlaag door de hiërarchie te laten "pogo-sticken".

## Communiceer de beschikbare opties

- **Gebruik heldere, specifieke, herkenbare bewoording.** Een menu is niet de plek voor verzonnen woorden, interne jargon, of abstracte hoog-niveau categorisering.
- **Maak labels scanbaar**: links uitlijnen (niet centreren/rechts uitlijnen), belangrijke woorden vooraan zetten.
- **Gebruik megamenu's of sequentiële navigatie bij grote sites** waar gebruikers meerdere niveaus diep moeten gaan — dit bespaart tijd t.o.v. laag-voor-laag klikken.
- **Visuele signalen (iconen, afbeeldingen) mogen scanbaarheid ondersteunen, maar vervangen nooit heldere tekstlabels** — dat is zowel een toegankelijkheids- als een bruikbaarheidseis.

## Maak het makkelijk te bedienen

- **Maak menu-links groot genoeg om te tikken/klikken** — te kleine of te dicht op elkaar staande links frustreren, ook op desktop.
- **Signaleer submenu's duidelijk met een pijltje/caret-icoon** — anders realiseren gebruikers zich niet dat een item uitklapbaar is.
- **Gebruik klik-geactiveerde submenu's, niet hover-geactiveerde.** Hover is niet universeel beschikbaar (touchscreens, toetsenbordnavigatie) en per ongeluk activeren/sluiten is voor iedereen vervelend.
- **Vermijd meerlagige cascaderende dropdowns.** Eén niveau werkt prima, twee wordt al frustrerend, meer dan twee is sterk afgeraden — de kans op per ongeluk de verkeerde subcategorie kiezen of het hele menu sluiten neemt toe (steering law). Gebruik bij meerdere niveaus een megamenu (2-3 niveaus goed te doen) of stuur door naar een routeringspagina.
- **Overweeg sticky menu's bij lange pagina's** zodat gebruikers niet helemaal terug hoeven te scrollen.
- **Plaats veelgebruikte commando's dicht bij het element dat het dropdown opent** (Fitts' wet: reistijd hangt af van afstand).
- **Vermijd gimmick-navigatie.** Opvallende, innovatieve interactiepatronen imponeren soms opdrachtgevers, maar gebruikers waarderen vooral herkenbare, goed toegankelijke navigatie boven originaliteit.

## Mobiele navigatiepatronen: kies bewust tussen zichtbaar en verborgen

Drie basispatronen, elk met eigen afwegingen (NN/g):

- **Navigatiebalk / tabbalk (expliciet zichtbaar)** — bovenaan (meestal Android) of onderaan (meestal iOS). Werkt goed bij **4-5 opties of minder**; meer opties passen niet zonder de aanraakdoelgrootte te schaden. Tabbalken zijn persistent (altijd zichtbaar); navigatiebalken verdwijnen vaak bij scrollen tenzij "sticky". Neemt kostbare schermruimte in — houd rekening met overige chrome (zoekbalk, account, winkelwagen) die er ook nog bij moet.
- **Hamburgermenu / navigatiemenu (verborgen)** — verbergt opties totdat de gebruiker er expliciet om vraagt. Kan veel opties in weinig ruimte herbergen en ondersteunt submenu's makkelijk, maar is minder ontdekbaar: gebruikers moeten een bewuste beslissing nemen om te openen, en vergeten dat vaak. **Best geschikt voor content-zware, "vooral-browsen"-sites** waar gebruikers zich tevreden stellen met wat gepresenteerd wordt.
- **Navigatie-hub (homepage als knooppunt)** — alle navigatie-opties op één centrale pagina (meestal de homepage); elke navigatiestap gaat via een terug-naar-hub-actie. Werkt goed bij **taakgerichte apps** waar gebruikers doorgaans maar één tak van de navigatieboom per sessie gebruiken (bv. inchecken voor een vlucht) — de terugkeer-naar-hub-stap is dan zelden nodig.

Kies het patroon waarbij de onvermijdelijke nadelen de gebruiker het minst pijn doen voor de taken die ze het vaakst uitvoeren — niet het patroon dat er het gaafst uitziet.

## Tabs als navigatiepatroon: twee varianten

- **Navigation Tabs** — platte navigatiestructuur (2–9 secties), duidelijke aanduiding van huidige locatie, vult de volledige paginabreedte. Elke tab is een link naar een aparte pagina/sectie. Niet gebruiken voor content-specifieke data (zoals "laatste artikelen") of wanneer een "meer..."-link nodig is voor te veel secties — kies dan een ander patroon.
- **Module Tabs** — zelfde flat-navigatie-idee (2–9 secties), maar de content laadt in hetzelfde content-gebied zonder paginaherlaad. Geschikt wanneer content per tab losstaand bekeken kan worden (niet in context van elkaar) en dezelfde structuur heeft. Toon altijd welke tab actief is (kleurcodering); behoud dezelfde tab-volgorde na een klik.

In beide gevallen: de hele tab (niet alleen de tekst) moet klikbaar zijn, de volgorde van tabs moet consistent blijven van pagina tot pagina, en de achtergrondkleur van de geselecteerde tab moet naadloos overlopen in de achtergrond van de bijbehorende content — dat verbindt de tab visueel met zijn inhoud.

## Veelgemaakte fouten

- Navigatie verbergen achter een hamburgermenu op desktop terwijl er ruimte genoeg is.
- Menu's op een onverwachte plek zetten (bv. lokale navigatie niet links, footer-navigatie niet onderaan).
- Geen indicatie van de huidige locatie — de meest voorkomende menu-fout volgens NN/g.
- Onduidelijke of jargon-labels ("Resources", "Oplossingen") in plaats van concrete, herkenbare termen.
- Hover-geactiveerde submenu's zonder toetsenbord-/touch-alternatief.
- Meerlagige cascaderende dropdowns (meer dan twee niveaus).
- Een geopend menu dat het hele scherm bedekt op desktop, met desoriëntatie tot gevolg.
- Gimmick-navigatiepatronen kiezen om indruk te maken in plaats van gebruikers te helpen.
- Op mobiel meer dan 5 opties in een tabbalk proppen, of een hamburgermenu gebruiken voor een taakgerichte app waar snelle herhaalde toegang tot een paar kernacties juist telt.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (animaties, iconografie, kleurgebruik) kan een galerij zoals collectui.com/designs/menu-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de zichtbaarheids-, locatie- en bedieningsregels hierboven (NN/g, ui-patterns.com) wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Menu-Design Checklist: 17 UX Guidelines](https://www.nngroup.com/articles/menu-design/)
- NN/g — [Basic Patterns for Mobile Navigation](https://www.nngroup.com/articles/mobile-navigation-patterns/)
- UX Collective — [Some common mobile nav patterns & when to use them](https://uxdesign.cc/some-common-mobile-nav-patterns-when-to-use-them-9b2bff9fcb0e)
- ui-patterns.com — [Navigation Tabs](https://ui-patterns.com/patterns/NavigationTabs)
- ui-patterns.com — [Module Tabs](https://ui-patterns.com/patterns/ModuleTabs)
- CollectUI — [Menu UI Design Inspiration](https://collectui.com/designs/menu-ui-design-inspiration) (visuele inspiratie)
