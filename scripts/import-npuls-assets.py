#!/usr/bin/env python3
"""Eenmalige import: vult npuls-assets/ vanuit de bronmap (clidev-presentaties/public/npuls).
Gebruik: python scripts/import-npuls-assets.py <bronmap>   (vereist Pillow voor PNG-optimalisatie)
Lettertypebestanden worden bewust NIET meegenomen (licentie)."""
import re, shutil, sys, unicodedata
from pathlib import Path

src = Path(sys.argv[1]).resolve()
dst = Path(__file__).resolve().parent.parent / "npuls-assets"

def kebab(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9.]+", "-", s).strip("-")

def png_opt(a, b):
    try:
        from PIL import Image
        Image.open(a).save(b, optimize=True)
    except Exception:
        shutil.copy2(a, b)

def svg_min(text):
    if "url(#" in text or "href=" in text:  # id-verwijzingen: niet aanraken
        return text
    if "fill=" not in text:  # kleur zit in <style>/class (bv. logo): laten staan
        return re.sub(r"\s+", " ", re.sub(r"<!--.*?-->", "", text, flags=re.S)).replace("> <", "><").strip()
    text = re.sub(r"<\?xml[^>]*\?>", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<style>.*?</style>", "", text, flags=re.S)       # fill staat al als attribuut
    text = re.sub(r'\s(class|xml:space|overflow|id)="[^"]*"', "", text)
    text = re.sub(r'\sxmlns:xlink="[^"]*"', "", text) if "xlink:" not in text else text
    return re.sub(r"\s+", " ", text).replace("> <", "><").strip()

for d in ("pptx", "logos", "vormen", "illustraties", "slides-preview", "web/vormen", "web/logos"):
    (dst / d).mkdir(parents=True, exist_ok=True)

shutil.copy2(src / "Npuls_powerpoint-template.potx", dst / "pptx/Npuls_powerpoint-template.potx")
for f in (src / "logos").iterdir():
    (png_opt if f.suffix == ".png" else shutil.copy2)(f, dst / "logos" / f.name)
shutil.copy2(src / "npuls_logo.jpg", dst / "logos/npuls-logo-roze.jpg")
for f in (src / "vormen").glob("*.svg"):
    shutil.copy2(f, dst / "vormen" / f.name)

# Illustraties en layout-graphics rechtstreeks uit de potx (officiele bron)
import hashlib, json, os, zipfile
from xml.etree import ElementTree as ET
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
R = "{%s}embed" % NS["r"]
zf = zipfile.ZipFile(src / "Npuls_powerpoint-template.potx")

def pics(part):
    """Geeft [(shape-naam, y, x, svg-pad of None, png-pad)] in leesvolgorde."""
    d, b = os.path.split(part)
    rels = {x.get("Id"): os.path.normpath(os.path.join(d, x.get("Target"))).replace("\\", "/")
            for x in ET.fromstring(zf.read(f"{d}/_rels/{b}.rels"))}
    out = []
    for pic in ET.fromstring(zf.read(part)).iter("{%s}pic" % NS["p"]):
        c = pic.find("p:nvPicPr/p:cNvPr", NS); bl = pic.find("p:blipFill/a:blip", NS)
        off = pic.find("p:spPr/a:xfrm/a:off", NS)
        ids = [bl.get(R)] + [e.get(R) for e in bl.iter() if e.tag.endswith("svgBlip")]
        paths = [rels[i] for i in ids if i in rels]
        svg = next((x for x in paths if x.endswith(".svg")), None)
        out.append((c.get("name"), int(off.get("y")) if off is not None else 0, int(off.get("x")) if off is not None else 0,
                    svg, next((x for x in paths if x.endswith(".png")), None)))
    return out

mapping, seen = {}, {}
n = 0
for slide in (18, 19):
    for name, y, x, svg, png in sorted(pics(f"ppt/slides/slide{slide}.xml"), key=lambda t: (round(t[1] / 600000), t[2])):
        if not svg:
            continue  # alleen PNG (geen illustratie): overgeslagen
        data = zf.read(svg); h = hashlib.sha256(data).hexdigest()
        if h in seen:
            continue
        n += 1; k = f"illustratie-{n:02d}.svg"; seen[h] = k
        (dst / "illustraties" / k).write_bytes(data)
        mapping[k] = f"bron: potx slide {slide}, shape '{name}' ({svg})"
# vormen/ en logos/ komen uit de communicatiekit; vormen/ is gecontroleerd tegen slideLayouts/slideMasters van de potx (zelfde paden)
(dst / "illustraties-mapping.json").write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

for f in sorted((src / "powerpoint_slides").iterdir()):
    png_opt(f, dst / "slides-preview" / (re.sub(r"(\d+)$", lambda m: m.group(1).zfill(2), kebab(f.stem)) + ".png"))

# web/: geoptimaliseerde kopieën + sprite
sym = []
for f in sorted((dst / "vormen").glob("*.svg")):
    t = svg_min(f.read_text(encoding="utf-8"))
    (dst / "web/vormen" / f.name).write_text(t, encoding="utf-8")
    m = re.match(r'<svg([^>]*)>(.*)</svg>$', t, flags=re.S)
    assert m, f
    if f.stem in ("npuls-logo", "cc-by-sa"):
        continue
    vb = re.search(r'viewBox="([^"]*)"', m.group(1))
    if vb:
        box = vb.group(1)
    else:
        w = re.search(r'width="([\d.]+)', m.group(1)); h = re.search(r'height="([\d.]+)', m.group(1))
        box = f"0 0 {w.group(1)} {h.group(1)}"
    sym.append(f'<symbol id="vorm-{f.stem}" viewBox="{box}">{m.group(2)}</symbol>')
(dst / "web/sprite.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="display:none">'
    + "".join(sym) + "</svg>\n", encoding="utf-8")
for f in (dst / "logos").glob("*.png"):
    shutil.copy2(f, dst / "web/logos" / f.name)
shutil.copy2(dst / "vormen/npuls-logo.svg", dst / "web/logos/npuls-logo.svg") if False else \
    (dst / "web/logos/npuls-logo.svg").write_text(svg_min((dst / "vormen/npuls-logo.svg").read_text(encoding="utf-8")), encoding="utf-8")
print("klaar:", dst)
