# Dashboard

Lees dit bestand zodra je zelf besluit een dashboard te ontwerpen. Een dashboard is een verzameling datavisualisaties op één scherm die in één oogopslag actiegerichte informatie geeft (ui-patterns.com, NN/g) — de metafoor is het dashboard van een auto: je wilt "Ben ik te snel?" kunnen zien zonder erover na te hoeven denken. Een dashboard is geen portal en geen plek om data te *verkennen*; het is bedoeld om snel te consumeren, met minimale interactie en cognitieve inspanning.

## Type dashboard bepaalt de rest van je keuzes

- **Operationeel** — dagelijkse bedrijfsvoering monitoren (serverstatus, dagverkoop, supportqueue). Vaak (bijna) real-time data; gebruikers nemen tijdgevoelige, onmiddellijke beslissingen.
- **Strategisch/executive** — periodieke KPI's (dagelijks/wekelijks/maandelijks) voor een leidinggevend team. Hoogniveau-overzicht, niet tijdgevoelig.
- **Analytisch** — biedt drill-down op operationele of strategische data voor wie dieper wil graven.

Bepaal dit vóór je een layout kiest: een operationeel dashboard vraagt om onmiddellijke leesbaarheid zonder interactie; een analytisch dashboard mag meer interactie en gelaagdheid bevatten.

## De vier kernvariabelen: kies bewust waar de spanning zit

Een dashboard-ontwerp is altijd een afweging tussen vier parameters: **schermruimte, data-abstractie, aantal pagina's, en interactie**. Wil je minder schermruimte gebruiken (of op één scherm blijven), dan moet je elders compenseren: sterkere abstractie van de data, meer pagina's, of meer interactie (doorklikken, filteren). Er bestaat geen ontwerp dat op alle vier tegelijk wint — wees expliciet over welke variabele je laat meebewegen.

## Houd het simpel: cognitieve belasting is de vijand

Onderzoek naar cognitive load theory (Sweller) onderscheidt drie soorten mentale inspanning:

- **Intrinsieke belasting** — de data is inherent complex; dat kun je niet wegontwerpen.
- **Extraneous belasting** — mentale energie verspild aan slecht ontwerp: rommelige layouts, verwarrende navigatie, ongelabelde grafieken. Dít moet je elimineren.
- **Germane belasting** — de productieve inspanning van patroonherkenning en inzicht. Hier is data-visualisatie ei͏genlijk voor bedoeld.

Het werkgeheugen houdt maar 3–5 items tegelijk vast (Miller/Cowan). Overschrijd je die capaciteit, dan maken gebruikers meer fouten, worden ze trager, en haken ze af.

Begin daarom met een eenvoudig ontwerp dat alleen de belangrijkste data uitlicht; voeg pas daarna eventueel meer toe. Eenvoudige representaties (staafdiagrammen, lijngrafieken, tabellen) zijn vaak duidelijker dan visueel complexe of "hippe" alternatieven.

**Test het zelf met de 5-seconden-test:** zet iemand die het dashboard niet kent ervoor en vraag wat het belangrijkste op het scherm is. Lukt dat niet binnen 5 seconden, dan moet je eerst dát oplossen vóór je verder bouwt.

## Preattentive processing: welke grafiekvorm gebruik je

Mensen verwerken bepaalde visuele eigenschappen razendsnel, zonder er bewust aandacht aan te besteden ("preattentive processing"): lengte, 2D-positie, oppervlakte, hoek en kleur. Niet al deze eigenschappen zijn even geschikt voor kwantitatieve informatie:

- **Lengte en 2D-positie** worden nauwkeurig en snel ingeschat. Gebruik daarom: **staafdiagrammen** (lengte — vergelijkingen tussen categorieën), **lijngrafieken** (2D-positie — trends over tijd), **spreidingsdiagrammen** (2D-positie — correlaties tussen variabelen).
- **Oppervlakte en hoek** worden slecht ingeschat — mensen kunnen wel zien dát iets groter is, maar niet goed hoevéél groter. Vermijd daarom **taartdiagrammen, donut charts, treemaps en gauges/meters** voor het snel communiceren van kwantitatieve verschillen. Een taartdiagram met meer dan 3–4 segmenten is vrijwel nooit de juiste keuze.
- **Vermijd 3D volledig.** 3D-weergave vervormt lengte, oppervlakte en hoek en maakt elke grafiek moeilijker te interpreteren — ook staafdiagrammen die normaal juist heel goed werken.
- **Kleur en vorm** zijn geschikt om categorieën/groepen te tonen (Gestalt-principe van gelijkenis: gelijke vorm/kleur wordt als gerelateerd gezien), maar níet om kwantitatieve waarden te communiceren — mensen ervaren kleuren niet als geordend.
- **De hover-test:** als een gebruiker moet hoveren om te begrijpen wat een grafiek toont, heeft de grafiek gefaald. Labels, legenda's en annotaties moeten in één oogopslag duidelijk zijn, zonder interactie.

## Gebruik interactie om ruimte te besparen — niet om complexiteit te verstoppen

Filters, dropdowns en knoppen beperken wat er op één scherm hoeft te staan. Twee kernpatronen:

- **Detail on demand** — extra info via hover/pop-up, zonder het scherm permanent te vullen.
- **Progressive disclosure** — toon eerst het essentiële, laat gebruikers klikken/uitklappen voor detail. Volg herkenbare hiërarchieën: geografisch (regio → land → stad), temporeel (jaar → kwartaal → maand → week), categorisch (afdeling → team → individu).

Let op Hick's wet: te veel filters tegelijk (20 opties) is cognitieve sabotage. Toon alleen het essentiële vooraf en verstop geavanceerde opties achter een "meer filters"-toggle.

## Context is niet optioneel

Een los getal zegt niets. Elke KPI-kaart heeft idealiter drie soorten context:

- **Temporele vergelijking** — week-over-week of maand-over-maand, met richting (omhoog/omlaag).
- **Benchmark/doel** — is het target gehaald?
- **Trendindicator** — sparkline, richtingspijl, of kleurgecodeerde status waarmee je in één oogopslag ziet: gezond, risico, of falend.

Er is een grens: genoeg context om een oordeel te vellen, niet om alle detail in één kaart te proppen. Wil de gebruiker dieper graven, gebruik dan een drill-down, geen overvolle kaart.

## Stem af op je doelgroep

- **Beginners/incidentele gebruikers** → gelaagde (stratified) layout met de belangrijkste data bovenaan, weinig interactie, sterk geabstraheerde informatie. Ontwerp niet voor de meest datageletterde persoon in de kamer en neem aan dat de rest zich wel aanpast — dat gebeurt niet, mensen haken af.
- **Experts/frequente gebruikers** → meer detail, personalisatie-opties, complexe analytische interacties (drill-downs).

Definieer per gebruikersrol wat ze moeten kunnen beslissen op basis van de data — als niemand een concreet antwoord heeft op "welke actie onderneem je op basis van dit cijfer?", hoort die metric niet op het dashboard (onderscheid vanity metrics zoals paginaweergaven van decision metrics zoals churn rate).

## Layout structureren

- **Volg het F-patroon**: gebruikers scannen eerst horizontaal bovenaan, dan een kortere sweep lager, dan verticaal langs links. Bij herhaalde elementen (een rij KPI-kaarts) valt de aandacht het sterkst op het eerste item en neemt af naar rechts/onder — bij vijf KPI-kaarts naast elkaar registreren gebruikers de laatste twee nauwelijks.
- **Inverted pyramid als structuur**: bovenaan de 3–5 belangrijkste samenvattende metrics (grote, leesbare getallen + context), middenin trend-/tijdreeksgrafieken, onderaan gedetailleerde tabellen voor wie verder wil graven.
- **Organiseer symmetrisch en groepeer op gedeelde attributen** (Gestalt: nabijheid, gelijkenis, omsluiting). Cluster omzetmetrics bij elkaar, engagementmetrics bij elkaar — gerelateerde data die visueel samen staat, laat patronen zien zonder extra denkwerk.
- **Gebruik een grid** (12- of 16-koloms, met een basiseenheid van 8px) voor consistente uitlijning, en genereuze witruimte tussen kaart-groepen om cognitieve belasting te verlagen.
- **Fitts' wet**: maak kritieke KPI's en actieknoppen groot en makkelijk bereikbaar; verstop ze niet in hoeken of achter kleine iconen.
- **Tabel-layout** voor het naast elkaar vergelijken van gelijksoortige data; **gelaagde layout** om de belangrijkste indicatoren bovenaan te benadrukken.

## States: ontwerp ook leeg, ladend en fout

- **Lege staat** — de grootste gemiste kans. Behandel het als een onboarding-moment: toon hoe de gevulde weergave eruitziet en geef een concrete volgende stap, in plaats van een leeg scherm.
- **Laadstatus** — skeletschermen die de uiteindelijke layout spiegelen houden gebruikers georiënteerd terwijl data laadt.
- **Foutstatus** — "Er ging iets mis" is geen ontwerpbeslissing. Gebruik heldere taal die zegt wat er gebeurde, en geef een concreet vervolgpad (opnieuw proberen, filter aanpassen, contact opnemen).

## Kleur: terughoudend en doelbewust

Kleur wordt structureel overgebruikt in dashboards. Gebruik een consistent kleurenschema per data-categorie en zet kleur nooit in zonder functionele of semantische betekenis. Gebruik kleur niet als primair middel om kwantitatieve waarden te communiceren (zie preattentive processing hierboven) — wel om categorieën te onderscheiden, als secundaire versterking van een signaal dat al via vorm of positie communiceert. Ongeveer 8% van de mannen heeft een vorm van kleurenblindheid: een rood/groen statussysteem is onvoldoende zonder tekstlabel ("Op schema", "Risico") erbij.

## Toegankelijkheid

- Kleurcontrast: minimaal 4,5:1 voor tekst, 3:1 voor grote tekst en UI-componenten (WCAG 2.1 AA) — verifieer met `scripts/contrast_checker.py` in plaats van op het oog te schatten.
- Volledige toetsenbordnavigatie: Tab, Shift+Tab, Enter, Escape moeten elk interactief element bereiken.
- ARIA-labels op alle interactieve elementen voor screenreader-ondersteuning.
- Leesbaar op 200% zoom zonder dat content breekt of overlapt.
- Koppel kleur altijd aan een tweede signaal (vorm, tekstlabel, patroon) — nooit kleur alleen.

## Veelgemaakte fouten

- Grafieken tonen die nobody leest omdat ze niet aan een concrete beslissing gekoppeld zijn (vanity metrics in plaats van decision metrics).
- Ontwerpen voor de meest ervaren gebruiker en aannemen dat de rest zich aanpast.
- Taartdiagrammen, donut charts, treemaps of gauges gebruiken om kwantitatieve verschillen snel te communiceren.
- 3D-grafieken — lost geen enkel leesbaarheidsprobleem op, creëert er juist een.
- Een los getal tonen zonder temporele vergelijking, benchmark of trend.
- Meer dan 3–5 items tegelijk laten opvallen in een rij herhaalde elementen (KPI-kaarts) zonder prioritering.
- Twintig filters tegelijk tonen in plaats van de essentiële vooraf en de rest achter progressive disclosure.
- Geen lege/laad/foutstatus ontworpen — pas bij eerste gebruik of storing blijkt dat het scherm dan gewoon leeg of cryptisch is.
- Kleur als enige onderscheid tussen statussen, zonder tekstlabel of vorm erbij.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (kaartstijlen, kleurgebruik, kleine animaties) kan een galerij zoals collectui.com/designs/dashboard-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de leesbaarheids- en cognitieve-belastingregels hierboven wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Dashboards: Making Charts and Graphs Easier to Understand](https://www.nngroup.com/articles/dashboards-preattentive/)
- ui-patterns.com — [Dashboard](https://ui-patterns.com/patterns/dashboard)
- UX Pilot — [12 Dashboard Design Principles For Better UX](https://uxpilot.ai/blogs/dashboard-design-principles)
- CollectUI — [Dashboard UI Design Inspiration](https://collectui.com/designs/dashboard-ui-design-inspiration) (visuele inspiratie)
