# Footer

Lees dit bestand zodra je zelf besluit een footer te ontwerpen. Een footer is het gebied onderaan elke pagina, onder de hoofdcontent (NN/g). Hij krijgt vaak minder aandacht dan de rest van de pagina, maar gebruikers gebruiken 'm wel degelijk — en een footer kan de ervaring nooit verpesten, alleen verrijken: het is een vrijwel gratis toevoeging aan de UX, mits je 'm niet laat opbollen tot iets dat de laadtijd schaadt.

## Waarom gebruikers de footer bezoeken

Twee hoofdscenario's (NN/g):

1. **Iemand heeft de pagina gescand en vindt niet wat ze zoeken, of wil meer.** De footer is dan een tweede kans om te overtuigen, of een laatste redmiddel voor moeilijk vindbare content (bv. vacatures bij een webshop).
2. **Iemand scrollt bewust naar de footer** omdat ze daar iets verwachten: contactgegevens, bedrijfsinfo, social media, of gerelateerde content. Sommige gebruikers gebruiken de footer zelfs als navigatie wanneer ze toch al onderaan zijn — dichterbij dan terugscrollen naar de top.

Ontwerp de footer dus altijd **consistent, voorspelbaar en makkelijk vindbaar** — ongeacht welke content je erin zet.

## Anatomie / bouwstenen

Kies en combineer op basis van site- en gebruikersdoelen:

- **Utility links** — contactgegevens, klantenservice, privacybeleid, gebruiksvoorwaarden. Voor vrijwel elke site: gebruikers zoeken hier specifiek naar deze items, ook als ze al bovenaan staan.
- **Doormat navigation** — de globale navigatie herhaald in de footer. Nuttig bij lange pagina's waar de hoofdnavigatie niet meer zichtbaar is onderaan.
- **Secundaire taken** — vacatures, investeerdersinformatie, documentatie/specificaties, mediakits, affiliates: taken die niet in de hoofdnavigatie thuishoren maar wel relevant zijn voor een deel van je gebruikers.
- **Sitemap-achtig overzicht** — combinatie van hoofdnavigatie én onderliggende subcategorieën. Alleen zinvol tot ongeveer 25 pagina's; anders wordt het onhandelbaar. Bij grotere sites: link naar een aparte sitemap-pagina in plaats van alles in de footer te proppen.
- **Testimonials/awards** — bouwt autoriteit en vertrouwen op, vooral nuttig voor startups of merken met weinig naamsbekendheid. Niet overdrijven — te veel testimonials wekt juist wantrouwen ("waarom moeten ze dit zo hard bewijzen?").
- **Merken binnen de organisatie** — relevant voor grote, multinationale organisaties met meerdere submerken.
- **Customer engagement** — nieuwsbrief-aanmelding, social-mediakoppelingen. Overweeg een ingesloten social-feed alleen als het account actief genoeg is om die ruimte te verdienen.

Fat-footer-variant (ui-patterns.com) bevat doorgaans: about-us, terms of service, privacybeleid, sitemap-achtige links, contact, adres/telefoonnummer (bouwt vertrouwen — toont dat het bedrijf "echt" is), social links.

## Wanneer welke variant

- **Lange pagina's / geen zichtbare hoofdnavigatie onderaan** → doormat navigation.
- **Grote site met meerdere niveaus of subdomeinen** → sitemap-achtig overzicht (begrensd tot ~25 links, anders doorverwijzen naar aparte sitemap-pagina).
- **Meerdere gebruikersgroepen met sterk uiteenlopende taken** (bv. klant vs. sollicitant vs. investeerder) → secundaire-taken-footer, eventueel contextueel per pagina/rol (bv. andere footer voor ingelogde leden vs. bezoekers).
- **Infinite scroll** (geen vaste paginabodem) → geen traditionele footer; plaats een "mini footer" met de utility-links in de rechter-kolom, sticky tijdens het scrollen. Gebruik nooit dezelfde footer voor zowel statische als oneindig scrollende pagina's — dat wordt een frustrerend "whack-a-mole"-spel waarbij links wegscrollen voordat gebruikers erop kunnen klikken.

## Veelgemaakte fouten

- **Meer dan twee niveaus informatiehiërarchie** proppen in de footer, of de hele sitemap erin zetten. Als alles belangrijk is, is niets belangrijk — herprioriteer naar alleen eerste- en tweede-niveau categorieën; een enkele belangrijke onderliggende pagina mag je alsnog expliciet tonen.
- **Onduidelijke linknamen** zoals "Resources" of "Company Info" in plaats van concrete termen als "Contact opnemen". Bij twijfel: toets de terminologie met een card sort of usability test.
- **Geen duidelijke structuur** — de footer als dumping ground voor losse links zonder groepering. Gebruikers doen dan óf een uitputtende blik óf negeren de footer volledig. Gebruik visuele hiërarchie (vetgedrukte hoofdcategorieën, normaal gewicht voor subniveaus) om structuur te tonen.
- **Onleesbare of verborgen footers** — te kleine tekst, te laag contrast, of een geanimeerde/accordion-footer die standaard is ingeklapt. Mensen verwachten de footer er gewoon te vinden; verberg 'm niet voor esthetiek.

## Toegankelijkheid & leesbaarheid

- Leesbare tekstgrootte en voldoende contrast — verifieer met `scripts/contrast_checker.py` (zie hoofdmap van deze skill) in plaats van op het oog te schatten.
- Geen decoratieve lettertypes voor footer-links; scanbaarheid gaat boven esthetiek hier.
- Behandel de footer niet als bijzaak in de tab-volgorde: links moeten net zo logisch doorlopen als de rest van de pagina.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (lay-out, kleurgebruik, iconografie) kan een galerij zoals collectui.com/designs/footer-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de structuur- en vindbaarheidsregels hierboven (NN/g, ui-patterns.com) wegen zwaarder dan een visuele trend.

## Bronnen

- NN/g — [Footers 101: Design Patterns and When to Use Each](https://www.nngroup.com/articles/footers/)
- ui-patterns.com — [Fat Footer](https://ui-patterns.com/patterns/FatFooter)
- CollectUI — [Footer UI Design Inspiration](https://collectui.com/designs/footer-ui-design-inspiration) (visuele inspiratie)
