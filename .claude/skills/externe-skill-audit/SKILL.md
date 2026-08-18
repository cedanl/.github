---
name: externe-skill-audit
description: Draagt het CEDA-model om te beoordelen of een van buiten overgenomen skill veilig in de collectie kan — wat `allowed-tools` wel en niet betekent, de vier oppervlakken (tools, netwerk, gebundelde scripts, chains), waarom een keten rechten kan optellen die geen losse skill heeft, en welke rechten je bij overname toekent. Gebruik wanneer iemand een skill van GitHub, skills.sh, een plugin of een marketplace wil overnemen, vraagt of een externe skill veilig is, `ceda-origin: external` of `extended` invult, of woorden gebruikt als "skill overnemen", "externe skill", "is dit veilig", "wat mag deze skill". LET OP — gaat het om het beoordelen van een skill-PR van een collega, gebruik dan `review-skill`, die laadt deze kennis zelf; om zelf een skill schrijven, `create-skill`. Niet voor het auditen van gewone applicatiecode of dependencies — dat is een andere discipline met andere gereedschappen.
allowed-tools: Read Grep Glob Bash
metadata:
  ceda-id: ceda.externe-skill-audit
  ceda-version: "0.1.0"
  ceda-type: reference
  ceda-subtype: knowledge
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: self
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Externe skill auditen

Met `ceda-origin: external` moedigen we aan om generieke skills over te nemen in plaats van
ze zelf te schrijven. Dat is de juiste volgorde, maar het controlepunt hoort erbij: een
overgenomen skill draait met **onze** rechten op **onze** data, en de auteur wist niet wat
dat betekent.

Deze kennis gaat over de vier oppervlakken die je nagaat en het besluit dat je erover neemt.
Niet over hoe je grept — dat weet je al.

## Wanneer dit geldt

Bij `ceda-origin: external` of `extended`, bij het bijwerken van een `extended` skill naar een
nieuwere upstream, en bij elke skill die van buiten de org komt — ook een plugin, ook een
skill die een collega ergens vandaan geplakt heeft.

## Let op: `allowed-tools` is voorafgaande toestemming, geen sandbox

Het veld zegt wat de skill mág vragen, niet wat de runtime tegenhoudt. Het is een
*intentieverklaring* die de audit leesbaar maakt, geen grens die iets afdwingt. Een skill
zonder `allowed-tools` is niet beperkt maar onbepaald — dat is de slechtere van de twee.

Praktisch gevolg: de audit maakt zichtbaar wat de auteur van plan was. De permissieregels van
de runtime en de review van de mens die de skill draait blijven het enige dat werkelijk
begrenst. Presenteer een auditverslag dus nooit als "deze skill kan geen kwaad".

## De vier oppervlakken

| Oppervlak | Wat je vaststelt | Waar het misgaat |
|---|---|---|
| **Tools** | welke tools de skill vraagt, en of dat matcht met wat hij doet | een reference-skill die `Write` of `Bash` vraagt |
| **Netwerk** | haalt hij tijdens uitvoering iets op | een skill die instructies van een url leest — dan bepaalt die url wat de agent doet |
| **Gebundelde scripts** | wat draait er zonder dat het model ernaar kijkt | `scripts/` kost alleen output aan context, dus niemand leest de broncode nog |
| **Chains** | welke andere skills hij aanroept of vereist | zie hieronder — dit is het oppervlak dat wordt overgeslagen |

De eerste drie vind je met één veeg. Zet 'm in de skilldirectory:

```bash
/usr/bin/grep -rnE "curl|wget|https?://|fetch|requests\.|urllib|child_process|exec|eval|base64|token|api[_-]?key|secret|\.env|credential|sudo|rm -rf|--dangerously" .
```

Loop elke treffer met de hand na. Documentatie-urls zijn de meeste hits en die zijn ongevaarlijk;
het gaat om urls die tijdens *uitvoering* opgehaald worden.

## Let op: een chain telt rechten op die geen losse skill heeft

Dit is het punt dat bij een handmatige audit structureel wordt gemist, omdat een verwijzing
naar een andere skill eruitziet als een documentatieprobleem ("die skill hebben we niet, dus
die link is stuk") en niet als een rechtenprobleem.

Een chain is een **pad**, en langs dat pad tellen rechten op. Skill A leest een externe pagina
en heeft alleen `Read Grep`. Skill B schrijft bestanden en heeft `Write Edit`. Roept A daarna
B aan met wat hij gelezen heeft, dan bestaat er een route van *onvertrouwde inhoud* naar
*schrijfrechten* die in geen van beide `allowed-tools`-lijsten te zien is.

Zoek de chain expliciet:

```bash
/usr/bin/grep -rnE "Skill\(|/[a-z][a-z0-9-]+\b|REQUIRED (SUB-SKILL|BACKGROUND)|gebruik dan \`" .
```

**De regel: het deel dat onvertrouwde inhoud verwerkt krijgt geen schrijfrechten.** Loopt de
keten daar toch doorheen, dan splits je — de inlezende stap wordt een aparte skill met
`Read Grep Glob`, en wat hij oplevert gaat als *data* naar de schrijvende stap, niet als
instructie. Kan dat niet, dan is een expliciete bevestigingsstap tussen de twee het minimum,
en dat is een zwakker antwoord.

Let bij een `extended` skill ook op verwijzingen die **buiten de skilldirectory** wijzen
(`../andere-skill/...`). Die breken bij het kopiëren, en een gebroken `REQUIRED BACKGROUND`
betekent dat de skill draait zonder de randvoorwaarde die zijn auteur nodig achtte.

## Het besluit: welke rechten krijgt hij bij ons

Een audit die eindigt in "ziet er schoon uit" is niet af. De uitkomst is een **ingevulde
`allowed-tools`** — dat is de prijs van `origin: external`, en het enige stuk van de audit dat
daarna nog iets doet.

| Wat de skill doet | Wat hij krijgt |
|---|---|
| oordeelt, rapporteert, classificeert | `Read Grep Glob` |
| genereert of wijzigt bestanden | `+ Write Edit` |
| draait commando's | `+ Bash`, en bij een bekende set een nauwe matcher: `Bash(git:*)` |
| leest iets van buiten in | dan geen `Write Edit` in dezelfde skill — zie de chain-regel |

Wijkt dat af van wat de auteur vroeg, noem dat dan: het verschil tussen wat hij wilde en wat
hij krijgt, is de samenvatting van de audit.

## Ook meenemen, want het is geen securityvraag maar het blokkeert wel

- **Licentie en bronvermelding.** Wat de licentie toestaat, en of er materiaal in zit dat van
  weer iemand anders overgenomen is zonder vermelding. `cedanl/.github` is publiek —
  herpubliceren onder onze vlag is een keuze, geen bijvangst.
- **Tegenspraak met onze eigen normen.** Een externe skill die andere regels draagt dan
  `skills-ontology` laat de agent onze bestaande skills als fout behandelen. Dat is geen
  veiligheidsprobleem en wél een reden om niet over te nemen.
- **Contextkosten.** Boven de 500 regels betaal je dat elke keer dat hij vuurt.

## Wat een audit niet vaststelt

Of de skill *werkt*. Daar is de ablation voor (`claude plugin eval --ablation with-without
<naam>`), en die is een aparte vraag met een aparte prijs. Bij uitkomst "niet overnemen"
hoef je hem niet te draaien.

## Important

- `allowed-tools` is toestemming, geen sandbox. Schrijf nooit op dat een skill "veilig" is;
  schrijf op wat hij aanraakt en welke rechten hij bij ons krijgt.
- De chain is het oppervlak dat wordt overgeslagen. Een keten van onvertrouwde inhoud naar
  schrijfrechten hoort gesplitst, niet afgevinkt.
- Deze kennis gaat over skills. Voor het auditen van applicatiecode, dependencies of
  containers gelden andere gereedschappen en een andere discipline.
