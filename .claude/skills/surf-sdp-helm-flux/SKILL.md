---
name: surf-sdp-helm-flux
description: >-
  Deploy and troubleshoot Helm/Flux workloads on the SURF SDP platform
  (GitLab CI → OCI chart in Harbor cr.surf.nl → FluxCD HelmRelease).
  Use this skill whenever the user works on GitLab CI pipelines that package
  or deploy Helm charts, debugs a failing or stuck HelmRelease, sees Flux
  reconciliation problems, hits 401/404 errors pulling charts from an OCI
  registry, encounters chart version mismatches in deploy verification, sets
  up cross-pipeline triggers, works on a Kubernetes CronJob or on-demand Job Helm
  template for scheduled/triggered batch runs, or mentions SDP, Harbor,
  cr.surf.nl, FluxCD, HelmRepository, or HelmRelease — even if they only paste a
  pipeline log or kubectl output without an explicit question.
---

# SURF SDP Helm/Flux Deployment Conventions

How deployments work on the SURF SDP (Kubernetes) platform, and how to
diagnose them when they don't. Read this fully before proposing fixes to a
pipeline log or Flux error someone pastes — most failures here are known
patterns with known one-line fixes, and generic Helm/Flux advice wastes time.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/surf-sdp-helm-flux`,
or automatically) whenever you work on GitLab CI that packages/deploys Helm
charts, debug a stuck/failing HelmRelease, hit 401/404 pulling charts from
Harbor OCI, see Flux reconciliation problems, or paste a pipeline log / kubectl
output. It is reference + troubleshooting, not a procedure to run.

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

**Blanket rule: always set `secretRef.namespace: flux-system` explicitly.**
The Harbor credentials secret lives in the `flux-system` namespace, not in
the tenant namespace. A `secretRef` without `namespace:` defaults to the
HelmRepository's own namespace, so Flux fails authentication and you get a
plain 404 on the registry API (`GET /v2/.../tags/list` → 404) — which looks
exactly like "chart doesn't exist." Check the secretRef namespace before
chasing the chart path:

```yaml
spec:
  interval: 1m
  provider: generic
  secretRef:
    name: sdp-harbor-credentials
    namespace: flux-system   # ← required; secret lives in flux-system
  type: oci
  url: oci://cr.surf.nl/<project>/<chart>
```

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

## Deployment is fine but the pipeline/ingress fails

Several failures look like the deployment broke when the HelmRelease is
actually healthy. Establish the HelmRelease state *before* acting on any of
these.

### `kubernetes:verify-up` fails on every run — known false-negative

**Symptom:** `kubernetes:verify-up` fails with `Kubernetes namespace  does
not exist` (note the double space — the namespace variable resolved to
empty) on every single pipeline run, regardless of whether the deploy
succeeded. `diff`, `dry-run`, `helm:publish`, `docker:docker-build` are all
green.

**Cause:** the component's namespace variable isn't set for the job — a
defect in the component wiring, not in your deployment. It has no relation
to whether the HelmRelease reached Ready.

**Action:** don't chase it. Verify deployment state directly:
```bash
kubectl get helmrelease <name> -n <ns>   # Ready=True?
kubectl get kustomization -n flux-system  # Ready=True?
```
Optionally give the job `allow_failure: true`, or set the missing namespace
variable, so it stops being a red herring on every pipeline.

### `kubernetes:diff` fails — ENVIRONMENT_NAME vs ENVIRONMENT_CLUSTER

**Symptom:** `Environment 'development', does not have Flux Resource or
Kubernetes namespace.` You *did* configure the environment.

**Cause:** the workspace sets `ENVIRONMENT_CLUSTER` (the logical cluster
name, e.g. `development`) but the Flux components look up the environment by
its *provisioned* GitLab name (which may differ, e.g. `odw-chat-development`).

**Fix:** set both variables in `workflow.rules`, mapping the logical cluster
to the provisioned environment name:
```yaml
workflow:
  rules:
    - if: $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH
      variables:
        ENVIRONMENT_CLUSTER: "development"
        ENVIRONMENT_NAME: "odw-chat-development"   # must match provisioned env
```

### Ingress instant 404 despite healthy pod (middleware annotation)

**Symptom:** `curl https://<app>.<env>.sdp.surf.nl/` returns an instant
`404 page not found` (Go's `http.NotFound`) — not a timeout. Pod/Service
are healthy (verify with a debug pod curling the Service inside the
namespace).

**Cause:** the Ingress's `traefik.ingress.kubernetes.io/router.middlewares`
annotation references a Middleware Traefik can't resolve — misnamed,
never created (only applied ad-hoc, not committed to `manifests/`), or it
is a *platform-injected* middleware (e.g. `infra-traefik-<class>-global-ratelimit`,
auto-added by the platform's admission webhook) that doesn't exist on that
specific cluster. Same-namespace refs use the short object name — Traefik
computes the `<namespace>-<name>@kubernetescrd` prefix itself:
```bash
kubectl get ingress <name> -n services-<app> -o jsonpath='{.metadata.annotations.traefik\.ingress\.kubernetes\.io/router\.middlewares}'
```
**Isolate** by stripping the annotation entirely:
```bash
kubectl annotate ingress <name> -n services-<app> traefik.ingress.kubernetes.io/router.middlewares-
```
If the route then resolves, the middleware chain was the fault. A missing
platform-provided middleware is a platform-side gap — report it; you have
no RBAC to inspect/confirm the injected middleware (`kubectl get middleware
-n infra-traefik-internal` → `Forbidden`).

### Cross-namespace ingress 504 / hang (NetworkPolicy block)

**Symptom:** `curl https://<app>.<env>.sdp.surf.nl/` hangs and 504s after
~30s. Pod is `1/1 Running`, HelmRelease Ready, Service endpoints healthy,
and `kubectl port-forward` to the pod works fine. The 504 only happens via
the real ingress URL. TLS handshake completes (Traefik answers) but the
backend never responds.

**Cause:** SDP enforces cross-namespace default-deny (Cilium). Traefik runs
in `infra-traefik-external`/`infra-traefik-internal`, your app in
`services-<app>` — the hop between them is silently dropped. Tenants have
**no RBAC** over Cilium's own CRDs (`kubectl auth can-i create
ciliumnetworkpolicies -n services-<app>` → no), but standard
`networking.k8s.io/v1` `NetworkPolicy` is allowed and is purely additive —
an allow rule can never make things more restrictive.

**Self-service fix:** commit a namespaced `NetworkPolicy` allowing ingress
from the Traefik namespaces (GitOps-tracked so Flux doesn't prune it):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: <app>-allow-traefik-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: infra-traefik-external
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: infra-traefik-internal
      ports:
        - protocol: TCP
          port: <container-port>
```
An **egress-only** policy (`policyTypes: [Egress]`) does NOT cause or fix
this — it has no bearing on inbound traffic. The rule must be `Ingress`.

### Container startup `ModuleNotFoundError` — Dockerfile COPY gap

**Symptom:** pod in CrashLoopBackOff; `kubectl logs --previous` shows
`ModuleNotFoundError: No module named 'core'` (or any app module) at import
time. The image built fine — it just misses runtime modules.

**Cause:** a Dockerfile `COPY` is missing app module directories, or the
build lacks a system package uv needs for git dependencies:
```dockerfile
COPY pyproject.toml uv.lock ./
COPY server.py ./
COPY core/ ./core/            # ← often omitted
COPY routes/ ./routes/
...
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev git   # ← git required when uv.lock has git deps
```
Fix the Dockerfile and push a new commit (new build number bypasses the
poisoned release).

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

## Batch workloads: scheduled CronJob + on-demand Job

ETL/ML steps run as batch workloads, not long-lived Deployments. The `instroom`
chart (`instroom-config/charts/instroom/templates/{etl,ml}/`) is the reference:
per service (`etlwo`, `etlho`, `ml`) it ships **two** templates, each gated by its
own `.Values.<svc>` flag:

- **`cron_<svc>.yaml`** — `kind: CronJob`, gated by `.Values.<svc>.cronJob.enabled`,
  with `schedule` (e.g. `"0 2 * * *"`), `concurrencyPolicy`, history limits and
  deadlines. This is the *scheduled* path.
- **`job_<svc>.yaml`** — `kind: Job`, gated by `.Values.<svc>.job.enabled`. This is
  the **on-demand** path: the pipeline flips `job.enabled=true` (via
  `HELM_UPGRADE_ARGS --set <svc>.job.enabled=true`, see cross-pipeline triggers
  above) and a fresh Job runs.

### On-demand = unique Job name per release

A plain `kind: Job` is immutable once created, so re-applying with the same name
does nothing. The chart makes each Helm release spawn a **new** Job by suffixing
the name with the release revision + random string:

```yaml
metadata:
  name: {{ include "instroom.fullname" . }}-<svc>-job-{{ .Release.Revision }}-{{ randAlphaNum 8 | lower }}
```

That is the whole "on-demand (unscheduled) cron job" mechanism from the notes:
a trigger → Helm upgrade → new revision → new Job name → it runs once.

### Both pull image by digest and env from the config/secret

The job containers select the image by `sha256:` digest when the tag is a digest
(same digest-not-tag rule as Deployments), and take MinIO/etc. config from the
Flux-managed ConfigMap + Secret (`envFrom` a `configMapRef`/`secretRef`, or
`valueFrom` on `existingConfigMap`/`existingSecret`). See `/sdp-secrets-management`
for where those come from.

### Known bugs in the reference chart (fix if you touch it)

The `instroom` templates have field errors worth correcting before reuse:

- **`cron_<svc>.yaml`** sets `successfulJobsHistoryLimit` **twice** (a duplicate
  YAML key — the second silently wins), and sets
  `ttlSecondsAfterFinished` from `activeDeadlineSeconds`, which conflates
  "how long the finished object lingers" with "how long the run may take". Set
  `ttlSecondsAfterFinished` from its own value — and keep it generous: the TTL
  deletes the Job **and its pods**, taking `kubectl logs` with them. A nightly ETL
  that fails at 02:00 under a short TTL has no logs left by morning, so allow at
  least a working day (or ship logs off-cluster).
- **`job_<svc>.yaml`** carries `successfulJobsHistoryLimit` /
  `failedJobsHistoryLimit` — these are **CronJob-only** fields and are invalid on
  a `kind: Job`. Drop them from the Job spec.

Validate any change with `helm template` / `kustomize build` (see *local preview*
above) before committing.

## Troubleshooting quick reference

| Symptom | Likely cause | First action |
|---|---|---|
| 401 pulling chart from cr.surf.nl | HelmRepository missing/wrong `secretRef` | `kubectl describe helmrepository <n> -n <ns>`; check secret exists |
| 404 / HEAD error for chart that exists | `+` vs `_` tag mismatch **or** secretRef without `namespace: flux-system` | `scripts/check-oci-tag.sh`; check secretRef namespace |
| HelmRepository has empty `Status:` | Never connected (auth/URL) | Fix secretRef/URL in source repo, reconcile source |
| Verify job: version mismatch + timeout | In progress **or** rolled back | `kubectl get hr <n> -n <ns>`; check for `UpgradeFailed` |
| HelmRelease stuck after failures | Remediation retries exhausted | New build, or `scripts/force-reconcile.sh` |
| `flux: unknown shorthand flag 'n'` | InfluxDB flux binary | Use kubectl annotate fallback |
| Protected-branch job never picked up | Runner missing Protected flag | GitLab Admin → Runners → Protected ✓ |
| Ingress `either defaultBackend or rules must be specified` | Component enabled with empty ingress values | Disable component or supply ingress host in values |
| verify-up fails with `Kubernetes namespace  does not exist` (double space) | Known false-negative: namespace variable empty | Don't trust it; verify HelmRelease status directly |
| Cross-namespace ingress 504 / hang, port-forward works | SDP default-deny NetworkPolicy blocks Traefik→app | Add namespaced `NetworkPolicy` allowing ingress from `infra-traefik-*` |
| Ingress instant 404 despite healthy pod | Traefik middleware annotation doesn't resolve | Strip the middleware annotation to isolate |
| `kubernetes:diff` "does not have Flux Resource or Kubernetes namespace" | ENVIRONMENT_NAME doesn't match provisioned env name | Map `ENVIRONMENT_CLUSTER` → actual env via `ENVIRONMENT_NAME` |

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

## Important
- **The pipeline never runs `helm upgrade` directly** — it pushes a chart and
  waits for Flux. Classify a "deploy problem" as (a) chart not published,
  (b) Flux can't fetch it, or (c) release fails — before acting.
- **Don't hand-edit Flux resources** (HelmRepository/HelmRelease) in-cluster —
  the next sync reverts them; fix the source repo instead.
- Check the `+`↔`_` OCI-tag spelling before assuming a chart is missing.
- Deploy by **image digest**, not floating tags.
- **Batch runs** = scheduled `CronJob` + on-demand `Job`; on-demand relies on a
  unique Job name per release (`{{ .Release.Revision }}-{{ randAlphaNum 8 }}`).
  The reference `instroom` chart has field bugs (duplicate
  `successfulJobsHistoryLimit`, wrong `ttlSecondsAfterFinished`, CronJob-only keys
  on a `Job`) — fix them if you reuse it.
- **`secretRef.namespace: flux-system` is mandatory** on HelmRepository — without
  it Flux auths in the wrong namespace and you get a 404 that looks like a
  missing chart.
- **`kubernetes:verify-up` has a known false-negative** (empty namespace var) —
  before acting on it, check the HelmRelease/Kustomization status directly.
- **Ingress 404 (instant) ≠ 504 (timeout):** instant 404 = middleware annotation
  that doesn't resolve; ~30s 504 with healthy pod = cross-namespace NetworkPolicy
  block. Add an `Ingress`-type namespaced `NetworkPolicy` for the Traefik
  namespaces; an egress-only policy won't fix inbound traffic.
- **ENVIRONMENT_NAME must map to the provisioned env name** when
  `ENVIRONMENT_CLUSTER` differs (see `kubernetes:diff` failures).
- This is a **GitLab/SDP** skill — use `glab`/kubectl, not `gh` or GitHub Actions.
- Applies to cedanl / SURF SDP repos.
