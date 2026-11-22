### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/stopwords.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 main HEAD && git log HEAD~1..HEAD --oneline && git diff --stat main..HEAD~0 2>/dev/null | tail -3; echo ---; git diff HEAD~1..HEAD --stat; echo ---; ls docs docs/specs 2>/dev/null; ls docs/architecture 2>/dev/null; find . -path ./node_modules -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'eslint*' -o -iname 'pyproject.toml' -o -iname 'setup.cfg' -o -name '.flake8' -o -name 'ruff.toml' \\) -print",
 "description": "Resolve commits, diff stat, and find spec and standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
5d0bd65954345f31b9e3a020427686dfceee0b0d
main
---
 docs/specs/stopwords.md | 15 +++++++++++++++
 tally/cli.py            | 29 ++++++++++++++++++++++++++---
 tests/test_cli.py       |  9 +++++++++
 3 files changed, 50 insertions(+), 3 deletions(-)
---
docs:
specs

docs/specs:
stopwords.md
```

### tool_use Bash

```json
{
 "command": "git branch -a && git log --oneline -5 && echo --- && git diff HEAD~1..HEAD && echo --- && cat docs/specs/stopwords.md && echo --- && find . -path ./.git -prune -o -type f -print | grep -v __pycache__ | head -50",
 "description": "Show branches, recent log, diff, spec, and file list"
}
```

### tool_result

```
* master
e4ec04c feat: leave out stopwords
5d0bd65 fixture
---
diff --git a/docs/specs/stopwords.md b/docs/specs/stopwords.md
new file mode 100644
index 0000000..e93f913
--- /dev/null
+++ b/docs/specs/stopwords.md
@@ -0,0 +1,15 @@
+# Leave out stopwords
+
+## Problem
+
+Counts are dominated by words like "the" and "and".
+
+## Behaviour
+
+`tally FILE --stopwords WORDS` leaves out every word listed in the file WORDS. WORDS holds one
+word per line; `#` starts a comment; blank lines are ignored; matching ignores case. Without
+`--stopwords` the output is unchanged.
+
+## Out of scope
+
+A built-in stopword list.
diff --git a/tally/cli.py b/tally/cli.py
index a5952b5..7aafe9d 100644
--- a/tally/cli.py
+++ b/tally/cli.py
@@ -17,9 +17,32 @@ def format_counts(counts):
 def main(argv=None):
     parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
     parser.add_argument("file", help="text file to count")
+    parser.add_argument("--stopwords", metavar="FILE",
+                        help="file of words to leave out, one per line")
     args = parser.parse_args(argv)
     with open(args.file, encoding="utf-8") as f:
-        counts = count_words(f.read())
-    for line in format_counts(counts):
-        print(line)
+        text = f.read()
+    # read the stopword file: one word per line, '#' starts a comment
+    stopwords = set()
+    if args.stopwords:
+        with open(args.stopwords, encoding="utf-8") as f:
+            for raw in f:
+                line = raw.split("#", 1)[0].strip().lower()
+                if not line:
+                    continue
+                stopwords.add(line)
+    # count every word that is not a stopword
+    counts = Counter()
+    for word in WORD.findall(text.lower()):
+        if word in stopwords:
+            continue
+        counts[word] += 1
+    # rank: most frequent first, ties in alphabetical order
+    ranked = []
+    for word, n in counts.items():
+        ranked.append((-n, word))
+    ranked.sort()
+    # print one "word count" line per word
+    for neg, word in ranked:
+        print(f"{word} {-neg}")
     return 0
diff --git a/tests/test_cli.py b/tests/test_cli.py
index a64f0f8..c3d8e21 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -25,6 +25,15 @@ class Main(unittest.TestCase):
             self.assertEqual(main([str(path)]), 0)
         self.assertEqual(out.getvalue(), "b 2\na 1\n")
 
+    def test_stopwords_are_left_out(self):
+        d = Path(tempfile.mkdtemp())
+        (d / "in.txt").write_text("The cat and the hat")
+        (d / "stop.txt").write_text("# common\nthe\n\nAND\n")
+        out = io.StringIO()
+        with redirect_stdout(out):
+            self.assertEqual(main([str(d / "in.txt"), "--stopwords", str(d / "stop.txt")]), 0)
+        self.assertEqual(out.getvalue(), "cat 1\nhat 1\n")
+
 
 if __name__ == "__main__":
     unittest.main()
---
# Leave out stopwords

## Problem

Counts are dominated by words like "the" and "and".

## Behaviour

`tally FILE --stopwords WORDS` leaves out every word listed in the file WORDS. WORDS holds one
word per line; `#` starts a comment; blank lines are ignored; matching ignores case. Without
`--stopwords` the output is unchanged.

## Out of scope

A built-in stopword list.
---
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
./docs/specs/stopwords.md
```

### tool_use Bash

```json
{
 "command": "cat -n tally/cli.py | head -20 && echo --- && cat README.md && echo --- && cat tests/test_cli.py | head -28 && echo --- && git show HEAD~1:tally/cli.py | sed -n 1,20p && echo --- && (python3 -m unittest discover -s tests -t . 2>&1 | tail -5)",
 "description": "Read cli.py header, README, tests, base version, and run tests"
}
```

### tool_result

```
     1	import argparse
     2	import re
     3	from collections import Counter
     4	
     5	WORD = re.compile(r"[a-z']+")
     6	
     7	
     8	def count_words(text):
     9	    return Counter(WORD.findall(text.lower()))
    10	
    11	
    12	def format_counts(counts):
    13	    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    14	    return [f"{word} {n}" for word, n in ranked]
    15	
    16	
    17	def main(argv=None):
    18	    parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
    19	    parser.add_argument("file", help="text file to count")
    20	    parser.add_argument("--stopwords", metavar="FILE",
---
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
---
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

    def test_stopwords_are_left_out(self):
---
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
---
....
----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

### assistant

## Standards

Repo has no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or lint config. The only documented standard is `README.md`, so I checked against it and the existing code's structure.

1. **Duplicated logic in `main` (Important).** `main` re-implements counting and ranking instead of reusing `count_words` and `format_counts`, which still exist and are still tested. The stopword filter could be an optional argument to `count_words`, which would keep `main` to argument parsing, file IO, and printing. As written, the ranking logic now lives in two places that can drift apart. `main` is also a long method (args, file IO, stopword parsing, counting, ranking, printing).
   - `tally/cli.py:35-53`
2. **Less readable ranking idiom (Minor).** The `ranked.append((-n, word))` / `for neg, word in ranked` / `-neg` pattern is harder to follow than the existing `sorted(..., key=lambda item: (-item[1], item[0]))` already used in `format_counts`.
   - `tally/cli.py:45-52`
3. **README not updated (Minor).** The README documents usage, and the new `--stopwords FILE` flag is not mentioned.
   - `README.md`

## Spec

Spec: `docs/specs/stopwords.md`. The implementation meets every stated behaviour.

- `--stopwords WORDS` is added and leaves out every listed word: met (`tally/cli.py:20-21`, filter at line 41).
- One word per line: met.
- `#` starts a comment: met (`raw.split("#", 1)[0]`).
- Blank lines are ignored: met (`if not line: continue`).
- Matching ignores case: met (stopwords and text are both lowercased).
- Without `--stopwords` the output is unchanged: met by reading. The new inline ranking sorts by `(-count, word)`, the same key as the old `format_counts`, and the counting uses the same `WORD` regex on lowercased text. The existing `test_prints_every_word` covers this path.
- Out of scope (built-in stopword list): not added.

Tests: `python3 -m unittest discover -s tests -t .` runs 4 tests, all passing. The new `test_stopwords_are_left_out` covers comment, blank line, and case-insensitive matching.

No spec gaps found, so there are no spec findings to report.

**Summary:** Standards: 3 findings, worst is the duplicated counting and ranking logic in `main` (Important). Spec: 0 findings.

Notes on the run:
- The repo has no `main` branch (only `master`), so I used `HEAD~1` (`5d0bd65`) as the base, as you specified.
- I ran both axes inline rather than dispatching reviewer subagents, since you didn't ask for subagents.
- No files were changed.

### result (success)
