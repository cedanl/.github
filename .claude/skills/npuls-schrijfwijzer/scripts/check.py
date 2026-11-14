"""Signaleer afwijkingen van de Npuls-schrijfwijzer in een tekstbestand.

Gebruik: python -I check.py <bestand> [--max-woorden 20]
Leest .md, .html, .txt. Geeft signalen, geen oordeel.
"""
import html
import re
import sys

SCHRAP = ["er", "totaal", "zoals", "momenteel", "huidig", "huidige", "in principe",
          "bepaalde", "bepaald", "gezamenlijk", "gezamenlijke"]
ENGELS = {
    "feedback": "terugkoppeling", "meeting": "overleg", "deadline": "einddatum",
    "update": "stand van zaken", "updates": "stand van zaken", "insights": "inzichten",
    "stakeholders": "betrokkenen", "stakeholder": "betrokkene", "impact": "effect",
    "challenge": "uitdaging", "skills": "vaardigheden", "tool": "hulpmiddel",
    "tools": "hulpmiddelen", "event": "bijeenkomst", "workshop": "werksessie",
    "roadmap": "planning", "kick-off": "start", "kickoff": "start", "pitch": "voorstel",
    "scope": "afbakening", "output": "uitkomst", "input": "inbreng", "check": "controle",
    "team": None, "dashboard": None, "data": None,  # gangbaar, niet melden
    "learnings": "lessen", "best practices": "goede voorbeelden", "community": "gemeenschap",
    "framework": "kader", "mindset": "houding", "sharen": "delen", "checken": "controleren",
}
BIJZIN = r"\b(die|dat|omdat|wanneer|terwijl|zodat|hoewel|nadat|voordat|doordat|indien|waardoor|waarmee|waarin)\b"
PASSIEF = re.compile(r"\b(word|wordt|worden|werd|werden|is|zijn|was|waren)\b(?:\s+\w+){0,6}?\s+\b(ge\w+[dt]|ver\w+[dt]|be\w+[dt]|ont\w+[dt]|her\w+[dt]|\w+ge\w+[dt])\b(?:\s+door\b)?", re.I)


def tekst_uit(pad):
    t = open(pad, encoding="utf-8", errors="replace").read()
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    if pad.lower().endswith((".html", ".htm")) or "<section" in t or "<div" in t:
        t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
        t = re.sub(r"<(br|/p|/li|/h\d|/td|/tr|/div|/section)\b[^>]*>", ".\n", t, flags=re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        t = html.unescape(t)
    t = re.sub(r"^---.*?---", " ", t, flags=re.S)  # frontmatter
    t = re.sub(r"^(#+ .*)$", r"\1.\n", t, flags=re.M)  # koppen zijn eigen zinnen
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    return t


def zinnen(t):
    t = re.sub(r"[ \t]+", " ", t)
    delen = re.split(r"(?<=[.!?])\s+|\n\s*\n|\n(?=\s*[-*#|])", t)
    uit = []
    for z in delen:
        z = re.sub(r"^[\s\-*#>|.]+", "", z).strip(" |.")
        if len(z.split()) >= 3:
            uit.append(z)
    return uit


def check(pad, maxw=20):
    bev = []
    for z in zinnen(tekst_uit(pad)):
        laag = z.lower()
        w = z.split()
        punten = []
        if len(w) > maxw:
            punten.append(f"lange zin ({len(w)} woorden)")
        m = PASSIEF.search(z)
        if m:
            punten.append(f"lijdende vorm? '{m.group(0)}'")
        if len(re.findall(BIJZIN, laag)) > 1:
            punten.append("meer dan één bijzin?")
        if len(re.findall(r"\b(en|maar|want)\b", laag)) >= 3:
            punten.append("veel en/maar/want: zet een punt")
        for s in SCHRAP:
            if re.search(rf"\b{re.escape(s)}\b", laag):
                punten.append(f"schrapwoord '{s}'")
        for e, nl in ENGELS.items():
            if nl and re.search(rf"\b{re.escape(e)}\b", laag):
                punten.append(f"Engels '{e}' → '{nl}'")
        if re.search(r"\b(u|uw)\b", laag):
            punten.append("u/uw → je/jouw")
        if re.search(r"\bdoor npuls\b", laag):
            punten.append("'door Npuls' → 'instellingen in Npuls'")
        if re.search(r"\b(de blog|de webinar|het column)\b", laag):
            punten.append("lidwoord: het blog, de column, het webinar")
        if punten:
            bev.append((z, punten))
    return bev


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    maxw = 20
    if "--max-woorden" in sys.argv:
        maxw = int(sys.argv[sys.argv.index("--max-woorden") + 1])
    bev = check(sys.argv[1], maxw)
    print(f"{len(bev)} zinnen met signalen")
    for z, p in bev:
        kort = z if len(z) < 160 else z[:157] + "..."
        print(f"\n> {kort}\n  - " + "\n  - ".join(p))


if __name__ == "__main__":
    main()
