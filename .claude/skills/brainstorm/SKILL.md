---
name: brainstorm
description: Structureer een brainstorm van idee naar getoetst besluit vóór implementatie, en leg dat besluit na de go vast als document dat het plan daarna kan lezen — geen code. Wanneer iemand een idee wil uitwerken of een besluit wil voorbereiden voordat er code of een plan komt. LET OP — ná de go hoort `plan`, niet dit.
allowed-tools: Read Write Grep Glob Bash AskUserQuestion Skill
license: MIT — afgeleid van superpowers (© 2025 Jesse Vincent)
metadata:
  ceda-id: ceda.brainstorm
  ceda-version: "0.2.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: extended
  ceda-upstream: superpowers:brainstorming
  ceda-source: https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Brainstorm

Structured brainstorming from an idea to a tested decision, before any implementation or plan. The output is a decision summary with recommendations — never code. Respond to the user in Dutch, caveman-terse.

Shares its spine with `superpowers:brainstorming` (MIT, © 2025 Jesse Vincent). Changed for
CEDA: Dutch and caveman-terse, assumptions-first with confidence levels instead of a question
round, and the summary lands in `docs/specs/` as the input for `/plan`. Which parts of upstream
are deliberately not here, and why: [`.claude/skills/README.md`](../README.md).

## Workflow

When the user invokes `/brainstorm [optioneel: onderwerp]`:

Create a todo per numbered step below and work them off in order. Steps that do not
apply — no real choice in step 4, for instance — you close with one line saying why.
The todo list is what keeps the gate from being skipped on a topic that feels simple.

### Hard gate

Until an explicit go:

- No code, no files, no commits or pushes
- No scaffolding, no installing dependencies, no "quick POC"
- Do not start other skills or plan mode; the only follow-up after go is planning or building what was agreed

The go lifts the gate for exactly one file: the decision summary from step 7. Nothing else
gets written, ever, by this skill.

"Too simple to brainstorm" does not exist: for simple topics the summary is a few lines, but it always comes.

### Communication

Caveman-terse: no filler, no hedging, no politeness phrases; technically accurate. Start with the answer or recommendation, no build-up. Short is the default; no walls of headings, tables, or bullet lists unless asked or genuinely needed. No recap of what you just did. Assume no prior knowledge: explain in plain language; steps numbered and one at a time. In doubt short or long: short.

### 1. Context first

Before asserting anything, read the relevant files, docs, and recent commits. Whatever is stated there does not become a question.

### 2. Scope check

Does the idea cover several independent subsystems — parts that could be built, tested and
used without each other? Say so before you ask anything else, and decompose first: name the
parts, say how they relate, propose an order. Then brainstorm the first part through the rest
of this workflow. Each part gets its own summary and its own `/plan`.

Do not spend questions on the details of something that has to be split anyway. `plan` splits
the same way (one plan per subsystem); deciding it here saves the round trip.

### 3. Assumptions first

No questionnaire. Analyse first, then present assumptions where the user only has to correct. Per assumption: what (with file reference), evidence, what breaks if it is wrong, confidence (Zeker / Waarschijnlijk / Onzeker). Ask only when something is genuinely not derivable or confidence is Onzeker; then one question per turn, multiple-choice where possible, no checklist grind. Problem first, solution space after.

### 4. Explore approaches

When there is real choice: 2-3 approaches with trade-offs. **Recommendation always up front**, with a reason that references evidence in the repo or earlier decisions. YAGNI: actively cut features and frills from each proposal.

### 5. Present the design in parts

Present the worked-out idea in parts, scaled to complexity (a few sentences to a short section). Check after each part whether it holds. Do not reopen locked decisions.

### 6. Self-review

Walk through the outcome yourself: contradictions, vagueness, ambiguity, gaps. Fix inline.

### 7. Decision summary

```markdown
## Brainstorm: [onderwerp]

### Beslissingen (locked)
### Aannames (met confidence)
### Open
### Deferred
### Volgende stap
Go? Dan [plan maken / bouwen wat hierboven staat].
```

Wait for an explicit go. On corrections: adjust, self-review again, present again.

### 8. Write the summary down

Only after the go. Save the same summary — unchanged, plus a `# <onderwerp>` heading and the
date — to `docs/specs/YYYY-MM-DD-<onderwerp>.md` and commit it.

This is not bookkeeping. `plan` reads this file: it needs a decision that was already made,
and after a context reset, a new session, or a `/worktree` in between, the chat summary is
gone. Whatever is not in the file does not reach the plan.

Does the repo have no `docs/specs/` yet? Then propose creating it — one line, with the path
you intend to use — and create it once the user agrees. Say no, and the summary stays in the
chat; then also say what that costs: `plan` has no input and the decision has to be repeated
by hand.

### 9. Hand over

The brainstorm ends here; it does not turn into building. Two routes:

| Scope of what was agreed | Next step |
|---|---|
| Multiple steps or multiple files | `/plan` on the spec — write the implementation plan first |
| The diff fits in one sentence | Build it directly, no plan |

Say which one it is and why in one line. Close with the literal command, path filled in, so
the user can copy it or say go:

> Besluit staat in `docs/specs/2026-08-15-<onderwerp>.md`. Meerdere bestanden, dus eerst een
> plan:
>
> ```
> /plan docs/specs/2026-08-15-<onderwerp>.md
> ```
>
> Zal ik dat draaien?

Do not ask the user to choose between planning and building when the criterion above already
decides it — the only question is whether you start now.

## Verificatie

`ceda-verifies: observable` — the brainstorm is done when the decision summary exists as a
file and a reader who was not part of this conversation can tell from it what was decided,
what is an assumption, and what the next step is. Concretely: `docs/specs/<datum>-<onderwerp>.md`
is committed, every locked decision in the chat is in it, and it names `/plan` or the one-line
build as the follow-up.

## Important

- Building starts only after an explicit go; the only follow-up is `/plan` or building what
  was agreed. The one file this skill writes is the summary in `docs/specs/`, and only after
  the go.
- All user-facing output is in Dutch; keep it terse and recommendation-first.
- Avoid the anti-patterns: working through a checklist of questions; asking what you can read yourself; premature constraints (narrowing the solution before the problem is clear); reopening locked decisions; listing options without a recommendation; multiple follow-ups without priority (one primary suggestion, alternatives secondary).
