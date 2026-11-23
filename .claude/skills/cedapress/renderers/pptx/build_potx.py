#!/usr/bin/env python
"""cedapress pptx-renderer (potx-engine, overgenomen uit powerclaude): bouwt een deck-spec op de Npuls-PowerPoint-template (.potx).

Wordt aangeroepen door build.mjs (--engine potx, de standaard); niet zelf draaien.
    python build_potx.py <payload.json>
build.mjs controleert de spec, rastert de illustraties en schrijft de payload:
{ name, title, author, template, out, slides, illu: {naam: png}, teamfoto, tokens: {C, VARIANTS, CARD, CHART_ORDER, FONT, ALLOWED} }

Elk slidetype gebruikt een layout uit de template (zie references/slidetypes.md, "potx-engine").
Uitvoer: exit 0 = gebouwd (waarschuwingen op stdout), 1 = fout.
"""
import copy
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_THEME_COLOR as TC
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

sys.stdout.reconfigure(encoding="utf-8")

P = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
T = P["tokens"]
C, VARIANTS, CARD, CHART_ORDER, FONT, ALLOWED = T["C"], T["VARIANTS"], T["CARD"], T["CHART_ORDER"], T["FONT"], T["ALLOWED"]
BODY, HEAD, QUOTE = FONT["body"], FONT["head"], FONT["quote"]
WARN = []

# Npuls-kleuren die als themakleur in de template staan: zo blijven ze in PowerPoint als themakleur kiesbaar.
THEME = {"oranje": TC.ACCENT_1, "roze": TC.ACCENT_3, "blauw": TC.ACCENT_4, "geel": TC.ACCENT_5, "groen": TC.ACCENT_6}

# Maten in inches (16:9, 13.333 × 7.5), gelijk aan de template: titel en tekst beginnen op x = 900000 EMU.
W, H = 13.333, 7.5
ML = 900000 / 914400
CW = W - 2 * ML
TOP = 1.8  # eerste regel onder de titel-placeholder
BOTTOM = 6.75  # boven het dianummer

# Minimale lettergrootte in pt op de 13,33 in brede dia. Edwins waarden gelden voor 10 in (body 11,5 pt, label 9 pt)
# en zijn omgerekend met 4/3: 15,3 en 12 pt (afgerond 15 en 12). Zie ontwerper-powerpoint OPP-05.
S = 4 / 3
MIN_BODY, MIN_LABEL = 15, 12
CONTENT_BOTTOM = 6.65  # onderkant inhoud; daaronder het dianummer

# Masters in de template: 0 wit, 1 roze, 2 oranje, 3 blauw, 4 geel.
MASTER = {"wit": 0, "roze": 1, "oranje": 2, "blauw": 3, "geel": 4}


def E(v):
    return Emu(int(round(v * 914400)))


# ---------------------------------------------------------------- template openen

def open_potx(path):
    """python-pptx opent geen .potx: zet het hoofd-contenttype om naar presentatie."""
    zi, buf = zipfile.ZipFile(path), io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist():
            d = zi.read(it.filename)
            if it.filename == "[Content_Types].xml":
                d = d.replace(b"presentationml.template.main+xml", b"presentationml.presentation.main+xml")
            zo.writestr(it, d)
    buf.seek(0)
    return Presentation(buf)


prs = open_potx(P["template"])
MASTERS = list(prs.slide_masters)
lst = prs.slides._sldIdLst
for sid in list(lst):  # voorbeeldslides van de template weghalen; masters en layouts blijven
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)


def layout(master, name):
    for l in MASTERS[master].slide_layouts:
        if l.name == name:
            return l
    raise SystemExit(f"FOUT  layout '{name}' ontbreekt in master {master} van de template")


# ---------------------------------------------------------------- kleur en tekst

def paint(colorfmt, name):
    if name in THEME:
        colorfmt.theme_color = THEME[name]
    else:
        colorfmt.rgb = RGBColor.from_string(C[name])


def plain(text):
    return re.sub(r"\*\*(.+?)\*\*", r"\1", str(text))


EM = {BODY: 0.53, HEAD: 0.56, QUOTE: 0.5}


def text_height(text, w, size, font=BODY, line=1.18):
    cpl = max(1, math.floor((w * 72) / (size * EM.get(font, 0.53))))
    lines = sum(max(1, math.ceil(len(p) * 1.06 / cpl)) for p in plain(text).split("\n"))
    return lines * size * line / 72


def longest_word_w(text, size, font=BODY):
    """Breedte in inches van het langste woord (schatting): past dat niet in het vak, dan breekt PowerPoint midden in het woord."""
    words = plain(text).split()
    return max((len(w_) for w_ in words), default=0) * size * EM.get(font, 0.53) / 72


def fit(text, w, h, size, font=BODY, mn=None):
    floor = mn if mn is not None else max(MIN_BODY if size >= MIN_BODY else MIN_LABEL, round(size * 0.75))
    for s in range(int(size), int(floor) - 1, -1):
        if text_height(text, w, s, font) <= h:
            return s, True
    return floor, False


ALL_SLIDES = []


class Slide:
    def __init__(self, n, s, master, layout_name):
        self.n, self.spec = n, s
        self.rects = []  # (soort, naam, x, y, w, h) van tekst en illustraties, voor de overlapcontrole
        self.top = TOP  # bovenkant van de inhoud; lager als er een intro onder de titel staat
        ALL_SLIDES.append(self)
        lay = layout(master, layout_name)
        self.s = prs.slides.add_slide(lay)
        for ph in lay.placeholders:  # dianummer wordt door python-pptx niet meegekopieerd
            if ph.placeholder_format.type == PP_PLACEHOLDER.SLIDE_NUMBER:
                self.s.shapes._spTree.append(copy.deepcopy(ph._element))
        self.v = VARIANTS.get(s.get("variant", "wit"), VARIANTS["wit"])
        if s.get("notes"):
            self.s.notes_slide.notes_text_frame.text = s["notes"]

    def warn(self, m):
        WARN.append(f"slide {self.n}: {m}")

    # --- placeholders
    def ph(self, idx):
        for p in self.s.placeholders:
            if p.placeholder_format.idx == idx:
                return p
        return None

    def drop(self, idx):
        p = self.ph(idx)
        if p is not None:
            p._element.getparent().remove(p._element)

    def place(self, idx, x=None, y=None, w=None, h=None):
        """Alle vier maten zetten; alleen top/height zetten geeft in python-pptx breedte 0."""
        p = self.ph(idx)
        p.left, p.top, p.width, p.height = (E(x) if x is not None else p.left, E(y) if y is not None else p.top,
                                            E(w) if w is not None else p.width, E(h) if h is not None else p.height)
        return p

    def set_ph(self, idx, text, color=None, size=None, max_chars=None, bullets=True, accent=None):
        p = self.ph(idx)
        if p is None or text in (None, ""):
            self.drop(idx)
            return None
        if max_chars and len(plain(text)) > max_chars:
            self.warn(f"tekst past mogelijk niet in de template-placeholder ({len(plain(text))} tekens, richtlijn {max_chars}): \"{plain(text)[:50]}…\"")
        self._fill(p.text_frame, text, color=color, size=size, accent=accent)
        if not bullets:
            no_bullet(p.text_frame.paragraphs)
        return p

    def title(self, text, idx=0, max_chars=None):
        """Titel in de titel-placeholder (40pt in de template); te lang → kleiner, tot 24pt."""
        color = None if self.v["bg"] in ("wit",) or self.v["bg"].startswith("licht") else self.v["title"]
        x, y, w, h = self.ph_box(idx)
        size, ok = fit(plain(text), w, max(h, 0.6) * 1.2, 40, HEAD, 24)
        if not ok:
            self.warn(f"titel te lang voor de template ({len(plain(text))} tekens): \"{plain(text)[:50]}\" → korter")
        # `**accentdeel**` krijgt de accentkleur van de slide (OPP-17, OPP-20)
        return self.set_ph(idx, text, color=color, size=size if size < 40 else None, accent=self.v["accent"] if "**" in str(text) else None)

    def note_rect(self, text, x, y, w, h, size, font, valign, align="left"):
        """Onthoud waar de tekst echt staat (niet het hele vak), zodat een illustratie eroverheen opvalt."""
        lines = plain(text).split("\n")
        used = min(w, max(len(l_) for l_ in lines) * size * EM.get(font, 0.53) / 72)
        th = min(h, text_height(text, w, size, font))
        ty = y if valign == "top" else (y + (h - th) / 2 if valign == "middle" else y + h - th)
        tx = x if align == "left" else (x + (w - used) / 2 if align == "center" else x + w - used)
        self.rects.append(("tekst", plain(text)[:30], tx, ty, used, th))

    def check_overlap(self):
        for a in (r for r in self.rects if r[0] == "illu"):
            for b in (r for r in self.rects if r[0] == "tekst"):
                ox = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2])
                oy = min(a[3] + a[5], b[3] + b[5]) - max(a[3], b[3])
                if ox > 0.05 and oy > 0.05:
                    self.warn(f"illustratie \"{a[1]}\" overlapt de tekst \"{b[1]}…\" → ruimte reserveren of de illustratie verplaatsen")

    # --- tekst
    def _fill(self, tf, text, color=None, size=None, font=None, accent=None, align=None, para_space=0, line=None, spc=None):
        tf.clear()
        for i, para in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if align:
                p.alignment = align
            if para_space and i > 0:
                p.space_before = Pt(para_space)
            if line:
                p.line_spacing = line
            for j, part in enumerate(re.split(r"\*\*(.+?)\*\*", para)):
                if not part:
                    continue
                r = p.add_run()
                r.text = part
                f = r.font
                strong = j % 2 == 1
                if strong:
                    f.name = HEAD
                elif font:
                    f.name = font
                if size:
                    f.size = Pt(size)
                c = (accent or color) if strong else color
                if c:
                    paint(f.color, c)
                if spc:
                    r._r.get_or_add_rPr().set("spc", str(spc))  # letterspatiëring in 1/100 pt

    def text(self, text, x, y, w, h, size, color="zwart", font=BODY, accent=None, align="left", valign="top",
             mn=None, para_space=0, link=None, line=None, kind="body", spc=None):
        """kind "body" (minimaal MIN_BODY pt) of "label" (labels, tags, pillen: minimaal MIN_LABEL pt). Kleinere
        groottes worden opgetrokken; past de tekst dan niet, dan volgt een waarschuwing (inkorten, niet verkleinen)."""
        if text in (None, ""):
            return None
        lo = MIN_LABEL if kind == "label" else MIN_BODY
        size, mn = max(size, lo), max(mn or 0, lo)
        sz, ok = fit(text, w, h, size, font, mn)
        if not ok:
            self.warn(f"tekst past niet ({w:.1f}×{h:.1f} in, {sz}pt): \"{plain(text)[:50]}…\" → inkorten of splitsen")
        elif longest_word_w(text, sz, font) > w:
            self.warn(f"woord past niet op één regel ({w:.1f} in breed, {sz}pt) en breekt midden in het woord: \"{max(plain(text).split(), key=len)}\" → breder vak of korter woord")
        self.note_rect(text, x, y, w, h, sz, font, valign, align)
        box = self.s.shapes.add_textbox(E(x), E(y), E(w), E(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[valign]
        al = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        self._fill(tf, text, color=color, size=sz, font=font, accent=accent, align=al, para_space=para_space, line=line, spc=spc)
        if link:  # link op het tekstvak: een hyperlink in de tekst kleurt PowerPoint altijd in de themakleur
            box.click_action.hyperlink.address = link
        return box

    def label(self, text, x, y, w, h, color, size=12, align="left"):
        self.text(str(text).upper(), x, y, w, h, size, color, font=HEAD, align=align, kind="label", spc=100)

    # --- vormen
    def box(self, x, y, w, h, fill, r=0.28, shape=None):
        sh = self.s.shapes.add_shape(shape or (MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE), E(x), E(y), E(w), E(h))
        sh.fill.solid()
        paint(sh.fill.fore_color, fill)
        sh.line.fill.background()
        sh.shadow.inherit = False
        if r and sh.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = min(r / min(w, h), 0.5)
        return sh

    def circle(self, x, y, d, fill=None, stroke=None, width=3):
        sh = self.s.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(d), E(d))
        if fill:
            sh.fill.solid()
            paint(sh.fill.fore_color, fill)
        else:
            sh.fill.background()
        if stroke:
            paint(sh.line.color, stroke)
            sh.line.width = Pt(width)
        else:
            sh.line.fill.background()
        sh.shadow.inherit = False
        return sh

    def line(self, x1, y1, x2, y2, color, width=2):
        ln = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
        paint(ln.line.color, color)
        ln.line.width = Pt(width)
        return ln

    def pill(self, text, x, y, w, h, fill, color, size=13):
        self.box(x, y, w, h, fill, r=h / 2)
        self.text(text, x + 0.1, y, w - 0.2, h, size, color, font=HEAD, align="center", valign="middle", kind="label")

    def badge(self, text, x, y, d, fill, color, size=None):
        self.circle(x, y, d, fill)
        self.text(text, x, y, d, d, size or round(d * 34), color, font=HEAD, align="center", valign="middle", mn=10)

    def picture(self, path, x, y, w, h, alt="", link=None):
        pic = self.s.shapes.add_picture(str(path), E(x), E(y))
        k = min(E(w) / pic.width, E(h) / pic.height)
        pic.width, pic.height = int(pic.width * k), int(pic.height * k)
        pic.left, pic.top = int(E(x) + (E(w) - pic.width) / 2), int(E(y) + (E(h) - pic.height) / 2)
        if alt:
            pic._element.nvPicPr.cNvPr.set("descr", alt)
        if link:
            pic.click_action.hyperlink.address = link
        return pic

    def movie(self, path, poster, x, y, w, h, alt=""):
        """mp4 in het bestand, passend geschaald naar de verhouding van de poster; speelt bij klik."""
        from PIL import Image
        with Image.open(poster) as im:
            pw, ph = im.size
        k = min(w / pw, h / ph)
        mw, mh = pw * k, ph * k
        mov = self.s.shapes.add_movie(str(path), E(x + (w - mw) / 2), E(y + (h - mh) / 2), E(mw), E(mh),
                                      poster_frame_image=str(poster), mime_type="video/mp4")
        mov._element.nvPicPr.cNvPr.set("name", alt or "Video")
        if alt:
            mov._element.nvPicPr.cNvPr.set("descr", alt)
        return mov

    def illustration(self, name, x, y, w, h, alt=""):
        png = P["illu"].get(name)
        if not png:
            return self.warn(f"illustratie \"{name}\" niet gevonden")
        pic = self.picture(png, x, y, w, h, alt)
        self.rects.append(("illu", name, pic.left / 914400, pic.top / 914400, pic.width / 914400, pic.height / 914400))
        return pic

    def ph_box(self, idx):
        p = self.ph(idx)
        return p.left / 914400, p.top / 914400, p.width / 914400, p.height / 914400

    def background(self, name):
        """Achtergrond van deze slide (Opmaak achtergrond); layout en placeholders blijven van de template."""
        if name == "wit":
            return
        f = self.s.background.fill
        f.solid()
        paint(f.fore_color, name)

    def check_pair(self, bg, fg, where):
        light = bg == "wit" or bg.startswith("licht-")
        if fg == bg or (not light and fg not in ALLOWED.get(bg, [])):
            self.warn(f"{fg} op {bg} ({where}) is geen toegestane Npuls-combinatie")


def no_bullet(paragraphs):
    for p in paragraphs:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "0")
        pPr.set("indent", "0")
        for old in pPr.findall(qn("a:buNone")):
            pPr.remove(old)
        pPr.insert(0, pPr.makeelement(qn("a:buNone"), {}))


def footnote(sl, s):
    note = s.get("footnote") or (f"Bron: {s['source']}" if s.get("source") else None)
    if note:
        sl.text(note, 1.6, 6.92, CW - 0.62, 0.3, 12, "zwart" if sl.v["bg"] != "blauw" else "roze", kind="label")


def footer(sl, s, y):
    if s.get("footer"):
        sl.text(s["footer"], ML, y, CW, 0.5, 18, sl.v["text"], accent=sl.v["accent"], mn=12)
    footnote(sl, s)


def content_slide(n, s, layout_name="Alleen titel"):
    """Inhoudsslide op de witte master; een niet-witte variant wordt de achtergrond van deze slide."""
    sl = Slide(n, s, 0, layout_name)
    sl.background(sl.v["bg"])
    if s.get("label"):
        label_pill(sl, s["label"])
    if s.get("intro"):  # korte regel onder de titel; de inhoud begint daaronder
        sl.text(s["intro"], ML, 1.66, CW, 0.5, 16, sl.v["text"], mn=15)
        sl.top = 2.35
    return sl


def card_colors(sl, items):
    return [it.get("color") or sl.v["cards"][i % len(sl.v["cards"])] for i, it in enumerate(items)]


# ---------------------------------------------------------------- componenten uit ceda-powerpoint-maker (Edwin)
# Maten van Edwin (10 × 5,625 in) zijn met S = 4/3 omgerekend naar de 13,33 × 7,5 in van de potx; de breedte volgt
# de potx-marges (ML, CW), de hoogte de inhoudszone onder de titel-placeholder. Zie references/pptx-slidetypes.md.
ICON_FG, TILE_ON, BADGE_FG = T["ICON_FG"], T["TILE_ON"], T["BADGE_FG"]
ICONS = P.get("icons", {})  # icoonnaam → PNG (zwart, transparant) uit iconen/<naam>.svg van het assetpakket
TILE_CYCLE = ["blauw", "geel", "groen", "oranje", "roze"]
SOFT = {"blauw": "licht-blauw", "groen": "licht-groen", "oranje": "licht-oranje"}
_icon_warned, _tint_cache = set(), {}


def soft_card(sl):
    """Kleur voor rijen en kaarten: wit op een lichte of gekleurde slide, een zacht accentvlak op een witte slide."""
    return SOFT.get(sl.v["accent"], "licht-blauw") if sl.v["bg"] == "wit" else "wit"


def tile_color(i, avoid=None):
    cyc = [c for c in TILE_CYCLE if c != avoid]
    return cyc[i % len(cyc)]


def tinted_icon(name, color):
    """Het zwarte icoon in de kleur van het tegelpaar (alpha blijft, de kleur wordt vervangen)."""
    png = ICONS.get(name)
    if not png:
        return None
    if (name, color) not in _tint_cache:
        from PIL import Image
        im = Image.open(png).convert("RGBA")
        flat = Image.new("RGBA", im.size, "#" + C[color])
        flat.putalpha(im.getchannel("A"))
        out = Path(P["out"]).parent / "img" / f"icoon-{name}-{color}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        flat.save(out)
        _tint_cache[(name, color)] = out
    return _tint_cache[(name, color)]


def icon_tile(sl, x, y, icon, tile, size=0.56):
    """Afgeronde tegel in een paletkleur met het icoon in de kleur van het tegelpaar (OPP-22). Zonder icoon in het
    assetpakket blijft de tegel leeg en volgt een waarschuwing; er worden geen eigen iconen meegeleverd."""
    sl.box(x, y, size, size, tile, r=size * 0.27)
    png = tinted_icon(icon, ICON_FG[tile]) if icon else None
    if png:
        sl.picture(png, x + size * 0.275, y + size * 0.275, size * 0.45, size * 0.45)
    elif icon and icon not in _icon_warned:
        _icon_warned.add(icon)
        sl.warn(f"icoon \"{icon}\" zit niet in het assetpakket (iconen/{icon}.svg): icoontegel zonder icoon. Iconen komen via een nieuwe assetrelease")
    return size


def label_pill(sl, text):
    """Label-pil linksboven (OPP-18): 1 tot 3 woorden in kapitalen, kleur = accent van de slide."""
    fill = sl.v["accent"] if sl.v["accent"] in BADGE_FG else "blauw"
    t = str(text).upper()
    w = (0.34 + 0.088 * len(t)) * S
    sl.box(ML, 0.55, w, 0.37, fill, r=0.185)
    sl.text(t, ML, 0.55, w, 0.37, 12, BADGE_FG[fill], font=HEAD, align="center", valign="middle", kind="label", spc=100)


def note_space(s):
    return 1.35 if s.get("note") else 0


def note_bar(sl, note, y, h=1.05):
    """Notitiebalk: brede balk met één boodschap, optioneel met icoontegel en vet begin (`bold`)."""
    note = {"text": note} if isinstance(note, str) else note
    c = note.get("color") or ("wit" if sl.v["bg"] == "roze" else "roze")
    sl.box(ML, y, CW, h, c, r=min(0.21, h * 0.25))
    tx = ML + 0.33
    if note.get("icon"):
        icon_tile(sl, ML + 0.27, y + (h - 0.56) / 2, note["icon"], note.get("tile") or tile_color(0, avoid=c))
        tx = ML + 1.07
    txt = (f"**{note['bold']}** " if note.get("bold") else "") + note["text"]
    fg = CARD[c]["text"]
    sl.text(txt, tx, y, CW - (tx - ML) - 0.33, h, 17, fg, accent=fg, valign="middle", mn=15)
    return h


def figure_card(sl, x, y, w, h, value, label, bg=None, color="oranje"):
    """Kerncijfer: groot getal (vet, oranje) met het label in kapitalen eronder."""
    bg = bg or ("wit" if sl.v["bg"] in ("licht-geel",) else "licht-geel")
    sl.check_pair(bg, color, "kerncijfer")
    sl.box(x, y, w, h, bg, r=0.21)
    sl.text(str(value), x + 0.29, y + 0.23, w - 0.58, min(1.0, h * 0.5), 59, color, font=HEAD, valign="middle", mn=36)
    sl.text(str(label).upper(), x + 0.29, y + 1.33, w - 0.58, max(0.4, h - 1.5), 12, "zwart", font=HEAD, kind="label", spc=100)


def step_row(sl, x, y, w, h, nr, title, text, bg, circle):
    """Horizontale stap: genummerde cirkel, vette titel, optionele toelichting."""
    sl.box(x, y, w, h, bg, r=min(0.21, h * 0.2))
    d = 0.53 if h >= 0.8 else 0.45
    sl.badge(str(nr), x + 0.24, y + (h - d) / 2, d, circle, BADGE_FG.get(circle, "zwart"), 16)
    tx = x + 0.24 + d + 0.27
    tw = w - (tx - x) - 0.2
    if text:
        sl.text(title, tx, y + 0.1, tw, 0.4, 19, "zwart", font=HEAD, mn=15)
        sl.text(text, tx, y + 0.5, tw, h - 0.55, 15, "zwart", mn=15)
    else:
        sl.text(title, tx, y, tw, h, 19, "zwart", font=HEAD, valign="middle", mn=15)


def step_card(sl, x, y, w, h, nr, title, text, bg, circle):
    """Stapkolom: verticale kaart met cirkel bovenaan, titel en toelichting."""
    sl.box(x, y, w, h, bg, r=0.17)
    sl.badge(str(nr), x + 0.27, y + 0.24, 0.53, circle, BADGE_FG.get(circle, "zwart"), 16)
    th = max(0.4, text_height(title, w - 0.54, 19, HEAD) + 0.05)
    sl.text(title, x + 0.27, y + 0.93, w - 0.54, th, 19, "zwart", font=HEAD, mn=15)
    sl.text(text, x + 0.27, y + 0.93 + th + 0.1, w - 0.54, h - (0.93 + th + 0.1) - 0.2, 15, "zwart", mn=15)
    return th


def t_steps(n, s):
    """Stapkolom (P7): 3 tot 4 verticale stap-kaarten naast elkaar, optioneel een notitiebalk eronder."""
    sl = content_slide(n, s)
    sl.title(s["title"])
    items = s["items"][:4]
    bottom = CONTENT_BOTTOM - note_space(s)
    gap = 0.33
    cw = (CW - gap * (len(items) - 1)) / len(items)
    tw = cw - 0.54
    need = max(0.93 + max(0.4, text_height(it["title"], tw, 19, HEAD) + 0.05) + 0.1 + text_height(it.get("text", ""), tw, 15) + 0.3 for it in items)
    ch = min(bottom - sl.top, max(3.0, need))
    bg, circle = soft_card(sl), sl.v["accent"]
    for i, it in enumerate(items):
        step_card(sl, ML + i * (cw + gap), sl.top, cw, ch, i + 1, it["title"], it.get("text", ""), bg, circle)
    if s.get("note"):
        note_bar(sl, s["note"], sl.top + ch + 0.3)
    footnote(sl, s)


def t_lead(n, s):
    """Kernzin met kerncijfers (P1): lead links; kerncijfers eronder en stappen rechts, of kerncijfers naast de lead."""
    sl = content_slide(n, s)
    sl.title(s["title"])
    v, top = sl.v, sl.top
    bottom = CONTENT_BOTTOM - note_space(s)
    figs, items = (s.get("figures") or [])[:2], (s.get("items") or [])[:4]
    gap = 0.33
    if items:
        lw = CW * 0.46
        lh = min(2.0, text_height(s["lead"], lw, 25) + 0.1) if s.get("lead") else 0
        sl.text(s.get("lead"), ML, top, lw, lh, 25, v["text"], accent=v["accent"], mn=18)
        fy = top + lh + 0.3
        if figs:
            fw = (lw - gap * (len(figs) - 1)) / len(figs)
            for k, f in enumerate(figs):
                figure_card(sl, ML + k * (fw + gap), fy, fw, max(1.9, min(2.46, bottom - fy)), f["value"], f.get("label", ""))
        rx = ML + lw + 0.6
        rw = CW - lw - 0.6
        ry = top
        if s.get("eyebrow"):
            sl.label(s["eyebrow"], rx, ry, rw, 0.3, v["accent"])
            ry += 0.45
        rh = min(1.07, (bottom - ry - 0.12 * (len(items) - 1)) / len(items))
        bg = soft_card(sl) if v["bg"] != "wit" else "licht-groen"
        for k, it in enumerate(items):
            step_row(sl, rx, ry + k * (rh + 0.12), rw, rh, k + 1, it["title"], it.get("text"), bg, "groen" if v["bg"] == "wit" else v["accent"])
    else:
        lw = CW * 0.58 if figs else CW
        sl.text(s.get("lead"), ML, top, lw, bottom - top, 25, v["text"], accent=v["accent"], mn=18)
        if figs:
            fx, fw = ML + lw + 0.5, CW - lw - 0.5
            fh = min(2.46, (bottom - top - 0.25 * (len(figs) - 1)) / len(figs))
            for k, f in enumerate(figs):
                figure_card(sl, fx, top + k * (fh + 0.25), fw, fh, f["value"], f.get("label", ""))
    if s.get("note"):
        note_bar(sl, s["note"], CONTENT_BOTTOM - 1.05)
    footnote(sl, s)


def t_hero(n, s):
    """Heldenkaart (P4): groot vlak met label en een grote vraag of stelling in Cooper, optioneel met illustratie."""
    sl = content_slide(n, s)
    sl.title(s["title"])
    c = s.get("color") or "groen"
    r = CARD[c]
    sl.check_pair(sl.v["bg"], c, "heldenkaart")
    top, bottom = sl.top, CONTENT_BOTTOM
    sl.box(ML, top, CW, bottom - top, c, r=0.21)
    tw = CW - 1.07 - (4.2 if s.get("illustration") else 0)
    if s.get("eyebrow"):
        sl.label(s["eyebrow"], ML + 0.53, top + 0.47, tw, 0.35, r["label"], size=13)
    sl.text(s["text"], ML + 0.53, top + 1.0, tw, bottom - top - 1.4, 31, r["text"], font=QUOTE, mn=22)
    if s.get("illustration"):
        side = min(3.7, bottom - top - 0.3)
        sl.illustration(s["illustration"], ML + CW - side - 0.3, top + 0.15, side, bottom - top - 0.3)
    footnote(sl, s)


def t_insight(n, s):
    """Inzichtregels (P3): rijen met icoon, vet sleutelwoord, tekst en een tag rechts (wie, wil, want, maar)."""
    sl = content_slide(n, s)
    sl.title(s["title"])
    rows = s["rows"][:5]
    bottom = CONTENT_BOTTOM - note_space(s)
    gap = 0.16
    rh = min(1.03, (bottom - sl.top - gap * (len(rows) - 1)) / len(rows))
    bg = soft_card(sl)
    for k, r in enumerate(rows):
        y = sl.top + k * (rh + gap)
        sl.box(ML, y, CW, rh, bg, r=0.21)
        icon_tile(sl, ML + 0.24, y + (rh - 0.56) / 2, r.get("icon"), r.get("tile") or tile_color(k))
        sl.text(r.get("key"), ML + 1.07, y, 1.9, rh, 21, "zwart", font=HEAD, valign="middle", mn=15)
        tag_w = 1.9 if r.get("tag") else 0
        sl.text(r["text"], ML + 3.1, y, CW - 3.1 - 0.3 - tag_w, rh, 20, "zwart", valign="middle", mn=15)
        if r.get("tag"):
            sl.text(str(r["tag"]).upper(), ML + CW - tag_w - 0.27, y, tag_w, rh, 12, sl.v["accent"], font=HEAD, align="right", valign="middle", kind="label", spc=100)
    if s.get("note"):
        note_bar(sl, s["note"], bottom + 0.3)
    footnote(sl, s)


def t_lists(n, s):
    """Lijstkaart en pillenkaart (P8, P13): 2 tot 3 kaarten naast elkaar met een kop, een icoontegel en een lijst met
    stippen (`style: 'list'`, standaard) of witte pillen (`style: 'pills'`, max. 4)."""
    sl = content_slide(n, s)
    sl.title(s["title"])
    groups = s["groups"][:3]
    bottom = CONTENT_BOTTOM - note_space(s)
    gap = 0.33
    wts = [0.55 if g.get("style") == "pills" and len(groups) == 2 else 1 for g in groups]
    unit = (CW - gap * (len(groups) - 1)) / sum(wts)
    x = ML
    h = bottom - sl.top
    for k, g in enumerate(groups):
        w = unit * wts[k]
        pills = g.get("style") == "pills"
        bg = g.get("bg") or soft_card(sl)
        sl.box(x, sl.top, w, h, bg, r=0.21)
        kx = x + 0.33
        if g.get("icon"):
            icon_tile(sl, kx, sl.top + 0.29, g["icon"], g.get("tile") or tile_color(k, avoid=bg))
            kx += 0.73
        sl.text(g["title"], kx, sl.top + 0.27, x + w - kx - 0.33, 0.6, 21 if pills else 23, "zwart", font=HEAD, valign="middle", mn=15)
        items = g["items"][:4] if pills else g["items"][:5]
        top = sl.top + 1.15
        if pills:
            ph = min(0.67, (h - 1.15 - 0.3) / len(items) - 0.16)
            for i, it in enumerate(items):
                py = top + i * (ph + 0.16)
                sl.box(x + 0.33, py, w - 0.66, ph, "wit" if bg != "wit" else "licht-blauw", r=0.21)
                sl.text(it, x + 0.6, py, w - 1.2, ph, 17, "zwart", valign="middle", mn=15)
        else:
            cols = g.get("columns", 1)
            per = math.ceil(len(items) / cols)
            rh = min(0.75, (h - 1.15 - 0.2) / per)
            kw = (w - 0.66) / cols
            stip = g.get("dot") or tile_color(k, avoid=bg)
            for i, it in enumerate(items):
                col, row = divmod(i, per)
                ix, iy = x + 0.4 + col * kw, top + row * rh
                sl.circle(ix, iy + 0.1, 0.15, stip)
                sl.text(it, ix + 0.33, iy, kw - 0.45, rh, 17, "zwart", mn=15)
        x += w + gap
    if s.get("note"):
        note_bar(sl, s["note"], bottom + 0.3)
    footnote(sl, s)


# ---------------------------------------------------------------- slidetypes

def t_title(n, s):
    v = s.get("variant", "roze")
    for k in ("agenda", "tagline"):
        if s.get(k):
            WARN.append(f"slide {n}: titelslide: {k} wordt in de template-titelslide niet getoond (toon het programma in een tijdlijn)")
    if v == "roze":
        sl = Slide(n, s, 1, "Titeldia")
        sl.set_ph(0, plain(s["title"]), max_chars=40)
        sl.set_ph(10, s.get("lede"), max_chars=80)
        sl.set_ph(1, s.get("kicker"), max_chars=60)
        if sl.set_ph(11, s.get("sub"), max_chars=70) is not None:
            sl.place(11, w=8.9)  # het datumvak is smal; een langere regel loopt anders over drie regels
        if s.get("illustration"):
            sl.illustration(s["illustration"], 9.2, 1.3, 3.4, 3.4)
        return
    m = MASTER.get(v)
    if m not in (1, 2, 3):
        WARN.append(f"slide {n}: titelslide '{v}' bestaat niet in de template; blauw gebruikt")
        m = 3
    sl = Slide(n, s, m, "Titeldia 3")
    sl.set_ph(0, plain(s["title"]), max_chars=40)
    sl.set_ph(12, s.get("lede"), max_chars=70)
    sl.set_ph(1, " · ".join(x for x in (s.get("kicker"), s.get("sub")) if x), max_chars=60)
    if s.get("illustration"):
        x, y, w, h = sl.ph_box(13)
        sl.drop(13)
        sl.illustration(s["illustration"], x + 0.3, y + 1.5, w - 0.6, w - 0.6)


def section_master(sl_n, v, kind):
    if v in MASTER and v != "wit":
        return MASTER[v]
    WARN.append(f"slide {sl_n}: {kind} '{v}' heeft geen eigen master in de template; blauw gebruikt")
    return 3


def t_section(n, s):
    sl = Slide(n, s, section_master(n, s.get("variant", "blauw"), "sectie"), "Sectiescheider")
    num = s.get("number")
    sl.set_ph(0, f"{int(num):02d}" if isinstance(num, (int, float)) else num)
    p = sl.set_ph(11, plain(s["title"]), max_chars=60)
    has_right = s.get("illustration")
    if has_right:
        sl.place(11, w=7.6)
    if s.get("text") and p is not None:
        para = p.text_frame.add_paragraph()
        para.space_before = Pt(18)
        r = para.add_run()
        r.text = plain(s["text"])
        r.font.size = Pt(22)
        r.font.name = BODY
    if has_right:
        sl.illustration(s["illustration"], 9.3, 2.2, 3.2, 3.2)
    footnote(sl, s)


def t_stats(n, s):
    sl = content_slide(n, s)
    v = sl.v
    sl.title(s["title"])
    y = sl.top
    if s.get("lede"):
        lh = min(0.95, text_height(s["lede"], CW, 20) + 0.05)
        sl.text(s["lede"], ML, y - 0.15, CW, lh, 20, v["text"], mn=15)
        y += lh + 0.2
    items = s["items"][:4]
    cols = card_colors(sl, items)
    gap = 0.24
    cw = (CW - gap * (len(items) - 1)) / len(items)
    max_h = (BOTTOM - y) - (1.15 if s.get("callout") else 0)
    text_h = max((text_height(it["text"], cw - 0.6, 14) if it.get("text") else 0) for it in items)
    ch = min(max_h, max(2.6, 2.05 + text_h + 0.25))
    for i, it in enumerate(items):
        x, c = ML + i * (cw + gap), cols[i]
        r = CARD[c]
        sl.check_pair(v["bg"], c, "kaart")
        sl.box(x, y, cw, ch, c)
        sl.text(str(it["value"]), x + 0.3, y + 0.25, cw - 0.6, 1.1, 64, r["big"], font=HEAD, valign="middle", mn=36)
        sl.text(it.get("label"), x + 0.3, y + 1.4, cw - 0.6, 0.45, 19, r["title"], font=HEAD, mn=13)
        sl.text(it.get("text"), x + 0.3, y + 1.85, cw - 0.6, ch - 2.0, 14, r["text"], mn=10)
    y += ch + 0.3
    if s.get("callout"):
        sl.box(ML, y, CW, 0.85, "wit" if v["bg"] != "wit" else "licht-blauw", r=0.2)
        sl.text(s["callout"], ML + 0.35, y, CW - 0.7, 0.85, 16, "zwart", accent="blauw", valign="middle", mn=11)
    footnote(sl, s)


def card_row(sl, s, items, y, max_h, min_h, compact=False):
    v = sl.v
    items = items[:4]
    cols = card_colors(sl, items)
    gap = 0.5 if s.get("arrows") else 0.3
    cw = (CW - gap * (len(items) - 1)) / len(items)
    iw = cw - 0.6
    ts = 20 if len(items) > 3 else 24
    pad = 0.22 if compact else 0.3
    has_badge = any(it.get("badge") or s.get("numbered") or it.get("icon") for it in items)
    bw = 0.6 if compact and has_badge else 0
    if sum(c_ in ("blauw", "groen", "oranje") for c_ in cols) > 2:
        sl.warn("meer dan 2 volle kaartkleuren (blauw, groen, oranje) op één slide: laat de rest wit of licht [OPP-21]")
    # Een illustratie krijgt een eigen blok boven de titel (kaart) of rechts naast de kop (compacte rij); de tekst loopt er nooit overheen.
    ill_h = 1.3 if not compact and any(it.get("illustration") for it in items) else 0
    ill_w = 1.0 if compact and any(it.get("illustration") for it in items) else 0
    iw -= ill_w
    longest = max(len(w_) for it in items for w_ in plain(it["title"]).split())  # geen woord afbreken
    while ts > 14 and longest * ts * EM[HEAD] > (iw - bw) * 72:
        ts -= 1
    head_h = 0.85 if not compact and any(it.get("badge") or s.get("numbered") or it.get("tag") or it.get("icon") for it in items) else 0
    title_h = max([0.4] + [text_height(it["title"], iw - bw, ts, HEAD) for it in items]) + 0.12
    sub_h = 0.5 if any(it.get("sub") for it in items) else 0

    def secs(it):
        return it.get("sections") or ([{"text": it["text"]}] if it.get("text") else [])

    n_sec = max(len(secs(it)) for it in items)
    sec_h = [max((((0.38 if (secs(it)[k].get("label")) else 0) + text_height(secs(it)[k]["text"], iw, 15,
                   HEAD if secs(it)[k].get("strong") else BODY) + 0.25) if k < len(secs(it)) else 0) for it in items)
             for k in range(n_sec)]
    fixed = pad + head_h + ill_h + title_h + sub_h + (0.05 if compact else 0.15)
    natural = fixed + sum(sec_h)
    if natural > max_h:
        sec_h = [h * (max_h - fixed) / (natural - fixed) for h in sec_h]
    ch = min(max_h, max(min_h, natural))
    for i, it in enumerate(items):
        x, c = ML + i * (cw + gap), cols[i]
        r = CARD[c]
        sl.check_pair(v["bg"], c, "kaart")
        sl.box(x, y, cw, ch, c)
        iy = y + pad
        badge = it.get("badge") or (str(i + 1) if s.get("numbered") else None)
        if it.get("icon"):
            icon_tile(sl, x + 0.3, iy - (0.02 if compact else 0), it["icon"], it.get("tile") or TILE_ON.get(c) or tile_color(i, avoid=c), 0.46 if compact else 0.56)
            badge = None if not it.get("tag") else badge
        if badge and compact:
            sl.badge(badge, x + 0.3, iy - 0.02, 0.46, r["pillBg"], r["pillFg"], 16)
        elif badge:
            sl.badge(badge, x + 0.3, iy, 0.6, r["pillBg"], r["pillFg"], 20)
        if it.get("tag"):
            sl.pill(it["tag"], x + (1.05 if badge else 0.3), iy + 0.08, cw - (1.35 if badge else 0.6), 0.44, r["pillBg"], r["pillFg"], 12)
        iy += head_h
        if it.get("illustration") and compact:
            sl.illustration(it["illustration"], x + cw - 1.1, y + 0.12, 0.85, 0.85)
        elif it.get("illustration"):
            sl.illustration(it["illustration"], x + 0.3, iy, 1.3, 1.3)
        iy += ill_h
        sl.text(it["title"], x + 0.3 + bw, iy, iw - bw, title_h - 0.15, ts, r["title"], font=HEAD, mn=14)
        iy += title_h
        if it.get("sub"):
            sl.text(it["sub"], x + 0.3, iy, iw, 0.4, 14, r["text"], font=QUOTE, mn=10)
        iy += sub_h + (0.05 if compact else 0.15)
        for k, sec in enumerate(secs(it)):
            sy = iy
            if sec.get("label"):
                sl.label(sec["label"], x + 0.3, sy, iw, 0.3, r["label"])
                sy += 0.38
            sl.text(sec["text"], x + 0.3, sy, iw, sec_h[k] - (sy - iy) - 0.15, 15, r["text"],
                    font=HEAD if sec.get("strong") else BODY, mn=10)
            iy += sec_h[k]
        if s.get("arrows") and i < len(items) - 1:
            ar = sl.s.shapes.add_shape(MSO_SHAPE.CHEVRON, E(x + cw + 0.12), E(y + ch / 2 - 0.3), E(0.26), E(0.6))
            ar.fill.solid()
            paint(ar.fill.fore_color, v["title"] if v["bg"] not in ("wit",) and not v["bg"].startswith("licht") else "zwart")
            ar.line.fill.background()
            ar.shadow.inherit = False
    return ch


def t_cards(n, s):
    sl = content_slide(n, s)
    sl.title(s["title"])
    callout_h = 1.1 if s.get("callout") else 0
    bottom = BOTTOM - 0.15 - (0.5 if s.get("footer") else 0) - (callout_h + 0.3 if callout_h else 0)
    y = sl.top
    if s.get("rows"):
        rows = s["rows"][:2]
        label_h, row_gap = 0.4, 0.3
        max_h = (bottom - y - len(rows) * label_h - row_gap * (len(rows) - 1)) / len(rows)
        for k, row in enumerate(rows):
            if row.get("label"):
                sl.label(row["label"], ML, y, CW, 0.3, sl.v["accent"])
            y += label_h
            y += card_row(sl, s, row["items"], y, max_h, 1.2, True) + (row_gap if k < len(rows) - 1 else 0)
    else:
        y += card_row(sl, s, s["items"], y, bottom - y, 3.4)
    if s.get("callout"):
        y += 0.3
        sl.box(ML, y, CW, callout_h, "wit" if sl.v["bg"] != "wit" else "licht-blauw", r=0.2)
        sl.text(s["callout"], ML + 0.4, y, CW - 0.8, callout_h, 22, "zwart", accent="blauw", valign="middle", mn=14)
        y += callout_h
    footer(sl, s, y + 0.2)


def t_split(n, s):
    left = s.get("side") == "left"
    sl = content_slide(n, s, "Tekst en afbeelding 2" if left else "Tekst en afbeelding 1")
    sl.title(s["title"])
    body_idx, pic_idx = 15, (13 if left else 1)
    parts = []
    if s.get("lede"):
        parts.append(s["lede"])
    if s.get("bullets"):
        parts += s["bullets"][:4]
    elif s.get("text"):
        parts.append(s["text"])
    p = sl.ph(body_idx)
    if p is not None:
        x, y, w, h = sl.ph_box(body_idx)
        sl.place(body_idx, h=BOTTOM - 0.2 - y)
        txt = "\n".join(parts)
        avail = (BOTTOM - 0.2 - y) - 0.15 * len(parts)
        size, ok = fit(txt, w - 0.45, avail, 20, BODY, 14)
        if not ok:
            sl.warn(f"tekst past niet naast de afbeelding: \"{plain(txt)[:50]}…\" → inkorten")
        sl._fill(p.text_frame, txt, size=size, accent=sl.v["accent"] if sl.v["bg"] != "wit" else "blauw", para_space=10)
        if s.get("lede") or not s.get("bullets"):
            no_bullet(p.text_frame.paragraphs[:1] if s.get("bullets") else p.text_frame.paragraphs)
    x, y, w, h = sl.ph_box(pic_idx)
    sl.drop(pic_idx)
    if s.get("image"):
        sl.picture(s["image"], x, y, w, h, s.get("alt", ""))
    elif s.get("illustration"):
        sl.box(x, y, w, h, "roze" if sl.v["bg"] != "roze" else "wit", r=0.25)
        sl.illustration(s["illustration"], x + 0.5, y + 0.5, w - 1.0, h - 1.0, s.get("alt", ""))
    footnote(sl, s)


def t_list(n, s):
    items = s["items"][:7]
    if len(items) <= 4 and not s.get("footer"):
        return list_steps(n, s, items)
    sl = content_slide(n, s)
    sl.title(s["title"])
    y0 = sl.top
    avail = (BOTTOM - y0) - (0.6 if s.get("footer") else 0)
    rh = min(0.95, avail / len(items) - 0.1)
    card = "roze" if sl.v["bg"] == "blauw" else ("licht-roze" if sl.v["bg"] == "wit" else "wit")
    for i, it in enumerate(items):
        y = y0 + i * (rh + 0.1)
        sl.box(ML, y, CW, rh, card, r=0.14)
        sl.text(it["title"], ML + 0.3, y + 0.06, 4.0, rh - 0.12, 16, "zwart", font=HEAD, valign="middle", mn=10)
        sl.text(it.get("text"), ML + 4.5, y + 0.06, 4.9 if it.get("status") else 6.6, rh - 0.12, 14, "zwart", valign="middle", mn=9)
        if it.get("status"):
            status_pill(sl, it, ML + CW - 1.95, y + rh / 2 - 0.18)
    footer(sl, s, y0 + len(items) * (rh + 0.1) + 0.15)


def status_pill(sl, it, x, y):
    sc = it.get("color") or "blauw"
    fg = "roze" if sc == "blauw" else "zwart"
    sl.pill(it["status"], x, y, 1.7, 0.36, sc, fg, 11)


def list_steps(n, s, items):
    """Tot vier rijen: de layout Stappen uit de template (golf links, vakken rechts)."""
    sl = content_slide(n, s, "Stappen")
    sl.title(s["title"])
    boxes = [(13, 14), (15, 21), (17, 18), (19, 20)]
    for k, (t_idx, p_idx) in enumerate(boxes):
        if k >= len(items):
            sl.drop(t_idx)
            sl.drop(p_idx)
            continue
        it = items[k]
        bx, by, bw, bh = sl.ph_box(t_idx)
        ph = sl.ph(t_idx)
        tf = ph.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        icon = it.get("illustration")
        left = 1.35 if icon else 0.3
        right = 2.0 if it.get("status") else 0.2
        tf.margin_left, tf.margin_right = E(left), E(right)
        tw = bw - left - right
        title_sz, _ = fit(it["title"], tw, 0.35, 16, HEAD, 12)
        text_sz, ok = fit(it.get("text", ""), tw, bh - 0.45, 13, BODY, 10)
        if not ok:
            sl.warn(f"stap \"{it['title'][:40]}\": tekst past niet in het vak → inkorten")
        sl._fill(tf, f"**{it['title']}**" + (f"\n{it['text']}" if it.get("text") else ""), color="zwart", size=text_sz, accent="zwart")
        tf.paragraphs[0].runs[0].font.size = Pt(title_sz)
        no_bullet(tf.paragraphs)
        px, py, pw, phh = sl.ph_box(p_idx)
        sl.drop(p_idx)
        if icon:
            sl.illustration(icon, px, py, pw, phh)
        if it.get("status"):
            status_pill(sl, it, bx + bw - 1.9, by + bh / 2 - 0.18)
    footnote(sl, s)


def t_table(n, s):
    sl = content_slide(n, s)
    v = sl.v
    sl.title(s["title"])
    rows, cols = s["rows"], s["columns"]
    fs = 12 if len(rows) > 8 else 14
    row_h = 0.42 if len(rows) > 8 else 0.5
    gf = sl.s.shapes.add_table(len(rows) + 1, len(cols), E(ML), E(sl.top), E(CW), E(row_h * (len(rows) + 1)))
    tbl = gf.table
    if s.get("widths"):
        for i, f in enumerate(s["widths"]):
            tbl.columns[i].width = E(f * CW)
    alt = ("licht-blauw", "wit") if v["bg"] == "wit" else ("wit", "licht-roze")

    def cell(r, c, text, fill, color, font):
        ce = tbl.cell(r, c)
        ce.fill.solid()
        paint(ce.fill.fore_color, fill)
        ce.vertical_anchor = MSO_ANCHOR.MIDDLE
        ce.margin_left = ce.margin_right = Pt(8)
        ce.margin_top = ce.margin_bottom = Pt(5)
        tf = ce.text_frame
        tf.text = ""
        run = tf.paragraphs[0].add_run()
        run.text = str(text)
        run.font.size, run.font.name = Pt(fs), font
        paint(run.font.color, color)

    for c, h in enumerate(cols):
        cell(0, c, h, "blauw", "roze", HEAD)
    for r, row in enumerate(rows, 1):
        for c, val in enumerate(row):
            cell(r, c, val, alt[r % 2], "zwart", BODY)
    if len(rows) > 10:
        sl.warn("tabel met meer dan 10 rijen: splitsen of samenvatten")
    footer(sl, s, sl.top + row_h * (len(rows) + 1) + 0.25)


def t_chart(n, s):
    sl = content_slide(n, s)
    v = sl.v
    sl.title(s["title"])
    kind = s.get("chart", "bar")
    side = 4.0 if s.get("takeaway") else 0
    x, y, w, h = ML, sl.top, CW - side - (0.3 if side else 0), BOTTOM - sl.top - 0.3
    if not (v["bg"] == "wit" or v["bg"].startswith("licht")):
        sl.box(x, y, w, h, "wit", r=0.2)
    cd = CategoryChartData()
    cd.categories = s["labels"]
    for se in s["series"]:
        cd.add_series(se["name"], [None if val is None else val for val in se["values"]])
    if kind == "bar":
        ct = (XL_CHART_TYPE.BAR_STACKED if s.get("stacked") else XL_CHART_TYPE.BAR_CLUSTERED) if s.get("horizontal") else \
             (XL_CHART_TYPE.COLUMN_STACKED if s.get("stacked") else XL_CHART_TYPE.COLUMN_CLUSTERED)
    else:
        ct = {"line": XL_CHART_TYPE.LINE_MARKERS, "pie": XL_CHART_TYPE.PIE, "doughnut": XL_CHART_TYPE.DOUGHNUT}[kind]
    gf = sl.s.shapes.add_chart(ct, E(x + 0.2), E(y + 0.2), E(w - 0.4), E(h - 0.4), cd)
    ch = gf.chart
    ch.font.name, ch.font.size = BODY, Pt(13)
    paint(ch.font.color, "zwart")
    pie = kind in ("pie", "doughnut")
    ch.has_legend = len(s["series"]) > 1 or pie
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
    colors = s.get("colors") or (CHART_ORDER if pie else CHART_ORDER[: len(s["series"])])
    plot = ch.plots[0]
    fmt = s.get("format", "#,##0")
    if s.get("values", True):
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format, dl.number_format_is_linked = fmt + ";;;" if s.get("stacked") else fmt, False
        dl.font.name, dl.font.size = HEAD, Pt(12)
        if kind == "bar" and s.get("stacked"):
            dl.position = XL_LABEL_POSITION.CENTER
    if pie:
        for i, pt in enumerate(plot.series[0].points):
            pt.format.fill.solid()
            paint(pt.format.fill.fore_color, colors[i % len(colors)])
    else:
        if kind == "bar":
            plot.gap_width = 60
            if s.get("stacked"):
                plot.overlap = 100
        for i, se in enumerate(plot.series):
            c = colors[i % len(colors)]
            if kind == "line":
                paint(se.format.line.color, c)
                se.format.line.width = Pt(3)
                se.marker.format.fill.solid()
                paint(se.marker.format.fill.fore_color, c)
                se.smooth = False
            else:
                se.format.fill.solid()
                paint(se.format.fill.fore_color, c)
        va = ch.value_axis
        va.tick_labels.number_format, va.tick_labels.number_format_is_linked = fmt, False
        if not re.search(r"\.[0#]", re.sub(r'"[^"]*"', "", fmt)) and all((v_ or 0) >= 0 for se in s["series"] for v_ in se["values"]):
            # formaat zonder decimalen: een geheel getal als stap, anders staan er dubbele labels op de as (4, 3, 3, 2, 2, 1, 1)
            sums = [sum(v_ or 0 for v_ in col) for col in zip(*[se["values"] for se in s["series"]])] if s.get("stacked") else                    [v_ or 0 for se in s["series"] for v_ in se["values"]]
            peak = max(sums + [1])
            step = next(k * 10 ** e for e in range(0, 9) for k in (1, 2, 5) if k * 10 ** e >= peak / 5)
            va.minimum_scale, va.major_unit = 0, step
            va.maximum_scale = math.ceil(peak / step) * step
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
        va.format.line.fill.background()
        if s.get("horizontal"):
            ch.category_axis.reverse_order = True
    if s.get("takeaway"):
        tx = ML + CW - side
        th = min(h, 1.2 + text_height(s["takeaway"], side - 0.6, 20, HEAD))
        c = v["cards"][0]
        r = CARD[c]
        sl.box(tx, y, side, th, c)
        sl.label(s.get("takeawayLabel", "Wat valt op"), tx + 0.3, y + 0.35, side - 0.6, 0.3, r["label"])
        sl.text(s["takeaway"], tx + 0.3, y + 0.8, side - 0.6, th - 1.0, 20, r["title"], font=HEAD, mn=13)
        if s.get("illustration"):
            sl.illustration(s["illustration"], tx + 0.4, y + th + 0.2, side - 0.8, h - th - 0.2)
    footnote(sl, s)


def t_quote(n, s):
    v = s.get("variant", "wit")
    m = 1 if v == "roze" else 0
    sl = Slide(n, s, m, "Quote")
    if m == 0:
        sl.background(sl.v["bg"])
    p = sl.set_ph(11, plain(s["text"]), max_chars=180)
    if p is not None and not (sl.v["bg"] == "wit" or sl.v["bg"].startswith("licht") or m == 1):
        for r in (r for para in p.text_frame.paragraphs for r in para.runs):
            paint(r.font.color, sl.v["quote"] if sl.v["quote"] != "zwart" else sl.v["title"])
    x, y, w, h = sl.ph_box(11)
    if s.get("by"):
        sl.text(s["by"], x, y + h + 0.2, w, 0.5, 18, sl.v["text"], font=HEAD)
    if s.get("illustration"):
        sl.illustration(s["illustration"], 0.5, 4.6, 1.8, 1.8)


def t_image(n, s):
    sl = content_slide(n, s)
    v = sl.v
    sl.title(s["title"])
    side = 4.1 if s.get("text") else 0
    bx, by, bw = ML, sl.top, CW - side - (0.3 if side else 0)
    bh = (BOTTOM - sl.top) - (0.55 if s.get("caption") else 0)
    alt = s.get("alt") or s.get("caption", "")
    if s.get("video"):
        sl.movie(s["video"], s["poster"], bx, by, bw, bh, alt)
    else:
        sl.picture(s["image"], bx, by, bw, bh, alt, link=s.get("link"))
    if s.get("caption"):
        sl.text(s["caption"], bx, by + bh + 0.12, bw, 0.4, 13, v["text"], align="center", mn=10)
    if s.get("text"):
        sl.text(s["text"], ML + CW - side, sl.top, side, BOTTOM - sl.top, 18, v["text"], accent=v["accent"] if v["bg"] != "wit" else "blauw", mn=12, para_space=8)
    footnote(sl, s)


def t_timeline(n, s):
    sl = content_slide(n, s)
    sl.title(s["title"])
    blocks = s["blocks"]
    total = s.get("total") or sum(b["minutes"] for b in blocks)
    gap = 0.05
    per = (CW - gap * (len(blocks) - 1)) / total
    bar_y, bar_h = 2.55, 1.0
    fmt = lambda m: f"{m // 60}:{m % 60:02d}"
    x, t = ML, 0
    for i, b in enumerate(blocks):
        w = b["minutes"] * per
        c = b.get("color") or sl.v["cards"][i % len(sl.v["cards"])]
        r = CARD[c]
        if w < 0.9:
            sl.warn(f"tijdlijnblok \"{b['title']}\" is te smal ({w:.2f} in): geef het meer minuten of voeg het samen")
        sl.text(fmt(b.get("start", t)), x, bar_y - 0.42, max(w, 0.9), 0.3, 14, "blauw", font=HEAD)
        sl.box(x, bar_y, w, bar_h, c, r=0)
        sl.text(f"{b['minutes']} min", x, bar_y, w, bar_h, 18, r["title"], font=HEAD, align="center", valign="middle", mn=10)
        sl.text(b["title"], x + 0.02, bar_y + bar_h + 0.25, w - 0.1, 0.8, 12, "zwart", font=HEAD, mn=9)
        sl.text(b.get("text"), x + 0.02, bar_y + bar_h + 1.1, w - 0.1, 0.9, 12, "zwart", mn=9)
        if b.get("tag"):
            sl.box(x + 0.02, bar_y + bar_h + 2.05, w - 0.04, 0.34, "wit" if sl.v["bg"] != "wit" else "licht-blauw", r=0.17)
            sl.text(b["tag"], x + 0.02, bar_y + bar_h + 2.05, w - 0.04, 0.34, 9, "blauw", font=HEAD, align="center", valign="middle", mn=7)
        x += w + gap
        t += b["minutes"]
    sl.text(fmt(total), ML + CW - 1.0, bar_y - 0.42, 1.0, 0.3, 14, "blauw", font=HEAD, align="right")
    lx = ML
    for l in s.get("legend", []):
        sl.box(lx, 6.34, 0.22, 0.22, l["color"], r=0)
        sl.text(l["label"], lx + 0.32, 6.3, 2.6, 0.3, 12, "zwart", valign="middle")
        lx += 0.32 + 0.11 * len(l["label"]) + 0.5
    footnote(sl, s)


def t_ceda(n, s):
    """Vaste CEDA-introslide, woordelijk gelijk aan clidev/_template.md, in de vertrouwde vorm:
    tekst links, rechts het roze Npuls-vlak met logo. Dat vlak is de layout Partnerslide van de template."""
    sl = Slide(n, s, 0, "Partnerslide")
    sl.drop(11)  # vak voor een partnerlogo; hier niet nodig
    x, w = ML, 5.3
    sl.label("Wie is CEDA", x, 1.75, w, 0.35, "oranje", size=13)
    sl.text("Centre of Educational Data Analytics", x, 2.15, w, 1.3, 32, "blauw", font=HEAD, mn=24)
    sl.text("Eén team binnen Npuls. Van ruwe data tot AI-toepassing, open source.", x, 3.5, w, 0.9, 18, "zwart", font=QUOTE, mn=14)
    for i, (b, c) in enumerate(zip(["Data, analytics en generatieve AI in één keten", "Altijd in co-creatie met mbo, hbo en wo",
                                    "Open source, voor elke instelling"], ["blauw", "oranje", "groen"])):
        y = 4.6 + i * 0.55
        sl.circle(x, y + 0.12, 0.17, c)
        sl.text(b, x + 0.35, y, w - 0.35, 0.55, 16, "zwart", mn=12)


TEAM_TEXT = "Diverse projecten, waaronder\n\n**Instroomprognose**\n\n**Staat van de Onderwijsinstelling**"


def t_team(n, s):
    """Vaste teamslide "Wie zijn wij": groepsfoto van het CEDA-team (zoals in de DAIR-decks); `text` mag anders."""
    t_image(n, {**s, "title": "Wie zijn wij", "image": P.get("teamfoto") or "public/shots/team/groep.png", "alt": "Groepsfoto van het CEDA-team",
                "text": s.get("text") or TEAM_TEXT})


def t_contact(n, s):
    """Vaste afsluitslide met de CEDA-links, zoals in de oude engine: roze titeldia (logo en bogen uit de template),
    gecentreerde kop en drie witte kaarten met een gekleurde pill en een link."""
    sl = Slide(n, s, 1, "Titeldia")
    for p in list(sl.s.placeholders):
        p._element.getparent().remove(p._element)
    sl.label("Tot slot", 0, 1.75, W, 0.35, "oranje", size=13, align="center")
    sl.text("Blijf in contact", 0, 2.15, W, 0.95, 44, "blauw", font=HEAD, align="center")
    sl.text("Vragen, feedback of zin om mee te bouwen? We horen graag van je.", 2.5, 3.15, W - 5, 0.5, 18, "zwart", align="center")
    links = [("GitHub", "github.com/cedanl", "blauw", "roze", "https://github.com/cedanl"),
             ("Community", "edu.nl/7b4yg", "groen", "zwart", "https://edu.nl/7b4yg"),
             ("Email", "ceda@surf.nl", "oranje", "zwart", "mailto:ceda@surf.nl")]
    cw, gap = 3.5, 0.3
    x0 = (W - (3 * cw + 2 * gap)) / 2
    for i, (tag, txt, c, fg, url) in enumerate(links):
        x = x0 + i * (cw + gap)
        sl.box(x, 4.0, cw, 1.35, "wit", r=0.2)
        sl.pill(tag, x + (cw - 1.6) / 2, 4.22, 1.6, 0.4, c, fg, size=12)
        box = sl.text(txt, x + 0.15, 4.78, cw - 0.3, 0.4, 14, "zwart", align="center", link=url)
        for rr in (rr for pa in box.text_frame.paragraphs for rr in pa.runs):
            rr.font.underline = True


def t_closing(n, s):
    v = s.get("variant", "roze")
    m = MASTER.get(v, 1) if v != "wit" else 1
    if v not in MASTER or v == "wit":
        WARN.append(f"slide {n}: afsluiting '{v}' heeft geen eigen master in de template; roze gebruikt")
    sl = Slide(n, s, m, "Sectiescheider")
    sl.set_ph(0, s.get("title", "Vragen?"))
    has_right = s.get("points") or s.get("illustration")
    lw = 5.8 if has_right else 8.4
    p = sl.place(11, w=lw, y=1.9, h=2.6)
    p.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
    # bottom-anchored: te veel tekst groeit omhoog over het label; daarom passend maken (44pt → min. 24pt)
    size, ok = fit(plain(s["question"]), lw, 2.6, 44, HEAD, 24)
    if not ok:
        sl.warn("afsluitvraag is lang voor de template-placeholder → inkorten")
    sl._fill(p.text_frame, plain(s["question"]), size=size)
    ty = 4.75
    if s.get("text"):
        sl.text(s["text"], ML, ty, lw, 0.9, 18, None, font=HEAD, mn=11)
        ty += 1.0
    if s.get("contact"):
        sl.text(s["contact"], ML, ty, lw, 0.45, 16, None, font=HEAD, mn=11)
    if s.get("points"):
        x, w = 7.2, W - ML - 7.2
        if s.get("pointsTitle"):
            sl.text(s["pointsTitle"], x, 1.75, w, 0.5, 22, None, font=HEAD)
        card = "wit" if sl.v["bg"] != "wit" else "licht-roze"
        r = CARD.get(card, CARD["wit"])
        ph_ = min(1.5, 4.3 / len(s["points"]) - 0.15)
        for i, pt in enumerate(s["points"]):
            y = 2.45 + i * (ph_ + 0.15)
            sl.box(x, y, w, ph_, card, r=0.25)
            if pt.get("tag"):
                sl.pill(pt["tag"], x + 0.3, y + 0.22, 1.5, 0.38, r["pillBg"], r["pillFg"], 11)
            sl.text(pt["text"], x + 0.3, y + (0.7 if pt.get("tag") else 0.2), w - 0.6, ph_ - (0.85 if pt.get("tag") else 0.4), 15, "zwart", mn=10)
    elif s.get("illustration"):
        sl.illustration(s["illustration"], 8.2, 1.6, 3.8, 3.8)
    # Tekstvakken zonder eigen kleur volgen de themakleur tekst 1 van de master (wit op blauw/oranje, zwart op roze/geel).


def t_einddia(n, s):
    Slide(n, s, 1, "Einddia")


LAYOUTS = {"title": t_title, "section": t_section, "stats": t_stats, "cards": t_cards, "split": t_split, "list": t_list,
           "table": t_table, "chart": t_chart, "quote": t_quote, "image": t_image, "video": t_image, "timeline": t_timeline,
           "ceda": t_ceda, "team": t_team, "contact": t_contact, "closing": t_closing, "einddia": t_einddia,
           "steps": t_steps, "lead": t_lead, "hero": t_hero, "insight": t_insight, "lists": t_lists}

slides = list(P["slides"])
if slides and slides[-1]["type"] == "contact" and P.get("einddia", True):
    slides.append({"type": "einddia"})
for i, s in enumerate(slides, 1):
    first = len(ALL_SLIDES)
    LAYOUTS[s["type"]](i, s)
    for sl_ in ALL_SLIDES[first:]:
        sl_.check_overlap()

prs.core_properties.title = P.get("title") or P["name"]
prs.core_properties.author = P.get("author") or "CEDA"
if P.get("bron"):
    prs.core_properties.keywords = f"cedapress-bron {P['bron']}"  # terugschrijven.py leest dit
out = Path(P["out"])
out.parent.mkdir(parents=True, exist_ok=True)
prs.save(out)
for w in WARN:
    print(f"WAARSCHUWING  {w}")
print(f"OK  {out} — {len(slides)} slides (Npuls-template), {len(WARN)} waarschuwing(en)")
