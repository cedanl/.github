#!/usr/bin/env python3
"""
WCAG contrast checker.

Verifieert de contrastverhouding tussen twee kleuren tegen de WCAG 2.1
drempelwaarden, zodat "ziet er donker genoeg uit" wordt vervangen door een
objectief getal. Gebruik dit script bij elke kleurbeslissing waar tekst op
een gekleurde of afbeelding-achtergrond komt te staan (V- en O-laag van het
ISGVO-model).

Gebruik:
    python contrast_checker.py "#111827" "#FFFFFF"
    python contrast_checker.py "#111827" "#FFFFFF" --large-text

Argumenten:
    kleur1, kleur2   Hex-kleuren (met of zonder '#'), bijv. #333 of 1a1a1a
    --large-text     Toets tegen de drempel voor grote tekst (>=18pt of
                      >=14pt bold) in plaats van normale tekst
"""

import sys


def _hex_to_rgb(hex_color: str):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Ongeldige hex-kleur: {hex_color}")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _relative_luminance(rgb):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    lum_a = _relative_luminance(_hex_to_rgb(hex_a))
    lum_b = _relative_luminance(_hex_to_rgb(hex_b))
    lighter, darker = max(lum_a, lum_b), min(lum_a, lum_b)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate(hex_a: str, hex_b: str, large_text: bool = False) -> dict:
    ratio = contrast_ratio(hex_a, hex_b)
    aa_threshold = 3.0 if large_text else 4.5
    aaa_threshold = 4.5 if large_text else 7.0
    return {
        "ratio": round(ratio, 2),
        "aa_pass": ratio >= aa_threshold,
        "aaa_pass": ratio >= aaa_threshold,
        "aa_threshold": aa_threshold,
        "aaa_threshold": aaa_threshold,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    large_text = "--large-text" in sys.argv

    if len(args) != 2:
        print(__doc__)
        sys.exit(1)

    result = evaluate(args[0], args[1], large_text=large_text)
    label = "grote tekst" if large_text else "normale tekst"

    print(f"Contrastverhouding: {result['ratio']}:1  ({label})")
    print(f"  WCAG AA  (>= {result['aa_threshold']}:1):  {'PASS' if result['aa_pass'] else 'FAIL'}")
    print(f"  WCAG AAA (>= {result['aaa_threshold']}:1): {'PASS' if result['aaa_pass'] else 'FAIL'}")

    sys.exit(0 if result["aa_pass"] else 1)


if __name__ == "__main__":
    main()
