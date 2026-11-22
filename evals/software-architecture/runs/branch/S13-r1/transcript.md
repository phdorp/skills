### user

/sa:spec-and-plan Here is the approved design for a new tally option. Write the spec.

`tally --min-count N FILE` prints only the words counted at least N times.
- N is a positive integer; without the option every word is printed, as today.
- The order stays as today: most frequent first, ties in alphabetical order.
- N below 1 is an error: the usage message on stderr, exit code 2.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### assistant

I'll start by looking at the repo: the tracker config, the existing `tally` code, and any project docs the spec should follow.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; ls docs 2>/dev/null; cat GLOSSARY.md 2>/dev/null | head -80",
 "description": "Survey repo files, tracker config, and glossary"
}
```

### tool_result

```
f3abafc fixture
./README.md
./tally/__main__.py
./tally/cli.py
./tally/__init__.py
./tests/test_cli.py
./tests/__init__.py
---
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

The repo has no `docs/` directory, no tracker config, no glossary, and no ADRs, so the spec goes to the local form. Next I'll read the spec template and check the branch state before committing.

### tool_use Bash

```json
{
 "command": "git branch -a && git remote -v; echo ---; cat /tmp/sa-arm-s99i4x9j/sa/skills/spec-and-plan/references/spec-template.md; echo ---; python3 -m unittest 2>&1 | tail -3",
 "description": "Check branches, read spec template, run existing tests"
}
```

### tool_result

```
* master
---
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

### Quality Requirements (set-up projects only)

Only when `docs/architecture/arc42.md` exists. Cite by ID; arc42 and the ADRs hold the text.

- **Serves:** the parent requirements (`R-n`).
- **Keeps:** the quality scenarios (`QS-n`) the work must still meet.
- **Builds on:** the accepted ADRs it relies on.
- **Blocked by:** each decision the work needs that only a proposed ADR settles, with the ADR number. The spec does not build on it until the architect accepts it.

### Out of Scope

What this spec deliberately does not cover, and where that work goes instead if it is planned.

### Further Notes

Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
---
Ran 3 tests in 0.001s

OK
```

### assistant

The repo has one branch, `master`, and no tracker config, so I'll write the spec to `docs/specs/` and commit it on a feature branch. The design is one slice in one file, so I'm skipping tickets and the plan. Writing the spec now.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-kk1otici/project/docs/specs/2026-11-22-tally-min-count-spec.md",
 "content": "# Tally Min-Count Spec\n\nStatus: ready-for-agent\nSource: the approved design given in the conversation that produced this spec (`tally --min-count N FILE`). The design owner was not available for questions; every point the design left open is recorded as an assumption under Further Notes.\n\n### Problem Statement\n\n`tally` prints every distinct word in a file. On a long text, most of the output is words that appear once or twice, and the words that recur are buried among them. A user who wants to see only the recurring words has to scroll through or post-process the whole list.\n\n### Solution\n\n`tally` accepts a `--min-count N` option. When it is given, `tally` prints only the words that occur at least N times in the file. Each line keeps the same `word count` format and the same order as today: most frequent first, ties in alphabetical order. When the option is omitted, the output is exactly as it is today. When N is zero or negative, `tally` refuses to run and reports a usage error.\n\n### User Stories\n\n1. As a user counting words in a file, I want to pass `--min-count N`, so that only the words counted at least N times are printed.\n2. As a user, I want `tally FILE` without the option to print every word, exactly as it does today, so that existing scripts keep working.\n3. As a user, I want the filtered list in the same order as the unfiltered list (most frequent first, ties alphabetical), so that I can read it the same way.\n4. As a user, I want a word that occurs exactly N times to be included, so that the threshold is inclusive (\"at least N\").\n5. As a user, I want `--min-count 1` to print every word, so that the option never hides a word unless I ask it to.\n6. As a user, I want N larger than the most frequent word's count to produce no output and exit successfully, so that \"no word repeats that often\" is a normal answer and not an error.\n7. As a user, I want an empty file to print nothing and exit successfully, with or without the option.\n8. As a user, I want `--min-count 0` to fail with the usage message on stderr and exit code 2, so that a mistaken threshold cannot silently print nothing or everything.\n9. As a user, I want a negative N (for example `--min-count -3`) to fail the same way as zero, so that the error is consistent.\n10. As a user, I want a non-integer N (for example `abc`, `2.5`, or an empty string) to fail with the usage message on stderr and exit code 2, so that a typo is reported and not guessed at.\n11. As a user, I want `--min-count` with no value to fail with the usage message on stderr and exit code 2.\n12. As a user, I want to write the option before or after the file name, and as `--min-count=N` or `--min-count N`, so that it behaves like the other options of the standard argument parser.\n13. As a user, I want nothing written to stdout when the option is rejected, so that a pipeline does not receive partial or misleading output.\n14. As a user, I want a very large N (for example one billion) to be accepted and produce no output, so that I never hit an artificial upper limit.\n15. As a user, I want the README to show the new option, so that I can find it without reading the source.\n\n### Implementation Decisions\n\n- **Counting is unchanged.** Words are still counted case-insensitively with the same word pattern. The option does not change any count; it only decides which counted words are printed.\n- **Filtering happens after counting and before printing.** A word is printed if and only if its count is greater than or equal to N. Ranking (most frequent first, ties alphabetical) is applied to the kept words exactly as it is today.\n- **Interface of the counting and formatting helpers.** The counting helper keeps its current contract. The formatting helper gains an optional minimum count that defaults to 1, so every existing caller and every existing test keeps its current behaviour.\n- **The option is parsed by the existing argument parser.** The option takes one value. The value is validated as a positive integer at parse time. Any invalid value, whether below 1, non-integer, or missing, is reported through the parser's standard usage-error path: the usage line and a specific message on stderr, exit code 2, with nothing written to stdout. The exact wording of the specific message is not fixed by this spec.\n- **No new module, no new file.** The change lives in the existing CLI module, with a one-sentence addition to the README's usage description.\n- **Unchanged behaviour.** Missing file argument, unreadable file, and the program's exit code 0 on success are not changed by this feature.\n\n### Testing Decisions\n\n- **What makes a good test here.** Tests observe external behaviour: the lines printed to stdout, the text written to stderr, and the exit code. They do not inspect internal data structures or the order in which helpers are called.\n- **Seam.** The existing `main(argv)` entry point in the CLI module is the seam. It already proves the behaviour end to end (argument parsing, counting, filtering, output), and the existing tests use it with captured stdout. No new seam is proposed.\n- **Modules tested.** The CLI module only. One direct test of the formatting helper's minimum-count parameter is acceptable as a boundary check, but the main proof is through `main`.\n- **Required cases through `main`:**\n  - with `--min-count 2` on a file whose counts are 3, 2, 1: only the words with counts 3 and 2 are printed, in the existing order;\n  - with `--min-count` equal to a word's count: that word is printed (inclusive boundary);\n  - with `--min-count` greater than every count: nothing is printed and the exit code is 0;\n  - with `--min-count 1`: the output equals the output without the option;\n  - without the option: the output is byte-for-byte what `test_prints_every_word` already expects;\n  - with `--min-count 0`, `--min-count -1`, `--min-count abc`, `--min-count 2.5`, and a missing value: `SystemExit` with code 2, the usage text on stderr, and nothing on stdout;\n  - the option written after the file name and in the `--min-count=N` form: same output as the canonical form.\n- **Prior art.** `tests/test_cli.py`: `Main.test_prints_every_word` shows how to call `main` with a temporary file and capture stdout. `CountWords.test_ranks_by_count_then_alphabetically` shows the expected ordering that filtered output must keep. Stderr capture and the `SystemExit` check have no prior art in this repo and are new.\n\n### Out of Scope\n\n- Changing the word pattern, case handling, or ordering.\n- A maximum value for N, or any upper bound.\n- Reading from standard input, or handling a missing or unreadable file more gracefully than today.\n- Other output formats, such as JSON or CSV.\n- A short option letter for `--min-count`.\n- Any change to the exit code of a successful run.\n\n### Further Notes\n\nThe design owner was not available to answer questions. The following points were open in the approved design or are implied by it. Each is recorded here as an assumption to confirm, with the reason for it. None is deferred.\n\n- **A1. Non-integer values are rejected like values below 1.** The design names only \"N below 1\". N is specified as a positive integer, so `abc`, `2.5`, and an empty string are treated as the same kind of error: usage on stderr, exit code 2.\n- **A2. A missing value is rejected the same way.** `--min-count` with no value after it is a usage error with exit code 2.\n- **A3. Negative values are values, not options.** `--min-count -3` is read as the value -3 and then rejected under A1's rule for values below 1.\n- **A4. Repeated option: the last value wins.** This is the standard behaviour of the argument parser, and the spec does not add a rejection for repeats.\n- **A5. No upper bound on N.** A very large N is valid and produces no output.\n- **A6. Usage errors exit with SystemExit(2).** The error is raised through the argument parser, so the code path is the same one that already handles unknown options. Callers of `main` that catch `SystemExit` see code 2. `__main__` passes the exit status through unchanged.\n- **A7. The exact wording of the error message is not fixed.** Tests check that the usage text appears on stderr and that the exit code is 2. They do not compare the full message.\n- **A8. Seam choice.** The seam is the existing `main(argv)` entry point, as described under Testing Decisions. The design did not name a seam, so this was chosen by the spec author.\n- **A9. README.** The README's usage text gains one sentence describing the option. This is part of the change, not a separate task.\n- **A10. Filtering is inclusive.** A word whose count equals N is printed. This follows from \"at least N times\" in the design.\n\nNothing in this list is deferred. Each item becomes final when the design owner reads this spec and either accepts it or asks for a change.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-kk1otici/project/docs/specs/2026-11-22-tally-min-count-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. Next I'll create a feature branch (the repo's only branch is `master`) and commit the file.

### tool_use Bash

```json
{
 "command": "git checkout -b spec/tally-min-count && git add docs/specs/2026-11-22-tally-min-count-spec.md && git commit -q -F - <<'EOF'\ndocs: add spec for tally --min-count\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline -2 && git status --short && ls docs/specs",
 "description": "Create spec branch and commit the spec file"
}
```

### tool_result

```
Switched to a new branch 'spec/tally-min-count'
d6583fd docs: add spec for tally --min-count
f3abafc fixture
?? tally/__pycache__/
?? tests/__pycache__/
2026-11-22-tally-min-count-spec.md
```

### tool_use Bash

```json
{
 "command": "rm -rf tally/__pycache__ tests/__pycache__ && git status --short && echo clean",
 "description": "Remove test-run cache directories I created"
}
```

### tool_result

```
clean
```

### assistant

The spec is written and committed as `docs/specs/2026-11-22-tally-min-count-spec.md` on a new branch, `spec/tally-min-count` (commit `d6583fd`). The repo has no tracker config, so I used the local file form. I did not write tickets or a plan, since this is a single slice.

Because you were unavailable, I recorded every open point as an assumption in the spec's Further Notes, marked as not deferred. Please confirm or change these:

- **Non-integer values** (`abc`, `2.5`, empty string) are rejected the same way as values below 1: usage on stderr, exit code 2.
- **A missing value** (`--min-count` with nothing after it) is also an exit-2 usage error.
- **Negative values** like `-3` are rejected as below 1.
- **Repeated `--min-count`**: the last value wins, which is the argument parser's default.
- **No upper bound** on N. A very large N prints nothing and exits 0.
- **Error wording** is not fixed. Tests check for the usage text on stderr and exit code 2.
- **Seam**: the existing `main(argv)` entry point, which the current tests already use. No new seam.
- **README**: gets one sentence about the option.

The spec also covers the inclusive boundary (a word counted exactly N times is printed) and keeps the existing ordering and the no-option output unchanged.

### result (success)
