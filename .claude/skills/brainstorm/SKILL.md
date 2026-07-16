---
name: brainstorm
description: Structureer een brainstorm van idee naar getoetst besluit vóór implementatie, met een beslis-samenvatting en aanbevelingen — geen code of bestanden. Wanneer iemand een idee wil uitwerken of een besluit wil voorbereiden voordat er code of een plan komt.
---

# Brainstorm

Structured brainstorming from an idea to a tested decision, before any implementation or plan. The output is a decision summary with recommendations — never code, files, or commits. Respond to the user in Dutch, caveman-terse.

## Workflow

When the user invokes `/brainstorm [optioneel: onderwerp]`:

### Hard gate

Until an explicit go:

- No code, no files, no commits or pushes
- No scaffolding, no installing dependencies, no "quick POC"
- Do not start other skills or plan mode; the only follow-up after go is planning or building what was agreed

"Too simple to brainstorm" does not exist: for simple topics the summary is a few lines, but it always comes.

### Communication

Caveman-terse: no filler, no hedging, no politeness phrases; technically accurate. Start with the answer or recommendation, no build-up. Short is the default; no walls of headings, tables, or bullet lists unless asked or genuinely needed. No recap of what you just did. Assume no prior knowledge: explain in plain language; steps numbered and one at a time. In doubt short or long: short.

### 1. Context first

Before asserting anything, read the relevant files, docs, and recent commits. Whatever is stated there does not become a question.

### 2. Scope check

Multiple independent parts are fine.

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

## Important

- Building starts only after an explicit go; the only follow-up is planning or building what was agreed.
- All user-facing output is in Dutch; keep it terse and recommendation-first.
- Avoid the anti-patterns: working through a checklist of questions; asking what you can read yourself; premature constraints (narrowing the solution before the problem is clear); reopening locked decisions; listing options without a recommendation; multiple follow-ups without priority (one primary suggestion, alternatives secondary).
