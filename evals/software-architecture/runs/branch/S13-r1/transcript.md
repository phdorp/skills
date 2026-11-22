### user

/sa:spec-and-plan Here is the approved design for a new tally option. Write the spec.

`tally --min-count N FILE` prints only the words counted at least N times.
- N is a positive integer; without the option every word is printed, as today.
- The order stays as today: most frequent first, ties in alphabetical order.
- N below 1 is an error: the usage message on stderr, exit code 2.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### assistant

I'll start by reading the project's docs, the tracker config, and the code that implements `tally`.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -100 && cat docs/agents/issue-tracker.md 2>/dev/null; ls docs 2>/dev/null; cat GLOSSARY.md 2>/dev/null; cat README* 2>/dev/null | head -80",
 "description": "Inspect repo layout, docs, and README"
}
```

### tool_result

```
4500178 fixture
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Run the tests with `python3 -m unittest`.
```

### tool_use Bash

```json
{
 "command": "for f in tally/__main__.py tally/cli.py tally/__init__.py tests/test_cli.py tests/__init__.py; do echo \"=== $f\"; cat -n \"$f\"; done",
 "description": "Read the tally source and tests"
}
```

### tool_result

```
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
=== tests/__init__.py
```

### assistant

The repo has no tracker config, no `docs/agents`, no arc42, and no glossary, so this goes to the local form. Next I'll read the spec template the skill points to.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-htaujrzn/sa/skills/spec-and-plan/references/spec-template.md; echo ----; ls /tmp/sa-arm-htaujrzn/sa/skills/spec-and-plan/references/; date +%F",
 "description": "Read spec template and today's date"
}
```

### tool_result

```
# Spec Template

The body is identical for both publication forms; only the wrapper changes.

## Local file form

Save to `docs/specs/YYYY-MM-DD-<topic>-spec.md`. Start with a status line so a reader knows whether the spec is agreed or still moving:

```markdown
# <Feature> Spec

Status: ready-for-agent
Source: <path to the design doc, or the conversation that produced this>
```

## Tracker issue form

- **Title**: `<Feature>`
- **Labels**: `ready-for-agent` unless the user says otherwise.
- **Body**: the sections below.
- **Parent**: if the source was an existing issue, publish this spec as its sub-issue. Do not modify the parent.

## Body

### Problem Statement

The problem the user is facing, from the user's perspective. What is painful today, who feels it, and what it costs them. No solution language.

### Solution

The solution to the problem, from the user's perspective. What changes for them when this ships.

### User Stories

A long, numbered list. Each one follows:

```
1. As an <actor>, I want <feature>, so that <benefit>
```

Cover every aspect of the feature, not just the happy path. Include:

- first use, returning use, and empty state
- permissions and roles
- failure and recovery
- limits and large inputs
- accessibility and platform differences where they matter
- the cases the user explicitly cares about

Example:

```
1. As a mobile bank customer, I want to see balances on my accounts, so that I can make better-informed decisions about my spending.
```

### Implementation Decisions

The decisions already made, in enough detail that a planner does not reopen them:

- modules to build or modify, and their responsibilities
- interfaces that change, in prose
- technical clarifications from the developer
- architectural decisions
- schema changes
- API contracts
- specific interactions and sequences

Do not include specific file paths or code snippets; they go stale quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.

### Testing Decisions

- What makes a good test here: external behaviour, through the agreed seams, not implementation details.
- Which modules will be tested, and at which seam.
- Prior art: similar tests already in the codebase, by path or name.

### Out of Scope

What this spec deliberately does not cover, and where that work goes instead if it is planned.

### Further Notes

Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
----
plan-template.md
quality-requirements.md
spec-template.md
ticket-template.md
2026-11-22
```

### assistant

The repo has no tracker, so I'll write the spec to `docs/specs/` and commit it, as the local form requires. The existing `main(argv)` entry point is the seam, so no new seam is needed. The spec states the assumptions I'd otherwise have asked you about.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-3jusvxhb/project/docs/specs/2026-11-22-min-count-spec.md",
 "content": "# Minimum Count Option Spec\n\nStatus: ready-for-agent\nSource: approved design in the conversation that produced this spec (`tally --min-count N FILE`). The user was unavailable for questions; every gap is resolved under Further Notes as a stated assumption.\n\n## Problem Statement\n\n`tally` prints every word in a text file, most frequent first. For a long file, the output is mostly words that appear once or twice, and the words that matter are buried among them. A person who wants to see only the recurring words has to scroll or pipe the output through another tool to filter it.\n\n## Solution\n\n`tally` accepts a `--min-count N` option. When it is given, `tally` prints only the words that occur at least N times in the file. Each printed line keeps its current form (`word count`), and the order does not change: most frequent first, ties in alphabetical order. Without the option, `tally` prints every word, as it does today.\n\n## User Stories\n\n1. As a person analysing a text file, I want to pass `--min-count N` to see only words counted at least N times, so that the recurring words stand out.\n2. As a person analysing a text file, I want a word counted exactly N times to be printed, so that the threshold is inclusive and I do not lose words sitting on the boundary.\n3. As a person analysing a text file, I want the printed words to keep the current order (most frequent first, ties alphabetical), so that filtered output reads the same way as unfiltered output.\n4. As a person analysing a text file, I want `--min-count 1` to print the same output as running without the option, so that 1 is a neutral threshold.\n5. As a person analysing a text file, I want to run `tally` without `--min-count` exactly as before, so that existing scripts and habits keep working.\n6. As a person analysing a text file, I want `--min-count` to print nothing and exit successfully when no word reaches N, so that an empty result is distinguishable from an error.\n7. As a person analysing an empty file, I want `--min-count N` to print nothing and exit successfully, so that an empty file behaves the same with or without the option.\n8. As a person who mistypes the threshold, I want `--min-count 0` to be rejected with the usage message on stderr and exit code 2, so that I learn the input was wrong instead of getting silently empty or unfiltered output.\n9. As a person who mistypes the threshold, I want a negative `--min-count` to be rejected with the usage message on stderr and exit code 2, so that a nonsensical threshold is never applied.\n10. As a person who mistypes the threshold, I want a non-integer `--min-count` value (for example `abc` or `1.5`) to be rejected with the usage message on stderr and exit code 2, so that the option never has a meaning I did not intend.\n11. As a person who forgets the value, I want `--min-count` given with no value to be rejected with the usage message on stderr and exit code 2, so that the option is never silently ignored.\n12. As a person who writes the option before or after the file name, I want both `tally --min-count 2 FILE` and `tally FILE --min-count 2` to work, so that I do not have to remember an order.\n13. As a person reading the help, I want `tally --help` to list `--min-count` with a short description, so that I can discover the option without reading the README.\n14. As a person reading the README, I want a usage example of `--min-count`, so that the new option is documented where the existing usage is.\n\n## Implementation Decisions\n\n- **Module changed:** the command-line module (`tally/cli.py`). The counting step and the ordering step are not changed. The threshold filter is applied to the counts after counting and before the existing ordering and formatting.\n- **Interface changed:** the command-line interface gains one option, `--min-count`, which takes one value. The value is parsed as an integer by the same argument parser that already parses the file argument. The file argument stays required and positional.\n- **Parameter contract:** the public function `main(argv)` keeps its signature and its return value (`0` on success). It handles the new option and returns `0` after printing the filtered words.\n- **Validation:** a value that is not an integer, or is an integer below 1, is reported through the argument parser's usage-error path. That path prints the usage message and an error line to stderr and exits with code 2. No other error path is added for this option.\n- **Threshold rule:** a word is printed when its count is greater than or equal to N. Words below N are dropped before ordering.\n- **Unchanged behaviour:** word splitting (letters and apostrophes, case-insensitive), the output line format, the sort order, and the exit code of a successful run.\n- **Schema, API, and dependencies:** none. No new dependencies.\n- **README:** the README's usage section gains one example that shows `--min-count`.\n\n## Testing Decisions\n\n- **What makes a good test:** these tests check what the command prints and what exit code it returns, given an argument list and a file. They do not check how the filter is written internally.\n- **Seam:** the existing `main(argv)` entry point in `tally/cli.py`. It already takes an argument list, writes to stdout, and returns the exit code, so no new seam is introduced. Usage errors leave the function by raising `SystemExit`, so tests check the exit code of that exception.\n- **Module tested:** `tally/cli.py`, through `main`. The existing `format_counts` and `count_words` tests keep covering ordering and counting; they are not changed.\n- **Test cases to cover:**\n  - threshold keeps words at exactly N and drops words below N (stories 1, 2)\n  - order of the kept words matches the unfiltered order (story 3)\n  - `--min-count 1` output equals the output without the option (story 4)\n  - no option prints every word, as the existing test does (story 5)\n  - a threshold above every count prints nothing and returns `0` (story 6)\n  - an empty file with the option prints nothing and returns `0` (story 7)\n  - `0`, a negative value, a non-integer value, and a missing value each raise `SystemExit` with code `2`, and the usage text appears on stderr (stories 8 to 11)\n  - the option works before and after the file argument (story 12)\n- **Prior art:** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temporary file, captures stdout with `redirect_stdout`, and asserts the output and the return value. The new tests follow that pattern. For the error cases, capture stderr in the same way with `redirect_stderr`.\n- **Run command:** `python3 -m unittest`, as the README states.\n\n## Out of Scope\n\n- A maximum count option or a range option.\n- Filtering by word length or by a word list.\n- Changing what counts as a word.\n- Changing how a missing or unreadable file is reported. That behaviour stays as it is today.\n- Any change to the output format, such as a header line or totals.\n\n## Further Notes\n\nAssumptions made in place of questions to the user. Each one can be changed later by editing this spec.\n\n1. **Non-integer values are rejected the same way as values below 1.** The design named only `N < 1`. Using an integer parser for the option makes `abc` and `1.5` fail with the same usage error and exit code 2. This is the assumption most likely to differ from what the user wants.\n2. **Integer parsing is the parser's default.** Values such as `+3` and `03` are accepted, because that is what the integer conversion accepts. Values with a decimal point or an exponent are rejected (see assumption 1).\n3. **The threshold is inclusive.** A word counted exactly N times is printed.\n4. **No matching word is not an error.** When no word reaches N, the command prints nothing and returns exit code `0`.\n5. **Repeating the option uses the last value**, which is the parser's default when an option is given twice.\n6. **Error wording is not pinned.** The spec requires the usage message on stderr and exit code 2. The exact text of the error line is whatever the argument parser prints.\n7. **The option name is `--min-count` only.** No short form is added.\n\nNo decision in this spec is left open for later.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-3jusvxhb/project/docs/specs/2026-11-22-min-count-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

Before committing, I'll check the spec's claims about argparse behaviour (exit code 2, usage on stderr, `+3` accepted) against the real parser.

### tool_use Bash

```json
{
 "command": "cd /tmp && rm -rf /tmp/spec-check && mkdir /tmp/spec-check && cd /tmp/spec-check && printf 'b a b' > in.txt && cat > /tmp/spec-check/probe.py <<'EOF'\nimport argparse, io, contextlib, sys\np = argparse.ArgumentParser(prog=\"tally\")\np.add_argument(\"file\")\np.add_argument(\"--min-count\", type=int, metavar=\"N\")\nfor argv in ([\"in.txt\",\"--min-count\",\"0\"],[\"--min-count\",\"-1\",\"in.txt\"],[\"in.txt\",\"--min-count\",\"abc\"],[\"in.txt\",\"--min-count\",\"1.5\"],[\"in.txt\",\"--min-count\"],[\"in.txt\",\"--min-count\",\"+3\"],[\"--min-count\",\"2\",\"in.txt\"],[\"in.txt\",\"--min-count\",\"2\"]):\n    err = io.StringIO()\n    try:\n        with contextlib.redirect_stderr(err):\n            ns = p.parse_args(argv)\n        print(argv, \"OK\", ns.min_count)\n    except SystemExit as e:\n        print(argv, \"exit\", e.code, \"| stderr starts:\", err.getvalue().splitlines()[0])\nEOF\npython3 -I /tmp/spec-check/probe.py",
 "description": "Probe argparse behaviour for the spec's claims"
}
```

### tool_result

```
['in.txt', '--min-count', '0'] OK 0
['--min-count', '-1', 'in.txt'] OK -1
['in.txt', '--min-count', 'abc'] exit 2 | stderr starts: usage: tally [-h] [--min-count N] file
['in.txt', '--min-count', '1.5'] exit 2 | stderr starts: usage: tally [-h] [--min-count N] file
['in.txt', '--min-count'] exit 2 | stderr starts: usage: tally [-h] [--min-count N] file
['in.txt', '--min-count', '+3'] OK 3
['--min-count', '2', 'in.txt'] OK 2
['in.txt', '--min-count', '2'] OK 2
Shell cwd was reset to /tmp/sa-eval-3jusvxhb/project
```

### assistant

The probe shows that `type=int` alone accepts `0` and `-1`, so the `N < 1` check needs an explicit step. I'll make that explicit in the spec.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-3jusvxhb/project/docs/specs/2026-11-22-min-count-spec.md",
 "old_string": "- **Validation:** a value that is not an integer, or is an integer below 1, is reported through the argument parser's usage-error path. That path prints the usage message and an error line to stderr and exits with code 2. No other error path is added for this option.",
 "new_string": "- **Validation:** a value that is not an integer is rejected by the integer conversion. A value below 1 is not rejected by the conversion alone (it accepts `0` and negative numbers), so it needs an explicit check. Both failures go through the argument parser's usage-error path, which prints the usage message and an error line to stderr and exits with code 2. No other error path is added for this option."
}
```

### tool_result

```
The file /tmp/sa-eval-3jusvxhb/project/docs/specs/2026-11-22-min-count-spec.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "rm -rf /tmp/spec-check && git add docs/specs/2026-11-22-min-count-spec.md && git commit -q -m \"docs: add spec for tally --min-count option\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit the spec file and confirm clean tree"
}
```

### tool_result

```
ae5b4c3 docs: add spec for tally --min-count option
4500178 fixture
```

### assistant

The spec is written and committed at `docs/specs/2026-11-22-min-count-spec.md` (commit `ae5b4c3`). I did not write tickets or a plan. The spec was the only artifact requested, and the work is a single slice.

The repo has no tracker configuration, so I used the local form. I did not run `setup-project-workflow`, since it would have needed your input.

**Seam:** the existing `main(argv)` in `tally/cli.py`. No new seam is needed, and the tests follow the pattern already in `tests/test_cli.py`.

**Assumptions I stated in the spec in place of questions** (listed under Further Notes):
1. Non-integer values such as `abc` and `1.5` also fail with usage on stderr and exit 2. This is the one most likely to differ from what you want.
2. The threshold is inclusive: a word counted exactly N times is printed.
3. If no word reaches N, the command prints nothing and exits 0.
4. Values like `+3` are accepted, because that is what integer parsing accepts.
5. The option works before or after the file name.

**Finding from checking the spec:** argparse's `type=int` accepts `0` and negative numbers. The `N < 1` rule therefore needs an explicit check that routes through the same usage-error path. I wrote that into the spec's Validation decision.

The spec also covers the README example and the test cases, and it leaves no decisions open.

### result (success)
