# Button

Lees dit bestand zodra je zelf besluit een button te ontwerpen of op te leveren — ook als het een "simpel" element lijkt. Onduidelijke button-states zijn een klassieke bron van uitvoeringskloof-problemen (kan de gebruiker zien of iets klikbaar is?) en evaluatiekloof-problemen (weet de gebruiker of zijn klik geregistreerd is?).

## States vs. styles — twee losse assen

Dit zijn twee verschillende dingen die vaak door elkaar worden gehaald:

- **Button state** = de interactiestatus op een moment (enabled, disabled, hover, focus, pressed, loading). Eén button doorloopt meerdere states tijdens het gebruik.
- **Button style** = de visuele nadruk (primary, secondary, tertiary). Eén button heeft maar één style, ongeacht de state.

Ontwerp beide assen expliciet — een button-ontwerp zonder gedefinieerde states is onvolledig, ook al ziet de "enabled"-versie er goed uit.

## De 5 kern-states

- **Enabled** (standaard) — klikbaar/tikbaar. Hoog contrast t.o.v. de rest van het ontwerp, leesbaar label, optioneel een lichte schaduw voor een 3D-gevoel. Bij een primaire/CTA-knop mag deze state opvallen.
- **Disabled** — actie is nu niet beschikbaar; het uiterlijk verandert niet wanneer de gebruiker toch klikt. Lichtgrijze/verzadigde kleur, lager contrast tussen label en achtergrond — maar niet zó laag dat het onleesbaar wordt, en niet zó hoog contrast dat het weer klikbaar oogt. Voeg altijd `aria-disabled="true"` toe: de knop blijft dan tab-bereikbaar maar screenreaders kondigen de inactieve status aan.
- **Hover** — verschijnt wanneer de cursor over de button beweegt; signaleert klikbaarheid. Niet zichtbaar voor toetsenbord- of touchgebruikers. Voeg een korte vertraging toe (~150–200ms) zodat een toevallige muisbeweging niet als hover-intentie geldt. Typisch: iets donkerdere achtergrondkleur, cursor verandert naar een hand.
- **Focus** (keyboard-focus) — toont welk element de toetsenbordfocus heeft tijdens tabben. Moet snel verschijnen (~100–150ms) na toetsaanslag, anders mist de gebruiker 'm tijdens het verder tabben. Gebruik een zichtbare rand/outline — niet alleen een kleurverandering, want (a) gebruikers verwachten de standaard-outline en (b) kleur alleen is voor sommige mensen met visuele beperkingen niet waarneembaar.
- **Pressed** — geeft feedback dat de klik/tap geregistreerd is; kleine kleurverandering of korte animatie. Moet binnen ~100–150ms verschijnen — te trage feedback leidt tot herhaalde klikken en dubbele acties.

## Extra states

- **Loading** — voor acties die langer duren (backend-verificatie, groot bestand). Bouwt meestal voort op de enabled-stijl met een spinner/indicator links van het label; laat de spinner bij voltooiing overgaan in een vinkje om succes te tonen.
- **Selected** — hoort bij checkboxes/radiobuttons, niet bij buttons zelf. Verwar 'm niet met de pressed-state van een button.

## Button-styles: primary / secondary / tertiary

- **Primary** — meeste visuele nadruk, voor de belangrijkste of meest voorkomende actie (opslaan, afrekenen, aanmaken). Meestal een gevulde, solide knop.
- **Secondary** — gemiddelde nadruk, voor minder belangrijke/frequente acties (annuleren, beantwoorden). Meestal een outline-knop.
- **Tertiary** — minste nadruk, voor optionele/aanvullende acties (bv. "meer bekijken").

Kies de style op basis van hoe belangrijk de actie is binnen die specifieke context — niet op basis van wat er toevallig al in de codebase staat.

## Labels

Een technisch correcte state-implementatie compenseert geen zwak label. Beschrijf concreet wat de knop doet; vermijd generieke labels als "Doorgaan" of "Volgende" — een specifiek label ("Bestelling plaatsen", "Account aanmaken") draagt direct bij aan vindbaarheid en toegankelijkheid.

## Veelgemaakte fouten

- Geen enkele state ontworpen behalve "enabled" — pas bij implementatie blijkt dan dat disabled/hover/focus/pressed ontbreken of inconsistent zijn.
- Disabled-knoppen met zó laag contrast dat het label onleesbaar wordt, óf zó hoog contrast dat gebruikers denken dat de knop klikbaar is.
- Focus alleen tonen via kleurverandering, zonder outline/rand.
- Pressed-feedback die te traag verschijnt, waardoor gebruikers meerdere keren klikken.
- `aria-disabled` vergeten op disabled-knoppen, waardoor screenreader-gebruikers geen onderscheid horen.
- Style (primary/secondary/tertiary) verwarren met state, of meerdere primary-knoppen naast elkaar tonen zonder duidelijke hiërarchie.
- Generieke labels ("Verzenden", "OK") die niet zeggen wat er precies gebeurt.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (vorm, kleurverloop, micro-animaties) kan een galerij zoals collectui.com/designs/button-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de state- en toegankelijkheidsregels hierboven (NN/g) wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Button States: Communicate Interaction](https://www.nngroup.com/articles/button-states-communicate-interaction/)
- CollectUI — [Button UI Design Inspiration](https://collectui.com/designs/button-ui-design-inspiration) (visuele inspiratie)
