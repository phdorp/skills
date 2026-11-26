### user

/sa:spec-and-plan Here is the approved design for a new tally option. Write the spec.

`tally --min-count N FILE` prints only the words counted at least N times.
- N is a positive integer; without the option every word is printed, as today.
- The order stays as today: most frequent first, ties in alphabetical order.
- N below 1 is an error: the usage message on stderr, exit code 2.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### assistant

I'll start by reading the repo: the tracker config, glossary, ADRs, and the existing `tally` code.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"---GLOSSARY\"; cat GLOSSARY.md 2>/dev/null; echo \"---ADR\"; find . -path ./.git -prune -o -iname '*adr*' -print",
 "description": "Inspect repo layout, tracker config, glossary, ADRs"
}
```

### tool_result

```
8424535 fixture
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
---
---GLOSSARY
---ADR
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

### assistant

No tracker config, glossary, or ADRs exist, so this spec goes to a local file. Next I'll read the spec template the skill points to.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-mhcgfou1/sa/skills/spec-and-plan/references/spec-template.md; echo; echo \"=== argparse probes\"; cd /tmp/sa-eval-laqvlexu/project && python3 -c \"import sys; print(sys.version)\"; printf 'b a b\\n' > /tmp/probe_in.txt; for a in \"--min-count 0\" \"--min-count -1\" \"--min-count abc\" \"--min-count\" \"--min-count 1.5\"; do echo \"## $a\"; python3 -m tally $a /tmp/probe_in.txt; echo \"exit=$?\"; done 2>&1 | head -60",
 "description": "Read spec template and probe current CLI behaviour"
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

=== argparse probes
3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]
## --min-count 0
usage: tally [-h] file
tally: error: unrecognized arguments: --min-count /tmp/probe_in.txt
exit=2
## --min-count -1
usage: tally [-h] file
tally: error: unrecognized arguments: --min-count /tmp/probe_in.txt
exit=2
## --min-count abc
usage: tally [-h] file
tally: error: unrecognized arguments: --min-count /tmp/probe_in.txt
exit=2
## --min-count
usage: tally [-h] file
tally: error: unrecognized arguments: --min-count
exit=2
## --min-count 1.5
usage: tally [-h] file
tally: error: unrecognized arguments: --min-count /tmp/probe_in.txt
exit=2
```

### assistant

The option doesn't exist yet, so those probes only confirm the baseline: argparse exits 2 with usage on stderr, which is the error path the spec should reuse. There's no tracker config, glossary, or ADR, so I'll write a local spec and commit it. The seam is the existing `main(argv)` used by `tests/test_cli.py`.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-laqvlexu/project/docs/specs && cat > /tmp/sa-eval-laqvlexu/project/docs/specs/2026-11-22-min-count-spec.md <<'EOF'\n# `--min-count` Spec\n\nStatus: ready-for-agent\nSource: approved design in the conversation of 2026-11-22 (`tally --min-count N FILE` prints only the words counted at least N times). The user was unavailable during spec writing; every point where a question would have been asked is stated as an assumption in Further Notes.\n\n### Problem Statement\n\n`tally` prints every word in a text file. On a long text most of the output is rare words, so a user who wants the frequent words has to scan past the whole list to find them.\n\n### Solution\n\n`tally` accepts a `--min-count N` option. When given, it prints only the words that occur at least N times in the file. Each printed line keeps today's format (`word count`), and the order stays most frequent first, ties in alphabetical order. Without the option, every word is printed, as today. N must be a positive integer; anything below 1 is a usage error.\n\n### User Stories\n\n1. As a writer reviewing a draft, I want to run `tally --min-count 3 draft.txt`, so that I see only the words I used three or more times.\n2. As a writer, I want a word used exactly N times to be included, so that the threshold is \"at least N\", not \"more than N\".\n3. As a writer, I want the kept words in the same order as the full output (most frequent first, ties alphabetical), so that I can read the two outputs side by side.\n4. As a user who runs `tally FILE` without the option, I want the output to be unchanged, so that existing scripts keep working.\n5. As a user who passes `--min-count 1`, I want the same output as when I omit the option, so that 1 is a no-op threshold.\n6. As a user whose N is larger than every word's count, I want no output and exit code 0, so that \"nothing matched\" is not treated as an error.\n7. As a user who passes `--min-count 0`, I want a usage message on stderr and exit code 2, with nothing printed to stdout, so that I learn the value is invalid.\n8. As a user who passes a negative N, I want the same usage error as for 0.\n9. As a user who passes a non-integer N (`abc`, `1.5`) or omits the value, I want a usage error with exit code 2.\n10. As a user who types the option after the file name (`tally FILE --min-count 3`), I want it to work the same as before the file name.\n11. As a user whose N is invalid and whose file does not exist, I want the usage error, so that I learn about the option before the file is opened.\n12. As a user of an empty file with `--min-count 2`, I want no output and exit code 0.\n13. As a user who runs `tally --help`, I want the option listed with a short description, so that I can discover it.\n14. As a user who passes a valid N and a file that does not exist, I want the same error as today, so that this change does not alter existing failure behaviour.\n\n### Implementation Decisions\n\n- **Interface change**: one new long-form option, `--min-count`, with an integer value. No short form. The value is required when the option is given.\n- **Validation at parse time**: values below 1 are rejected by the argument parser, so the error takes the same path as any other usage error: usage text and error line on stderr, exit code 2. Validation runs before the input file is opened.\n- **Filtering**: the filter is applied to the word counts after counting and before formatting. It compares each word's total occurrences in the file against N and keeps words where the total is at least N. Ordering and output format are unchanged, so the ranking rule stays in one place.\n- **Counting is unchanged**: words are still case-insensitive, and N is compared against the total number of occurrences, not the number of distinct words.\n- **Entry point**: `main(argv)` keeps its signature and its return value (0 on success). `count_words` and `format_counts` keep their current behaviour; the filter may be applied inside `main` or in a helper, which is the implementer's choice.\n- **Documentation**: the README's usage section gains the option, one line.\n\n### Testing Decisions\n\n- **Seam**: `main(argv)` in `tally/cli.py`. It is the highest existing seam and already covers the CLI contract. Tests pass an argument list, capture stdout and stderr, and check the return value or `SystemExit` code. No new seam is needed.\n- **Module under test**: `tally/cli.py`, through `main` only. Do not assert on internal helper names.\n- **What makes a good test here**: each test runs one command line against a temporary file and checks what a user would see: printed lines, stderr content, and exit code.\n- **Prior art**: `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temp file, calls `main([...])` inside `redirect_stdout`, and checks the output string. New tests follow that pattern and add stderr capture with `redirect_stderr`.\n- **Required tests** (new cases in `tests/test_cli.py`):\n  - threshold keeps words with count >= N, and drops the rest\n  - a word with count exactly N is kept\n  - kept words keep the most-frequent-first, alphabetical-tie order\n  - N = 1 produces the same output as omitting the option\n  - N above every count prints nothing and returns 0\n  - N = 0, a negative N, and a non-integer N each raise `SystemExit` with code 2, print usage to stderr, and print nothing to stdout\n  - the option with no value raises `SystemExit` with code 2\n  - the option after the file name works\n  - an invalid N with a non-existent file raises `SystemExit` with code 2, not `FileNotFoundError`\n  - an empty file with a valid N prints nothing and returns 0\n\n### Out of Scope\n\n- A maximum-count option or a range filter.\n- A short flag such as `-m`.\n- Any change to tokenising, case handling, or ranking.\n- Output formats other than `word count` lines (JSON, CSV).\n- Changes to the glossary: the repo has no `GLOSSARY.md`, and this spec adds no new domain terms.\n\n### Further Notes\n\nAssumptions made because the user was unavailable. Each is the reading I would have asked about. The user should confirm or correct them on review.\n\n1. **Non-integer values** (`abc`, `1.5`, empty string) are rejected with the same usage error and exit code 2 as N below 1. This follows from \"N is a positive integer\".\n2. **Negative values** are errors, the same as 0, because the design says \"N below 1 is an error\".\n3. **Threshold is inclusive**: a word is kept when its total count is at least N.\n4. **No matching words is not an error**: the output is empty and the exit code is 0.\n5. **Error text**: stderr contains the standard argparse usage line and an error line. The exact wording of the error line is not pinned; tests check for the usage line and exit code 2.\n6. **Option position**: the option may appear before or after `FILE`, as argparse allows by default.\n7. **Validation before file access**: an invalid N is reported before the file is opened.\n8. **No upper bound** on N. Very large integers are accepted and simply match no words.\n9. **README** gets a one-line mention of the option. This is a small documentation change inside the same work, not a new deliverable.\nEOF\ncd /tmp/sa-eval-laqvlexu/project && git add docs/specs/2026-11-22-min-count-spec.md && git commit -q -m \"docs: add spec for --min-count option\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline -2 && git status --short",
 "description": "Write the spec file and commit it"
}
```

### tool_result

```
155ba70 docs: add spec for --min-count option
8424535 fixture
?? tally/__pycache__/
```

### assistant

The spec is committed. The untracked `__pycache__` came from my probe run, and the tree was clean at the start, so I'll remove it.

### tool_use Bash

```json
{
 "command": "rm -rf tally/__pycache__ && git status --short && echo \"clean\"",
 "description": "Remove probe-generated pycache and confirm clean tree"
}
```

### tool_result

```
clean
```

### assistant

I wrote the spec and committed it as `155ba70` at `docs/specs/2026-11-22-min-count-spec.md`. The repo has no tracker config, glossary, or ADRs, so the local-file form applied.

The spec covers the problem and solution, 14 user stories (including the failure, empty-output, and no-regression cases), implementation decisions, and testing decisions. It sets the seam as the existing `main(argv)`, extending the `Main` test class in `tests/test_cli.py`. It also lists the tests to add.

Because you weren't available, I stated these assumptions in Further Notes rather than asking. Please confirm or correct them:

1. Non-integer values (`abc`, `1.5`) get the same usage error and exit 2 as N below 1.
2. Negative N is an error, like 0.
3. The threshold is inclusive: a word is kept when its count is at least N.
4. If no word meets the threshold, the output is empty and the exit code is 0.
5. The stderr error wording is argparse's default; tests check the usage line and exit 2.
6. The option works before or after `FILE`.
7. Validation runs before the file is opened, so an invalid N with a missing file gives the usage error.
8. N has no upper bound.
9. The README gets a one-line mention of the option.

The spec contains no code. The option does not exist yet, so I did not run any tests.

### result (success)
