# CEDA Portfolio & Groeikader — Beslissingsrecord

## Waarom dit document bestaat

CEDA wil groeien: meer zichtbaarheid naar buiten, hogere kwaliteit van producten en diensten, en AI inzetten in de eigen ontwikkeling. Om AI incrementeel in te zetten op je eigen werk moet je eerst weten wat je hebt, op welk niveau het zit, en waar de gaten zitten. Dit document legt de beslissingen vast die dat mogelijk maken.

Het is geen eindpunt — het is een start zodat het team daarop kan bouwen, schieten en aanpassen.

---

## Wat we gebouwd hebben

### Stap 1 — Antwoord op issue #81

Issue #81 vroeg om de skills-ontologie te splitsen in drie afzonderlijke documenten:

| Document | Wat |
|---|---|
| `skills/ceda-werklandkaart.md` | Het CEDA-werk als coördinatenstelsel: 8 ketenstappen + 4 dwarslagen, skill-onafhankelijk |
| `skills/skills-landkaart.md` | Alle 65 CEDA-skills gemapped op de werklandkaart, met verbindingen en gaten per gebied |
| `skills/skill-bouwmodel.md` | Pointer naar de `skills-ontology` SKILL.md als canonieke bron voor het classificatiemodel |

### Stap 2 — Doorgedacht: wat is er als houvast nodig

De werklandkaart beschrijft *hoe we werken*. Wat ontbrak was een productmodel: *wat bouwen we*, op welk niveau, en wie is verantwoordelijk voor de kwaliteit. Dit leidde tot de producttaxonomie hieronder.

### Stap 3 — Maturity en lifecycle per type uitgewerkt

Per type vastgelegd: welke maturity-standaard, welke versioning-conventie, en één gedeelde lifecycle. Zie [`ceda-producttaxonomie.md`](ceda-producttaxonomie.md) voor de volledige uitwerking en beslissingsrationale.

---

## De taxonomie

### Maintained — CEDA borgt kwaliteit

GDS-maturity: Discovery → Alpha → Beta → Live → Retired.
Lifecycle: Plan → Design → Build → Test → Release → Maintain → Evaluate.
Versioning: SemVer (Library) · CalVer `YYYY.0M.MICRO` (Application) · SemVer of adoptie-label (Developer Tools).

**Library** — importeerbare code met versienummer, gepubliceerd op PyPI of CRAN

| Repo | Maturity |
|---|---|
| eencijfer | Live |
| wisselstroom | Live |
| student-signal | Beta |
| 1cijferho | Beta |
| 1cijfermbo | Beta |
| rio-onderwijsdata | Beta |
| cbs-onderwijsdata | Beta |
| duo-mbo-datafiles | Beta |
| mbo-bekostiging-bestanden | Beta |
| synthetische-onderwijsdata | Beta |
| arbeidsmarkt-mbo | Alpha |

**Application** — interactief product voor eindgebruikers, actief onderhouden door CEDA

| Repo | Maturity |
|---|---|
| Uitnodigingsregel | Beta |
| regiobijeenkomst-tool | Beta |
| onderwijsdata-chat | Alpha |
| samenwijzer | Alpha |
| savvy | Alpha |
| SkillsRadar | Alpha |
| Assistentie | Alpha |
| studentprognose | Alpha |
| dashboard-instroomprognose-mbo | Alpha |

**Developer Tools** — tooling voor CEDA-bouwers, geen eindgebruikers buiten CEDA

| Subcategorie | Repo's | Maturity |
|---|---|---|
| Skills & Agents | .github · ceda-skills-library | Live · Beta |
| Templates | streamlit-app-template · python-uv-devcontainer · r-devcontainer · r-p3-template | Live · Live · Live · Alpha |
| Tooling | sdp-tools · ceda-quickrun · ceda-store · ceda-toolkit · dev-dots · repo-context-as-data · Markov-chain | Beta · Alpha · Alpha · Alpha · Alpha · Alpha · Alpha |
| Workshops | ceda-workshop-starter | Alpha |
| Testing | uitnodigingsregel-benchmark | Alpha |
| In ontwikkeling | ceda-os *(npm package die CEDA AI-dev setup installeert)* | Discovery |

---

### Community — geen kwaliteitsborging door CEDA

Maturity: Draft → Active → Archived.
Lifecycle: zelfde 7 stappen als Maintained; Plan/Design/Build leeg voor extern bijgedragen items.
Geen GDS-verwachting. Community borgt zelf. Zichtbaar als showcase, niet als product.

**Community Tools** — code en software van of met de community

| Repo | Opmerking |
|---|---|
| no-fairness-without-awareness | |
| lta-hhs-fairnessawareness | |
| 1cho_ins_visualisation_powerbi | |
| powerbi-vsv | |
| selectie-evaluatietool | ⚠️ mogelijk duplicaat — verifiëren |
| 1cijferho-evaluatietool | |
| wisselstroom_demo | |
| overzicht-landelijke-databronnen | |
| textanalysis | |
| instroomprognose-mbo | |
| vsv_analysis | |
| studentjourney-mbo | |
| 1cho_ins_preparation_r | |
| prep1cho | |
| docker_1cho | |
| Uitnodigingsregel_datapreparatie | |
| staat-van-onderwijsinstelling | |
| student-instroom-mbo | |
| 1cho_ins_visualisation_tableau | *(archiveer kandidaat — Tableau-tijdperk, vervangen)* |
| 1cho_nl_visualisation_tableau | *(archiveer kandidaat — Tableau-tijdperk, vervangen)* |
| 1cho_nl_preparation_r | *(archiveer kandidaat — oud, 2023)* |
| ed2c-storage | *(archiveer kandidaat — 2023, stilgelegd)* |
| ed2c-python | *(archiveer kandidaat — 2023, stilgelegd)* |
| evaluatietool-selectie | *(archiveer kandidaat — leeg, duplicaat)* |
| demo-instroomprognose | *(archiveer kandidaat — nooit gevuld)* |
| maak_een_hex | *(archiveer kandidaat — eenmalig)* |
| 1cijferho_avans | *(archiveer kandidaat — instelling-specifiek, nooit verder)* |
| onderwijsdata-synthese | *(archiveer kandidaat — overlapt met synthetische-onderwijsdata)* |
| edusynth | *(archiveer kandidaat — generieke SDV-wrapper, superseded)* |

**Community Content** — niet-software outputs: research, docs, presentaties, events

| Repo | Opmerking |
|---|---|
| AI-Alignment | |
| SamenOntdekken | |
| clidev-presentaties | |
| CEDA-verhaal | |
| regiobijeenkomsten | |
| discourse-as-data | |
| ceda-innovatiefunnel | |
| ai-tech-learnings | |
| entire-checkpoints | |
| ceda-algemeen | |
| project_algemeen | |
| communicatie | |
| dair-agentic-coding | *(wordt DAIR workshop)* |
| public_activities | *(archiveer kandidaat — vervangen door clidev-presentaties)* |
| centre_documentation | *(archiveer kandidaat — oude docs-site)* |

---

### Buiten catalogus — mirrors

Read-only GitHub-syncs van GitLab. Geen eigenstandige producten. Label: `mirror`.

`gitlab-instroom-etl-ho` · `gitlab-instroom-etl-wo` · `gitlab-instroom-ml` · `gitlab-instroom-viz` · `gitlab-instroom-config` · `gitlab-1cijfer-config` · `gitlab-1cijfer-ho` · `gitlab-streamlit-template-app` · `gitlab-text-analysis`

---

## Maturity en lifecycle per type

| Type | Maturity | Versioning | Lifecycle |
|---|---|---|---|
| Library | GDS | SemVer (`0.x` → `1.x`) | Plan → Design → Build → Test → Release → Maintain → Evaluate |
| Application | GDS | CalVer (`2024.09.1`) | Plan → Design → Build → Test → Release → Maintain → Evaluate |
| Developer Tools | GDS | SemVer (package) / adoptie-label | Plan → Design → Build → Test → Release → Maintain → Evaluate |
| Community Tools | Draft → Active → Archived | — | Zelfde lifecycle; Plan/Design/Build leeg voor extern |
| Community Content | Draft → Active → Archived | — | Zelfde lifecycle; Plan/Design/Build leeg voor extern |

Zie [`ceda-producttaxonomie.md`](ceda-producttaxonomie.md) voor de volledige per-type uitwerking inclusief SemVer/CalVer-tabellen.

---

## Drie toepassingen

**Extern — portfolio/website**
Per type en maturity zichtbaar maken wat CEDA biedt. Maintained-producten als primaire catalogus, Community als showcase-sectie. Zo weten instellingen direct wat productie-klaar is en wat experimenteel.

**Intern — governance**
Per maturity-niveau bepalen wat verplicht of optioneel is: CI/CD, documentatie, tests, licentie, changelog. Hoe hoger de maturity, hoe strenger de eisen. Developer Tools en Libraries delen dezelfde ladder; Applications hebben aanvullend gebruikerscriteria (toegankelijkheid, onboarding).

**AI-ontwikkeling — gap-analyse**
Skills-landkaart × taxonomie toont waar skills ontbreken, welk type werk ongedekt is, en welke ketenstap de meeste aandacht nodig heeft. Dat verdeel je in het team en pak je stapsgewijs op — niet alles tegelijk.

---

## Wat dit nog niet is

- Maturity-criteria per type zijn globaal uitgeschreven (SemVer/CalVer-tabellen); nog niet als formele gate-checklist (wat is verplicht bij Beta voor Library vs. Application?)
- Archiveer-kandidaten zijn nog niet bevestigd door het team
- De skills-landkaart is nog niet herzien op basis van de taxonomie
- Community-bijdragen hebben nog geen submissie- of zichtbaarheidsproces
- Lifecycle-extensie voor Community Content (Review + Feedback-stap) nog niet geïmplementeerd

---

## Volgende stappen

- Team bevestigt taxonomie en archiveer-kandidaten
- Grid bouwen per type: maturity × lifecycle met skills erin geplot
- Skills-landkaart herzien op basis van de 5 typen
- Pilot: `textanalysis` als eerste bestaand product dat door het kader gaat — toetst taxonomie, maturity-criteria én AI-ontwikkeling tegelijk
- Daarna: website of skills-plot als volgende stap in issue #81
