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
    def write_input(self, text="b a b"):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text(text)
        return str(path)

    def run_main(self, argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(argv)
        return code, out.getvalue()

    def test_prints_every_word(self):
        code, out = self.run_main([self.write_input()])
        self.assertEqual(code, 0)
        self.assertEqual(out, "b 2\na 1\n")

    def test_top_option_prints_only_n_words(self):
        code, out = self.run_main(["--top", "1", self.write_input("b a b c c c")])
        self.assertEqual(code, 0)
        self.assertEqual(out, "c 3\n")

    def test_top_option_accepted_after_file(self):
        code, out = self.run_main([self.write_input("b a b"), "--top", "1"])
        self.assertEqual(out, "b 2\n")

    def test_top_zero_or_negative_is_rejected(self):
        for value in ("0", "-2"):
            with self.subTest(value=value), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as cm:
                    main(["--top", value, self.write_input()])
                self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
