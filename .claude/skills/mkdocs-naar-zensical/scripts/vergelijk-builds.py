#!/usr/bin/env python3
"""Vergelijk een MkDocs-build met een Zensical-build van dezelfde site.

Gebruik:  python3 -I vergelijk-builds.py <map-mkdocs> <map-zensical>

Controleert (alleen standaardbibliotheek):
  1. dezelfde HTML-pagina's        -> ontbrekende pagina's zijn een fout
  2. dezelfde interne links        -> links die alleen in de MkDocs-build staan zijn een fout
  3. dezelfde paginatitels         -> verschillen zijn een waarschuwing
  4. bestanden uit docs/ (afbeeldingen, downloads) -> ontbrekende zijn een fout
  5. een zoekindex in de Zensical-build

Exitcode 0 = geen fouten, 1 = minstens een fout. Waarschuwingen veranderen de exitcode niet.
Dit script vergelijkt structuur, geen uiterlijk: maak voor het uiterlijk schermafbeeldingen.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

# Thema-bestanden verschillen per generator; die vergelijken we niet.
THEME_IGNORE = (
    "assets/stylesheets/",
    "assets/javascripts/",
    "assets/images/",
    "search/",
    "search.json",
    "sitemap.xml",
    "sitemap.xml.gz",
    "404.html",
    ".nojekyll",
    ".cache/",
)


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titel = ""
        self._in_title = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.titel += data


def normaliseer(pagina: str, href: str):
    """Maak van een href een pad relatief aan de siteroot, of None voor externe/anker-links."""
    u = urlparse(href)
    if u.scheme or u.netloc:
        return None
    if not u.path:
        # "#anker" blijft op dezelfde pagina; "" (Zensical) wijst naar de pagina zelf
        if u.fragment or u.query:
            return None
        pagina_zelf = pagina[: -len("index.html")].rstrip("/") if pagina.endswith("index.html") else pagina
        return pagina_zelf
    pad = PurePosixPath(unquote(u.path))
    basis = PurePosixPath(pagina).parent
    doel = pad if str(pad).startswith("/") else basis / pad
    delen = []
    for deel in doel.parts:
        if deel in ("", "/", "."):
            continue
        if deel == "..":
            if delen:
                delen.pop()
        else:
            delen.append(deel)
    res = "/".join(delen)
    if res.endswith("index.html"):
        res = res[: -len("index.html")].rstrip("/")
    return res


def lees(map_: Path):
    paginas = {}
    for f in sorted(map_.rglob("*.html")):
        rel = f.relative_to(map_).as_posix()
        if rel.startswith(THEME_IGNORE):
            continue
        p = Pagina()
        p.feed(f.read_text(encoding="utf-8", errors="replace"))
        links = {normaliseer(rel, h) for h in p.links}
        paginas[rel] = (re.sub(r"\s+", " ", p.titel).strip(), links - {None})
    return paginas


def bestanden(map_: Path):
    uit = set()
    for f in map_.rglob("*"):
        if f.is_file() and f.suffix != ".html":
            rel = f.relative_to(map_).as_posix()
            if not rel.startswith(THEME_IGNORE):
                uit.add(rel)
    return uit


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    a, b = Path(sys.argv[1]), Path(sys.argv[2])
    for m in (a, b):
        if not m.is_dir():
            print(f"FOUT: {m} is geen map")
            return 2
    pa, pb = lees(a), lees(b)
    fouten, waarschuwingen = [], []

    for p in sorted(set(pa) - set(pb)):
        fouten.append(f"pagina ontbreekt in Zensical-build: {p}")
    for p in sorted(set(pb) - set(pa)):
        waarschuwingen.append(f"pagina alleen in Zensical-build: {p}")

    for p in sorted(set(pa) & set(pb)):
        titel_a, links_a = pa[p]
        titel_b, links_b = pb[p]
        if titel_a != titel_b:
            waarschuwingen.append(f"titel verschilt op {p}: '{titel_a}' -> '{titel_b}'")
        for l in sorted(links_a - links_b):
            if not l.startswith(THEME_IGNORE):
                fouten.append(f"link ontbreekt op {p}: /{l}")

    for f in sorted(bestanden(a) - bestanden(b)):
        fouten.append(f"bestand ontbreekt in Zensical-build: {f}")

    if not ((b / "search.json").exists() or (b / "search" / "search_index.json").exists()):
        fouten.append("geen zoekindex in de Zensical-build")

    print(f"MkDocs: {len(pa)} pagina's | Zensical: {len(pb)} pagina's")
    for w in waarschuwingen:
        print("  !", w)
    for f in fouten:
        print("  ✗", f)
    print(f"{len(fouten)} fout(en), {len(waarschuwingen)} waarschuwing(en)")
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
