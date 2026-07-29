#!/usr/bin/env bash
# Re-key all SOPS-encrypted files after changing recipients in .sops.yaml.
# Run from the repo root (where .sops.yaml lives).
# Usage: rekey-all.sh [search-root]   (default: manifests/)
set -euo pipefail

ROOT="${1:-manifests}"
[ -f .sops.yaml ] || { echo "No .sops.yaml in $(pwd) — run from repo root" >&2; exit 1; }

FOUND=0
while IFS= read -r -d '' f; do
  if grep -q 'ENC\[' "$f" || grep -q '^sops:' "$f"; then
    FOUND=1
    echo ">> sops updatekeys $f"
    sops updatekeys --yes "$f"
  fi
done < <(find "$ROOT" -name '*.yaml' -print0)

[ "$FOUND" -eq 1 ] || echo "No encrypted files found under ${ROOT}/"
echo "Done. Remember: new recipients can only decrypt after this ran and was pushed."
