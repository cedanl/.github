---
name: surf-ingress-migration
description: >-
  Migrate a tenant's ingress from Kong to Traefik-external with cert-manager TLS
  and per-environment values. Use when planning or executing a Kong→Traefik ingress
  upgrade on SDP, or when the user mentions ingress migration, Kong deprecation,
  Traefik external LoadBalancer, or references a tenants's ingress configuration.
---

# SURF SDP Ingress Migration (Kong → Traefik)

Migrate a tenant's ingress from the legacy Kong ingress controller to the modern
Traefik-external LoadBalancer setup, with cert-manager certificate automation and
per-environment Helm values handling. This is a multi-repo, multi-environment
coordinated change — explicit verification steps prevent partial migrations that
break deployments.

## Workflow

When the user invokes `/surf-ingress-migration [optional: tenant name]`, walk
through the steps below:

### 1. Pre-flight checklist

Verify the prerequisites before starting the migration:

- [ ] User has kubectl access to all target environments (development/test/staging/production)
- [ ] User has push access to the app's config repo (manifests + values)
- [ ] Current ingress is working (pod responds to requests via the old Kong setup)
- [ ] No active MRs that modify ingress configuration (merge or close them first)
- [ ] Traefik-external is already deployed on all target clusters
  - Check: `kubectl get deployment -n traefik-external traefik`
  - Must show `Ready 1/1` (or replicas matching your cluster setup)
- [ ] cert-manager is deployed and `Certificate` CRD is available
  - Check: `kubectl get crds | grep cert-manager`

If any check fails, stop and have the user fix it before continuing.

### 2. Plan the per-environment values changes

Kong ingress configs use the `Ingress` resource type and `kubernetes.io/ingress.class: kong`.
Traefik-external uses the **LoadBalancer service** pattern: expose a service of type
`LoadBalancer` with label `traefik.io/expose=true`, and let Traefik's service monitor
pick it up.

Ask the user:
- Does your app already use a LoadBalancer service, or do you need to convert from Ingress?
- Which environments need the migration (all five, or a subset)?
- Do you use TLS/HTTPS today? (cert-manager is needed for the new setup)

Then walk through the values changes:

**Base values** (`manifests/base/values-base.yaml`):
```yaml
# Remove Kong Ingress block:
# ingress:
#   className: kong
#   hosts:
#     - host: app.example.com
#       paths: ...

# Add LoadBalancer service + cert-manager Certificate:
service:
  type: LoadBalancer
  annotations:
    traefik.io/expose: "true"

certificate:
  enabled: true
  issuer: letsencrypt-prod  # or letsencrypt-staging for test/dev
  dnsNames:
    - app.example.com
```

**Per-environment overrides** (`manifests/<env>/values.yaml`):

Each environment specifies its own DNS names:
```yaml
certificate:
  dnsNames:
    - app.development.sdp.surf.nl   # development
    # OR
    - app.test.sdp.surf.nl          # test
    # OR
    - app.staging.sdp.surf.nl       # staging
    # OR
    - app.sdp.surf.nl               # production
```

**Important:** Use explicit per-env values, never rely on value merging/defaults for
DNS names. The old Kong setup likely used inline Ingress host lists; Traefik + cert-manager
require explicit certificate configuration.

### 3. Draft the Helm chart changes

In `charts/<app>/values.yaml`, add the new schema:

```yaml
service:
  type: LoadBalancer
  port: 80
  targetPort: 8080
  annotations: {}

certificate:
  enabled: false  # default off; enabled per-env
  issuer: letsencrypt-prod
  dnsNames: []
  secretName: <app>-tls
```

In `charts/<app>/templates/service.yaml`, ensure the LoadBalancer is created:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "app.fullname" . }}
  labels:
    {{- include "app.labels" . | nindent 4 }}
  annotations:
    {{- if .Values.service.annotations }}
    {{- toYaml .Values.service.annotations | nindent 4 }}
    {{- end }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
  selector:
    {{- include "app.selectorLabels" . | nindent 4 }}
```

In `charts/<app>/templates/certificate.yaml` (new file):
```yaml
{{- if .Values.certificate.enabled }}
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: {{ .Values.certificate.secretName }}
  namespace: {{ .Release.Namespace }}
spec:
  secretName: {{ .Values.certificate.secretName }}
  issuerRef:
    name: {{ .Values.certificate.issuer }}
    kind: ClusterIssuer
  dnsNames:
    {{- range .Values.certificate.dnsNames }}
    - {{ . }}
    {{- end }}
{{- end }}
```

### 4. Create the MR and run preview

Draft the changes:

```bash
# In the config repo
git checkout -b feat/kong-to-traefik-<app>
# Edit charts/, manifests/ as above
git add .
git commit -m "feat: migrate ingress Kong→Traefik-external with cert-manager

- Convert Ingress resources to LoadBalancer + Certificate CRs
- Add per-environment certificate DNS names
- Update service.type to LoadBalancer in values

Related: voxpop production ingress migration"
```

Preview what will be deployed (for one environment):

```bash
# Dry-run
helm template <app> charts/<app> \
  -f charts/<app>/values.yaml \
  -f manifests/base/values-base.yaml \
  -f manifests/development/values.yaml \
  --namespace services-<app>
# or
kustomize build manifests/development
```

Verify:
- [ ] Service type is `LoadBalancer` (not `ClusterIP`)
- [ ] Traefik annotations are present on the service
- [ ] Certificate resource exists with correct `dnsNames`
- [ ] No Kong/Ingress resources remain

Then push and open an MR (target: main).

### 5. Post-merge: verify on each environment

Once the MR is merged and the GitLab pipeline completes, verify the migration
on each environment in sequence (development → test → staging → production):

**Check 1: LoadBalancer IP is assigned**

```bash
kubectx development
kubectl get svc -n services-<app>
# Should show TYPE=LoadBalancer with an EXTERNAL-IP (not <pending>)
```

If EXTERNAL-IP stays `<pending>` for more than 2 minutes, the LoadBalancer isn't
provisioning. Check:
```bash
kubectl describe svc <app> -n services-<app>
# Look for events like "no nodes available" or networking errors
```

**Check 2: Certificate is ready**

```bash
kubectl get certificate -n services-<app>
# Should show READY=True, AGE <1m
```

If not ready:
```bash
kubectl describe certificate <app>-tls -n services-<app>
# Check conditions; common issues:
# - "DNS validation failed" → DNS name doesn't resolve yet (wait 1-2 min)
# - "Issuer error" → cert-manager can't reach Let's Encrypt (check ClusterIssuer)
```

**Check 3: Traefik picked up the service**

```bash
kubectl logs -n traefik-external deployment/traefik | grep <app>
# Should show routing rules being added
```

**Check 4: End-to-end connectivity**

```bash
# Wait 30s for Traefik and DNS to settle
sleep 30

curl -v https://app.development.sdp.surf.nl/healthz
# Should return 200 OK with a valid TLS cert
```

Repeat checks 1-4 for test, staging, and production environments.

### 6. Decommission Kong Ingress (cleanup)

Once all environments are verified:

```bash
# Remove the old Kong Ingress resource and any kong annotations
# from manifests/ (if not already done in step 4)
git checkout -b cleanup/remove-kong-ingress
# Delete any remaining Ingress resources or kong-specific config
git commit -m "cleanup: remove Kong Ingress resources after Traefik migration"
git push && open MR
```

Merge after verification.

### 7. Bevestig en voer uit

Summarize the migration plan:

> **Migration plan for <app>:**
>
> **Changes:**
> - Convert Kong Ingress → LoadBalancer service
> - Add cert-manager Certificate CRs (per-environment DNS names)
> - Update Helm values for service type and certificate config
>
> **Environments affected:** [development, test, staging, production]
>
> **Verification steps:**
> 1. LoadBalancer IP assigned (kubectl get svc)
> 2. Certificate ready (kubectl get certificate)
> 3. Traefik routing active (kubectl logs)
> 4. End-to-end curl to /healthz
>
> **Timeline:** 30–60 minutes per environment (mostly waiting for DNS/cert provisioning)
>
> Ready to proceed with step 1 (pre-flight checks)?

Wait for the user to confirm before continuing. If they say no or request changes,
adjust the plan and re-confirm.

## Important

- **Multi-repo coordination:** changes span app config repo + infrastructure/certificates;
  ensure both are merged before moving to the next environment.
- **Never migrate production first.** Test on development/test first; production is last.
- **DNS propagation delay:** After cert-manager provisions a Certificate, DNS may take
  1–2 minutes to update. Don't retry curl immediately if DNS resolution fails.
- **LoadBalancer IP:** If EXTERNAL-IP stays `<pending>` after 2 minutes, infrastructure
  issue (not DNS). Check cluster capacity/networking with platform team.
- **Traefik version:** This skill assumes Traefik 2.x with the service monitor controller.
  Older setups may need Ingress CRDs instead; check your cluster's Traefik version.
- This is a **GitLab/SDP** skill — use `glab`, `kubectl`, `helm`, not `gh` or GitHub Actions.
- Applies to cedanl / SURF SDP repos.
