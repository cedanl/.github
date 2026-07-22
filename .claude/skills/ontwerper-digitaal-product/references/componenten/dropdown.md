# Dropdown

Lees dit bestand zodra je zelf besluit een dropdown te gebruiken — ook als de gebruiker het woord "dropdown" niet noemt. Een dropdown is een van de meest overused en clunky patronen in UI (NN/g); check eerst of het wel het juiste element is voordat je 'm bouwt.

## Anatomie

Vier onderdelen: **container box** (toont geselecteerde/standaardwaarde), **pijl-knop** (opent de lijst), **lijst met items** (verschijnt pas na klik), **label** (blijft zichtbaar, ook als de lijst open is).

Twee families, niet hetzelfde:
- **Dropdown box** — voor formulieren en attribuutselectie (bv. land, categorie). Heeft een pijl, toont de huidige waarde.
- **Dropdown menu** — voor commando's of navigatie (bv. een "Publiceren"-menu). macOS/Windows-richtlijnen raden af om hier hetzelfde visuele patroon als een dropdown box voor te gebruiken — een commandomenu hoort er niet uit te zien als een select-veld.

Verwar dit niet met een **listbox**: die toont opties direct zonder klik en ondersteunt multi-select. Een dropdown vereist een klik en staat alleen single-select toe.

## Wanneer gebruiken (en wanneer niet)

Beslisregels, samengevat uit NN/g's vergelijking van listbox vs. dropdown:

- **≤5 opties, mutually exclusive** → gebruik radiobuttons, geen dropdown. Alle opties in één oogopslag is sneller dan een klik + scannen.
- **5–15 opties** → dropdown is prima, zeker bij beperkte schermruimte. Is er ruimte over en wil je opties meer aandacht geven → listbox.
- **>15 opties** → overweeg een listbox (toont meer in één keer) in plaats van een lange scrollende dropdown. Is de waarde bij de gebruiker al bekend (land, staat) → laat ze typen in een tekstveld, dat is sneller dan scrollen.
- **Multi-select nodig** → geen dropdown (die staat maar één keuze toe). Gebruik een listbox met checkboxes.
- **Data die gebruikers "in hun vingers hebben"** (geboortedatum, land bij adres) → vermijd een dropdown; typen is sneller en foutbestendiger.
- **Er is geen duidelijke default-optie** → een listbox toont alle opties gelijkwaardig; een dropdown suggereert juist één zichtbare (voorkeurs)waarde.
- **Navigatie-shortcut nodig** (snel naar een specifieke pagina/functie ongeacht hiërarchie) → een dropdown kán hiervoor (ui-patterns.com's "Shortcut Dropdown": een `<select>` met vaste URL's, bij selectie of submit navigeert de gebruiker direct). Gebruik dit spaarzaam en nooit als vervanging van je primaire navigatie.
- **Globale navigatie van de site** → stop dit nooit volledig in een dropdown; dat begraaft je topcategorieën en schaadt vindbaarheid (NN/g).

## Interactie & toetsenbord

- Ondersteun toetsenbordinvoer: pijltjestoetsen om door opties te bewegen, Enter/Space om te selecteren, Escape om te sluiten zonder wijziging.
- Type-ahead: laat gebruikers een letter typen om direct naar de eerste optie te springen die daarmee begint.
- Vermijd **interacting menus** — waarbij de opties van dropdown A veranderen op basis van de keuze in dropdown B op dezelfde pagina. Gebruikers raken hierdoor in de war omdat opties komen en gaan zonder duidelijke oorzaak.
- Sluiten gebeurt bij: selectie van een item, klik buiten de dropdown, of Escape.

## Toegankelijkheid

- **Gebruik een native `<select>` tenzij je een dwingende visuele reden hebt om af te wijken.** Native selects zijn gratis toegankelijk (toetsenbord, screenreader, mobiel besturingssysteem-UI) — een custom dropdown moet dat allemaal zelf nabouwen.
- Bouw je toch een custom versie: volg het WAI-ARIA APG-patroon — trigger met `aria-haspopup="listbox"` en `aria-expanded`, paneel met `role="listbox"`, items met `role="option"` en `aria-selected`, en beheer focus met `aria-activedescendant` in plaats van focus daadwerkelijk te verplaatsen.
- Label altijd zichtbaar en programmatisch gekoppeld (`<label for>` of `aria-labelledby`) — nooit alleen een placeholder als label.
- Grote genoeg aanraakdoelen (≥44×44px) voor trigger en elke optie.
- Verifieer kleurcontrast van tekst/opties met `scripts/contrast_checker.py` (zie hoofdmap van deze skill).

## States

- **Geselecteerd/standaard** — zichtbaar in de container box, ook als de lijst gesloten is.
- **Open** — lijst met opties zichtbaar; het label/de titel blijft zichtbaar (zie veelgemaakte fouten).
- **Disabled optie** — grijs weergeven, niet verwijderen. Overweeg een korte uitleg bij hover waarom de optie niet beschikbaar is.
- **Scrollbaar** — vanaf een bepaald aantal items; houd de lijst zo breed en kort mogelijk (steering law: een lange, smalle lijst kost meer tijd en precisie om te bedienen dan een korte, brede).
- **Leeg** (geen opties beschikbaar) — toon een expliciete melding, geen lege lijst.

## Veelgemaakte fouten

- Label verbergen zodra de lijst open is — gebruikers moeten dan onthouden waar ze voor kozen.
- Disabled opties verwijderen in plaats van grijs tonen — breekt ruimtelijke consistentie, moeilijker te leren.
- Een lange lijst zonder scrollbalk of duidelijk einde — gebruikers weten niet of er nog meer opties onder staan.
- Een dropdown gebruiken voor commando's (bv. "Verwijderen", "Delen") terwijl het er hetzelfde uitziet als een attribuutkeuze — gebruik daarvoor een menu-knop, geen select-styling.
- Een dropdown gebruiken waar typen sneller is (geboortedatum, land, postcode).
- De volledige globale navigatie in één dropdown stoppen.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele en micro-interactie-inspiratie (animaties, hover-states, iconografie) kan een galerij zoals collectui.com/designs/dropdown-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de bruikbaarheidsregels hierboven (NN/g, ui-patterns.com) wegen zwaarder dan een visueel trend.

## Bronnen

- NN/g — [Dropdowns: Design Guidelines](https://www.nngroup.com/articles/drop-down-menus/)
- NN/g — [Listboxes vs. Dropdown Lists](https://www.nngroup.com/articles/listbox-dropdown/)
- ui-patterns.com — [Shortcut Dropdown](https://ui-patterns.com/patterns/ShortcutDropdown)
- CollectUI — [Dropdown UI Design Inspiration](https://collectui.com/designs/dropdown-ui-design-inspiration) (visuele inspiratie)
