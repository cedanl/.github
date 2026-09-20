# CEDA Producttaxonomie

Alle CEDA-repos ingeplugd op de vijf types uit het groeikader. Maintained-producten hebben GDS-maturity; Community-producten hebben geen kwaliteitsborging van CEDA.

**Referentie:** beslissingen en rationale staan in [`ceda-portfolio-groeikader.md`](ceda-portfolio-groeikader.md).

---

## Maintained — CEDA borgt kwaliteit

GDS-maturity: Discovery → Alpha → Beta → Live → Deprecated.

### Library

Importeerbare code met versienummer, gepubliceerd op PyPI of CRAN.

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

**Beslisregel:** heeft het een `pyproject.toml` of `DESCRIPTION` met versienummer én is het gepubliceerd? → Library. Zo niet → Infrastructure (buiten catalogus).

---

### Application

Interactief product voor eindgebruikers, actief onderhouden door CEDA.

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

---

### Developer Tools

Tooling voor CEDA-bouwers; geen eindgebruikers buiten CEDA.

| Subcategorie | Repo | Maturity |
|---|---|---|
| Skills & Agents | .github | Live |
| Skills & Agents | ceda-skills-library | Beta |
| Templates | streamlit-app-template | Live |
| Templates | python-uv-devcontainer | Live |
| Templates | r-devcontainer | Live |
| Templates | r-p3-template | Alpha |
| Tooling | sdp-tools | Beta |
| Tooling | ceda-quickrun | Alpha |
| Tooling | ceda-store | Alpha |
| Tooling | ceda-toolkit | Alpha |
| Tooling | dev-dots | Alpha |
| Tooling | repo-context-as-data | Alpha |
| Tooling | Markov-chain | Alpha |
| Workshops | ceda-workshop-starter | Alpha |
| Testing | uitnodigingsregel-benchmark | Alpha |
| In ontwikkeling | ceda-os | Discovery |

---

## Community — geen kwaliteitsborging door CEDA

Community borgt zelf. Zichtbaar als showcase, niet als product. Geen GDS-verwachting.

### Community Tools

Code en software van of met de community.

| Repo | Status |
|---|---|
| no-fairness-without-awareness | |
| lta-hhs-fairnessawareness | |
| 1cho_ins_visualisation_powerbi | |
| powerbi-vsv | |
| selectie-evaluatietool | ⚠️ mogelijk duplicaat van evaluatietool-selectie — verifiëren |
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

---

### Community Content

Niet-software outputs: research, docs, presentaties, events.

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

## Buiten catalogus — mirrors

Read-only GitHub-syncs van GitLab. Geen eigenstandige producten. Label: `mirror`.

| Repo |
|---|
| gitlab-instroom-etl-ho |
| gitlab-instroom-etl-wo |
| gitlab-instroom-ml |
| gitlab-instroom-viz |
| gitlab-instroom-config |
| gitlab-1cijfer-config |
| gitlab-1cijfer-ho |
| gitlab-streamlit-template-app |
| gitlab-text-analysis |

---

## Maturity × lifecycle per type

**Lifecycle — alle types:**
```
Plan → Design → Build → Test → Release → Maintain → Evaluate
```

- *Release* = publiceren op PyPI/CRAN (Library) · deployen of distribueren (Application) · distribueren (Developer Tools) · publiceren of leveren (Community)
- *Evaluate* = post-release terugblik; sluit de lus terug naar Plan
- Externe bijdragen (Community) hebben sommige fases leeg — dat is informatief, geen probleem

> **Toekomstige extensie:** voor Community Content een variant met expliciete Review- en Feedback-stap vóór Release — nog niet geïmplementeerd.

---

| Type | Maturity | Versioning |
|---|---|---|
| Library | GDS: Discovery → Alpha → Beta → Live → Retired | SemVer |
| Application | GDS: Discovery → Alpha → Beta → Live → Retired | CalVer |
| Developer Tools | GDS: Discovery → Alpha → Beta → Live → Retired | SemVer (package) of adoptie-gebaseerd |
| Community Tools | Draft → Active → Archived | — |
| Community Content | Draft → Active → Archived | — |

---

### Library — details

Gebruikersoppervlak: ontwikkelaars die de library importeren in eigen code; zij pinnen op een versie.

| GDS-fase | SemVer | Wat het zegt |
|---|---|---|
| Discovery | *(geen release)* | Onderzoek of het nodig/haalbaar is |
| Alpha | `0.1.x – 0.3.x` | Eerste versie; API instabiel |
| Beta | `0.4.x – 0.9.x` | API nadert stabiel; gedocumenteerd |
| Live | `1.x.x+` | Stabiele API-belofte; breaking changes alleen bij MAJOR |
| Retired | *(geen nieuwe releases)* | EOL aangekondigd; opvolger aangewezen |

Changelog-taal: `Added · Changed · Fixed · Removed` — API-gericht.

---

### Application — details

Gebruikersoppervlak: eindgebruikers via een UI — web of desktop (zelfde codebase mogelijk).

| GDS-fase | CalVer | Wat het zegt |
|---|---|---|
| Discovery | *(geen release)* | Gebruikersonderzoek; probleemafbakening |
| Alpha | `2024.03.1` | Vroege versie; uitgenodigd publiek |
| Beta | `2024.09.1` | Bredere groep; stabiel genoeg |
| Live | `2025.01.1` | Productie; actief ondersteund |
| Retired | *(offline)* | Niet meer beschikbaar of onderhouden |

CalVer-formaat: `YYYY.0M.MICRO` — geeft ruimte voor hotfix binnen dezelfde maand.
Changelog-taal: datum + feature/fix in proza — geen API-terminologie.

---

### Developer Tools — details

Gebruikersoppervlak: CEDA-developers. GDS-criteria hertaald: "user research" = developer research, geen accessibility-audit.

| GDS-fase | Versioning | Wat het zegt |
|---|---|---|
| Discovery | *(geen release)* | Is er een echte behoefte bij CEDA-teams? |
| Alpha | SemVer `0.x` of geen | Eerste versie; 1–2 teams testen |
| Beta | SemVer `0.x` of geen | Meerdere teams; nadert standaard |
| Live | SemVer `1.x+` of "Standard" | Officiële CEDA-standaard |
| Retired | — | Vervangen; migratieroute aangewezen |

Versioning: SemVer als het een package is (bijv. `ceda-toolkit`); adoptie-label ("Standard") als het een template of skill is.

---

### Community — details

Geen kwaliteitsborging door CEDA. Maturity-stappen beschrijven zowel de status als de lifecycle.

| Fase | Community Tools | Community Content |
|---|---|---|
| Draft | Ingediend, nog niet geverifieerd | In voorbereiding (CEDA-workshop, publicatie) |
| Active | Featured in catalogus; in gebruik | Gepubliceerd of geleverd; beschikbaar |
| Archived | Niet meer relevant of onderhouden | Vervangen, verouderd of eenmalig event |

Voor extern bijgedragen items zijn Plan/Design/Build leeg aan CEDA-kant — Release = opnemen in catalogus, Maintain = relevantie bewaken.

---

## Open vragen

- Worden PowerBI-dashboards actief onderhouden? Zo ja → Application overwegen
- `arbeidsmarkt-mbo` — heeft het een package-interface? Zo ja → Library ✓; zo nee → Infrastructure
- Zijn er plannen voor meer workshop-materiaalrepos? Dan heeft een "Event"-subtype waarde
- `AI-Alignment` en `SamenOntdekken` — is er peer review? Zo ja → Community Content ✓; zo nee → Sandbox
