---
name: release-notes
description: Draft release notes in Dutch from merged PRs and closed issues since the last tag, then create a GitHub Release. Use before publishing a new version or when preparing a release.
---

# Release Notes

Draft release notes in Dutch based on real GitHub data (merged PRs + closed issues since the last tag), then create a GitHub Release draft.

## Workflow

When the user invokes `/release-notes [optional: version]`:

### 1. Determine the version

- If the user passed a version (e.g. `/release-notes 0.2.0`), use that.
- Otherwise, read `VERSION` from repo root: `cat VERSION`
- Confirm with the user before continuing.

### 2. Find the previous tag

```bash
gh release list --limit 5
```

Note the most recent tag (e.g. `v0.1.2`). All PRs and issues since that release are candidates for the notes.

If there are no previous releases, use the first commit as the baseline:

```bash
git log --oneline | tail -1
```

### 3. Fetch merged PRs since last tag

```bash
# Get the date of the last release
LAST_RELEASE_DATE=$(gh release view <last-tag> --json publishedAt --jq '.publishedAt')

# Fetch merged PRs since then
gh pr list --state merged --json number,title,body,mergedAt,author,labels \
  --jq "[.[] | select(.mergedAt > \"$LAST_RELEASE_DATE\")]"
```

For each PR, collect: number, title, body (first paragraph), author, labels.

### 4. Fetch closed issues since last tag

```bash
gh issue list --state closed --json number,title,closedAt,labels \
  --jq "[.[] | select(.closedAt > \"$LAST_RELEASE_DATE\")]"
```

**Exclude** issues that were closed without a linked PR (e.g. duplicates, won't-fix). Look for issues referenced in PR bodies via `Closes #N` or `Fixes #N`.

### 5. Classify changes

Map each PR/issue to a category based on its title prefix or labels:

| Prefix / label | Categorie |
|---|---|
| `feat:` / `feature` label | Nieuw |
| `fix:` / `bug` label | Opgelost |
| `refactor:` | Verbeterd |
| `docs:` / `documentation` label | Documentatie |
| `chore:`, `ci:`, `test:` | Intern |

- Items with no clear prefix: use context from the title to assign a category.
- `chore` / `ci` / `test` items go under **Intern** — these are typically not user-facing and can be collapsed or omitted from the main notes.

### 6. Draft the release notes in Dutch

Use this structure (matches existing CEDA releases like v0.1.1 and v0.1.2):

```markdown
### <Thematische kop — één zin die de kern van deze release beschrijft>

<2-3 zinnen die uitleggen wat er veranderd is en waarom het relevant is voor de gebruiker.>

#### Nieuw
- <beschrijving> (#PR-nummer)

#### Opgelost
- <beschrijving> (#PR-nummer)

#### Verbeterd
- <beschrijving> (#PR-nummer)

#### Documentatie
- <beschrijving> (#PR-nummer)

#### Intern
<details>
<summary>Technische wijzigingen</summary>

- <beschrijving> (#PR-nummer)

</details>
```

**Writing guidelines:**
- Write for the end user, not the developer — explain *what changed* and *why it matters*, not implementation details.
- Use plain Dutch. No jargon. No GitHub slugs in prose.
- Keep bullets short (max one line each).
- For the release title, follow the pattern: `<Projectnaam> v<version> – <Korte thematische beschrijving>` (e.g. `1CijferHO v0.1.3 – Snellere verwerking en betere foutmeldingen`)
- If a section has no items, omit it entirely.

### 7. Show the draft for review

Present the draft release notes and title to the user:

```
## Draft release notes: <Projectnaam> v<version>

**Titel:** <release title>

---
<notes>
---

Ziet dit er goed uit? Dan maak ik de GitHub Release aan.
```

Wait for confirmation before publishing.

### 8. Create the GitHub Release

Once confirmed:

```bash
gh release create v<version> \
  --title "<release title>" \
  --notes "<release notes>" \
  --draft
```

Always create as `--draft` first so the user can review it on GitHub before publishing. Tell the user:

> "Release draft aangemaakt: https://github.com/cedanl/<repo>/releases — controleer en publiceer wanneer je klaar bent."

If the user explicitly says to publish immediately, add `--latest` and omit `--draft`.

### 9. (Optional) Tag if not yet tagged

If `v<version>` tag does not exist yet:

```bash
git tag v<version>
git push origin v<version>
```

Ask the user before pushing the tag, as this triggers the PyPI publish workflow if `/publish-pypi` has been set up.

## Notes

- If the repo uses `/publish-pypi`, tagging is what triggers the publish — coordinate the order: finish the release notes draft, then tag + push, then publish the GitHub Release draft.
- Always verify the version in `VERSION` and `pyproject.toml` matches the tag before releasing.
- If there are no merged PRs (e.g. direct commits to main), fall back to `git log v<last-tag>..HEAD --oneline` and classify commits manually using the same table above.
