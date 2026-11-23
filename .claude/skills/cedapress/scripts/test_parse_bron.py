"""Tests voor parse_bron.py. Draaien: python -m unittest <cedapress>/scripts/test_parse_bron.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_bron import bron_hash, parse, voor_vorm  # noqa: E402

BRON = """---
titel: Uitval in beeld
project: Instroomprognose
publiek: bestuurders mbo
kernboodschap: Uitval zit vooral in jaar 1
vorm: beide            # html | pptx | beide
fancy: B
---

## Slide 1 — Uitval in het eerste jaar
type: stats
Tekst op de slide: 1 op de 4 studenten stopt in jaar 1.
Notes: Benadruk dat dit landelijk is, niet per instelling.

::: html
Teller loopt op van 0 naar 25%.
:::
::: pptx
Statische grafiek; uitsplitsing op volgende slide.
:::

## Slide 2 — Uitsplitsing per sector
alleen: pptx
Tabel met mbo, hbo, wo.
Notes: Alleen in de pptx, in HTML zit dit achter een klik.

## Peiling
alleen: html
Mentimeter: wat verbaast je?
Notes: Twee minuten.
"""


class TestParseBron(unittest.TestCase):
    def setUp(self):
        self.doc = parse(BRON)

    def test_meta_en_slides(self):
        self.assertEqual(self.doc["fouten"], [])
        self.assertEqual(self.doc["meta"]["vormen"], ["html", "pptx"])
        self.assertEqual([s["titel"] for s in self.doc["slides"]],
                         ["Uitval in het eerste jaar", "Uitsplitsing per sector", "Peiling"])

    def test_slide_velden(self):
        s = self.doc["slides"][0]
        self.assertEqual(s["type"], "stats")
        self.assertIn("1 op de 4", s["tekst"])
        self.assertNotIn("Teller", s["tekst"])
        self.assertTrue(s["notes"].startswith("Benadruk"))
        self.assertEqual(s["html"], "Teller loopt op van 0 naar 25%.")
        self.assertTrue(s["pptx"].startswith("Statische grafiek"))

    def test_per_vorm(self):
        html = voor_vorm(self.doc, "html")
        pptx = voor_vorm(self.doc, "pptx")
        self.assertEqual([s["titel"] for s in html["slides"]], ["Uitval in het eerste jaar", "Peiling"])
        self.assertEqual([s["titel"] for s in pptx["slides"]], ["Uitval in het eerste jaar", "Uitsplitsing per sector"])
        self.assertEqual(html["slides"][0]["extra"], "Teller loopt op van 0 naar 25%.")
        self.assertNotIn("pptx", html["slides"][0])

    def test_fouten(self):
        doc = parse("## A\nalleen: beamer\n::: video\nx\n:::\n## B\n::: html\nopen")
        f = " ".join(doc["fouten"])
        self.assertIn("alleen moet html of pptx", f)
        self.assertIn("onbekend blok", f)
        self.assertIn("niet afgesloten", f)
        self.assertIn("geen slides", " ".join(parse("---\ntitel: x\n---\nlos")["fouten"]))

    def test_hash_stabiel_over_regeleinden(self):
        self.assertEqual(bron_hash(BRON), bron_hash(BRON.replace("\n", "\r\n")))
        self.assertNotEqual(bron_hash(BRON), bron_hash(BRON + "x"))
        self.assertRegex(bron_hash(BRON), r"^sha256:[0-9a-f]{16}$")


if __name__ == "__main__":
    unittest.main()
