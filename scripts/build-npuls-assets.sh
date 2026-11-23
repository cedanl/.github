#!/usr/bin/env bash
# Bouwt dist/npuls-assets-<versie>.zip uit npuls-assets/ en regenereert npuls-assets/web/npuls.css (uit design-tokens.json)
# en npuls-assets/manifest.json.
#   --check  alleen controleren: faalt als de gecommitte npuls.css afwijkt van design-tokens.json (schrijft niets)
# Werkt in Git Bash en Linux; vereist alleen bash en Python 3.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || { echo "Python 3 niet gevonden" >&2; exit 1; }

if [ "${1:-}" = "--check" ]; then
  exec "$PY" -I "$ROOT/scripts/gen_npuls_css.py" --check "$ROOT"
fi
"$PY" -I "$ROOT/scripts/gen_npuls_css.py" "$ROOT"

VERSION="$(tr -d '[:space:]' < "$ROOT/npuls-assets/VERSION")"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Ongeldige VERSION: '$VERSION'" >&2; exit 1; }
# In CI: tag moet bij VERSION passen
if [ -n "${GITHUB_REF_NAME:-}" ] && [[ "$GITHUB_REF_NAME" == npuls-assets-v* ]] && [ "$GITHUB_REF_NAME" != "npuls-assets-v$VERSION" ]; then
  echo "Tag $GITHUB_REF_NAME komt niet overeen met VERSION $VERSION" >&2; exit 1
fi

"$PY" - "$ROOT" "$VERSION" <<'PYEOF'
import hashlib, json, sys, zipfile
from pathlib import Path

root, version = Path(sys.argv[1]), sys.argv[2]
pkg = root / "npuls-assets"
mapping = json.loads((pkg / "illustraties-mapping.json").read_text(encoding="utf-8"))
tegels = json.loads((pkg / "tegels-mapping.json").read_text(encoding="utf-8"))

def describe(rel):
    p = rel.split("/")
    if rel == "pptx/Npuls_powerpoint-template.potx": return ("pptx-template", "Npuls PowerPoint-template (19 slides)")
    if p[0] == "logos": return ("logo", "Npuls logo of beeldmerk (" + p[-1] + ")")
    if p[0] == "vormen": return ("vorm", "Npuls vorm of tegel (SVG)")
    if p[0] == "illustraties":
        m = mapping.get(p[-1], {})
        return ("illustratie", "Illustratie, bron: " + (m.get("bron", "") if isinstance(m, dict) else m))
    if p[0] == "tegels":
        m = tegels.get(p[-1], {})
        return ("tegel", "Gekleurde tegel van npuls.nl, bron: " + m.get("bron", ""))
    if p[0] == "huisstijlgids": return ("doc", "Officiele Npuls-huisstijlgids (PDF)")
    if p[0] == "ceda": return ("ceda", "Eigen CEDA-asset (" + p[-1] + ")")
    if p[0] == "slides-preview": return ("preview", "PNG-preview van templateslide")
    if rel == "web/npuls.css": return ("css", "CSS-variabelen, kleurcombinaties, typografie, logo en bogen")
    if rel == "web/sprite.svg": return ("sprite", "Alle vormen als <symbol id=vorm-...>")
    if p[0] == "web": return ("web", "Geoptimaliseerde kopie voor HTML")
    if rel == "fonts.md": return ("doc", "Uitleg lettertypen en licenties")
    if rel == "illustraties-mapping.json": return ("data", "Herkomst en oude naam per illustratie")
    if rel == "tegels-mapping.json": return ("data", "Herkomst per tegel")
    return ("doc", rel)

files = []
for f in sorted(pkg.rglob("*")):
    rel = f.relative_to(pkg).as_posix()
    if not f.is_file() or rel == "manifest.json": continue
    t, d = describe(rel)
    files.append({"path": rel, "type": t, "sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "description": d})
manifest = {"name": "npuls-assets", "version": version, "files": files}
(pkg / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

dist = root / "dist"; dist.mkdir(exist_ok=True)
out = dist / f"npuls-assets-{version}.zip"
if out.exists(): out.unlink()
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in sorted(pkg.rglob("*")):
        if f.is_file():
            zi = zipfile.ZipInfo(f.relative_to(pkg).as_posix(), (2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, f.read_bytes())
print(f"{out} ({out.stat().st_size / 1e6:.1f} MB, {len(files) + 1} bestanden)")
PYEOF
