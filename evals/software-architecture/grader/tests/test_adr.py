import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import adr  # noqa: E402


def write(text, name="0004-export-format.md"):
    p = Path(tempfile.mkdtemp()) / name
    p.write_text(text)
    return p


HEADING = """# 4. Export notes as JSON Lines

## Status

Proposed

## Context

R-1 and QG-3.

## Decision

Export as JSON Lines.

## Consequences

Easy to parse.
"""

LABEL = """# Export notes as JSON Lines

**Status:** Accepted 2026-11-21
Context: R-2 matters.
**Decision:** JSON Lines.
Consequences: none.
"""


class Parse(unittest.TestCase):
    def test_parse_heading_style(self):
        a = adr.parse(write(HEADING))
        self.assertEqual((a.number, a.title), (4, "4. Export notes as JSON Lines"))
        self.assertEqual(set(a.fields), {"status", "context", "decision", "consequences"})
        self.assertIn("QG-3", a.fields["context"])

    def test_parse_label_style(self):
        a = adr.parse(write(LABEL))
        self.assertEqual(set(a.fields), {"status", "context", "decision", "consequences"})
        self.assertEqual(a.fields["decision"].strip(), "JSON Lines.")

    def test_status_is_lowercased_first_line(self):
        self.assertEqual(adr.parse(write(HEADING)).status, "proposed")
        self.assertEqual(adr.parse(write(LABEL)).status, "accepted 2026-11-21")

    def test_parse_heading_with_inline_value(self):
        a = adr.parse(write("# T\n\n## Status: Proposed\n\n## Context\n\nR-1\n"))
        self.assertEqual(a.status, "proposed")

    def test_subheadings_stay_inside_their_field(self):
        a = adr.parse(write("# T\n\n## Decision\n\n### Format\n\nJSON Lines.\n\n## Consequences\n\nNone.\n"))
        self.assertIn("JSON Lines.", a.fields["decision"])
        self.assertEqual(a.fields["consequences"], "None.")

    def test_status_styles_found_in_the_wild(self):
        for text in ("# T\n\n**Status**: proposed\n", "# T\n\n## Status\n\n`proposed`\n",
                     "# T\n\n## Status\n\n- Proposed\n"):
            self.assertEqual(adr.parse(write(text)).status, "proposed", text)

    def test_body_ignores_status_only(self):
        a = adr.parse(write(HEADING))
        b = adr.parse(write(HEADING.replace("Proposed", "accepted 2026-11-21")))
        c = adr.parse(write(HEADING.replace("Easy to parse.", "Hard to parse.")))
        self.assertEqual(adr.body(a), adr.body(b))
        self.assertNotEqual(adr.body(a), adr.body(c))

    def test_missing_field_absent_from_fields(self):
        a = adr.parse(write("# T\n\nJust a paragraph.\n"))
        self.assertEqual((a.fields, a.status), ({}, ""))


class Diff(unittest.TestCase):
    def test_new_and_changed_adrs(self):
        base, ws = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
        for d in (base, ws):
            (d / "docs" / "adr").mkdir(parents=True)
            (d / "docs" / "adr" / "0001-a.md").write_text("# A\n")
            (d / "docs" / "adr" / "0002-b.md").write_text("# B\n")
        (ws / "docs" / "adr" / "0002-b.md").write_text("# B changed\n")
        (ws / "docs" / "adr" / "0003-c.md").write_text("# C\n")
        self.assertEqual([p.name for p in adr.new_adrs(ws, base)], ["0003-c.md"])
        self.assertEqual([p.name for p in adr.changed_adrs(ws, base)], ["0002-b.md"])
        (ws / "docs" / "adr" / "0001-a.md").unlink()
        self.assertEqual([p.name for p in adr.changed_adrs(ws, base)], ["0001-a.md", "0002-b.md"])


if __name__ == "__main__":
    unittest.main()
