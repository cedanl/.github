---
name: ship
description: The review-fix-commit-push loop with guardrails — verify the change actually works before claiming done, check git state after branch operations, and commit with conventional messages. Use when finishing a piece of work that needs to land on a branch.
---

# ship

Land a change safely. Verify the work actually runs before calling it done.

## Guardrails (the point of this skill)
- **Verify before "done".** Run the tests. For UI/browser changes that can't be
  tested headless, SAY SO explicitly and ask for confirmation of the behavior —
  never claim a UI change works without evidence. Distinguish "static checks
  pass" from "feature verified".
- **Check git state after checkouts/rebases.** After `git checkout`/`switch`/
  rebase, run `git status` and confirm no unintended staged changes (a checkout
  can silently stage reverting changes). Reconcile local vs remote before
  committing.
- **Never commit stray files.** Stage specific paths by name, not `git add -A` —
  this avoids sweeping in local build artifacts, reports, or editor junk
  (`coverage.xml`, generated HTML, etc.).

## Steps
1. Make the change.
2. Run the relevant tests + linter (`uv run pytest ...`, `uvx ruff check ...`).
   Note: heavy Polars tests may segfault locally under x86/Rosetta emulation —
   that's environmental, not a code failure; CI runners are native and fine.
3. Verify behavior for anything user-facing; be explicit about coverage gaps.
4. Review the diff. Stage only intended files by name.
5. Commit with a conventional message (`fix:`/`feat:`/`test:`/`ci:` ...); body
   in Dutch is fine. If the team convention is to attribute AI-assisted commits,
   add a trailing `Co-Authored-By: Claude <noreply@anthropic.com>` line.
6. Push. If it involves a PR, consider `/pr-reply` or `/branch-pr` next.

## Auth
Prefix `gh` with `unset GITHUB_TOKEN &&` (invalid token may shadow the login).
