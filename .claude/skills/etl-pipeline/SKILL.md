---
name: etl-pipeline
description: Build or extend a CEDA instroom-style ETL pipeline — a containerized transport step that pulls source data (e.g. SurfDrive), processes it, and lands it in MinIO, wired via docker-compose env and deployed through the GitLab/SDP flow. Use when working on instroom-etl-* / instroom-ml or a similar ingest→store pipeline.
---

# etl-pipeline

The `instroom-etl-ho` / `instroom-etl-wo` / `instroom-ml` repos share one shape:
a small, single-purpose **containerized transport step**. Grounded in
`instroom-etl-ho`.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/etl-pipeline`, or
automatically) when you work on `instroom-etl-*` / `instroom-ml` or a similar
ingest→store pipeline. It is reference/convention.

## Shape
```
src/transport.py        # entrypoint: ingest → (process) → store
Dockerfile              # uv-based image (see /docker)
docker-compose.yml      # env wiring + local run
env.txt / .env          # SURFDRIVE_* + MINIO_* (gitignored for real values)
```
The transport step takes a filename argument, downloads it from the source,
and uploads to MinIO. It exits cleanly (with a message) when no filename is given.

## Data flow
```
SurfDrive public share  →  download CSV  →  upload to MinIO
   (SURFDRIVE_*)            surfdrive.py       minio_file (account=…)
```
- Ingest: `surfdrive.download_surfdrive_csv(filename)` — see /surfdrive.
- Store: `minio_file.create_connection(account="HO")` + `upload_file(...)`.
- `instroom-ml` extends this with a modelling step on the stored data.

## Config (docker-compose env)
Compose passes env from `.env`:
`SURFDRIVE_SHARE_TOKEN`, `SURFDRIVE_PASSWORD`, `MINIO_ACCESS_KEY`,
`MINIO_SECRET_KEY`, `MINIO_ENDPOINT`, `MINIO_BUCKET`. In deployed environments
these come from SOPS-encrypted secrets — see /sdp-secrets-management.

## Local dev
- `docker compose build && docker compose up`; the dev compose often runs
  `sleep infinity` and bind-mounts `src/` so you `docker exec` in and run the
  step by hand while iterating.
- Run the step: `uv run python src/transport.py <filename>`.

## Deploy
Built image is deployed via the GitLab/SDP flow (cross-pipeline trigger hands the
image digest to the config repo). See /gitlab-ci and /surf-sdp-helm-flux
(deploy by **image digest**, not floating tags).

## Important
- **Verify a run actually lands the file in MinIO** (list the bucket) before
  calling it done — a silent download failure returns `None`, which the step must
  raise on.
- Config secrets (`SURFDRIVE_*`, `MINIO_*`) via `.env` locally, SOPS in deployed
  envs — never commit plaintext (see /sdp-secrets-management).
- Deploy by **image digest**, not floating tags (see /gitlab-ci,
  /surf-sdp-helm-flux). Ingest specifics: /surfdrive.
- Applies to cedanl repos.
