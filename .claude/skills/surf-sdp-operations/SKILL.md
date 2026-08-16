---
name: surf-sdp-operations
description: >-
  Reference guide for SURF SDP operations — tenant lifecycle, multi-environment
  patterns, kubectl access via kubelogin + OIDC, glab CLI for GitLab, database
  access via kubectl exec, and common workflows. Use when working on SDP tenants,
  asking about kubectl setup, glab authentication, database access, OIDC login,
  or referencing docs/scripts from glab-surf.
---

# SURF SDP Operations Handbook

Consolidated reference for operating SURF SDP tenants: tenant provisioning,
multi-environment GitLab/Kubernetes patterns, credential management (OIDC,
kubelogin), direct database access, and common troubleshooting workflows.

## When this applies

This is a **knowledge skill** — it loads automatically whenever you work on
SURF SDP repos (cedar/voxpop/other cedanl tenants), ask about kubectl setup,
glab authentication, tenant provisioning, or reference operational docs. It is
reference/convention, not a step-by-step procedure. Use `/surf-sdp-operations`
explicitly for a full runbook, or read relevant sections inline as needed.

## Tenant Lifecycle Overview

### Phases

| Phase | Who | Duration | Output |
|-------|-----|----------|--------|
| **Request** | Developer (Backstage form) | 1 day | Tenant namespace, Flux config, environments (dev/test/staging/prod) |
| **GitLab setup** | Developer (Terraform in gitlab-config) | 1–2 hours | App repo + config repo (via CI) |
| **kubeconfig + OIDC** | Developer (kubelogin, SURFconext login) | 15 min | Kubeconfig with OIDC token issuer |
| **App scaffold** | Developer (copy from template, customize) | 1–2 hours | Charts/, manifests/, CI/CD wired up |
| **Deploy to test** | CI/CD (GitLab pipeline) | 10–20 min | Pod running in test namespace |
| **Promote to staging** | CI/CD (same pipeline, env selector) | 10–20 min | Pod running in staging |
| **Promote to production** | CI/CD (protected-branch approval) | 10–20 min | Pod running in production |

### Tenant namespace naming

- **Namespace:** `services-<tenant>` (e.g., `services-voxpop`, `services-ceda-app`)
- **Helm release:** `<tenant>` or `<tenant>-<component>` (e.g., `voxpop`, `voxpop-migrations`)
- **GitLab project:** under `git.ia.surf.nl/surf-internal/npuls/ceda/<tenant>`
- **Flux Kustomization:** `<tenant>-sync` (watches the config repo for `manifests/<env>` changes)

### Config repo structure (standard)

```
charts/<tenant>/
  Chart.yaml              # app name, version (overwritten in CI)
  values.yaml             # chart defaults
  templates/
    deployment.yaml
    service.yaml
    ...

manifests/
  base/
    kustomization.yaml    # base overlays, Flux resources
    values-base.yaml      # shared values for all environments
    helmrelease.yaml      # Flux HelmRelease (pulls chart from Harbor)
    helmrepo.yaml         # Harbor OCI repository credentials
  development/
    kustomization.yaml    # patch: namespace, values-dev
    values.yaml
  test/
    kustomization.yaml
    values.yaml
  staging/
    kustomization.yaml
    values.yaml
  production/
    kustomization.yaml
    values.yaml

.gitlab-ci.yml            # Pipeline: build → chart:package → deploy:verify
.gitlab/                  # CI artifacts, scripts
```

Key pattern: **base + per-env overlays**, each with its own `values.yaml`. The Flux
Kustomization in `flux-system` namespace patches base for each environment.

## Kubectl Access: kubelogin + SURFconext OIDC

### Setup (one-time, per machine)

**1. Install kubelogin:**

```bash
# macOS
brew install kubelogin

# Linux
curl -sSLo kubelogin.tar.gz \
  "https://github.com/int128/kubelogin/releases/download/v1.29.0/kubelogin_linux_amd64.tar.gz"
tar -xzf kubelogin.tar.gz -C ~/.local/bin/
```

**2. Get your kubeconfig:**

Contact SDP platform team; they'll provide a kubeconfig with OIDC issuer pre-configured.

**3. Login (interactive):**

```bash
# First time: opens browser, you log in to SURFconext
kubectl oidc_login get-token

# Subsequent uses: token is cached; only re-auth if expired
kubectx development
kubectl get pods
```

### In devcontainers (special setup)

Devcontainers don't have interactive terminal flow; use the `authcode-keyboard` login:

```bash
# In devcontainer's Dockerfile or post-create script:
echo 'export KUBELOGIN_FLOW=authcode-keyboard' >> ~/.bashrc

# Then at runtime:
kubectl oidc_login get-token
# Follow the keyboard prompt (no browser)
```

### Troubleshooting kubelogin

| Error | Fix |
|-------|-----|
| "OIDC config not found" | Kubeconfig is missing `exec` block with OIDC issuer; get updated kubeconfig from platform team |
| "audience claim" mismatch | Kubeconfig audience doesn't match SURFconext app registration; platform team to fix |
| "browser didn't open" (in devcontainer) | Set `KUBELOGIN_FLOW=authcode-keyboard` and follow the keyboard prompt |
| Token expired | Run `kubectl oidc_login get-token` again; tokens are cached locally |

## glab Authentication & Common Queries

### Setup

```bash
# Login to git.ia.surf.nl (one-time)
glab auth login --hostname git.ia.surf.nl

# Prompted for:
# 1. Protocol: https
# 2. Token: generate at https://git.ia.surf.nl/-/user_settings/personal_access_tokens
#    (scopes: api, write_repository)
# 3. Git auth: yes

# Verify
glab auth status
```

### Common queries (for inventory/debugging)

```bash
# List all groups you belong to
glab api --hostname git.ia.surf.nl "/groups" | jq '.[] | {id, name, path}'

# List all projects in a group
glab api --hostname git.ia.surf.nl "/groups/4/projects" | jq '.[] | {id, name, path_with_namespace}'

# Get open MRs in a project
glab api --hostname git.ia.surf.nl "/projects/5388/merge_requests?state=opened" | jq '.[] | {iid, title, web_url}'

# Get pipeline status
glab api --hostname git.ia.surf.nl "/projects/5388/pipelines?per_page=5&order_by=id&sort=desc" | jq '.[] | {id, status, ref}'

# Get environments
glab api --hostname git.ia.surf.nl "/projects/5388/environments" | jq '.[] | {id, name, state}'
```

**Note:** Always use `--hostname git.ia.surf.nl` to avoid falling back to gitlab.com.

### Troubleshooting glab

| Error | Fix |
|-------|-----|
| "404 Project Not Found" | glab defaulted to gitlab.com; run `glab config set host git.ia.surf.nl` |
| "401 Unauthorized" | Token expired; regenerate at personal_access_tokens; re-run `glab auth login` |
| Missing scopes | Token doesn't have `api` + `write_repository`; regenerate with correct scopes |

## Multi-Environment Database Access (PostgreSQL, MinIO)

### PostgreSQL via kubectl exec

No client binary needed on host — run queries inside a pod container:

```bash
# Get connection URI from secrets
kubectl -n services-<app> get secret <app>-db -o jsonpath='{.data.uri}' | base64 -d

# Or manually query:
kubectl exec -it deploy/<app> -n services-<app> -- \
  psql "postgresql://user:pass@postgres.default/dbname" \
  -c "SELECT COUNT(*) FROM table_name;"

# Using Node.js + psql in a container (reusable pattern):
kubectl run -it --rm psql-client --image=node:18 --restart=Never -- \
  npm install pg && node -e "
    const pg = require('pg');
    const client = new pg.Client('postgresql://...');
    client.connect();
    client.query('SELECT 1', (err, res) => { console.log(res.rows); process.exit(); });
  "
```

### MinIO access (S3 compatible)

```bash
# Get credentials
kubectl -n services-<app> get secret <app>-minio -o jsonpath='{.data.accessKey}' | base64 -d
kubectl -n services-<app> get secret <app>-minio -o jsonpath='{.data.secretKey}' | base64 -d

# Use via AWS CLI (s3 compatible)
aws s3 --endpoint-url https://minio.sdp.surf.nl \
  ls s3://bucket-name/

# Or mount into a pod and access directly (depends on networking)
```

## Common Operational Patterns

### Port-forward to a service (read-only debug)

```bash
kubectl port-forward -n services-<app> svc/<app> 8080:8080
# Then access http://localhost:8080
```

### Get logs from a deployment

```bash
# Stream logs
kubectl logs -n services-<app> deploy/<app> --tail=50 -f

# From a specific container (if multi-container pods)
kubectl logs -n services-<app> deploy/<app> -c <container-name>

# Previous pod (if it crashed)
kubectl logs -n services-<app> deploy/<app> --previous
```

### Check pod resource usage

```bash
kubectl top pods -n services-<app>
kubectl top nodes
```

### Watch deployment progress

```bash
kubectl rollout status deploy/<app> -n services-<app>
kubectl rollout history deploy/<app> -n services-<app>
kubectl describe deploy/<app> -n services-<app>  # events
```

### List all resources in a namespace

```bash
kubectl get all -n services-<app>
kubectl get event -n services-<app> --sort-by='.lastTimestamp' | tail -20
```

## SOPS & Secrets Management

### Setup (per repository)

```bash
# Generate AGE key (once per repo)
age-keygen -o ~/.config/sops/age/keys.txt
AGE_PUBLIC_KEY=$(age-keygen -l ~/.config/sops/age/keys.txt | cut -d' ' -f3)

# Create .sops.yaml in repo root
cat > .sops.yaml <<EOF
creation_rules:
  - age: $AGE_PUBLIC_KEY
    encrypted_regex: '^(data|stringData)$'
EOF

# Initialize a secret
sops -e -i secrets/development-secrets.yaml
```

### Decrypt & view

```bash
sops -d secrets/development-secrets.yaml | grep PASSWORD
```

### Troubleshooting

See `/surf-kubectl-troubleshoot` symptom 4 (SOPS secret won't decrypt) for common issues.

## Flux CD Patterns

### Force reconciliation (when stuck)

```bash
# Using flux CLI (if available)
flux reconcile helmrelease <name> -n <namespace>

# Or kubectl fallback (always works)
kubectl annotate helmrelease <name> \
  reconcile.fluxcd.io/requestedAt="$(date +%s)" \
  -n <namespace> --overwrite
```

### Monitor reconciliation

```bash
# Watch Kustomizations
kubectl get kustomization -n flux-system -w

# Watch HelmReleases
kubectl get helmrelease -n services-<app> -w

# Check conditions
kubectl describe helmrelease <name> -n services-<app>
```

## Git Config Workarounds (devcontainers)

If `.gitconfig` is mounted read-only in a devcontainer:

```bash
# Use environment variable instead
export GIT_CONFIG_GLOBAL=~/.gitconfig-local

# Then add user config
git config --global user.name "Your Name"
git config --global user.email "you@surf.nl"
```

## GitLab Repos via Terraform (not UI)

**Important:** SDP repos cannot be created via the GitLab UI or API. They must be
declared in Terraform:

```bash
cd gitlab-config
git checkout -b create-<tenant>
# Edit terraform/npuls/ceda/main.tf:
module "<tenant>" {
  source = "../../modules/project"
  name   = "CEDA <Tenant>"
  path   = "<tenant>"
  ...
}
git add . && git commit && git push
# Open MR; SDP admins merge
```

See `/sdp-onboard` for the full flow.

## Per-Environment Value Merging (Helm + Kustomize)

**Important for debugging:** Helm values are merged in this order:

```
chart defaults (values.yaml)
  ↓
base overlay (manifests/base/values-base.yaml)
  ↓
per-env override (manifests/<env>/values.yaml)
```

Later files override earlier ones. If a value is missing, it falls through to the earlier layer.

**Preview the merged values:**

```bash
# For development environment
helm template <app> charts/<app> \
  -f charts/<app>/values.yaml \
  -f manifests/base/values-base.yaml \
  -f manifests/development/values.yaml \
  --namespace services-<app>
```

## Important

- **Never mutate a cluster by hand.** All changes go through GitLab CI → Flux.
- **Test environments first.** development → test → staging → production. Never production first.
- **Backup kubeconfig.** If OIDC token issuer changes, kubeconfig becomes invalid; get a new one from platform team.
- **SOPS keys are local.** Each developer must have their own AGE key in `~/.config/sops/age/keys.txt`. CI/CD uses a CI-specific key (stored in GitLab CI/CD variables).
- **Logs are transient.** Pod logs are lost when pods restart; set up persistent logging with your monitoring system.
- **Use kubectx for context switching.** `kubectx development` is faster and safer than `kubectl config use-context`.
- **This is a GitLab/SDP skill** — use `glab`, `kubectl`, `git`, not `gh`.
- **Applies to cedanl / SURF SDP repos.**

## See Also

- `/surf-sdp-helm-flux` — Helm packaging, Flux reconciliation, chart versioning
- `/surf-ingress-migration` — Kong → Traefik upgrade workflow
- `/surf-tenant-rename` — Coordinated multi-repo tenant rename
- `/surf-kubectl-troubleshoot` — Interactive diagnostics for common issues
