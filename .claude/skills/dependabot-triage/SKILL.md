---
name: dependabot-triage
description: Triage en ruim openstaande dependency-CVE-alerts op in een CEDA-repo (GitHub Dependabot óf GitLab Dependency Scanning). Dedupliceert het opgeblazen aantal alerts naar unieke packages, scheidt directe van transitieve deps, bumpt ze via de lockfile, verifieert de tests, en fixt de config-oorzaak (verkeerde ecosystem) zodat alerts niet blijven oplopen. Gebruik wanneer een repo een stapel open dependency-/CVE-alerts heeft, of wanneer iemand vraagt "waarom staan er zoveel Dependabot-meldingen open". Zusje van gate (die gaat over Sonar/CodeQL quality gates; deze over dependency-alerts).
---

# dependabot-triage

Een groot alert-getal is bijna altijd opgeblazen — veel advisories stapelen op
een paar packages. Dedupliceer eerst, fix op de lockfile, en check *waarom* ze
opliepen voor je klaar zegt. Werkt op zowel **GitHub** (Dependabot) als
**GitLab** (Dependency Scanning) — kies de juiste kolom hieronder.

## Forge & auth

| | GitHub | GitLab |
|---|---|---|
| CLI | `gh` (prefix `unset GITHUB_TOKEN &&` — invalide token kan login shadowen) | `glab` |
| Alerts ophalen | `gh api repos/{owner}/{repo}/dependabot/alerts` | `glab api projects/{id}/vulnerability_findings` of Security Dashboard |
| Config | `.github/dependabot.yml` | `.gitlab-ci.yml` (Dependency Scanning template) + renovate |
| Auto-update PRs | Dependabot | Renovate (CEDA-standaard op GitLab) of GitLab-native |

## Stappen

1. **Inventariseer, gededupliceerd.** Het alert-getal telt advisories, geen
   packages. GitHub:
   ```
   gh api repos/{owner}/{repo}/dependabot/alerts --paginate \
     -q '.[] | select(.state=="open") | (.dependency.package.name|ascii_downcase)
         +"\t"+(.security_vulnerability.first_patched_version.identifier//"none")
         +"\t"+.security_advisory.severity'
   ```
   Klap samen tot **uniek package → hoogste benodigde patch-versie**. "51 alerts"
   is routineus ~7 packages.

2. **Direct vs transitief.** Grep elk package in de manifest
   (`pyproject.toml` / `package.json` / `DESCRIPTION`). Transitieve (de normale
   situatie) staan niet door jou gepind — één lockfile-refresh fixt er meerdere.
   Een package dat alleen build-backend is (bijv. `setuptools`) valt vaak gewoon
   uit de resolutie.

3. **Bump op de lockfile, gericht.** Liever benoemde packages dan een blanket
   upgrade (die verplaatst meer dan de CVEs en verbreedt de review):
   - uv: `uv lock --upgrade-package A --upgrade-package B …`
   - npm: `npm audit fix` of gericht `npm install pkg@ver`
   - poetry: `poetry update A B …`
   - R/renv: `renv::update(c("A","B"))`
   Bevestig daarna dat elke gelockte versie de drempel haalt.

4. **Verifieer dat het werkt (niet overslaan).** `uv sync` + draai de testsuite.
   - Segfault een **native/pyarrow/Polars-test lokaal** (arm64/Rosetta)? Bewijs
     dat het environment is, niet jouw bump: stash de lockfile, re-sync, draai
     dezelfde files op baseline — crashen ze identiek op `main`, dan is het
     bestaand. Zeg dat expliciet; native CI-runners draaien ze prima. Claim nooit
     groen dat je niet gezien hebt.

5. **Fix de oorzaak — de config.** Liepen alerts op ondanks een config, dan klopt
   de **ecosystem** meestal niet voor de toolchain:
   - **uv-project** → GitHub-ecosystem moet **`uv`** zijn, niet `pip`. De
     pip-updater leest `uv.lock` niet, dus alerts vuren maar er landt nooit een
     update-PR. (Verifieer de identifier tegen GitHub's actuele ecosystem-lijst —
     die is veranderd toen native uv-support landde.)
   - GitLab: staat Dependency Scanning überhaupt aan in `.gitlab-ci.yml`, en pakt
     Renovate de lockfile? Zonder dat vuren findings zonder MR's.

6. **Land het.** Lockfile-bump + config-fix op één `fix(deps)`-branch vanaf
   `main`. Stage per bestandsnaam (nooit `git add -A` — bekende ruis hier:
   `install.cmd`, `claudereport.html`, `coverage.xml`). PR/MR-body: gededupliceerde
   tabel (voor→na→drempel), wat transitief is, testbewijs incl. de segfault-caveat,
   en de config-fix als oorzaak. Volg [[branch-pr]] (GitHub) resp. de GitLab-MR-flow.

## Principe
Dedupliceer voor je telt; fix transitieve CVEs op de lockfile; en vraag altijd
waarom ze opliepen — een niet-gefixte verkeerde-ecosystem-config betekent dat je
hier over een maand weer staat. Rapporteer wat je verifieerde vs. wat je niet
kon verifiëren.
