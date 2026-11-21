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

    def test_top_keeps_only_the_most_frequent(self):
        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}, top=2), ["c 3", "a 1"])

    def test_top_larger_than_vocabulary_keeps_all(self):
        self.assertEqual(format_counts({"b": 1, "a": 2}, top=10), ["a 2", "b 1"])


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

    def test_top_rejects_non_positive_values(self):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("a")
        for value in ("0", "-1", "x"):
            with self.subTest(value=value), redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as cm:
                    main(["--top", value, str(path)])
                self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
