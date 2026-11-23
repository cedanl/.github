#!/usr/bin/env python3
"""Bron-markdown van een cedapress-deck splitsen per slide en per vorm (html/pptx).

Formaat: references/bronformaat.md. Stdlib only.

Gebruik:
  python parse_bron.py bron.md                 # JSON: meta + alle slides
  python parse_bron.py bron.md --vorm html     # alleen slides voor html, met alleen het html-blok
  python parse_bron.py bron.md --vorm pptx
  python parse_bron.py bron.md --hash          # hash van de bron (gelijk aan renderers/lib/bron.mjs)
  python parse_bron.py bron.md --check         # alleen valideren; exit 1 bij fouten

Exit 0 = ok, 1 = fouten in de bron, 2 = gebruik.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

VORMEN = ("html", "pptx")
SLIDE_KEYS = ("type", "alleen", "variant", "layout", "deel", "label")
SLIDE_HEAD = re.compile(r"^##\s+(?:Slide\s+\d+\s*[—–-]\s*)?(?P<titel>.+?)\s*$")
BLOK_OPEN = re.compile(r"^:::\s*(?P<vorm>[a-z]+)\s*$")
BLOK_DICHT = re.compile(r"^:::\s*$")
NOTES = re.compile(r"^notes\s*:\s*(?P<rest>.*)$", re.I)
KEY = re.compile(r"^(?P<k>[a-z-]+)\s*:\s*(?P<v>.*)$")


def bron_hash(text: str) -> str:
    text = text.lstrip("﻿").replace("\r\n", "\n")
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _frontmatter(lines: list[str]) -> tuple[dict, int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    meta: dict = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return meta, i + 1
        m = KEY.match(lines[i].strip())
        if m:
            meta[m["k"]] = re.sub(r"\s+#.*$", "", m["v"]).strip()  # commentaar na # weg
    raise ValueError("frontmatter niet afgesloten met ---")


def parse(text: str) -> dict:
    """Geeft {meta, slides, fouten, waarschuwingen}. Gooit geen fouten: alles komt in `fouten`."""
    lines = text.lstrip("﻿").replace("\r\n", "\n").split("\n")
    fouten: list[str] = []
    warns: list[str] = []
    try:
        meta, start = _frontmatter(lines)
    except ValueError as e:
        return {"meta": {}, "slides": [], "fouten": [str(e)], "waarschuwingen": []}

    vorm = meta.get("vorm", "html, pptx").replace("beide", "html, pptx")
    meta["vormen"] = [v.strip() for v in vorm.split(",") if v.strip()]
    for v in meta["vormen"]:
        if v not in VORMEN:
            fouten.append(f"frontmatter: onbekende vorm {v!r} (html, pptx of beide)")
    if meta.get("fancy") and meta["fancy"].upper() not in ("A", "B", "C"):
        fouten.append(f"frontmatter: fancy moet A, B of C zijn, niet {meta['fancy']!r}")
    # vaste CEDA-slides (Wie is CEDA, Wie zijn wij, Blijf in contact) zijn optioneel: ja of nee, de auteur kiest per deck
    vast = meta.get("vaste-slides", "").lower()
    if vast and vast not in ("ja", "nee"):
        fouten.append(f"frontmatter: vaste-slides moet ja of nee zijn, niet {meta['vaste-slides']!r}")
    meta["vaste_slides"] = {"ja": True, "nee": False}.get(vast)  # None = niet opgegeven
    for k in ("titel", "publiek", "kernboodschap"):
        if not meta.get(k):
            warns.append(f"frontmatter: {k} ontbreekt")

    slides: list[dict] = []
    cur: dict | None = None
    blok: str | None = None
    in_notes = False
    for nr, line in enumerate(lines[start:], start + 1):
        if blok:
            if BLOK_DICHT.match(line):
                blok = None
            else:
                cur[blok].append(line)
            continue
        head = SLIDE_HEAD.match(line)
        if head and not line.startswith("###"):
            cur = {"nr": len(slides) + 1, "titel": head["titel"], "regel": nr, "tekst": [], "notes": [],
                   "html": [], "pptx": [], "_keys": True}
            slides.append(cur)
            in_notes = False
            continue
        if cur is None:
            if line.strip():
                warns.append(f"regel {nr}: tekst vóór de eerste slide wordt genegeerd")
            continue
        m = BLOK_OPEN.match(line)
        if m:
            if m["vorm"] not in VORMEN:
                fouten.append(f"regel {nr}: onbekend blok ::: {m['vorm']} (html of pptx)")
                blok = "_onbekend"
                cur.setdefault("_onbekend", [])
            else:
                if cur[m["vorm"]]:
                    fouten.append(f"regel {nr}: slide {cur['nr']} heeft twee ::: {m['vorm']}-blokken")
                blok = m["vorm"]
            cur["_keys"] = False
            continue
        if cur["_keys"] and line.strip():
            k = KEY.match(line.strip())
            if k and k["k"] in SLIDE_KEYS:
                cur[k["k"]] = k["v"].strip()
                continue
            cur["_keys"] = False
        n = NOTES.match(line.strip())
        if n:
            in_notes = True
            if n["rest"]:
                cur["notes"].append(n["rest"])
            continue
        (cur["notes"] if in_notes else cur["tekst"]).append(line)
    if blok:
        fouten.append(f"blok ::: {blok} niet afgesloten met :::")

    for s in slides:
        s.pop("_keys", None)
        s.pop("_onbekend", None)
        for k in ("tekst", "notes", "html", "pptx"):
            s[k] = "\n".join(s[k]).strip()
        alleen = s.get("alleen")
        if alleen and alleen not in VORMEN:
            fouten.append(f"slide {s['nr']} ({s['titel']}): alleen moet html of pptx zijn, niet {alleen!r}")
        for v in VORMEN:
            if alleen and alleen != v and s[v]:
                warns.append(f"slide {s['nr']} ({s['titel']}): ::: {v}-blok bij alleen: {alleen} wordt genegeerd")
        if not s["notes"]:
            warns.append(f"slide {s['nr']} ({s['titel']}): geen Notes")
    if not slides:
        fouten.append("geen slides gevonden (elke slide begint met '## ')")
    return {"meta": meta, "slides": slides, "fouten": fouten, "waarschuwingen": warns}


def voor_vorm(doc: dict, vorm: str) -> dict:
    """Alleen de slides voor één vorm; per slide `extra` = het blok van die vorm, andere blokken weg."""
    out = []
    for s in doc["slides"]:
        if s.get("alleen") and s["alleen"] != vorm:
            continue
        t = {k: v for k, v in s.items() if k not in VORMEN}
        t["extra"] = s[vorm]
        out.append(t)
    return {**doc, "vorm": vorm, "slides": out}


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    text = Path(args[0]).read_text(encoding="utf-8")
    if "--hash" in argv:
        print(bron_hash(text))
        return 0
    doc = parse(text)
    doc["bron"] = bron_hash(text)
    if "--vorm" in argv:
        vorm = argv[argv.index("--vorm") + 1]
        if vorm not in VORMEN:
            print("--vorm moet html of pptx zijn", file=sys.stderr)
            return 2
        doc = voor_vorm(doc, vorm)
    for w in doc["waarschuwingen"]:
        print(f"WAARSCHUWING  {w}", file=sys.stderr)
    for f in doc["fouten"]:
        print(f"FOUT          {f}", file=sys.stderr)
    if "--check" not in argv:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
    else:
        print(f"{len(doc['slides'])} slides · {doc['bron']}", file=sys.stderr)
    return 1 if doc["fouten"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
