#!/usr/bin/env python3
"""Genereert npuls-assets/web/npuls.css uit design-tokens.json en scripts/npuls.css.tmpl (alleen stdlib).

Gebruik: python -I scripts/gen_npuls_css.py [--check] [repo-root]
  zonder vlag  schrijft npuls-assets/web/npuls.css
  --check      faalt (exit 1) als de gecommitte npuls.css afwijkt, of als het css_variables-blok in de tokens afwijkt
"""
import json, re, sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
check = "--check" in sys.argv
root = Path(args[0]) if args else Path(__file__).resolve().parent.parent
tokens_path = root / ".claude/skills/vormgever-npuls-huisstijl/references/design-tokens.json"
tmpl_path = root / "scripts/npuls.css.tmpl"
out_path = root / "npuls-assets/web/npuls.css"

t = json.loads(tokens_path.read_text(encoding="utf-8"))
version = (root / "npuls-assets/VERSION").read_text().strip()
c = t["colors"]


def short(n):
    return n[len("npuls-"):] if n.startswith("npuls-") else n


def var(n):
    return f"--npuls-{short(n)}"


def real(group):
    return {k: v for k, v in group.items() if not k.startswith("_")}


prim, sec = real(c["primary"]), real(c["secondary"])
colors = {}
for group in (prim, sec, real(t["neutrals"]), real(c["layout"])):
    for k, v in group.items():
        colors.setdefault(var(k), v)

prim_vars = {var(k) for k in prim}
sec_vars = {var(k) for k in sec}


def size(spec, vw):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:-(\d+(?:\.\d+)?))?px", spec)
    lo, hi = m.group(1), m.group(2)
    if hi is None:
        return f"{lo}px"
    if vw:
        return f"clamp({lo}px, {vw}, {hi}px)"
    return f"{(float(lo) + float(hi)) / 2:g}px"


fonts = {"--npuls-font-primary": t["font_loading"]["primary_stack"],
         "--npuls-font-secondary": t["font_loading"]["secondary_stack"]}
scale = {f"--npuls-{k}": size(s["size"], s.get("fluid_vw")) for k, s in t["typography"]["scale"].items()}
space = {f"--npuls-space-{k}": v for k, v in real(t["spacing"]).items()}
radius = {f"--npuls-radius-{k}": v for k, v in real(t["radii"]).items()}
shadow = {f"--npuls-shadow-{k}": v for k, v in real(t["shadows"]).items()}

decl = {**colors, **fonts, **scale, **space, **radius, **shadow}


def rows(items, per, indent="  "):
    return [indent + " ".join(items[i:i + per]) for i in range(0, len(items), per)]


def block(d, per):
    return rows([f"{k}: {v};" for k, v in d.items()], per)


root_lines = []
root_lines += block({k: v for k, v in colors.items() if k in prim_vars}, 4)
root_lines += block({k: v for k, v in colors.items() if k in sec_vars}, 3)
root_lines += block({k: v for k, v in colors.items() if k not in prim_vars | sec_vars}, 4)
root_lines += block(fonts, 1)
root_lines += block(scale, 3)
root_lines += block(space, 4)
root_lines += block(radius, 5)
root_lines += block(shadow, 1)
root_css = "\n".join(root_lines)

bg = [k for k in prim if k != "npuls-zwart"] + list(sec)  # zwart nooit als achtergrond
parts = rows([f".bg-{short(k)} {{ background: var({var(k)}); }}" for k in bg], 2, "")
parts += rows([f".fg-{short(k)} {{ color: var({var(k)}); }}" for k in prim], 4, "")
parts.append("/* kant-en-klare paren (achtergrond-voorgrond) */")
for combo in c["allowed_combinations"]:
    b = combo["background"]
    if b == "npuls-zwart":
        continue
    for w in combo["with"]:
        parts.append(f".npuls-{short(b)}-{short(w)} {{ background: var({var(b)}); color: var({var(w)}); }}")
combos_css = "\n".join(parts)

# --- slide-varianten en kaartkleuren voor cedapress-decks (slide_roles, card_roles, tile_pairs) ---
def cname(n):
    """Klassenaam in de deck-HTML: npuls-blauw -> blauw, licht-blauw -> lblauw."""
    return short(n).replace("licht-", "l")


def light(n):
    return n == "npuls-wit" or n.startswith("licht-")


roles, cards, tiles = t["slide_roles"], t["card_roles"], t["tile_pairs"]
slides = ["/* Slide-varianten (slide_roles): --paper = achtergrond, --ink = tekst, --accent = accentdeel, --accent-2 = openingsteken citaat */"]
for bg, r in roles.items():
    if bg.startswith("_"):
        continue
    slides.append(f".s-{cname(bg)} {{ --paper: var({var(bg)}); --ink: var({var(r['text'])}); "
                  f"--accent: var({var(r['accent'])}); --accent-2: var({var(r['accent_2'])}); }}")
slides.append("/* Titel en citaat op verzadigde vlakken, alleen waar de rol afwijkt van de tekstkleur; op wit en licht-* volgt de titel de layout */")
for bg, r in roles.items():
    if bg.startswith("_") or light(bg):
        continue
    if r["title"] != r["text"]:
        slides.append(f".s-{cname(bg)} .slide-head h2 {{ color: var({var(r['title'])}); }}")
    if r["quote"] != r["text"]:
        slides.append(f".s-{cname(bg)} .quote {{ color: var({var(r['quote'])}); }}")
slides.append("/* Markering achter het accentdeel van de titel, waar het accent als tekst te weinig contrast haalt (title_highlight) */")
for bg, r in roles.items():
    if bg.startswith("_") or not r.get("title_highlight"):
        continue
    slides.append(f".s-{cname(bg)} .slide-head h2 .hl {{ color: var(--ink); background: var({var(r['title_highlight'])}); padding: 0 .1em; "
                  "-webkit-box-decoration-break: clone; box-decoration-break: clone; }")
slides.append("/* Kaarten (card_roles); licht-* kaarten gebruiken de rollen van npuls-wit */")
for k, r in cards.items():
    if not k.startswith("_"):
        slides.append(f".card.{cname(k)} {{ background: var({var(k)}); color: var({var(r['text'])}); }}")
for k in sec:
    slides.append(f".card.{cname(k)} {{ background: var({var(k)}); color: var({var(cards['npuls-wit']['text'])}); }}")
hero = t["component_defaults"]["hero"]
slides.append("/* Heldenkaart: standaardkleur uit component_defaults.hero, de andere kleuren als .held.<kleur> */")
slides.append(f".held {{ background: var({var(hero)}); color: var({var(cards[hero]['text'])}); }}")
for k, r in cards.items():
    if not k.startswith("_") and k != hero:
        slides.append(f".held.{cname(k)} {{ background: var({var(k)}); color: var({var(r['text'])}); }}")
slides.append("/* Icoontegels (tile_pairs.icon_fg): tegelkleur en kleur van het icoon */")
for k, fg in tiles["icon_fg"].items():
    slides.append(f".ico.{cname(k)} {{ background: var({var(k)}); color: var({var(fg)}); }}")
slides_css = chr(10).join(slides)

header = ("/* GEGENEREERD uit design-tokens.json — niet met de hand bewerken "
          "(scripts/gen_npuls_css.py, sjabloon scripts/npuls.css.tmpl) */\n")
css = header + (tmpl_path.read_text(encoding="utf-8").replace("@@VERSION@@", version)
                .replace("@@ROOT@@", root_css).replace("@@COMBINATIES@@", combos_css)
                .replace("@@SLIDES@@", slides_css))

problems = []
for k, v in t.get("css_variables", {}).items():
    if not k.startswith("_") and decl.get(k) != v:
        problems.append(f"css_variables {k}: tokens '{v}' != gegenereerd '{decl.get(k)}'")

if check:
    cur = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    if cur != css:
        problems.append(f"{out_path.relative_to(root).as_posix()} wijkt af van design-tokens.json — draai: bash scripts/build-npuls-assets.sh")
    if problems:
        print("\n".join("FOUT  " + p for p in problems), file=sys.stderr)
        sys.exit(1)
    print("npuls.css komt overeen met design-tokens.json")
else:
    if problems:
        print("\n".join("WAARSCHUWING  " + p for p in problems), file=sys.stderr)
    out_path.write_text(css, encoding="utf-8", newline="\n")
    print(f"geschreven: {out_path.relative_to(root).as_posix()}")
