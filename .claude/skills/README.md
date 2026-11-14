# CEDA-skills

De org-brede skillcollectie. Eén map per skill, met een `SKILL.md` die de frontmatter uit de
Agent Skills-spec draagt plus het CEDA-`metadata`-blok. Zie `skills-ontology` voor wat die
velden betekenen en `create-skill` voor het aanmaken en valideren.

```bash
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills            # hele collectie
python3 .claude/skills/create-skill/scripts/validate-skill.py .claude/skills/<naam>     # één skill
```

## Herkomst: wat we uit superpowers hebben overgenomen

[superpowers](https://github.com/obra/superpowers) (MIT, © 2025 Jesse Vincent) is een
persoonlijke plugin, geen org-tooling. Wat het team nodig heeft is daarom gevendord: een kopie
in deze collectie, met `ceda-origin: extended` en `ceda-upstream` als onderhoudslink, zodat
bijwerken mogelijk blijft.

| CEDA-skill | Upstream | Aangepast voor CEDA |
|---|---|---|
| `brainstorm` | `brainstorming` | Nederlands en caveman-bondig; aannames-eerst met confidence in plaats van een vragenronde; samenvatting landt in `docs/specs/` als input voor `/plan` |
| `plan` | `writing-plans` | Plan in `docs/plans/`; input is de samenvatting uit `docs/specs/`; taken worden issues via `/write-issue` in plaats van een losse checklist |
| `worktree` | `using-git-worktrees` | CEDA-branchnaamgeving; detecteert eerst of je al in een worktree zit |

`brainstorm` is een randgeval: de tekst is in huis geschreven (commit `19d7e2f`), maar de
ruggengraat is die van upstream — hard gate, "te simpel bestaat niet", 2-3 aanpakken, in delen
presenteren, self-review, doorgeven aan het plan. Daarom `extended` en niet `own`: verandert
upstream die ruggengraat, dan is dat hier het lezen waard.

## Wat we bewust niet hebben overgenomen

**De reviewer-subagent-prompts.** Upstream levert `brainstorming/spec-document-reviewer-prompt.md`
en `writing-plans/plan-document-reviewer-prompt.md`: losse prompts om een subagent de spec of
het plan te laten nakijken. Geen van beide upstream-`SKILL.md`'s roept ze nog aan; writing-plans
zegt zelfs expliciet *"This is a checklist you run yourself — not a subagent dispatch"*. De
bestanden komen uit een plan van januari 2026 en zijn blijven liggen toen die review naar inline
verhuisde. Onze self-review-stap in `brainstorm` en `plan` is die inline-versie. Overnemen zou
een ronde terugzetten die upstream zelf geschrapt heeft.

**De visual companion.** Upstream `brainstorming` heeft een browsergebaseerde metgezel voor
mockups en diagrammen: een gids van ~300 regels plus ~1.400 regels node/bash (lokale HTTP- en
WebSocket-server met session-key, `--open` naar een browsertab). Niet overgenomen, om vier
redenen:

1. `brainstorm` is een beslisskill; de output is een beslis-samenvatting, geen mockup. Visuele
   keuzes horen bij `ui-designer`, `ontwerper-digitaal-product` en `vormgever-npuls-huisstijl`.
2. Gebundelde scripts zijn oppervlak 3 uit `externe-skill-audit`. Een meegeleverde server vergt
   een volledige audit en een expliciete `allowed-tools`-grant, in een publieke repo.
3. Upstream noemt hem zelf *"still new and can be token-intensive"*.
4. 1.400 gevendorde regels die we op upstream moeten blijven volgen.

Wil iemand dit alsnog: eigen skill, eigen audit — niet stil aan `brainstorm` plakken.

**`executing-plans` en `subagent-driven-development`.** Upstream eindigt `writing-plans` in een
keuze tussen die twee uitvoeringsskills. Wij hebben ze niet geport; `plan` stap 8 doet de
verkorte versie zelf (verse subagent per taak, review tussendoor). Als de uitvoering complexer
wordt dan die stap aankan, is dit het eerste dat alsnog moet komen.

---

Deze pagina hoort op termijn in de gepubliceerde documentatie (`docs/`), niet in `.claude/`.
Hij staat hier zolang de skillcollectie zelf nog geen plek in de mkdocs-navigatie heeft.
