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
