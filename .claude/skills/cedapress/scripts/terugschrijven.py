#!/usr/bin/env python3
"""Tekst en notes uit een (op SharePoint bewerkte) pptx terughalen naar bron.md. SKELET.

Gebruik:
  python terugschrijven.py <deckmap> <bewerkte.pptx>            # toont of de pptx bewerkt is + diff per slide
  python terugschrijven.py <deckmap> <bewerkte.pptx> --json     # zelfde, als JSON voor de skill

Werkwijze (pitch cedanl/clidev-presentaties#16, gekozen optie b):
  1. <deckmap>/<naam>.pptx.meta.json bevat de hash van de geëxporteerde pptx en van de bron.
  2. Zelfde pptx-hash → niets te doen. Andere hash → de pptx is in PowerPoint bewerkt.
  3. Tekst en notes per slide uitlezen en naast bron.md zetten (diff).
  4. De skill (niet dit script) toont de diff, past bron.md aan na akkoord van de gebruiker,
     commit "wijziging uit pptx" en bouwt HTML en exports opnieuw.
Alleen tekst en notes komen terug; opmaak niet.

TODO(cedapress):
  - slides koppelen aan bron-slides op volgorde ná weglaten van alleen:html-slides, vaste CEDA-slides
    en de Einddia; nu alleen op volgorde van titels (zwak bij ingevoegde of verwijderde slides).
  - per veld (titel, tekst, notes) de wijziging terugzetten in bron.md in plaats van alleen tonen.
  - waarschuwen als bron.md sinds de export zelf ook gewijzigd is (meta.bron != huidige hash): conflict.
Vereist: pip install python-pptx
"""
from __future__ import annotations

import difflib
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_bron import bron_hash, parse, voor_vorm  # noqa: E402


def pptx_hash(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def lees_pptx(p: Path) -> list[dict]:
    from pptx import Presentation  # pas hier: --help werkt ook zonder python-pptx

    uit = []
    for i, slide in enumerate(Presentation(str(p)).slides, 1):
        titel = slide.shapes.title.text_frame.text.strip() if slide.shapes.title is not None else ""
        tekst = [sh.text_frame.text.strip() for sh in slide.shapes
                 if sh.has_text_frame and sh != slide.shapes.title and sh.text_frame.text.strip()]
        notes = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
            notes = slide.notes_slide.notes_text_frame.text.strip()
        uit.append({"nr": i, "titel": titel, "tekst": "\n".join(tekst), "notes": notes})
    return uit


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    deck, pptx = Path(args[0]), Path(args[1])
    metas = list(deck.glob("*.pptx.meta.json"))
    if not metas:
        print(f"FOUT  geen *.pptx.meta.json in {deck}: deze pptx is niet door cedapress geëxporteerd", file=sys.stderr)
        return 1
    meta = json.loads(metas[0].read_text(encoding="utf-8"))
    bron_tekst = (deck / "bron.md").read_text(encoding="utf-8")
    status = {
        "pptx_bewerkt": pptx_hash(pptx) != meta.get("pptx"),
        "bron_gewijzigd_sinds_export": bron_hash(bron_tekst) != meta.get("bron"),
    }
    if not status["pptx_bewerkt"]:
        print(json.dumps(status) if "--json" in argv else "OK  pptx ongewijzigd sinds export; niets terug te schrijven")
        return 0

    bron = [s for s in voor_vorm(parse(bron_tekst), "pptx")["slides"]]
    titels = {s["titel"]: s for s in bron}
    diffs = []
    for s in lees_pptx(pptx):
        b = titels.get(s["titel"])  # TODO: robuuster koppelen (zie docstring)
        if not b:
            diffs.append({"pptx_slide": s["nr"], "titel": s["titel"], "status": "geen bron-slide met deze titel"})
            continue
        if b["notes"].strip() != s["notes"].strip():
            diffs.append({"pptx_slide": s["nr"], "titel": s["titel"], "veld": "notes",
                          "diff": "\n".join(difflib.unified_diff(b["notes"].splitlines(), s["notes"].splitlines(), "bron", "pptx", lineterm=""))})
        # TODO: tekst vergelijken; bron-tekst is markdown, pptx-tekst is platte tekst per vorm → eerst normaliseren.
    status["verschillen"] = diffs
    if "--json" in argv:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        if status["bron_gewijzigd_sinds_export"]:
            print("WAARSCHUWING  bron.md is sinds de export ook gewijzigd: conflict, beslis per verschil")
        for d in diffs:
            print(f"slide {d['pptx_slide']} ({d['titel']}): {d.get('status') or d['veld']}")
            if d.get("diff"):
                print(d["diff"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
