---
name: pypi-project
description: Set up or publish a CEDA Python package to PyPI the house way — src-layout + setuptools + uv, PEP 621 pyproject metadata, and GitHub Actions Trusted Publishing (OIDC) on v* tags with a TestPyPI preview. Use when making a repo pip-installable, adding a release workflow, or cutting a PyPI release.
---

# pypi-project

Package and publish a Python project matching the modern CEDA convention
(`1cijferho`/`eencijferho`). Read the target repo's existing `pyproject.toml`
first and match it; don't invent a different toolchain.

## Toolchain (modern house style)
- **Build backend:** setuptools. **Env/deps:** uv. **Layout:** `src/<pkg>/`.
- **Publishing:** GitHub Actions + **Trusted Publishing (OIDC)** — no API tokens
  stored anywhere.

## pyproject.toml shape
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "<dist-name>"            # may differ from import name (e.g. eencijferho)
version = "0.1.0"
description = "..."
readme = "README.md"
requires-python = ">=3.12,<3.14"
license = {text = "MIT"}
authors = [{name = "CEDA", email = "info@cedanl.nl"}]
keywords = [...]
classifiers = [...]             # Dev Status, Intended Audience, License, Py versions, Topic
dependencies = [...]

[project.urls]                  # Homepage, Documentation, Repository, Issues (github.com/cedanl/...)

[project.optional-dependencies] # feature extras, e.g. frontend / minio / postgres
[project.scripts]               # console entry point, e.g. <name> = "<pkg>.cli:main"

[dependency-groups]
dev = ["pytest>=9.0.2", "pytest-cov>=6.0"]

[tool.setuptools.packages.find]
where = ["src"]
include = ["<pkg>*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```
Notes: dist name and import name can differ. Use `requires-python` with an upper
bound. Extras for optional features; a `[project.scripts]` entry if there's a CLI.

## Release workflow (modern: pypi-publish.yml)
Trigger on version tags; three jobs, each `needs:` the previous:
1. **test** — `uv sync --group dev` + `uv run pytest`.
2. **build** — `pip install build` + `python -m build`, upload `dist/` as an
   artifact (`persist-credentials: false` on checkout).
3. **publish-to-pypi** — `if: startsWith(github.ref, 'refs/tags/')`,
   `environment: {name: pypi, url: https://pypi.org/project/<name>/}`,
   `permissions: id-token: write`, download the artifact, then
   `pypa/gh-action-pypi-publish@release/v1`.
```yaml
on:
  push:
    tags: ['v*.*.*']
```
- The `pypi` GitHub **environment** gates publish behind **manual approval**.
- Trusted Publishing must be configured once in PyPI (publisher = this
  repo/workflow/environment `pypi`). Flag this to the user — it's a one-time
  PyPI-side setup you can't do from code.

## TestPyPI preview (preview.yml)
Publish dev builds to **TestPyPI** on push to main / `workflow_dispatch`:
`environment: test-pypi`, `id-token: write`, and
`pypa/gh-action-pypi-publish@release/v1` with
`repository-url: https://test.pypi.org/legacy/`. Bump to a `-dev.N` version so
each build is unique.

## Cutting a release
1. Bump `version` in `pyproject.toml` (repo may have a "bump versie naar vX" commit convention).
2. Verify locally: `uv build` then `uv run twine check dist/*` (twine check is the
   legacy-repo habit; keep it).
3. Commit, then tag `vX.Y.Z` and push the tag — the workflow runs; approve the
   `pypi` environment when prompted.
4. Confirm the release on PyPI; don't call it "published" until the run + approval
   complete. See the principle of verifying work actually runs before calling it done.

## Related
CI matrix / test conventions: [[actions-ci]]. gh auth: the gh auth note (an invalid $GITHUB_TOKEN can shadow the gh login; prefix gh commands with `unset GITHUB_TOKEN &&`).
Legacy quartet repos (`eencijfer`,`minio-file`,`sdp-tools`) use poetry+tox in
`preview.yml`/`release.yml` — match the repo you're in rather than converting.
