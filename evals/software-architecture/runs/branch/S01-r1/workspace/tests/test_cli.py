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

    def _run(self, text, argv_extra):
        path = Path(tempfile.mkdtemp()) / "in.txt"
        path.write_text(text)
        out = io.StringIO()
        with redirect_stdout(out):
            code = main([str(path), *argv_extra])
        return code, out.getvalue()

    def test_top_prints_only_most_frequent_words(self):
        code, out = self._run("c c c b b a d", ["--top", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "c 3\nb 2\n")

    def test_top_larger_than_vocabulary_prints_all_words(self):
        code, out = self._run("b a b", ["--top", "10"])
        self.assertEqual(out, "b 2\na 1\n")

    def test_top_zero_prints_nothing(self):
        code, out = self._run("b a b", ["--top", "0"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_top_rejects_negative_number(self):
        with self.assertRaises(SystemExit) as ctx, redirect_stdout(io.StringIO()), \
                redirect_stderr(io.StringIO()):
            self._run("b a b", ["--top", "-1"])
        self.assertEqual(ctx.exception.code, 2)

    def test_top_rejects_non_integer(self):
        with self.assertRaises(SystemExit) as ctx, redirect_stdout(io.StringIO()), \
                redirect_stderr(io.StringIO()):
            self._run("b a b", ["--top", "many"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
