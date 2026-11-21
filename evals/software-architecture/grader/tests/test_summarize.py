import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import summarize  # noqa: E402


def v(c, ok=True):
    return {"criterion": c, "pass": ok, "quote": "q", "source": "transcript.md"}


class JudgeRate(unittest.TestCase):
    def test_rate_counts_passes_out_of_all_criteria(self):
        judge = {"criteria": ["J1", "J2"], "verdicts": [v("J1"), v("J2", False)],
                 "needs_review": False}
        self.assertEqual(summarize.judge_rate(judge), 0.5)

    def test_rate_is_none_while_run_needs_review(self):
        judge = {"criteria": ["J1", "J2", "J3"], "verdicts": [v("J1")], "needs_review": True}
        self.assertIsNone(summarize.judge_rate(judge))

    def test_rate_is_none_without_judge(self):
        self.assertIsNone(summarize.judge_rate(None))


if __name__ == "__main__":
    unittest.main()
