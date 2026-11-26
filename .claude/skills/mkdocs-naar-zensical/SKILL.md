---
name: mkdocs-naar-zensical
description: Zet een bestaande MkDocs- of Material for MkDocs-site van een cedanl-repo over op Zensical zonder dat de site anders werkt: eerst controleren, dan bouwen en vergelijken, daarna pas CI en publicatie omzetten. Gebruik bij "migreer naar Zensical", "MkDocs vervangen door Zensical", "overstappen op Zensical". LET OP — nieuwe site of Npuls-huisstijl: `docs-setup`.
allowed-tools: Read Grep Glob Write Edit Bash AskUserQuestion
compatibility: Requires python3, uv and gh CLI
metadata:
  ceda-id: ceda.mkdocs-naar-zensical
  ceda-version: "0.2.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: https://zensical.org/docs/compatibility/mkdocs/migration/
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# MkDocs naar Zensical

Zensical is de opvolger van Material for MkDocs, gemaakt door dezelfde mensen. Het leest dezelfde `mkdocs.yml`, dus de overstap is klein — maar niet nul: plugins die Zensical niet kent worden stil genegeerd, `gh-deploy` bestaat niet en de site moet dus op een andere manier gepubliceerd worden. Deze skill doet de overstap in volgorde van laag naar hoog risico en laat MkDocs als vangnet werken tot het eind.

Bron: de migratiepagina van Zensical. Lees die zelf na als iets hieronder niet meer klopt; Zensical is nog pre-1.0 en verandert snel.

## Workflow

When the user invokes `/mkdocs-naar-zensical [optioneel: pad of repo]`:

### 1. Inventariseer — nog niets wijzigen

```bash
ls mkdocs.yml mkdocs.yaml zensical.toml 2>/dev/null
grep -nE "^(plugins|hooks|theme|extra_css|extra_javascript|markdown_extensions):|custom_dir" mkdocs.yml
grep -rnE "mkdocs|mike" pyproject.toml requirements*.txt .github/workflows 2>/dev/null
gh api repos/<org>/<repo>/pages --jq '{build_type,source}'
```

Leg vast: welke **plugins** (lees de hele `plugins:`-lijst), is er een **`hooks`**-sectie, is er een **`custom_dir`** (sjabloonoverrides), hoe wordt er nu **gepubliceerd** (`build_type: legacy` met `gh-pages` = branch; `workflow` = Actions) en waar staan de MkDocs-dependencies (`pyproject.toml`, requirements, workflow).

### 2. Toets of Zensical dit aankan

Haal de actuele lijst op bij [de ondersteunde plugins](https://zensical.org/docs/compatibility/mkdocs/plugins/) en vergelijk elke plugin uit stap 1. Stop en leg aan de gebruiker voor bij:

| Bevinding | Gevolg |
|---|---|
| `hooks` in `mkdocs.yml` | Niet ondersteund. Zonder alternatief niet migreren. |
| Plugin niet op de lijst | Wordt **stil genegeerd**: de build slaagt, de functie ontbreekt. Besluit per plugin: weglaten, vervangen of wachten. |
| `custom_dir` met eigen sjablonen | Moet tegen Material 9.6.18 of nieuwer kloppen (Zensical gebruikt MiniJinja, geen Jinja). Controleer elk overschreven blok in de build. |
| `docs_dir: .` | Niet ondersteund; verplaats de bronbestanden naar een submap. |
| Versiebeheer met `mike` | Niet getoetst in deze skill; stop en bespreek. |

### 3. Baseline: bouw de site zoals hij nu is

```bash
uv run --with mkdocs-material mkdocs build --strict -d /tmp/docs-mkdocs   # plus de plugins uit stap 1
```

Slaagt de strikte MkDocs-build niet, repareer dat eerst of stop: je kunt anders niet zeggen wat de overstap kapot maakte.

### 4. Bouw dezelfde site met Zensical

Zoek de nieuwste versie op en pin die exact:

```bash
curl -s https://pypi.org/pypi/zensical/json | python3 -I -c "import json,sys;print(json.load(sys.stdin)['info']['version'])"
uv run --with "zensical==<versie>" zensical build --strict --clean
```

De uitvoer staat in `site/` (of `site_dir`). Bij een Material-site met eigen CSS: voeg `variant: classic` toe onder `theme:` in `mkdocs.yml`; dat bewaart het oude Material-uiterlijk, terwijl `modern` de standaard is en kan afwijken. Dit geldt alleen voor een overstap zonder nieuwe vormgeving. Wil de gebruiker de CEDA/Npuls-stijl, laat `variant` dan weg: de stijl van `docs-setup` (en van de eigen site `https://cedanl.github.io/.github/`) is op de modern-variant gebouwd, met Lucide-iconen per pagina via front matter (bijvoorbeeld `icon: lucide/compass`, `icon: lucide/code-xml`) en een subtiele roze markering van de huidige pagina. Pas verder **niets** aan: houd `mkdocs.yml` en zet de configuratie niet om naar `zensical.toml` (niet nodig, en Zensical zelf adviseert daarmee te wachten).

### 5. Vergelijk — dit is de eigenlijke toets

```bash
python3 -I .claude/skills/mkdocs-naar-zensical/scripts/vergelijk-builds.py /tmp/docs-mkdocs site
```

Het script vergelijkt pagina's, interne links, bestanden en de zoekindex. Een **fout** (exit 1) betekent dat er iets verdwenen is: los het op of leg het voor. **Waarschuwingen** (titels) zijn verschillen om te beoordelen, geen blokkade.

Het script ziet geen uiterlijk. Maak daarom schermafbeeldingen van de startpagina en minstens één inhoudspagina uit beide builds (`python3 -m http.server -d <map> <poort>` plus een browser) en leg ze naast elkaar. Verschilt het uiterlijk, controleer dan eerst de keuze voor `variant` (`classic` of de standaard `modern`) en daarna de eigen CSS. Gaat het om de CEDA/Npuls-stijl, vergelijk dan met de live site [https://cedanl.github.io/.github/](https://cedanl.github.io/.github/).

### 6. Zet CI en publicatie om

Zensical heeft geen `gh-deploy`. Publiceren gaat via GitHub Pages met bron `GitHub Actions`.

1. Vervang de workflow door het sjabloon `assets/docs-workflow.yml.tpl` uit de skill `docs-setup` (zelfde repo): strikte Zensical-build op elke pull request, deploy alleen op `main`, rechten per job, versie vastgepind.
2. Vervang in `pyproject.toml` (als die er is) `mkdocs`, `mkdocs-material` en de plugins die Zensical zelf bevat door één regel `zensical`, vastgepind op dezelfde versie; draai daarna `uv lock`.
3. Toon de wijzigingen en wacht op akkoord.

### 7. Zet de Pages-bron om — apart akkoord, vlak voor de merge

Staat Pages op `legacy`, vraag dan expliciet akkoord en zet het om vlak vóór je de PR merget, niet eerder:

```bash
gh api -X PUT repos/<org>/<repo>/pages -f build_type=workflow
```

Start na de merge de workflow (`workflow_dispatch`) als die niet vanzelf draait en controleer dat de site online staat. Verwijder de `gh-pages`-branch **niet** in dezelfde ronde: zolang hij bestaat kun je Pages terugzetten.

### 8. Rond af

Controleer of `site/` in `.gitignore` staat (Zensical maakt daarnaast een `.cache/` die zichzelf negeert) en pas teksten aan die nog MkDocs als gereedschap noemen. Open daarna de PR met `/branch-pr`.

## Let op: een strikte build vangt een stil genegeerde plugin niet

`zensical build --strict` slaagt ook als een plugin niet ondersteund is: de configuratie wordt dan zonder melding genegeerd. Een site met `redirects`, `git-revision-date` of eigen macro's kan dus groen bouwen en toch functies missen. Daarom bestaat stap 2, en daarom is stap 5 de toets en niet stap 4.

## Let op: `gh-deploy` en de omzetting van Pages

Wie `mkdocs gh-deploy` in CI heeft, kan die regel niet vervangen door een Zensical-commando. Het script `zensical build` schrijft alleen naar een map. Wijs de workflow daarom naar de Pages-actions en zet de Pages-bron om (stap 7). Zet je de bron al om vóór de eerste deploy, dan is de site in die tussentijd niet gegarandeerd bereikbaar; houd de periode kort.

## Let op: opties en commando's die niet bestaan

Niet ondersteund in `zensical build`: `--site-dir`, `--theme`, `--use-directory-urls` (gebruik `site_dir`, `theme.variant`, `use_directory_urls` in de configuratie); niet aanwezig: `gh-deploy` en `get-deps` (declareer dependencies in `pyproject.toml`). Een MkDocs-script of Makefile dat die opties gebruikt, breekt dus pas bij de overstap.

## Let op: de overstap blijft terug te draaien

Houd `mkdocs.yml` in plaats van het om te zetten naar `zensical.toml`. MkDocs bouwt de site dan nog steeds, ook met `variant: classic` of zonder `variant` (getest met een strikte MkDocs-build): `git revert` van de PR en een Pages-bron terug naar de branch volstaan. Een omzetting naar `zensical.toml` maakt dat vangnet kapot zonder dat de overstap er iets door wint.

## Let op: Zensical is pre-1.0

Pin de exacte versie in de workflow en in `pyproject.toml`, en verhoog die bewust met een strikte build en de vergelijking uit stap 5 als toets. Wijzigt de versie zonder dat iemand het ziet, dan verandert de site met de volgende release.

## Let op: `include-markdown` werkt anders

Zensical ondersteunt het zonder extra pakket, maar negeert argumenten per invoeging (zoals `rewrite-relative-urls`) en lost links altijd op vanaf de insluitende pagina. Een site met spiegelbestanden die Markdown uit de hoofdmap insluiten kan daardoor andere links krijgen; de vergelijking in stap 5 vangt dat. Zet bronpagina's liever direct in `docs/`.

## Verificatie

`ceda-verifies: measurable` — de overstap is geslaagd als beide commando's exit code `0` geven:

```bash
uv run --with "zensical==<versie>" zensical build --strict --clean
python3 -I .claude/skills/mkdocs-naar-zensical/scripts/vergelijk-builds.py /tmp/docs-mkdocs site
```

Controleer de live site met `curl`: de pagina verwijst naar `stylesheets/extra.css` en `logos/npuls_logo.jpg`, heeft de generator-tag van `zensical`, en `stylesheets/extra.css` bevat `roze-subtiel` (alleen bij de CEDA/Npuls-stijl). Daarnaast heeft een mens de schermafbeeldingen uit stap 5 gezien en bevestigd dat de site online staat na de Pages-omzetting.

## Gebundelde bestanden

- `scripts/vergelijk-builds.py <map-mkdocs> <map-zensical>` — draaien, niet lezen: vergelijkt pagina's, interne links, bestanden en zoekindex van twee builds (stap 5 en Verificatie)

## Important

- Wijzig niets aan de Pages-instelling, de `gh-pages`-branch of de merge zonder expliciet akkoord van de gebruiker; dat zijn instellingen en acties buiten de code.
- Migreer één site per keer en toon de uitkomst van stap 2 en 5 voordat je verdergaat.
- Deze skill zet een bestaande site over zonder de vormgeving te veranderen. Voor een nieuwe site, of om een site in de Npuls-huisstijl te zetten (modern-variant, iconen, roze markering), is er `docs-setup`.
