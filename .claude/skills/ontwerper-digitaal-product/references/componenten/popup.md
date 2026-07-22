# Popup / overlay

Lees dit bestand zodra je zelf besluit een popup, modal, lightbox of overlay te gebruiken. Mensen haten popups (NN/g, decennia aan onderzoek bevestigen dit) — gemiddeld 25 per week per gebruiker, wat ruim boven wat draaglijk is. De meeste popups verschijnen op het verkeerde moment, onderbreken kritieke taken, gebruiken zwakke copy, en desoriënteren gebruikers. Overweeg bij elk gebruik eerst: moet dit echt een popup zijn?

## Anatomie: drie assen

Een popup verschilt op twee onafhankelijke dimensies (NN/g):

1. **Modal vs. nonmodal** — bij modal is de rest van de pagina uitgeschakeld tot de gebruiker de overlay expliciet afhandelt. Bij nonmodal kan de gebruiker nog steeds met de achtergrond interacteren (links volgen, knoppen indrukken) terwijl de overlay zichtbaar blijft.
2. **Gedimde achtergrond of niet** — een overlay met gedimde achtergrond heet een **lightbox**. Lightboxes zijn vaak, maar niet altijd, modal.

Kies bewust: hoe indringender de onderbreking (modal + gedimd), hoe zwaarder de rechtvaardiging moet zijn.

## Timing: nooit vóór interactie of tijdens kritieke taken

- **Nooit een popup tonen vóórdat de hoofdcontent geladen is.** Gebruikers negeren 'm of sluiten 'm meteen — het voelt wanhopig en frustrerend. Enige uitzondering: wettelijk verplichte cookie-/leeftijdstoestemming.
- **Niet direct na inloggen.** Gebruikers hebben een vervolgstap in gedachten (waarom zouden ze anders inloggen?) — geef ze ruimte. Nieuwe features mogen later, en dan liever via een tooltip of kleine nonmodal overlay dan een modal.
- **Niet om een e-mailadres vragen vóór enige interactie.** Gebruikers weten nog niet of ze iets willen abonneren en verwachten spam. Wacht tot een moment waarop het aanbod logisch aansluit (bv. na het lezen van een artikel), en bied iets tastbaars in ruil.
- **Niet om feedback vragen vóórdat de gebruiker iets zinvols gedaan heeft.** Vraag feedback direct ná een afgeronde kerntaak — anders krijg je geen bruikbare respons, of een geïrriteerde gebruiker.
- **Nooit tijdens een kritieke taak onderbreken** (bv. een instapkaart downloaden). Bied in plaats daarvan een permanente, niet-opdringerige weg om feedback te geven: een tab, footerlink, of navigatielink.
- **Nooit meerdere popups na elkaar tonen.** Dat oogt onprofessioneel en overweldigt. Test expliciet of jouw site niet per ongeluk meerdere overlays tegelijk toont.

## Context: transities en toegang tot content niet blokkeren

- **Geen modal vóór een gebruiker naar een subdomein/externe site gaat.** Dit overdrijft de transitie en desoriënteert (gebruikers "weten niet meer waar ze zijn"). Gebruik in plaats daarvan een tooltip op de link, en behoud altijd navigatie terug naar de hoofdsite.
- **Geen modal die de toegang tot content blokkeert** (bv. direct bij het openen van een artikel). Dit ondermijnt vertrouwen en geloofwaardigheid — het voelt alsof toegang "geconditioneerd" wordt. Gebruik een dunne, makkelijk te sluiten banner bovenaan de pagina in plaats daarvan.

## Content: een modal is geen garantie dat de boodschap aankomt

- **Gebruik geen modal voor GDPR/cookiemeldingen.** Gebruikers sluiten modals reflexmatig zonder te lezen. Gebruik een nonmodal overlay onderaan of opzij, met heldere (niet vage) taal over wat er met de data gebeurt.
- **Gebruik geen modal om zonder concreet voordeel over te stappen naar een ander kanaal** (bv. "download onze app"). Gebruikers vrezen opnieuw te moeten beginnen op een ander kanaal. Gebruik een subtiele banner en benoem het concrete voordeel.

## Wanneer een popup wél gerechtvaardigd is

Bewaar modal overlays voor het overbrengen van **cruciale informatie, op het juiste moment** — niet om essentiële taken te onderbreken of relevante content te blokkeren. Denk aan bevestigingsdialogen vóór een onomkeerbare actie (verwijderen, afsluiten zonder opslaan). Test met echte gebruikers of de timing en noodzaak kloppen.

## Veelgemaakte fouten

- Popup verschijnt vóór de pagina geladen is (behalve wettelijk verplichte consent).
- Popup direct na login, terwijl de gebruiker al een vervolgstap in gedachten heeft.
- E-mail- of feedbackverzoek vóór enige zinvolle interactie.
- Meerdere popups tegelijk of na elkaar.
- Modal vóór een externe/subdomein-transitie, zonder duidelijke weg terug.
- Modal die toegang tot content blokkeert in plaats van 'm te ondersteunen.
- GDPR/cookiemelding als opdringerige modal met vage taal in plaats van een rustige nonmodal banner met heldere uitleg.
- Kanaaltransitie (bv. app-download) promoten via een modal zonder concreet voordeel te noemen.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (animaties, lay-out, kleurgebruik) kan een galerij zoals collectui.com/designs/pop-up-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de timing- en contextregels hierboven (NN/g) wegen zwaarder dan een visuele trend: het overgrote deel van popup-problemen zit in wanneer en waarom, niet in hoe het eruitziet.

## Bronnen

- NN/g — [Popups: 10 Problematic Trends and Alternatives](https://www.nngroup.com/articles/popups/)
- CollectUI — [Pop-up UI Design Inspiration](https://collectui.com/designs/pop-up-ui-design-inspiration) (visuele inspiratie)
