### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/stopwords.md. Report your findings; don't change any files.

### assistant

I'll run this inline: one pass per axis, kept separate, since I'm not dispatching subagents for this review.

### tool_use Bash

```json
{
 "command": "git rev-parse main HEAD~1 HEAD && git log main..HEAD --oneline && git log -1 --format='%H%n%s%n%b' HEAD && git diff --stat main HEAD~1..HEAD; echo \"---\"; git diff HEAD~1..HEAD; echo \"--- spec\"; ls docs/specs 2>/dev/null; ls docs/architecture 2>/dev/null; find . -maxdepth 3 \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'README.md' \\) -not -path './node_modules/*' -not -path './.git/*'",
 "description": "Resolve refs, show commit diff, list spec and standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
main
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
--- spec
stopwords.md
./README.md
```

### assistant

The `main` ref doesn't resolve here, so I'll check branches and read the full post-commit files.

### tool_use Bash

```json
{
 "command": "git branch -a && git rev-parse HEAD~1 HEAD && echo \"--- cli.py\" && cat -n tally/cli.py && echo \"--- tally package\" && ls tally && cat -n tally/__init__.py 2>/dev/null; echo \"--- tests\" && cat -n tests/test_cli.py && echo \"--- README\" && cat README.md && echo \"--- tests run\" && (python -m unittest discover -s tests -q 2>&1 | tail -5)",
 "description": "List branches, read cli, tests, README, and run tests"
}
```

### tool_result

```
* master
5d0bd65954345f31b9e3a020427686dfceee0b0d
e4ec04c8ea30002539608e05c0a6c95804a8e9df
--- cli.py
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
    21	                        help="file of words to leave out, one per line")
    22	    args = parser.parse_args(argv)
    23	    with open(args.file, encoding="utf-8") as f:
    24	        text = f.read()
    25	    # read the stopword file: one word per line, '#' starts a comment
    26	    stopwords = set()
    27	    if args.stopwords:
    28	        with open(args.stopwords, encoding="utf-8") as f:
    29	            for raw in f:
    30	                line = raw.split("#", 1)[0].strip().lower()
    31	                if not line:
    32	                    continue
    33	                stopwords.add(line)
    34	    # count every word that is not a stopword
    35	    counts = Counter()
    36	    for word in WORD.findall(text.lower()):
    37	        if word in stopwords:
    38	            continue
    39	        counts[word] += 1
    40	    # rank: most frequent first, ties in alphabetical order
    41	    ranked = []
    42	    for word, n in counts.items():
    43	        ranked.append((-n, word))
    44	    ranked.sort()
    45	    # print one "word count" line per word
    46	    for neg, word in ranked:
    47	        print(f"{word} {-neg}")
    48	    return 0
--- tally package
__init__.py
__main__.py
cli.py
     1	"""Word frequency counter."""
--- tests
     1	import io
     2	import tempfile
     3	import unittest
     4	from contextlib import redirect_stdout
     5	from pathlib import Path
     6	
     7	from tally.cli import count_words, format_counts, main
     8	
     9	
    10	class CountWords(unittest.TestCase):
    11	    def test_counts_case_insensitively(self):
    12	        self.assertEqual(count_words("The cat and the hat"),
    13	                         {"the": 2, "cat": 1, "and": 1, "hat": 1})
    14	
    15	    def test_ranks_by_count_then_alphabetically(self):
    16	        self.assertEqual(format_counts({"b": 1, "a": 1, "c": 3}), ["c 3", "a 1", "b 1"])
    17	
    18	
    19	class Main(unittest.TestCase):
    20	    def test_prints_every_word(self):
    21	        path = Path(tempfile.mkdtemp()) / "in.txt"
    22	        path.write_text("b a b")
    23	        out = io.StringIO()
    24	        with redirect_stdout(out):
    25	            self.assertEqual(main([str(path)]), 0)
    26	        self.assertEqual(out.getvalue(), "b 2\na 1\n")
    27	
    28	    def test_stopwords_are_left_out(self):
    29	        d = Path(tempfile.mkdtemp())
    30	        (d / "in.txt").write_text("The cat and the hat")
    31	        (d / "stop.txt").write_text("# common\nthe\n\nAND\n")
    32	        out = io.StringIO()
    33	        with redirect_stdout(out):
    34	            self.assertEqual(main([str(d / "in.txt"), "--stopwords", str(d / "stop.txt")]), 0)
    35	        self.assertEqual(out.getvalue(), "cat 1\nhat 1\n")
    36	
    37	
    38	if __name__ == "__main__":
    39	    unittest.main()
--- README
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
--- tests run
/bin/bash: line 1: python: command not found
```

### assistant

The base is `5d0bd65` and the commit is `e4ec04c` on `master`; there is no `main` branch in this repo. Next I'll run the suite and read the standards reference the skill points to.

### tool_use Bash

```json
{
 "command": "python3 -m unittest -v 2>&1 | tail -12; echo \"--- git show base for count of main() behaviour\"; git stash list | head -1; ls /tmp/sa-arm-q2tpg6rc/sa/skills/code-review/references/ && cat /tmp/sa-arm-q2tpg6rc/sa/skills/code-review/references/standards-and-smells.md",
 "description": "Run unit tests and read standards reference"
}
```

### tool_result

```
test_counts_case_insensitively (tests.test_cli.CountWords.test_counts_case_insensitively) ... ok
test_ranks_by_count_then_alphabetically (tests.test_cli.CountWords.test_ranks_by_count_then_alphabetically) ... ok
test_prints_every_word (tests.test_cli.Main.test_prints_every_word) ... ok
test_stopwords_are_left_out (tests.test_cli.Main.test_stopwords_are_left_out) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
--- git show base for count of main() behaviour
architecture-axis.md
receiving-feedback.md
reviewer-prompt.md
standards-and-smells.md
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
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the conce
[... 1727 chars cut]
```

### assistant

## Standards

No documented standards exist: there is no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or linter config. `README.md` has no style section. So these are judgement-call smells from the Fowler baseline, not documented-rule breaches.

1. **Duplicated Code** (possible), `tally/cli.py:40-47` and `tally/cli.py:13-14`. `main()` re-implements the ranking and formatting that `format_counts()` already does, using a negated-count tuple trick. Before this commit the CLI called `count_words` and `format_counts`. Now both helpers are dead on the CLI path and only their unit tests use them. Fix: build `counts` as a `Counter` and call `format_counts(counts)` again, which restores the original ordering logic.
2. **Long Method** (possible), `tally/cli.py:17-48`. `main()` now does argument parsing, file reading, stopword loading, counting, ranking, and printing, and it needs comment labels to show its parts. Fix: extract `load_stopwords(path)` for lines 25-33 and let `main()` read like its comments.
3. **Mysterious Name** (minor), `tally/cli.py:41-47`. `neg` and `-neg` exist only to sort descending while keeping alphabetical ties. Fix: `sorted(counts.items(), key=...)` as `format_counts` already does, which makes the tie-break visible.

## Spec

Source: `docs/specs/stopwords.md`. All four behaviour clauses are implemented:
- `--stopwords FILE` leaves out listed words.
- One word per line, blank lines ignored, `#` starts a comment (`split("#", 1)`).
- Matching ignores case (both the stopwords and the text are lowercased).
- Without `--stopwords`, output is unchanged. The ordering and format are the same as before, and `test_prints_every_word` passes.
- Built-in stopword list is not added, as the spec's out-of-scope section requires.

Gap (minor): `test_stopwords_are_left_out` does not prove comment handling. The `# common` line would not match any word in the input `"The cat and the hat"` even if comments were not stripped, so the test passes either way. Fix: put `common` in the input text, and add an inline-comment case such as `the # article`.

Not specified by the spec and not covered: a missing stopwords file produces a raw traceback. This is an open question for the spec author, not a violation.

## Architecture

Skipped: `docs/architecture/arc42.md` does not exist.

## Summary

- Standards: 3 judgement-call findings. Worst: Duplicated Code in `main()` (`cli.py:40-47`), which bypasses the existing `format_counts`.
- Spec: 0 unmet requirements. Worst: the comment-handling test does not verify comment stripping (`tests/test_cli.py:28-35`).

Notes: the repo has no `main` branch, so I took the base as `HEAD~1` (`5d0bd65`) against `HEAD` (`e4ec04c`) on `master`. The suite passes (4 tests, `python3 -m unittest`). I did not dispatch reviewer subagents; I ran each axis as a separate pass. No files were changed.

### result (success)
