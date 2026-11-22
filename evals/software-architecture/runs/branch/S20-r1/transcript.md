### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/stopwords.md. Report your findings; don't change any files.

### assistant

I'll pin the commit range, locate the spec and standards, then review the two axes in separate passes.

### tool_use Bash

```json
{
 "command": "git rev-parse main HEAD~1 HEAD && git log main..HEAD --oneline; echo \"---\"; git log HEAD~1..HEAD --oneline; echo \"---\"; git diff --stat HEAD~1..HEAD; echo \"---\"; ls docs docs/specs 2>/dev/null; echo \"---\"; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'arc42.md' \\) -print",
 "description": "Resolve refs, list commits, diff stat, and find spec and standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
main
---
8c58a3a feat: leave out stopwords
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
---
```

### tool_use Bash

```json
{
 "command": "git branch -a; echo \"---\"; git rev-parse HEAD~1 HEAD; echo \"---\"; git diff HEAD~1..HEAD; echo \"---\"; cat docs/specs/stopwords.md; echo \"---\"; ls -la; find . -path ./.git -prune -o -type f -print | head -100",
 "description": "Show branches, full diff, spec, and file listing"
}
```

### tool_result

```
* master
---
2a5be1a5dc3f94bdf6977ad62e3dd8bbc2581d10
8c58a3a73e8a024036e152729906da7a6b5858e5
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
total 28
drwxr-xr-x 6 root root 4096 Nov 22 16:02 .
drwx------ 3 root root 4096 Nov 22 18:20 ..
drwxr-xr-x 8 root root 4096 Nov 22 18:20 .git
-rw-r--r-- 1 root root  218 Nov 21 10:44 README.md
drwxr-xr-x 3 root root 4096 Nov 22 16:02 docs
drwxr-xr-x 2 root root 4096 Nov 22 16:02 tally
drwxr-xr-x 2 root root 4096 Nov 22 16:02 tests
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
./docs/specs/stopwords.md
```

### assistant

The `main` branch doesn't exist here, so I'm using `HEAD~1` (2a5be1a) as the fixed point, as you specified. Next I'll read the full files around the change.

### tool_use Bash

```json
{
 "command": "cat -n tally/cli.py; echo \"---\"; cat -n tests/test_cli.py; echo \"---\"; cat README.md; echo \"---\"; cat tally/__init__.py tally/__main__.py; echo \"---\"; git show 2a5be1a --stat | head -20",
 "description": "Read full source, tests, README, and prior commit"
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
---
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
---
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
---
"""Word frequency counter."""
import sys

from tally.cli import main

sys.exit(main())
---
commit 2a5be1a5dc3f94bdf6977ad62e3dd8bbc2581d10
Author: eval <eval@example.invalid>
Date:   Sun Nov 22 18:20:33 2026 +0100

    fixture

 README.md         | 10 ++++++++++
 tally/__init__.py |  1 +
 tally/__main__.py
[... 175 chars cut]
```

### assistant

The Spec axis is clear. Before I review Standards, I'll read the Standards reference the skill points to, and run the test suite without writing bytecode, so no files change.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-71mgtxdb/sa/skills/code-review/references/standards-and-smells.md; echo \"=== REVIEWER PROMPT ===\"; cat /tmp/sa-arm-71mgtxdb/sa/skills/code-review/references/reviewer-prompt.md; echo \"=== TESTS ===\"; cd /tmp/sa-eval-90h62kiv/project && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v 2>&1 | tail -15; echo \"=== INLINE COMMENT CHECK ===\"; cd /tmp/sa-eval-90h62kiv/project && PYTHONDONTWRITEBYTECODE=1 python3 -c \"\nimport io,tempfile,pathlib\nfrom contextlib import redirect_stdout\nfrom tally.cli import main\nd=pathlib.Path(tempfile.mkdtemp())\n(d/'in.txt').write_text('the cat the')\n(d/'stop.txt').write_text('the # article\\n')\no=io.StringIO()\nwith redirect_stdout(o): main([str(d/'in.txt'),'--stopwords',str(d/'stop.txt')])\nprint(repr(o.getvalue()))\n\"",
 "description": "Read standards reference, reviewer prompt, run tests, check inline comment"
}
```

### tool_result

```
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
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need sho
[... 8860 chars cut]
```

### assistant

## Review of `8c58a3a` (feat: leave out stopwords)

Range: `HEAD~1..HEAD` (2a5be1a → 8c58a3a) on `master`. There is no `main` branch in this repo, so I used `HEAD~1` as the fixed point, as you named it. The commit touches `docs/specs/stopwords.md`, `tally/cli.py` and `tests/test_cli.py`. No files were changed. The 4 tests pass.

## Standards

No documented standards exist here: no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, linter config, or style section in the README. I reviewed against the Fowler smell baseline, and these are judgement calls, not hard violations.

**1. Possible Duplicated Code, and dead helpers** (`tally/cli.py:35-47`, `tally/cli.py:8-14`)
- `main()` reimplements the counting and ranking that `count_words` and `format_counts` already do. The CLI no longer calls either helper; only the tests do.
- The ranking is also clumsy: it builds `(-n, word)` tuples, sorts them, then negates back with `-neg` at line 47.
- Fix (your call): filter the existing `Counter` and reuse `format_counts`:
  ```python
  counts = Counter({w: n for w, n in count_words(text).items() if w not in stopwords})
  for line in format_counts(counts):
      print(line)
  ```
  This keeps one ranking rule and removes about 10 lines.

**2. Possible Long Method** (`tally/cli.py:17-48`)
- `main()` grew from about 6 lines to about 32, and now covers argument parsing, file I/O, stopword parsing, counting, ranking and printing. Its inline comments at lines 25, 34, 40 and 45 mark the separate parts.
- Fix: extract `load_stopwords(path) -> set[str]`. This is cleaner whether or not finding 1 is applied.

## Spec

Spec source: `docs/specs/stopwords.md`. Every stated behaviour is implemented:
- `--stopwords FILE` is accepted (`tally/cli.py:20-21`).
- One word per line, blank lines ignored (`tally/cli.py:29-32`).
- `#` starts a comment. I checked both forms: a whole-line comment, and an inline `the # article`, which correctly drops `the`.
- Matching ignores case on both sides (`tally/cli.py:30`, `:36`).
- Without the flag, output is unchanged. The ordering matches the old `format_counts`, and `test_prints_every_word` covers it.
- Nothing beyond the spec was added. The built-in stopword list stays out of scope, as the spec says.

Findings (all minor):
- **Test gap:** `test_stopwords_are_left_out` covers only whole-line comments. The inline `#` case works but is not tested.
- **Unhandled missing file:** `--stopwords missing.txt` gives a raw `FileNotFoundError` traceback. The spec is silent on this, and the input file has the same behaviour. A reasonable user would expect a clean error.
- **Silent empty argument:** `--stopwords ""` is ignored (`if args.stopwords:`). This is a low-impact edge case.

**Declined to judge:** the `WORD` regex (`[a-z']+`) drops digits and non-ASCII letters. That tokenizer predates this commit and is outside this change.

---

**Per axis:** Standards has 2 findings, both judgement calls, and the worst is possible Duplicated Code (finding 1). Spec has 0 requirement violations and 3 minor findings, and the worst is the unhandled missing-file traceback.

### result (success)
