---
name: build-marp-deck
description: Bouw of bewerk een Marp presentatie (.md → HTML/PDF) in de Npuls huisstijl, met live preview-server en visuele overflow-controle. Gebruik wanneer iemand "maak een marp", "bouw een deck", "marp presentatie", "preview", "preview venster", "live preview", "open de marp" vraagt, of /build-marp-deck aanroept. Bij een Marp-deck open je standaard de live preview-server (niet losse HTML in de browser). Voor Slidev gebruik je clidev; dit is puur Marp.
---

# Build Marp Deck

Maak Marp presentaties in de CEDA/Npuls huisstijl. Marp rendert Markdown → slides via de
`marp` CLI. Deze skill bundelt het `npuls` thema en de werkende slide-patronen, en bakt een
**render → visueel checken → fixen** loop in zodat overflow niet stilletjes blijft staan.

Marp is bewust **niet** Slidev. Wil iemand Slidev? → gebruik `clidev`.

## Live preview (standaard tijdens bewerken)

Zodra je een deck **bouwt of bewerkt**, start meteen de Marp preview-server in plaats van
losse HTML in de browser te openen. De server heeft **live reload**: elke save aan de `.md`
ververst het venster vanzelf — geen handmatige re-render per wijziging.

```bash
marp --preview --server .
```

Start dit **in de achtergrond** (Bash `run_in_background: true`), open daarna het deck direct:

```bash
open "http://localhost:8080/<deck>.md"
```

- `--server .` serveert de map (live reload); `--preview` opent het preview-venster.
- Draait er al een server op 8080? Niet opnieuw starten — alleen de deck-URL openen.
- Triggers: "preview", "preview mode", "preview venster", "live", "open de marp" → start dit,
  niet de statische `deck.html` in de browser.

Stoppen:

```bash
pkill -f "marp --preview"
```

> De statische render (`marp deck.md -o exports/deck.html` + `--pdf -o exports/deck.pdf`)
> levert de **eindproducten** in de `exports/`-submap. Voor het iteratief bouwen/bekijken is
> de HTML preview-server (live reload) of de PDF-watch (stap 3b) sneller.

## Stap 1 — Setup (altijd eerst)

Controleer of de `marp` CLI bestaat:

```bash
which marp || echo "niet aanwezig"
```

Niet aanwezig? Installeer:

```bash
brew install marp-cli
```

Kopieer het thema naar de projectmap als het er nog niet staat (assets zitten in deze skill):

```bash
SKILL_DIR="$HOME/.claude/skills/build-marp-deck/assets"
[ -f npuls.css ]   || cp "$SKILL_DIR/npuls.css" .
[ -f .marprc.yml ] || cp "$SKILL_DIR/.marprc.yml" .
```

`.marprc.yml` (`themeSet: [npuls.css]`) zorgt dat `marp` het thema automatisch laadt — geen
`--theme` vlag nodig zolang je vanuit die map rendert.

## Stap 2 — Schrijf de deck

Begin elke deck met deze frontmatter:

```yaml
---
marp: true
theme: npuls
paginate: true
---
```

- Slides scheiden met `---` op een eigen regel.
- Per-slide variant: `<!-- _class: X -->` bovenaan de slide (underscore = alléén deze slide).
- Gebruik `assets/_template.md` als startpunt — die toont alle slide-classes in actie.

### Slide-classes (uit `npuls.css`)

| Class | Effect |
|-------|--------|
| `title` | Blauwe titelslide, gecentreerd (ondertitel roze) |
| `divider` | Oranje full-bleed sectie-scheider, grote witte tekst |
| `accent` | Groene slide met witte tekst |
| `light-blue` / `light-pink` / `light-green` / `light-orange` / `light-yellow` | Zachte gekleurde achtergrond |
| `dense` | Kleinere tabel/code/quote (0.70em) — bij veel inhoud |
| `dense-table` | Alleen tabel kleiner |
| `dense-code` | Alleen codeblok kleiner |

`class` (zonder underscore) i.p.v. `_class` = geldt vanaf die slide tot je hem weer wijzigt.

### Layout & helpers (rauwe HTML in de Markdown)

```html
<div class="columns">
<div class="col"> … links … </div>
<div class="col"> … rechts … </div>
</div>
```

- `<div class="big-impact">85%</div>` — groot oranje kerngetal.
- `<div class="medium-impact">…</div>` — blauwe subkop, gecentreerd.
- `<div class="highlight-box"><h3>…</h3></div>` — blauw→oranje gradient kader.

### Kleuren (`--npuls-*` vars)

oranje `#DD784B` · blauw `#3D68EC` · groen `#00AF81` · geel `#F4D74B` · roze `#F4D9DC`.
Standaard: H1/H2 oranje, `**strong**` en links blauw, tabel-header blauw met gestreepte rijen,
blockquote oranje linkerrand.

## Stap 3 — Render & visueel controleren

Render de **eindproducten** naar de `exports/`-submap. De `.md` blijft in de hoofdmap; de
`html`- én `pdf`-versies komen in `exports/`:

```bash
mkdir -p exports
marp deck.md -o exports/deck.html
marp deck.md --pdf -o exports/deck.pdf
```

Beide bestanden zijn eindproducten en **blijven staan** in `exports/`. De PDF dient
tegelijk als overflow-check — niet meer weggooien.

Lees de PDF met de **Read tool**, `pages "1-N"` (tot 20 per call), en controleer elke slide op:

- inhoud die aan de onder-/rechterrand wordt **afgekapt** (overflow — Marp waarschuwt hier niet voor);
- tekst die te klein of te groot is;
- lege of onevenwichtige slides.

**Fix overflow** in de `.md` en render opnieuw:
- veel tekst → splits de slide in twee, of `<!-- _class: dense -->`;
- brede tabel → `<!-- _class: dense-table -->`;
- lang codeblok → `<!-- _class: dense-code -->`;
- naast elkaar → `columns`.

Herhaal render → Read → fix tot alle slides schoon zijn.

> `exports/*.html` en `exports/*.pdf` erven automatisch het `npuls`-thema — Marp bakt de CSS
> in elk bestand in. Geen aparte print-CSS nodig: de PDF-lay-out is identiek aan de HTML.

### Stap 3b — PDF live-preview (wijzigingen direct zien)

Wil je overflow live zien terwijl je bewerkt: render de PDF in **watch**-modus en open hem
in een viewer die automatisch herlaadt.

```bash
marp deck.md --pdf -o exports/deck.pdf --watch
```

Start dit **in de achtergrond** (Bash `run_in_background: true`), open daarna de PDF:

```bash
open exports/deck.pdf
```

- `--watch` re-rendert de PDF bij elke save van de `.md`.
- macOS **Preview** herlaadt een gewijzigde PDF meestal vanzelf; **Skim** doet dit het
  betrouwbaarst (zet *Preferences → Sync → Check for file changes* aan).
- De HTML preview-server is sneller voor tekst en flow; de PDF-watch toont de **echte
  paginaranden** en dus de overflow.

Stoppen: `pkill -f "marp.*--watch"`.

## Bestaande deck updaten

Bij het wijzigen van een bestaande deck: **sla stap 1 over** — `npuls.css` en `.marprc.yml`
staan al naast de `.md`. Niet opnieuw kopiëren, niet overschrijven.

1. Edit de `.md` gericht (Edit-tool, niet de hele file herschrijven).
2. Re-render beide eindproducten: `marp deck.md -o exports/deck.html && marp deck.md --pdf -o exports/deck.pdf`.
3. **Check alleen de geraakte slides** op overflow — lees de gewijzigde pagina's uit
   `exports/deck.pdf` met de Read tool, fix waar nodig. De PDF blijft staan (geen opruimen).

Grootste risico bij update: tekst toevoegen aan een bestaande slide duwt inhoud over de rand —
Marp clipt stil. Neem nooit aan dat een geraakte slide nog past; check hem visueel.

## Gotchas

- **Overflow is stil.** Marp clipt zonder error. Altijd visueel checken (stap 3).
- **`columns` vereist rauwe `<div>`-HTML**, geen Markdown-kolommen.
- **`_class` vs `class`**: underscore = deze slide; zonder = vanaf deze slide.
- **PDF/PNG-export vereist Chromium.** Chrome staat op deze Mac. Faalt export? Zet
  `CHROME_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` of geef `--browser chrome`.
- **Lokale fonts** (`General Sans`, `Cooper Light BT`) vallen netjes terug op Plus Jakarta Sans
  als ze ontbreken — geen blocker.
- **Links/e-mails op donkere slides** (`accent`/`divider`/`title`) blijven blauw → laag contrast.
  Schrijf contactgegevens als platte tekst, of vermijd links op gekleurde achtergronden.

## Optioneel — programmatische overflow-check (Playwright/Chrome MCP)

Wil je overflow detecteren zonder vision-tokens: open `deck.html` via een browser-MCP en meet
per `section` of `scrollHeight > clientHeight`. Krachtiger voor grote decks, maar vereist een
geconfigureerde MCP en mikken op Marp's bespoke DOM. De PDF+Read-loop hierboven is de standaard.

## Benodigde permissies (verse machine)

Voeg toe aan `~/.claude/settings.json` → `permissions.allow` voor prompt-vrij renderen:

```json
"Bash(marp:*)",
"Bash(npx marp:*)",
"Bash(which marp)",
"Bash(brew install marp-cli:*)",
"Bash(open:*)",
"Bash(pkill:*)",
"Read(**/*.pdf)"
```

`Bash(marp:*)` dekt ook de preview-server (`marp --preview --server .`); `Bash(open:*)` opent de
deck-URL prompt-vrij; `Bash(pkill:*)` stopt de preview-server.

`Read(**/*.pdf)` laat de PDF in `exports/` zonder prompt lezen. Het aanmaken van `exports/`
en het kopiëren van assets (`mkdir`/`cp`) blijft prompt-on-first-use — bewust niet breed.
