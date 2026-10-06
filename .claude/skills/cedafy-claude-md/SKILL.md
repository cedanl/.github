---
name: cedafy-claude-md
description: Past de CEDA-baseline voor projectinstructies toe op een repo die er al een heeft — vult aan wat ontbreekt, laat staan wat al gedekt is, en legt elke tegenstrijdigheid als keuze voor in plaats van te overschrijven. Gebruik bij "projectinstructies bijwerken", "CEDA-conform maken" of "sessie-afspraken toevoegen". LET OP — bij een nieuwe repo doet `init-repo` dit al.
allowed-tools: Read Write Edit Grep Glob Bash AskUserQuestion
compatibility: Requires the gh CLI to fetch the template from cedanl/.github
metadata:
  ceda-id: ceda.cedafy-claude-md
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: own
  ceda-upstream: ""
  ceda-source: werkafspraken/_claude-md-template.md
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: observable
---

# Cedafy CLAUDE.md

Bring an existing repository's `CLAUDE.md` in line with the CEDA baseline without throwing away
what the repository already decided for itself. Insert and adjust, never replace.

Is there no `CLAUDE.md` yet? Then this is a fill-in job: take the template, fill in the
`<...>` slots from step 2, write it, done. The rest of this skill is about the harder case.

## Workflow

When the user invokes `/cedafy-claude-md [optional: path to the repository]`:

### 1. Read both sides

The template lives in `cedanl/.github`, not in the repository you are working in:

```bash
gh api repos/cedanl/.github/contents/werkafspraken/_claude-md-template.md --jq .content | base64 -d
```

`gh` must run outside the sandbox here, and `unset GITHUB_TOKEN` first — see `branch-pr`.

Then read the repository's own `CLAUDE.md`, in full. Not a grep for headings: the point of this
skill is judging what the existing text *means*, and a heading does not tell you that.

### 2. Read the repository, for the slots

The template has `<...>` slots. Fill them from the repository itself, not from assumptions:

| Slot | Where it comes from |
|---|---|
| Stack, language version | `pyproject.toml`, `DESCRIPTION`, `package.json` |
| Package manager | a `uv.lock`, `renv.lock`, `package-lock.json` |
| Run, test, lint commands | the scripts in that same file, the CI workflow, the README |

Cannot find a command? Leave the slot empty and say so at the end. An invented test command is
worse than a missing one — it fails in a session where nobody expects it.

### 3. Classify every template point

Three buckets. Do this per point, not per section, because one section can be half covered.

| Bucket | Meaning |
|---|---|
| *ontbreekt* | The current `CLAUDE.md` does not say this at all |
| *al gedekt* | The current text says the same thing in different words |
| *tegenstrijdig* | The current text says something else |

What counts as contradictory:

| Current `CLAUDE.md` | Template | Bucket |
|---|---|---|
| "werk gewoon op main" | worktree before the first write | tegenstrijdig |
| "draai altijd de volledige suite" | one targeted test file | tegenstrijdig |
| "vraag altijd eerst om bevestiging" | brainstorm before building | al gedekt |
| an own commit flow with extra steps | no counterpart in the template | repo-eigen, leave alone |

**A doubtful case counts as contradictory**, so it becomes a question. One question too many
beats an agreement that is silently overwritten — the user wrote that line for a reason you
cannot see from here.

### 4. Insert what is missing, leave what is covered

*Ontbreekt* → insert directly, in the template's wording. Do not ask; that is the whole point
of the skill.

*Al gedekt* → do nothing. A second line saying the same thing in other words makes the file
longer and the instruction weaker.

### 5. Put every contradiction to the user

Per contradictory point, three options via the choice menu:

1. follow the template
2. keep the current line
3. combine — **with the proposed combined text in the option itself**, so the choice is
   concrete instead of a promise

Four questions per call at most, so batch them. Do not ask them one at a time in chat: this is
a fixed set of answers, and a menu is faster and yields better answers than an open question.

### 6. Write and report

Process the answers, leave repo-specific sections untouched, and write the file. Then report,
in Dutch:

> **Bijgewerkt:** `CLAUDE.md`
> - Toegevoegd: <points>
> - Overgeslagen omdat het al gedekt was: <points>
> - Jouw keuze: <point> → <chosen>
> - Slots die ik niet kon invullen: <slots, or "geen">

## Let op: de volgorde van het bestaande bestand blijft staan

The temptation is to rewrite the file into the template's order — it reads better and the diff
looks clean. Do not. Someone put those sections in that order, and a reordering diff hides
which lines actually changed in the review. Insert at the place where the point belongs in the
existing structure, and add a section at the end only when there is no such place.

## Verificatie

`ceda-verifies: observable` — done when all three hold, checked against the diff:

- every repo-specific section from before is still present, in the same order
- every point classified as *tegenstrijdig* has a user decision behind it, none silently
  overwritten
- no point appears twice, once in the template's words and once in the repository's

## Important

- Never remove a repo-specific section, and never rewrite the file into the template's order.
  Insert and adjust, not replace.
- Every contradiction goes to the user. A doubtful case is a contradiction.
- The reverse direction — noticing that a repo-specific rule actually belongs in the org
  template — is out of scope. That needs a view of every `CLAUDE.md` at once and belongs with
  repo-context-as-data.
- For a repository that has no `CLAUDE.md` because it is brand new, `init-repo` writes the
  template as part of the scaffold.
