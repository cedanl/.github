"""Npuls-assetpakket vinden vanuit Python (zelfde regels als npuls-assets.mjs).

1. env NPULS_ASSETS_DIR
2. python <vormgever>/scripts/npuls_assets.py ensure --version <assets.lock> -> laatste regel stdout
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]


def locked_version() -> str:
    lock = (SKILL_DIR / "assets.lock").read_text(encoding="utf-8")
    m = re.search(r"^npuls-assets\s*==\s*([0-9][\w.+-]*)\s*$", lock, re.M)
    if not m:
        raise RuntimeError(f"assets.lock: geen regel 'npuls-assets==<versie>' in {SKILL_DIR / 'assets.lock'}")
    return m.group(1)


def _helper() -> Path | None:
    rel = Path("vormgever-npuls-huisstijl", "scripts", "npuls_assets.py")
    home = Path.home()
    for p in (SKILL_DIR.parent / rel, home / ".claude/skills" / rel, home / ".agents/skills" / rel,
              home / "Projects/.github/.claude/skills" / rel):
        if p.exists():
            return p
    return None


def npuls_assets_dir() -> Path:
    env = os.environ.get("NPULS_ASSETS_DIR")
    if env:
        if not Path(env).exists():
            raise RuntimeError(f"NPULS_ASSETS_DIR={env} bestaat niet")
        return Path(env).resolve()
    helper = _helper()
    if not helper:
        raise RuntimeError("vormgever-npuls-huisstijl/scripts/npuls_assets.py niet gevonden; zet NPULS_ASSETS_DIR")
    r = subprocess.run([sys.executable, str(helper), "ensure", "--version", locked_version()],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"npuls_assets.py ensure faalde:\n{r.stderr}")
    d = Path(r.stdout.strip().splitlines()[-1].strip())
    if not d.exists():
        raise RuntimeError(f"npuls_assets.py gaf {d}, maar dat pad bestaat niet")
    return d.resolve()
