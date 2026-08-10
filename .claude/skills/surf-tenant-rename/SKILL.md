---
name: surf-tenant-rename
description: >-
  Rename a SURF SDP tenant across all Git repos, Kubernetes namespaces, CI/CD
  pipelines, and secrets vaults with a coordinated multi-repo checklist. Use when
  a tenant changes its name (e.g., project codename → product name), or the user
  mentions refactoring tenant identifiers across repos.
---

# SURF SDP Tenant Rename Orchestration

Rename a tenant (e.g., `savvy` → `voxpop`, `codename-project` → `product-name`)
across all its Git repositories, Kubernetes namespaces, Helm values, CI/CD
pipelines, and SOPS encryption keys. This is a **multi-system coordinated
change** — execute the checklist step-by-step to avoid breaking deployments.

A real case study: `savvy` → `voxpop` rename (2026-05-XX) involved 5 repos,
3 namespaces, and 15+ files. This skill ensures no step is missed.

## Workflow

When the user invokes `/surf-tenant-rename [old-name] [new-name]`, walk through
the checklist below:

### Phase 1: Planning & Validation

**Ask the user:**
1. Which repos does this tenant own? (list them: app repo, config repo, any shared repos)
2. Which Kubernetes namespaces? (typically `services-<tenant>`)
3. Does the tenant use SOPS encryption? Which AGE keys are involved?
4. Which environments need the rename? (dev/test/staging/prod, or all)
5. Are there any downstream repos that reference this tenant? (other apps' Helm charts, pipelines)

**Validation checklist:**
- [ ] All repos are cloned and up-to-date (`git fetch origin`)
- [ ] No uncommitted changes or WIP branches in any repo
- [ ] User has push access to all repos
- [ ] User has kubectl access to all target namespaces (read-only is OK for now)
- [ ] User has SOPS/AGE access if tenant uses encrypted secrets

### Phase 2: Database & Secrets

Execute in this order (these must be done early, before renaming repos):

**2a. SOPS AGE key renaming (if applicable)**

SOPS keys are stored per-repo under `.sops.yaml` and reference tenant namespaces.
If tenant name appears in AGE key identifiers, rotate them:

```bash
# In each config repo with SOPS setup:
grep -r "<old-name>" .sops.yaml
# If no match, skip this step.
# If match, rotate the AGE key:
sops -d secrets/<old-name>-secrets.yaml > /tmp/secrets-backup.yaml
# Update .sops.yaml with new key
age-keygen -o age-new-key.txt
# Re-encrypt with new key
sops -d /tmp/secrets-backup.yaml | sops -e -f secrets/<new-name>-secrets.yaml /dev/stdin
```

**2b. Database credentials (if applicable)**

If tenant owns a database (PostgreSQL, MongoDB), credentials may be stored as
Kubernetes secrets or in a vault. Flag these for manual rotation after the rename:

```bash
kubectl -n services-<old-name> get secrets | grep -E "(password|uri|credentials)"
# Document these; they'll need to be re-encrypted/rotated after step 4
```

### Phase 3: Git Repository Renames (coordinated)

Rename repos in this order to avoid circular references:

**3a. App repository** (code repo, if separate from config)

```bash
cd <app-repo>
# Rename locally (no git command; just plan the changes)
# Update references in CI files, README, package.json, etc.
grep -r "<old-name>" . | grep -v ".git" | head -20
# Manually edit files to replace old-name → new-name
# Examples: package.json name field, Dockerfile labels, CI variable names

git add .
git commit -m "refactor: rename tenant identifier <old-name> → <new-name>

- Update package/module names
- Update Docker image labels
- Update CI variable references
- No logic changes; rename only

Related: tenant consolidation"

git push origin feat/rename-<old-name>-<new-name>
```

Open MR, request review (tenant admin + platform team).

**3b. Config/manifests repository** (Helm charts, Flux, K8s manifests)

This is the heavy one — namespace names, Helm release names, and values all
reference the tenant:

```bash
cd <config-repo>
git checkout -b feat/rename-<old-name>-<new-name>

# Find all references
grep -r "<old-name>" . | grep -v ".git" | tee /tmp/rename-refs.txt

# Update in three sections:

# Section 1: Kubernetes manifests
# - manifests/base/kustomization.yaml: namespace, Flux resource names
# - manifests/<env>/kustomization.yaml: patch overlays
sed -i 's/<old-name>/<new-name>/g' manifests/*/kustomization.yaml
sed -i 's/<old-name>/<new-name>/g' manifests/base/kustomization.yaml

# Section 2: Helm chart names and values
# - charts/<old-name>/ → charts/<new-name>/
git mv charts/<old-name> charts/<new-name>
sed -i 's/<old-name>/<new-name>/g' charts/<new-name>/Chart.yaml
sed -i 's/<old-name>/<new-name>/g' charts/<new-name>/values.yaml

# Section 3: Flux resources (HelmRelease, HelmRepository, Kustomization)
sed -i 's/<old-name>/<new-name>/g' manifests/base/helmrelease.yaml
sed -i 's/<old-name>/<new-name>/g' manifests/base/kustomization.yaml

# Section 4: CI/CD (.gitlab-ci.yml, environment names)
sed -i 's/<old-name>/<new-name>/g' .gitlab-ci.yml

# Section 5: Documentation
sed -i 's/<old-name>/<new-name>/g' README.md docs/*.md

git add .
git commit -m "refactor: rename tenant <old-name> → <new-name>

- Rename Kubernetes namespaces in manifests/*/kustomization.yaml
- Rename Helm chart directories and values
- Rename Flux resources (HelmRelease, HelmRepository)
- Rename CI/CD variables and environments
- Update documentation

Related: tenant consolidation"

git push origin feat/rename-<old-name>-<new-name>
```

Open MR. Request review from platform team (this must be merged before step 4).

**3c. Shared infrastructure repos (if applicable)**

If the tenant is referenced in a shared infra repo (`kubernetes-clusters`,
`gitlab-config`, SDP platform repos), update there too:

```bash
cd <shared-infra-repo>
git checkout -b feat/rename-<old-name>-<new-name>
grep -r "<old-name>" terraform/ docs/
# Edit Terraform module blocks, TF variables, documentation
git add . && git commit -m "infra: rename tenant <old-name> → <new-name>" && git push
```

**Merge order:** App repo → Config repo → Shared infra. Wait for CI to pass on each.

### Phase 4: Kubernetes Namespace Rename (destructive — coordinated cutover)

Once all MRs are merged, perform the namespace rename on each cluster. **This is
the point of no return** — all services must be redeployed to the new namespace.

**For each environment (development first, production last):**

```bash
kubectx <env>

# 4a. Create the new namespace with the same setup
kubectl create namespace services-<new-name>
kubectl config set-context --current --namespace=services-<new-name>

# 4b. Copy secrets from old namespace (they'll be re-encrypted post-deployment)
kubectl get secrets -n services-<old-name> -o yaml | \
  sed "s/namespace: services-<old-name>/namespace: services-<new-name>/g" | \
  kubectl apply -n services-<new-name> -f -

# 4c. Reconcile Flux on the new namespace
# (The Flux Kustomization now points to the new namespace via the merged config repo)
kubectl delete kustomization <old-name>-sync -n flux-system
# Flux will auto-create the new one from the updated GitLab repo
kubectl get kustomization -n flux-system | grep <new-name>
# Wait 1-2 minutes for initial sync

# 4d. Monitor Flux reconciliation
kubectl get kustomization -n flux-system -w
# Watch until Status=Reconciling or Ready, no errors

# 4e. Verify deployment
kubectl get pods -n services-<new-name>
kubectl describe helmrelease <new-name> -n services-<new-name>
# Check conditions; should show Ready=True

# 4f. Verify application connectivity
kubectl get svc -n services-<new-name>
curl -v http://<app-service>:8080/healthz -n services-<new-name>

# 4g. Only after verification: delete old namespace
kubectl delete namespace services-<old-name>
```

### Phase 5: Post-Deployment Verification (all environments)

After step 4 is complete on all environments:

**5a. End-to-end connectivity**

```bash
# Test each environment
for env in development test staging production; do
  kubectx $env
  curl -v https://<app>.$env.sdp.surf.nl/healthz
  echo "✓ $env OK"
done
```

**5b. Pipeline verification**

Trigger a new build in the GitLab pipeline:
- A test commit to main should deploy to all environments
- Verify deployment versions match the new namespace

**5c. Audit logs**

Check GitLab audit logs and Kubernetes audit logs for successful namespace operations:
```bash
# GitLab
glab api --hostname git.ia.surf.nl "/events" | jq '.[] | {created_at, action, resource_type}'

# Kubernetes
kubectl logs -n kube-system -l component=audit | grep services-<new-name>
```

### Phase 6: Cleanup

Once verification is complete:

**6a. Delete old Git branches**

```bash
for repo in <app-repo> <config-repo> <shared-infra-repo>; do
  cd $repo
  git branch -d feat/rename-<old-name>-<new-name>
  git push origin --delete feat/rename-<old-name>-<new-name>
done
```

**6b. Rotate secrets (if applicable)**

Secrets that were copied in step 4b should be rotated to use new encryption keys.
Coordinate with platform team:
- Re-encrypt SOPS secrets with new AGE keys
- Rotate database credentials
- Rotate API tokens

**6c. Update documentation and runbooks**

Any playbooks, operational docs, or team wikis that reference the old tenant name
should be updated.

### 7. Bevestig en voer uit

Summarize the rename plan:

> **Tenant rename: `<old-name>` → `<new-name>`**
>
> **Scope:**
> - Repos: [list]
> - Namespaces: [list]
> - Environments: [list]
> - Uses SOPS: [yes/no]
>
> **Phases:**
> 1. Planning & validation
> 2. Database & secrets (manual)
> 3. Git repo renames (3 coordinated MRs)
> 4. Kubernetes namespace rename (production cutover)
> 5. Verification (end-to-end tests)
> 6. Cleanup (branch deletion, secret rotation)
>
> **Timeline:** 2–3 hours total (mostly waiting for Flux reconciliation)
>
> **Risk:** High — namespace rename is destructive. Rollback requires manual
> restoration from backups. Ensure step 5 verification before proceeding to cleanup.
>
> Ready to start Phase 1 (planning)?

Wait for the user to confirm. If they identify issues, adjust and re-confirm.

## Important

- **Execute phases in order.** Skipping or reordering steps can lead to inconsistent state.
- **Merge all MRs before step 4.** The Kubernetes cutover depends on the config repo changes.
- **Test environments first (development → test).** Production is last. Never rename production first.
- **Namespace rename is destructive.** Rollback requires manual Kubernetes backup restoration.
  Ensure verification (step 5) is thorough before deleting the old namespace.
- **Secrets are copied, not migrated.** After the rename, rotate secrets to use new encryption keys.
- **Watch Flux reconciliation carefully.** If HelmRelease shows errors, check the config repo MR for syntax issues.
- This is a **GitLab/SDP** skill — use `glab`, `kubectl`, `git`, not `gh`.
- Applies to cedanl / SURF SDP repos.
