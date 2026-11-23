# Lettertypen

Dit pakket bevat geen losse lettertypebestanden. De officiële potx (`pptx/Npuls_powerpoint-template.potx`) heeft General Sans en Cooper Lt BT wel **ingesloten**, zoals Npuls hem aanlevert. Daardoor ziet het template er in PowerPoint goed uit, ook zonder lokale installatie.

Bewuste keuze (Aslam, 2026-11-23): de potx blijft ongewijzigd, inclusief de ingesloten fonts. Let op: Cooper Lt BT is een commercieel font. Gebruik de ingesloten fonts alleen voor Npuls/CEDA-presentaties en haal ze niet uit de potx om los te verspreiden.

| Font | Gebruik | Hoe laden |
|---|---|---|
| General Sans (Regular 400, SemiBold 600) | Primair: koppen en lopende tekst | Web: Fontshare-CDN, `@import url('https://api.fontshare.com/v2/css?f[]=general-sans@400,600&display=swap');` (zit al in `web/npuls.css`). PowerPoint: ingesloten in de potx |
| Plus Jakarta Sans | Digitale vervanger als General Sans niet laadt | Google Fonts, ook al in `web/npuls.css` |
| Cooper Light BT | Alleen introducties, ondertitels en quotes | PowerPoint: ingesloten in de potx. Web: lokaal installeren uit de Npuls-communicatiekit |
