### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/stopwords.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1..HEAD && git diff HEAD~1..HEAD && ls docs docs/specs 2>/dev/null; ls docs/architecture 2>/dev/null; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS*' -o -iname 'CONTRIBUTING*' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STYLE*' \\) -print",
 "description": "Resolve range, show commit diff, list spec and standards files"
}
```

### tool_result

```
2a5be1a5dc3f94bdf6977ad62e3dd8bbc2581d10
8c58a3a73e8a024036e152729906da7a6b5858e5
8c58a3a feat: leave out stopwords
 docs/specs/stopwords.md | 15 +++++++++++++++
 tally/cli.py            | 29 ++++++++++++++++++++++++++---
 tests/test_cli.py       |  9 +++++++++
 3 files changed, 50 insertions(+), 3 deletions(-)
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
docs:
specs

docs/specs:
stopwords.md
```

### tool_use Bash

```json
{
 "command": "git show HEAD:tally/cli.py && echo ---- && find . -path ./.git -prune -o -type f -print && echo ---- && git show HEAD~1:tally/cli.py | head -20 && cat tally/__init__.py 2>/dev/null; ls tally; grep -rn \"format_counts\\|count_words\\|WORD\\b\" --include=*.py . ; git show HEAD:tests/test_cli.py | head -30",
 "description": "Read full CLI source, usages, and tests"
}
```

### tool_result

```
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
    parser.add_argument("--stopwords", metavar="FILE",
                        help="file of words to leave out, one per line")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    # read the stopword file: one word per line, '#' starts a comment
    stopwords = set()
    if args.stopwords:
        with open(args.stopwords, encoding="utf-8") as f:
            for raw in f:
                line = raw.split("#", 1)[0].strip().lower()
                if not line:
                    continue
                stopwords.add(line)
    # count every word that is not a stopword
    counts = Counter()
    for word in WORD.findall(text.lower()):
        if word in stopwords:
            continue
        counts[word] += 1
    # rank: most frequent first, ties in alphabetical order
    ranked = []
    for word, n in counts.items():
        ranked.append((-n, word))
    ranked.sort()
    # print one "word count" line per word
    for neg, word in ranked:
        print(f"{word} {-neg}")
    return 0
----
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
./docs/specs/stopwords.md
----
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
"""Word frequency counter."""
__init__.py
__main__.py
cli.py
tests/test_cli.py:7:from tally.cli import count_words, format_counts, main
tests/test_cli.py:12:        self.assertEqual(count_words("The cat and the hat"),
tests/test_cli.py:16:        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}), ["c 3", "a 1", "b 1"])
tally/cli.py:5:WORD = re.compile(r"[a-z']+")
tally/cli.py:8:def count_words(text):
tally/cli.py:9:    return Counter(WORD.findall(text.lower()))
tally/cli.py:12:def format_counts(counts):
tally/cli.py:36:    for word in WORD.findall(text.lower()):
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
        d = Path(tempfile.mkdtemp())
        (d / "in.txt").write_text("The cat and the hat")
```

### tool_use Bash

```json
{
 "command": "cat README.md; echo ----; cat tally/__main__.py; echo ----; cat /tmp/sa-arm-8t9802jr/sa/skills/code-review/references/standards-and-smells.md 2>/dev/null | head -150",
 "description": "Read README, entry point, and standards smell reference"
}
```

### tool_result

```
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
----
import sys

from tally.cli import main

sys.exit(main())
----
# Standards sources and the smell baseline

The Standards axis asks whether the diff conforms to how this repo writes code. Two kinds of source answer that: what the repo documents, and a fixed baseline of code smells for what it does not.

## 1. Find the documented standards

Search the repo for every file that says how code should be written. Typical candidates:

- `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `README.md` sections on style.
- `docs/` conventions, ADRs, architecture notes, review checklists, `STYLE.md`. When `docs/architecture/arc42.md` exists, ADRs and arc42 belong to the Architecture axis ([architecture-axis.md](architecture-axis.md)), not here.
- Linter and formatter configs (`.eslintrc*`, `eslint.config.*`, `ruff.toml`, `pyproject.toml`, `.golangci.yml`, `.rubocop.yml`, `.editorconfig`) — these show what tooling enforces, which you must not re-report.
- Language- or area-specific docs (`docs/api-guidelines.md`, `packages/*/README.md`).
- Domain vocabulary in `GLOSSARY.md`: a name that contradicts the glossary is a Mysterious Name finding with a documented fix.

List the files you found and check they exist in the checkout at `HEAD`. The reviewer has no other way to read them if you only name a path, so either pass their contents or confirm the reviewer can read them in its own checkout.

**Skip anything tooling already enforces.** A linter, formatter, or type checker that runs in CI owns those findings. Re-reporting them wastes the reviewer's budget and buries the judgement calls.

## 2. Apply the smell baseline

On top of whatever the repo documents, always carry this fixed set of Fowler code smells (_Refactoring_, ch. 3). Two rules bind it:

- **The repo overrides.** A documented repo standard always wins. Where a repo standard endorses something the baseline would flag, suppress the smell and say nothing.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. A documented-standard breach can be hard; a smell cannot.

Each smell reads *what it is* → *how to fix*. **(OO)** marks a smell that assumes objects and classes; its entry names the dataflow counterpart (blocks, connections, signals, as in `codebase-design`) where one exists. Match it against the diff:

- **Long Method**: a function so long that its parts need comments or names of their own. → extract the parts into named functions.
- **Large Class**: a class or module holding many unrelated fields or responsibilities. → split it along its responsibilities.
- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** (OO): a method that reaches into another object's data more than its own. → move the method onto the data it envies. Dataflow: a block reading another block's internal variables instead of its outputs → read its output signal, or add one.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one mod
[... 1408 chars cut]
```

### assistant

# Review of `8c58a3a` (feat: leave out stopwords)

Range: `HEAD~1..HEAD` (`2a5be1a..8c58a3a`), files `tally/cli.py`, `tests/test_cli.py`, `docs/specs/stopwords.md`. No files were changed.

I ran the two axes as separate inline passes rather than dispatching subagents, since you didn't ask for them. The repo has no standards docs (no CONTRIBUTING, CODING_STANDARDS, AGENTS.md, or linter config), so Standards uses the Fowler smell baseline only.

## Standards

Judgement calls from the smell baseline. No documented repo standard applies.

1. **Duplicated Code** (possible), `tally/cli.py:34-47`. `main()` re-implements `count_words` (the `Counter` loop at 35-39) and `format_counts` (the ranking at 40-44) inline instead of calling them. `format_counts` is now dead in production code and survives only because the tests import it. Fix: extract a filtered count helper and have `main` call `format_counts`, or make `count_words` take the stopword set. You decide which.
2. **Long Method** (possible), `tally/cli.py:17-48`. `main()` now does argument parsing, file reading, stopword loading, counting, ranking, and printing. The inline comments at lines 25, 34, and 40 mark parts that want names. Fix: extract `load_stopwords(path)` at least.
3. **Mysterious Name** (minor), `tally/cli.py:46-47`. `neg` holds a negated count, which is then negated back in `print`. Fix: store `(-n, word)` and unpack as `count` or use `sorted(...)` directly, which also drops the `ranked` append loop.

Worst Standards issue: Duplicated Code (possible), `tally/cli.py:34-47`.

## Spec

Checked against `docs/specs/stopwords.md`. The diff implements it faithfully.

- `--stopwords FILE` is added, and the file is read one word per line.
- `#` starts a comment (`split("#", 1)[0]`), blank lines are skipped, and matching is case-insensitive (both the stopword and the text are lowercased).
- Stopped words are excluded before counting.
- Without `--stopwords`, the output is unchanged: the sort key `(-n, word)` and the `word n` format match the old `format_counts`.
- `test_stopwords_are_left_out` covers comments, a blank line, mixed case, and an exclusion.

Gaps the spec does not decide, so these are not violations:

- A missing stopwords file raises an uncaught `FileNotFoundError`, the same way a missing input file already does. The spec is silent on this.
- `README.md` does not mention `--stopwords`. The spec does not require it.

Worst Spec issue: none that breaks the spec. The missing-file traceback is the only open question, and the spec should decide it if you want a clean error.

**Summary:** Standards has 3 findings (worst: Duplicated Code, `tally/cli.py:34-47`). Spec has 0 spec violations (worst: unspecified missing-file behaviour, `tally/cli.py:27-28`).

### result (success)
