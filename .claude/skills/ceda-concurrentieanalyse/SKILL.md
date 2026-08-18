---
name: ceda-concurrentieanalyse
description: "Voer een concurrentieanalyse uit voor een CEDA-product, -dienst of -initiatief binnen het onderwijsdatadomein (mbo/hbo/wo). Gebruik deze skill altijd wanneer de gebruiker wil weten hoe een CEDA-aanbod zich verhoudt tot alternatieven, wie de concurrenten zijn, waar een gat in de markt zit, of wat een onderscheidend verkoopargument (USP/niche) kan zijn. Trigger ook bij zinnen als \"concurrentieanalyse\", \"hoe verhoudt dit zich tot X\", \"wie doet dit nog meer\", \"waar zit onze niche\", \"wat maakt ons uniek\", \"vergelijk ons met de markt\", of wanneer de gebruiker concurrenten aanlevert en wil laten vergelijken. Werkt ook voor nieuwe productontwikkeling waarbij een landschapsscan nodig is."
---

# Concurrentieanalyse

Voer een gestructureerde concurrentieanalyse uit voor een CEDA-aanbod. Doel is niet alleen "wie doet wat",
maar het vinden van een **niche of uniek verkoopargument dat concurrenten niet aanbieden** — waar CEDA
onderscheidend is of kan worden.

Deze skill hoort bij de bredere CEDA-context (zie de `ceda`-skill voor missie, merk en positionering).
Lees die eerst als je 'm nog niet in context hebt — de positionering is nodig om de niche te toetsen.

---

## De methode (Waarom / Hoe)

**Waarom:** een niche of USP vinden die concurrenten niet bieden.

**Hoe:** identificeer de belangrijkste concurrenten en breng hun aanbod in kaart. Kijk welke
gebruikersbehoeften onvervuld blijven. Wat CEDA daar wél kan leveren, is de niche.

Deze skill is de kwalitatieve landschapsscan. Een volledige concurrentieanalyse voor nieuwe
productontwikkeling combineert dit vaak met veldonderzoek naar gebruikersbehoeften — noem dat als
vervolgstap wanneer de behoeftekant dun onderbouwd is. (Achtergrond: *Universal Methods of Design*,
Martin & Hannington 2012, h.15; *Observing the User Experience*, Goodman/Kuniavsky/Moed, h.5.)

---

## Workflow

### Stap 1 — Bepaal het analyse-object en de behoeften

Vraag de gebruiker (of leid af uit de conversatie):
- **Wat** wordt geanalyseerd? Een concreet product (bijv. Instroomprognose-tool, Schooluitval-dashboard),
  een dienst, of CEDA als geheel?
- **Voor wie?** De relevante doelgroep (data-analisten, Institutional Researchers, BI-specialisten,
  informatiemanagers bij mbo/hbo/wo).
- **Welke gebruikersbehoeften** staan centraal? Als de gebruiker dit niet weet, stel een korte lijst
  aannames voor en markeer die expliciet als aannames — de niche is alleen zo sterk als de behoeftekant.

Stel maximaal enkele vragen tegelijk. Kom met een voorzet in plaats van een blanco vragenlijst.

### Stap 2 — Identificeer concurrenten (gebruiker + web)

Combineer twee bronnen:
1. **Concurrenten die de gebruiker aanlevert** — neem die altijd mee.
2. **Web-aanvulling** — zoek zelf naar spelers die de gebruiker mist.

Denk breed — concurrentie zit óók buiten het eigen domein. Vier categorieën om af te lopen:

- **Commerciële BI/analytics-leveranciers** — proprietary dashboards en platforms die instellingen kunnen
  kopen (bijv. gevestigde onderwijs-BI-leveranciers, generieke BI-suites).
- **Andere publieke/sector-initiatieven** — DUO, SURF-diensten, andere Npuls-programma's, sectorale
  data-coalities, kennisnet-achtige initiatieven.
- **Instellingen die zelf bouwen** — de "doe-het-zelf"-optie is een reëel alternatief: een instelling die
  intern een dashboard bouwt kiest níét voor CEDA.
- **Niets doen / status quo** — geen tool, handmatig werk, Excel. Vaak de echte concurrent.

Zoek per relevante speler naar: wat ze aanbieden, doelgroep, prijsmodel (gratis/betaald/licentie),
open vs. gesloten, en of het sector-breed of instelling-specifiek is. Zoek gericht; verifieer actuele
feiten via het web in plaats van uit het geheugen.

### Stap 3 — Bouw de vergelijkingsmatrix

Lever een **markdown-tabel inline**. Rijen = concurrenten (met CEDA als eerste rij, ter referentie).
Kolommen = de vergelijkingsassen die er voor deze doelgroep toe doen. Standaardassen (pas aan op de casus):

| As | Wat je vastlegt |
|---|---|
| Aanbod | Wat levert de speler concreet? |
| Doelgroep | Voor wie? mbo/hbo/wo, welke rol? |
| Prijsmodel | Gratis / open source / licentie / betaald |
| Openheid | Open source & documentatie vs. proprietary/black box |
| Reikwijdte | Sector-breed vs. één instelling of type |
| Co-creatie | Samen mét instellingen gebouwd, of kant-en-klaar geleverd? |

De laatste drie assen (openheid, reikwijdte, co-creatie) zijn precies CEDA's positioneringskruispunt —
houd ze erin, want daar wordt de niche vaak zichtbaar.

Voorbeeldvorm:

| Speler | Aanbod | Doelgroep | Prijs | Openheid | Reikwijdte | Co-creatie |
|---|---|---|---|---|---|---|
| **CEDA** | ... | ... | Gratis, open source | Open | Sector-breed | Ja |
| Concurrent A | ... | ... | ... | ... | ... | ... |

Vul cellen kort en concreet in. Waar je iets niet zeker weet, schrijf "onbekend" of "onduidelijk" —
verzin geen feiten.

### Stap 4 — Vind de gaten

Analyseer de matrix expliciet:
- Welke **gebruikersbehoeften** worden door niemand (goed) vervuld?
- Waar clustert de concurrentie, en welke hoek blijft leeg?
- Welke leegte sluit aan bij een échte behoefte uit stap 1 (niet zomaar een lege cel)?

Benoem dit in 2–4 bondige observaties, niet als lange lap tekst.

### Stap 5 — Formuleer de niche / USP (verplicht)

Sluit **altijd** af met een concreet niche- of USP-advies. Toets het aan drie criteria:
1. **Onvervuld** — biedt geen (sterke) concurrent dit al?
2. **Behoefte** — willen gebruikers dit daadwerkelijk?
3. **Leverbaar** — kan CEDA dit waarmaken vanuit z'n positionering (sector-breed, open source,
   community-gedreven, praktisch toepasbaar, legitimiteit via Npuls)?

Geef bij voorkeur één scherp hoofdadvies plus eventueel 1–2 alternatieve hoeken. Wees eerlijk als de
niche wankel is (bijv. behoefte onzeker) en benoem dan welke validatie nog nodig is — meestal
gebruikersonderzoek (zie de methode-sectie).

---

## Toon & vorm

- Nederlands, bondig en direct (conform de CEDA-schrijfrichtlijnen: informeel maar professioneel).
- De matrix inline als markdown-tabel, niet als los bestand — tenzij de gebruiker om een xlsx vraagt.
- Geen marketing-speak. Show, don't tell: onderbouw claims met wat de matrix laat zien.
- Wees transparant over onzekerheid en over wat nog gevalideerd moet worden.

## Checklist voor je afrondt

- [ ] Analyse-object en doelgroep expliciet gemaakt
- [ ] Concurrenten uit alle vier categorieën overwogen (ook "zelf bouwen" en "niets doen")
- [ ] Door gebruiker aangeleverde concurrenten meegenomen én web-aanvulling gedaan
- [ ] Matrix bevat CEDA als referentierij en de drie positioneringsassen
- [ ] Onbekende cellen als "onbekend" gemarkeerd, niets verzonnen
- [ ] Gaten expliciet benoemd en gekoppeld aan echte behoeften
- [ ] Afgesloten met concreet niche/USP-advies, getoetst op onvervuld + behoefte + leverbaar
- [ ] Waar de niche wankelt: validatie-vervolgstap benoemd