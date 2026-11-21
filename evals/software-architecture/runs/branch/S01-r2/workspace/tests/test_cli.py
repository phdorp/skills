import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tally.cli import count_words, format_counts, main


class CountWords(unittest.TestCase):
    def test_counts_case_insensitively(self):
        self.assertEqual(count_words("The cat and the hat"),
                         {"the": 2, "cat": 1, "and": 1, "hat": 1})

    def test_ranks_by_count_then_alphabetically(self):
        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}), ["c 3", "a 1", "b 1"])

    def test_top_keeps_only_most_frequent(self):
        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}, top=2), ["c 3", "a 1"])

    def test_top_larger_than_vocabulary_keeps_all(self):
        self.assertEqual(format_counts({"b": 1, "a": 1}, top=10), ["a 1", "b 1"])


class Main(unittest.TestCase):
    def _run(self, text, argv_extra=()):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text(text)
        out = io.StringIO()
        with redirect_stdout(out):
            code = main([str(path), *argv_extra])
        return code, out.getvalue()

    def test_prints_every_word(self):
        code, out = self._run("b a b")
        self.assertEqual(code, 0)
        self.assertEqual(out, "b 2\na 1\n")

    def test_top_option_prints_only_n_words(self):
        code, out = self._run("b a b c c d", ["--top", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "b 2\nc 2\n")

    def test_top_option_rejects_non_positive(self):
        for bad in ("0", "-1", "x"):
            with self.subTest(value=bad), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    self._run("a", ["--top", bad])
                self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
