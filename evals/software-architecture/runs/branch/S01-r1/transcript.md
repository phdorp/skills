### user

Add a `--top N` option to the tally CLI that prints only the N most frequent words
(all words when the option is absent). Work the way you normally would on a change like this,
add tests, make sure all tests pass, and commit your work. I'm not available for questions.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -100 && cat package.json 2>/dev/null; cat CLAUDE.md 2>/dev/null",
 "description": "Inspect project layout and status"
}
```

### tool_result

```
Exit code 1
d4c7e8e fixture
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
```

### tool_use Bash

```json
{
 "command": "for f in README.md tally/__main__.py tally/cli.py tally/__init__.py tests/test_cli.py tests/__init__.py; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read project source and test files"
}
```

### tool_result

```
=== README.md
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
=== tally/__main__.py
import sys

from tally.cli import main

sys.exit(main())
=== tally/cli.py
import argparse
import re
from collections import Counter

WORD = re.compile(r"[a-z']+")


def count_words(text):
    return Counter(WORD.findall(text.lower()))


def format_counts(counts):
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"{word} {n}" for word, n in ranked]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
    parser.add_argument("file", help="text file to count")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        counts = count_words(f.read())
    for line in format_counts(counts):
        print(line)
    return 0
=== tally/__init__.py
"""Word frequency counter."""
=== tests/test_cli.py
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


if __name__ == "__main__":
    unittest.main()
=== tests/__init__.py
```

### assistant

I'll add the tests first, then the option, then update the README and commit.

### tool_use Bash

```json
{
 "command": "python3 - <<'EOF'\nimport re\np='tests/test_cli.py'\ns=open(p).read()\ns=s.replace('''        self.assertEqual(format_counts({\"b\": 1, \"a\": 1, \"c\": 3}), [\"c 3\", \"a 1\", \"b 1\"])\n''','''        self.assertEqual(format_counts({\"b\": 1, \"a\": 1, \"c\": 3}), [\"c 3\", \"a 1\", \"b 1\"])\n\n    def test_top_keeps_only_most_frequent(self):\n        counts = {\"b\": 1, \"a\": 1, \"c\": 3, \"d\": 2}\n        self.assertEqual(format_counts(counts, top=2), [\"c 3\", \"d 2\"])\n\n    def test_top_larger_than_vocabulary_prints_all(self):\n        self.assertEqual(format_counts({\"a\": 1}, top=5), [\"a 1\"])\n''')\ns=s.replace('''        self.assertEqual(out.getvalue(), \"b 2\\\\na 1\\\\n\")\n''','''        self.assertEqual(out.getvalue(), \"b 2\\\\na 1\\\\n\")\n\n    def test_top_option_prints_only_n_words(self):\n        path = Path(tempfile.mkdtemp()) / \"in.txt\"\n        path.write_text(\"b a b c c c\")\n        out = io.StringIO()\n        with redirect_stdout(out):\n            self.assertEqual(main([str(path), \"--top\", \"2\"]), 0)\n        self.assertEqual(out.getvalue(), \"c 3\\\\nb 2\\\\n\")\n\n    def test_top_must_be_positive(self):\n        path = Path(tempfile.mkdtemp()) / \"in.txt\"\n        path.write_text(\"a\")\n        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):\n            main([str(path), \"--top\", \"0\"])\n''')\nopen(p,'w').write(s)\n\np='tally/cli.py'\ns=open(p).read()\ns=s.replace('''def format_counts(counts):\n    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))\n    return [f\"{word} {n}\" for word, n in ranked]\n''','''def format_counts(counts, top=None):\n    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))\n    if top is not None:\n        ranked = ranked[:top]\n    return [f\"{word} {n}\" for word, n in ranked]\n\n\ndef positive_int(text):\n    value = int(text)\n    if value < 1:\n        raise argparse.ArgumentTypeError(\"must be a positive integer\")\n    return value\n''')\ns=s.replace('''    parser.add_argument(\"file\", help=\"text file to count\")\n    args = parser.parse_args(argv)\n    with open(args.file, encoding=\"utf-8\") as f:\n        counts = count_words(f.read())\n    for line in format_counts(counts):''','''    parser.add_argument(\"file\", help=\"text file to count\")\n    parser.add_argument(\"--top\", type=positive_int, metavar=\"N\",\n                        help=\"print only the N most frequent words\")\n    args = parser.parse_args(argv)\n    with open(args.file, encoding=\"utf-8\") as f:\n        counts = count_words(f.read())\n    for line in format_counts(counts, top=args.top):''')\nopen(p,'w').write(s)\n\np='README.md'\ns=open(p).read()\ns=s.replace('''Prints one `word count` line per word, most frequent first, ties in alphabetical order.\n''','''Prints one `word count` line per word, most frequent first, ties in alphabetical order.\n\nUse `--top N` to print only the N most frequent words:\n\n```sh\npython3 -m tally --top 10 notes.txt\n```\n''')\nopen(p,'w').write(s)\nEOF\npython3 -m unittest -v 2>&1 | tail -15; python3 -m tally --top 2 README.md; python3 -m tally --top 0 README.md; echo \"exit $?\"",
 "description": "Add tests, --top option, and README docs; run tests"
}
```

### tool_result

```
test_counts_case_insensitively (tests.test_cli.CountWords.test_counts_case_insensitively) ... ok
test_ranks_by_count_then_alphabetically (tests.test_cli.CountWords.test_ranks_by_count_then_alphabetically) ... ok
test_top_keeps_only_most_frequent (tests.test_cli.CountWords.test_top_keeps_only_most_frequent) ... ok
test_top_larger_than_vocabulary_prints_all (tests.test_cli.CountWords.test_top_larger_than_vocabulary_prints_all) ... ok
test_prints_every_word (tests.test_cli.Main.test_prints_every_word) ... ok
test_top_must_be_positive (tests.test_cli.Main.test_top_must_be_positive) ... usage: tally [-h] [--top N] file
tally: error: argument --top: must be a positive integer
ok
test_top_option_prints_only_n_words (tests.test_cli.Main.test_top_option_prints_only_n_words) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.004s

OK
m 3
python 3
usage: tally [-h] [--top N] file
tally: error: argument --top: must be a positive integer
exit 2
```

### assistant

All 7 tests pass. The invalid-value test prints argparse's usage text to stderr, so I'll silence that and commit.

### tool_use Bash

```json
{
 "command": "python3 - <<'EOF'\np='tests/test_cli.py'\ns=open(p).read()\ns=s.replace(\"from contextlib import redirect_stdout\",\"from contextlib import redirect_stderr, redirect_stdout\")\ns=s.replace(\"with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):\",\"with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):\")\nopen(p,'w').write(s)\nEOF\npython3 -m unittest 2>&1 | tail -3 && git add -A && git commit -q -m \"feat(cli): add --top N to print only the N most frequent words\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Silence expected stderr, rerun tests, and commit"
}
```

### tool_result

```
Ran 7 tests in 0.002s

OK
5fcda74 feat(cli): add --top N to print only the N most frequent words
d4c7e8e fixture
```

### assistant

`tally` now accepts `--top N` and prints only the N most frequent words. Without the option it prints every word as before. The full suite passes (7 tests), and the work is committed as `5fcda74` on `master`.

- **Implementation:** `format_counts` takes an optional `top` and slices the existing ranking, so ties at the cutoff are broken alphabetically like everywhere else. `main` wires the option through.
- **Tests:** I added tests for the cutoff, for N larger than the vocabulary, for the CLI output with `--top 2`, and for rejecting `0`.
- **README:** added a short `--top` example.

One choice I made that you didn't specify: `--top` must be a positive integer. `--top 0` and negative values are rejected by argparse with exit code 2. If you'd rather `--top 0` print nothing, that's a one-line change.

### result (success)
