---
name: docker
description: Containerize a CEDA app the house way — a uv-based Python image, non-root runtime user, pinned apt packages, and a docker-compose for local dev. Use when adding or editing a Dockerfile / docker-compose.yml in a CEDA repo, or debugging a container build.
---

# docker

CEDA repos ship a Dockerfile + docker-compose per repo. Match the existing
conventions (grounded in `text-analysis/Dockerfile` and `docs/gitlab.md`); read
the target repo's current Dockerfile first.

## Image conventions
- **Base:** `python:3.12-slim` (multi-arch: `FROM --platform=${BUILDPLATFORM} ...`).
- **Security updates:** `apt-get update && apt-get -y upgrade`, install only what's
  needed with `--no-install-recommends`, and **pin apt package versions**
  (`cron=3.0pl1-162`, …). End the layer with `rm -rf /var/lib/apt/lists/*`.
- **uv for deps:** copy `pyproject.toml` + `uv.lock`, then `uv sync --frozen --no-dev`.
  (Older repos `pip install -r requirements.txt`; match what the repo uses.)
- **Non-root runtime.** Create a user (`useradd -m streamlit`), `chown` what it
  needs, `USER <name>` before the app runs. Never run the service as root.
- **Entrypoint** for Streamlit apps: `CMD ["uv", "run", "streamlit", "run", "src/main.py"]`.

## Best practices (from docs/gitlab.md)
1. Multi-stage builds to shrink the image where it helps.
2. Combine related `RUN` commands to reduce layers.
3. Specific version tags on the base image (not `latest`).
4. Remove build-only deps after use.
5. Non-root user (see above).
6. Include a healthcheck (compose or Dockerfile) — Streamlit apps expose `/healthz`.

## Lint before committing
```bash
hadolint Dockerfile
```

## docker-compose (local dev)
- Env comes from a **`.env`** file (gitignored); compose references
  `${VAR}` (e.g. `MINIO_*`, `SURFDRIVE_*` — see [[surfdrive]]).
- Bind-mount `src/` for live editing during dev.
- Common commands:
  ```bash
  docker compose build
  docker compose up          # -d for detached
  docker compose down        # -v to drop volumes
  docker exec -ti <svc> bash # shell in; -u root for maintenance
  ```

## Honesty
A local `docker compose up` validates the image builds and starts — it does not
prove the deployed behavior on SDP (that's Flux/GitLab CI; see [[surf-sdp-helm-flux]]).
Verify the container actually serves before calling it done.
