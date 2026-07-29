---
name: pr-reply
description: Fetch a PR's review comments, assess each on its merits, and post threaded replies (in Dutch) plus a summary comment citing the fixing commit, then re-request review. Use when a reviewer has left comments on a PR and you want to respond to all of them.
---

# pr-reply

Respond to review feedback on a GitHub PR, thoroughly and honestly.

## Workflow

When the user invokes `/pr-reply [optional: PR number]`:

1. Identify the PR (ask if ambiguous). Get the latest review + inline comments:
   - `unset GITHUB_TOKEN && gh api repos/{owner}/{repo}/pulls/{n}/comments --jq 'sort_by(.created_at) | .[] | {id, path, line, in_reply_to: .in_reply_to_id, body}'`
   - Also check `gh pr view {n} --json reviews` and issue comments.
   - Filter to comments newer than your last reply so you don't re-answer old ones.
2. For EACH comment, read the actual code at that path/line before responding.
   Assess it on merits — agree when right, push back with reasoning when not.
   Do not rubber-stamp. If a comment is "vanuit claude" (relayed AI analysis),
   still verify it against the real code.
3. Make the fixes (or hand off to `/ship`), commit, and note the commit SHA.
4. Post a THREADED reply under each comment:
   `unset GITHUB_TOKEN && gh api repos/{owner}/{repo}/pulls/{n}/comments/{comment_id}/replies -f body="..."`
   - Write replies in the team's working language (Dutch for CEDA).
   - Say what changed, why, and cite the commit SHA.
5. Post ONE summary comment tagging the reviewer, recapping each point + SHA:
   `unset GITHUB_TOKEN && gh pr comment {n} --body "@reviewer ..."`
6. Be honest about test coverage gaps (e.g. "regressiewachter, geen live-browsertest").

## Important

- Use the team's working language for all PR-facing text (Dutch for CEDA).
- Cite the specific commit that addresses each comment.
- **Never claim something is fixed without having verified it** — this skill does
  NOT rubber-stamp comments or mark them resolved on the author's behalf.
- **gh auth**: an invalid `$GITHUB_TOKEN` may shadow the real `gh` login — prefix
  every `gh` command with `unset GITHUB_TOKEN &&`. If `gh auth status` still fails,
  ask the user to re-auth; do NOT fall back to curl for authenticated endpoints.
- Applies to cedanl repos.
