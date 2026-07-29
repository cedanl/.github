---
name: branch-pr
description: Open a new PR or finalize an existing one — assess the diff vs main, draft a real title and body, fill in the repo's PR template instead of leaving it blank, and handle the gh auth quirk. Use when creating a PR or turning a WIP/draft into a review-ready PR.
---

# branch-pr

Create or finalize a PR properly — no blank template bodies, no WIP left in the title.

## Workflow

When the user invokes `/branch-pr [optional: PR number]`:

1. Understand the change set:
   - `git log main..HEAD --oneline` and `git diff main...HEAD --stat`
   - Check for an existing PR: `unset GITHUB_TOKEN && gh pr list --head {branch} --state all`
2. If a repo PR template exists (`.github/pull_request_template.md` or the body
   GitHub pre-fills), FILL IT IN — don't submit the raw template. Cover: type of
   change, description (bullet the real changes), testing instructions, deps.
3. Draft a concise title (<70 chars), no "WIP". Details go in the body.
4. Write the body to a temp file to avoid shell-quoting issues with apostrophes:
   `gh pr create --base main --head {branch} --title "..." --body-file /tmp/pr_body.md`
   or `gh pr edit {n} --title "..." --body-file /tmp/pr_body.md` to finalize.
5. Return the PR URL.

## Important
- Dutch is fine for the body if the team uses it.
- Be honest in testing instructions about what's automated vs manual.
- Flag deployment caveats (e.g. "init.sql only runs on a fresh volume").
- **Never submit the raw/blank PR template** and never leave "WIP" in the title.
- **gh auth**: prefix every `gh` command with `unset GITHUB_TOKEN &&` (an invalid
  `$GITHUB_TOKEN` may shadow the login). If `gh auth status` fails, stop and ask
  the user to re-auth rather than working around it.
- Applies to cedanl repos.
