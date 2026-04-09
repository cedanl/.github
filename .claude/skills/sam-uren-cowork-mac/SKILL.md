---
name: sam-uren-cowork-mac
description: Vraag Gebruiker elke vrijdag welke uren hij heeft gemaakt en voer ze in SAM in
---


## Jouw taak
Vraag de gebruiker welke uren hij deze week heeft gemaakt en voer ze vervolgens in SAM in.

## Stap 1: Vraag Gebruiker naar zijn uren

Start het gesprek met een begroeting en vraag hem voor elke werkdag van deze week (maandag t/m vrijdag):
- Op welk project hij heeft gewerkt
- Hoeveel uur per dag

Bekende projecten van Gebruiker zijn:
- **Npuls F2 - AI & Data Voorzieningen** (projectnummer: 21.1469/001/001, fase: AI&D 2026 - Voorzieningen)
- **Npuls F2 - LT Kennisinfrastructuur** (projectnummer: 21.1455/001/001, fase: LT 2026 Kennisinfrastructuur)

De activiteitscode is altijd: **A2002**.

De gebruiker werkt 8 uur per dag. Vraag ook of hij vrij was of niet heeft gewerkt op bepaalde dagen.

Wacht op zijn antwoord voordat je verdergaat.

## Stap 2: Open SAM in Chrome

Gebruik osascript (AppleScript) om SAM te openen. SAM is bereikbaar via Control Chrome of via osascript.

Navigeer via osascript naar de urenregistratie pagina:

```applescript
tell application "Google Chrome"
  activate
  open location "https://sam.surf.nl"
end tell
```

Wacht 2 seconden en navigeer dan direct naar urenregistratie:

```applescript
tell application "Google Chrome"
  set theTab to tab 1 of window 1
  execute theTab javascript "window.location.href = '/?qvActie=launchmureig';"
end tell
```

**Belangrijk:** Chrome moet "Allow JavaScript from Apple Events" aan hebben staan (View → Developer → Allow JavaScript from Apple Events). Als dit niet werkt, vraag gebruiker dit in te schakelen.

## Stap 3: Lees de huidige weekstaat

Lees de pagina uit om te controleren welke week het is en of er al uren zijn ingevuld:

```applescript
tell application "Google Chrome"
  set theTab to tab 1 of window 1
  set result to execute theTab javascript "document.body.innerText"
  return result
end tell
```

Controleer het jaar/week en de periode. Dit moet de huidige week zijn.

## Stap 4: Voer uren in via de tabelinvoer

Klik op het icoontje voor nieuwe tabelregel (id "NieuweRegel" of zoek naar het element):

```applescript
tell application "Google Chrome"
  set theTab to tab 1 of window 1
  -- Zoek de knop voor nieuwe regel invoer
  execute theTab javascript "
    var html = document.body.innerHTML;
    var idx = html.indexOf('NieuweRegel');
    // of zoek naar de tabel-invoer knop
  "
end tell
```

Voor elke projectregel die gebruiker heeft opgegeven:

1. Klik op de knop voor nieuwe tabelregel (het icoontje met 3 streepjes + plusje)
2. Vul het projectnummer in (bijv. 21.1469/001/001)
3. Selecteer het subproject en de fase
4. Vul activiteitscode A2002 in
5. Vul de uren per dag in
6. Klik op het groene vinkje om te bevestigen

**Alternatief via formulier (als tabel niet werkt):**
Klik op "Nieuw" onder Acties in het rechtermenu om een formulier te openen. Vul van boven naar beneden in: bestemming (project), projectnummer, subproject, fase, activiteitscode, uren per dag.

## Stap 5: Weekstaat gereedmelden

Nadat alle uren zijn ingevoerd, meld de weekstaat gereed:

```applescript
tell application "Google Chrome"
  set theTab to tab 1 of window 1
  -- Submit het formulier met de vrijgevenweek actie
  execute theTab javascript "
    var f = document.forms[0];
    if (f && f.action && f.action.indexOf('vrijgevenweek') !== -1) {
      f.submit();
    } else {
      // Klik op de link 'Weekstaat wel/niet definitief maken'
      document.getElementById('vrijgevenweek').click();
    }
  "
end tell
```

Wacht 2 seconden en verifieer dat de regels de status **Definitief** hebben.

## Stap 6: Bevestig aan Gebruiker

Lees de pagina opnieuw uit en bevestig aan gebruiker welke uren zijn ingevoerd, op welke projecten, en dat de weekstaat definitief is gemeld.

## Foutafhandeling

- **"Er zijn nog weekstaatregels niet gereedgemeld"**: Ga terug naar de betreffende week (Week achteruit bladeren) en meld die lege weekstaat gereed (zonder uren als hij niet heeft gewerkt) via `document.forms[0].submit()` wanneer de form action `vrijgevenweek` bevat.
- **Activiteitscode niet gevonden**: Vraag gebruiker contact op te nemen met de projectleider.
- **Chrome niet reagerend**: Vraag gebruiker Chrome te openen en "Allow JavaScript from Apple Events" in te schakelen.

## Technische context

- SAM hoofdmenu URL: https://sam.surf.nl/
- Urenregistratie directe URL: https://sam.surf.nl/?qvActie=launchmureig
- Chrome JavaScript via AppleScript vereist: View → Developer → Allow JavaScript from Apple Events
- Weekstaat gereedmelden: via form submit met action `qvActie=vrijgevenweek`
- Week achteruit: klik element met id `WekenAchteruit`
- Week vooruit: klik element met id `WekenVooruit`
