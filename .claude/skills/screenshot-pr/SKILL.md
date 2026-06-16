---
name: screenshot-pr
description: Maak een screenshot van de draaiende app en embed het correct in een GitHub PR-beschrijving. Gebruik wanneer iemand een voor/na-screenshot wil toevoegen aan een PR, visuele bewijs wil leveren van een UI-wijziging, of vraagt om de app te fotograferen voor een pull request.
---

# Screenshot PR

Neemt een screenshot van de lokaal draaiende app via Playwright en embed het in de PR-body via een absolute `raw.githubusercontent.com` URL. Relatieve paden werken niet in GitHub PR-beschrijvingen.

## Workflow

When the user invokes `/screenshot-pr`:

### 1. Controleer of de dev server draait

```bash
curl -sf http://localhost:5173 >/dev/null 2>&1 && echo "ok" || echo "niet bereikbaar"
```

Als de server niet bereikbaar is: start hem op via `make dev` of het project-specifieke startcommando en wacht tot de poort reageert:

```bash
make dev > /tmp/dev.log 2>&1 &
timeout 30 bash -c 'until curl -sf http://localhost:5173 >/dev/null 2>&1; do sleep 1; done'
```

### 2. Kies screenshot-tool

Probeer eerst `chromium-cli` (als het beschikbaar is):

```bash
which chromium-cli 2>/dev/null && echo "beschikbaar" || echo "niet beschikbaar"
```

**Als `chromium-cli` beschikbaar is:**

```bash
chromium-cli --session pr-screenshot <<'EOF'
nav http://localhost:5173
wait-for text=<zichtbare tekst op de pagina>
screenshot
EOF
```

Screenshots landen in `chromium_cli/sessions/pr-screenshot/screenshots/`.

**Als `chromium-cli` niet beschikbaar is — gebruik Playwright:**

```bash
cd /tmp && npm init -y > /dev/null 2>&1 && npm install playwright > /dev/null 2>&1
npx playwright install chromium 2>&1 | tail -3
```

Maak vervolgens het screenshot via een inline Node-script:

```bash
cd /tmp && node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://localhost:5173');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  await browser.close();
})();
"
```

### 3. Verplaats screenshot naar de repo

```bash
mv /tmp/screenshot.png <repo-root>/screenshot.png
```

Commit het bestand zodat het via `raw.githubusercontent.com` bereikbaar is:

```bash
git add screenshot.png
git commit -m "Add screenshot for PR"
git push
```

### 4. Bepaal de absolute URL

De raw URL heeft altijd dit formaat:

```
https://raw.githubusercontent.com/<org>/<repo>/<branch>/<pad-naar-bestand>
```

Haal de benodigde onderdelen op:

```bash
git remote get-url origin          # → https://github.com/<org>/<repo>.git
git branch --show-current          # → <branch>
```

Voorbeeld: bestand `screenshot.png` op branch `ui/dark-theme` in repo `cedanl/savvy`:

```
https://raw.githubusercontent.com/cedanl/savvy/ui/dark-theme/screenshot.png
```

### 5. Embed in de PR-body

Gebruik de absolute URL in markdown — nooit een relatief pad:

```markdown
## Voor / Na

| Voor | Na |
|------|----|
| ![Voor](https://raw.githubusercontent.com/<org>/<repo>/<branch>/screenshot-before.png) | ![Na](https://raw.githubusercontent.com/<org>/<repo>/<branch>/screenshot-after.png) |
```

Update een bestaande PR:

```bash
gh pr edit <nummer> --body "$(cat <<'EOF'
...markdown met absolute URLs...
EOF
)"
```

Of maak een nieuwe PR aan met screenshots direct in de body:

```bash
gh pr create --title "..." --body "$(cat <<'EOF'
## Samenvatting
...

## Voor / Na
| Voor | Na |
|------|----|
| ![Voor](<absolute-url-voor>) | ![Na](<absolute-url-na>) |
EOF
)"
```

## Important

- **Relatieve paden werken niet** in GitHub PR-beschrijvingen — gebruik altijd `raw.githubusercontent.com`
- Screenshot-bestanden moeten gecommit en gepusht zijn naar de branch vóór de URL werkt
- `chromium-cli` heeft de voorkeur als het beschikbaar is; Playwright is de fallback
- Bij Playwright: installeer in `/tmp` om de project-repo niet te vervuilen
- `--no-sandbox` is vereist in devcontainer-omgevingen zonder root
- Voor voor/na-vergelijkingen: maak de voor-screenshot vóór je wijzigingen doorvoert
