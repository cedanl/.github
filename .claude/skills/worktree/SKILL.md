---
name: worktree
description: Zet een geïsoleerde werkplek op voordat er iets geschreven wordt — detecteert eerst of je er al in zit, gebruikt daarna het native worktree-mechanisme en pas als laatste git, en zet er een CEDA-branchnaam op. Gebruik bij "worktree", "aparte branch", "los van main werken", of voordat je aan een issue begint. LET OP — voor het afronden en pushen is er `ship`, voor de PR `branch-pr`.
allowed-tools: Read Grep Glob Bash AskUserQuestion
license: MIT — afgeleid van superpowers (© 2025 Jesse Vincent)
compatibility: Requires git 2.5+; a native worktree tool is used when the harness provides one
metadata:
  ceda-id: ceda.worktree
  ceda-version: "0.1.0"
  ceda-type: workflow
  ceda-subtype: ""
  ceda-origin: extended
  ceda-upstream: superpowers:using-git-worktrees
  ceda-source: https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/SKILL.md
  ceda-activation: command
  ceda-binding: default
  ceda-execution: inline
  ceda-scope: org
  ceda-verifies: measurable
---

# Worktree

Ensure the work happens in an isolated workspace, on its own branch, **before** the first
write. Moving changes into a worktree afterwards is manual, error-prone work; creating the
worktree first costs one command.

Derived from `superpowers:using-git-worktrees` (MIT, © 2025 Jesse Vincent). Changed for CEDA:
branch naming, project setup for the uv/R stack, and Dutch user-facing output.

## Workflow

When the user invokes `/worktree [optional: issue number or short description]`:

### 1. Detect existing isolation

**Check this before creating anything.** A worktree inside a worktree is the most common
failure here.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
git rev-parse --show-superproject-working-tree 2>/dev/null   # non-empty = submodule
```

`GIT_DIR != GIT_COMMON` **and** the submodule check is empty → you are already in a linked
worktree. Skip to step 4. Report in Dutch:

> Je zit al geïsoleerd in `<pad>` op branch `<naam>`. Geen nieuwe worktree nodig.

At a detached HEAD, add that a branch still has to be created before finishing.

`GIT_DIR == GIT_COMMON`, or the submodule check returned a path → normal checkout, continue.

### 2. Ask consent, unless it is already given

Did the user ask for a worktree, or do the project instructions require one before the first
write? Then do not ask — that consent already exists. Otherwise:

> Zal ik een aparte worktree opzetten? Dan blijft je huidige branch onaangeraakt.

If the user declines, work in place and skip to step 4. "Op main" is a valid answer.

### 3. Determine the branch name, then create the workspace

CEDA branch naming:

| Situation | Name |
|---|---|
| There is an issue | `issue-<nr>-<slug>` |
| A fix without an issue | `fix-<slug>` |

The slug is lowercase, hyphenated, three or four words at most. No issue number and no idea
what the work is? Then this skill is too early — the work is not defined yet.

#### 3a. Native tool first

Do you have a worktree tool from the harness — something named `EnterWorktree`, a
`/worktree` command, a `--worktree` flag? Use it, with the branch name from the table, and go
to step 4.

This ordering is not cosmetic. `git worktree add` while a native tool exists produces
worktrees the harness does not know about, does not show, and does not clean up.

#### 3b. Git fallback

Only when there is no native tool.

Directory, in this order: an explicit preference from the user or the project instructions;
otherwise an existing `.worktrees/` (wins) or `worktrees/`; otherwise `.worktrees/` at the
repository root.

A project-local directory **must** be ignored before you create anything in it, otherwise the
worktree contents end up in `git status` and eventually in a commit:

```bash
git check-ignore -q .worktrees || { echo ".worktrees/" >> .gitignore; git add .gitignore; git commit -m "chore: ignore .worktrees"; }
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"
```

Fails on a permission error? The sandbox blocked it. Say so, work in the current directory,
and continue with step 4 — do not retry with escalating flags.

### 4. Project setup

A fresh worktree has no dependencies installed. Detect and run what applies:

```bash
[ -f pyproject.toml ] && uv sync                      # CEDA default for Python
[ -f requirements.txt ] && [ ! -f pyproject.toml ] && uv pip install -r requirements.txt
[ -f DESCRIPTION ] && Rscript -e 'devtools::load_all()'
[ -f package.json ] && npm install                    # Slidev/Marp decks
```

No dependency file → skip this step, do not invent one.

### 5. Verify a clean baseline

Run the project's own test command (`uv run pytest`, `Rscript -e 'devtools::test()'`, whatever
the project instructions name).

Tests failing **before** you change anything is the whole point of this step: without it you
cannot tell your own breakage from what was already broken. Report the failures and ask
whether to continue or investigate first. Never silently continue.

No test suite at all? Say so in one line and continue.

### 6. Report

> Worktree klaar op `<volledig pad>`, branch `<naam>`.
> Baseline: `<N tests geslaagd>` / `<geen testsuite>` / `<N gefaald — doorgaan?>`
> Klaar om aan `<onderwerp>` te werken.

## Let op: al geïsoleerd zijn is de normale toestand, niet de uitzondering

Modern harnesses put a session in a worktree on their own. Step 1 exists because the failure it
prevents is invisible: a nested worktree looks like it works until the branches diverge and
neither the harness nor `git worktree list` shows what you expected.

The same holds for a submodule — `GIT_DIR != GIT_COMMON` is true there too, which is why the
submodule check is part of step 1 and not an afterthought.

## Verificatie

`ceda-verifies: measurable` — after this skill,

```bash
[ "$(cd "$(git rev-parse --git-dir)" && pwd -P)" != "$(cd "$(git rev-parse --git-common-dir)" && pwd -P)" ] && git branch --show-current
```

prints a branch name matching `issue-<nr>-<slug>` or `fix-<slug>`. When the user declined
isolation, this check does not apply and the report says so explicitly.

## Important

- Never create a worktree when step 1 detects existing isolation, and never use
  `git worktree add` when a native worktree tool exists. Both produce state nobody can see.
- Never create a project-local worktree directory that is not ignored.
- This skill only opens the workspace. Finishing it — review, commit, push — is `ship`;
  opening the pull request is `branch-pr`.
