### user

/sa:spec-and-plan Here is the approved design for a new tally option. Write the spec.

`tally --min-count N FILE` prints only the words counted at least N times.
- N is a positive integer; without the option every word is printed, as today.
- The order stays as today: most frequent first, ties in alphabetical order.
- N below 1 is an error: the usage message on stderr, exit code 2.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -100 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"exit=$?\"; ls docs 2>/dev/null; cat GLOSSARY.md 2>/dev/null | head -50",
 "description": "Inspect repo layout, tracker config, glossary"
}
```

### tool_result

```
1dd54cd fixture
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
---
exit=1
```

### tool_use Bash

```json
{
 "command": "for f in README.md tally/__main__.py tally/cli.py tally/__init__.py tests/test_cli.py; do echo \"=== $f\"; cat -n \"$f\"; done",
 "description": "Read the tally source, tests, and README"
}
```

### tool_result

```
=== README.md
     1	# tally
     2	
     3	Counts word frequencies in a text file.
     4	
     5	```sh
     6	python3 -m tally notes.txt
     7	```
     8	
     9	Prints one `word count` line per word, most frequent first, ties in alphabetical order.
    10	Run the tests with `python3 -m unittest`.
=== tally/__main__.py
     1	import sys
     2	
     3	from tally.cli import main
     4	
     5	sys.exit(main())
=== tally/cli.py
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
    20	    args = parser.parse_args(argv)
    21	    with open(args.file, encoding="utf-8") as f:
    22	        counts = count_words(f.read())
    23	    for line in format_counts(counts):
    24	        print(line)
    25	    return 0
=== tally/__init__.py
     1	"""Word frequency counter."""
=== tests/test_cli.py
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
    28	
    29	if __name__ == "__main__":
    30	    unittest.main()
```

### tool_use Bash

```json
{
 "command": "cat -n /tmp/sa-arm-xx7ame0q/sa/skills/spec-and-plan/references/spec-template.md; echo ===; ls /tmp/sa-arm-xx7ame0q/sa/skills/spec-and-plan/references/; cd /tmp/sa-eval-6egot8jr/project && python3 -m unittest 2>&1 | tail -3; python3 --version",
 "description": "Read the spec template and check the test baseline"
}
```

### tool_result

```
     1	# Spec Template
     2	
     3	The body is identical for both publication forms; only the wrapper changes.
     4	
     5	## Local file form
     6	
     7	Save to `docs/specs/YYYY-MM-DD-<topic>-spec.md`. Start with a status line so a reader knows whether the spec is agreed or still moving:
     8	
     9	```markdown
    10	# <Feature> Spec
    11	
    12	Status: ready-for-agent
    13	Source: <path to the design doc, or the conversation that produced this>
    14	```
    15	
    16	## Tracker issue form
    17	
    18	- **Title**: `<Feature>`
    19	- **Labels**: `ready-for-agent` unless the user says otherwise.
    20	- **Body**: the sections below.
    21	- **Parent**: if the source was an existing issue, publish this spec as its sub-issue. Do not modify the parent.
    22	
    23	## Body
    24	
    25	### Problem Statement
    26	
    27	The problem the user is facing, from the user's perspective. What is painful today, who feels it, and what it costs them. No solution language.
    28	
    29	### Solution
    30	
    31	The solution to the problem, from the user's perspective. What changes for them when this ships.
    32	
    33	### User Stories
    34	
    35	A long, numbered list. Each one follows:
    36	
    37	```
    38	1. As an <actor>, I want <feature>, so that <benefit>
    39	```
    40	
    41	Cover every aspect of the feature, not just the happy path. Include:
    42	
    43	- first use, returning use, and empty state
    44	- permissions and roles
    45	- failure and recovery
    46	- limits and large inputs
    47	- accessibility and platform differences where they matter
    48	- the cases the user explicitly cares about
    49	
    50	Example:
    51	
    52	```
    53	1. As a mobile bank customer, I want to see balances on my accounts, so that I can make better-informed decisions about my spending.
    54	```
    55	
    56	### Implementation Decisions
    57	
    58	The decisions already made, in enough detail that a planner does not reopen them:
    59	
    60	- modules to build or modify, and their responsibilities
    61	- interfaces that change, in prose
    62	- technical clarifications from the developer
    63	- architectural decisions
    64	- schema changes
    65	- API contracts
    66	- specific interactions and sequences
    67	
    68	Do not include specific file paths or code snippets; they go stale quickly.
    69	
    70	Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.
    71	
    72	### Testing Decisions
    73	
    74	- What makes a good test here: external behaviour, through the agreed seams, not implementation details.
    75	- Which modules will be tested, and at which seam.
    76	- Prior art: similar tests already in the codebase, by path or name.
    77	
    78	### Out of Scope
    79	
    80	What this spec deliberately does not cover, and where that work goes instead if it is planned.
    81	
    82	### Further Notes
    83	
    84	Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
===
plan-template.md
quality-requirements.md
spec-template.md
ticket-template.md
Ran 3 tests in 0.001s

OK
Python 3.13.5
```

### tool_use Bash

```json
{
 "command": "cd /tmp && cat > /tmp/argcheck.py <<'EOF'\nimport argparse\ndef pos(s):\n    n = int(s)\n    if n < 1:\n        raise argparse.ArgumentTypeError(f\"must be a positive integer, got {s}\")\n    return n\np = argparse.ArgumentParser(prog=\"tally\")\np.add_argument(\"--min-count\", type=pos)\np.add_argument(\"file\")\nprint(p.parse_args([\"--min-count\", \"2\", \"f\"]))\np.parse_args([\"--min-count\", \"0\", \"f\"])\nEOF\npython3 -I /tmp/argcheck.py; echo \"exit=$?\"; rm -f /tmp/argcheck.py",
 "description": "Verify argparse error behaviour for invalid N"
}
```

### tool_result

```
usage: tally [-h] [--min-count MIN_COUNT] file
tally: error: argument --min-count: must be a positive integer, got 0
Namespace(min_count=2, file='f')
exit=2
Shell cwd was reset to /tmp/sa-eval-6egot8jr/project
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-6egot8jr/project/docs/specs/2026-11-22-min-count-spec.md",
 "content": "# Min-Count Option Spec\n\nStatus: ready-for-agent\nSource: conversation with the maintainer, which approved this design: `tally --min-count N FILE` prints only the words counted at least N times; N is a positive integer; without the option every word is printed as today; order unchanged (most frequent first, ties alphabetical); N below 1 is an error with the usage message on stderr and exit code 2.\n\n### Problem Statement\n\nWhen a text file is large, `tally` prints one line for every distinct word, including the many words that appear only once. The person reading the output has to scroll past or filter out those singletons by hand to see the words that actually recur. They want to ask for only the words that occur at least a given number of times.\n\n### Solution\n\n`tally` accepts a `--min-count N` option. When it is given, the output lists only the words that were counted at least N times, in the same order and format as today. When it is not given, the output is exactly what `tally` prints today.\n\n### User Stories\n\n1. As a writer reviewing a long draft, I want to run `tally --min-count 5 draft.txt`, so that I see only the words I repeat often and can spot overused vocabulary quickly.\n2. As a writer, I want the output order to stay the same as without the option (most frequent first, ties alphabetical), so that I can compare filtered and unfiltered runs without relearning the layout.\n3. As a writer, I want the output format to stay `word count` per line, so that scripts that already parse `tally` output keep working when they add the option.\n4. As a user who runs `tally FILE` today, I want the output to be unchanged when I do not pass `--min-count`, so that my existing workflows are not affected.\n5. As a user, I want `--min-count 1` to print the same output as no option at all, so that 1 is a safe lower bound that does not hide anything.\n6. As a user, I want a count threshold equal to a word's count to include that word (the comparison is \"at least N\"), so that `--min-count 3` shows a word that appears exactly three times.\n7. As a user, I want `--min-count` to be accepted before or after the file name, so that I can type the option in whichever position I remember.\n8. As a user, I want `--min-count=N` (the single-argument form) to work the same as `--min-count N`, so that the option matches the convention of other command-line tools.\n9. As a user, I want `--min-count 0` to fail with the usage message on stderr and exit code 2, so that a mistaken threshold is reported instead of silently printing everything.\n10. As a user, I want a negative value (for example `--min-count -3`) to fail with the same usage error and exit code 2, so that every value below 1 is treated the same way.\n11. As a user, I want a value that is not an integer (for example `abc` or `2.5`) to fail with the usage error and exit code 2, so that the option never accepts a threshold it cannot apply.\n12. As a user, I want a usage error to print nothing on stdout and to leave the file unread, so that a failed run produces no partial output.\n13. As a user, I want a threshold larger than every word's count (for example `--min-count 1000` on a short file) to print nothing and exit with code 0, so that an empty result is not reported as a failure.\n14. As a user, I want an empty input file to print nothing with or without the option and exit with code 0, so that the empty case behaves as it does today.\n15. As a user, I want a very large threshold to be accepted without special handling, so that I do not need to know the size of my file in advance.\n16. As a user, I want a missing or unreadable file to fail exactly as it does today when `--min-count` is given, so that the new option does not change file-error behaviour.\n17. As a user, I want `--help` to list the new option with a short description, so that I can discover it without reading this spec.\n\n### Implementation Decisions\n\n- **Counting is unchanged.** Words are counted exactly as today: case-insensitive, same word pattern, same counting step. The threshold is applied to the finished counts, not during counting.\n- **Filter.** A word is kept when its count is greater than or equal to N. The filter runs after counting and before output. Without the option, no filter is applied, which is equivalent to N = 1.\n- **Ordering and format.** Kept words are ordered by the existing rule (count descending, then word ascending) and printed in the existing `word count` format, one per line.\n- **Option.** One long option, `--min-count`, takes one value. It is optional and its default is \"no threshold\". Its value is parsed as an integer and must be at least 1. Any other value (below 1, non-integer, missing value) is a usage error.\n- **Usage error.** A usage error prints the standard argument-parser usage line and an error message on stderr, and exits with code 2. Nothing is written to stdout, and the input file is not opened. This is the behaviour the platform's argument parser already produces for invalid option values, so the implementation should rely on it rather than hand-write the message. Assumption: the \"usage message\" in the approved design means that standard usage line plus the error line.\n- **Exit codes.** Successful runs exit with 0, including runs that print nothing because no word meets the threshold. Usage errors exit with 2. File errors keep their current behaviour.\n- **Public interface.** The command-line interface gains `--min-count`. The `main` entry point keeps its existing signature and return behaviour; the option is added to the arguments it already parses. No other module's public behaviour changes.\n- **No new dependencies.** The option uses the argument parsing and counting already in the project.\n\n### Testing Decisions\n\n- **What makes a good test.** Tests assert external behaviour through the command-line entry point: the output lines, their order, the exit code, what is written to stdout and stderr, and whether an error occurs. Tests do not assert on internal helper calls or on how the filter is structured.\n- **Seam.** The `main(argv)` function in the CLI module is the seam. It is the highest existing seam that can prove every behaviour in this spec, including the usage error and exit code, so no new seam is needed. Assumption: no seam change is needed; the maintainer was not asked to confirm this.\n- **Modules tested.** The CLI module only. Counting and formatting helpers are already covered by unit tests and are not changed in behaviour, so they need no new tests unless the implementation changes them.\n- **Cases to cover through `main`:**\n  - without the option, output is identical to the current output for a file with several words of different counts (regression);\n  - `--min-count 2` keeps exactly the words with count 2 or more, with the same order as without the option;\n  - a word whose count equals N is included;\n  - `--min-count 1` gives the same output as no option;\n  - `--min-count` before and after the file argument both work, and `--min-count=N` works;\n  - a threshold above every count prints nothing and returns 0;\n  - an empty file prints nothing and returns 0 with and without the option;\n  - `0`, a negative value, and a non-integer each raise a system exit with code 2, print nothing to stdout, and print a usage line and an error message to stderr;\n  - a missing file with the option behaves as it does without the option.\n- **Prior art.** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`: it calls `main` with a temporary file, captures stdout with `redirect_stdout`, and checks the return code and output. New tests follow the same pattern and add `redirect_stderr` and an assertion on the raised `SystemExit` code for the error cases.\n- **Test runner.** Tests run with `python3 -m unittest`, as the README states.\n\n### Out of Scope\n\n- Other filters, such as a maximum count, a top-N limit, or a minimum word length. These are not part of this design.\n- Changes to what counts as a word, to case handling, or to the sort order.\n- Changes to output format, for example CSV or JSON output.\n- Changes to how missing or unreadable files are reported.\n- A short option letter for `--min-count`.\n- Documentation beyond the `--help` text and the existing README line. Updating the README's description of the output is left to the implementer as a single line if the maintainer wants it; this spec does not require it.\n\n### Further Notes\n\nAssumptions made because the maintainer was not available to answer. Each is recorded here so the planner and implementer can check them:\n\n1. **Non-integer values are usage errors.** `abc`, `2.5`, and an empty string are rejected like values below 1, with exit code 2. The approved design only named values below 1; this extends it to all invalid integers.\n2. **Inclusive threshold.** \"Counted at least N times\" is read as `count >= N`.\n3. **Threshold above all counts.** The output is empty and the exit code is 0. It is not treated as an error.\n4. **Usage error output.** Stdout is empty. Stderr has the standard usage line and the error line produced by the argument parser. The input file is not opened.\n5. **Option position and syntax.** Both `--min-count N` and `--min-count=N` are accepted, before or after the file name. This is the argument parser's default behaviour.\n6. **No upper bound.** Any positive integer is accepted. There is no maximum value.\n7. **Default is no filter.** Omitting the option is the same as `--min-count 1`, so the existing output is preserved exactly.\n8. **Seam.** The existing `main(argv)` entry point is the test seam. No new seam is introduced.\n\nNo decision in this spec is deferred. The open items above are assumptions for the maintainer to confirm or change after the fact; any change to them is a change to this spec, not a new design round.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-6egot8jr/project/docs/specs/2026-11-22-min-count-spec.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-min-count-spec.md && git commit -q -F - <<'EOF'\ndocs: add spec for --min-count option\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline | head -2 && git status --short",
 "description": "Commit the spec file and confirm clean tree"
}
```

### tool_result

```
5c850a5 docs: add spec for --min-count option
1dd54cd fixture
?? tally/__pycache__/
?? tests/__pycache__/
```

### tool_use Bash

```json
{
 "command": "rm -rf tally/__pycache__ tests/__pycache__ && git status --short && echo clean",
 "description": "Remove pycache artifacts from my test run"
}
```

### tool_result

```
clean
```

### assistant

The spec is written and committed at `docs/specs/2026-11-22-min-count-spec.md` (commit `5c850a5`). The repo has no tracker config, so it is a local file, not a tracker issue. I did not break the work into tickets or write a plan, since this is one small slice.

**Seam:** the existing `main(argv)` in `tally/cli.py`. The current tests already call it this way, and it can prove every behaviour, including the exit-2 usage error. No new seam.

**Assumptions I made where you were unavailable** (all recorded in the spec's Further Notes):
1. Non-integer values (`abc`, `2.5`, empty) are usage errors with exit 2, not just values below 1. Your design only named values below 1.
2. The threshold is inclusive: a word is kept when `count >= N`.
3. A threshold above every count prints nothing and exits 0. It is not an error.
4. "Usage message" means the argparse usage line plus the error line on stderr. Stdout stays empty, and the input file is not opened.
5. Both `--min-count N` and `--min-count=N` work, before or after the file name.
6. No upper bound on N. Omitting the option behaves like N = 1, so output is unchanged.

I confirmed the exit-2 and stderr behaviour by running argparse with a `type` that rejects values below 1.

The spec lists the test cases to add to `tests/test_cli.py`, following the existing `Main` test class. It does not reopen any decision you approved.

### result (success)
