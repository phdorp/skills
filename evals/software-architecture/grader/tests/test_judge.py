import shutil
import sys
import tempfile
import unittest
from pathlib import Path

GRADER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GRADER))

import judge  # noqa: E402
import run  # noqa: E402

SUITE = GRADER.parent
REFERENCE = GRADER / "reference" / "S01"


def _run_dir():
    d = Path(tempfile.mkdtemp()) / "S01-r1"
    shutil.copytree(REFERENCE, d)
    return d


class Rubric(unittest.TestCase):
    def test_load_rubric_reads_criteria(self):
        rubric = judge.load_rubric(SUITE / "RUBRIC.md")
        self.assertEqual([c.id for c in rubric["S01"]], ["J1", "J2", "J3"])
        self.assertTrue(all(c.text for c in rubric["S01"]))


class Parse(unittest.TestCase):
    def test_parse_verdicts_takes_last_json_block(self):
        text = ('Example:\n```json\n[{"criterion": "J0"}]\n```\nVerdicts:\n```json\n'
                '[{"criterion": "J1", "pass": true, "quote": "q", "source": "transcript.md"}]\n```\n')
        self.assertEqual(judge.parse_verdicts(text)[0]["criterion"], "J1")

    def test_parse_verdicts_rejects_text_without_json(self):
        with self.assertRaises(ValueError):
            judge.parse_verdicts("no verdicts here")


class Quotes(unittest.TestCase):
    def setUp(self):
        self.run_dir = _run_dir()

    def v(self, quote, source="transcript.md"):
        return [{"criterion": "J1", "pass": True, "quote": quote, "source": source}]

    def test_verify_quotes_accepts_exact_quote_with_whitespace_differences(self):
        quote = "I'll add a failing test for `--top 1`,\n   then the option."
        self.assertEqual(judge.verify_quotes(self.v(quote), self.run_dir), [])

    def test_verify_quotes_accepts_workspace_file(self):
        quote = 'parser.add_argument("file", help="text file to count")'
        self.assertEqual(judge.verify_quotes(self.v(quote, "workspace/tally/cli.py"),
                                             self.run_dir), [])

    def test_verify_quotes_rejects_paraphrase(self):
        self.assertNotEqual(judge.verify_quotes(self.v("I added a test for top first."),
                                                self.run_dir), [])

    def test_verify_quotes_rejects_empty_quote(self):
        self.assertNotEqual(judge.verify_quotes(self.v("  "), self.run_dir), [])

    def test_verify_quotes_rejects_missing_source_file(self):
        self.assertNotEqual(judge.verify_quotes(self.v("OK", "workspace/nope.md"),
                                                self.run_dir), [])

    def test_verify_quotes_rejects_source_outside_run(self):
        self.assertNotEqual(judge.verify_quotes(self.v("OK", "../../etc/passwd"),
                                                self.run_dir), [])


class Prompt(unittest.TestCase):
    def test_build_prompt_contains_task_criteria_transcript_and_workspace_files(self):
        scenario = run.load_scenarios(SUITE / "TASKS.md")["S01"]
        criteria = judge.load_rubric(SUITE / "RUBRIC.md")["S01"]
        prompt = judge.build_prompt(scenario, criteria, REFERENCE)
        self.assertIn("Add a `--top N` option", prompt)
        self.assertIn(criteria[0].text, prompt)
        self.assertIn("I'll read the CLI and its tests first.", prompt)
        self.assertIn("=== workspace/tally/cli.py ===", prompt)
        self.assertNotIn("{{", prompt)


class Review(unittest.TestCase):
    def test_needs_review_when_criterion_missing(self):
        verdicts = [{"criterion": "J1", "pass": True, "quote": "OK", "source": "transcript.md"}]
        out = judge.assess(verdicts, ["J1", "J2"], _run_dir())
        self.assertTrue(out["needs_review"])
        self.assertIn("J2", " ".join(out["quote_errors"]))

    def test_no_review_when_all_quotes_verify(self):
        verdicts = [{"criterion": c, "pass": True, "quote": "OK", "source": "transcript.md"}
                    for c in ("J1", "J2")]
        out = judge.assess(verdicts, ["J1", "J2"], _run_dir())
        self.assertEqual((out["needs_review"], out["quote_errors"]), (False, []))


if __name__ == "__main__":
    unittest.main()
