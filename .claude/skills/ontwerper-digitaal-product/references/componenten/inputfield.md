# Input field

Lees dit bestand zodra je zelf besluit een tekstinvoerveld te ontwerpen. Een invoerveld vraagt meer van de gebruiker dan bijna elk ander UI-element: waar een klik passief is, moet de gebruiker bij een invoerveld stoppen, nadenken, iets onthouden en het correct typen. Dat maakt dit element een van de kwetsbaarste punten in elke flow — kleine ontwerpfouten hebben grote impact op afhaakpercentages.

## Anatomie

Een tekstinvoerveld bestaat uit zes onderdelen (Aufait UX):

- **Container** — de interactieve zone; communiceert visueel states als focus, fout, disabled.
- **Label** — zegt wat het veld verwacht; blijft altijd zichtbaar.
- **Placeholder/voorbeeldtekst** — optionele aanvullende hint of formaatvoorbeeld, verdwijnt bij typen.
- **Helper text** — extra uitleg bij regels of beperkingen die niet vanzelfsprekend zijn.
- **Foutmelding** — legt uit wat er mis is en hoe de gebruiker het oplost.
- **Optionele iconen** — bv. zoeken, veld leegmaken, wachtwoord tonen.

## Label vs. placeholder: nooit vervangen

- **Gebruik nooit een placeholder als vervanging van het label.** Zodra de gebruiker begint te typen verdwijnt de placeholder, en moet hij onthouden wat er ook alweer gevraagd werd — vooral bij lange formulieren, onderbrekingen (tabwisseling, telefoontje) of mobiel gebruik is dat een reëel probleem (NN/g).
- **Zonder zichtbaar label kan de gebruiker zijn invoer niet controleren** vóór het versturen, en bij een foutmelding niet zien wat er mis ging zonder elk veld opnieuw leeg te klikken.
- **Placeholder-tekst heeft doorgaans te weinig contrast** (standaard lichtgrijs) en wordt niet door elke screenreader voorgelezen — een toegankelijkheidsprobleem op zich.
- **Lege velden trekken het oog** (eyetracking); een veld met placeholder-tekst erin wordt minder snel opgemerkt of aangezien voor een reeds ingevulde waarde, waardoor gebruikers het overslaan.
- **Floating labels** (label verschuift naar boven bij focus) zijn een verbetering t.o.v. pure placeholders — ze lossen het geheugenprobleem op — maar hebben nog steeds de zichtbaarheids- en toegankelijkheidsnadelen. **Beste optie, als de ruimte het toelaat: label altijd zichtbaar boven het veld, placeholder alleen voor aanvullende voorbeeldtekst.**
- Gebruik placeholders nooit als enige bron van kritieke instructies — die horen altijd buiten het veld, permanent zichtbaar.

## Layout: proximiteit en whitespace (Gestalt Law of Proximity)

- **Plaats het label dichter bij het bijbehorende veld dan bij andere velden.** Gelijke afstand tussen alle labels en velden laat de gebruiker aarzelen over welk label bij welk veld hoort — en die aarzeling kost al respons-rate.
- **Groepeer gerelateerde velden visueel** (bv. "Persoonlijke gegevens", "Contactgegevens") met extra witruimte tussen groepen. Dit breekt een lang formulier op in kleinere, behapbare stukken zonder het aantal velden te verminderen.
- **Plaats labels boven het veld, niet links ernaast.** Boven-plaatsing kost meer verticale ruimte maar is het best scanbaar: label en veld vallen in dezelfde oogfixatie, en lange labels passen zonder afkapping. Links uitgelijnde labels mogen alleen als ruimte een harde eis is — houd ze dan qua lengte gelijk en zo dicht mogelijk bij het veld; rechts uitgelijnde labels ver van het veld zijn de slechtste optie.
- **Gebruik een enkele kolom-layout** voor de hoofdstroom van een formulier — dat volgt de natuurlijke top-naar-onder leesrichting en voorkomt gemiste velden. Meerdere kolommen alleen bij korte, nauw verwante velden die de gebruiker al herkent (bv. Plaats/Provincie/Postcode).

## Doel en type per veld

- **Maak per veld direct duidelijk wat er verwacht wordt** — nooit laten gokken. Onduidelijke doelbepaling is een van de belangrijkste redenen voor vertraging en afhaken.
- **Houd labels kort, op één regel, in gewone taal** — geen jargon, geen meerdere regels. Verplaats gedetailleerde uitleg naar helper text onder het veld.
- **Kies het juiste besturingselement, niet automatisch een tekstveld:** radiobuttons voor een kleine, enkelvoudige keuzeset (alle opties in één oogopslag); checkboxes voor meervoudige selectie; dropdown alleen bij langere lijsten; zoek/autosuggest bij zeer grote sets (landen, steden). Zichtbaarheid van opties vermindert nadenken — zie ook `dropdown.md`.
- **Veldbreedte is een visuele aanwijzing voor het verwachte type invoer.** Een te lang postcodeveld suggereert meer invoer dan nodig; een te krap tekstvak voor een bericht ontmoedigt uitgebreide invoer. Match de breedte op de verwachte lengte.

## Typen verminderen

- **Autocomplete bekende gegevens** (naam, e-mail, adres) — laat de gebruiker niet herhalen wat het systeem al weet.
- **Auto-suggest bij lange/complexe lijsten** (land, functietitel) om scrollen en zoeken te vermijden.
- **Pre-fill intelligent, maar houd het bewerkbaar** — gebruikers vertrouwen systemen die helpen, niet systemen die vastzetten.
- **Automatische opmaak tijdens typen** voor telefoonnummers, datums, creditcardnummers, zodat de gebruiker niet over syntaxis hoeft na te denken.
- **Sta copy-paste toe in elk veld**, inclusief wachtwoordvelden — plakken is vaak betrouwbaarder dan overtypen.

## Gevoelige invoer: transparantie

- **Leg uit waarom je iets vraagt**, direct naast het veld, in gewone taal ("we gebruiken je telefoonnummer voor belangrijke updates, niet voor reclame").
- **Geef een "toon wachtwoord"-optie** in plaats van dubbele wachtwoordinvoer — dat helpt fouten voorkomen zonder de gebruiker te vertragen.
- **Vermijd dubbele invoer ter controle** (wachtwoord tweemaal typen); zichtbaarheids-toggle plus directe feedback werkt beter.

## Validatie en foutmeldingen

- **Valideer tijdens het typen, niet pas na versturen.** Feedback die pas na submit verschijnt voelt bestraffend en dwingt de gebruiker de hele pagina af te speuren naar wat mis ging.
- **Plaats de foutmelding direct onder het betreffende veld**, in simpele, neutrale taal, met een concrete oplossing. Vermijd vage meldingen ("Ongeldige invoer", "Er ging iets mis").
- **Gebruik input-masks/beperkingen om ongeldige tekens te voorkomen** in plaats van foutieve invoer pas achteraf af te keuren.
- **Geef rustige, directe visuele bevestiging** wanneer invoer correct is — dat bouwt vertrouwen op tijdens het formulier, niet pas aan het eind.

## Mobiel: 14-punts checklist (NN/g, verkort naar kernregels)

- **Is dit veld echt noodzakelijk?** Elk overbodig veld is een drempel.
- **Label boven het veld** (niet erin, niet eronder); markeer velden als verplicht/optioneel; geen placeholder-tekst als vervanging.
- **Veld groot genoeg** om de meeste waarden zichtbaar te tonen, en zichtbaar in beide schermoriëntaties mét geopend toetsenbord.
- **Vul zoveel mogelijk voor de gebruiker in:** slimme standaardwaarden, invoergeschiedenis, veelgebruikte waarden, telefoonfuncties (camera, gps, spraak, contacten), of bereken de waarde uit andere velden (bv. plaats uit postcode).
- **Ondersteun copy-paste.**
- **Gebruik het juiste toetsenbordtype** (numeriek voor cijfers, e-mailtoetsenbord voor e-mail, enzovoort).
- **Bied autocomplete/suggesties op basis van de eerste letters.**
- **Autocorrigeer nooit namen, adressen of e-mailadressen.**
- **Sta typefouten/afkortingen toe waar mogelijk**, en laat de gebruiker het eigen voorkeursformaat gebruiken (telefoonnummers, creditcardnummers) — auto-formatteer het voor hen in plaats van een streng format af te dwingen.

## Toegankelijkheid

- Zorg voor voldoende contrast tussen tekst/labels en achtergrond (WCAG: minimaal 4,5:1 voor normale tekst) — verifieer met `scripts/contrast_checker.py` in plaats van op het oog te schatten.
- Zorg voor zichtbare focus-states voor toetsenbord- en assistieve-technologiegebruikers.
- Formulier volledig bedienbaar met alleen het toetsenbord, met logische tab-volgorde.
- Labels, instructies en foutmeldingen correct gekoppeld (bv. via `<label for>`/`aria-describedby`) zodat screenreaders ze meesturen.
- Vertrouw nooit op kleur alleen om status (fout/succes) aan te geven — combineer met tekst en/of icoon.

## States

- **Leeg (rust)** — label zichtbaar boven het veld, eventuele placeholder als aanvullend voorbeeld.
- **Focus** — duidelijke visuele focusindicator, placeholder verdwijnt (indien aanwezig), label blijft staan.
- **Invoer bezig / inline validatie** — directe, rustige feedback zodra genoeg context bekend is (niet meteen bij het eerste teken).
- **Fout** — foutmelding direct onder het veld, in duidelijke taal met oplossing; veldrand/icoon ondersteunt maar vervangt de tekst niet.
- **Correct/bevestigd** — subtiele positieve indicatie (bv. vinkje), geen overdreven animatie.
- **Disabled** — visueel duidelijk onderscheiden van invulbare velden, met `aria-disabled` waar relevant (zie ook `button.md` voor de disabled-vs-aria-disabled afweging).

## Veelgemaakte fouten

- Placeholder gebruiken als vervanging van het label.
- Labels te ver van hun veld plaatsen, of alle labels op gelijke afstand van alle velden zetten.
- Een lang formulier zonder groepering/witruimte, waardoor het overweldigend oogt.
- Foutmeldingen pas tonen na volledige submit, in plaats van tijdens het typen.
- Vage foutmeldingen ("Ongeldige invoer") zonder concrete oplossing.
- Dubbele wachtwoordinvoer i.p.v. een zichtbaarheids-toggle.
- Een tekstveld gebruiken waar een radiobutton/checkbox/dropdown sneller en duidelijker zou zijn.
- Autocorrectie toepassen op namen, adressen of e-mailadressen.
- Veldbreedte die niet overeenkomt met de verwachte invoerlengte.
- Formulieren alleen voor desktop ontwerpen, waardoor typen en precisie op mobiel lijden.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (veldstyling, iconografie, kleurgebruik) kan een galerij zoals collectui.com/designs/form-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de label-, validatie- en toegankelijkheidsregels hierboven (NN/g, Aufait UX) wegen zwaarder dan een visuele trend.

## Bronnen

- Aufait UX — [Input Field Design Best Practices](https://www.aufaitux.com/blog/input-field-design-best-practices/)
- NN/g — [Placeholders in Form Fields Are Harmful](https://www.nngroup.com/articles/form-design-placeholders/)
- NN/g — [Group Form Elements Effectively Using White Space](https://www.nngroup.com/articles/form-design-white-space/)
- NN/g — [A Checklist for Designing Mobile Input Fields](https://www.nngroup.com/articles/mobile-input-checklist/)
- CollectUI — [Form UI Design Inspiration](https://collectui.com/designs/form-ui-design-inspiration) (visuele inspiratie)
