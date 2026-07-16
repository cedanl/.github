#!/usr/bin/env bash
# One-shot health summary for a Flux HelmRelease and its source.
# Usage: hr-status.sh <helmrelease> <namespace>
set -euo pipefail

HR="${1:?usage: hr-status.sh <helmrelease> <namespace>}"
NS="${2:?usage: hr-status.sh <helmrelease> <namespace>}"

hdr() { printf '\n=== %s ===\n' "$1"; }

hdr "HelmRelease ${HR} (${NS}) — conditions"
kubectl get helmrelease "${HR}" -n "${NS}" \
  -o jsonpath='{range .status.conditions[*]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}' \
  | column -t -s $'\t' || true

hdr "Deployed vs desired"
kubectl get helmrelease "${HR}" -n "${NS}" \
  -o jsonpath='desired: {.spec.chart.spec.version}{"\n"}last deployed: {.status.history[0].chartVersion}{"\n"}failures: {.status.failures}{"\n"}' || true

hdr "Source (HelmRepository)"
SRC="$(kubectl get helmrelease "${HR}" -n "${NS}" \
  -o jsonpath='{.spec.chart.spec.sourceRef.name}')"
if [ -n "${SRC}" ]; then
  kubectl get helmrepository "${SRC}" -n "${NS}" -o wide || true
  READY="$(kubectl get helmrepository "${SRC}" -n "${NS}" \
    -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || true)"
  if [ -z "${READY}" ]; then
    echo "WARNING: HelmRepository has no Ready condition / empty status."
    echo "         Classic sign of auth or URL problems — check secretRef."
  fi
else
  echo "(no HelmRepository sourceRef found — GitRepository-based release?)"
fi

hdr "Recent jobs in namespace"
kubectl get jobs -n "${NS}" \
  --sort-by=.metadata.creationTimestamp 2>/dev/null | tail -6 || true

hdr "Recent events"
kubectl get events -n "${NS}" --sort-by=.lastTimestamp 2>/dev/null | tail -10 || true
