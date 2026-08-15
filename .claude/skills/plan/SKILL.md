---
name: plan
description: Zet een genomen besluit om in een uitvoerbaar implementatieplan — bestandsindeling, taken met eigen testcyclus, exacte paden en commando's, een issue per taak — en voert dat plan daarna taak voor taak uit. Gebruik na een go, bij "maak een plan" of "hoe pakken we dit aan", of bij werk over meerdere stappen of bestanden. LET OP — vóór de go hoort `brainstorm`, niet dit.
allowed-tools: Read Write Edit Grep Glob Bash Task AskUserQuestion Skill
license: MIT — afgeleid van superpowers (© 2025 Jesse Vincent)
metadata:
  ceda-id: ceda.plan
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: extended
  ceda-upstream: superpowers:writing-plans
  ceda-source: https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Plan

Write the implementation plan for someone who knows how to program but knows nothing about
this codebase, this toolset, or this problem domain. Everything they need is in the plan:
which files, which code, which command, what output to expect.

Derived from `superpowers:writing-plans` (MIT, © 2025 Jesse Vincent). Changed for CEDA: plans
live in `docs/plans/`, the input is the brainstorm summary in `docs/specs/`, and the tasks land
as issues via `/write-issue` instead of in a loose checklist.

Upstream also ships `plan-document-reviewer-prompt.md`, a subagent that reviews the finished
plan. Not ported: upstream's own `SKILL.md` no longer dispatches it and says the check is a
"checklist you run yourself — not a subagent dispatch". That checklist is step 6 here.

## Workflow

When the user invokes `/plan [optional: subject or path to a spec]`:

Create a todo per numbered step below and work them off in order. The steps that get skipped
under time pressure — the self-review in step 6 and the file structure in step 2 — are exactly
the ones that cost an execution round.

### 1. Check the input

A plan needs a decision that has already been made. In order of preference:

1. A brainstorm summary in `docs/specs/YYYY-MM-DD-<onderwerp>.md` — what `/brainstorm` leaves
   behind after the go. Was no path given, look there for the most recent file and name which
   one you are using.
2. An issue with an agreed approach, or a spec somewhere else in the repo.

Is there none of these, then this skill is too early: run `/brainstorm` first and come back
after the go. A decision that only exists in the chat scrollback is not an input — the plan is
written for someone who was not there, and that includes you after a context reset.

Does the spec cover several independent subsystems? Then propose one plan per subsystem. Each
plan must produce working, testable software on its own.

**Isolated workspace.** Is the work going to touch the repo you are standing in, and are you
on `main` or in a worktree that belongs to something else? Then run `/worktree` before you
write the plan. The execution in step 8 commits per task, and those commits need a branch of
their own.

### 2. Map the file structure first

Before any task exists, write down which files are created or modified and what each one is
responsible for. This is where the decomposition is decided; task boundaries follow from it.

- One clear responsibility per file. Files that change together live together — split by
  responsibility, not by technical layer.
- Smaller focused files over one large file. You reason better about what you can hold in
  context at once, and edits land more reliably.
- In an existing codebase, follow the pattern that is there. Do not restructure on your own
  initiative; a split is fair game when the file you are touching has already grown unwieldy.

### 3. Cut the tasks

A task is the smallest unit that carries its own test cycle and is worth a reviewer's
judgement. Fold setup, configuration, scaffolding, and documentation into the task whose
deliverable needs them. Split only where a reviewer could reject one task while approving the
one next to it. Every task ends in something independently testable.

Within a task each step is one action of a few minutes: write the failing test, run it and see
it fail, write the minimal implementation, run it and see it pass, commit.

### 4. Write the plan

Save to `docs/plans/YYYY-MM-DD-<onderwerp>.md`.

Header:

```markdown
# <Onderwerp> — implementatieplan

> **Uitvoering:** taak voor taak, een verse subagent per taak, één commit per taak. De stappen
> zijn aanvinkbaar (`- [ ]`); wie dit plan oppakt hoeft de sessie waarin het geschreven is niet
> gezien te hebben.

**Bron:** <pad naar de spec of brainstorm-samenvatting waar dit plan uit volgt>
**Doel:** <één zin: wat dit oplevert>
**Aanpak:** <2-3 zinnen>
**Stack:** <talen, frameworks, package manager>

## Randvoorwaarden

<De projectbrede eisen uit de spec — versievloeren, naamgeving, platformeisen —
één regel per stuk, waarden letterlijk uit de spec overgenomen. Deze gelden
impliciet voor elke taak.>

---
```

Per task:

````markdown
### Taak N: <naam>

**Bestanden:**
- Nieuw: `exact/pad/naar/bestand.py`
- Wijzigen: `exact/pad/bestaand.py:123-145`
- Test: `tests/exact/pad/test_bestand.py`

**Interfaces:**
- Gebruikt: <wat uit eerdere taken komt — exacte signatures>
- Levert: <wat latere taken nodig hebben — exacte functienamen, parameter- en
  returntypes. Wie deze taak uitvoert ziet alleen deze taak; dit blok is de
  enige plek waar hij de namen van de buren leert.>

- [ ] **Stap 1: schrijf de falende test**

```python
def test_specifiek_gedrag():
    assert functie(invoer) == verwacht
```

- [ ] **Stap 2: draai de test, zie hem falen**

Draai: `uv run pytest tests/pad/test_bestand.py::test_specifiek_gedrag -v`
Verwacht: FAIL — "functie not defined"

- [ ] **Stap 3: minimale implementatie**

```python
def functie(invoer):
    return verwacht
```

- [ ] **Stap 4: draai de test, zie hem slagen**

Draai: `uv run pytest tests/pad/test_bestand.py::test_specifiek_gedrag -v`
Verwacht: PASS

- [ ] **Stap 5: commit**

```bash
git add tests/pad/test_bestand.py src/pad/bestand.py
git commit -m "feat: <wat>"
```
````

### 5. No placeholders

These are plan failures, not shortcuts. Never write them:

- "TBD", "TODO", "later invullen", "details volgen"
- "voeg passende foutafhandeling toe" / "vang randgevallen af"
- "schrijf hier tests voor" without the actual test code
- "net als taak N" — repeat the code; tasks get read out of order
- a step that says what to do without showing how (code steps need a code block)
- a reference to a type, function, or method that no task defines

### 6. Self-review

Run this yourself, on the finished plan, against the spec. Not a subagent.

1. **Coverage** — walk through every requirement in the spec. Can you point at the task that
   implements it? List the gaps and add the missing tasks.
2. **Placeholders** — search your own plan for the patterns in step 5. Fix them.
3. **Type consistency** — do the names and signatures in later tasks match what earlier tasks
   defined? `clearLayers()` in task 3 and `clearFullLayers()` in task 7 is a bug that costs an
   entire execution round.

Fix what you find inline and move on. No second review round.

### 7. Land the tasks as issues

Split into two questions, because they have different answers:

- **The plan** stays a file in `docs/plans/`. It is the working document; it does not belong in
  an issue body.
- **The tasks** become issues via `/write-issue`, so that the work lands on the CEDA board and
  is visible to others. One issue per task, referring back to the plan file and the task number.

Ask before creating anything:

> Plan staat in `docs/plans/<bestand>.md` — <N> taken.
> Zal ik daar issues van maken op het CEDA-board, of houden we het bij het plan?

Never call `gh issue create` directly; `/write-issue` owns the template and the board fields.

### 8. Execute

One task at a time, in order, a commit per task. Dispatch a **fresh subagent per task**: it
gets the plan file and the task number, nothing else — no scrollback, no memory of why a
choice was made. That is the whole point of writing exact paths, complete code and literal
commands: the plan gets tested by the only reader who cannot fill in the gaps from memory.
Executing everything yourself in the session that wrote the plan hides exactly the holes step 6
is looking for.

After each task: read the diff, run the test the task names, show the result, and wait before
starting the next one. A subagent that got stuck or improvised is a defect in the plan — repair
the plan first, then re-dispatch.

Is a task too small to be worth a subagent (one line, one file)? Then do it inline and say so.

Handing the plan to a new session instead is equally valid; the file is written for that.

## Let op: het plan is voor iemand zonder context

The most expensive mistake here is writing the plan for yourself. You know why a choice was
made and what the file is called; the person executing does not, and neither does a fresh
session of yourself after a context reset. Exact paths, complete code, literal commands with
the output you expect. "Similar to the one above" costs an execution round.

## Verificatie

`ceda-verifies: observable` — the plan is done when a reader who has not been part of this
conversation can answer, per task: which files, which code, which command, and what output
proves it works. Concretely, the step 6 checklist is clean: every spec requirement maps to a
task, no placeholder patterns remain, and the names in later tasks match the earlier ones.

## Important

- No code before the plan is agreed. Is there no decision yet, then `brainstorm` comes first,
  and its summary in `docs/specs/` is the input here.
- Issues only via `/write-issue`, and only after the user says yes — a plan of ten tasks is ten
  issues on a shared board.
- This skill writes the plan and drives its execution, a fresh subagent per task. The isolated
  workspace is `worktree`, reviewing and landing the result is `ship`, the pull request is
  `branch-pr`.
