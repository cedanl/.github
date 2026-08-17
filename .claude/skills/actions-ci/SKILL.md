---
name: actions-ci
description: Author and debug GitHub Actions workflows, automated tests, and CI pipelines the CEDA way. Covers the reusable-workflow orchestration pattern, the uv + matrix test setup, object-store (MinIO/S3/SURF) integration jobs, security scanning (bandit/semgrep/codeql/sonarcloud), and release/publish. Use when adding or fixing a workflow, test job, object-store CI, or pipeline in a GitHub repo.
---

# actions-ci

CEDA GitHub repos use uv-based Python CI. There are **two generations** — match
the one the repo already uses rather than mixing them.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/actions-ci`, or
automatically) when you add or fix a GitHub Actions workflow, a test job, a
coverage/security-scan step, or a release workflow in a CEDA GitHub repo. It is
reference/convention, not a step-by-step procedure. For the GitLab config repos,
use /gitlab-ci instead.

## Which generation is this repo on?
- **Modern / orchestrated** (e.g. `1cijferho`): a thin `ci.yml` that calls
  reusable workflows via `uses: ./.github/workflows/<name>.yml` + `workflow_call`.
  Uses `ruff` (blocking), `uv sync --group dev`, and a security suite. Prefer this
  for new/serious repos.
- **Legacy quartet** (e.g. `eencijfer`, `minio-file`, `sdp-tools`):
  `dev.yml` / `preview.yml` / `release.yml` / `test.yml`, `uv pip install -e ".[dev,test]"`,
  flake8/black/isort/mypy run **non-blocking** (`|| true`), Codecov upload.
  Extend in place; don't rewrite to the modern style unless asked.

## Conventions that hold across both
- **uv** for everything: `astral-sh/setup-uv`, `actions/setup-python@v5`,
  Python **3.13** on modern repos (matrix 3.9–3.12 + multi-OS on legacy).
- Triggers: `push`/`pull_request` on `main` (modern also scans `feat/**`,`fix/**`).
- `actions/checkout@v4`; `fetch-depth: 0` when a tool needs full history (Sonar).
- **Windows in the matrix** matters here — past pain with `ErrorActionPreference`
  and Scoop writing to **stderr** (treat stderr as non-fatal unless exit code≠0).
- Env `PYTHONUTF8: "1"` on Windows jobs.

## Reusable workflow pattern (modern)
- A leaf workflow declares `on: workflow_call:` and does one thing (unit tests,
  a MinIO integration run, a pipeline config).
- `ci.yml` wires them as jobs with `uses: ./.github/workflows/<leaf>.yml`.
- Add a new check = new leaf workflow + one `uses:` line in `ci.yml`.
- A workflow under `tests/eencijferho/` is auto-collected by the unit job — no CI
  edit needed to add a test file there.

## Tests & coverage
- `uv run pytest tests/... --cov=<import_name> --cov-report=xml` (cov target is
  the **package import name**, not a filesystem path).
- Integration tests needing services: start MinIO via `docker run`, Postgres via
  a `services:` container; install extras with `uv sync --group dev --extra minio --extra postgres`.
- Merge unit+integration coverage with `--cov-append` before uploading to Sonar/Codecov.
- See /gate for reading a failing SonarCloud/CodeQL gate.

## Object-store backends in CI (MinIO stand-in + real SURF)
When a repo has a pluggable object-store backend (`STORAGE_BACKEND=minio|s3`,
S3-compatible), CI runs the integration suite against a **MinIO container as an
S3 stand-in** — same S3 API, no VPN, no secrets. A real-SURF job is kept
**separate and secret-gated**, because of a hard network boundary (below).
- **MinIO-as-S3 leaf** (e.g. `s3.yml`): `docker run` MinIO, then
  `uv sync --group dev --extra s3 --extra minio`. The `--extra minio` is needed
  even for the boto3/`s3` backend when `conftest.py` guards the whole integration
  dir with a module-level `import minio` (skips the dir if absent). Point the
  suite at it with `S3_TEST_ENDPOINT`/`S3_TEST_ACCESS_KEY`/… and path-style
  addressing (`S3_TEST_PATH_STYLE=true`) — RADOS-Gateway/MinIO need path-style.
- **Real-SURF leaf** (e.g. `s3-surf.yml`): a `check-secrets` job gates on a
  `SURF_S3_*` secret being present, so it no-ops on forks and when unconfigured.
  Trigger on `push: [main]` + `workflow_dispatch` only (secret-bearing) — not on
  arbitrary branches, and never from fork PRs (secrets are withheld there).
- **VPN gotcha (important):** GitHub-hosted runners have a public cloud IP and no
  VPN, so they **cannot reach a VPN/firewall-gated store** like
  `objectstore.surf.nl` → `EndpointConnectionError` after a long hang. Two
  consequences: (1) give the S3 client a short `connect_timeout` + capped
  `retries` (`max_attempts` ~2) so it fails in ~30s instead of hanging for hours;
  (2) **document in the repo + PR that CI does not test against the real store**
  for this reason — verify the real backend locally (from inside the VPN) instead.
- **Least-privilege CI creds:** never a root key. Use the root/admin key once to
  mint a non-root, S3-only IAM user + a dedicated CI bucket, store *that* user's
  key as the secret. See /objectstore-onboarding for the account/profile setup and
  provisioning the working profile.

## Security scanning (modern repos)
- **bandit** (`bandit[sarif]`, `--severity-level medium`), **semgrep**, **codeql**,
  **sonarcloud** — each uploads SARIF via `github/codeql-action/upload-sarif@v3`
  with a distinct `category`. Dependabot for deps.
- Scan steps are typically non-blocking on findings but surface results in the
  Security tab.

## Release / publish (legacy quartet)
- `release.yml` triggers on `v*` tags → PyPI **trusted publishing**
  (`permissions: id-token: write`, `environment: pypi`). No stored token.

## Debugging CI
- `unset GITHUB_TOKEN && gh run list/view/watch` to inspect runs (an invalid
  `$GITHUB_TOKEN` can shadow the `gh` login, so prefix `gh` with `unset GITHUB_TOKEN &&`).
- Reproduce failures locally where possible before pushing fix-attempts — avoid
  guess-and-check CI loops. Verify a fix actually resolves the failure before
  calling it done.
- Heavy Polars tests can segfault under local x86/Rosetta emulation — that's the
  dev machine, not CI (native runners are fine).

## GitLab note
The `*-config` GitOps repos use **GitLab CI** (`.gitlab-ci.yml`, reusable
`.gitlab/*.yaml` with `spec.inputs`), not Actions — see /surf-sdp-helm-flux and /gitlab-ci.
Don't apply Actions patterns there.

## Important
- **Match the repo's existing generation** (modern orchestrated vs legacy
  quartet); don't rewrite one style into the other unless asked.
- This skill covers **GitHub Actions only** — it does NOT apply to the GitLab
  config repos (use /gitlab-ci there).
- Reproduce CI failures locally where possible; avoid guess-and-check loops.
- **gh auth**: prefix `gh` with `unset GITHUB_TOKEN &&` (an invalid token may
  shadow the login).
- Applies to cedanl repos.
