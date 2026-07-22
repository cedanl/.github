# Oplevertemplates

Twee vaste scenario's komen steeds terug. Gebruik onderstaande structuur als skelet — vul in, laat weg wat niet van toepassing is, maar begin niet bij een leeg vel telkens opnieuw.

## Scenario A — Nieuw ontwerp vanaf nul

```markdown
## Probleemdiagnose
- Gebruiker & doel: [wie, wat willen ze bereiken]
- Uitvoeringskloof / evaluatiekloof: [welke van de twee, of beide, spelen]
- Excise: [welke stappen dienen alleen de organisatie, niet de gebruiker]

## ISGVO-beslissingen
- Inhoud: [wat moet zichtbaar zijn, wat mag weg]
- Structuur: [flow / navigatie in het kort]
- Gedrag: [belangrijkste micro-interacties, feedback, foutafhandeling]
- Verbeelding: [hiërarchie, kleur, typografie — kort, de code spreekt voor zich]
- Omgeving: [platform, toegankelijkheidseisen, fysieke context]

## Oplevering
[code, of wireframe-beschrijving, of beide]
```

## Scenario B — Bestaande UI verbeteren

Herschrijf niet alles. Maak gerichte verbeteringen die het werkelijke probleem aanpakken.

```markdown
## Wat er niet klopt (en waarom)
- Symptoom: [wat de gebruiker meldt, letterlijk]
- Diagnose: [de onderliggende oorzaak — welke ISGVO-laag, welke UX-wet of Cialdini-principe dit verklaart]

## Gerichte aanpassingen
1. [aanpassing] — lost op: [welk deel van de diagnose]
2. [aanpassing] — lost op: [welk deel van de diagnose]

## Wat je bewust niet aanraakt
[noem expliciet wat buiten scope blijft, zodat duidelijk is dat dit een keuze was]

## Oplevering
[gerichte code-diff of aangepast component — niet het hele scherm herschreven]
```

## Bij twijfel over vorm

- Concrete code gevraagd (component, pagina, flow) → lever werkende code, geen los ontwerp-document.
- Alleen advies of diagnose gevraagd (nog geen build) → gebruik de markdown-structuur hierboven in de chat, geen apart bestand nodig tenzij de gebruiker erom vraagt.
- Screenshot of bestaande code aangeleverd → benoem eerst expliciet wat je waarneemt (welk element, welke flow) vóór je de diagnose geeft — dit voorkomt dat je op aannames ontwerpt.
