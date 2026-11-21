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
    def test_prints_every_word(self):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("b a b")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main([str(path)]), 0)
        self.assertEqual(out.getvalue(), "b 2\na 1\n")

    def run_main(self, argv):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text("c a c b b b d")
        out = io.StringIO()
        with redirect_stdout(out):
            status = main([str(path), *argv])
        return status, out.getvalue()

    def test_top_prints_only_most_frequent_words(self):
        status, out = self.run_main(["--top", "2"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "b 3\nc 2\n")

    def test_top_larger_than_vocabulary_prints_all_words(self):
        status, out = self.run_main(["--top", "10"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "b 3\nc 2\na 1\nd 1\n")

    def test_top_zero_prints_nothing(self):
        status, out = self.run_main(["--top", "0"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "")

    def test_negative_top_is_rejected(self):
        err = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()), \
                redirect_stderr(err):
            self.run_main(["--top=-1"])
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("must be >= 0", err.getvalue())


if __name__ == "__main__":
    unittest.main()
