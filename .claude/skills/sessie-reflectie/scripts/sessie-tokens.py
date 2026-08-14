#!/usr/bin/env python3
"""Telt het tokenverbruik van de lopende Claude Code-sessie op.

Draaien, niet lezen. Zonder argument pakt hij het nieuwste transcript van de
huidige werkdirectory; geef anders een pad naar een .jsonl mee.

Output is YAML, klaar om in de frontmatter van een reflectie te plakken.
"""

import json
import sys
from pathlib import Path

VELDEN = (
    ("input_tokens", "tokens-in"),
    ("output_tokens", "tokens-uit"),
    ("cache_creation_input_tokens", "tokens-cache-schrijf"),
    ("cache_read_input_tokens", "tokens-cache-lees"),
)


def transcript_voor_cwd() -> Path | None:
    slug = str(Path.cwd()).replace("/", "-")
    directory = Path.home() / ".claude" / "projects" / slug
    if not directory.is_dir():
        return None
    bestanden = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    return bestanden[-1] if bestanden else None


def main() -> int:
    pad = Path(sys.argv[1]) if len(sys.argv) > 1 else transcript_voor_cwd()
    if pad is None or not pad.is_file():
        # Geen transcript: geen reden om de reflectie te blokkeren.
        print("sessie-id: \"\"")
        for _, naam in VELDEN:
            print(f"{naam}: 0")
        print("# geen transcript gevonden voor deze werkdirectory")
        return 0

    totalen = dict.fromkeys((bron for bron, _ in VELDEN), 0)
    berichten = 0
    for regel in pad.read_text(errors="replace").splitlines():
        try:
            record = json.loads(regel)
        except json.JSONDecodeError:
            continue
        bericht = record.get("message")
        gebruik = bericht.get("usage") if isinstance(bericht, dict) else None
        if not isinstance(gebruik, dict):
            continue
        berichten += 1
        for bron in totalen:
            totalen[bron] += gebruik.get(bron) or 0

    print(f'sessie-id: "{pad.stem}"')
    print(f"sessie-berichten: {berichten}")
    for bron, naam in VELDEN:
        print(f"{naam}: {totalen[bron]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
