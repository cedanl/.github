# Variant A (standaard voor nieuwe repos: GitHub Pages op "GitHub Actions" met pyproject.toml)
name: Docs

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Install docs dependencies
        run: uv sync --group docs

      - name: Build docs (strict)
        run: uv run mkdocs build --strict

      - name: Upload Pages artifact
        if: github.event_name != 'pull_request'
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    needs: build
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

# ---
# Variant B (voor repos zonder pyproject.toml of met bestaande gh-pages branch, zoals cedanl/.github):
# Gebruik in beide jobs `uv run --with mkdocs-material` (voeg `--with mkdocs-include-markdown-plugin` toe als de site include-markdown gebruikt):
# - job `build`: `mkdocs build --strict` (ook op pull_request)
# - job `deploy` (`if: github.event_name != 'pull_request'`, `permissions: contents: write`): `mkdocs gh-deploy --force`
