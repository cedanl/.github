---
name: centrale-inzichten-lll
description: "Genereer centrale inzichten (key insights) voor de leven-lang-lerende en de leven-lang-lerende-begeleider volgens het WIE/WIL/WANT/MAAR-stramien, op basis van empathy map-input (ziet, hoort, gedrag, pijn, verlangen, motivatie). Gebruik deze skill altijd wanneer de gebruiker centrale inzichten, key insights, insight statements of kerninzichten wil voor lerenden, studenten, studentbegeleiders, studieloopbaanbegeleiders of praktijkopleiders in mbo/hbo/wo. Trigger ook bij zinnen als \"maak hier centrale inzichten van\", \"key insights\", \"kerninzichten\", \"wat zijn de inzichten uit deze empathy map\", \"vertaal deze persona naar inzichten\", \"WIE WIL WANT MAAR\", \"insight statement\", of wanneer iemand empathy map-onderdelen (ziet/hoort/denkt/voelt/doet/pijn/verlangen) aanlevert en daar spanningen uit wil destilleren. Werkt ook zonder input: dan gebruik je de ingebouwde persona's. Levert 3-5 inzichten in de chat plus een .md-bestand op, en verwijst door naar de hoe-kunnen-we skill."
---

# Centrale inzichten — leven-lang-lerende (en begeleider)

Een centraal inzicht legt een **spanning** bloot: iemand wil iets, om een reden, maar iets zit in de
weg. Het is geen samenvatting van de empathy map en geen probleemstelling — het is de scherpst
mogelijke formulering van waar behoefte en werkelijkheid botsen.

Jouw rol: **je schrijft de inzichten zelf.** Je begeleidt geen sessie, je levert de set.

Domein: leven lang leren in mbo/hbo/wo en de overgang naar werk. De lerende is niet per se een
18-jarige voltijdstudent — het kan een werkende zijn die zich omschoolt, een mbo'er die doorstroomt,
of iemand die modulair leert. De begeleider is studieloopbaanbegeleider, studentbegeleider, decaan,
praktijkopleider of leercoach.

---

## Stap 0 — Bepaal je input

Drie situaties:

1. **De gebruiker levert empathy map-input aan** (ziet, hoort, gedrag/doet, pijn, verlangen,
   motivatie, denkt, voelt). Gebruik die als primaire bron. Vul aan met de ingebouwde persona's uit
   `references/persona-leven-lang-lerende-begeleider.md` waar dat verrijkt, maar laat de eigen input leidend zijn.
2. **De gebruiker noemt alleen een persona** ("maak inzichten voor de begeleider"). Gebruik
   `references/persona-leven-lang-lerende-begeleider.md`.
3. **Onduidelijk voor wie.** Vraag één keer kort: lerende, begeleider, of beide? Ga daarna door.

Lees `references/persona-leven-lang-lerende-begeleider.md` in situatie 1 en 2 — daar staan de vaste empathy maps voor de
leven-lang-lerende en de begeleider, plus de bronmaterialen.

Ontbreekt de **pijn** of het **verlangen** in aangeleverde input? Vraag dat één ronde na. Zonder
pijn geen MAAR; zonder verlangen geen WANT. Ziet/hoort/gedrag kun je desnoods plausibel invullen en
als aanname markeren.

---

## Het stramien

Elk inzicht bestaat uit vier onderdelen:

- **WIE** — de persoon uit de empathy map. Specifiek, niet "de student" maar de rol met haar
  kenmerkende situatie.
- **WIL** — de activiteit. Wat de persoon feitelijk probeert te doen.
- **WANT** — het doel, de onderliggende reden. Waarom die activiteit ertoe doet.
- **MAAR** — de restrictie, het obstakel. De harde werkelijkheid die ertussen zit.

Notatie in de output:

> **Centrale inzicht 1 — [korte titel]**
> **[WIE]** wil **[WIL]**, **want** [WANT], **maar** [MAAR].

Daaronder per inzicht: 2-3 zinnen onderbouwing met verwijzing naar de empathy map-elementen waar het
op rust (bijv. "rust op: pijn — onzekerheid door gebrek aan actuele informatie; gedrag — valt terug
op intuïtie").

---

## Stap 1 — Ontleed de empathy map

Loop de onderdelen langs en markeer per onderdeel wat een **spanning** bevat, niet wat informatie
is. "Zoekt actief naar trends" is gedrag. "Zoekt actief naar trends maar vindt geen actuele data"
is een spanning.

Let specifiek op deze drie spanningsbronnen:

| Bron | Waar te vinden | Levert |
|---|---|---|
| **Verlangen vs. pijn** | verlangen ↔ pijn | de meest directe inzichten |
| **Gedrag vs. verlangen** | gedrag ↔ verlangen | inzichten over coping en workarounds |
| **Ziet/hoort vs. wil** | omgeving ↔ eigen motivatie | inzichten over systeem en context |

Een goede set inzichten put uit alle drie. Vijf inzichten die allemaal uit "verlangen vs. pijn"
komen, dekken de persona niet.

---

## Stap 2 — Bepaal het niveau van de MAAR

Voor elk inzicht: zit het obstakel in het **proces**, in de **vaardigheid** van de persoon, in het
**systeem** eromheen, of in de **emotie/vertrouwen**? Benoem dit expliciet per inzicht — het bepaalt
wat er later ontworpen kan worden.

Voor dit domein zijn vier obstakelniveaus dominant:

- **Beschikbaarheid** — data bestaat niet, is niet actueel, of is niet ontsloten.
- **Duiding** — data bestaat wel maar is niet te interpreteren of niet te vergelijken met een
  referentie (cohort, opleiding, arbeidsmarkt).
- **Vertrouwen** — privacy, dataveiligheid, angst voor verkeerde interpretatie of misbruik.
- **Regie en deelbaarheid** — de lerende is geen eigenaar; delen met begeleider, werkgever of
  volgende opleiding gaat moeizaam.

Een set van 3-5 inzichten die alle vier niveaus raakt, is sterker dan een set die drie keer op
beschikbaarheid landt.

---

## Stap 3 — Schrijf 3-5 inzichten

Regels:

- **Eén spanning per inzicht.** Twee obstakels in één MAAR = twee inzichten.
- **Geen oplossing in de MAAR.** "maar er is geen dashboard" is een oplossing die ontbreekt, geen
  obstakel. Schrijf: "maar hij kan zijn voortgang niet vergelijken met die van anderen."
- **De WANT gaat over betekenis, niet over de activiteit.** Niet "want hij wil beter plannen"
  (dat is de WIL nog eens), maar "want hij wil weten of hij op koers ligt voordat het te laat is."
- **Concreet en herkenbaar.** Een inzicht dat op elke persona in het onderwijs past, is te vaag.
- **Onderscheidend.** Vijf inzichten die dezelfde spanning anders verwoorden zijn één inzicht.
- **Doorgaans niet meer dan 5.** Bij rijke input mag je clusteren: noem de losse spanningen, kies
  de 5 sterkste, en zet de rest onder "niet uitgewerkt".

**Vraag je bij elk inzicht af:** kun je hier morgen een brainstorm mee starten? Zo nee, is de MAAR
te vaag of te breed.

---

## Stap 4 — Toets de set

Loop deze checklist expliciet af in je antwoord (kort, per inzicht één regel of als tabel):

- [ ] Alle vier onderdelen aanwezig en op de juiste plek (WANT ≠ herhaling van WIL)?
- [ ] Elk inzicht herleidbaar tot concrete empathy map-elementen?
- [ ] Obstakelniveau per inzicht benoemd?
- [ ] Minimaal drie verschillende obstakelniveaus in de set?
- [ ] Geen oplossing verstopt in de MAAR?
- [ ] Inzichten onderling onderscheidend?

Signaleer wat je zelf hebt aangenomen. Aannames markeer je met *(aanname)*.

---

## Stap 5 — Output

**In de chat:**

1. Korte kop: voor wie de inzichten zijn en op welke input ze rusten.
2. De 3-5 inzichten in het stramien, elk met onderbouwing en obstakelniveau.
3. De toetsingstabel uit stap 4.
4. Eventuele aannames en niet-uitgewerkte spanningen.
5. Eén afsluitende regel: bied aan de inzichten door te zetten naar "Hoe kunnen we..."-vragen via
   de **hoe-kunnen-we** skill.

**Als bestand:** schrijf dezelfde inhoud naar
`/mnt/user-data/outputs/centrale-inzichten-[persona]-[datum].md` en presenteer die.

Toon: bondig en direct, actieve vorm, Nederlands. Geen inleidende plichtplegingen.

---

## Valkuilen

| Valkuil | Waarom fout | In plaats daarvan |
|---|---|---|
| "De student wil goede data" | Geen persoon, geen spanning | Benoem wie, welke activiteit, welk obstakel |
| MAAR = ontbrekende tool | Oplossing vermomd als probleem | Beschrijf wat de persoon niet kán, niet wat hij niet héeft |
| WANT herhaalt WIL | Levert geen richting op | Zoek de laag eronder: waarom doet dit ertoe? |
| Alles op beschikbaarheid | Set is eendimensionaal | Dwing spreiding over de vier obstakelniveaus |
| Persona als categorie | "Lerenden vinden privacy belangrijk" | Blijf bij één herkenbaar iemand |
| Inzicht in de vorm van een vraag | Dat is al een HMW | Insight = spanningsbewering; HMW komt daarna |

---

## Referentiebestanden

- `references/persona-leven-lang-lerende-begeleider.md` — vaste empathy maps voor de leven-lang-lerende en de
  leven-lang-lerende-begeleider, plus de brondocumentatie. Lees dit voor je inzichten schrijft,
  tenzij de gebruiker volledige eigen input aanlevert.
- `references/voorbeelden.md` — uitgewerkte voorbeeldsets met goed/fout-vergelijkingen. Lees dit
  wanneer je twijfelt over de scherpte van een formulering.
