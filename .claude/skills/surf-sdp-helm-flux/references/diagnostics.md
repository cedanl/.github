# Diagnostic runbook: Flux/Helm on SDP

Work top-down: source → release → workload. Stop at the first broken layer;
everything below it is noise.

## 0. Orient

```bash
# What Flux resources exist in the tenant namespace?
kubectl get helmrepositories,helmreleases -n <ns>

# Which Kustomization owns them? (hand edits get reverted by this)
kubectl get helmrelease <name> -n <ns> \
  -o jsonpath='{.metadata.labels.kustomize\.toolkit\.fluxcd\.io/name}'
```

## 1. Source layer (HelmRepository)

```bash
kubectl describe helmrepository <name> -n <ns>
```

Healthy: `Status:` shows `Ready: True` with an artifact revision.
Broken signs:

- **Empty `Status:` and `Events: <none>`** → never connected. Check `URL:`
  (must be `oci://cr.surf.nl/...`) and `Secret Ref:` name.
- Verify the secret exists and is a docker-registry secret:

```bash
kubectl get secret sdp-harbor-credentials -n <ns> -o yaml | head
```

- Manual pull test (note the `_` tag form for versions with `+`):

```bash
helm pull oci://cr.surf.nl/<project>/<chart> --version '<version-with-_>'
```

## 2. Release layer (HelmRelease)

```bash
kubectl describe helmrelease <name> -n <ns>
kubectl get helmrelease <name> -n <ns> -o yaml | grep -A 30 'status:'
```

Read these fields:

- `conditions[type=Released]` — `UpgradeFailed` means Helm ran and the
  release itself failed (template/values error, admission rejection).
  The message contains the real error, e.g.
  `Ingress "x" is invalid: spec: either defaultBackend or rules must be
  specified` → a subchart/component is enabled but its ingress values are
  empty.
- `Running 'upgrade' action with timeout of 5m0s` — still in flight; wait.
- `history:` — compare `chartVersion` of the last deployed entry with what
  the pipeline expects. Old version + `failures: N` = rolled back.
- `spec.install.remediation.retries: -1` means retry forever on *install*;
  upgrade remediation is configured separately and usually is not infinite.

Force a retry:

```bash
flux reconcile helmrelease <name> --namespace <ns>       # real flux CLI
# or, always available:
kubectl annotate helmrelease <name> \
  reconcile.fluxcd.io/requestedAt="$(date +%s)" -n <ns> --overwrite
```

Unstick a wedged release:

```bash
flux suspend helmrelease <name> -n <ns>
flux resume  helmrelease <name> -n <ns>
```

## 3. Workload layer

```bash
# Watch what the release actually creates
kubectl get jobs,pods -n <ns> -w

# Failed hook/migration job logs (job names are timestamped)
kubectl logs job/<release>-<timestamp> -n <ns>

# Events, most recent last
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20
```

Common finding: an image pull error on a job pod because the values point
at a tag/digest that was never pushed — cross-check against the Harbor UI
or `crane ls` / `helm pull`.

## 4. Kustomization sync (when your fix "doesn't apply")

If you changed HelmRepository/HelmRelease manifests in the config repo but
the cluster doesn't reflect it:

```bash
kubectl get kustomization -n flux-system | grep <tenant>
kubectl describe kustomization <tenant>-sync -n flux-system
flux reconcile kustomization <tenant>-sync -n flux-system
```

Conversely: if you edited the live resource with kubectl and it reverted,
that's this sync doing its job. Fix the repo.

## 5. Post-renderer annotations

SDP HelmReleases carry kustomize `postRenderers` that patch a
`sdp.surf.nl/team: <team>` annotation onto Deployments, StatefulSets,
ReplicaSets and DaemonSets. If a resource type is rejected during upgrade
with a patch error, check whether the postRenderer patch targets match the
API versions actually rendered by the chart.
