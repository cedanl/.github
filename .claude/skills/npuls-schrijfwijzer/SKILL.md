---
name: npuls-schrijfwijzer
description: Gebruik wanneer een tekst moet worden gecontroleerd of herschreven volgens de Npuls-schrijfwijzer (14 april 2025) — teksten van Aslam of collega's, of door AI geschreven tekst voor slides, README's, pitches, issues, nieuwsbrieven, webteksten of LinkedIn. Ook bij "/npuls-schrijfwijzer", "check op de schrijfwijzer", "Npuls-proof", "klopt de toon".
allowed-tools: Read Edit Bash
compatibility: Requires python 3 (alleen standaardbibliotheek)
metadata:
  ceda-id: ceda.npuls-schrijfwijzer
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: "Npuls Schrijfwijzer, team Communicatie, 14 april 2025 (communicatie@npuls.nl)"
  ceda-activation: ambient
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Npuls-schrijfwijzer: tekst controleren

Bron: *Schrijfwijzer – Eerste hulp bij het schrijven van een Npuls tekst* (14 april 2025). Vragen: communicatie@npuls.nl.

## Werkwijze

1. **Automatische check.** Zet de tekst in een bestand (of gebruik het bronbestand: .md, .html, .txt) en draai:
   `python -I <skill>/scripts/check.py <bestand>`
   Het script meldt per zin: lange zinnen (>20 woorden), lijdende vorm, schrapwoorden, Engelse woorden, "u/uw", "door Npuls", te veel bijzinnen en zinnen die steeds met en/maar/want doorlopen. HTML-tags en codeblokken worden genegeerd.
2. **Handmatige check** op wat een script niet ziet (lijst hieronder).
3. **Rapporteer kort:** eerste regel = oordeel (bijv. "7 punten, vooral lange zinnen"). Daarna per punt: citaat → voorstel. Geen uitleg van de regels tenzij gevraagd.
4. **Herschrijven alleen als gevraagd**, of als de gebruiker "pas aan" zegt. Houd feiten, cijfers en termen gelijk; verander alleen vorm.

Het script geeft signalen, geen oordeel. Een lijdende vorm of Engels vakwoord kan terecht zijn (bijv. "dashboard", een productnaam, een citaat). Neem alleen over wat de tekst echt beter maakt.

## Regels uit de schrijfwijzer

**Toon (tone of voice):** toegankelijk en duidelijk · samenwerkend en inclusief · inspirerend en positief · betrouwbaar en professioneel (consistente termen, onderbouwd met feiten, eerlijk over uitdagingen).

**Aanspreekvorm:** altijd "je" of "wij". Nooit "u/uw".

**In Npuls, door de instellingen:** instellingen zijn het onderwerp. Schrijf "instellingen in Npuls" of "samen met instellingen", niet "door Npuls" of "Npuls levert aan instellingen". Laat voorbeelden uit instellingen zien. Benadruk gelijkwaardigheid, eigenaarschap, samen leren.

**Actief schrijven:** "Wij organiseren…", niet "…wordt georganiseerd door ons". Beperk "worden" en "zijn".

**Nederlands eerst:** geen Engels woord als er een goed Nederlands woord is (feedback → terugkoppeling, meeting → overleg, deadline → einddatum, update → stand van zaken, insights → inzichten, stakeholders → betrokkenen). Engelse doelgroep: Brits-Engels (realise, organise, programme; uitzondering Center for Teaching and Learning), datum "11 May", tijd 24-uurs ("14:00").

**Lidwoorden:** het blog, de column, het webinar.

**Zinsbouw:**
- Zinnen ≤ 20 woorden.
- Hooguit één bijzin per zin.
- Geen tangconstructies (tussenzinnen, woordstapels tussen lidwoord en zelfstandig naamwoord).
- Niet steeds zinsdelen koppelen met en/maar/want: zet een punt.
- Schrap overbodige woorden: er, totaal, zoals, momenteel, huidig, in principe, bepaalde, gezamenlijk.

**Doen:** inclusieve taal · consistente termen · begrijpelijk, jargon vermijden of uitleggen · toegankelijk voor docenten en ondersteuners van verschillende taalniveaus.
**Laten:** lange omslachtige zinnen · vakjargon zonder uitleg · dubbelzinnige termen · exclusieve taal.

**Kanalen:**
- *Web:* korte alinea's, opsommingen, kernboodschap in de eerste zinnen.
- *Social media:* kort en krachtig, activerende taal en call-to-action, hashtags en mentions voorstellen.
- *Nieuwsbrief:* heldere, pakkende koppen; weinig onderwerpen; tekst ≤ 350 tekens; duidelijke call-to-action.

## Handmatige checklist (niet door het script gedekt)

- Staat de kernboodschap in de eerste zin of kop?
- Is elk vakwoord (RO, crebo, BRIN, 1CHO, cohort, nominale duur…) uitgelegd of vervangen?
- Zijn instellingen het onderwerp, en Npuls/CEDA partner?
- Positief en eerlijk: worden beperkingen genoemd zonder te verbloemen?
- Eén term per begrip in de hele tekst (niet afwisselend "student" en "deelnemer").
- Spelling en grammatica.

## Typische AI-tekstvalkuilen om extra op te letten

- Holle opener of samenvatting ("In de snel veranderende wereld van…", "Kortom,…").
- Opsomming van drie bijvoeglijke naamwoorden zonder inhoud.
- Engelse leenwoorden en anglicismen ("impact maken", "in lijn met", "het einde van de dag").
- Overmatig "cruciaal", "essentieel", "naadloos", "robuust", "holistisch".
- Lange gedachtestreep-constructies die een bijzin verstoppen.
