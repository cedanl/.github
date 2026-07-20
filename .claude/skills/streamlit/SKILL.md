---
name: streamlit
description: Build a CEDA Streamlit app the house way — src/ layout with a frontend/ page tree, st.navigation multipage wiring, npuls logo/branding, and uv+Docker packaging. Use when creating a new Streamlit app, adding a page, or structuring the frontend of a CEDA tool.
---

# streamlit

CEDA Streamlit apps follow a shared shape. Start from `streamlit-template-app`
for a new app; match the target repo's existing structure when extending one.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/streamlit`, or
automatically) when you create a new Streamlit app, add a page, or structure the
frontend of a CEDA tool. It is reference/convention.

## Project layout
```
src/
├── main.py                 # entrypoint: page config, navigation, logo
├── frontend/               # pages grouped by subdirectory
│   ├── Overview/Home.py    # (or Home/Home.py)
│   ├── Files/...
│   └── Modules/...
├── backend/                # non-UI logic (file handling, processing)
├── config/                 # config.yaml + helpers
└── assets/                 # npuls_logo.png etc.
```

## Two multipage patterns (match the repo)
1. **Auto-discovery** (`streamlit-template-app`): `config/screen_scanner.py`
   provides `get_screens()` + `group_pages_by_subdirectory()`; `main.py` calls
   `st.navigation(grouped_pages)`. Add a page = drop a `.py` in a `frontend/`
   subdir; no wiring needed.
2. **Explicit** (`1cijferho`): `main.py` declares each page with
   `st.Page("frontend/<Group>/<Page>.py", icon="…", title="…")` and passes the
   list to `st.navigation([...])`. Add a page = add a `.py` **and** a `st.Page`
   line.

## main.py essentials
```python
st.set_page_config(page_title="CEDA …", page_icon=":material/edit:")
pg = st.navigation(pages)          # grouped dict or explicit list
st.logo("src/assets/npuls_logo.png")
pg.run()
```
Global CSS is applied once in `main.py` and shared across pages. For NPULS
house style, see the `npuls-huisstijl` skill.

## Auth (optional, SRAM)
Apps gate access with OIDC via SRAM when `OIDC_PROVIDER` is set — wrap the app
in `require_authentication()`. See /sram-oidc. Auth is disabled cleanly when
the env vars are absent, so local dev needs no login.

## Packaging & run
- Deps via **uv** (`pyproject.toml` + `uv.lock`); run `uv run streamlit run src/main.py`.
- Container + local dev: see /docker. Deploy on SDP: see /sdp-onboard,
  /surf-sdp-helm-flux (Streamlit URL pattern `https://<app>.<env>.sdp.surf.nl`,
  health probe `/healthz`, ingress port 8501).

## Important
- **Match the repo's multipage pattern** (auto-discovery vs explicit `st.Page`);
  don't mix them.
- Streamlit UI can't be meaningfully unit-tested headless — run the app and click
  through the golden path before calling a UI change done; say so if you can't.
- Auth is **opt-in**: no `OIDC_PROVIDER` → app runs open (fine for local dev).
  See /sram-oidc. Packaging/deploy: /docker, /sdp-onboard.
- Applies to cedanl repos.
