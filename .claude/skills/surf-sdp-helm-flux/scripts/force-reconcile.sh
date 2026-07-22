#!/usr/bin/env bash
# Force FluxCD to retry a HelmRelease.
# Usage: force-reconcile.sh <helmrelease> <namespace>
#
# Prefers the real flux CLI; falls back to kubectl annotate, which also
# sidesteps the classic trap of having the InfluxDB 'flux' binary in PATH.
set -euo pipefail

HR="${1:?usage: force-reconcile.sh <helmrelease> <namespace>}"
NS="${2:?usage: force-reconcile.sh <helmrelease> <namespace>}"

is_fluxcd_cli() {
  # The InfluxDB flux CLI has 'fmt' and 'test' subcommands and no 'reconcile'.
  command -v flux >/dev/null 2>&1 && flux --help 2>&1 | grep -q reconcile
}

if is_fluxcd_cli; then
  echo ">> flux reconcile helmrelease ${HR} --namespace ${NS}"
  flux reconcile helmrelease "${HR}" --namespace "${NS}"
else
  echo ">> fluxcd CLI not found (or InfluxDB flux detected); using kubectl annotate fallback"
  kubectl annotate helmrelease "${HR}" \
    "reconcile.fluxcd.io/requestedAt=$(date +%s)" \
    -n "${NS}" --overwrite
fi

echo ">> watching status (Ctrl-C to stop)"
kubectl get helmrelease "${HR}" -n "${NS}" -w
