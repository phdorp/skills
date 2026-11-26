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

    def test_top_keeps_only_the_most_frequent_words(self):
        counts = {"b": 1, "a": 1, "c": 3, "d": 2}
        self.assertEqual(format_counts(counts, top=2), ["c 3", "d 2"])

    def test_top_larger_than_vocabulary_prints_all(self):
        self.assertEqual(format_counts({"a": 1}, top=5), ["a 1"])


class ParseTop(unittest.TestCase):
    def test_rejects_non_positive_top(self):
        with self.assertRaises(SystemExit):
            with redirect_stderr(io.StringIO()):
                main(["--top", "0", "nofile.txt"])


class Main(unittest.TestCase):
    def test_prints_every_word(self):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("b a b")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main([str(path)]), 0)
        self.assertEqual(out.getvalue(), "b 2\na 1\n")

    def test_top_prints_only_n_words(self):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("b a b c c c")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(["--top", "2", str(path)]), 0)
        self.assertEqual(out.getvalue(), "c 3\nb 2\n")


if __name__ == "__main__":
    unittest.main()
