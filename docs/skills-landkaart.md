# CEDA Skills Landkaart

Een kaart van alle CEDA-skills, geordend naar de werklandkaart. Twee soorten verbindingen:

- **→ opvolging** — "na skill A kun je door met skill B"; volgt de ketenrichting
- **↔ afbakening** — "gebruik A in plaats van B voor dit doel"; mutual exclusion

De kaart beschrijft de bestaande collectie. Lege gebieden worden benoemd, niet gevuld.

**Referentie:** procesgebieden komen uit [`ceda-werklandkaart.md`](ceda-werklandkaart.md). Het classificatiemodel voor skills staat in [`skill-bouwmodel.md`](skill-bouwmodel.md).

---

## Kernketen

### 1. Verkennen

| Skill | Subproces |
|---|---|
| `ceda-trendanalyse` | Omgevingsscan — DESTEP trends en maatschappelijke opgaven |
| `ceda-concurrentieanalyse` | Concurrentie- en landschapsanalyse |
| `future-backcasting` | Probleemverkenning — toekomstscenario's terugwerken naar nu |
| `brainstorm` | Probleemverkenning — idee van idee naar getoetst besluit |
| `sparren` | Probleemverkenning — gesprekspartner vóór er gebouwd wordt |
| `mindmapping` | Probleemverkenning — thema's in kaart brengen |

**Verbindingen:**
- `ceda-trendanalyse` → `brainstorm` (trends als input voor brainstorm)
- `ceda-concurrentieanalyse` → `sparren` (landschapskennis als basis voor strategie)

**Gaten:** stakeholderanalyse heeft geen skill.

---

### 2. Ontwerpen

| Skill | Subproces |
|---|---|
| `centrale-inzichten-lll` | Empathie & inzicht — leven-lang-lerenden en hun begeleiders |
| `centrale-inzichten-docent` | Empathie & inzicht — docenten en onderwijsondersteuners |
| `hoe-kunnen-we` | Kansformulering — inzichten omzetten naar HMW-vragen |
| `ideeen-ontwikkelen` | Ideation — divergeren en convergeren vanuit een HMW |
| `ontwerper-digitaal-product` | Conceptontwikkeling & visualisatie — UX/UI-ontwerp |
| `grafiekkeuze` | Visualisatie & prototype — juiste grafiektype kiezen |

**Verbindingen:**
- `centrale-inzichten-lll` → `hoe-kunnen-we` (inzichten als input voor HMW)
- `centrale-inzichten-docent` → `hoe-kunnen-we`
- `hoe-kunnen-we` → `ideeen-ontwikkelen`
- `centrale-inzichten-lll` ↔ `centrale-inzichten-docent` (zelfde structuur, andere doelgroep)

**Gaten:** geen skill voor empathie-onderzoek (interviews, observaties).

---

### 3. Data

| Skill | Subproces |
|---|---|
| `surfdrive` | Databronnen ontsluiten — SurfDrive-integratie in pipeline |
| `etl-pipeline` | Databronnen ontsluiten — containerized ingest naar MinIO |
| `voorspellen-dataprep` | Datakwaliteit & voorbereiding |
| `browser-pseudonymize` | Privacy & pseudonimisering — in-browser versleuteling |
| `identifier-mapping` | Privacy & pseudonimisering — BSN/PGN naar UUID |
| `objectstore-onboarding` | Opslag & beheer — SURF Object Store setup |
| `objectstore-experiments` | Opslag & beheer — S3-features testen |

**Verbindingen:**
- `surfdrive` → `etl-pipeline` (SurfDrive als bron in pipeline)
- `voorspellen-dataprep` → `voorspellen-classificatie` / `voorspellen-continu` / `voorspellen-ranking`
- `browser-pseudonymize` ↔ `identifier-mapping` (zelfde doel, andere aanpak: client-side vs. server-side)
- `objectstore-onboarding` → `objectstore-experiments` (setup eerst, dan testen)

**Gaten:** weinig skills voor datagovernance, kwaliteitsmonitoring en datakatalogus.

---

### 4. Analyseren & modelleren

| Skill | Subproces |
|---|---|
| `voorspellen-classificatie` | Voorspellend modelleren — categorische uitkomsten |
| `voorspellen-continu` | Voorspellend modelleren — continue uitkomsten |
| `voorspellen-ranking` | Voorspellend modelleren — risico-ranking, top-N selectie |

**Verbindingen:**
- `voorspellen-dataprep` → `voorspellen-classificatie` / `voorspellen-continu` / `voorspellen-ranking` (data klaar als input)
- `voorspellen-classificatie` ↔ `voorspellen-ranking` (zelfde domein, ander doel: label vs. sortering)
- `voorspellen-continu` ↔ `voorspellen-classificatie` (zelfde domein, categorisch vs. numeriek)

**Gaten:** geen skill voor exploratieve analyse, feature engineering of model-validatie.

---

### 5. Product bouwen

| Skill | Subproces |
|---|---|
| `streamlit` | App-ontwikkeling — CEDA Streamlit-apps |
| `ontwerper-digitaal-product` | App-ontwikkeling — UX/UI-ontwerp (raakt ook Ontwerpen) |
| `grafiekkeuze` | Visualisatie — grafiektype kiezen (raakt ook Ontwerpen) |
| `vormgever-npuls-huisstijl` | Branding — Npuls-stijl op webapps en assets |
| `npuls-huisstijl` | Branding — centrale brand-assets en tokens |
| `clidev` | Presentaties — Slidev CEDA/Npuls-deck |
| `build-marp-deck` | Presentaties — Marp-deck |
| `demo-video` | Documentatie voor gebruikers — geannoteerde demo opnemen |
| `screenshot-pr` | Documentatie voor gebruikers — UI-bewijs in PR-beschrijving |
| `notebooklm` | Presentaties / Documentatie — NotebookLM API |

**Verbindingen:**
- `npuls-huisstijl` → `vormgever-npuls-huisstijl` (bron → toepassing)
- `npuls-huisstijl` → `clidev` (bron → Slidev-thema)
- `clidev` ↔ `build-marp-deck` (zelfde doel, andere tool: Slidev vs. Marp)
- `ontwerper-digitaal-product` → `streamlit` (ontwerp naar implementatie)
- `grafiekkeuze` → `streamlit` (grafiektype als input voor app)

**Gaten:** geen skill voor R Shiny-apps, API-endpoints of mobile/native.

---

### 6. Uitrollen & beheren

| Skill | Subproces |
|---|---|
| `sdp-onboard` | Deployment — nieuw SDP-tenant opzetten |
| `surf-sdp-helm-flux` | Deployment — Helm/Flux workloads op SDP |
| `gitlab-ci` | CI/CD-pipelines — GitLab-pipelines voor config-repos |
| `actions-ci` | CI/CD-pipelines — GitHub Actions workflows |
| `docker` | Deployment & CI/CD — containerbouwen CEDA-style |
| `surf-kubectl-troubleshoot` | Monitoring & troubleshooting — K8s-problemen diagnosticeren |
| `surf-sdp-operations` | Monitoring & troubleshooting — SDP operations |
| `surf-ingress-migration` | Deployment — Kong→Traefik ingressmigratie |
| `surf-tenant-rename` | Deployment — tenant hernoemen over repos |
| `sdp-secrets-management` | Secrets & toegang — SOPS+AGE |
| `sram-oidc` | Secrets & toegang — SRAM-authenticatie toevoegen |
| `dependabot-triage` | Dependency-beheer — CVE-alerts opruimen |
| `gate` | CI/CD-pipelines — SonarCloud/CodeQL quality gate fixen |

**Verbindingen:**
- `sdp-onboard` → `surf-sdp-helm-flux` (tenant eerst, dan deploy)
- `sdp-onboard` → `sdp-secrets-management` (tenant + secrets setup samen)
- `docker` → `surf-sdp-helm-flux` (image als input voor deployment)
- `gitlab-ci` → `surf-sdp-helm-flux` (pipeline triggert deploy)
- `surf-sdp-operations` → `surf-kubectl-troubleshoot` (operations leidt naar troubleshoot bij problemen)
- `surf-ingress-migration` ↔ `sdp-onboard` (niet tegelijk; migratie is geen onboarding)

**Gaten:** geen skill voor observability/monitoring setup, SLO/SLA-definitie.

---

### 7. Overdragen & gebruiken

| Skill | Subproces |
|---|---|
| `release-notes` | Releases publiceren — release notes opstellen |
| `github-release` | Releases publiceren — GitHub Release aanmaken |
| `pypi-project` | Releases publiceren — PyPI-pakket setup en publicatie |
| `mkdocs-setup` | Documentatie genereren — MkDocs-site opzetten |
| `write-issue` | Issues & feedback — GitHub issues aanmaken |
| `screenshot-pr` | Issues & feedback — visueel bewijs bij PR (raakt ook Product bouwen) |

**Verbindingen:**
- `release-notes` → `github-release` (notes als input voor release)
- `mkdocs-setup` → `github-release` (docs klaar vóór publicatie)
- `write-issue` ↔ `branch-pr` (issue → PR, maar aparte skills)
- `write-issue-cowork` ↔ `write-issue` (verouderd; gebruik `write-issue`)

**Gaten:** geen skill voor kennisoverdracht aan eindgebruikers (training, begeleiding), geen user-onboarding flow.

---

### 8. Evalueren & leren

| Skill | Subproces |
|---|---|
| `generate-slides-retro` | Retrospectief op productniveau — sprint review op basis van GitHub-data |
| `generate-slides-retro-simple` | Retrospectief op productniveau — compacte sprint review per domein |

**Verbindingen:**
- `generate-slides-retro` ↔ `generate-slides-retro-simple` (zelfde doel, ander detailniveau)
- `generate-slides-retro-simple` ↔ `sessie-terugblik` (productniveau vs. werkwijze-terugblik)

**Gaten:** geen skill voor productimpact meten, gebruikersonderzoek of A/B-analyse.

---

## Dwarslagen

### Communicatie & community

| Skill | Subproces |
|---|---|
| `clidev` | Presentaties & pitches |
| `build-marp-deck` | Presentaties & pitches |
| `npuls-huisstijl` | Branding |
| `vormgever-npuls-huisstijl` | Branding |
| `grafiekkeuze` | Visualisatie van uitkomsten |
| `demo-video` | Community-engagement / productzichtbaarheid |
| `notebooklm` | Presentaties |

**Gaten:** geen skill voor externe communicatie buiten git (Slack, email outreach, sociale media). Dit is de meest skill-arme dwarslag.

---

### Data-randvoorwaarden

| Skill | Subproces |
|---|---|
| `browser-pseudonymize` | Privacy & gevoelige identifiers |
| `identifier-mapping` | Privacy & gevoelige identifiers |
| `sdp-secrets-management` | Datagovernance — secrets en toegang |
| `objectstore-onboarding` | Datagovernance — opslag-setup |

**Gaten:** geen skill voor ethiek/AI-act compliance, datakwaliteitsbeleid, auditability of data-classificatie.

---

### Platform & tech

| Skill | Subproces |
|---|---|
| `docker` | Infra & SDP — containerbouwen |
| `sdp-onboard` | Infra & SDP — tenant opzetten |
| `surf-sdp-helm-flux` | Infra & SDP — Helm/Flux deployment |
| `surf-sdp-operations` | Infra & SDP — operationeel beheer |
| `surf-kubectl-troubleshoot` | Infra & SDP — troubleshooting |
| `surf-ingress-migration` | Infra & SDP — ingres-migratie |
| `surf-tenant-rename` | Infra & SDP — tenant-hernoemen |
| `objectstore-onboarding` | Infra & SDP — Object Store-inrichting |
| `objectstore-experiments` | Infra & SDP — Object Store-validatie |
| `sdp-secrets-management` | Security-standaarden |
| `sram-oidc` | Security-standaarden |
| `dependabot-triage` | Security-standaarden — dependency-CVE's |
| `gate` | Security-standaarden — quality gates |
| `init-repo` | Tooling & standaarden — nieuwe repo opzetten |
| `migrate-cookiecutter` | Tooling & standaarden — bestaande repo migreren |
| `check-style` | Tooling & standaarden — stijlcontrole |

**Gaten:** geen skill voor GenAI-model-selectie, kosten-/limieten-management bij API-gebruik.

---

### Werkwijze & kennis

| Skill | Categorie |
|---|---|
| `create-skill` | Skill-onderhoud — nieuwe skills schrijven |
| `review-skill` | Skill-onderhoud — skill-PRs beoordelen |
| `dedup-skills` | Skill-onderhoud — duplicaten opruimen |
| `skills-ontology` | Skill-onderhoud — skills classificeren |
| `externe-skill-audit` | Skill-onderhoud — externe skills beoordelen |
| `ship` | Issue/PR-flow — wijziging veilig laten landen |
| `simplify-ceda` | Issue/PR-flow — code reviewen voor kwaliteit |
| `de-hardcode` | Issue/PR-flow — hardcoded waarden wegwerken |
| `branch-pr` | Issue/PR-flow — PR openen en finaliseren |
| `pr-reply` | Issue/PR-flow — reviewcomments beantwoorden |
| `write-issue` | Issue/PR-flow — GitHub issues aanmaken |
| `conventional-commit` | Issue/PR-flow — commit messages |
| `git-workflow` | Issue/PR-flow — git-workflows |
| `r-package-refactor` | Dossierkennis — R-packages verbeteren |
| `sam-uren-cowork-mac` | Dossierkennis — uren invoeren |
| `sparren` | Agent-werkwijze — gesprekspartner voor beslissingen |
| `brainstorm` | Agent-werkwijze — brainstorm structureren |
| `sessie-terugblik` | Reflectie op werkwijze (meta-skill) |

**Meta-skills (werkwijze-leren, los van productevaluatie):**
- `sessie-terugblik` — hoe werkte deze sessie; terugblik op de eigen werkwijze
- `generate-slides-retro` / `generate-slides-retro-simple` — horen in ketenstap 8 (productniveau), niet hier

**Verbindingen:**
- `create-skill` → `review-skill` (schrijven → reviewen)
- `skills-ontology` → `create-skill` (model laden vóór schrijven)
- `externe-skill-audit` → `create-skill` (audit vóór overnemen)
- `dedup-skills` → `review-skill` (opruimen ook via review-cyclus)
- `write-issue` → `branch-pr` → `ship` (issue → PR → landen)
- `simplify-ceda` → `ship` (kwaliteitscontrole vóór landen)
- `write-issue-cowork` ↔ `write-issue` (verouderd; gebruik `write-issue`)

**Gaten:** geen skill voor dossierkennis-opbouw (PKM/MKM), beslissingslogboeken, projectmatige context vastleggen.

---

## Samenvatting dekkingsgraad

| Gebied | Skills aanwezig | Gaten |
|---|---|---|
| Verkennen | 6 | Stakeholderanalyse |
| Ontwerpen | 6 | Empathie-onderzoek (interviews, observaties) |
| Data | 7 | Datagovernance, kwaliteitsmonitoring |
| Analyseren & modelleren | 3 | Exploratieve analyse, feature engineering, modelvalidatie |
| Product bouwen | 10 | R Shiny, API-endpoints |
| Uitrollen & beheren | 13 | Observability setup, SLO-definitie |
| Overdragen & gebruiken | 6 | Eindgebruikersoverdracht, user onboarding |
| Evalueren & leren | 2 | Productimpact meten, gebruikersonderzoek |
| Communicatie & community | 7 | Externe communicatie buiten git |
| Data-randvoorwaarden | 4 | Ethiek/AI-act, datakwaliteitsbeleid |
| Platform & tech | 16 | GenAI-model-selectie |
| Werkwijze & kennis | 19 | Dossierkennis/PKM |
