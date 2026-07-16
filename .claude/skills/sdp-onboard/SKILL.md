---
name: sdp-onboard
description: Take a CEDA app from code to a running Kubernetes deployment on SURF's SDP — obtain access, create the GitLab repo (Terraform in gitlab-config), request a tenant, copy the GitLab scaffolding from a template repo, and wire up per-env manifests/URLs. Use when standing up a NEW CEDA/SDP service or onboarding a repo to the SURF Developer Platform.
---

# sdp-onboard

End-to-end path to get a CEDA app running on the **SURF Developer Platform (SDP)**,
distilled from the CEDA runbook (`text-analysis/docs/{access,gitlab,streamlit-setup}.md`
in that repo — read the current version there for full detail).
Several steps need **SDP-admin approval** — flag those; you can't self-merge them.

## Prereqs / access (docs/access.md)
- SURF account (`@surf.nl`), on the **SURF VPN (eduVPN)**.
- GitLab is `https://git.ia.surfsara.nl/surf-internal/npuls/ceda/` — **not** github.com.
- SSH: Ed25519 key (`ssh-keygen -t ed25519`), add pubkey to GitLab (Authentication & Signing).
- Tools: `brew install hadolint yamllint k9s kubectl kubectx kubelogin kustomize helm flux sops`.

## 1. Create the GitLab repo (needs SDP-admin merge)
The repo is declared as **Terraform** in the `surf-internal/gitlab-config` repo:
```bash
git clone git@git.ia.surfsara.nl:surf-internal/gitlab-config.git
cd gitlab-config && git checkout -b create_repository_ceda_<app>
# edit terraform/npuls/ceda/main.tf — add a module block:
```
```tf
module "<app>" {
  source = "../../modules/project"
  name = "CEDA <App>"
  path = "<app>"
  description = "..."
  namespace_id = var.parent_group_id
  visibility_level = "internal"
  topics = ["npuls", "ceda", "<app>"]
  container_cleanup_enabled = false
  group_ids_to_grant_access = { (var.teams_id_map["ceda-team"]) = "maintainer" }
  invite_admin_role_urn = var.teams_invite_admin_role_urn_map["ceda-team"]
  invite_dev_role_urn   = var.teams_invite_dev_role_urn_map["ceda-team"]
}
```
Module name: letter/underscore start; letters, digits, `_`, `-` only. Push, open
an MR, assign an **SDP-team reviewer** to merge (ping via Element/Backstage).

## 2. Request a tenant (needs SDP-admin action)
Gets you the SDP environments to run in. Use the Backstage "Requesting a tenant"
form: Department `NPULS - CEDA`, Service phase `Pilot/PoC`, Sizing `S`,
Kafka/MinIO/PostgreSQL as needed, the GitLab repo URL, Internal access `Yes`.
Infra tweaks (e.g. Ingress port propagation, which environments) may need an MR to
`surf-internal/sdp/infrastructure/kubernetes-clusters`.

## 3. Point your code at the new repo
```bash
git remote set-url origin git@git.ia.surfsara.nl:surf-internal/npuls/ceda/<app>.git
```
(The runbook has a full rebase dance to start `main` clean when migrating from a
GitHub repo — follow docs/streamlit-setup.md carefully; don't improvise a
`reset --hard` without reading it.)

## 4. Copy GitLab scaffolding from a template repo
Pull the deployment machinery from an existing repo (e.g. `text-analysis`) and rename:
```bash
GITLAB_FILES="requirements.txt manifests Dockerfile docker-compose.yml charts .gitlab-ci.yml .gitlab"
git fetch <template-remote> HEAD:<branch>
git checkout <branch> -- $GITLAB_FILES
find $GITLAB_FILES -type f | xargs perl -pi -e 's/text-analysis/<app>/g'
git mv charts/text-analysis charts/<app>   # Chart.yaml name field is manual
```
`python-fastapi-template` is the from-scratch SDP starting template.

## 5. Wire up environments (GitLab web UI)
For each of development/testing/staging/playground, in **Operate → Environments → edit**:
```
External URL: https://<app>.<env>.sdp.surf.nl   (dev uses .dev., test uses .test.)
GitLab agent: <env>
Kubernetes namespace: services-<app>
Flux resource: <app>
```
(Note: this is web-UI-only — there is currently no code-based way to set it.)

## Deploy model: Flux + Kustomize (corrects plain-Helm assumptions)
`manifests/base/` holds Flux `helmrelease.yaml` + `helmrepo.yaml` +
`kustomization.yaml` + `values-base.yaml`; each env dir has a `kustomization.yaml`
that patches base with its `values.yaml`. **Flux** syncs; deploy = commit + MR
triggering the GitLab pipeline. See [[gitlab-ci]], [[surf-sdp-helm-flux]], [[sdp-secrets-management]].

## Cluster access & inspection (read-only)
```bash
kubectx <env>                                            # development/testing/...
kubectl config set-context --current --namespace=services-<app>   # once per context
kubectl -n services-<app> get pod,ep,svc,ing,deployment
kubectl logs <pod> -n services-<app>
```
Health probes hit `/healthz`. Never mutate a cluster by hand — deploys go via CI.

## Honesty
Steps 1–2 depend on SDP admins; say so and don't claim "done" until merged/granted.
The template-copy rename is mechanical — verify `grep -ri <template-name>` comes back
clean (except Chart.yaml). See the principle of verifying work actually runs before calling it done.
