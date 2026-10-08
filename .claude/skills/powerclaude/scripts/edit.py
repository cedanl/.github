#!/usr/bin/env python3
"""Bestaande .pptx aanpassen zonder opnieuw te bouwen: lezen, tekst vervangen, logo wisselen, slides klonen of verplaatsen.

Voor decks die je niet zelf met build.mjs hebt gemaakt (bijvoorbeeld een voorstel dat al gedeeld is, of een
deck van een collega). Voor een nieuw deck gebruik je build.mjs en een deck-spec, geen edit.py.

Vereist: pip install python-pptx

Gebruik:
  python edit.py dump      in.pptx [--notes]
  python edit.py replace   in.pptx uit.pptx map.json [--lenient]
  python edit.py beeldmerk in.pptx uit.pptx
  python edit.py media     in.pptx uit.pptx ppt/media/image1.png nieuw.png [...paren]
  python edit.py kloon     in.pptx uit.pptx --slide N --naar M
  python edit.py verplaats in.pptx uit.pptx --slide N --naar M

Slidenummers beginnen bij 1. `--naar M` is de positie die de slide daarna heeft.
"""
import argparse
import copy
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

for _stroom in (sys.stdout, sys.stderr):  # Windows-consoles gebruiken anders cp1252 en struikelen over tekens als →
    _stroom.reconfigure(encoding="utf-8")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"


# ---------- lezen ----------

def tekstframes(slide, notes=False):
    for sh in slide.shapes:
        yield from frames_in(sh)
    if notes and slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
        yield slide.notes_slide.notes_text_frame


def frames_in(shape):
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for sub in shape.shapes:
            yield from frames_in(sub)
    elif shape.has_text_frame:
        yield shape.text_frame
    elif getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                yield cell.text_frame


def dump(inp, notes):
    prs = Presentation(inp)
    for n, slide in enumerate(prs.slides, 1):
        print(f"--- slide {n} ({slide.slide_layout.name})")
        for sh in slide.shapes:
            tekst = " | ".join(f.text.replace("\n", " / ") for f in frames_in(sh) if f.text.strip())
            soort = sh.shape_type
            if tekst:
                print(f"  [{sh.shape_id}] {sh.name}: {tekst}")
            elif soort == MSO_SHAPE_TYPE.PICTURE:
                print(f"  [{sh.shape_id}] {sh.name}: (afbeelding)")
        if notes and slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
            t = slide.notes_slide.notes_text_frame.text.strip()
            if t:
                print(f"  notities: {t[:200]}")


# ---------- tekst vervangen ----------

def vervang_in_alinea(para, oud, nieuw):
    """Vervangt `oud` in een alinea, ook als het over meerdere runs is verdeeld. Geeft het aantal vervangingen terug."""
    n = 0
    for r in para.runs:
        if oud in r.text:
            n += r.text.count(oud)
            r.text = r.text.replace(oud, nieuw)
    if n:
        return n
    volledig = "".join(r.text for r in para.runs)
    if oud in volledig and para.runs:  # opmaak van de eerste run blijft behouden
        n = volledig.count(oud)
        para.runs[0].text = volledig.replace(oud, nieuw)
        for r in para.runs[1:]:
            r._r.getparent().remove(r._r)
    return n


def replace(inp, uit, mapfile, lenient):
    mapping = json.loads(Path(mapfile).read_text(encoding="utf-8"))
    prs = Presentation(inp)
    telling = {oud: 0 for oud in mapping}
    for slide in prs.slides:
        for tf in tekstframes(slide, notes=True):
            for para in tf.paragraphs:
                for oud, nieuw in mapping.items():
                    telling[oud] += vervang_in_alinea(para, oud, nieuw)
    ontbreekt = [o for o, n in telling.items() if n == 0]
    for oud, n in telling.items():
        print(f"{n:3d}x  {oud[:70]}")
    if ontbreekt and not lenient:
        sys.exit(f"FOUT: {len(ontbreekt)} zoekterm(en) niet gevonden (gebruik --lenient om dat toe te staan)")
    prs.save(uit)
    print("->", uit)


# ---------- beeldmerk ----------

def voorinstelling(shape):
    geom = shape._element.spPr.find(f"{A}prstGeom") if hasattr(shape._element, "spPr") else None
    return geom.get("prst") if geom is not None else None


def stipkleur(shape):
    try:
        rgb = str(shape.fill.fore_color.rgb)
    except Exception:
        return "zwart"
    r, g, b = (int(rgb[i:i + 2], 16) for i in (0, 2, 4))
    return "wit" if 0.299 * r + 0.587 * g + 0.114 * b > 140 else "zwart"


def beeldmerk(inp, uit):
    """Vervangt een zelfgetekend of indicatief stippenmerk (>= 20 kleine cirkels) door het echte Npuls-beeldmerk."""
    max_stip = int(0.12 * 914400)
    prs = Presentation(inp)
    vervangen = 0
    for slide in prs.slides:
        stippen = [s for s in slide.shapes
                   if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and voorinstelling(s) == "ellipse"
                   and s.width <= max_stip and s.height <= max_stip]
        if len(stippen) < 20:
            continue
        links = min(s.left for s in stippen)
        boven = min(s.top for s in stippen)
        rechts = max(s.left + s.width for s in stippen)
        onder = max(s.top + s.height for s in stippen)
        zijde = max(rechts - links, onder - boven)
        cx, cy = (links + rechts) // 2, (boven + onder) // 2
        kleur = stipkleur(stippen[0])
        for s in stippen:
            s._element.getparent().remove(s._element)
        pic = slide.shapes.add_picture(str(ASSETS / f"npuls-beeldmerk-{kleur}.png"), cx - zijde // 2, cy - zijde // 2, zijde, zijde)
        pic.name = "Npuls beeldmerk"
        vervangen += 1
    prs.save(uit)
    print(f"beeldmerk vervangen op {vervangen} slides -> {uit}")


# ---------- afbeeldingen ----------

def media(inp, uit, paren):
    """Vervangt de inhoud van een afbeelding in het bestand (bijvoorbeeld ppt/media/image1.png, zonder
    beginslash: Git Bash maakt van een beginslash een Windows-pad). Alle slides die die afbeelding gebruiken, krijgen
    de nieuwe."""
    if len(paren) % 2:
        sys.exit("FOUT: geef paren van onderdeelnaam en nieuw bestand")
    prs = Presentation(inp)
    gewenst = {paren[i].lstrip("/"): Path(paren[i + 1]).read_bytes() for i in range(0, len(paren), 2)}
    gevonden = set()
    for part in prs.part.package.iter_parts():
        naam = str(part.partname).lstrip("/")
        if naam in gewenst:
            part._blob = gewenst[naam]
            gevonden.add(naam)
    ontbreekt = set(gewenst) - gevonden
    if ontbreekt:
        sys.exit(f"FOUT: niet gevonden in het bestand: {', '.join(sorted(ontbreekt))}")
    prs.save(uit)
    print(f"{len(gevonden)} afbeelding(en) vervangen -> {uit}")


# ---------- slides ----------

def verplaats_slide(prs, van, naar):
    lijst = prs.slides._sldIdLst
    ids = list(lijst)
    el = ids[van - 1]
    lijst.remove(el)
    lijst.insert(naar - 1, el)


def kloon(inp, uit, nummer, naar):
    prs = Presentation(inp)
    bron = prs.slides[nummer - 1]
    nieuw = prs.slides.add_slide(bron.slide_layout)
    for sh in list(nieuw.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in bron.shapes:
        el = copy.deepcopy(sh._element)
        for blip in el.iter(f"{A}blip"):
            rid = blip.get(R_EMBED)
            if rid:
                rel = bron.part.rels[rid]
                blip.set(R_EMBED, nieuw.part.relate_to(rel.target_part, rel.reltype))
        nieuw.shapes._spTree.append(el)
    if bron.has_notes_slide and bron.notes_slide.notes_text_frame is not None:
        ns = nieuw.notes_slide
        if ns.notes_text_frame is None:  # notitiemaster zonder tekstvak: neem de structuur van de bron over
            for sh in list(ns.shapes):
                sh._element.getparent().remove(sh._element)
            for sh in bron.notes_slide.shapes:
                ns.shapes._spTree.append(copy.deepcopy(sh._element))
        ns.notes_text_frame.text = bron.notes_slide.notes_text_frame.text
    verplaats_slide(prs, len(prs.slides), naar)
    prs.save(uit)
    print(f"slide {nummer} gekloond naar positie {naar} -> {uit}")


def verplaats(inp, uit, nummer, naar):
    prs = Presentation(inp)
    verplaats_slide(prs, nummer, naar)
    prs.save(uit)
    print(f"slide {nummer} verplaatst naar positie {naar} -> {uit}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dump"); d.add_argument("inp"); d.add_argument("--notes", action="store_true")
    r = sub.add_parser("replace"); r.add_argument("inp"); r.add_argument("uit"); r.add_argument("map"); r.add_argument("--lenient", action="store_true")
    b = sub.add_parser("beeldmerk"); b.add_argument("inp"); b.add_argument("uit")
    m = sub.add_parser("media"); m.add_argument("inp"); m.add_argument("uit"); m.add_argument("paren", nargs="+")
    for naam in ("kloon", "verplaats"):
        k = sub.add_parser(naam); k.add_argument("inp"); k.add_argument("uit")
        k.add_argument("--slide", type=int, required=True); k.add_argument("--naar", type=int, required=True)
    a = p.parse_args()
    if a.cmd == "dump":
        dump(a.inp, a.notes)
    elif a.cmd == "replace":
        replace(a.inp, a.uit, a.map, a.lenient)
    elif a.cmd == "beeldmerk":
        beeldmerk(a.inp, a.uit)
    elif a.cmd == "media":
        media(a.inp, a.uit, a.paren)
    elif a.cmd == "kloon":
        kloon(a.inp, a.uit, a.slide, a.naar)
    elif a.cmd == "verplaats":
        verplaats(a.inp, a.uit, a.slide, a.naar)


if __name__ == "__main__":
    main()
