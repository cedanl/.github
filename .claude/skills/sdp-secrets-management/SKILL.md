---
name: sdp-secrets-management
description: >-
  Manage SOPS + AGE encrypted Kubernetes secrets for SURF SDP projects
  (instroom-config style): .sops.yaml creation
  rules, key management for teams, GitLab CI integration, and the decision
  tree for when to use Ansible Vault, SOPS+AGE, or a secret server
  (OpenBao/Infisical). Use this skill whenever the user encrypts or decrypts
  secrets, edits a *.secret.yaml or secret_orig.yaml file, hits SOPS errors
  ("no identity matched", "sops metadata not found", "no matching creation
  rules"), rotates or adds AGE keys, asks where to store a credential, or
  mentions sops, age, .sops.yaml, ansible-vault vs alternatives — even if
  they only paste a SOPS error without a question.
---

# SDP Secrets Management (SOPS + AGE)

Secrets for SDP Kubernetes deployments are **encrypted in Git** with SOPS
using AGE keys. No secret server is involved in the standard flow. Follow
these conventions; read `references/sops-errors.md` for the full error
catalogue before improvising fixes.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/sdp-secrets-management`,
or automatically) when you encrypt/decrypt a secret, edit a `*.secret.yaml` /
`secret_orig.yaml`, hit a SOPS error, rotate/add AGE keys, or ask where a
credential should live. It is reference + a decision tree, not a procedure to run.

## Which tool for which secret — decision tree

- Secret used **only by Ansible** → Ansible Vault (see the
  surf-ansible-conventions skill). Zero extra infrastructure.
- Secret consumed by **k8s manifests, GitLab CI, and/or multiple tools**,
  encrypted-at-rest-in-Git acceptable → **SOPS + AGE** (this skill's
  default; works in air-gapped environments).
- Need runtime injection, rotation, per-secret audit/RBAC → a secret
  server (OpenBao or self-hosted Infisical, optionally with External
  Secrets Operator syncing into k8s). Heavier to operate — propose it only
  when SOPS demonstrably falls short, not by default.
- CSI driver and ESO are *integration layers*, not stores — they still
  need a backend and don't compete with SOPS.

## Repository conventions

```
<config-repo>/
├── .sops.yaml                    # creation rules, repo root
└── manifests/
    └── <env>/
        ├── secret_orig.yaml      # plaintext working copy — NEVER commit
        └── secret.yaml           # SOPS-encrypted, committed
```

`.sops.yaml` at the repo root:

```yaml
creation_rules:
  - path_regex: manifests/.*/secret.*\.yaml$
    encrypted_regex: ^(data|stringData)$
    age: <age-public-key>[,<second-recipient>,...]
```

Rules that matter:

- **`path_regex` is a regex, not a glob.** `manifests/*/...` does not mean
  "any subdirectory" — it means "zero or more `/` characters". Write
  `manifests/.*/` and test against the real filename; "no matching
  creation rules found" is almost always this.
- `encrypted_regex: ^(data|stringData)$` encrypts only the secret payload
  of a k8s Secret, leaving `kind`/`metadata` readable — keep it that way
  so diffs and code review stay possible.
- The `*_orig.yaml` plaintext working copies must be in `.gitignore`.
  Encrypt to the committed name:
  `sops --encrypt manifests/dev/secret_orig.yaml > manifests/dev/secret.yaml`
- When operating from a subdirectory, pass the config explicitly:
  `sops --config ../../.sops.yaml ...` (note: the flag is `--config`, not
  `-a`).

## Retrieve an existing value from a cluster (to reuse in a secret)

Often a value you need to put in `secret_orig.yaml` already lives in the
cluster (e.g. a MinIO admin key created by another chart). Pull and decode it:

```bash
kubectx <env>                                  # per-env cluster context
kubectl get secret -n <namespace>              # list; find the one you need
kubectl get secret -o yaml -n <ns> <name>      # values are base64-encoded
echo <base64-value> | base64 -d                # decode
```

Treat the decoded output as sensitive — don't paste it into commits or logs.
To inspect an already-encrypted repo file without editing: `sops -d <file>`.

## Key management

- Generate: `age-keygen -o ~/.config/sops/age/keys.txt` — the file holds
  the private key; the public key (`age1...`) goes into `.sops.yaml`.
- SOPS finds the private key via `SOPS_AGE_KEY_FILE`
  (`~/.config/sops/age/keys.txt` is the conventional path — export it in
  your shell profile) or `SOPS_AGE_KEY` (the key string itself; this is
  the form used as a masked GitLab CI variable).
- **Team access = multiple recipients.** List every teammate's public key
  comma-separated in the `age:` field. Files must be **re-keyed** after
  changing recipients — editing `.sops.yaml` alone changes nothing for
  existing files: `sops updatekeys manifests/dev/secret.yaml` (or
  `scripts/rekey-all.sh` for the whole repo).
- Losing all private keys means the secrets are gone. At least two
  recipients per repo, always.

## GitLab CI integration

- Store the private key as a masked, protected CI/CD variable
  `SOPS_AGE_KEY` (variable type, not file — SOPS reads it directly).
- Decrypt in the job just-in-time; never write plaintext to an artifact:

```yaml
deploy:
  script:
    - sops --decrypt manifests/$ENV/secret.yaml | kubectl apply -f -
```

- For Flux-managed environments, prefer letting **Flux decrypt in-cluster**
  instead of the pipeline: store the age private key as a k8s secret
  (`sops-age`) in the tenant namespace and set
  `spec.decryption: {provider: sops, secretRef: {name: sops-age}}` on the
  Kustomization. Then the pipeline never handles plaintext at all.

## Error quick reference

| Error | Meaning | Fix |
|---|---|---|
| `no identity matched any of the recipients` | private key for the file's recipient not available | set `SOPS_AGE_KEY_FILE`; check you're a recipient; ask a recipient to `updatekeys` after adding you |
| `sops metadata not found` | file is plaintext, you used edit/decrypt | encrypt it first (`sops -e`), or you grabbed the `_orig` file |
| `no matching creation rules found` | `path_regex` doesn't match the path | fix the regex (glob vs regex trap); test with `sops filestatus` |
| Encrypted file has plaintext fields | `encrypted_regex` too narrow, or file edited outside sops | re-encrypt; only edit via `sops <file>` |
| CI decrypt works locally, fails in job | `SOPS_AGE_KEY` unset/unprotected branch | check variable scope + protected flag |

Full diagnostic walk-throughs: `references/sops-errors.md`.

## Bundled scripts

- `scripts/sops-doctor.sh [file]` — checks key setup (env vars, key file,
  recipient match) and optionally test-decrypts a file.
- `scripts/rekey-all.sh <path-regex-root>` — runs `sops updatekeys` over
  all encrypted files after a recipient change in `.sops.yaml`.

## Important
- **Never commit plaintext secrets.** Only `secret.yaml` (encrypted) is committed;
  `*_orig.yaml` plaintext working copies must be gitignored — stage by name.
- **Never print decrypted values** in a way that persists (logs, artifacts, chat).
- **Re-key after changing recipients** — editing `.sops.yaml` alone changes
  nothing for existing files (`sops updatekeys` / `scripts/rekey-all.sh`).
- Keep **≥2 recipients per repo** — losing all private keys means the secrets are
  gone.
- Prefer SOPS+AGE; propose a secret server only when SOPS demonstrably falls short,
  not by default.
- Applies to cedanl / SURF SDP repos.
