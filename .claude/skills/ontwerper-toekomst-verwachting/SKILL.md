---
name: future-backcasting
description: "Voer een Future Backcasting-analyse uit voor een CEDA-dataproduct, informatieproduct, dienst of initiatief in het onderwijsdatadomein (mbo/hbo/wo). Backcasting schetst één of meer toekomstscenario's en werkt terug naar het heden om de stappen, blockers, enablers en quick wins te vinden die nodig zijn om een gewenste toekomst te bereiken of een ongewenste te vermijden. Gebruik deze skill altijd wanneer de gebruiker een nieuw dataproduct of informatieproduct verkent, wil weten hoe iets zich richting de toekomst kan ontwikkelen, of vraagt om een backcasting, toekomstverkenning of scenario-analyse. Trigger ook bij zinnen als \"nieuw dataproduct\", \"nieuw informatieproduct\", \"waar gaat dit heen\", \"hoe ziet de toekomst van X eruit\", \"backcasting\", \"toekomstscenario\", \"waar moeten we nu op inzetten\", of wanneer de gebruiker een idee, dienst of initiatief aandraagt en wil weten welke stappen vandaag nodig zijn om daar te komen. Levert inzichten in de chat plus een .md-bestand op."
---

# Future Backcasting

Future Backcasting is een verkenningsmethode: je schetst een hypothetische toekomst en werkt
*terug* naar het heden om te bepalen welke stappen, blockers, enablers en quick wins die toekomst
met vandaag verbinden. Anders dan forecasting (dat het heden extrapoleert) begint backcasting bij
een gewenste of te vermijden eindsituatie en vraagt: wat moet er nú gebeuren om daar te komen —
of dat te voorkomen?

Voor CEDA is dit waardevol bij het verkennen van een **nieuw dataproduct of informatieproduct**:
het maakt strategische keuzes expliciet, legt afhankelijkheden bloot (data-architectuur,
governance, adoptie bij instellingen) en levert concrete acties voor vandaag.

Jouw rol: **je vult de backcasting-analyse zelf in** op basis van de input van de gebruiker en
je kennis van het CEDA-domein. Je begeleidt geen workshop — je lévert de analyse.

---

## Voordat je begint

Zorg dat je deze input hebt. Ontbreekt er iets essentieels, vraag het kort na (max één ronde);
vul de rest zelf plausibel in op basis van CEDA-context en markeer aannames expliciet.

- **Onderwerp** — welk dataproduct, informatieproduct, dienst of initiatief? (bijv. een
  landelijke instroomprognose-tool, een studenttevredenheidsdashboard, een nieuwe open-source pipeline)
- **Doelgroep** — wie gebruikt of raakt het? (data-analisten, IR'ers, BI-specialisten,
  instellingsbestuur, studenten)
- **Tijdshorizon** — welk jaartal is de toekomst? Standaard **5–7 jaar** vooruit als niets genoemd is.
- **Richting** — mikt de gebruiker op een *gewenste* toekomst (nastreven) of een *ongewenste*
  (vermijden)? Zo niet gespecificeerd: verken beide waar zinvol.

Zoek waar mogelijk **1–3 actuele signalen** op (recent nieuws, beleidsontwikkelingen,
technologische verschuivingen) die de toekomstscenario's onderbouwen — denk aan EU AI Act,
vendor lock-in-debat, DUO/SURF/Studielink/Studiewijzer123/OCW-ontwikkelingen, open-source-trends in onderwijsdata. Deze
signalen verankeren de scenario's in de realiteit in plaats van in fantasie.

---

## De vier stappen

Werk deze vier stappen in volgorde uit. Elke stap bouwt op de vorige.

### Stap 1 — Toekomstscenario('s) schetsen

Kies per analyse **1–3 scenario's**. Gebruik de vier scenariotypes om te bepalen wat voor
toekomst je schetst:

- **Possible** — zou ooit kunnen, ook bij grote onzekerheid ("wat als…")
- **Plausible** — geloofwaardig gegeven wat we nu weten
- **Probable** — meest waarschijnlijk als huidige trends doorzetten
- **Preferred** — de gewenste toekomst; waar we naartoe willen sturen

Schrijf elk scenario als een **kort nieuwsartikel uit de toekomst**: een titel + korte
beschrijving (3–6 zinnen), gedateerd op de gekozen tijdshorizon. Dit maakt de toekomst
concreet en bespreekbaar. Koppel elk scenario expliciet aan de signalen uit het heden waar het
uit voortkomt.

### Stap 2 — Het heden beschrijven ("today section")

Beschrijf de vertreksituatie. Kies de vorm die het beste past bij het onderwerp:

- **Persona** — als het draait om een individuele gebruiker (bijv. een IR'er bij een hogeschool
  die met het product werkt)
- **Service description** — als het om een dienst of aanbod gaat (bijv. CEDA's manier van
  informatieproducten ophalen en delen)
- **System scenario** — als het om een systeem, infrastructuur of ecosysteem gaat (bijv. de
  landelijke data-architectuur rond 1CijferHO)

Benoem in het heden alle informatie die de toekomstscenario's raakt: huidige capaciteiten,
databronnen, afhankelijkheden, adoptiegraad, governance-randvoorwaarden.

### Stap 3 — Stappen terug definiëren (heden → toekomst)

Definieer voor elk scenario de **stappen** die het heden met de toekomst verbinden. Werk van de
toekomst terug naar nu. Benoem per stap:

- **Blockers** — wat houdt deze stap tegen? (technisch, organisatorisch, juridisch, cultureel)
- **Enablers** — wat maakt deze stap mogelijk of versnelt hem?

Zo worden de meest kritische punten (veel blockers, weinig enablers) direct zichtbaar.

### Stap 4 — Quick wins identificeren

Benoem de **quick wins**: acties die vandaag haalbaar zijn en je meteen dichter bij de gewenste
toekomst brengen (of verder van de ongewenste). Dit zijn de concrete take-aways die het werk van
nu beïnvloeden. Wees specifiek en toepasbaar — geen vage intenties.

---

## Outputstructuur

Lever twee dingen:

1. **Inzichten in de chat** — een beknopte synthese: de scherpste observaties, de meest kritische
   blockers, en de belangrijkste quick wins. Geen kopie van het hele document; de *inzichten*.
2. **Een .md-bestand** volgens onderstaand sjabloon, gepresenteerd via `present_files`.

Gebruik ALTIJD deze structuur voor het .md-bestand:

```markdown
# Future Backcasting — [Onderwerp]

**Doelgroep:** [...]
**Tijdshorizon:** [jaartal]
**Richting:** [gewenste toekomst nastreven / ongewenste vermijden]

## Signalen uit het heden
- [signaal + bron/link]
- [...]

## Toekomstscenario('s)
### [Scenariotype] — [Titel artikel] ([jaartal])
[Korte beschrijving in artikelvorm]
*Voortkomend uit: [welke signalen]*

## Het heden ([persona / service / system])
[Beschrijving vertreksituatie + relevante info voor de toekomst]

## Stappen: heden → toekomst
### Stap 1 — [naam]
- **Blockers:** [...]
- **Enablers:** [...]
### Stap 2 — [naam]
- **Blockers:** [...]
- **Enablers:** [...]

## Quick wins
- [concrete, haalbare actie voor vandaag]
- [...]

## Aannames
- [expliciet gemarkeerde aannames waar input ontbrak]
```

---

## Toon & principes

Volg de CEDA-schrijfstijl: **praktisch, concreet, toegankelijk**. Geen hoog-over abstracties
zonder voorbeeld. Waar relevant voor onderwijsdata: verbind met CEDA's kernthema's —
co-creatie, openheid (open source), betrouwbare inzichten, digitale autonomie, sectorbreed
denken (mbo/hbo/wo).

- Maak scenario's levendig maar geloofwaardig — verankerd in echte signalen.
- Wees eerlijk over onzekerheid; markeer aannames.
- Quick wins moeten écht uitvoerbaar zijn, niet aspiratief.
- Denk aan CEDA-specifieke afhankelijkheden: data-architectuur bij instellingen, governance,
  adoptie, vendor lock-in, financiering binnen Npuls.