# Loading / voortgangsindicatie

Lees dit bestand zodra je zelf besluit een loading state te ontwerpen — spinner, skeleton, voortgangsbalk of anders. Visibility of system status is een van de oudste en belangrijkste bruikbaarheidsheuristieken (NN/g): de gebruiker moet altijd weten dat het systeem zijn actie heeft ontvangen en eraan werkt. Zonder feedback ontstaat onzekerheid, dubbele clicks en voortijdig afhaken.

## Anatomie: twee assen

1. **Determinate vs. indeterminate** (Pencil & Paper) — determinate indicatoren communiceren een begin- en eindpunt en dus een gevoel van duur (percent-done balk, stappenindicator). Indeterminate indicatoren hebben een onzekere duur (spinner, looping animatie) — minder informatief, soms onvermijdelijk.
2. **Passief vs. actief laden** (Pencil & Paper) — passief laden gebeurt vooraf, zonder gebruikersactie (pagina opent, bestand wordt geopend). Actief laden volgt op een gebruikersactie (formulier versturen, export starten). Bij actief laden is directe feedback des te belangrijker: de gebruiker moet meteen weten dat de actie is geregistreerd.

## Kies de indicator op basis van wachttijd

De duur van de wachttijd bepaalt welk type feedback passend is — niet smaak. Vuistregel (NN/g, bevestigd door Pencil & Paper):

- **< 0,1 seconde** — onmiddellijk, niet waarneembaar. Toon gewoon het resultaat. Uitzondering: bij de laatste stap van een lange workflow kan een korte kunstmatige vertraging ("fake loader" / labor illusion) het gevoel geven dat het systeem serieus werk heeft verzet — gebruik dit spaarzaam en bewust.
- **0,1–1 seconde** — merkbaar maar kort. Gebruik hier géén spinner of animatie: gebruikers kunnen niet bijhouden wat er flitst en raken eerder onrustig dan gerustgesteld.
- **1–2 seconden** — geef altijd onmiddellijke feedback zodra de gebruiker een actie start (knop die "ingedrukt" oogt, veld dat vervaagt) — anders herhaalt de gebruiker de actie omdat hij denkt dat er niets gebeurd is.
- **2–10 seconden** — gebruik een looped/indeterminate indicator (spinner) of, beter voor grotere oppervlaktes, een skeleton screen. Voeg waar mogelijk korte tekst toe die uitlegt wat er gebeurt ("Reacties laden…").
- **10 seconden en meer** — gebruik een determinate percent-done indicator (voortgangsbalk/-cirkel) of een stappenindicator. Geef de gebruiker controle: een manier om te annuleren, of de mogelijkheid om door te gaan met iets anders terwijl het systeem doorwerkt.

**Kritieke regel:** laat een percent-done indicator nooit vastlopen op 99%. Als je de duur niet precies kunt schatten, gebruik dan liever een stappenindicator of algemene tijdsindicatie ("dit kan een paar minuten duren") dan een percentage dat je niet kunt waarmaken.

## Patronen per situatie

- **Spinner (indeterminate)** — geschikt voor kleine, afgebaken componenten (knop na klik, rij in een tabel), niet voor volledige paginaladingen langer dan een paar seconden: geen gevoel van voortgang, dus frustratie bij langere wachttijd.
- **Skeleton screen (ghost elements/greeking)** — de norm voor volledige paginaladingen. Toont een wireframe-achtige voorvorm van de layout vóór echte content verschijnt, en zet zo de verwachting van wat komen gaat. Optioneel: shimmer- of pulse-animatie om aandacht van het wachten af te leiden; optioneel dominante-kleur-uitsnede uit afbeeldingen voor visuele dynamiek (alleen bij beeldrijke content).
- **Tijdsindicator (determinate)** — algemene schatting ("dit kan een paar minuten duren") in plaats van een exacte klok; voorkomt beloftes die je niet kunt waarmaken.
- **Voortgangsbalk (determinate)** — werkt zowel op componentniveau als paginaniveau; gebruik een ease-in-animatie zodat de voortgang lijkt te versnellen.
- **Stappenindicator** — breekt de wacht op in behapbare stukken ("Stap 2 van 4", "Dubbele contacten opschonen…"). Toon bij verwerking van meerdere items expliciet hoeveel er al klaar zijn; bied bij langere processen een annuleeroptie.
- **Percent-done indicator (determinate)** — voortgangsbalk/-cirkel die vult naar 100%; geeft gebruikers een concrete inschatting van resterende tijd en dus controle over hun eigen wachttijd.
- **"Meld wanneer klaar" (indeterminate, voor zeer lange taken)** — geen wachttijd in de app zelf; het systeem meldt (in-app of per e-mail) zodra de taak klaar is. Geschikt wanneer de duur niet te schatten is.
- **Taak op de achtergrond (determinate)** — de taak krijgt zichtbaarheid in een klein deel van het scherm (bv. een drawer) zonder de rest van de workflow te blokkeren. Combineert directe feedback, voortgang-zichtbaarheid én ononderbroken workflow — de sterkste combinatie voor grote taken.
- **Statische tekst ("Laden…", "Even geduld") — vermijd dit.** Geeft geen enkele informatie over voortgang; als het systeem vastloopt, heeft de gebruiker geen manier om dat te herkennen.
- **Waarschuwingen als "niet nogmaals klikken"— vermijd dit.** Gebruikers lezen zulke teksten zelden op tijd. Los dubbele acties op door te tonen dat de eerste klik al geaccepteerd is, niet door te dreigen.

## Schaal en volgorde van laden

- **Rijke, complexe componenten (kaarten met afbeelding, tekst, knop)** — laad en toon ze één voor één; dat geeft de gebruiker meteen iets om mee te werken en verlaagt de gepercipieerde wachttijd.
- **Lichte, gelijkvormige componenten (tabelrijen)** — laad en toon in batches of allemaal tegelijk; individueel laden voegt hier weinig toe.
- **Grote hoeveelheden items** — gebruik lazy loading: infinite scroll (passief, automatisch bij naderen van het einde), een "Meer laden"-knop (gebruiker beslist expliciet), of paginering (gebruiker navigeert bewust, bouwt een mentale kaart op van waar content staat). Let op: infinite scroll zonder grenzen kan de paginaprestatie schaden bij zeer grote datasets.

## Frequentie van updates

- **Zeer frequente sync (continu op de achtergrond)** — houd de indicator minimaal en onopvallend (bv. een klein "opgeslagen"-icoon); een opvallende indicator bij elke sync zou storen.
- **Zeldzame updates (gebruiker moet zelf verversen)** — communiceer duidelijk zodra nieuwe content beschikbaar is, met iets prominenters dan bij continue sync (bv. een banner of toast) omdat de gebruiker het anders mist.

## Toegankelijkheid

- Zorg dat animaties (spinners, shimmer, pulse) niet de enige informatiedrager zijn — screenreaders hebben tekstuele aankondiging nodig (bv. via `aria-live` / `aria-busy`) dat er geladen wordt en wanneer dat klaar is.
- Geef contrast tussen skeleton-elementen en achtergrond niet te laag — verifieer met `scripts/contrast_checker.py` in plaats van op het oog te schatten.
- Houd rekening met mobiele verbindingssnelheid: wat op een snelle desktopverbinding 1 seconde duurt, kan op mobiel data ruim boven de 10-seconden-drempel uitkomen — plan de indicator op de trage kant van de schatting, niet de snelle.

## States

- **Direct na actie** — onmiddellijke visuele bevestiging dat de actie geregistreerd is (knop verandert van state, veld vervaagt), los van welke loading-indicator daarna volgt.
- **Bezig (kort, < 10s)** — spinner of skeleton, eventueel met korte statustekst.
- **Bezig (lang, ≥ 10s)** — percent-done of stappenindicator, met optie tot annuleren en/of doorgaan met andere taken.
- **Vastgelopen/timeout** — expliciete foutstatus met vervolgactie (opnieuw proberen, contact/support), nooit een oneindig draaiende spinner zonder uitweg.
- **Klaar** — duidelijke overgang naar eindresultaat; bij "meld wanneer klaar" een expliciete melding (in-app en/of extern).

## Veelgemaakte fouten

- Statische "Laden…"-tekst zonder animatie of voortgangsinformatie.
- Spinner gebruiken voor acties die langer dan 10 seconden duren — gebruikers raken ongeduldig zonder gevoel van voortgang.
- Percent-done indicator die blijft hangen op 99%.
- Geen enkele feedback tonen direct na een gebruikersactie, waardoor de gebruiker denkt dat er niets gebeurd is en opnieuw klikt.
- Waarschuwingen gebruiken ("niet nogmaals klikken") in plaats van simpelweg te tonen dat de actie al geaccepteerd is.
- Labels/skeleton-content met onvoldoende contrast met de achtergrond.
- Bij kinderen/games: een interim-laadanimatie die verward kan worden met de eigenlijke inhoud of het eigenlijke spel.
- Volledige-paginaspinner gebruiken waar een skeleton screen de layout-verwachting beter zou zetten.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (animatiestijlen, kleurgebruik, vormgeving van spinners/skeletons) kan een galerij zoals collectui.com/designs/loading-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de drempel- en toegankelijkheidsregels hierboven (NN/g, Pencil & Paper) wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Progress Indicators Make a Slow System Less Insufferable](https://www.nngroup.com/articles/progress-indicators/)
- Pencil & Paper — [UX Design Patterns for Loading](https://www.pencilandpaper.io/articles/ux-pattern-analysis-loading-feedback)
- CollectUI — [Loading UI Design Inspiration](https://collectui.com/designs/loading-ui-design-inspiration) (visuele inspiratie)
