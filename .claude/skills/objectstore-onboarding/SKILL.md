---
name: objectstore-onboarding
description: Take a user from "granted access" to a working, least-privilege setup on the SURF Object Store (Ceph RGW, S3-compatible at objectstore.surf.nl) — detect the account type, install/configure aws-cli, split a privileged root profile from a non-root working profile, and verify S3 access. Use when onboarding to Object Store, setting up aws profiles for objectstore.surf.nl, or debugging a login 401/AccessDenied.
---

# objectstore-onboarding

End-to-end path to get a user running on the **SURF Object Store**, an
S3-compatible service backed by **Ceph RGW** in SURF's Amsterdam data centers
(endpoint `https://objectstore.surf.nl`). Distilled from the SURF servicedesk
docs (Object Store landing + IAM account quickstart) and verified against a live
CEDA account; the profile names align with the `object-store-evaluation` repo's
boto3 notebooks.

**Account creation itself needs a SURF admin** — you cannot self-provision. If no
account/project exists yet, the first step is a servicedesk request; the rest of
this workflow starts once SURF has sent credentials.

## Workflow

When the user invokes `/objectstore-onboarding [optional: project name]`, walk
these steps in order. First determine the account type (step 1) — it decides
which auth path applies.

## 1. Determine the account type

SURF Object Store has **two** auth mechanisms; using the wrong one is the most
common cause of a `401`.

| Account | Auth | How you got it | Path |
|---------|------|----------------|------|
| **New (preferred)** | Ceph **internal IAM** | SURF emailed an S3 **access + secret key** for a root user | steps 2–6 |
| **Legacy** | OpenStack **Keystone** | you set `OS_*` env vars and run `openstack ec2 credentials create` | step 7 |

**If you were emailed an S3 access + secret key → new IAM account.** Ignore
Keystone/`openstack` entirely and follow steps 2–6. Quickstart:
`https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/302481491/`

## 2. Install aws-cli
```bash
brew install awscli   # the FORMULA — there is no awscli cask; installing a "cask" installs nothing
aws --version         # want v2.13+; it honors endpoint_url in config, so no per-command --endpoint-url
```

## 3. Configure the root profile (privileged — manage users only)
Name it for the project, e.g. `ceda-root`. **Never** name it `default`.
```bash
aws configure --profile ceda-root set aws_access_key_id     <ACCESS_KEY>
aws configure --profile ceda-root set aws_secret_access_key <SECRET_KEY>
aws configure --profile ceda-root set region                us-east-1     # dummy; RGW ignores it
aws configure --profile ceda-root set endpoint_url          https://objectstore.surf.nl
aws --profile ceda-root s3 ls        # empty output = authenticated OK
```

## 4. Rotate the emailed key
The key travelled over email + a one-time link, so replace it. **Order matters:
delete the old key only after the new one is confirmed working.**
```bash
aws --profile ceda-root iam create-access-key            # copy the new pair
aws configure --profile ceda-root set aws_access_key_id     <NEW_ID>
aws configure --profile ceda-root set aws_secret_access_key <NEW_SECRET>
aws --profile ceda-root s3 ls                            # confirm, THEN:
aws --profile ceda-root iam delete-access-key --access-key-id <OLD_ID>
```

## 5. Create a non-root working user
```bash
aws --profile ceda-root iam create-user --user-name <username>
aws --profile ceda-root iam create-access-key --user-name <username>   # copy the pair
aws --profile ceda-root iam attach-user-policy --user-name <username> \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess              # S3 yes, IAM no
```
The AWS-managed `AmazonS3FullAccess` ARN works on Ceph RGW.

## 6. Configure the working profile — name it `object-store`
The `object-store-evaluation` notebooks call `boto3.Session(profile_name="object-store")`,
so use that exact name and they (and /objectstore-experiments) work unchanged.
```bash
aws configure --profile object-store set aws_access_key_id     <NONROOT_ID>
aws configure --profile object-store set aws_secret_access_key <NONROOT_SECRET>
aws configure --profile object-store set region                us-east-1
aws configure --profile object-store set endpoint_url          https://objectstore.surf.nl
aws --profile object-store s3 mb s3://<username>-test-bucket && aws --profile object-store s3 ls
```
Success here = onboarding done. Hand off to /objectstore-experiments to
exercise features.

## 7. Legacy Keystone path (only if you were NOT given an S3 key)
Set env vars, then mint EC2 credentials. SURF CUA users use `CuaUsers` for both
domains; local Keystone users use `Default`.
```bash
export OS_AUTH_URL=https://objectstore.surf.nl:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_USERNAME=<user>  OS_PASSWORD=<pw>  OS_PROJECT_NAME=<project>
export OS_USER_DOMAIN_NAME=CuaUsers  OS_PROJECT_DOMAIN_NAME=CuaUsers
openstack token issue            # isolates auth failures from the ec2 step
openstack ec2 credentials create # yields access + secret S3 keys
```
Docs: `https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/112591313/`

## Debugging a 401 / AccessDenied
- **Wrong flow for the account type**: you ran `openstack ...` on an IAM account
  (or the reverse). Re-check which credential type SURF sent.
- **Legacy `openstack` 401**: wrong `OS_PASSWORD`, wrong domain (`Default` vs
  `CuaUsers`), or no access to `OS_PROJECT_NAME`. Isolate with `openstack token
  issue`, then `openstack project list`.
- **No project yet**: onboarding is partly manual on SURF's side — the
  account/project may need creating before any command works. Request it via the
  servicedesk (state the project name and whether it must be created).

## Important
- **Least privilege**: do daily work as the non-root `object-store` user; use the
  root profile *only* to create/rotate users and policies.
- **Credentials are secrets**: keep `~/.aws/{config,credentials}` at mode `600`,
  never commit them, never paste them into chats/logs/issues. Prefer named
  profiles over hardcoded keys (why the eval notebooks reference profiles by name).
- **Rotate** any key that has been transmitted; `create-access-key` +
  `delete-access-key` retires one in seconds.
- **Personal vs project accounts**: a personal test account is not for production
  data — request a separate account for a real project.
- For Ceph-vs-AWS behavioural quirks and runnable feature demos, see
  /objectstore-experiments.
