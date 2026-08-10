---
name: surf-kubectl-troubleshoot
description: >-
  Diagnose Kubernetes issues on SURF SDP — Flux reconciliation hangs, HelmRelease
  won't deploy, SOPS secrets won't decrypt, ingress has no IP, pods crash with
  ImagePullBackOff. Interactive troubleshooting menu. Use when debugging cluster
  state, Flux errors, HelmRelease conditions, SOPS decryption failures, or any
  kubectl output showing an error.
---

# SURF SDP Kubernetes Troubleshooting

Interactive diagnostic tool for common Kubernetes issues on SURF SDP: Flux
reconciliation, HelmRelease deployments, SOPS encryption, ingress, and pod
failures. Pick a symptom, run the diagnostics, interpret the output, and get
a targeted fix.

## Workflow

When the user invokes `/surf-kubectl-troubleshoot`, present a menu of symptoms
and guide them through the diagnostics.

### Step 1: Pick a symptom

Ask the user which symptom best describes their issue:

```
What's the issue you're seeing?

1. HelmRelease is stuck (shows Reconciling, UpgradeFailed, or no status)
2. Pod won't start (ImagePullBackOff, CrashLoopBackOff, Pending)
3. Flux Kustomization isn't syncing (Reconciling for >5min, error in conditions)
4. SOPS secret won't decrypt (can't read encrypted values.yaml, "permission denied")
5. Ingress has no external IP or shows error
6. "flux" command not found or wrong binary (returns unknown flags)
7. Something else — describe it briefly
```

Wait for their choice. For "something else", ask them to paste the error message
or describe the symptom (then route to the closest match).

### Step 2: Run diagnostics for the symptom

Based on their choice, run the appropriate kubectl commands and ask them to share
the output. Use the commands below as templates:

---

#### **Symptom 1: HelmRelease is stuck**

**Diagnostics:**

```bash
kubectl config current-context
kubectl get helmrelease -A -o wide
# Find the stuck one; note its namespace and name

kubectl describe helmrelease <name> -n <ns>
# Look for Status.Conditions; any Reason=UpgradeFailed, ReconciliationFailed?

kubectl get helmrepo -n <ns>
# HelmRepository status; any errors?

kubectl logs -n flux-system deploy/helm-controller --tail=50 | grep <name>
# Any errors in the helm controller?
```

**Interpret the output:**

Ask the user to share the output from `kubectl describe helmrelease <name> -n <ns>`.
Look for:

| Condition | Reason | Meaning | Fix |
|-----------|--------|---------|-----|
| Ready=False | UpgradeFailed | Helm upgrade failed (e.g. bad values, chart syntax) | Check `kubectl describe helmrelease` for the actual Helm error; fix chart/values and re-push |
| Ready=False | ReconciliationFailed | Flux gave up after retries | New git commit (new build number) or `/surf-sdp-helm-flux` |
| Ready=Unknown | Progressing | Still trying (upgrade in progress, job running) | Wait 2-5 min; it's not stuck yet |
| HelmRepository status empty | Never connected | Wrong URL, auth error, or DNS issue | Check `secretRef` exists and credentials are valid |

---

#### **Symptom 2: Pod won't start**

**Diagnostics:**

```bash
kubectl config current-context
kubectl get pods -n services-<app> -o wide
# Find the failing pod

kubectl describe pod <name> -n services-<app>
# Look for Events section; what's the last event?

kubectl logs <name> -n services-<app> --previous 2>/dev/null
# If pod crashed, get the previous log (--previous flag)

kubectl get events -n services-<app> --sort-by='.lastTimestamp' | tail -20
# Recent events in the namespace
```

**Interpret the output:**

| Status | Event | Likely cause | Fix |
|--------|-------|--------------|-----|
| ImagePullBackOff | "failed to pull image" | Image not found in registry, or pull auth failed | Check image digest/tag in HelmRelease; verify Harbor credentials (HelmRepository.secretRef) |
| CrashLoopBackOff | "OOMKilled" or "Killed" | Pod exceeded memory limit | Increase `resources.limits.memory` in values; or find memory leak in app |
| Pending | "0/N nodes available" | No node capacity or scheduling constraint unsatisfied | Check cluster capacity; ensure node taints/tolerations match pod spec |
| Error | "Liveness probe failed" | Health check failing | App is unhealthy; check logs (`kubectl logs`) for app errors |

---

#### **Symptom 3: Flux Kustomization isn't syncing**

**Diagnostics:**

```bash
kubectl config current-context
kubectl get kustomization -n flux-system
# Find the stuck one; note its name

kubectl describe kustomization <name> -n flux-system
# Status.Conditions; any LastUpdateTime > 5 minutes ago?

kubectl logs -n flux-system deploy/kustomize-controller --tail=50 | grep <name>
# Controller logs

git status
# Any uncommitted changes in your local checkout?
```

**Interpret the output:**

| Condition | Reason | Meaning | Fix |
|-----------|--------|---------|-----|
| Ready=False | GitNotAvailable | Git repo URL invalid or auth failed | Check repo URL in Kustomization spec; verify glab/GitHub auth |
| Ready=False | ReconciliationFailed | Kustomize build failed (bad YAML, missing patch) | Check `kubectl kustomize build manifests/<env>` locally for errors |
| Ready=Unknown | Progressing | Syncing in progress (normal, wait) | Wait 1-2 min; if stuck longer, check controller logs |
| Ready=True but old | (no error) | Kustomization is up-to-date but you expect a change | New commits aren't in the branch; check git log / git push |

---

#### **Symptom 4: SOPS secret won't decrypt**

**Diagnostics:**

```bash
kubectl config current-context
ls -la .sops.yaml

# Run the sops-doctor script:
bash scripts/sops-doctor.sh

# Or manually check:
which age
age-keygen -l ~/.config/sops/age/keys.txt

# Try decrypting:
sops -d secrets/<env>-secrets.yaml 2>&1 | head -20
```

**Interpret the output:**

| Error | Meaning | Fix |
|-------|---------|-----|
| "age: recipient stanza could not be decrypted" | Key in ~/.config/sops/age/keys.txt doesn't match the file's age public key | Verify key file path in `.sops.yaml`; regenerate if needed |
| "permission denied" on keys.txt | File permission issue | `chmod 600 ~/.config/sops/age/keys.txt` |
| "unknown key type in metadata" | `.sops.yaml` is malformed or references wrong key type | Check `.sops.yaml` syntax; ensure it lists the correct `age` key |
| "gpg: decryption failed" | GPG key missing (if using GPG instead of age) | Use `gpg --import` or switch to age (better for CI/CD) |

---

#### **Symptom 5: Ingress has no external IP**

**Diagnostics:**

```bash
kubectl config current-context
kubectl get ingress -n services-<app>
# or, if using LoadBalancer:
kubectl get svc -n services-<app>
# EXTERNAL-IP should not be <pending>

kubectl describe ingress <name> -n services-<app>
# or
kubectl describe svc <name> -n services-<app>

# Check ingress controller:
kubectl get pods -n traefik-external
kubectl logs -n traefik-external deploy/traefik | grep -i "error\|warn" | tail -10

# Check DNS:
nslookup <app>.<env>.sdp.surf.nl
```

**Interpret the output:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| EXTERNAL-IP = `<pending>` for >2 min | LoadBalancer not provisioning (cluster issue) or ingress misconfigured | Check cluster capacity; verify Traefik deployment is running; restart if needed |
| Ingress with no IP but no error | Ingress controller not watching this namespace | Add label `traefik.io/expose=true` to the service; Traefik's watch will pick it up |
| nslookup fails | DNS name not registered or not propagated | Wait 1-2 min; or ask platform team to register the DNS name |

---

#### **Symptom 6: "flux" command not found or wrong binary**

**Diagnostics:**

```bash
which flux
flux version
# If flux is InfluxDB's flux (not FluxCD), output will show "Flux" + influxdb version

# Use the kubectl fallback instead:
kubectl annotate helmrelease <name> \
  reconcile.fluxcd.io/requestedAt="$(date +%s)" \
  -n <namespace> --overwrite
```

**Interpret the output:**

| Output | Issue | Fix |
|--------|-------|-----|
| `flux version: v0.X.X` (no cloud version) | FluxCD is installed but old | Reinstall via `brew install fluxcd/tap/flux` or update |
| `Flux v1.X.X` (InfluxDB, not FluxCD) | Wrong flux binary | Uninstall InfluxDB; install FluxCD; or use kubectl annotate workaround |
| "command not found" | FluxCD not installed | `brew install fluxcd/tap/flux` (macOS) or `apt-get install flux` (Linux) |

**Workaround:** Use the kubectl annotate fallback — it doesn't require the flux binary.

---

### Step 3: Suggest a fix

Based on the diagnostics output the user shared, offer a targeted fix. Examples:

- **HelmRelease error:** "The chart values have a syntax error. Try `helm template` locally to validate."
- **ImagePullBackOff:** "The image digest is wrong. Check the HelmRelease spec; push a new git commit with the correct digest."
- **SOPS decryption:** "Your AGE key is missing or wrong. Run `sops-doctor` to diagnose, or regenerate the key."
- **Ingress pending:** "The LoadBalancer isn't provisioning. Check cluster capacity with `kubectl top nodes`."

### Step 4: Apply the fix and re-verify

Ask the user to run the fix:
1. Apply the suggested change (edit files, run commands, etc.)
2. Re-run the diagnostics from step 2
3. Confirm the issue is resolved

If it's not resolved, dig deeper:
- Ask for the full output (not just the error line)
- Suggest escalating to the platform team if it's infrastructure-level (network, DNS, cluster capacity)

## Bundled scripts

Reference these scripts in diagnostic output (assume they're available in the user's repo):

- `scripts/sops-doctor.sh` — diagnose AGE/SOPS setup
- `scripts/flux-hr-status.sh <helmrelease> <ns>` — quick HelmRelease health check
- `scripts/flux-force-reconcile.sh <helmrelease> <ns>` — force Flux to retry

## Important

- **Always run diagnostics locally before escalating.** The user often finds the issue while running commands.
- **Distinguish between "stuck" and "slow."** HelmRelease may be in `Progressing` state legitimately — wait 2-5 min before assuming it's stuck.
- **Use kubectl annotate as the flux CLI fallback.** If the flux binary isn't available (or is the InfluxDB one), the kubectl workaround always works.
- **SOPS keys are per-environment.** Ensure the user is decrypting the right file with the right AGE key (check `.sops.yaml`).
- **Check cluster capacity first for Pending pods.** `kubectl top nodes` and `kubectl describe nodes` reveal over-capacity issues.
- **Logs are your friend.** Pod logs (`kubectl logs`), controller logs (`kubectl logs -n flux-system`), and Kubernetes events (`kubectl get events`) tell the full story.
- This is a **GitLab/SDP** skill — use `kubectl`, `glab`, `git`, not `gh`.
- Applies to cedanl / SURF SDP repos.
