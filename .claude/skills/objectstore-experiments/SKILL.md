---
name: objectstore-experiments
description: Exercise and verify S3 features against the SURF Object Store (Ceph RGW) with boto3 — versioning, lifecycle policies, multipart upload, SSE-C encryption, and presigned URLs — plus the known Ceph-vs-AWS behavioural quirks. Use when testing Object Store functionality, writing boto3 against objectstore.surf.nl, or checking whether an S3 feature behaves as it does on AWS.
---

# objectstore-experiments

Runnable feature checks against the **SURF Object Store** (Ceph RGW,
`https://objectstore.surf.nl`) using boto3 and the `object-store` aws profile.
Grounded in the `object-store-evaluation` repo's `functionality/` + `security/`
notebooks and the accompanying `experiment_*.py` scripts, all verified against a
live CEDA account.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/objectstore-experiments`,
or automatically) when you test Object Store features, write boto3 against
`objectstore.surf.nl`, or need to know whether an S3 feature behaves the same as
on AWS. It is reference/convention. For getting access + profiles first, see
[[objectstore-onboarding]].

## Setup (shared by every experiment)
```python
import boto3
c = boto3.Session(profile_name="object-store").client("s3")   # endpoint from ~/.aws/config
```
Run scripts with an isolated, recent boto3 (endpoint_url in config needs boto3 that reads it):
```bash
uv run --with boto3,requests python3 experiment_*.py
```

## Features verified to work (same as AWS S3)
- **Versioning**: `put_bucket_versioning(Status="Enabled")`. Re-PUT a key → new
  `VersionId`; `delete_object` places a **delete marker** (data retained);
  restore by deleting the marker version. `list_object_versions` shows both
  `Versions` and `DeleteMarkers`.
- **Lifecycle**: `put_bucket_lifecycle_configuration` with
  `NoncurrentVersionExpiration` and/or `Expiration` (day-granular; runs on Ceph's
  own schedule — not observable in real time).
- **Multipart**: `create_multipart_upload` → `upload_part` (track `PartNumber` +
  `ETag`, parts ≥ 5 MiB except the last) → `complete_multipart_upload`.
  `list_multipart_uploads` shows in-progress; `abort_multipart_upload` cleans up.
- **SSE-C**: `put_object(SSECustomerKey=<32 bytes>, SSECustomerAlgorithm="AES256")`.
  GET requires the same key. Server echoes `SSECustomerKeyMD5` proving it used your key.
- **Presigned URLs**: `generate_presigned_url("get_object"|"put_object", ...)`.
  A credential-less client can PUT/GET via the URL (`requests.put/get`).

## Ceph-vs-AWS quirks (empirically confirmed — do not assume AWS behaviour)
1. **Presigned URLs default to SigV2** (`?AWSAccessKeyId=...&Signature=...`), not
   SigV4. Both work; force SigV4 with `Config(signature_version="s3v4")` if a tool
   requires it.
2. **SSE-C key errors return `400 InvalidArgument`**, not AWS's `403 AccessDenied`
   — for *both* a missing key and a wrong key. Assert "GET is denied", not a
   specific status code.
3. **No service-managed encryption**: `ServerSideEncryption="aws:kms"` (and
   SSE-S3) is **rejected** (`400`). SSE-C (customer-provided keys) is the *only*
   at-rest encryption exposed via the API. This is a deliberate SURF limitation.
4. **Lifecycle rules are normalised on read-back**: a rule sent with
   `Filter={"Prefix": ""}` comes back as a legacy top-level `Prefix` (no `Filter`
   wrapper). Functionally equivalent, but "what I sent" ≠ "what's stored" byte-wise.
5. **Multipart ETag** of a completed object is `<hash>-<numparts>` (e.g. `...-5`) —
   the `-N` suffix marks a multipart object; it is not an MD5 of the whole object.

## Reference scripts (bundled in `scripts/`)
Runnable against the `object-store` profile; each creates and cleans up its own
bucket. Also mirrored as notebooks in the `object-store-evaluation` repo.
- `scripts/experiment_versioning.py` — versioning + restore + presigned GET
- `scripts/experiment_lifecycle.py` — policy round-trip (+ deferred `check`)
- `scripts/experiment_multipart.py` — parts, abort, sha256 integrity
- `scripts/experiment_sse_c.py` — SSE-C enforcement + service-managed probe
- `scripts/experiment_presigned_put.py` — presigned PUT, SigV2 vs SigV4

## Important
- Use the **non-root `object-store` profile** for all of this — never the root
  profile (see [[objectstore-onboarding]]).
- Experiments **create and delete buckets** — each script cleans up after itself.
  Bucket names must be lowercase and unique within the store; parameterise them so
  reruns don't collide on an existing name.
- Lifecycle expiration cannot be observed live (day granularity + Ceph's schedule)
  — verify the policy *round-trips*, then re-check after a day.
- SSE-C keys are **client-side secrets**: if you lose the key, the object is
  unrecoverable. There is no service-managed fallback on this store.
- Applies to cedanl repos using the SURF Object Store.
