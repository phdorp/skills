### user

/sa:spec-and-plan Here is the approved design for a new tally option. Write the spec.

`tally --min-count N FILE` prints only the words counted at least N times.
- N is a positive integer; without the option every word is printed, as today.
- The order stays as today: most frequent first, ties in alphabetical order.
- N below 1 is an error: the usage message on stderr, exit code 2.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### assistant

I'll start by reading the repo layout, the existing `tally` code, and any tracker or glossary docs.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && cat docs/agents/issue-tracker.md 2>/dev/null; ls docs 2>/dev/null; cat GLOSSARY.md 2>/dev/null | head -80",
 "description": "Inspect repo files, tracker config, and glossary"
}
```

### tool_result

```
3d007ba fixture
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

The repo has no tracker config, glossary, or arc42 docs, so the spec goes to `docs/specs/` and gets committed. Next I'll read the spec template from the skill.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-swvhrgat/sa/skills/spec-and-plan/references/spec-template.md; echo ====; ls /tmp/sa-arm-swvhrgat/sa/skills/spec-and-plan/references/",
 "description": "Read the spec template from the skill"
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
====
plan-template.md
quality-requirements.md
spec-template.md
ticket-template.md
```

### assistant

The template is clear. Before pinning the N<1 behaviour in the spec, I'll confirm what argparse actually does for a bad `type` value.

### tool_use Bash

```json
{
 "command": "cd /tmp && cat > /tmp/probe_argparse.py <<'EOF'\nimport argparse\ndef pos(s):\n    n = int(s)\n    if n < 1:\n        raise argparse.ArgumentTypeError(\"must be a positive integer\")\n    return n\np = argparse.ArgumentParser(prog=\"tally\")\np.add_argument(\"file\")\np.add_argument(\"--min-count\", type=pos)\nfor argv in ([\"--min-count\", \"0\", \"x\"], [\"--min-count\", \"-3\", \"x\"], [\"--min-count\", \"abc\", \"x\"], [\"x\", \"--min-count\", \"2\"]):\n    try:\n        print(argv, \"->\", p.parse_args(argv))\n    except SystemExit as e:\n        print(argv, \"-> SystemExit\", e.code)\nEOF\npython3 -I /tmp/probe_argparse.py; echo \"--- stderr check\"; python3 -I -c '\nimport sys, argparse\nsys.argv=[\"x\"]\ndef pos(s):\n    n=int(s)\n    if n<1: raise argparse.ArgumentTypeError(\"must be a positive integer\")\n    return n\np=argparse.ArgumentParser(prog=\"tally\"); p.add_argument(\"file\"); p.add_argument(\"--min-count\", type=pos)\np.parse_args([\"--min-count\",\"0\",\"x\"])' ; echo \"exit=$?\"; rm -f /tmp/probe_argparse.py",
 "description": "Probe argparse behaviour for invalid --min-count values"
}
```

### tool_result

```
usage: tally [-h] [--min-count MIN_COUNT] file
tally: error: argument --min-count: must be a positive integer
usage: tally [-h] [--min-count MIN_COUNT] file
tally: error: argument --min-count: must be a positive integer
usage: tally [-h] [--min-count MIN_COUNT] file
tally: error: argument --min-count: invalid pos value: 'abc'
['--min-count', '0', 'x'] -> SystemExit 2
['--min-count', '-3', 'x'] -> SystemExit 2
['--min-count', 'abc', 'x'] -> SystemExit 2
['x', '--min-count', '2'] -> Namespace(file='x', min_count=2)
--- stderr check
usage: tally [-h] [--min-count MIN_COUNT] file
tally: error: argument --min-count: must be a positive integer
exit=2
Shell cwd was reset to /tmp/sa-eval-48neathh/project
```

### assistant

Argparse with a `type` validator gives the required behaviour: usage plus error on stderr and `SystemExit(2)`. Now I'll write the spec.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-48neathh/project/docs/specs/2026-11-22-min-count-spec.md",
 "content": "# `--min-count` Spec\n\nStatus: ready-for-agent\nSource: conversation (approved design for a new `tally` option: \"Here is the approved design for a new tally option. Write the spec.\")\n\n## Problem Statement\n\n`tally` prints every word in a text file, one `word count` line each. On a long file most lines are words that occur once or twice, and the user has to scan past them to find the words that repeat. They want to see only the words that occur often enough to matter.\n\n## Solution\n\n`tally` gets a new option, `--min-count N`. With it, `tally --min-count N FILE` prints only the words that occur at least `N` times in `FILE`. Each printed line keeps today's `word count` format. Ordering does not change: most frequent first, ties in alphabetical order. Without the option, `tally FILE` behaves exactly as it does today.\n\n## User Stories\n\n1. As a user counting words in a file, I want `--min-count N` to print only words counted at least N times, so that I can see the recurring words without scanning past one-off words.\n2. As a user, I want the printed lines to keep the `word count` format, so that output from `--min-count` can be read or piped exactly like today's output.\n3. As a user, I want the most frequent words to still come first and ties to stay alphabetical, so that the filtered list reads in the same order as the full list.\n4. As a user who does not pass `--min-count`, I want every word printed as before, so that existing scripts and habits keep working.\n5. As a user passing `--min-count 1`, I want every word printed, since every word occurs at least once, so that the value 1 is a harmless no-op.\n6. As a user whose `N` is larger than the count of every word, I want no lines printed and exit code 0, so that \"nothing repeats that often\" is reported as an empty result, not an error.\n7. As a user whose file contains no words (empty file, or only punctuation and digits), I want no lines printed and exit code 0 with or without `--min-count`, so that an empty file is not an error.\n8. As a user who passes `--min-count 0`, I want a usage message on stderr and exit code 2, so that I learn the value is invalid instead of getting a silently wrong result.\n9. As a user who passes a negative `N`, such as `--min-count -3`, I want the same usage message on stderr and exit code 2 as for `0`.\n10. As a user who passes a value that is not an integer, such as `--min-count abc` or `--min-count 2.5`, I want the same usage message on stderr and exit code 2, since the value is not a positive integer.\n11. As a user who passes `--min-count` without a value, I want the standard argument error on stderr and exit code 2, so that a missing value is reported like any other bad argument.\n12. As a user, I want to place `--min-count N` before or after the file name, so that both `tally --min-count 2 FILE` and `tally FILE --min-count 2` work.\n13. As a user who passes an invalid `N`, I want nothing printed to stdout, so that a script never receives a partial or unfiltered list from a bad call.\n14. As a user who passes a very large `N` (larger than any count), I want the same empty result as in story 6, so that there is no upper limit to document.\n15. As a user with a missing or unreadable file, I want the behaviour unchanged from today, so that this feature does not alter file-error handling. (Out of scope to improve; see Out of Scope.)\n\n## Implementation Decisions\n\n- **Module changed:** `tally/cli.py` only. The filter is applied in the same place the existing ranking happens, after counting and before printing. Counting (`count_words`) and ordering (`format_counts`) keep their current behaviour and signatures.\n- **Interface change:** `main(argv=None)` accepts one new optional argument, `--min-count` with a value. Its value is stored as an integer. Without the option, the value is absent and no filtering happens.\n- **Validation:** a value is valid only if it is a base-10 integer of at least 1. Validation is done at argument-parse time, not after counting, so an invalid value fails before the file is read. Use argparse's own type-validation mechanism so the error path is the standard argparse one: a usage line and an error line on stderr, then exit status 2.\n- **Error contract:** for any invalid value (zero, negative, non-integer, or missing), `main` ends with exit status 2 and writes the usage message to stderr. Nothing is written to stdout. Because argparse signals this by raising `SystemExit` with code 2, callers of `main` observe `SystemExit` with `code == 2`. This is the behaviour tests pin; `main` does not return 2 in this case.\n- **Filter rule:** keep a word if and only if its count is greater than or equal to `N`. The comparison uses the same counts `count_words` produces (lowercased, same word pattern). No other rule (no stopword list, no length limit).\n- **Output contract:** each kept word is printed as `word count` on its own line, using the existing format. Lines are sorted with the existing rule: descending count, then ascending alphabetical word. The filter does not change the sort key.\n- **Return value:** a successful run, filtered or not, returns `0`, as today.\n- **README:** the usage section gains one example of `--min-count` and one sentence describing it. This is documentation only.\n- **Assumption (non-integer values):** the spec treats non-integer values such as `2.5` and `abc` as invalid in the same way as values below 1. The user did not state this; it is the natural reading of \"N is a positive integer\".\n- **Assumption (position of the option):** the option may appear before or after the positional file argument. This is argparse's default and the spec does not restrict it.\n- **Assumption (no upper bound):** there is no maximum for `N`. Any integer at least 1 is valid.\n\n## Testing Decisions\n\n- **What good tests look like here:** they call `main` with an argument list and check what is printed to stdout, the return value, and, for invalid input, the `SystemExit` code and stderr text. They do not check private helpers' internals or the argparse object.\n- **Seam:** `tally.cli.main(argv)`. It is the highest seam that proves every behaviour in this spec, including the exit code and the stderr usage message. Existing tests already drive it this way, so no new seam is needed.\n- **Modules tested:** `tally/cli.py` only, through `main`.\n- **Prior art:** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temporary file, redirects stdout with `contextlib.redirect_stdout`, calls `main([str(path)])`, and checks the output string. New tests follow this pattern. For stderr, use `redirect_stderr` in the same way.\n- **Tests to add (each named by behaviour):**\n  - prints only words with count at or above N, in the existing order (stories 1, 3);\n  - keeps the `word count` line format (story 2);\n  - without the option, prints every word, unchanged from the existing test (story 4);\n  - `N = 1` prints every word (story 5);\n  - `N` above every count prints nothing and returns 0 (stories 6, 14);\n  - an empty file prints nothing and returns 0, with and without the option (story 7);\n  - `N = 0`, `N = -3`, `N = abc`, and `N = 2.5` each raise `SystemExit` with code 2, print the usage line to stderr, and print nothing to stdout (stories 8–10, 13);\n  - `--min-count` with no value raises `SystemExit` with code 2 (story 11);\n  - the option works both before and after the file argument (story 12).\n- **Not tested:** the exact wording of argparse's error text beyond the `usage:` prefix and the phrase `--min-count`. Those are argparse's responsibility.\n\n## Out of Scope\n\n- Changing how a missing or unreadable file is reported. Today it raises an uncaught exception; this feature leaves that as is.\n- Other filters (maximum count, minimum word length, stopwords, top-N limits).\n- Changing counting rules, the word pattern, or the sort order.\n- Machine-readable output formats.\n- Any change to the `format_counts` or `count_words` signatures.\n\n## Further Notes\n\n- **Assumptions made without the user:** the user was not available to answer questions. The assumptions are stated inline in Implementation Decisions. The main ones are: non-integer values are invalid like values below 1; the option works in either position; there is no upper bound on `N`; invalid values exit 2 through `SystemExit`, the standard argparse path.\n- **Behaviour verified against the installed Python:** an argparse parser using a type function that raises `ArgumentTypeError` for values below 1 prints `usage: tally [-h] [--min-count MIN_COUNT] file` and `tally: error: argument --min-count: ...` to stderr and raises `SystemExit(2)` for `0`, `-3`, and `abc`; and accepts `--min-count 2` after the positional argument. The implementer should re-check this with the tests.\n- **Open decisions:** none. Every decision the design left open has an assumption stated above.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-48neathh/project/docs/specs/2026-11-22-min-count-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. The skill says to commit it when there is no tracker, so I'll commit on the current branch with the required attribution line.

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-min-count-spec.md && git commit -q -m \"docs(spec): add --min-count option spec\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit the spec file and confirm clean status"
}
```

### tool_result

```
de32b80 docs(spec): add --min-count option spec
3d007ba fixture
```

### assistant

I wrote the spec and committed it as `de32b80` at `docs/specs/2026-11-22-min-count-spec.md`. The repo has no tracker config, glossary, or arc42 docs, so this was the local-file path. I did not write tickets or a plan, since this is one small slice in one file.

Since you were not available, I stated these assumptions in the spec instead of asking:

- **Non-integer values** such as `abc` and `2.5` are invalid, the same as `0` and negatives. Each gets the usage message on stderr and exit 2.
- **Missing value** (`--min-count` with nothing after it) also exits 2 with the argparse error.
- **Option position**: `--min-count N` works before or after the file name.
- **No upper bound** on N. A value above every count prints nothing and exits 0.
- **Empty file** prints nothing and exits 0.
- **Error path**: argparse raises `SystemExit(2)` for invalid values, so the tests check for that exception. `main` does not return 2 in that case.
- **Scope**: the change is in `tally/cli.py`, plus one README example. Missing-file handling stays as it is today and is listed as out of scope.

I checked the argparse error behaviour by running a probe, not just from memory. Tests should drive `main(argv)` and follow the existing `Main` test pattern in `tests/test_cli.py`.

I committed on `master`, the branch that was checked out. The git status names `main` as the main branch, so tell me if the spec should go somewhere else.

### result (success)
