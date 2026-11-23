#!/usr/bin/env python3
"""Haal een vaste versie van het Npuls-assetpakket op en print het pad (alleen stdlib, Python 3.9+).

  npuls_assets.py ensure --version 0.1.0 [--local <map>]   print absoluut pad naar de pakketmap
  npuls_assets.py path <relatief> --version 0.1.0          print pad van een bestand in het pakket

--local <map> of env NPULS_ASSETS_DIR: gebruik een lokale npuls-assets/ (voor testen), geen download.
Exit-codes: 0 ok, 1 bestand niet in pakket, 2 download mislukt (offline?), 3 verificatie mislukt, 4 ongeldige invoer.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_VERSION = "0.1.0"
URL = "https://github.com/cedanl/.github/releases/download/npuls-assets-v{v}/npuls-assets-{v}.zip"
CACHE = Path.home() / ".cache" / "ceda" / "npuls-assets"


def fail(code, msg):
    print(f"fout: {msg}", file=sys.stderr)
    sys.exit(code)


def verify(folder):
    """Controleer alle bestanden tegen manifest.json. Geeft een lijst met afwijkingen."""
    try:
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"manifest.json onleesbaar: {e}"]
    bad = []
    for f in manifest.get("files", []):
        p = folder / f["path"]
        if not p.is_file():
            bad.append(f"ontbreekt: {f['path']}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != f["sha256"]:
            bad.append(f"sha256 wijkt af: {f['path']}")
    return bad


def ensure(version, local):
    local = local or os.environ.get("NPULS_ASSETS_DIR")
    if local:
        folder = Path(local).expanduser().resolve()
        if not (folder / "manifest.json").is_file():
            fail(4, f"geen manifest.json in {folder}")
        return folder
    folder = CACHE / version
    if (folder / "manifest.json").is_file() and not verify(folder):
        return folder
    url = URL.format(v=version)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except (urllib.error.URLError, OSError) as e:
        fail(2, f"download mislukt ({url}): {e}. Offline? Gebruik --local <map> of NPULS_ASSETS_DIR met een lokale npuls-assets/.")
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=CACHE, prefix=f".{version}-"))
    try:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for n in z.namelist():  # zip-slip voorkomen
                    if n.startswith("/") or ".." in Path(n).parts:
                        fail(3, f"onveilig pad in zip: {n}")
                z.extractall(tmp)
        except zipfile.BadZipFile:
            fail(3, "download is geen geldige zip")
        bad = verify(tmp)
        if bad:
            fail(3, "verificatie tegen manifest mislukt: " + "; ".join(bad[:5]))
        if json.loads((tmp / "manifest.json").read_text(encoding="utf-8")).get("version") != version:
            fail(3, "versie in manifest komt niet overeen met gevraagde versie")
        if folder.exists():
            shutil.rmtree(folder)
        tmp.rename(folder)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return folder


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("ensure", "path"):
        p = sub.add_parser(name)
        p.add_argument("--version", default=DEFAULT_VERSION)
        p.add_argument("--local")
        if name == "path":
            p.add_argument("relative")
    a = ap.parse_args()
    folder = ensure(a.version, a.local)
    if a.cmd == "ensure":
        print(folder)
        return
    target = (folder / a.relative).resolve()
    if folder not in target.parents or not target.is_file():
        fail(1, f"{a.relative} niet in pakket {folder}")
    print(target)


if __name__ == "__main__":
    main()
