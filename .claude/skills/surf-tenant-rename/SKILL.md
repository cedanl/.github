---
name: surf-tenant-rename
description: >-
  Rename a SURF SDP tenant across kubernetes-clusters, GitLab environments, the
  app repo and gitlab-config (Terraform moved-blocks, Harbor kept), with a
  coordinated multi-repo checklist. Use when a tenant changes its name (e.g.,
  project codename → product name), or the user mentions refactoring tenant
  identifiers across repos.
---

# SURF SDP Tenant Rename Orchestration

Rename a tenant (e.g., `savvy` → `voxpop`, `codename-project` → `product-name`)
across all its Git repositories, Kubernetes namespaces, Helm values, CI/CD
pipelines, and SOPS encryption keys. This is a **multi-system coordinated
change** — execute the checklist step-by-step to avoid breaking deployments.

A real case study: `savvy` → `voxpop` rename (2026-05-XX) involved 5 repos,
3 namespaces, and 15+ files. This skill ensures no step is missed. The SDP
procedure in Phase 3 comes from that rename and the earlier `sumilearn` rename
(see Gotchas).

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
# Document these; they'll need to be re-encrypted/rotated after Phase 4
```

### Phase 3: SDP-procedure (volgorde)

Do the five steps in this order. Each step names the repo or system it touches;
wait for CI to pass on each MR before moving on.

**Harbor is never renamed.** The Harbor project keeps the old name
(`lifecycle { ignore_changes = [name] }` in `harbor.tf`). So every Harbor
reference — `image.repository`, `helmrepo.url` — keeps pointing at the **old**
Harbor project name, and a blanket `sed s/<old-name>/<new-name>/` must skip them.
The examples below skip lines that contain `harbor`; check the remaining Harbor
references by hand afterwards.

#### Step 1: kubernetes-clusters (MR)

Rename the tenant directory under `services/base/` and everything that points at it:

```bash
cd kubernetes-clusters
git checkout -b feat/rename-<old-name>-<new-name>
git mv services/base/<old-name> services/base/<new-name>

# Internal references: namespace, secrets, git URL, kustomizations
grep -rn "<old-name>" . --exclude-dir=.git | tee /tmp/rename-refs.txt
grep -rl "<old-name>" services/base/<new-name> | \
  xargs sed -i '/harbor/!s/<old-name>/<new-name>/g'

# Cluster kustomizations (development, testing, playground, ...) that list the tenant
grep -rln "services/base/<old-name>" . --exclude-dir=.git
# Edit each hit to services/base/<new-name>

git add . && git commit -m "refactor: rename tenant <old-name> → <new-name>"
git push origin feat/rename-<old-name>-<new-name>
```

Open the MR and request review from the platform team.

#### Step 2: GitLab environments (`kubernetes_namespace`, `flux_resource_path`)

GitLab environments are **not** updated automatically when the namespace changes.
For every environment of the app project, via the UI (Operate → Environments →
Edit) or the API:

- `kubernetes_namespace` → `services-<new-name>`
- `flux_resource_path` → the new path (same form as the current value, with the
  new tenant name)

```bash
glab api --hostname git.sdp.surf.nl "projects/<project-id>/environments" \
  | jq '.[] | {id, name, kubernetes_namespace, flux_resource_path}'

glab api --hostname git.sdp.surf.nl -X PUT \
  "projects/<project-id>/environments/<env-id>" \
  -f kubernetes_namespace=services-<new-name> \
  -f flux_resource_path=<new-flux-resource-path>
```

#### Step 3: App repo (Helm chart, templates, values, CI)

```bash
cd <app-repo>
git checkout -b feat/rename-<old-name>-<new-name>

# Helm chart directory
git mv charts/<old-name> charts/<new-name>

# Internal references in templates, values, CI — Harbor refs excluded
grep -rn "<old-name>" . --exclude-dir=.git
grep -rl "<old-name>" charts/<new-name> .gitlab-ci.yml README.md | \
  xargs sed -i '/harbor/!s/<old-name>/<new-name>/g'

# Check: image.repository and helmrepo.url still use the OLD Harbor project name
grep -rn -e "repository:" -e "helmrepo" charts/ .gitlab-ci.yml

git add . && git commit -m "refactor: rename tenant <old-name> → <new-name>

- Rename Helm chart directory, templates and values
- Update CI references
- Harbor references (image.repository, helmrepo.url) keep the old project name"
git push origin feat/rename-<old-name>-<new-name>
```

Do not touch the `HARBOR_PROJECT` CI variable: it is set automatically.

#### Step 4: gitlab-config (MR, Terraform `moved` blocks)

1. Rename the tenant's module in the right `main.tf`.
2. Add `moved` blocks in `terraform/moves.tf` for **all** resources of the
   module, Harbor resources included (project, retention, robot account, member
   groups). Without them Terraform plans a destroy + create.
3. After `terraform apply`, remove the `moved` blocks again (follow-up MR).

```hcl
# terraform/moves.tf — one block per resource address the plan wants to recreate
moved {
  from = module.<old-name>.<resource-address>
  to   = module.<new-name>.<resource-address>
}
```

Check the plan before merging: it must show moves only, no destroy of the
Harbor project or any other resource.

#### Step 5: Restore branch protection

If branch protection was switched off for direct pushes during the rename, switch
it back on in every repo where you did that:

```bash
glab api --hostname git.sdp.surf.nl "projects/<project-id>/protected_branches"
```

### Phase 4: Flux cutover (per environment)

The namespace `services-<new-name>` and its secrets are defined in
`services/base/<new-name>` (Step 1), so Flux creates them once the
kubernetes-clusters MR is merged. Do **not** create the namespace or copy
secrets by hand: Flux owns them, and manual objects conflict with what it applies.

**For each environment (development first, production last):**

```bash
kubectx <env>

# 4a. Monitor Flux reconciliation
kubectl get kustomization -n flux-system -w
# Watch until Ready, no errors

# 4b. Verify deployment
kubectl get pods -n services-<new-name>
kubectl describe helmrelease <new-name> -n services-<new-name>
# Check conditions; should show Ready=True

# 4c. Verify application connectivity
kubectl get svc -n services-<new-name>
curl -v http://<app-service>:8080/healthz -n services-<new-name>

# 4d. Only after verification: remove the old namespace if it still exists
kubectl get namespace services-<old-name>
kubectl delete namespace services-<old-name>
```

### Phase 5: Post-Deployment Verification (all environments)

After Phase 4 is complete on all environments:

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
for repo in kubernetes-clusters <app-repo> gitlab-config; do
  cd $repo
  git branch -d feat/rename-<old-name>-<new-name>
  git push origin --delete feat/rename-<old-name>-<new-name>
done
```

**6b. Rotate secrets (if applicable)**

Secrets under the renamed `services/base/<new-name>` keep their old values.
Coordinate rotation with the platform team:
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
> 3. SDP procedure: kubernetes-clusters MR → GitLab environments → app repo →
>    gitlab-config MR (moved blocks, removed after apply) → branch protection
> 4. Flux cutover per environment (development first, production last)
> 5. Verification (end-to-end tests)
> 6. Cleanup (branch deletion, secret rotation)
>
> **Timeline:** 2–3 hours total (mostly waiting for Flux reconciliation)
>
> **Risk:** High — the namespace changes. Rollback requires manual
> restoration from backups. Ensure Phase 5 verification before proceeding to cleanup.
>
> Ready to start Phase 1 (planning)?

Wait for the user to confirm. If they identify issues, adjust and re-confirm.

## Important

- **Execute phases and steps in order.** Phase 3 follows the SDP procedure:
  kubernetes-clusters → GitLab environments → app repo → gitlab-config → branch protection.
- **Merge all Phase 3 MRs before the Phase 4 cutover.** The cutover depends on the kubernetes-clusters changes.
- **Test environments first (development → test).** Production is last. Never rename production first.
- **Namespaces belong to Flux.** Do not create, copy into or delete Flux-managed
  namespaces by hand before verification (Phase 5) is thorough.
- **Secrets keep their values.** After the rename, rotate secrets to use new encryption keys.
- **Watch Flux reconciliation carefully.** If HelmRelease shows errors, check the kubernetes-clusters MR for syntax issues.
- This is a **GitLab/SDP** skill — use `glab`, `kubectl`, `git`, not `gh`.
- Applies to cedanl / SURF SDP repos.

## Gotchas

- **The Harbor project name does not change** — `lifecycle { ignore_changes = [name] }`
  in `harbor.tf`. `image.repository` and `helmrepo.url` keep the old Harbor name.
- **`HARBOR_PROJECT` is set automatically.** The CI variable cannot be changed by hand; leave it.
- **GitLab environments are not updated automatically** on a namespace rename:
  Step 2 is always manual.
- **Container scanning can fail when image tag `latest` does not exist.** That is
  a separate problem, not caused by the rename.
- **Pipeline race condition on quick successive commits** — a false alarm; check
  the pod status (`kubectl get pods -n services-<new-name>`) before you act on it.
- **Precedent:** the `sumilearn` rename — gitlab-config MR !120, kubernetes-clusters MR !336.
  Read those before a new rename.

## References

- `gitlab-config/terraform/modules/project/harbor.tf` — Harbor project naming and lifecycle
