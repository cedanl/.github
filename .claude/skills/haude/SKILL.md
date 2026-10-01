---
name: haude
description: Gebruik wanneer iemand een presentatie als los HTML-bestand wil in Npuls/CEDA-huisstijl in plaats van Slidev — een HTML-deck, html-presentatie, show-deck, kick-off of keynote die moet opvallen, met Mentimeter-peilingen, of één bestand dat je kunt mailen. Ook bij "/haude" of "maak het zoals het LLM-wiki-deck".
---

# haude — HTML-presentaties met Claude

Eén zelfstandig HTML-bestand per presentatie, gebouwd op een vaste **frame** (engine, slide-varianten, componenten) die is afgeleid van het deck *"Welk open-source model kan mijn LLM-wiki het beste onderhouden?"* van Janna Berkhout (KIS). Jij schrijft alleen de slides; de vormgeving komt uit de frame.

**REQUIRED BACKGROUND:** laad `vormgever-npuls-huisstijl` voor kleuren, combinaties, typografie, iconen en vormtaal. Die skill wordt niet aangepast. `haude` voegt alleen het presentatiedeel toe.

**Waar haude bewust afwijkt van vormgever-npuls-huisstijl** (alleen deze drie punten; de rest volgt vormgever):

| vormgever zegt | haude doet | Reden |
|---|---|---|
| Plus Jakarta Sans via Google Fonts als digitale vervanger | Echte General Sans + Cooper Light uit `public/npuls/` | De echte fonts staan in de repo; `bundle.mjs` bakt ze in |
| Font Awesome *solid sharp* | `fa-solid` | Sharp zit alleen in Font Awesome Pro |
| Presentaties → start met `clidev` | HTML-deck → `haude` | `clidev` blijft voor Slidev; dit is de HTML-route |

**Slidev of haude?** Terugkerende reviewdecks met vaste sjablonen → `clidev`. Iets dat moet opvallen, één deelbaar bestand, Mentimeter → `haude`.

## Werkwijze

`<skill>` = de map van deze skill (staat bovenaan als "Base directory").

### 1. Project vinden

Het deck moet in de root van `clidev-presentaties` staan: daar zitten de echte fonts, het logo en de illustraties (`public/npuls/`) en `playwright-chromium`.

```bash
find ~ -type d -name Npuls_lettertype -path "*public/npuls*" 2>/dev/null | sed 's#/public/npuls/Npuls_lettertype##' | head -3
```

Niets gevonden → vraag waar het mag komen en `git clone https://github.com/cedanl/clidev-presentaties.git <pad>`. Daarna `npm install` als `node_modules/` ontbreekt.

### 2. Briefing

Je hebt nodig — vraag wat ontbreekt, in één bericht:

1. **Titel**
2. **Aanleiding** — waarom deze presentatie, 1-2 zinnen
3. **Bronnen** — mappen/bestanden met de inhoud; lees die zelf
4. **Publiek, toon en duur** — bijv. "reviewmeeting DUO, 15 min"
5. **Spreker, team, datum**

Optioneel: Mentimeter-URL, contact (e-mail of teamnaam voor de afsluitslide), gewenst aantal slides. Een gevraagd aantal telt **inhoudsslides**; titel en afsluiting komen erbij. Geen aantal → ~1 inhoudsslide per 2 minuten.

### 3. Frame kopiëren en invullen

```bash
cp <skill>/assets/frame.html YYMMDD_onderwerp.html
```

Naam: `YYMMDD_onderwerp.html` in de projectroot, tenzij de gebruiker een andere naam geeft — die mag ook, zolang het bestand in de projectroot staat.

- Vul de `{{…}}`-placeholders in (titel, brand-label zoals `Npuls · CEDA`, kicker, lede, spreker, afsluitvraag, contact). Geen contact bekend → haal die `<p>` weg, verzin geen adres.
- Zet je slides tussen `<!-- SLIDES:START -->` en `<!-- SLIDES:END -->`, tussen de titelslide en de afsluitslide in. Die twee blijven staan.
- Raak `<style>` en `<script>` niet aan. Mis je echt een component, voeg dan één klein CSS-blok toe onderaan `<style>` met alleen `var(--npuls-*)`-kleuren.

### 4. Slides bouwen

Lees `references/components.md` (snippets per slidetype, varianten, vormtaal) en `references/assets.md` (illustraties, logo).

- Eén boodschap per slide; de `h2` is een bewering met het kernwoord in `<span class="hl">`.
- Varianten afwisselen: licht ↔ wit, één verzadigde slide per kernboodschap.
- Per slide max ~60 woorden zichtbare tekst. Meer → splitsen.
- Gebruik minstens twee echte Npuls-illustraties in het deck.
- Sprekersnotities in een HTML-commentaar boven de `<section>`.

### 5. Controleren — verplicht, in deze volgorde

```bash
node <skill>/scripts/check.mjs YYMMDD_onderwerp.html     # huisstijl, varianten, paden, placeholders
node <skill>/scripts/qa.mjs YYMMDD_onderwerp.html        # screenshots 1920×1080 + 1366×768, overflow, fonts
```

- **FOUT** → oplossen en opnieuw draaien tot beide scripts slagen.
- **WAARSCHUWING** "tekst ligt over decoratie" → verplaats de deco naar een andere hoek of haal hem weg.
- Bekijk daarna **elke** screenshot op 1366×768 (`exports/<naam>/qa/*_1366x768.png`) met Read. Scripts zien geen lelijke witruimte, rare uitlijning of een te volle slide; jij wel.

### 6. Opleveren

```bash
node <skill>/scripts/bundle.mjs YYMMDD_onderwerp.html          # exports/<naam>/<naam>.html — één bestand om te mailen
node <skill>/scripts/qa.mjs YYMMDD_onderwerp.html --pdf        # + exports/<naam>/<naam>.pdf
```

Meld: pad van het deck, de gebundelde versie, de PDF, en de uitkomst van check en qa. Presenteren: open het bestand, `f` = volledig scherm, pijltjes/spatie/clicker = volgende.

## Vaste regels

| Regel | Waarom |
|---|---|
| Altijd starten vanuit `assets/frame.html` | Eigen engine of eigen CSS = elk deck ziet er anders uit |
| Fonts uit `public/npuls/Npuls_lettertype`, nooit Google Fonts | Dat zijn de echte Npuls-fonts; de frame laadt ze al |
| Zwart is nooit een slide- of kaartachtergrond | vormgever-regel; gebruik `s-blauw` voor een donker accent |
| Logo (`npuls_logo.jpg`) alleen op `s-roze` | Het jpg heeft een roze vlak |
| Geen grijze of zelfverzonnen kaartkleuren | Alleen `.card` + Npuls-kleur of licht-variant |
| Geen hex-kleuren in slides, ook niet in SVG | `style="fill:var(--npuls-…)"`; check.mjs faalt op hex |
| Niet "klaar" melden zonder check + qa + screenshots bekeken | Fonts, overflow en botsingen zie je niet in de broncode |

## Veelgemaakte fouten

| Symptoom | Oplossing |
|---|---|
| Koppen in een systeemfont | Deck staat niet in de projectroot, of de `@font-face`-paden zijn aangepast |
| Inhoud loopt onder de navigatiebalk op 1366×768 | Minder tekst, `g4` → `g3`, of splitsen over twee slides |
| Deco door de titel | Andere hoek (`br`/`bl`) of kleinere deco |
| Balken blijven leeg | `--w` vergeten op `.bar-fill` |
| Illustratie laadt niet | Spatie in bestandsnaam niet als `%20` geschreven |
| Font Awesome-icoon ontbreekt | Alleen `fa-solid` (gratis set); geen `fa-sharp` (Pro) |
