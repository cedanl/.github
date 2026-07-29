---
name: surfdrive
description: Integrate SurfDrive into a CEDA data pipeline — download a CSV from a SurfDrive public share (share token + password) and hand it onward (typically to MinIO). Use when wiring SurfDrive ingest, setting SURFDRIVE_* config, or debugging a SurfDrive download step.
---

# surfdrive

CEDA ETL repos ingest source data from **SurfDrive public shares**. The pattern
comes from `instroom-etl-ho/src/transport.py`.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/surfdrive`, or
automatically) when you wire SurfDrive ingest, set `SURFDRIVE_*` config, or debug
a SurfDrive download step. It is reference/convention.

## Config (env vars)
- `SURFDRIVE_SHARE_TOKEN` — the public-share token (the id in the share URL).
- `SURFDRIVE_PASSWORD` — the share's password.
Both are provided via `.env` locally (compose reads `${SURFDRIVE_*}`) and via
SOPS-encrypted secrets in deployed environments — see /sdp-secrets-management.
Never commit them in plaintext.

## Usage pattern (transport.py)
```python
import surfdrive
import minio_file

df = surfdrive.download_surfdrive_csv(filename)   # pulls from the share
if df is None:
    raise Exception(f"Can not download {filename}")
# ... then push onward, e.g. to MinIO:
minio = minio_file.create_connection(account="HO")
minio_file.upload_file(conn=minio, local_path=fullpath, remote_path=filename)
```
So the flow is: **SurfDrive share → download CSV → upload to MinIO**. The
`transport` step takes a filename argument and no-ops (with a message) when none
is given.

## Note on the `surfdrive` module
`surfdrive` (and `minio_file`) are imported as packages — they are **not** vendored
in the ETL repos' source. They're CEDA-internal/external dependencies. If you need
the module's internals (auth mechanism, WebDAV vs public-share API), locate the
package rather than assuming; this skill covers the *usage contract*
(`download_surfdrive_csv(filename) -> DataFrame | None`), not its implementation.

## Important
- `SURFDRIVE_SHARE_TOKEN` / `SURFDRIVE_PASSWORD` are **secrets** — never commit in
  plaintext (SOPS in deployed envs; see /sdp-secrets-management).
- The `surfdrive`/`minio_file` modules are **not vendored** in the ETL repos —
  this skill covers the *usage contract* (`download_surfdrive_csv(filename) ->
  DataFrame | None`), not the implementation. Locate the package for internals.
- A failed download returns `None` — the step must raise, not proceed silently.
- Part of the ETL container flow — see /etl-pipeline and /docker.
- Applies to cedanl repos.
