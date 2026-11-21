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


if __name__ == "__main__":
    unittest.main()
