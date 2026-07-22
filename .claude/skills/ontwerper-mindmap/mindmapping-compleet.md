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


---

# Bijlage A - references/formaten.md

# Uitvoerformaten

Drie formaten. Lees het deel dat je nodig hebt.

- [1. Markdown-outline](#1-markdown-outline)
- [2. Mermaid](#2-mermaid)
- [3. Visuele SVG](#3-visuele-svg)
- [4. Kleurenpalet](#4-kleurenpalet)
- [5. Symbolen](#5-symbolen)

---

## 1. Markdown-outline

Snelst, kopieerbaar naar elk document. Lever als bestand (`.md`) wanneer de gebruiker het wil bewaren, anders inline in de chat.

Structuur:

```markdown
# 🧠 [CENTRAAL WOORD]

## 🎯 [Hoofdtak 1]
- [Sleutelwoord]
  - [Sub-sleutelwoord]
  - [Sub-sleutelwoord]
- [Sleutelwoord]

## 📊 [Hoofdtak 2]
- ...

---

## 🔗 Kruisverbanden
- **[Tak A] ↔ [Tak B]** — [waarom in max 8 woorden]
- **[Tak C] ↔ [Tak A]** — [waarom]
```

Elke hoofdtak krijgt een eigen emoji als symbool. Houd sleutelwoorden op één of twee woorden.

---

## 2. Mermaid

Werkt in Notion, GitHub, Obsidian, veel documentatietools. Gebruik het `mindmap`-type, dat rendert radiaal — dichter bij Buzan dan een flowchart.

```
mindmap
  root((CENTRAAL WOORD))
    Hoofdtak 1
      Sleutelwoord
        Sub
        Sub
      Sleutelwoord
    Hoofdtak 2
      Sleutelwoord
```

Let op bij Mermaid mindmap:
- Inspringing bepaalt de hiërarchie. Wees consistent (2 spaties per niveau).
- `root(( ))` geeft de centrale cirkel.
- Geen leestekens zoals `(`, `)`, `:` in labels — dat breekt de parser. Vervang door spaties of streepjes.
- Mermaid mindmap ondersteunt géén kruisverbanden. Zet die er onder als losse lijst, of bied de SVG-versie aan als kruisverbanden belangrijk zijn.

Gebruik `visualize:show_widget` met een Mermaid-render als dat beschikbaar is, anders lever de code in een codeblok zodat de gebruiker hem kan plakken.

---

## 3. Visuele SVG

Dit komt het dichtst bij een handgetekende Buzan-mindmap. Genereer via `visualize:show_widget` (roep eerst `visualize:read_me` aan met module `diagram`). Kan ook als `.svg`-bestand voor printen.

### Opbouwregels

**Canvas.** Breed liggend, bijvoorbeeld `viewBox="0 0 1200 800"`. Centrum op (600, 400).

**Centraal beeld.** Een gevulde ellips of afgeronde rechthoek in het midden, met het woord in groot vet schrift (28-34px). Geef het een eigen kleur die van de takken verschilt — vaak donker of neutraal, zodat de takken eromheen kleuren.

**Hoofdtakken.** Verdeel radiaal over 360°. Bij 6 takken dus elke 60°. Teken ze als **organische curven**, niet als rechte lijnen — dat is essentieel voor het Buzan-effect:

```
<path d="M 600 400 Q 700 340 820 300" stroke="..." stroke-width="8" fill="none" stroke-linecap="round"/>
```

De tak wordt dunner naarmate hij verder van het centrum komt: hoofdtak `stroke-width="8"`, tweede niveau `4`, derde niveau `2`.

**Labels.** Plaats tekst *op* of direct langs de tak, niet in een doosje. Hoofdtak 16-18px vet, subtak 12-13px normaal. Gebruik `text-anchor="start"` voor takken rechts van het centrum en `text-anchor="end"` links, zodat tekst naar buiten leest.

**Kleur.** Elke hoofdtak een eigen kleur uit het palet hieronder. Subtakken erven de kleur van hun hoofdtak — dat is wat de kaart leesbaar houdt.

**Symbolen.** Zet een emoji of eenvoudige SVG-vorm bij elke hoofdtak, vlak bij het label. Beeld onthoudt beter dan tekst.

**Kruisverbanden.** Gestippelde bogen in een neutrale grijstint tussen twee subtakken:

```
<path d="..." stroke="#9ca3af" stroke-width="1.5" stroke-dasharray="4 4" fill="none" opacity="0.7"/>
```

**Ruimte.** Laat de kaart ademen. Overlappende tekst maakt een mindmap onbruikbaar. Bereken labelposities zo dat ze elkaar niet raken; verplaats een tak liever iets dan dat je labels laat botsen.

### Volgorde van tekenen

1. Kruisverbanden (onderop, zodat ze achter de takken vallen)
2. Hoofdtakken en subtakken
3. Alle tekstlabels
4. Centraal beeld als laatste, zodat het bovenop ligt

---

## 4. Kleurenpalet

Zes kleuren die naast elkaar leesbaar blijven en niet schreeuwen:

| Tak | Kleur | Hex |
|---|---|---|
| 1 | Warm rood | `#e2574c` |
| 2 | Oker | `#e8a33d` |
| 3 | Groen | `#4a9d5f` |
| 4 | Blauw | `#3b7dd8` |
| 5 | Paars | `#8b5fbf` |
| 6 | Teal | `#22a3a3` |
| 7 (indien nodig) | Roze | `#d9538f` |

Centrum: `#2d3142` met witte tekst.
Kruisverbanden: `#9ca3af` gestippeld.

Werkt de gebruiker binnen een huisstijl (bijvoorbeeld MERLINQ of een instellingsstijl)? Gebruik die kleuren en houd het contrastniveau vergelijkbaar.

---

## 5. Symbolen

Kies per hoofdtak een symbool dat het thema draagt. Een greep die vaak past in onderwijscontext:

🎯 doel · 📚 inhoud · 👥 mensen · ⚖️ beleid/wet · 💰 geld · ⏱️ tijd · 🔧 uitvoering · 📊 data · ⚠️ risico · 💡 idee · 🔄 proces · 🏛️ instelling · 🎓 student · 🧑‍🏫 docent · 🌐 systeem · 🚧 belemmering

Gebruik ze consequent: hetzelfde symbool betekent door de hele kaart hetzelfde.


---

# Bijlage B - references/onderwijscontext.md

# Onderwijscontext (mbo/hbo/wo)

Gebruik dit als checklist bij het clusteren, niet als voorgeschreven takkenlijst. Doel: voorkomen dat een mindmap in één invalshoek blijft hangen.

- [Perspectieven-check](#perspectieven-check)
- [Actoren](#actoren)
- [Kaders en wetgeving](#kaders-en-wetgeving)
- [Jaarritme](#jaarritme)
- [Terugkerende spanningen](#terugkerende-spanningen)
- [Verschillen mbo / hbo / wo](#verschillen-mbo--hbo--wo)

---

## Perspectieven-check

Loop deze langs. Als drie of meer perspectieven ontbreken, mist de kaart waarschijnlijk breedte.

1. **Lerende** — student, deelnemer, leven lang ontwikkelen
2. **Docent / begeleider** — werkdruk, professionalisering, autonomie
3. **Instelling** — beleid, organisatie, bekostiging, kwaliteitszorg
4. **Systeem** — sector, ministerie, koepels, inspectie
5. **Techniek en data** — systemen, informatievoorziening, AI, privacy
6. **Arbeidsmarkt** — werkveld, stages, aansluiting, tekortsectoren
7. **Maatschappij** — kansengelijkheid, demografie, publieke waarden

## Actoren

**Landelijk:** OCW, Inspectie van het Onderwijs, NRO, SURF, Npuls, DUO, NVAO (accreditatie hbo/wo), SBB (mbo-werkveld), CvTE.

**Koepels:** MBO Raad, Vereniging Hogescholen, Universiteiten van Nederland (UNL), JOB (mbo-studenten), ISO en LSVb (hbo/wo-studenten), AOb en CNV Onderwijs.

**Binnen de instelling:** College van Bestuur, opleidingsmanager, examencommissie, opleidingscommissie, medezeggenschap, studieadviseur, ICT/functioneel beheer, data-analist, privacy officer (FG).

## Kaders en wetgeving

WEB (mbo), WHW (hbo/wo), AVG en de rol van de Functionaris Gegevensbescherming, kwaliteitsafspraken en kwaliteitsagenda's, accreditatiestelsel, examinering en diplomabesluit, EU AI Act (relevant bij AI-toepassingen in onderwijs), toegankelijkheidseisen (WCAG) bij digitale leeromgevingen.

## Jaarritme

Het onderwijsjaar stuurt veel meer dan mensen verwachten. Bij planningsvragen is dit ritme vaak de natuurlijke takkenstructuur:

Instroom en intake (aug/sep) · onderwijsperiodes en blokken · tussentijdse toetsing · herkansingen · stages en praktijkleren · uitval- en switchmomenten (met name na de eerste maanden) · diplomering en uitstroom (juni/juli) · jaarverslag en verantwoording · begrotingscyclus (najaar).

## Terugkerende spanningen

Deze leveren de interessantste takken en kruisverbanden op:

- Maatwerk voor de student ↔ schaalbaarheid voor de organisatie
- Datagedreven werken ↔ privacy en autonomie van de lerende
- Innovatie ↔ werkdruk van docenten
- Standaardisatie ↔ eigenheid van de opleiding
- Meten en verantwoorden ↔ vertrouwen in de professional
- Toegankelijkheid ↔ selectie en rendement
- Landelijke afspraken ↔ instellingsautonomie
- Snelheid van technologie ↔ traagheid van besluitvorming

## Verschillen mbo / hbo / wo

**mbo** — kwalificatiedossiers, beroepspraktijkvorming (BPV), niveau 1-4, entree-opleidingen, sterke werkveldkoppeling via SBB, relatief veel jongere en kwetsbare studenten, regionale functie.

**hbo** — praktijkgericht onderzoek, lectoraten, associate degree / bachelor / master, stage en afstuderen in het werkveld, professionele beroepsprofielen, grote instroomdiversiteit.

**wo** — wetenschappelijk onderzoek als kerntaak, bachelor-master, internationalisering en Engelstaligheid, promotietraject, sterke faculteitsstructuur, andere bekostigings- en publicatieprikkels.

Weet je niet welke sector de gebruiker bedoelt? Maak een kaart die alle drie kan dienen, en bied aan hem toe te spitsen.
