# Slider

Lees dit bestand zodra je zelf besluit een slider te gebruiken om een waarde of bereik te laten kiezen. Een slider is een bedieningselement met een knop/hendel die horizontaal beweegt om een variabele te sturen (bv. volume, helderheid) (NN/g). Een precieze waarde kiezen met een slider is moeilijk en vergt fijne motoriek, zelfs bij een goed ontworpen slider — dit is de kernafweging bij dit component.

## De centrale vraag: moet de exacte waarde er echt toe doen?

- **Gebruik een slider alleen als de precieze waarde de gebruiker niet uitmaakt, en een benadering volstaat.** Vertrektijd "rond het middaguur" kiezen werkt prima met een slider; leeftijd, gewicht, of lengte invullen in een formulier niet.
- **Hoe breder of dichter het selecteerbare bereik, hoe moeilijker een precieze waarde te raken is.** Een schaal van 6,0 tot 10,0 in stappen van 0,1 vraagt motorische precisie die de meeste mensen niet hebben — en roept de vraag op waarom je niet gewoon een eenvoudigere 5-puntsschaal gebruikt.
- **Twijfel je?** Kies een ander element dat tikken of typen toestaat in plaats van drag-gebaren: sterren/tik-schaal voor beoordelingen, een getalveld voor gewicht, radiobuttons/dropdown voor een beperkte set opties.

## Waarom sliders lastig zijn: de steering law

Sliders vallen onder dezelfde steering law als dropdowns en horizontale scrollbars: hoe langer en smaller de "tunnel" waarbinnen je moet bewegen, hoe meer tijd en precisie het kost. Op mobiel is dit extra problematisch — gebruikers bedienen het scherm vaak met één hand, terwijl ze lopen of tv kijken, en duwen de slider net van de bedoelde waarde af op het moment dat ze hun vinger optillen.

**Toegankelijkheid weegt hier zwaar.** Mensen met verminderde fijne motoriek (waaronder veel oudere gebruikers) hebben extra moeite met een slider. Vraag jezelf af: zou deze gebruiker ook maar in de buurt van de bedoelde waarde kunnen komen, en hoeveel pogingen zou dat kosten? Zo niet, kies een ander element.

## Think about the thumb: labels moeten zichtbaar blijven

Bij touchscreens bedekt de vinger van de gebruiker een deel van het scherm tijdens het bedienen. Een label vlak onder de slider (prima op desktop met een muis) wordt op mobiel verborgen door de vinger van de gebruiker precies op het moment dat hij de waarde wil aflezen.

**Plaats labels altijd boven of naast de slider-knop, nooit eronder**, zodat ze zichtbaar blijven tijdens de hele interactie — zowel de duim van de gebruiker als de "duim" (knop) van de slider zelf moeten in het zicht blijven.

## Wanneer een slider wél gerechtvaardigd is

- De gebruiker kiest een benaderende waarde binnen een intuïtief begrepen bereik (volume, helderheid, prijsrange bij filteren).
- Het bereik is niet te breed of te fijnmazig voor de vereiste precisie — rond af naar zinvolle stappen (hele uren, hele euro's) in plaats van tiende-precisie.
- Labels/huidige waarde blijven zichtbaar boven of naast de knop tijdens het slepen.

## Veelgemaakte fouten

- Een slider gebruiken voor waarden waar precisie wél telt (leeftijd, gewicht, lengte) — gebruik in plaats daarvan een getalveld of tik-schaal.
- Een te fijnmazige schaal (bv. stappen van 0,1) waarbij de exacte waarde toch weer belangrijk lijkt te zijn — dan had je beter meteen een eenvoudigere schaal of een ander element gekozen.
- Startwaarde die willekeurig ver van de meest waarschijnlijke gebruikerswaarde ligt, waardoor iedereen eerst een lange weg moet afleggen.
- Labels onder de slider-track plaatsen op touchscreens, waardoor de vinger van de gebruiker ze precies verbergt tijdens gebruik.
- Geen rekening houden met motorische beperkingen — geen alternatieve manier bieden om de waarde te tikken of te typen.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (track-styling, knop-vorm, kleurverloop) kan een galerij zoals collectui.com/designs/range-slider-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de precisie- en toegankelijkheidsafweging hierboven (NN/g) weegt zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Slider Design: Rules of Thumb](https://www.nngroup.com/articles/gui-slider-controls/)
- CollectUI — [Range Slider UI Design Inspiration](https://collectui.com/designs/range-slider-ui-design-inspiration) (visuele inspiratie)
