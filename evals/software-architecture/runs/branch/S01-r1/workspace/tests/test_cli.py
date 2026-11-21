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


class Main(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / "in.txt"
        self.path.write_text("b a b c c c")

    def run_main(self, argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main([str(self.path), *argv])
        return code, out.getvalue()

    def test_prints_every_word(self):
        code, out = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(out, "c 3\nb 2\na 1\n")

    def test_top_prints_only_the_n_most_frequent_words(self):
        code, out = self.run_main(["--top", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "c 3\nb 2\n")

    def test_top_larger_than_vocabulary_prints_all_words(self):
        code, out = self.run_main(["--top", "10"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "c 3\nb 2\na 1\n")

    def test_top_zero_prints_nothing(self):
        code, out = self.run_main(["--top", "0"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_top_rejects_negative_numbers(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            self.run_main(["--top", "-1"])
        self.assertEqual(cm.exception.code, 2)

    def test_top_rejects_non_integers(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            self.run_main(["--top", "many"])
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
