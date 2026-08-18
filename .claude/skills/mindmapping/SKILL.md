---
name: mindmapping
description: Maak een volledige mindmap volgens de Buzan-methode op basis van één enkel woord of kort begrip dat de gebruiker aanlevert, gericht op de onderwijssector (mbo/hbo/wo). Gebruik deze skill altijd wanneer de gebruiker een mindmap, gedachtekaart, brainstormkaart, spindiagram, concept map of associatiekaart vraagt — ook wanneer ze alleen een woord noemen met "mindmap dit", "maak hier een mindmap van", "brainstorm rond X", "wat komt hier allemaal bij kijken", "breng X in kaart" of "geef me overzicht van het thema X". Trigger ook bij het voorbereiden van een les, workshop, presentatie, scriptie, samenvatting, projectplan of vergadering waarbij de gebruiker eerst het onderwerp wil verkennen of structureren. Levert een mindmap in het gekozen formaat (markdown-outline, Mermaid-diagram of visuele SVG) plus een korte toelichting.
---

# Mindmapping

Maak van één woord een complete, bruikbare mindmap volgens de methode van Tony Buzan, toegespitst op de Nederlandse onderwijssector.

De gebruiker levert typisch weinig: één woord, soms een korte zin. Dat is genoeg. De waarde zit in het associëren — jij vult de kaart, de gebruiker herkent, schrapt en breidt uit. Vraag niet door voordat je iets maakt. Maak eerst een kaart, bied daarna aan om te verdiepen.

## Wat een goede mindmap doet

Buzan's uitgangspunt: het brein werkt associatief en visueel, niet lineair. Een mindmap benut dat door een centraal beeld, radiale hoofdtakken, sleutelwoorden en kleur te combineren. De structuur zelf is het geheugenanker — de gebruiker onthoudt de vorm, niet de zinnen.

Praktisch betekent dat:

- **Eén sleutelwoord per tak.** Geen zinnen. "Toetsing" niet "Hoe we toetsen inrichten".
- **Sleutelwoorden zijn associatiekapstokken.** Kies woorden die verder vertakken, niet woorden die dichttimmeren.
- **5-7 hoofdtakken.** Minder is dun, meer is onoverzichtelijk. Zeven is het plafond van het werkgeheugen.
- **2-3 niveaus diep** per hoofdtak. Dieper mag als het thema dat draagt.
- **Kleur per hoofdtak**, consistent doorgevoerd naar de subtakken.
- **Symbolen en beeld** waar het helpt — een icoon onthoudt makkelijker dan een woord.
- **Kruisverbanden** tussen takken die elkaar beïnvloeden. Dit is waar mindmaps meer opleveren dan een boomstructuur: leg minstens 2-3 verbanden tussen verschillende takken.

Wees flexibel met deze regels. Als een sleutelwoord twee woorden nodig heeft om te kloppen, gebruik er twee. Structuur dient het denken, niet andersom.

## Werkwijze

### 1. Bepaal het formaat

Als de gebruiker geen formaat noemt, vraag het kort met de opties: **markdown-outline** (snel, kopieerbaar), **Mermaid** (diagram in tekst, werkt in Notion/GitHub/docs) of **visueel SVG** (echte radiale mindmap met kleur, printbaar). Bij twijfel of haast: maak SVG, dat sluit het dichtst aan op Buzan.

Vraagt de gebruiker "alles" of "meerdere"? Lever markdown-outline plus SVG.

### 2. Associeer breed voor je structureert

Voordat je takken kiest: genereer intern minstens 20-30 associaties bij het centrale woord. Divergeer eerst, ruim daarna op. Als je meteen naar nette categorieën springt, krijg je een saaie kaart met de voor de hand liggende indeling.

Zoek daarbij bewust naar:
- Het onverwachte perspectief (wie heeft hier last van? wat gaat er mis? wat is de tegenbeweging?)
- Het concrete (welke tool, welke wet, welk cijfer, welk moment in het jaar)
- De spanning (waar botsen belangen?)

### 3. Clusteren naar hoofdtakken

Groepeer de associaties tot 5-7 hoofdtakken. Gebruik de onderwijs-perspectieven in `references/onderwijscontext.md` als check: dek je genoeg invalshoeken af, of zit alles in één hoek? Lees dat bestand wanneer het thema onderwijsspecifiek is en je meer grip wilt op de sector — actoren, wetgeving, jaarritme, gangbare thema's.

Vermijd de luie indeling (Voordelen / Nadelen / Toekomst). Kies takken die het specifieke thema recht doen.

### 4. Bouw de mindmap

Volg het gekozen formaat. Zie `references/formaten.md` voor de exacte sjablonen van markdown, Mermaid en SVG — lees dat bestand vóór je de mindmap genereert, de SVG-opbouw en kleurgebruik staan daar uitgeschreven.

### 5. Lever op

Geef bij de mindmap kort mee:
- **Waar je bewust bent afgeweken** of iets hebt weggelaten (max 2 zinnen).
- **Twee tot drie takken die zich lenen voor verdieping**, als aanbod: "Zal ik `Toetsing` uitwerken tot een eigen mindmap?"

Geen lange toelichting. De kaart spreekt voor zich.

## Toepassing sturen

Het formaat mag hetzelfde blijven, maar de invalshoek verschilt per gebruikssituatie. Herken deze en pas de takken aan:

**Leren en onthouden** (samenvatting, examen, scriptie) → takken volgen de structuur van de stof, sleutelwoorden zijn triggerwoorden voor reproductie. Meer diepte, minder breedte.

**Brainstorm en creativiteit** (nieuw idee, ontwerpvraag) → takken zijn perspectieven, niet categorieën. Duw richting het onverwachte. Meer kruisverbanden.

**Planning en overzicht** (project, les, vergadering) → takken zijn fasen, rollen of resultaten. Concrete subtakken: wie, wanneer, wat af.

**Analyse en besluitvorming** (beleid, probleem) → takken zijn krachten of belanghebbenden. Kruisverbanden dragen hier de meeste betekenis.

Weet je het niet? Kies de brainstorm-invalshoek — die is het meest generatief en de gebruiker kan altijd bijsturen.

## Voorbeeld

**Input:** "Kunstmatige intelligentie"

**Slechte takken:** Voordelen / Nadelen / Geschiedenis / Toekomst / Voorbeelden
→ generiek, past op elk onderwerp, nodigt niet uit tot associatie.

**Goede takken (onderwijscontext):** Toetsing & fraude / Docentrol / Studentvaardigheden / Data & privacy / Instellingsbeleid / Arbeidsmarkt
→ specifiek, elk met eigen spanning, en kruisverbanden liggen voor de hand (Toetsing ↔ Studentvaardigheden, Data & privacy ↔ Instellingsbeleid).

## Wanneer je géén mindmap moet maken

Als de gebruiker een lineair antwoord wil (een uitleg, een lijst, een tekst), lever dat. Een mindmap is een denkinstrument, geen decoratie. Bij twijfel: maak de mindmap én bied aan het uit te schrijven.
