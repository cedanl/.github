# Vormpatronen — welke sectie verdient hier z'n plek

Het skelet is de bodem: kop, oriëntatie, `## Workflow` of `## Wanneer dit geldt`, en
`## Important`. Alles hieronder is optioneel en **verdient z'n plek pas als het antwoord op de
toelatingsvraag ja is**. Een lege of ceremoniële sectie is slechter dan geen sectie: de agent
moet er doorheen lezen en vindt niets.

Elk patroon verwijst naar een skill in de collectie die het al goed doet. Lees die als
voorbeeld in plaats van het patroon na te bouwen uit deze beschrijving.

## Kopjes die het feit noemen

**Toelatingsvraag:** is er één specifiek feit dat de lezer moet vinden terwijl hij iets
anders aan het lezen is?

Dan wordt dat feit een kop, niet een bullet. `## Critical gotcha: '+' becomes '_' in OCI
tags` is vindbaar bij het scannen; `## Gotchas` met zeven bullets is dat niet. Dit is het
goedkoopste patroon dat er is: dezelfde inhoud, andere kop.

Voorbeeld: `surf-sdp-helm-flux`.

## Symptoom-tabel

**Toelatingsvraag:** produceert dit domein terugkerende foutmeldingen of symptomen?

| Symptoom | Waarschijnlijke oorzaak | Eerste actie |
|---|---|---|

De hoogste informatiedichtheid per token die er is, en precies de vorm waarin iemand een
probleem tegenkomt: hij plakt een foutmelding, niet een vraag. Zet de letterlijke tekst van
de fout in de linkerkolom — daar matcht de lezer op.

Voorbeelden: `surf-sdp-helm-flux` (8 rijen), `sdp-secrets-management` (error quick reference).

## Het dubbelzinnige geval

**Toelatingsvraag:** is er een symptoom met twee verschillende oorzaken die om tegengestelde
acties vragen?

Dan is dat een eigen sectie waard, want dit is waar mensen én modellen de fout in gaan. Vorm:
noem het symptoom, dan genummerd de twee oorzaken, per oorzaak het onderscheidende signaal en
de bijbehorende actie.

`surf-sdp-helm-flux` doet dit met "stuck vs. slow": dezelfde timeout-output betekent óf dat
Flux nog bezig is, óf dat Flux het heeft opgegeven en teruggerold — en het verschil bepaalt
of je moet wachten of moet ingrijpen.

## Beslisboom

**Toelatingsvraag:** moet de lezer kiezen tussen meerdere tools, paden of formats, en hangt
er iets vanaf?

Eén tabel of genummerde vragenreeks die naar één uitkomst leidt. Geen menu van
gelijkwaardige opties — kies een default en noem het alternatief in een bijzin.

Voorbeeld: `sdp-secrets-management`, "welke tool voor welk secret".

## Architectuur-schets

**Toelatingsvraag:** moet de lezer weten hoe iets door het systeem beweegt voor hij een fout
kan plaatsen?

Een ASCII-schets van de keten plus de eigenschappen die eruit volgen. De waarde zit niet in
het plaatje maar in de conclusie eronder: "elk deployprobleem is dus (a), (b) of (c) — stel
eerst vast welke". Dat is wat een diagnose stuurt.

Voorbeeld: `surf-sdp-helm-flux`, "how a change reaches the cluster".

## Gebundelde bestanden

**Toelatingsvraag:** staan er bestanden naast `SKILL.md`?

Dan is deze sectie verplicht, want er is geen frontmatter-veld dat het werk doet: de agent
leest de body. Eén regel per bestand, met de conditie erin.

```markdown
## Gebundelde bestanden

- `references/diagnostics.md` — lees bij een vastgelopen release, voor de volledige
  describe/get/watch-volgorde
- `scripts/hr-status.sh <release> <namespace>` — draaien, niet lezen: geeft condities,
  history en recente jobs in één overzicht
```

Scripts krijgen hun aanroep erbij. Een script kost alleen z'n output aan context, niet z'n
broncode — dat is het hele punt.

## Output-template

**Toelatingsvraag:** moet de output een vaste vorm hebben die de gebruiker herkent?

Zet de template letterlijk in de skill; modellen matchen beter op een concrete structuur dan
op een beschrijving ervan. Korte templates inline, lange in `assets/`.

## Checklist en validatielus

**Toelatingsvraag:** heeft de workflow stappen die van elkaar afhangen, of een controle die
kan falen?

Checklist bij afhankelijke stappen. Validatielus bij een controle die kan falen: doe het
werk, draai de check, herstel, herhaal tot hij slaagt. Bij batch- of destructieve acties de
zwaardere variant: maak eerst een plan in een gestructureerd bestand, valideer dat tegen de
bron van waarheid, en voer het pas daarna uit.

## Important als recap

**Toelatingsvraag:** altijd ja.

Drie tot zes regels, en het mag herhalen wat hierboven al stond — dat is bewuste redundantie,
geen slordigheid. Neem hier op: wat er misgaat als je het negeert, en waar de skill níet
geldt. Dupliceren *binnen* een skill is goedkoop; dupliceren *tussen* skills is de drift die
we juist bestrijden.

---

## Het diagnose-patroon: kennis die een procedure is

Bij troubleshooting valt de scheiding tussen workflow en reference weg. De kennis *is*
"in situatie X doe Y" — daar is geen sequentie die je van begin tot eind draait, maar wel een
handelingsvolgorde per symptoom. Dat blijft `ceda-type: reference` met
`ceda-subtype: knowledge`; forceer er geen `## Workflow` op.

De vorm die dan werkt, in deze volgorde:

1. **Oriëntatie met een instructie** — "lees dit volledig voor je een fix voorstelt; generiek
   advies kost hier tijd". Niet een samenvatting van wat volgt.
2. **Mentaal model** — de architectuur-schets, met de indeling die de diagnose stuurt.
3. **De benoemde valkuilen** — elk met een eigen kop die het feit noemt.
4. **De dubbelzinnige gevallen** — zelfde symptoom, tegengestelde actie.
5. **Conventies** — wat je moet aanhouden als je iets bouwt in plaats van repareert.
6. **Symptoom-tabel** — de snelle ingang voor wie alleen een foutmelding plakt.
7. **Gebundelde bestanden** — het volledige commando-runbook en de scripts.
8. **Important** — de recap.

Dit is de vorm van `surf-sdp-helm-flux` en `sdp-secrets-management`. Bouw je zoiets, lees dan
één van die twee helemaal door voor je begint.
