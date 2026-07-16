---
name: surf-sdp-helm-flux
description: >-
  Conventions and troubleshooting for Helm/Flux deployments on the SURF SDP
  platform (GitLab CI → OCI chart in Harbor cr.surf.nl → FluxCD HelmRelease).
  Use this skill whenever the user works on GitLab CI pipelines that package
  or deploy Helm charts, debugs a failing or stuck HelmRelease, sees Flux
  reconciliation problems, hits 401/404 errors pulling charts from an OCI
  registry, encounters chart version mismatches in deploy verification, sets
  up cross-pipeline triggers, or mentions SDP, Harbor, cr.surf.nl, FluxCD,
  HelmRepository, or HelmRelease — even if they only paste a pipeline log or
  kubectl output without an explicit question.
---

# SURF SDP Helm/Flux Deployment Conventions

How deployments work on the SURF SDP (Kubernetes) platform, and how to
diagnose them when they don't. Read this fully before proposing fixes to a
pipeline log or Flux error someone pastes — most failures here are known
patterns with known one-line fixes, and generic Helm/Flux advice wastes time.

## Repo layout & local preview

Config repos share this layout:

```
charts/<app>/Chart.yaml
charts/<app>/values.yaml          # chart defaults
manifests/base/values-base.yaml   # shared base overlay + Flux helmrelease/helmrepo/kustomization
manifests/<env>/values.yaml       # per-env override (development/test/staging/playground/production)
manifests/<env>/kustomization.yaml
```

Environments are **directories under `manifests/`** (not a `values-<env>.yaml`
naming scheme); each env's `kustomization.yaml` patches base with its
`values.yaml`. A base-wide change goes in `manifests/base/values-base.yaml`; an
env-specific one in that env's file — don't cross them, and give `production`
extra scrutiny.

Preview what a change renders to **before committing** (never mutates a cluster):

```bash
helm template <release> charts/<app> \
  -f charts/<app>/values.yaml \
  -f manifests/base/values-base.yaml \
  -f manifests/<env>/values.yaml
# or, since Flux uses Kustomize overlays:
kustomize build manifests/<env>
```

## Architecture: how a change reaches the cluster

```
git push / tag
  → GitLab CI pipeline
      build:   container image → Harbor (cr.surf.nl)
      helm:package: chart version rewritten with yq, packaged,
                    pushed as OCI artifact → Harbor
  → FluxCD in the cluster
      Kustomization (flux-system) syncs tenant namespace
      HelmRepository (type: oci, secretRef to Harbor credentials)
      HelmRelease pulls the chart, installs/upgrades
  → pipeline verify job
      waits for HelmRelease Ready condition
      compares deployed chart version against expected version
```

Key properties of this setup:

- **The pipeline never runs `helm upgrade` against the cluster directly.**
  It pushes a chart and then *waits for Flux* to act. Any "deployment"
  problem is therefore really one of: (a) chart not published correctly,
  (b) Flux can't fetch it, or (c) Flux fetched it but the release fails.
  Establish which of the three it is before doing anything else.
- Chart versions carry semver build metadata tied to the commit:
  `0.0.4-rc.197+5545fff1` or `0.0.1-build.20+branch.f085e792`.
- Each tenant namespace gets its HelmRepository/HelmRelease from a
  Kustomization in `flux-system` (label
  `kustomize.toolkit.fluxcd.io/name=<tenant>-sync`). Hand-editing those
  resources gets reverted by the next sync — fix the source repo instead.

## Critical gotcha: `+` becomes `_` in OCI tags

Semver build metadata uses `+`, but `+` is not a valid character in OCI
tags. Harbor stores the chart under a tag with `_` instead:

- Chart version: `0.0.1-build.20+testminio.f085e792`
- Harbor tag:    `0.0.1-build.20_testminio.f085e792`

Helm and Flux translate this automatically *most of the time*, but when you
see a 404/"not found"/`unexpected status from HEAD request` for a chart you
are sure exists, check both spellings before anything else. When manually
verifying with `helm pull`, use the `_` form of the tag. The bundled
`scripts/check-oci-tag.sh` does this check for you.

A `401 Unauthorized` on chart pull is a different problem: the
HelmRepository is missing its `secretRef` (Harbor credentials, e.g.
`sdp-harbor-credentials`), or the referenced secret doesn't exist in the
tenant namespace. A HelmRepository with a completely **empty `Status:`
section and no events** in `kubectl describe` is the classic sign it never
successfully connected at all.

## Deploy verification: stuck vs. slow

The verify job fails with something like:

```
ERROR: Deployed Helm Chart has version: 0.0.4-rc.189+2bc7cc59, expected: 0.0.4-rc.197+5545fff1
error: timed out waiting for the condition on helmreleases/<name>
```

Do not immediately assume the deployment is broken. Two very different
causes produce this identical output:

1. **Still in progress.** Flux's upgrade action has its own timeout (often
   5m) and background migrations/jobs can exceed the pipeline's wait.
   Check: `kubectl get helmrelease <name> -n <ns>` — if the status shows
   `Running 'upgrade' action`, it is slow, not stuck. Retry the verify job
   after it settles.
2. **Flux gave up and rolled back.** After exhausting `remediation`
   retries, Flux rolls back to the last good release and *stops trying*.
   The deployed version will stay at the old build forever. Check the
   `history:` and `Released` condition in
   `kubectl describe helmrelease <name> -n <ns>` for `UpgradeFailed`.
   Recovery, in order of preference:
   - fix the underlying failure and push a new commit (new build number
     bypasses the poisoned release), or
   - force a retry: `scripts/force-reconcile.sh <helmrelease> <namespace>`, or
   - if it stays wedged: `flux suspend helmrelease <name> -n <ns>` followed
     by `flux resume ...`.

**Beware the wrong `flux` binary.** InfluxDB also ships a `flux` CLI (a
query language tool). If `flux reconcile` errors with
`unknown shorthand flag: 'n'` or the help output shows `fmt`/`test`
subcommands, that's the InfluxDB one. Don't chase flag syntax — use the
kubectl fallback, which always works:

```bash
kubectl annotate helmrelease <name> \
  reconcile.fluxcd.io/requestedAt="$(date +%s)" \
  -n <namespace> --overwrite
```

(`--overwrite` is required; the annotation usually already exists.)

## Pipeline conventions

### Chart packaging (`helm:package`)

Runs in the `quay.io/helmpack/chart-testing` image (Alpine — install extras
with `apk add --no-cache yq`). The chart version is rewritten from a
pipeline-computed `CHART_VERSION` before packaging:

```bash
export TARGET_VERSION="$CHART_VERSION"
yq eval -i '.version = strenv(TARGET_VERSION)' Chart.yaml
helm package --dependency-update .
```

Never hardcode a version in `Chart.yaml`; it is always overwritten in CI.

### Cross-pipeline triggers

Upstream (e.g. an ETL image build) triggers the config repo's pipeline and
hands over the exact image digest. Conventions:

- Downstream has a `trigger:receive` job that validates incoming variables
  and re-exports them via a **dotenv artifact** so later jobs can `needs:`
  it and inherit the values.
- Trigger routing uses two variables:
  `$CI_PIPELINE_SOURCE == "trigger"` and a `$TRIGGER_ACTION` value naming
  the component (e.g. `etl_wo`).
- Component-selective deploys pass overrides through `HELM_UPGRADE_ARGS`,
  always with `--reuse-values` so untouched components keep their config:

```yaml
etl-wo:deploy:
  stage: deploy
  variables:
    HELM_UPGRADE_ARGS: >-
      --set etlwoTransport.tag=$ETL_WO_IMAGE_DIGEST
      --set etl.job.enabled=true
      --set streamlit.enabled=false
      --reuse-values
  rules:
    - if: $CI_PIPELINE_SOURCE == "trigger" && $TRIGGER_ACTION == "etl_wo"
  needs:
    - trigger:receive
```

Deploy by **image digest**, not floating tags. `tag: latest` with
`pullPolicy: Always` is only acceptable as a temporary unblocking measure
in test namespaces — flag it as debt if you see it.

### Runners

Jobs on protected branches are silently ignored by a runner unless the
runner itself has the **Protected** flag set (Admin → Runners → edit →
Protected ✓). If a job stays "pending" with a runner that is online and
correctly tagged, check this flag before anything else — the symptom looks
exactly like a tagging problem but isn't.

## Troubleshooting quick reference

| Symptom | Likely cause | First action |
|---|---|---|
| 401 pulling chart from cr.surf.nl | HelmRepository missing/wrong `secretRef` | `kubectl describe helmrepository <n> -n <ns>`; check secret exists |
| 404 / HEAD error for chart that exists | `+` vs `_` tag mismatch | `scripts/check-oci-tag.sh` |
| HelmRepository has empty `Status:` | Never connected (auth/URL) | Fix secretRef/URL in source repo, reconcile source |
| Verify job: version mismatch + timeout | In progress **or** rolled back | `kubectl get hr <n> -n <ns>`; check for `UpgradeFailed` |
| HelmRelease stuck after failures | Remediation retries exhausted | New build, or `scripts/force-reconcile.sh` |
| `flux: unknown shorthand flag 'n'` | InfluxDB flux binary | Use kubectl annotate fallback |
| Protected-branch job never picked up | Runner missing Protected flag | GitLab Admin → Runners → Protected ✓ |
| Ingress `either defaultBackend or rules must be specified` | Component enabled with empty ingress values | Disable component or supply ingress host in values |

For the full diagnostic command runbook (describe/get/watch sequences,
suspend/resume, checking Kustomization sync, job log retrieval), read
`references/diagnostics.md`.

## Bundled scripts

- `scripts/force-reconcile.sh <helmrelease> <namespace>` — force a Flux
  retry using the flux CLI when available, kubectl annotate otherwise.
- `scripts/check-oci-tag.sh <oci-url> <chart-version>` — checks whether a
  chart version exists in the registry under the `+` and/or `_` tag form.
- `scripts/hr-status.sh <helmrelease> <namespace>` — one-shot health
  summary: HelmRelease conditions, history, HelmRepository status, recent
  jobs in the namespace.
