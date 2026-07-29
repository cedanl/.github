#!/usr/bin/env bash
# Check whether a Helm chart version exists in an OCI registry, testing both
# the semver form (+build metadata) and the OCI tag form (+ replaced by _).
#
# Usage: check-oci-tag.sh <oci-url> <chart-version>
# Example:
#   check-oci-tag.sh oci://cr.surf.nl/ceda-instroom-config/instroom-config/instroom \
#                    '0.0.1-build.20+testminio.f085e792'
#
# Requires: helm (logged in to the registry if it is private:
#   helm registry login cr.surf.nl)
set -uo pipefail

URL="${1:?usage: check-oci-tag.sh <oci-url> <chart-version>}"
VER="${2:?usage: check-oci-tag.sh <oci-url> <chart-version>}"

UNDERSCORE_VER="${VER//+/_}"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "${TMPDIR}"' EXIT

try_pull() {
  local v="$1"
  if helm pull "${URL}" --version "${v}" -d "${TMPDIR}" >/dev/null 2>&1; then
    echo "FOUND:    ${URL}:${v}"
    return 0
  else
    echo "missing:  ${URL}:${v}"
    return 1
  fi
}

echo "Checking chart tags for version '${VER}'"
FOUND=1
try_pull "${VER}" && FOUND=0
if [ "${VER}" != "${UNDERSCORE_VER}" ]; then
  try_pull "${UNDERSCORE_VER}" && FOUND=0
fi

if [ "${FOUND}" -ne 0 ]; then
  echo
  echo "Neither form found. Check:"
  echo "  - are you logged in?  helm registry login cr.surf.nl"
  echo "  - does the repo path match Harbor exactly (project/repo/chart)?"
  echo "  - was the helm:package / push job in the pipeline successful?"
  exit 1
fi
