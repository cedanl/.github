---
name: gitlab-ci
description: Author and debug GitLab CI for the CEDA/SURF config repos (*-config) — the SDP shared components, the branch→cluster rules, Helm package/publish/promote, and kubernetes diff/dry-run/verify stages. Use when editing .gitlab-ci.yml, a .gitlab/*.yaml component, or debugging a GitLab pipeline in a config repo.
---

# gitlab-ci

The `*-config` GitOps repos (`instroom-config`, `1cijfer-config`, …) deploy via
**GitLab CI built on SURF's shared SDP components**. This is a different world
from the GitHub Actions repos (see [[actions-ci]]).

## Branch → cluster mapping (workflow.rules)
`.gitlab-ci.yml` sets `ENVIRONMENT_CLUSTER` from the trigger:
- **Merge request** (`$CI_MERGE_REQUEST_IID`) → `development`
- default branch or `pipeline` branch → `testing`
- pipeline trigger / `test/trigger` → `testing`
- **tag** (`$CI_COMMIT_TAG`) → `playground`

When changing where something deploys, edit these `workflow.rules`, not scattered
job rules. Be explicit about which cluster a change targets.

## SDP shared components (don't reinvent)
Pipelines `include:` versioned components from
`$CI_SERVER_FQDN/surf-internal/sdp/components/...`:
- `base/base`, `base/security`
- `semver/generate-version`, `semver/promote-version`
- `helm/helm-lint`, `helm/helm-publish`, `helm/helm-promote`
- `kubernetes/diff`, `kubernetes/dry-run`, `kubernetes/verify-up`, `kubernetes/deploy-preview`
Plus the repo-local `.gitlab/helm-package.yaml` (a `spec.inputs` component that
patches the docker image ref + chart version, then `helm package`).
Prefer wiring an existing SDP component over writing bespoke job YAML.

## The deploy flow
package → publish (to Harbor OCI: `oci://$HARBOR_HOST/...`) → promote →
`kubernetes/diff` → `dry-run` → `verify-up`. The pipeline itself runs the
diff/dry-run/verify against `${ENVIRONMENT_CLUSTER}` — so review the **diff and
dry-run** output in the pipeline before a change reaches a real cluster. Don't
run `kubectl apply`/`helm upgrade` by hand.

## Chart / values layout
`charts/<app>/` + `manifests/<env>/values.yaml` over `manifests/base/values-base.yaml`.
See [[surf-sdp-helm-flux]] for the full layout and SOPS secret handling.

## Local component structure (authoring)
Repo-local components live in `.gitlab/*.yaml` with a `spec: inputs:` header
(typed inputs w/ defaults) then `---` then the job body using `$[[ inputs.x ]]`.
Match that shape when adding one.

## Debugging
- Use `glab` (GitLab CLI) or the GitLab web UI for MRs/pipelines — **not** `gh`.
- Read pipeline logs before retrying; avoid guess-and-check (see the principle of verifying work actually runs before calling it done).
- Secrets are SOPS-encrypted (`.sops.yaml`); never print or commit plaintext.

## Reference
See the CEDA repo split (GitLab *-config repos vs GitHub app repos) for which repos are GitLab-config vs GitHub-app.
