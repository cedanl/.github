# Skill-gaps CEDA

Analyse van de skill-collectie in `cedanl/.github/.claude/skills`, inclusief openstaande PR's en branches. Peildatum 21 juli 2026.

## Uitgangssituatie

| Bron | Skills |
|---|---|
| `main` | 34 |
| PR #48 objectstore | 2 (`objectstore-onboarding`, `objectstore-experiments`) |
| PR #46 app-integration | 5 (`docker`, `streamlit`, `surfdrive`, `etl-pipeline`, `sram-oidc`) |
| PR #43 sdp-platform | 4 (`sdp-onboard`, `sdp-secrets-management`, `gitlab-ci`, `surf-sdp-helm-flux`) |
| PR #42 workflow | 6 (`ship`, `pr-reply`, `branch-pr`, `gate`, `actions-ci`, `pypi-project`) |
| PR #47 create-skill | 0 nieuwe skills; voegt skill-type "Kennis" toe aan de conventies |
| branch `skills/datascience` | 2 (`data-cleaner`, `data-scientist`) — **geen PR geopend** |

Totaal ~53 skills, waarvan 19 nog niet beschikbaar voor het team.

Twee observaties vooraf, want ze kleuren elke gap hieronder:

- **Het knelpunt is mergen, niet schrijven.** Negentien geschreven skills liggen stil. De datascience-branch (commit 20 juli) heeft nooit een PR gekregen. Nieuwe skills toevoegen aan een collectie die niet doorstroomt vergroot vooral de achterstand.
- **De collectie is scheef verdeeld.** Vormgeving/presentaties (7 skills) en dev-workflow (16) zijn ruim bediend. De inhoudelijke kern van CEDA — van data naar besluit — is dun, en het staartstuk ontbreekt volledig.

---

## Gap 1 — Interpretatie en actie

**Wat er is:** niets. Ook niet in branches.

**Waarom dit de belangrijkste gap is.** De CEDA-pijplijn loopt ingest → prepare → transform → combine → analyze/export. Met `data-cleaner`, `data-scientist` en de vier `voorspellen-*` skills is alles tot en met *analyze* gedekt. Wat erna komt niet: hoe je een uitkomst duidt, welke nuances je moet benoemen, welke definitiekeuzes de conclusie sturen, en hoe je van uitkomst naar interventie gaat.

Precies daar loopt onderwijsanalytics in de praktijk vast. Een uitvalprognose die niemand vertaalt naar handelen levert niets op. En een instelling die "uitval" anders definieert dan het model komt tot een tegengestelde conclusie op dezelfde data.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `definitie-check` | Kennis | Veelgebruikte onderwijsdefinities (uitval, switch, rendement, instroom) en wat de keuze doet met de uitkomst |
| `resultaat-duiden` | Workflow | Van modeluitkomst naar bevinding: onzekerheid, confounders, wat je *niet* mag concluderen |
| `interventie-ontwerp` | Workflow | Van bevinding naar handeling: wie doet wat, hoe meet je effect, wat is de nulhypothese |

**Prioriteit: hoog.** Grootste inhoudelijke gat, en het onderscheidt CEDA van een willekeurig analytics-team.

---

## Gap 2 — Data governance, AVG en architectuur

**Wat er is:** niets.

**Waarom.** CEDA werkt met onderwijsdata en persoonsgegevens: DUO-leveringen, 1CHO, SIS-koppelingen. Bij elke instelling is de eerste vraag wat er met die data gebeurt, wie erbij kan en op welke grondslag. Op dit moment zit dat antwoord alleen in hoofden. `sdp-secrets-management` (PR #43) dekt technische secrets, niet governance.

Dit is ook de gap met het grootste afbreukrisico: een fout hier is niet een bug maar een incident.

**Architectuur hoort bij deze gap.** Governance zonder architectuur blijft abstract: pas als je data indeelt naar object en classificatie kun je grondslagen, toegang en pseudonimisering concreet maken. De sector heeft die indeling al gestandaardiseerd — we hoeven hem niet zelf te verzinnen, wel te codificeren:

- **HORA** ([hora.surf.nl](https://hora.surf.nl/index.php/Over_HORA)) — de Hoger Onderwijs Referentie Architectuur van SURF: bedrijfsfuncties, applicatielandschap en informatiemodel als gedeelde taal met instellingen.
- **OOAPI v6** ([oeapi.eu/v6.0](https://oeapi.eu/v6.0/#/), spec op [open-education-api/specification](https://github.com/open-education-api/specification)) — het objectmodel voor onderwijsdata (programma's, cursussen, personen, resultaten); het natuurlijke splitsingsniveau voor dataleveringen.
- **BIV-classificatie** — per object beschikbaarheid, integriteit en vertrouwelijkheid vastleggen, als basis voor wie erbij mag en hoe het opgeslagen wordt.
- **[Npuls-OKx/meta](https://github.com/Npuls-OKx/meta)** — inspiratie voor de vorm: ArchiMate-model in de repo, ADR's voor architectuurkeuzes, MOKA-koppelvlaktemplates en het principe "OEAPI, tenzij". Ook hun combinatie van architectuurdocumentatie met agent-artifacten en slash commands is direct relevant voor onze skill-aanpak.

**Doorwerking naar de ETL-skills.** `etl-pipeline` (PR #46) en `data-cleaner` (branch `skills/datascience`) horen naar deze laag te verwijzen. Een levering is pas af als hij niet alleen schoon is, maar ook goed gesplitst (per object, per BIV-klasse), gepseudonimiseerd waar vertrouwelijkheid dat vraagt, en beheersbaar ingericht: per set een eigenaar, een bewaartermijn en herleidbaar wie hem mag zien. Data-cleaning dekt "ziet de data er goed uit"; inrichting en beheersbaarheid ná de ETL is de andere helft en ontbreekt nu in beide skills.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `data-governance` | Kennis | Grondslagen, bewaartermijnen, pseudonimisering, verwerkersovereenkomsten in onderwijscontext |
| `referentie-architectuur` | Kennis | HORA-mapping, OOAPI-objectmodel, BIV-classificatie per object; gedeelde taal richting instellingen |
| `privacy-check` | Workflow | Loop een repo/dataset na op persoonsgegevens, herleidbaarheid en onbedoelde export |
| `data-oplevering` | Workflow | Toets een ETL-output: gesplitst per object en BIV-klasse, gepseudonimiseerd waar nodig, eigenaar en bewaartermijn per set |

**Prioriteit: hoog.** Lage bouwkosten, hoog risico bij afwezigheid. Het architectuurdeel is bovendien randvoorwaarde voor de ETL-skills in PR #46: die kunnen beter niet gemerged worden zonder verwijzing naar deze laag.

---

## Gap 3 — Doelgroep en intake

**Wat er is:** `ontwerper-concurrentie-analyse`, `ontwerper-toekomst-verwachting`, `ontwerper-trend-analyse`. Dat is markt- en trendanalyse, geen gebruikersonderzoek.

**Waarom.** Er is geen skill voor het begin van een project: wie is de gebruiker, wat is de vraag achter de vraag, wat is de scope. `write-issue` pakt dat impliciet op zodra de vraag al scherp is, maar het traject daarvóór — het gesprek met een instelling — is niet gecodificeerd. Gevolg: elke intake is maatwerk en de kwaliteit hangt af van wie hem doet.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `intake-instelling` | Workflow | Van open vraag naar afgebakende opdracht: wat is beschikbaar, wat is haalbaar, wat is de beslissing die het moet ondersteunen |
| `persona-onderwijs` | Kennis | Rollen bij instellingen (opleidingsmanager, beleidsmedewerker, decaan, IR) en wat elk nodig heeft |

**Prioriteit: midden.** Hoge waarde bij opschaling naar meer instellingen; minder urgent voor lopend werk.

---

## Gap 4 — Testen en reproduceerbaarheid

**Wat er is:** `check-style` (stijlconventies), `gate` in PR #42 (deels kwaliteitscontrole).

**Waarom.** Geen testconventies voor R of Python, en niets over reproduceerbaarheid: environments vastleggen, seeds, dataversies. Bij voorspelmodellen is dat geen luxe — zonder vastgelegde dataversie is een uitkomst niet te herleiden en dus niet te verdedigen tegenover een instelling.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `testconventies` | Kennis | testthat / pytest, wat test je wel en niet in een analyse-repo |
| `reproduceerbaar` | Workflow | Environments, seeds, dataversionering, run-vastlegging |

**Prioriteit: midden.** Wordt urgent zodra modellen bij instellingen in gebruik gaan.

---

## Gap 5 — Onboarding van mensen

**Wat er is:** `sdp-onboard` en `objectstore-onboarding` — dat is platform-onboarding, niet mens-onboarding.

**Waarom.** Niets voor een nieuw teamlid ("waar begin ik, welke repo's, welke conventies, welke skills") en niets voor een nieuwe instelling. Het TKM-ontwerp in `cedanl/project_algemeen#41` beschrijft de kennisarchitectuur, maar is nog geen skill.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `onboard-teamlid` | Workflow | Eerste week: toegang, repo's, conventies, welke skill wanneer |
| `kennis-vastleggen` | Workflow | TKM-praktijk: wat leg je vast, waar, in welke laag |

**Prioriteit: midden.** Schaalt met teamgroei.

---

## Gap 6 — Skill-lifecycle

**Wat er is:** `create-skill` (aanmaken), PR #47 (skill-type "Kennis" toevoegen aan de conventies).

**Waarom.** Aanmaken is gedekt, de rest van de levensloop niet. Concrete symptomen nu al zichtbaar:

- **Dubbelingen:** `vormgever-npuls-huisstijl` en `-2`; `generate_slides_retro`, `generate-slides-retro` en `-simple`; `write-issue` en `write-issue-cowork`.
- **Stilstand:** 19 skills in 5 PR's, één branch zonder PR.
- **Geen deprecatiepad:** een vervangen skill blijft gewoon staan en blijft dus ook triggeren.

Bij 53 skills is dit hinderlijk. Bij 80 is het een probleem, want overlappende descriptions maken auto-activatie onbetrouwbaar.

Twee onderdelen van de levensloop die we tot nu toe helemaal niet benoemd hadden:

**Herkomst van de inhoud.** De grootste kwaliteitsvariabele bij het aanmaken is niet de vorm maar waar de inhoud vandaan komt. Een skill die je een model laat verzinnen uit algemene kennis levert generieke instructies op ("ga zorgvuldig om met fouten"); een skill gedestilleerd uit een echt uitgevoerde taak levert de specifieke conventies, valkuilen en correcties op die hem waardevol maken. Bruikbare bronnen: een sessie waarin je de taak daadwerkelijk hebt gedaan mét jouw correcties, bestaande interne documentatie en runbooks, code-review-commentaar, en git-historie van fixes.

Dit weegt in onze context zwaarder dan in de bronnen waar het vandaan komt. Bij onderwijsdata — DUO-leveringen, 1CHO-definities, SIS-eigenaardigheden — heeft het model weinig achtergrond, dus is verzonnen inhoud slecht herkenbaar als verzonnen. `create-skill` hoort daarom een verplichte stap te krijgen: *waar komt deze inhoud vandaan?*, met `self` als expliciete claim in plaats van stilzwijgende default.

**Auditen van skills en skill-chains.** Met `origin: external` in de ontologie moedigen we aan om generieke skills over te nemen. Dat is de juiste volgorde, maar op dit moment zonder controlepunt. Een overgenomen skill draait met onze rechten en onze data; hij hoort nagelopen te worden op wat hij aanraakt (`allowed-tools`), of hij externe netwerkbronnen benadert, en welke andere skills hij aanroept. Dat laatste is het punt dat we nog nergens dekken: een chain is een pad, en een pad kan rechten optellen die geen enkele losse skill heeft. Bij een keten die extern materiaal inleest en daarna schrijfrechten gebruikt, hoort een scheiding — het deel dat onvertrouwde inhoud verwerkt krijgt geen schrijfrechten.

**Voorgestelde skills**

| Skill | Type | Scope |
|---|---|---|
| `review-skill` | Workflow | Beoordeel een skill-PR: scope, overlap met bestaande skills, description-kwaliteit (incl. exclusion-clause), kennis- of workflow-type, herkomst van de inhoud |
| `dedup-skills` | Workflow | Detecteer overlappende skills, voeg samen of deprecate |
| `audit-skill` | Workflow | Loop een externe of gewijzigde skill na: tools, netwerkoproepen, gebundelde scripts, en de chains waar hij in zit |

Een vierde ontbrekend stuk van de levensloop — meten of een skill überhaupt iets toevoegt ten opzichte van géén skill — staat apart uitgewerkt in `cedanl/.github#49`. Dat is het instrument onder `dedup-skills`: zonder baseline is "deze skill is overbodig" een mening.

**Prioriteit: hoog.** Niet omdat het inhoudelijk het belangrijkst is, maar omdat het de andere gaps blokkeert: zonder doorstroming landt nieuw werk niet.

---

## Wat dit betekent voor de indeling

De voorgestelde categorisering (Data science / Repo's / Coding / Documentatie / Infra / Design / Doelgroep / Proces) klopt als inhoudsopgave, maar mengt drie assen: kennisdomein, artefact en handeling. PR #47 zet de eerste stap door "Kennis" als expliciet skill-type te introduceren — dat onderscheid is het waard om door te trekken, omdat kennis-skills breed en dun zijn en worden opgezocht, terwijl workflow-skills smal en diep zijn en worden uitgevoerd.

Twee categorieën vragen om splitsing zodra de openstaande PR's landen:

- **Proces** → *dev-workflow* (`ship`, `branch-pr`, `gate`, `actions-ci`, `pr-reply`) versus *team-proces* (retro-slides, `write-issue`, `brainstorm`, `sparren`).
- **Infra** → *platform* (SDP, Object Store, GitLab CI) versus *app-integratie* (`docker`, `streamlit`, `sram-oidc`, `surfdrive`).

## Voorgestelde volgorde

1. Merge-achterstand wegwerken en PR openen voor `skills/datascience` (Gap 6 als aanleiding).
2. Governance, architectuur en interpretatie bouwen (Gap 1 en 2) — grootste inhoudelijke en risico-gaten, en het architectuurdeel is randvoorwaarde voor de ETL-skills in PR #46.
3. Intake, testen, onboarding (Gap 3, 4, 5) — schalen mee met groei van team en instellingen.
