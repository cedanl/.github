site_name: <site_name>
site_url: https://cedanl.github.io/<repo>/
site_description: <site_description>
repo_url: https://github.com/cedanl/<repo>
repo_name: cedanl/<repo>

docs_dir: docs

theme:
  name: material
  language: nl
  logo: assets/logos/npuls_logo.jpg
  favicon: assets/logos/beeldmerk.svg
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.indexes
    - navigation.path
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - toc.follow
  palette:
    - scheme: default
      primary: custom
      accent: custom

extra_css:
  - stylesheets/extra.css

nav:
  - Start: index.md
  - Aan de slag: aan-de-slag.md
  # Voeg alleen toe bij Python src/<package>/ met Google-style docstrings:
  # - API-referentie:
  #   - Overzicht: api/index.md

extra:
  generator: false

copyright: >-
  Centrum Educatieve Data Analyse (CEDA) · Onderdeel van <a href="https://npuls.nl/" target="_blank" rel="noopener">Npuls</a> · <a href="https://edu.nl/twt84" target="_blank" rel="noopener">CEDA-community</a> · <a href="mailto:ceda@surf.nl">ceda@surf.nl</a>

plugins:
  - search:
      lang: nl
  # Alleen toevoegen als docs/ een bestand uit de hoofdmap insluit (bijv. README.md):
  # - include-markdown
  # Voeg toe bij Python src/<package>/ API-documentatie:
  # - mkdocstrings:
  #     handlers:
  #       python:
  #         paths: [src]
  #         options:
  #           docstring_style: google
  #           show_source: false
  #           show_root_heading: true
  #           show_symbol_type_heading: true
  #           members_order: source

markdown_extensions:
  - attr_list
  - md_in_html
  - tables
  - admonition
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  # Vervang pymdownx.superfences hierboven door onderstaand blok als Mermaid gewenst is:
  # - pymdownx.superfences:
  #     custom_fences:
  #       - name: mermaid
  #         class: mermaid
  #         format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  # Voeg toe als MathJax gewenst is (samen met extra_javascript):
  # - pymdownx.arithmatex:
  #     generic: true
