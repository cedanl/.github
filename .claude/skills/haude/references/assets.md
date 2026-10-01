# Echte Npuls-assets in clidev-presentaties

Alle paden zijn **relatief vanaf de projectroot** (waar het deck staat). Spaties in bestandsnamen als `%20` schrijven.

## Fonts — zitten al in de frame

`public/npuls/Npuls_lettertype/`: General Sans Regular + Semibold (`.otf`), Cooper Light BT (`.ttf`). Nooit vervangen door Google Fonts.

## Logo

`public/npuls/npuls_logo.jpg` — 200×200, beeldmerk + woordmerk op een **roze vlak** (≈ `--npuls-roze`). Daarom alleen op `s-roze`-slides (check.mjs dwingt dit af). De frame zet het al op de afsluitslide.

## Illustraties

`public/npuls/powerpoint_illustrations/*.svg` — isometrische Npuls-illustraties, zwarte contour, vlakken in het Npuls-palet. Vierkant (720×720) tenzij anders vermeld.

```html
<img class="illu" src="public/npuls/powerpoint_illustrations/kennisdeling.svg" alt="">
<img class="illu-sm" src="public/npuls/powerpoint_illustrations/Ster%20geel.svg" alt="">
```

| Thema | Bestanden |
|---|---|
| Data, AI, tech | `data` (servers), `Servers`, `chip`, `kunstmatigeintelligentie` (brein + AI-chip), `brains` (brein + tandwiel), `hersenen`, `learninganalystics` (laptop + dashboards), `netwerk` (kubussen), `Connecties` (atoom), `globe`, `vr`, `video` |
| Laptop, scherm | `laptop`, `Laptop met beeld`, `Laptop leeg beeld`, `pc`, `Digitale leermaterialen Npuls` |
| Mensen | `onderwijsprofessional`, `lerende`, `bestuurder` (persoon + munten), `Laptopman`, `figure` (zittend met laptop), `Man`, `Dame blauw pak`, `Dame oranje blauw`, `Dokter`, `Man in rolstoel`, `present` (presentator) |
| Samen, delen | `kennisdeling` (drie mensen + lamp), `gesprek`, `bijeenkomst`, `hands` (handdruk), `Combineren` |
| Onderwijs | `hat` (afstudeerhoed), `books`, `Boeken blauw roze blauw`, `Boeken blauw rozen groen`, `Boeken roze blauw`, `Boek puzzelstuk`, `schoolgebouwen`, `Gebouw blauw met boom`, `Gebouw blauw en roze dak` |
| Idee, inzicht | `Lamp`, `light` (lamp met stralen), `verrekijker`, `locatie` (pin) |
| Proces, planning | `events` (kalender), `Stopwatch`, `Document`, `Pakket compact`, `Blokken stapel`, `Puzzelstuk 2D`, `Puzzelstuk 3D`, `Boom` (groei) |
| Geld, veiligheid | `Financien` (persoon + munten + rekenmachine), `Sleutel`, `Slot` |
| Erkenning | `MC Vaantje`, `Vaantje geel met vink`, `Vaantje oranje`, `cadeau` |
| Vormtaal (vlak, klein) | `Ster geel`, `Ster oranje` (starburst), `Stip geel`, `Pijlen naar elkaar`, `Pijlen rechts grafisch` (chevrons), `Pijlen roze rechts`, `Cirkel grafisch` (ringen), `Golven` |

**Kiezen:** één illustratie per slide, als beeld naast tekst (`split`) of klein in een kaart (`illu-sm`). Niet als achtergrond, niet naast een decoratieve `.deco` op dezelfde plek.

## Wat níét gebruiken

- `public/npuls/powerpoint_slides/*.PNG` — volledige Slidev-achtergronden met vaste contentzones; horen bij `clidev`, botsen met de slide-varianten hier.
- Verzonnen logo's of een nagetekend beeldmerk.
