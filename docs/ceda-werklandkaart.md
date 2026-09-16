# CEDA Werklandkaart

Een skill-onafhankelijke kaart van het CEDA-werk: de kernketen met richting en de vier dwarslagen die elke stap raken.

**Gebruik:** deze kaart is het coördinatenstelsel. Skills hangen hieraan — zie [`skills-landkaart.md`](skills-landkaart.md) voor de mapping. Het classificatiemodel voor skills zelf staat in [`skill-bouwmodel.md`](skill-bouwmodel.md).

**Dekkingsgraad** meet je op niveau 2 (subprocessen) en niveau 3 (skill-aanknopingspunten), nooit op niveau 1 (kopjes). Niveau 1 is een oriëntatiepunt, geen meetobject.

---

> **Notitie — procesmodel vs. productmodel**
>
> Deze kaart beschrijft *hoe we werken*, niet *wat we bouwen*. De CEDA-portfolio bevat productcategorieën (Data Platform, AI & ML, Applications, SDKs & Libraries, Developer Platform) die niet één-op-één op deze keten mappen. Twee concrete spanningen:
>
> 1. **"Data" in de keten is twee dingen.** Platform-data (ETL, connectors, objectstore) is permanente infrastructuur — dat is geen projectstap maar een voorwaarde. Project-data (dataprep voor één analyse of model) is wél een ketenstap. De huidige kaart behandelt ze als één.
>
> 2. **SDKs & Libraries ontbreekt.** Packages als `student-signal` en `wisselstroom` zijn herbruikbare domein-libraries, geen apps en geen platform. Ze hebben een eigen ontwikkelcyclus (versionering, publicatie naar PyPI). Die productvorm heeft geen plek in de huidige keten.
>
> Dit aanpassen ligt buiten de scope van het huidige issue. De notitie staat hier zodat een volgende iteratie weet waar de grens zit.

---

## Kernketen

De keten heeft richting: van verkennen naar leren. Iteraties zijn mogelijk; de richting van de keten geeft aan waar je normaal gesproken begint en eindigt.

### 1. Verkennen

Begrijpen wat er speelt voordat er een richting wordt gekozen.

- **Probleemverkenning** — wat is het vraagstuk, wie heeft het, hoe urgent is het
- **Omgevingsscan** — trends, beleid, regelgeving, maatschappelijke opgaven
- **Concurrentie- en landschapsanalyse** — wie doet dit nog meer, waar zit het gat
- **Stakeholderanalyse** — wie zijn betrokken partijen, welke belangen spelen

### 2. Ontwerpen

Van vraagstuk naar richting: inzichten ophalen, kansen formuleren, ideeën ontwikkelen.

- **Empathie & inzicht** — doelgroep begrijpen, centrale inzichten formuleren
- **Kansformulering** — van inzicht naar ontwerpvraag (HMW)
- **Ideation** — ideeën genereren, clusteren, prioriteren
- **Conceptontwikkeling** — ideeën uitwerken tot toetsbare richtingen
- **Visualisatie & prototype** — schermen, flows, dashboards schetsmatig ontwerpen

### 3. Data

Data verzamelen, ontsluiten en klaarmaken voor gebruik.

- **Databronnen ontsluiten** — koppelingen met bronnen (SurfDrive, APIs, databases)
- **Datakwaliteit & voorbereiding** — opschonen, valideren, gereed maken voor analyse
- **Privacy & pseudonimisering** — gevoelige identifiers beschermen vóór verwerking
- **Opslag & beheer** — data landen in de juiste store (MinIO, objectstore, database)

### 4. Analyseren & modelleren

Van data naar inzicht of voorspelling.

- **Exploratieve analyse** — patronen vinden, distributies begrijpen, hypothesen toetsen
- **Voorspellend modelleren** — classificatie, regressie, risico-ranking
- **Validatie & evaluatie van modellen** — hoe goed presteert het model, op welke populatie

### 5. Product bouwen

Van analyse of ontwerp naar een werkend, bruikbaar product.

- **App-ontwikkeling** — Streamlit-apps, dashboards, REST-services
- **Visualisatie** — grafieken, kaarten, interactieve rapporten
- **Branding & huisstijl** — Npuls-uitstraling toepassen op outputs
- **Presentaties** — slides voor interne en externe doeleinden
- **Documentatie voor gebruikers** — handleidingen, onboarding, uitleg bij een product

### 6. Uitrollen & beheren

Een product of dienst stabiel beschikbaar maken en houden.

- **Deployment** — containers bouwen, SDP-tenant aanvragen, Helm/Flux configureren
- **CI/CD-pipelines** — geautomatiseerde test-, bouw- en deploystappen
- **Monitoring & troubleshooting** — problemen signaleren en oplossen in productie
- **Secrets & toegang** — SOPS-encrypted secrets, SRAM-authenticatie, least-privilege
- **Dependency-beheer** — CVE-alerts triageren, pakketten bijhouden

### 7. Overdragen & gebruiken

Het product en de kennis eromheen bereiken de eindgebruiker.

- **Releases publiceren** — versietags, release notes, PyPI, GitHub Releases
- **Documentatie genereren** — MkDocs, API-docs, architectuuroverzichten
- **Issues & feedback** — gebruikersproblemen en wensen bijhouden
- **Kennisoverdracht** — training, presentaties, begeleiding van eindgebruikers

### 8. Evalueren & leren

Of het product iemand helpt — los van hoe ons werkproces loopt.

- **Productimpact meten** — helpt dit de lerende, de docent, de instelling
- **Gebruikersonderzoek** — feedback ophalen, gebruikssessies analyseren
- **Retrospectief op productniveau** — wat werkte, wat niet, wat doen we anders

---

## Dwarslagen

Dwarslagen raken elke stap in de kernketen. Ze zijn geen fasering; ze zijn permanent van kracht.

### Communicatie & community

Alles wat gaat over zichtbaarheid, samenwerking en het delen van kennis — intern en extern.

- **Presentaties & pitches** — voor stakeholders, conferenties, teamoverleggen
- **Visualisatie van uitkomsten** — grafieken en dashboards als communicatiemiddel
- **Branding** — herkenbare uitstraling van producten en outputs
- **Community-engagement** — bijdragen aan de bredere onderwijsdatagemeen-schap

### Data-randvoorwaarden

De kaders waarbinnen data-werk verantwoord plaatsvindt.

- **Datakwaliteit & volwassenheid** — structureel geborgd, niet ad hoc
- **Privacy & gevoelige identifiers** — AVG-compliant verwerken van BSN, PGN, onderwijsnummer
- **Ethiek & AI-act** — verantwoord gebruik van modellen en geautomatiseerde beslissingen
- **Datagovernance** — wie mag wat, classificatie, auditability

### Platform & tech

Wat er moet staan voordat het product-werk kan beginnen — infrastructuur, standaarden, tooling.

- **Infra & SDP** — tenants, namespaces, objectstore, persistent storage
- **Security-standaarden** — secrets, least-privilege, Dependabot, CVE-beleid
- **Tooling & standaarden** — project-layout, coding conventions, repo-templates
- **GenAI-modellen** — welke modellen zijn beschikbaar, hoe worden ze gebruikt

*Onderscheid met ketenstap 6:* de laag bevat wat er moet staan vóórdat je begint; de ketenstap gaat over wat je met dít specifieke product doet.

### Werkwijze & kennis

Hoe we als team werken — en of onze manier van werken werkt. Inclusief meta-skills.

- **Issue/PR-flow** — issues schrijven, PRs openen en reviewen, mergen
- **Agent-werkwijze** — hoe we Claude inzetten, skills schrijven en onderhouden
- **Skill-onderhoud** — collectie bewaken, dedupliceren, depreceren
- **Dossierkennis** — projectkennis, beslissingen, context vastleggen
- **Reflectie op werkwijze** — terugkijken op hoe we werken (niet op wat we opleverden)

*Onderscheid met ketenstap 8:* ketenstap 8 evalueert het product (helpt het iemand?); deze laag evalueert de werkwijze (werkt onze aanpak?).
