# De description schrijven — en de overlap oplossen

De description is wat de agent bij het starten van elke sessie in z'n systeemprompt krijgt,
van álle skills tegelijk. De rest van de skill bestaat op dat moment nog niet. De keuze "is
deze skill relevant" wordt volledig op deze ene regel gemaakt. Een uitstekende skill met een
vage description vuurt nooit.

Budget: 1024 tekens, hard begrensd door de spec — maar dat is een plafond, geen streefwaarde.

## Hoeveel triggeroppervlak heb je nodig? Kijk naar `ceda-activation`

| Activation | Wat de description moet doen | Richtlijn |
|---|---|---|
| `ambient` | vuren op iets wat niemand aankondigt: een geplakte foutmelding, een bestand dat iemand opent | het volle budget als het nodig is |
| `command`, `chained` | herkend worden als iemand `/naam` typt of de projectinstructies ernaar verwijzen | ≤400 tekens |

Bij `ambient` is onder-triggeren het grootste risico; formuleer daar bij twijfel iets te
opdringerig. Bij een aangeroepen skill werkt dat averechts: de activatie is al geregeld, en
elk extra woord concurreert alleen nog met de descriptions van álle andere skills.

De validator waarschuwt boven de 400 tekens bij `command` of `chained`.

## Wat er niet in hoort

Mechaniek. Concreet: bestemmingen en paden (`data/<datum>/<repo>/`), repo- en bestandsnamen,
tool- en stapnamen, vlaggen, bestandsformaten, het interne schema.

De toets: **verandert dit zonder dat de trigger verandert, dan hoort het in de body.** Verhuist
de output morgen naar een andere repo, dan is dat geen reden om de description aan te raken —
staat het pad erin, dan is het dat wel, en betaal je die regel intussen in élke sessie.

De validator waarschuwt op paden, bestandsnamen, `--vlaggen` en `<placeholders>` in de
description.

## Vier eisen

1. **Derde persoon, met echte triggers.** Niet wat de skill *is* maar wanneer hij *aan moet*.
   Neem de woorden op die de gebruiker letterlijk typt — inclusief productnamen, foutmeldingen
   en systeemnamen. `surf-sdp-helm-flux` doet dit goed: hij noemt SDP, Harbor, cr.surf.nl,
   FluxCD, HelmRepository, HelmRelease én "even if they only paste a pipeline log or kubectl
   output without an explicit question". Dat laatste is de belangrijkste zin: mensen plakken
   een fout, ze stellen geen vraag.
2. **Een exclusion-clause.** Zie hieronder — er zijn twee vormen en de tweede wordt vaak
   vergeten.
3. **Taal: volg de gebruiker.** Schrijf in de taal waarin de triggers gesteld zijn. Twee
   varianten alleen als het team het onderwerp echt in twee talen benoemt
   (`issue`/`melding`, `deployen`/`uitrollen`). Een verzonnen vertaling naast elke term kost
   budget en vuurt nergens op.
4. **Niet tijdsgebonden.** Geen "de nieuwe manier om…" — dat veroudert stil.

Bij twijfel — en alleen bij `ambient` — iets te opdringerig formuleren. Onder-triggeren is
daar in de praktijk vaker het probleem, en een skill die te vaak afgaat merk je meteen.

## De exclusion-clause heeft twee vormen

**(a) Verwijzend — een andere skill hoort hier te vuren.**

> LET OP — als het doel is te sorteren en de top-N te selecteren, gebruik dan
> `voorspellen-ranking`.

**(b) Begrenzend — geen enkele skill hoort hier te vuren.**

Dit is de vorm die het vaakst ontbreekt, en hij is belangrijker. Een skill met scherpe
triggers vuurt ook op het buurdomein, en dan geeft hij advies dat dáár aantoonbaar fout is.

`surf-sdp-helm-flux` is het voorbeeld: hij triggert op Helm, Flux, HelmRelease en geplakte
`kubectl`-output. Wie een gewone Kubernetes-opstelling debugt krijgt dan SDP-specifieke
antwoorden — de `+`↔`_` OCI-tagtruc, `cr.surf.nl`-authenticatie, de Protected-vlag op GitLab
runners. Alle drie kloppen ze niet buiten SDP. Wat er hoort te staan:

> LET OP — niet voor Helm of Flux buiten het SURF SDP-platform. Zonder Harbor/cr.surf.nl en
> een GitLab-SDP-pipeline gelden deze conventies niet; val dan terug op generieke
> Helm/Flux-kennis.

Vuistregel: kan iemand met een *vergelijkbaar maar ander* systeem deze skill per ongeluk
binnenhalen? Dan hoort vorm (b) erin, met de aannames die dan wegvallen.

## Vorm

```
<Wat de skill doet, één zin, derde persoon.> Gebruik wanneer <expliciete triggerzinnen,
systeemnamen, foutmeldingen — ook als iemand alleen output plakt zonder vraag>. LET OP —
<verwijzend of begrenzend, of allebei>.
```

## De overlap-check

Draai deze stap altijd, ook als de nieuwe skill duidelijk uniek voelt.

```bash
grep -h "^description:" .claude/skills/*/SKILL.md
```

Bepaal per bestaande skill of hij triggerwoorden deelt met de nieuwe. Vier of meer gedeelde
inhoudswoorden is genoeg om onbetrouwbaar te worden. `scripts/validate-skill.py
.claude/skills` doet deze vergelijking machinaal en waarschuwt per paar; woorden die in meer
dan ~12% van alle descriptions voorkomen ("maak", "levert", "gebruik") gooit hij eerst weg,
want die dragen geen triggersignaal.

**Bij overlap verander je twee descriptions, niet één.** De nieuwe skill krijgt een clause die
naar de bestaande wijst, en de bestaande krijgt er een die terugwijst — in dezelfde PR. Doe je
dat niet, dan groeit de collectie en verslechtert de activatie tegelijk.

Bekende overlappen in de huidige collectie, bruikbaar als testgeval:
`vormgever-npuls-huisstijl` / `-2`, `generate_slides_retro` / `generate-slides-retro-simple`,
`write-issue` / `write-issue-cowork`.

## Toetsen voor je verder gaat

- Zou deze description vuren op elk van de triggerzinnen uit het interview? Zo nee, welk woord
  ontbreekt?
- Zou hij vuren op een zin die bij een andere skill hoort, of op een buurdomein waar de
  aannames niet gelden? Dan de exclusion-clause verscherpen.
- Staat er een woord in dat alleen jij gebruikt en de gebruiker nooit typt? Vervangen.
