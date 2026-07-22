#!/usr/bin/env bash
# Diagnose local SOPS+AGE setup, optionally test-decrypt a file.
# Usage: sops-doctor.sh [encrypted-file]
set -uo pipefail

ok()   { printf 'OK    %s\n' "$1"; }
warn() { printf 'WARN  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; }

command -v sops >/dev/null && ok "sops installed: $(sops --version 2>/dev/null | head -1)" || fail "sops not in PATH"
command -v age-keygen >/dev/null && ok "age installed" || warn "age-keygen not in PATH (only needed for key generation)"

KEYFILE="${SOPS_AGE_KEY_FILE:-$HOME/.config/sops/age/keys.txt}"
if [ -n "${SOPS_AGE_KEY:-}" ]; then
  ok "SOPS_AGE_KEY is set (using in-env private key)"
elif [ -f "$KEYFILE" ]; then
  ok "key file present: $KEYFILE"
  grep -h 'public key' "$KEYFILE" | sed 's/^# /      my /'
else
  fail "no private key: SOPS_AGE_KEY unset and $KEYFILE missing"
fi

if [ $# -ge 1 ]; then
  FILE="$1"
  echo "--- checking ${FILE} ---"
  if ! grep -q '^sops:' "$FILE" && ! grep -q '"sops":' "$FILE"; then
    fail "no sops metadata — file is PLAINTEXT (or an _orig working copy)"
    exit 1
  fi
  echo "recipients:"
  grep -o 'age1[a-z0-9]*' "$FILE" | sort -u | sed 's/^/      /'
  if sops --decrypt "$FILE" >/dev/null 2>&1; then
    ok "test decrypt succeeded"
  else
    fail "test decrypt failed — your key is not among the recipients, or key not found"
    echo "      -> ask an existing recipient to add your public key to .sops.yaml"
    echo "         and run 'sops updatekeys' (see references/sops-errors.md)"
    exit 1
  fi
fi
