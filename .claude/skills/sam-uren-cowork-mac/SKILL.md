---
name: sam-uren-cowork-mac
description: Voer wekelijks uren in SAM in voor de ingelogde gebruiker. Opent SAM via Control Chrome MCP, leest projecten dynamisch uit de weekstaat, en vraagt login + uren in één bericht.
---

## Jouw taak

Voer de uren van de gebruiker in SAM (urenregistratiesysteem van SURF/Npuls) in voor de huidige week.

## Stap 1: Open SAM én vraag uren tegelijk

Doe dit gelijktijdig — wacht niet op de pagina voordat je de gebruiker aanspreekt:

1. Navigeer via het **Control Chrome MCP** naar de SAM urenregistratiepagina:
   `https://sam.surf.nl/?qvActie=launchmureig`

2. Stuur de gebruiker meteen dit bericht:
   > "Goedemorgen! Ik heb SAM geopend in Chrome — log even in met tiqr als dat nog niet is gebeurd.
   >
   > Geef ondertussen je uren voor deze week door: hoeveel uur per dag en op welk project? Geef ook aan als je een dag niet hebt gewerkt."

3. Wacht op het antwoord van de gebruiker (zowel bevestiging van login als de uren).

## Stap 2: Controleer of SAM is geladen

Lees de paginatekst via Control Chrome. Als er een login- of tiqr-scherm zichtbaar is, wacht dan op bevestiging van de gebruiker en laad de pagina opnieuw. Ga pas verder als de weekstaatpagina zichtbaar is (herkenbaar aan "Eigen Weekstaten" of "Jaar/week" in de tekst).

## Stap 3: Lees de weekstaat en projecten dynamisch uit

Haal de bestaande projectregels op uit de tabel:

```javascript
var rows = document.querySelectorAll('#brwTable tbody tr');
var projecten = [];
rows.forEach(function(row, i) {
  var cellen = row.querySelectorAll('td');
  if (cellen.length > 3) {
    projecten.push({
      rij: i + 1,
      nummer: cellen[2] ? cellen[2].innerText.trim() : '',
      omschrijving: cellen[3] ? cellen[3].innerText.trim() : '',
      fase: cellen[4] ? cellen[4].innerText.trim() : '',
      activiteit: cellen[5] ? cellen[5].innerText.trim() : ''
    });
  }
});
JSON.stringify(projecten);
```

Gebruik deze projectnamen en -nummers als context bij het verwerken van de opgegeven uren. Vraag om verduidelijking als een projectnaam niet overeenkomt met een bestaande rij.

Als er nog geen projectregels bestaan, maak ze aan via "Nieuw" in het Acties-menu (projectnummer, fase, activiteitscode, uren per dag).

## Stap 4: Voer uren in via inline bewerking

Voor elke projectregel (browserRow1, browserRow2, etc.):

**1. Activeer bewerkmode:**
```javascript
document.querySelector('#browserRow1 a.editMode').click()
```

**2. Vul uurvelden in** (h-dag-uur1 = maandag t/m h-dag-uur7 = zondag):
```javascript
document.getElementById('h-dag-uur1').value = '8';  // maandag
document.getElementById('h-dag-uur2').value = '0';  // dinsdag
// etc. — lege dagen leeg laten of '0'
```

**3. Sla op en wacht 2 seconden:**
```javascript
document.querySelector('#browserRow1 a.save').click()
```

Herhaal voor elke rij (browserRow2, browserRow3, etc.).

## Stap 5: Weekstaat definitief melden

```javascript
var links = document.querySelectorAll('a');
links.forEach(function(l) {
  if (l.textContent.indexOf('definitief') !== -1) l.click();
});
```

Wacht 2 seconden en lees de pagina opnieuw. Controleer of de status van alle regels "Definitief" is.

## Stap 6: Bevestig aan de gebruiker

Stuur een overzicht van de ingevoerde uren per project en per dag, en bevestig dat de weekstaat definitief is gemeld.

## Foutafhandeling

- **Login- of tiqr-scherm na bevestiging**: Vraag de gebruiker de pagina te verversen en opnieuw te bevestigen.
- **"Er zijn nog weekstaatregels niet gereedgemeld"**: Ga naar de vorige week via `WekenAchteruit` en meld die weekstaat gereed.
- **Projectregel ontbreekt**: Maak aan via "Nieuw" in het Acties-menu.
- **Activiteitscode niet gevonden**: Vraag de gebruiker contact op te nemen met de projectleider.

## Technische context

- SAM urenregistratie: `https://sam.surf.nl/?qvActie=launchmureig`
- Navigatie: gebruik het **Control Chrome MCP** (niet osascript)
- Bewerkknop per rij: `#browserRowN a.editMode`
- Uurvelden: `h-dag-uur1` (maandag) t/m `h-dag-uur7` (zondag)
- Opslaan per rij: `#browserRowN a.save`
- Weekstaat definitief: link met tekst "definitief" in Acties-sectie
- Week achteruit/vooruit: `WekenAchteruit` / `WekenVooruit`

