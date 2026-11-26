import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import grade  # noqa: E402


class Measure(unittest.TestCase):
    def test_has_measure_accepts_numbers(self):
        for text in ("0 unreadable logs in 100 trials", "the suite passes on all three OSes",
                     "100% of 50 sightings accepted", "every one of the twelve tests passes"):
            self.assertTrue(grade.has_measure(text), text)

    def test_has_measure_rejects_vague_wording(self):
        for text in ("every command feels fast", "all requests are quick", "fast enough",
                     "none of the users complain", "responds instantly for one user", "no"):
            self.assertFalse(grade.has_measure(text), text)


class Section(unittest.TestCase):
    TEXT = ("Intro.\n\n## Standards\n\n- long main\n\n## Architecture\n\n- ADR-0003 broken\n\n"
            "### Minor\n\n- QS-3 touched\n\n## Spec\n\n- fine\n")

    def test_section_reads_h2_up_to_next_same_level(self):
        body = grade.section(self.TEXT, "Architecture")
        self.assertIn("ADR-0003", body)
        self.assertIn("QS-3", body)  # a deeper heading stays inside
        self.assertNotIn("fine", body)

    def test_section_reads_h3(self):
        body = grade.section("# Review\n\n### Architecture\n\nADR-3\n\n### Spec\n\nok\n",
                             "Architecture")
        self.assertEqual(body.strip(), "ADR-3")

    def test_section_ignores_bold_text(self):
        self.assertIsNone(grade.section("**Architecture**\n\nADR-0003\n", "Architecture"))

    def test_section_accepts_decorated_heading(self):
        self.assertIn("x", grade.section("## 3. **Architecture** findings:\n\nx\n", "Architecture"))

    def test_section_skips_hash_lines_in_code_fences(self):
        text = "## Architecture\n\n```python\n# a comment\nimport sqlite3\n```\n\nADR-0003\n\n## Spec\n"
        self.assertIn("ADR-0003", grade.section(text, "Architecture"))

    def test_section_missing_is_none(self):
        self.assertIsNone(grade.section("## Standards\n\nx\n", "Architecture"))

    def test_section_runs_to_end(self):
        self.assertEqual(grade.section("## Architecture\n\nlast\n", "Architecture").strip(), "last")


def _write_block(path, content):
    body = json.dumps({"file_path": path, "content": content}, indent=1)
    return f"### tool_use Write\n\n```json\n{body}\n```\n\n### tool_result\n\nok\n\n"


class WrittenFile(unittest.TestCase):
    def _run_dir(self, transcript):
        d = Path(tempfile.mkdtemp(prefix="sa-test-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        (d / "transcript.md").write_text(transcript)
        return d

    def test_written_file_returns_last_write(self):
        d = self._run_dir("### user\n\nscan\n\n"
                          + _write_block("/tmp/architecture-review-1.html", "<p>first</p>")
                          + _write_block("/tmp/notes.md", "other")
                          + _write_block("/tmp/architecture-review-2.html", "<p>second ```</p>")
                          + "### assistant\n\ndone\n")
        self.assertEqual(grade.written_file(d, ".html"), "<p>second ```</p>")

    def test_written_file_none_without_write(self):
        d = self._run_dir("### user\n\nscan\n\n" + _write_block("/tmp/notes.md", "x")
                          + "### assistant\n\n### tool_use Write\n\nnot a heading\n")
        self.assertIsNone(grade.written_file(d, ".html"))
        self.assertIsNone(grade.written_file(Path(tempfile.mkdtemp(prefix="sa-test-")), ".html"))


class MarkedSections(unittest.TestCase):
    @staticmethod
    def doc(sections):
        return "# x\n\n" + "".join(f"## {n}. Heading {n}\n\n{body}\n\n" for n, body in sections)

    def test_marked_sections_requires_marker_in_filled_sections(self):
        text = self.doc([(2, "*As found, unconfirmed.*\n\n- stdlib only"),
                         (8, "Errors go to stderr with exit code 1.")])
        ok, detail = grade.marked_sections(text)
        self.assertFalse(ok)
        self.assertIn("8", detail)

    def test_marked_sections_ignores_empty_and_confirmed_sections(self):
        text = self.doc([(1, "| ID | requirement |\n|---|---|\n| R-1 | add items |"),
                         (5, "*As found, unconfirmed.*\n\n| block | responsibility |\n|---|---|\n| `cli` | commands |"),
                         (6, "| step | what |\n|---|---|"), (9, "ADRs in docs/adr/."),
                         (10, "| ID | measure |\n|---|---|\n| QS-1 | 0 lost |"), (12, "No terms yet.")])
        self.assertEqual(grade.marked_sections(text), (True, ""))

    def test_marked_sections_accepts_italic_marker(self):
        text = self.doc([(4, "*As found, unconfirmed*\n\nAppend-only file."),
                         (11, "_as found,\nunconfirmed_ - no lock around appends")])
        self.assertTrue(grade.marked_sections(text)[0])


class BaseWorkspace(unittest.TestCase):
    def test_base_workspace_skips_bytecode_left_in_the_fixture(self):
        cache = grade.run.SUITE / "fixtures" / "undocumented" / "pantry" / "__pycache__"
        made = not cache.exists()
        cache.mkdir(exist_ok=True)
        (cache / "stray.cpython-313.pyc").write_bytes(b"x")
        try:
            base = grade.base_workspace("S09")
            names = [p.name for p in base.rglob("*")]
            shutil.rmtree(base.parent, ignore_errors=True)
        finally:
            (cache / "stray.cpython-313.pyc").unlink()
            if made:
                cache.rmdir()
        self.assertNotIn("__pycache__", names)


def _tool_block(name, data):
    return f"### tool_use {name}\n\n```json\n{json.dumps(data, indent=1)}\n```\n\n### tool_result\n\n```\nok\n```\n\n"


class Turns(unittest.TestCase):
    def _run_dir(self, transcript):
        d = Path(tempfile.mkdtemp(prefix="sa-test-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        (d / "transcript.md").write_text(transcript)
        return d

    def test_turn_texts_splits_at_user_headings(self):
        d = self._run_dir("### user\n\nfirst\n\n### assistant\n\nlooking\n\n"
                          + _tool_block("Read", {"file_path": "/p/docs/architecture/arc42.md"})
                          + "### assistant\n\nWhich goals?\n\n### result (success)\n\n"
                          "### user\n\nsecond\n\n### assistant\n\nOption A serves QG-1.\n\n"
                          "### result (success)\n")
        texts = grade.turn_texts(d)
        self.assertEqual(len(texts), 2)
        self.assertIn("looking", texts[0])
        self.assertIn("Which goals?", texts[0])
        self.assertNotIn("arc42.md", texts[0])
        self.assertNotIn("first", texts[0])
        self.assertEqual(texts[1].strip(), "Option A serves QG-1.")

    def test_skill_called_matches_prefixed_and_plain(self):
        d = self._run_dir("### user\n\nx\n\n" + _tool_block("Skill", {"skill": "sa:add-requirements"}))
        self.assertTrue(grade.skill_called(d, "add-requirements"))
        plain = self._run_dir("### user\n\nx\n\n" + _tool_block("Skill", {"skill": "add-requirements"}))
        self.assertTrue(grade.skill_called(plain, "add-requirements"))
        read = self._run_dir("### user\n\nx\n\n"
                             + _tool_block("Read", {"file_path": "/s/add-requirements/SKILL.md"})
                             + "### assistant\n\nRun `/add-requirements`.\n")
        self.assertFalse(grade.skill_called(read, "add-requirements"))
        other = self._run_dir("### user\n\nx\n\n" + _tool_block("Skill", {"skill": "sa:domain-modeling"}))
        self.assertFalse(grade.skill_called(other, "add-requirements"))


class Report(unittest.TestCase):
    def _run_dir(self, transcript, status=None):
        d = Path(tempfile.mkdtemp(prefix="sa-test-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        (d / "transcript.md").write_text(transcript)
        if status is not None:
            (d / "git-status.txt").write_text(status)
        return d

    def test_last_message_is_final_assistant_text(self):
        d = self._run_dir("### user\n\ngo\n\n### assistant\n\nStarting.\n\n"
                          + _tool_block("Bash", {"command": "git commit"})
                          + "### assistant\n\nADR-0004 is proposed.\n\n### result (success)\n")
        self.assertEqual(grade.last_message(d).strip(), "ADR-0004 is proposed.")
        self.assertEqual(grade.last_message(self._run_dir("### user\n\ngo\n")), "")

    def test_uncommitted_reads_git_status(self):
        d = self._run_dir("", "?? docs/adr/0004-tags.md\n M notes/store.py\n")
        self.assertEqual(grade.uncommitted(d), ["docs/adr/0004-tags.md", "notes/store.py"])
        self.assertEqual(grade.uncommitted(self._run_dir("", "")), [])


ADR_TEXT = ("# {n}. {title}\n\n## Status\n\n{status}\n\n## Context\n\nServes R-1; keeps QS-3.\n\n"
            "## Decision\n\nDo it.\n\n## Consequences\n\nSome.\n")


class Tightened(unittest.TestCase):
    def _dir(self):
        d = Path(tempfile.mkdtemp(prefix="sa-test-"))
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        return d

    def test_is_proposed(self):
        self.assertTrue(grade.is_proposed("proposed"))
        self.assertTrue(grade.is_proposed(" Proposed "))
        for s in ("proposed 2026-11-22", "accepted 2026-11-22", ""):
            self.assertFalse(grade.is_proposed(s), s)

    def test_unquote_porcelain(self):
        self.assertEqual(grade.unquote_porcelain('"docs/adr/0004 tags.md"'), "docs/adr/0004 tags.md")
        self.assertEqual(grade.unquote_porcelain('"caf\\303\\251.md"'), "caf\u00e9.md")
        self.assertEqual(grade.unquote_porcelain("plain.md"), "plain.md")

    def test_uncommitted_unquotes_and_follows_renames(self):
        d = self._dir()
        (d / "git-status.txt").write_text('?? "docs/adr/0004 tags.md"\nR  old.py -> new.py\n')
        self.assertEqual(grade.uncommitted(d), ["docs/adr/0004 tags.md", "new.py"])

    def test_added_lines_finds_nested_and_root_files(self):
        base, ws = self._dir(), self._dir()
        for root in (base, ws):
            (root / "notes" / "sub").mkdir(parents=True)
            (root / "notes" / "sub" / "store.py").write_text("# old tag note\nx = 1\n")
        (ws / "notes" / "sub" / "store.py").write_text("# old tag note\nx = 1\ntags = []\n")
        (ws / "cli.py").write_text("parser.add_argument('--tag')\n")
        found = grade.added_lines(ws, base, "**/*.py", grade.TAG_WORD)
        self.assertEqual(sorted(found), ["cli.py", "notes/sub/store.py"])
        self.assertEqual(found["notes/sub/store.py"], ["tags = []"])

    def test_added_lines_ignores_unchanged_mentions(self):
        base, ws = self._dir(), self._dir()
        for root in (base, ws):
            (root / "a.py").write_text("# tag\n")
        self.assertEqual(grade.added_lines(ws, base, "**/*.py", grade.TAG_WORD), {})

    def test_status_line(self):
        self.assertTrue(grade.STATUS_NEEDS_DECISION.search("Done.\n\n**Status:** NEEDS_DECISION\n"))
        self.assertTrue(grade.STATUS_NEEDS_DECISION.search("Status: NEEDS_DECISION"))
        self.assertFalse(grade.STATUS_NEEDS_DECISION.search(
            "**Status:** DONE\n\nI would report NEEDS_DECISION if the ADR were open."))

    def _adrs(self, *specs):
        d = self._dir()
        paths = []
        for n, status in specs:
            p = d / f"{n:04d}-x.md"
            p.write_text(ADR_TEXT.format(n=n, title="X", status=status))
            paths.append(p)
        return paths

    def test_proposed_adrs_accepts_a_consecutive_split(self):
        ok, _ = grade.proposed_adrs(self._adrs((4, "proposed"), (5, "proposed")), 4, {"R-1", "QS-3"})
        self.assertTrue(ok)

    def test_proposed_adrs_rejects_gap_accepted_dated_or_unknown_ids(self):
        known = {"R-1", "QS-3"}
        self.assertFalse(grade.proposed_adrs(self._adrs((4, "proposed"), (6, "proposed")), 4, known)[0])
        self.assertFalse(grade.proposed_adrs(self._adrs((4, "proposed"), (5, "accepted 2026-11-22")), 4, known)[0])
        self.assertFalse(grade.proposed_adrs(self._adrs((4, "proposed 2026-11-22")), 4, known)[0])
        self.assertFalse(grade.proposed_adrs(self._adrs((5, "proposed")), 4, known)[0])
        self.assertFalse(grade.proposed_adrs(self._adrs((4, "proposed")), 4, {"R-1"})[0])
        self.assertFalse(grade.proposed_adrs([], 4, known)[0])


class OpenDecision(unittest.TestCase):
    def test_open_decision_passes_proposed_and_open_wording(self):
        for t in ("- ADR-0004 is proposed; the change follows it.",
                  "- Important: relies on a proposed ADR (ADR-0004).",
                  "- The change rests on ADR-0004, an open decision.",
                  "- ADR-0004 is not accepted, so this does not conform to a rule yet."):
            self.assertTrue(grade.open_decision(t), t)

    def test_open_decision_fails_conformance_and_loose_words(self):
        for t in ("- Conforms to ADR-0004: the export depends on its temp-file rule.",
                  "- No findings pending against ADR-0004.",
                  "- Compliant with proposed ADR-0004: writes atomically.",
                  "- ADR-0003 is proposed."):
            self.assertFalse(grade.open_decision(t), t)


if __name__ == "__main__":
    unittest.main()
