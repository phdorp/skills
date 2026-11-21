import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tally.cli import count_words, format_counts, main


class CountWords(unittest.TestCase):
    def test_counts_case_insensitively(self):
        self.assertEqual(count_words("The cat and the hat"),
                         {"the": 2, "cat": 1, "and": 1, "hat": 1})

    def test_ranks_by_count_then_alphabetically(self):
        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}), ["c 3", "a 1", "b 1"])


class Main(unittest.TestCase):
    def test_prints_every_word(self):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("b a b")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main([str(path)]), 0)
        self.assertEqual(out.getvalue(), "b 2\na 1\n")

    def _run(self, text, *args):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text(text)
        out = io.StringIO()
        with redirect_stdout(out):
            status = main([*args, str(path)])
        return status, out.getvalue()

    def test_top_prints_only_most_frequent_words(self):
        status, out = self._run("c c c b b a", "--top", "2")
        self.assertEqual(status, 0)
        self.assertEqual(out, "c 3\nb 2\n")

    def test_top_larger_than_vocabulary_prints_all_words(self):
        status, out = self._run("b a b", "--top", "10")
        self.assertEqual(out, "b 2\na 1\n")

    def test_top_zero_prints_nothing(self):
        status, out = self._run("b a b", "--top", "0")
        self.assertEqual(status, 0)
        self.assertEqual(out, "")

    def test_top_breaks_ties_alphabetically(self):
        status, out = self._run("d c b a", "--top", "2")
        self.assertEqual(out, "a 1\nb 1\n")

    def test_negative_top_is_rejected(self):
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            self._run("b a", "--top", "-1")
        self.assertEqual(cm.exception.code, 2)

    def test_non_integer_top_is_rejected(self):
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            self._run("b a", "--top", "many")
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
