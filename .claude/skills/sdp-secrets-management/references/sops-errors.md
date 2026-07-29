# SOPS error catalogue — detailed walk-throughs

## "Failed to get the data key ... no identity matched any of the recipients"

SOPS knows which public key(s) the file was encrypted for (listed in the
error and in the file's `sops.age` metadata block), but can't find a
matching private key.

1. Which recipients can decrypt this file?
   ```bash
   grep -A2 'recipient:' secret.yaml
   ```
2. Where is your private key, and does SOPS know?
   ```bash
   ls ~/.config/sops/age/keys.txt
   echo "$SOPS_AGE_KEY_FILE"; echo "${SOPS_AGE_KEY:+set}"
   export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt
   ```
3. Does your public key match a recipient?
   ```bash
   grep 'public key' ~/.config/sops/age/keys.txt
   ```
   If your key is *not* among the file's recipients: add your public key
   to `.sops.yaml` and have someone who **can** decrypt run
   `sops updatekeys` on the file(s). You cannot grant yourself access.

## "sops metadata not found"

The file is plain YAML — no `sops:` block at the bottom
(`tail -20 <file>` to confirm). Causes:

- You targeted the `_orig` plaintext working copy.
- The file was committed unencrypted (incident! rotate the secret, not
  just the file).
- You want first-time encryption: `sops -e -i <file>` or
  `sops -e <orig> > <target>`.

## "error loading config: no matching creation rules found"

The file's path doesn't match any `path_regex` in the `.sops.yaml` in
effect.

- `path_regex` is a **regex**: `manifests/*/x` means "manifest" + zero or
  more slashes — not a glob. Use `manifests/.*/secret.*\.yaml$`.
- The path is matched relative to the `.sops.yaml` location; when running
  from a subdirectory with `--config`, check what the relative path
  resolves to.
- Confirm which config SOPS uses — it searches upward from the target
  file for `.sops.yaml`. An unexpected nested `.sops.yaml` shadows the
  root one.
- Quick test: temporarily broaden to `path_regex: .*\.yaml$`; if that
  matches, the pattern is the problem, not the config discovery.

## Editing and verifying

- Always edit via `sops <file>` (decrypt→$EDITOR→re-encrypt). Editing the
  encrypted file directly corrupts the MAC.
- Show recipients and key groups: `sops --show-master-keys <file>` (older
  syntax) or inspect the `sops:` metadata block.
- Verify what is and isn't encrypted after changing `encrypted_regex`:
  `grep -c 'ENC\[' <file>` and eyeball the non-payload fields.

## Flux in-cluster decryption

Store the age private key in the tenant namespace:

```bash
kubectl create secret generic sops-age \
  --namespace <tenant> \
  --from-file=age.agekey=/path/to/keys.txt
```

Kustomization spec:

```yaml
spec:
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

Symptoms of a broken setup: Kustomization events show
`decryption secret error` (secret missing/wrong key name — the data key
must end in `.agekey`) or the same "no identity matched" text as local
SOPS (wrong private key for the recipients).

## Incident: plaintext secret committed

1. Rotate the actual credential immediately — history rewriting is
   secondary, the secret must be assumed leaked.
2. Encrypt the corrected value properly; add the `_orig` name to
   `.gitignore`.
3. Only then consider `git filter-repo` if policy requires history
   cleanup.
