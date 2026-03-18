# generate_slides_retro

Genereer een Slidev sprint review presentatie voor CEDA op basis van actuele GitHub data.

## Instructies

Wanneer deze skill wordt aangeroepen:

### Stap 0: Clone het clidev project

Voordat je iets doet, zorg dat het clidev-presentaties project beschikbaar is:

1. Zoek of het project al ergens op de machine staat:
   ```bash
   find ~ -type f -name "_template.md" 2>/dev/null | xargs -I{} dirname {} | while read dir; do
     [ -d "$dir/theme" ] && [ -d "$dir/public/npuls" ] && echo "$dir"
   done | head -3
   ```
2. Als het niet gevonden wordt, clone het:
   ```bash
   git clone https://github.com/cedanl/clidev-presentaties.git ~/clidev-presentaties
   ```
3. Installeer dependencies als `node_modules/` ontbreekt:
   ```bash
   cd <project-pad> && npm install
   ```
4. Genereer de presentatie **in deze directory** met het clidev-thema (`theme: ./theme`). Gebruik de naamconventie `YYMMDD_sprint_review.md` (bijv. `260318_sprint_review.md`).

### Stap 1: Data ophalen

**BELANGRIJK: Gebruik ALTIJD de `$GITHUB_TOKEN` environment variable voor authenticatie!**
Zonder token is de rate limit 60 requests/uur — dat is niet genoeg voor alle repo's.
Met token: 5000 requests/uur. Voeg aan ELKE `curl` call toe: `-H "Authorization: token $GITHUB_TOKEN"`.
Als `$GITHUB_TOKEN` niet is ingesteld, waarschuw de gebruiker en stop.

1. **Bepaal de sprint-periode** automatisch:
   - Sprint duurt 2 weken, eindigend op de huidige datum.
   - Bereken `SPRINT_START` (14 dagen geleden) en `SPRINT_END` (vandaag) in ISO 8601 formaat.

2. **Haal de repolijst op en filter op activiteit**:
   - Haal alle repos op: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/orgs/cedanl/repos?per_page=100&type=public"`
   - Werk `config.json` bij met de resultaten.
   - **Pre-filter**: gebruik het `pushed_at` veld uit de repolijst om alleen repo's te selecteren waar `pushed_at >= SPRINT_START`. Dit voorkomt onnodige API-calls.
   - **Neem ALLE actieve repo's mee in de slides**, ook als ze geen gesloten issues of merged PRs hebben. Activiteit = `pushed_at >= SPRINT_START`. Repo's zonder afgerond werk worden alsnog getoond in de velocity-tabel (met 0-waarden) en in relevante overzichten.

3. **Scan ALLE actieve repo's** (die de pre-filter doorstaan):
   - Open issues: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/cedanl/{repo}/issues?state=open&per_page=100"`
   - Gesloten issues in sprint: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/cedanl/{repo}/issues?state=closed&since={SPRINT_START}&per_page=100"`
   - Merged PRs: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/cedanl/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=30"` — filter op `merged_at` binnen sprint-periode.
   - Open PRs: `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/cedanl/{repo}/pulls?state=open&per_page=30"` — gebruik `created_at` om te berekenen hoe lang de PR al openstaat.
   - **Controleer na het ophalen** of de API-response een array is. Als het een dict met `"message"` is, dan is er een fout (rate limit, 404, etc). Log de fout en waarschuw de gebruiker.

4. **Scan oude tickets** (backlog health):
   - De open issues uit stap 3 bevatten het `created_at` veld. Gebruik dit om de exacte leeftijd te berekenen.
   - Filter: `created_at < (vandaag - 1 maand)`.
   - Bereken leeftijd: `(SPRINT_END - created_at)` omrekenen naar maanden (afronden op hele maanden).
   - **Schat NOOIT de leeftijd** — gebruik altijd het `created_at` veld uit de API response.
   - Groepeer per repo: issue nummer, titel, exacte leeftijd in maanden, en assignee. Sorteer van oudste naar nieuwste.

### Stap 2: Bereken metrics

5. **Sprint velocity**:
   - Afgerond deze sprint: aantal gesloten issues + merged PRs.
   - Open werk: aantal open issues + open PRs.
   - Toon als kerncijfers op de titelslide.

6. **Backlog health**:
   - Aantal oude tickets (>1 maand) per repo.
   - Totaal aantal oude tickets over alle repo's.

### Stap 3: Genereer slides

7. **Genereer `YYMMDD_sprint_review.md`** in het clidev project (met `theme: ./theme` in de frontmatter) met deze slides:

   - **Slide 1 — Titel**: "CEDA Sprint Review" + datum + sprint-periode. Layout van boven naar onder:
     1. Titel + subtitel (datum, actieve repos, teamleden)
     2. **Agenda vandaag** (paars blok, volle breedte): genummerde lijst van onderwerpen die besproken worden
     3. **Drie kerncijfers naast elkaar** (volle breedte, `flex` met `gap: 0.8rem`):
        - Groen blok: "Afgerond" + hero-getal + subtekst "X issues + Y merged PRs"
        - Blauw blok: "Open werk" + hero-getal + subtekst "X open issues + Y open PRs"
        - Rood blok: "Aandacht" + hero-getal + subtekst "X tickets ouder dan 1 maand"
     - Elk blok: gekleurde `border-left`, lichte achtergrond, label + ronde badge met getal + 1 regel subtekst. Geen verdere details — die komen later in de presentatie.

   - **Slide 2 — Sprintdoel**: Leid het sprintdoel automatisch af uit de opgehaalde data (belangrijkste gesloten issues en merged PRs). Geef een visueel overzicht: wat is er bereikt deze sprint, samengevat in 1-2 zinnen. Houd het simpel en eerlijk.

   - **Slide 3 — Demo Highlights**: Bepaal automatisch welke repo's iets noemenswaardigs hebben opgeleverd op basis van de merged PRs en gesloten issues. Per repo: korte beschrijving van wat er is opgeleverd. Gebruik relevante Npuls illustraties (bijv. Laptop met beeld.svg, Combineren.svg). Dit is de slide waar stakeholders het meest naar uitkijken.

   - **Slide 4 — Sprint Velocity**: Tabel met per actieve repo: gesloten issues, merged PRs, open issues, open PRs. Daaronder hero-getallen (afgerond vs. open) met een HTML progress bar (groen/rood). **Geen Mermaid** — gebruik pure HTML voor de visualisatie, want Mermaid-blokken werken niet binnen HTML `<div>` containers in Slidev.

   - **Slide 5 — Afgerond deze sprint** (kaarten-layout): Toon per repo een **kaart** in een grid (2-3 kolommen). Elke kaart bevat:
     - Gekleurde balk bovenaan (`border-top: 4px solid {kleur}`), unieke kleur per repo
     - Hero-getal in een ronde badge (aantal afgeronde items)
     - 1-zin samenvatting van wat er is opgeleverd
     - Assignee namen als gekleurde tags onderaan
     - Gebruik `background: rgba(255,255,255,0.85)`, `border-radius: 10px`, `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`
     - Geen bullet lists, geen issue-nummers — alleen het totaalplaatje

   - **Slide 6 — Impact per repo**: 1 slide met een compacte tabel: per actieve repo 1 zin over wat de impact is voor eindgebruikers/instellingen. Baseer dit op de gesloten issues en merged PRs (bijv. "1cijferho: instellingen kunnen nu via pip install de decoder gebruiken"). Als de impact onduidelijk is, schrijf een neutrale samenvatting.

   - **Slide 7 — Volgende stappen**: HTML tabel met 3 kolommen per actieve repo: **Repo**, **Behaald deze sprint** (met groen vinkje `&#10003;` + korte samenvatting), **Mogelijke volgende stap** (concrete vervolgactie afgeleid uit open issues). Geeft in 1 oogopslag per project de richting voor de komende sprint.

   - **Slide 8 — Teamoverzicht**: HTML grid (2-3 kolommen) met kaarten per teamlid. Elke kaart bevat: naam (bold, in repo-kleur), en een lijst van repo's waaraan die persoon heeft gewerkt (op basis van assignees van gesloten issues en merged PRs). Gebruik `border-left: 4px solid {kleur}` per kaart. **Geen Mermaid** — gebruik pure HTML, want Mermaid-blokken werken niet binnen HTML `<div>` containers in Slidev.

   - **Slide — Backlog Health**: Overzicht van alle open issues ouder dan 1 maand. HTML tabel met kolommen: Repo, Issue, Titel, Oud (leeftijd in weken/maanden), Wie (assignee). Header: "Zijn deze nog relevant?" — dit nodigt het team uit om te beslissen: sluiten, opsplitsen, of oppakken. Gebruik de backlog health kleurcodering (zie sectie hieronder).

   - **Slide — Open PRs & Review-tijd**: HTML tabel van alle openstaande PRs over alle actieve repo's. Kolommen: Repo, PR nummer, Titel, Auteur, Open sinds (dagen). Gebruik dezelfde kleurcodering als backlog health: hoe langer open, hoe roder. Drempel: >7 dagen = oranje, >14 dagen = rood, >30 dagen = donkerrood. Header: "Wachten op review" — dit maakt zichtbaar waar PRs vastzitten en reviewers nodig zijn.

   - **Slide — PR Review Roulette** (interactief): Draaiend wiel met teamleden. Techniek:
     - Cirkelvormig wiel via `conic-gradient` met 1 segment per teamlid (360° / N teamleden)
     - Elke naam gepositioneerd via: `position: absolute; top: 50%; left: 50%; transform: rotate({middenhoek}deg) translateY(-95px) rotate(-{middenhoek}deg);` — dit plaatst de naam in het midden van het segment en houdt tekst rechtop
     - Middenhoek per segment = `(index * segmentgrootte) + (segmentgrootte / 2)`
     - **Naam-kleur koppeling**: elke naam krijgt dezelfde kleur als het segment waarop die staat. Gebruik `color: #fff` met `text-shadow: 0 1px 3px rgba(0,0,0,0.5)` voor leesbaarheid op alle segmentkleuren. De segmentkleuren komen uit het repo kleurenpalette (cyclisch toegewezen als er meer teamleden dan kleuren zijn).
     - Pijl (▼) bovenaan het wiel wijst naar de winnaar
     - "Draai!" knop: `onclick` zet `wheel.style.transform = 'rotate(' + (random + 1440) + 'deg)'` met `transition: transform 4s cubic-bezier(0.17, 0.67, 0.12, 0.99)`
     - Na 4.2s timeout: toon winnaar + de langst openstaande PR die diegene moet reviewen
     - Gebruik de repo kleurenpalette voor de segmenten
     - **Confetti & huilende emojis bij resultaat**: na het tonen van de winnaar, lanceer een confetti-explosie en huilende emojis. Techniek:
       - Genereer 60 confetti-deeltjes via een `for`-loop. Elk deeltje is een `<div>` met `position: fixed`, random `left` (0-100%), `top: -20px`, random kleur uit het repo kleurenpalette, `width/height: 8-14px`, `border-radius: 2px` (rechthoekig) of `50%` (rond, random).
       - Animatie via `@keyframes confettiFall`: van `top: -20px; opacity: 1; transform: rotate(0deg)` naar `top: 110vh; opacity: 0; transform: rotate(720deg)`. Duur: `2-4s` (random per deeltje), `ease-out`. Verwijder deeltjes na animatie met `animation: confettiFall {duur}s ease-out forwards`.
       - Genereer 8 huilende emojis (😭) met `position: fixed`, random `left` (10-90%), `top: 30-70%`, `font-size: 2-4rem`, `opacity: 0`. Animatie via `@keyframes emojiPop`: `0%: scale(0) opacity(0)` → `50%: scale(1.3) opacity(1)` → `100%: scale(1) opacity(0)`. Duur: `1.5s`, `delay: 0-0.8s` (gestaffeld).
       - Alle animatie-elementen worden in een container `<div id="confetti-container">` geplaatst die na 5 seconden wordt verwijderd via `setTimeout`.
       - De winnaar-tekst krijgt een extra groot emoji: "😭 {NAAM} 😭" met `font-size: 1.2rem`.

   - **Slide — Two Truths One Lie** (interactief): **Persoonsgebonden** quiz als standalone HTML-pagina, embedded via iframe in de slide. Genereer `public/two-truths.html` in het clidev project.

     **Stap 1: Genereer `public/two-truths.html`** met deze structuur:
     - Standalone HTML-pagina (geen externe dependencies)
     - **Styling**:
       - Body: `font-family: 'Segoe UI', sans-serif; background: #fafafa; color: #333; display: flex; flex-direction: column; align-items: center; padding: 2rem;`
       - Titel: `font-size: 1.6rem; color: #6A1B9A;` + subtitel "Klik op de leugen. Gebaseerd op echte GitHub data uit deze sprint."
       - Scorebalk: `Score: X / Y` met score in `color: #2E7D32; font-weight: bold; font-size: 1.2rem;`
     - **Player tabs** (horizontale rij bovenaan): Per teamlid een tab-knop in een `flex` container:
       - Tab: `padding: 0.5rem 1.2rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold; border: 2px solid #ddd; background: #fff;`
       - `.active`: `background: #6A1B9A; color: #fff; border-color: #6A1B9A;`
       - `.done`: `background: #E8F5E9; color: #2E7D32; border-color: #2E7D32;` (na beantwoording)
       - Klikken op een tab wisselt naar die speler
     - **Statement-kaarten** (gestapeld, verticaal): Per speler 3 stellingen (2 waarheden, 1 leugen). Elke kaart:
       - `background: #fff; border: 2px solid #ddd; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; cursor: pointer; transition: all 0.25s; font-size: 0.95rem;`
       - Hover: `border-color: #6A1B9A; box-shadow: 0 2px 12px rgba(106,27,154,0.1);`
       - Geselecteerd: `border-color: #E53935; background: #FFF3F3;`
       - Na onthulling — waarheid: `border-color: #2E7D32; background: #E8F5E9;` met badge "WAAR"
       - Na onthulling — leugen: `border-color: #E53935; background: #FFEBEE;` met badge "LEUGEN"
       - Badge: `position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); font-weight: bold; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 10px;`
     - **"Onthul!" knop**: `padding: 0.6rem 2rem; border-radius: 25px; background: #6A1B9A; color: #fff;`. Disabled totdat een statement is geselecteerd.
     - **Resultaat**: Na onthulling toon "Goed geraden!" (groen) of "Fout! Dat was geen leugen." (rood)
     - **Auto-advance**: Na 2 seconden automatisch naar volgende onbeantwoorde speler
     - **Data**: `const players = [...]` array met per speler:
       - `name`: voornaam of GitHub username
       - `color`: kleur uit repo kleurenpalette
       - `statements`: array van 3 objecten `{ text: "...", truth: true/false }`
       - Genereer 1 speler per actief teamlid (op basis van assignees van gesloten issues en merged PRs)
       - Baseer waarheden op echte data van die persoon, maak de leugen geloofwaardig maar net verkeerd
       - Schrijf stellingen in eerste persoon: "Ik heb..." (niet "Ahmed heeft...")
     - **Shuffle**: Statement-volgorde wordt random geshuffled per speler bij page load

     **Stap 2: Embed in de slide** via een fullscreen iframe:
     ```html
     <iframe src="/two-truths.html" style="position: absolute; inset: 0; width: 100%; height: 100%; border: none; z-index: 1;" />
     ```

   - **Slide — Hot Takes Poll** (interactief): Genereer 3-5 prikkelende stellingen over de sprint op basis van de opgehaalde data (bijv. "We hadden X eerder moeten mergen", "Repo Y heeft te veel open issues"). Techniek:
     - Elke stelling in een eigen kaart met twee knoppen: `<span style="cursor:pointer; font-size:1.5rem;" onclick="...">👍</span>` en `<span style="cursor:pointer; font-size:1.5rem;" onclick="...">👎</span>`
     - Per stelling een teller-variabele en een **animated bar** die het percentage 👍 vs 👎 toont
     - Bar: twee `<div>`s naast elkaar in een flex container. Linker div (groen, `#43A047`) = % eens, rechter div (rood, `#E53935`) = % oneens. Breedte via `style.width = percentage + '%'` met `transition: width 0.5s ease`
     - Na elke klik: update tellers, herbereken percentages, toon animatie
     - Onder de bar: `<span style="font-size: 0.6rem; color: #666;">{N} stemmen</span>`
     - Kaart-styling: `background: rgba(255,255,255,0.9); border-radius: 10px; padding: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 0.8rem;`
     - Header: "Hot Takes — Eens of oneens?" met subtitel "Klik om te stemmen"

   - **Laatste slide — Afsluiting**: "Vragen?" + teamfoto's + link naar github.com/cedanl.

8. Alle tekst in het **Nederlands**.

## Backlog Health kleurcodering

Hoe ouder een ticket, hoe roder de rij. Elke week een duidelijk ander kleurniveau voor maximaal contrast. Gebruik een HTML `<table>` met inline styles per `<tr>`:

| Leeftijd | Achtergrond | Tekst | Beschrijving |
|----------|-------------|-------|--------------|
| 6+ weken | `#B71C1C` | `#fff` + `font-weight: bold` | Donkerrood — kritiek, direct actie nodig |
| 5 weken | `#D32F2F` | `#fff` | Rood — te lang open |
| 4 weken | `#E65100` | `#fff` | Donkeroranje — aandacht nodig |
| 3 weken | `#F57C00` | `#000` | Oranje — begint op te vallen |
| 2 weken | `#FFA000` | `#000` | Amber — nog acceptabel |
| 1 week | `#FDD835` | `#000` | Geel — net oud, lichte waarschuwing |

Legenda onderaan de slide met gekleurde badges:

```html
<div style="display: flex; gap: 1rem; justify-content: center; font-size: 0.6rem; font-weight: bold;">
  <span><span style="background:#B71C1C; color:#fff; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 6+ wk</span>
  <span><span style="background:#D32F2F; color:#fff; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 5 wk</span>
  <span><span style="background:#E65100; color:#fff; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 4 wk</span>
  <span><span style="background:#F57C00; color:#000; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 3 wk</span>
  <span><span style="background:#FFA000; color:#000; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 2 wk</span>
  <span><span style="background:#FDD835; color:#000; padding: 0.1rem 0.4rem; border-radius: 3px;">&#9632;</span> 1 wk</span>
</div>
```

## Open PRs kleurcodering

Zelfde principe als backlog health: hoe langer open, hoe roder. Gebruik `created_at` van de PR om exacte dagen te berekenen.

| Open sinds | Achtergrond | Tekst |
|------------|-------------|-------|
| >30 dagen | `#B71C1C` | `#fff` + `font-weight: bold` |
| 14-30 dagen | `#E53935` | `#fff` |
| 7-14 dagen | `#FF9800` | `#000` |
| <7 dagen | geen kleur (standaard) | normaal |

Legenda:

```html
<div style="display: flex; gap: 2rem; justify-content: center; font-size: 0.75rem; font-weight: bold;">
  <span><span style="background:#B71C1C; color:#fff; padding: 0.1rem 0.5rem; border-radius: 3px;">&#9632;</span> >30 dagen</span>
  <span><span style="background:#E53935; color:#fff; padding: 0.1rem 0.5rem; border-radius: 3px;">&#9632;</span> 14-30 dagen</span>
  <span><span style="background:#FF9800; color:#000; padding: 0.1rem 0.5rem; border-radius: 3px;">&#9632;</span> 7-14 dagen</span>
</div>
```

## Visuele componenten

### Kaart (voor "Afgerond deze sprint")

```html
<div style="background: rgba(255,255,255,0.85); border-radius: 10px; border-top: 4px solid {KLEUR}; padding: 0.8rem 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <span style="font-weight: bold; font-size: 0.8rem;">{REPO}</span>
    <span style="background: {KLEUR}; color: #fff; border-radius: 50%; width: 2rem; height: 2rem; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem;">{AANTAL}</span>
  </div>
  <p style="font-size: 0.6rem; color: #555; margin: 0.4rem 0 0.2rem;">{SAMENVATTING}</p>
  <span style="font-size: 0.55rem; background: {KLEUR_LICHT}; padding: 0.15rem 0.4rem; border-radius: 10px; color: {KLEUR};">{ASSIGNEES}</span>
</div>
```

### Progress bar (voor "Open werk" panelen)

```html
<div style="background: #E0E0E0; border-radius: 6px; height: 8px; margin-bottom: 0.6rem;">
  <div style="background: linear-gradient(90deg, #2E7D32, #43A047); height: 100%; width: {PERCENTAGE}%; border-radius: 6px;"></div>
</div>
```

### Badge-tellers

```html
<!-- Issues badge (blauw) -->
<span style="background: #1565C0; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.6rem; font-weight: bold;">{N}</span>
<!-- PRs badge (oranje) -->
<span style="background: #E65100; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.6rem; font-weight: bold;">{N}</span>
<!-- Nul badge (grijs) -->
<span style="background: #999; color: #fff; padding: 0.1rem 0.4rem; border-radius: 8px; font-size: 0.6rem;">0</span>
```

### Assignee tag

```html
<span style="font-size: 0.55rem; background: {KLEUR_LICHT}; padding: 0.1rem 0.35rem; border-radius: 8px; color: {KLEUR};">{NAAM}</span>
```

### Repo kleurenpalette

Gebruik per repo een vaste kleur + lichte variant voor tags:

| Repo | Kleur | Licht | Gebruik |
|------|-------|-------|---------|
| Uitnodigingsregel | `#2E7D32` | `#E8F5E9` | Groen |
| 1cijferho | `#1565C0` | `#E3F2FD` | Blauw |
| 1cho ins preparation r | `#E65100` | `#FFF3E0` | Oranje |
| prep1cho | `#6A1B9A` | `#F3E5F5` | Paars |
| studentprognose | `#00838F` | `#E0F7FA` | Teal |
| nfwa | `#AD1457` | `#FCE4EC` | Roze |
| .github | `#6A1B9A` | `#F3E5F5` | Paars |
| Assistentie | `#2E7D32` | `#E8F5E9` | Groen |

## Mermaid mindmap regels

Mermaid mindmap nodes mogen GEEN speciale tekens bevatten. Dit veroorzaakt parse errors in Slidev:
- **Geen** `.` (punt) — gebruik bijv. `github` ipv `.github`
- **Geen** `/` (slash) — gebruik bijv. `Uitval VSV` ipv `Uitval / VSV`
- **Geen** `-` (koppelteken) — gebruik bijv. `instroomprognose mbo` ipv `instroomprognose-mbo`
- **Geen** `_` (underscore) — gebruik bijv. `1cho ins preparation r` ipv `1cho_ins_preparation_r`
- Afkortingen zijn OK: `nfwa` ipv `no-fairness-without-awareness`

## Slide layout patroon

Elke content-slide volgt dit patroon (achtergrond als `<img>`, content in absolute positioned `<div>`):

```html
<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;">
  <img src="/npuls/powerpoint_slides/SlideX.PNG" style="width: 100%; height: 100%; object-fit: cover;" />
</div>

<div style="position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 2rem 4rem; z-index: 1;">
  <!-- content hier -->
</div>
```

Beschikbare achtergronden:
- `Slide1.PNG` — Titelslide (eerste en laatste slide)
- `Slide3.PNG` — Content slides (wit/licht)
- `Slide5.PNG` — Overzicht slides (tabellen, mindmaps)

## Bestanden

- `config.json` — Alle cedanl-repositories (wordt bijgewerkt bij elke run, in de skill-directory)
- `<clidev-pad>/YYMMDD_sprint_review.md` — Slidev-presentatie (output, in het clidev project)
- `<clidev-pad>/theme/` — Npuls huisstijl (CSS, fonts, uit clidev repo)
- `<clidev-pad>/public/` — Afbeeldingen, illustraties, logo's (uit clidev repo)

## Presentatie starten

De server moet in een **aparte terminal** gestart worden (niet vanuit Claude Code, Slidev vereist een interactieve terminal):

```bash
cd <clidev-pad>
npx slidev YYMMDD_sprint_review.md --open
```

De presentatie opent op http://localhost:3030.

## Toekomstige uitbreidingen

- **CEDA Board integratie** (github.com/orgs/cedanl/projects/2): Todo/In Progress/Done/On Hold status per issue via GraphQL API.
- **Sprint-vergelijking**: velocity deze sprint vs. vorige sprint (lijn-grafiek over meerdere sprints).
- **Commit-activiteit**: aantal commits per repo in de sprint-periode.
- **PDF export**: automatisch exporteren via `npx slidev export`.
