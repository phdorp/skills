# `--min-count` Spec

Status: ready-for-agent
Source: the approved design in the conversation that produced this spec: `tally --min-count N FILE` prints only the words counted at least N times. The user was unavailable for questions; every gap they would have been asked about is recorded as an assumption under Further Notes.

## Problem Statement

`tally` prints every word in a file, most frequent first. On a long text, the output is dominated by the long tail of words that appear once or twice. A user who wants only the recurring vocabulary has to filter the output by hand, which is slow and error-prone on a large list.

## Solution

`tally` accepts a `--min-count N` option. When it is given, the output lists only the words that appear at least N times in the file. Everything else is unchanged: the `word count` line format, the ordering (most frequent first, ties in alphabetical order), and the exit code on success. Without the option, every word is printed, as today.

## User Stories

1. As a user, I want to run `tally --min-count 3 notes.txt`, so that I see only the words that occur at least three times.
2. As a user, I want the option to work when it appears after the file name, so that I can add it to the end of a command I already typed.
3. As a user, I want the `--min-count=3` form to work, so that I can use the style I already use with other tools.
4. As a user, I want `--min-count 1` to print the same output as running without the option, so that I can rely on 1 as the "no filtering" value.
5. As a user, I want a word that occurs exactly N times to be included, so that the boundary is inclusive and matches the wording "at least N times".
6. As a user, I want the surviving words to keep the same order as the unfiltered output, so that I can compare the two outputs directly.
7. As a user, I want ties at the cut-off to be ordered alphabetically like every other tie, so that the output is predictable.
8. As a user, I want the output to be empty and the exit code to be 0 when no word reaches N, so that a script can treat "no recurring words" as a normal result.
9. As a user, I want the output to be empty and the exit code to be 0 when the file is empty, so that an empty file behaves as it does today.
10. As a user, I want `N` of 0 to be rejected, so that a mistake is caught instead of silently printing everything.
11. As a user, I want a negative `N` to be rejected, so that a sign mistake is caught.
12. As a user, I want a non-integer `N` (such as `abc` or `2.5`) to be rejected, so that the value is never guessed.
13. As a user, I want a rejected `N` to print the usage message on stderr and exit with code 2, so that I see the standard argument-error output and scripts can detect it.
14. As a user, I want a rejected `N` to print nothing on stdout, so that a failed run does not look like a partial result.
15. As a user, I want `--min-count` with no value to be rejected with the usage message and exit code 2, so that a forgotten number is caught.
16. As a user, I want `--help` to list the new option with a short description, so that I can discover it without reading the README.
17. As a user, I want the README to show the new option with one example, so that the documented usage matches the program.
18. As a user, I want a missing input file to fail exactly as it does today, so that the new option does not change error handling for files.
19. As a user, I want a very large N, larger than every count in the file, to print nothing and exit 0, so that I do not need to know the largest count in advance.
20. As a user, I want a repeated `--min-count` to use the last value given, so that the behaviour matches other argparse-based tools.
21. As a user, I want the option to work with an input file that contains words with apostrophes or mixed case, so that the filter uses the same word definition as the rest of the tool.

## Implementation Decisions

- **Scope of change**: one new option on the existing command-line entry point. The word-counting rule, the output line format, and the sort order do not change.
- **Filter placement**: the filter is applied to the word counts after counting and before formatting. A word is kept when its count is greater than or equal to N. Sorting is applied to the kept words with the same rule as today: descending count, then ascending word.
- **Value validation**: N is accepted only when it is an integer of value 1 or more. Any other value (zero, negative, non-integer text, or a missing value) is rejected by the argument parser, which prints the usage line and an error line on stderr and exits with code 2. Nothing is printed to stdout in that case.
- **Option syntax**: the option takes one value. Both the separate-argument form and the `=` form are accepted. The option may appear before or after the file argument. If the option is repeated, the last value wins.
- **Default**: when the option is absent, behaviour is identical to today. Equivalently, the default is a minimum of 1.
- **Help text**: the option appears in the help output with the metavar `N` and a one-line description that says the option hides words counted fewer than N times.
- **Interfaces**: the public command-line interface gains the `--min-count N` option. The `main` entry point keeps its existing contract: it takes an optional argument list, returns 0 on success, and writes results to stdout. Its failure path for an invalid N is the argument parser's standard exit (code 2), so the entry point does not need a new return value.
- **Counting and formatting helpers**: the existing counting and formatting functions keep their current behaviour when no threshold is given. A threshold may be added as an optional parameter to the formatting step, with a default that keeps today's output.
- **Schema, network, and persistence**: none.

## Testing Decisions

- **What makes a good test**: assert on externally visible behaviour: the lines printed to stdout, the text printed to stderr, and the exit code. Do not assert on internal data structures or on the order in which helper functions are called.
- **Seam**: the command-line entry point `main` is the highest seam that can prove the option's behaviour end to end, including the exit code and stderr. Use it for the boundary cases, the error cases, and the position and syntax of the option. This is an existing seam; no new seam is introduced.
- **Secondary seam**: the existing ranking helper may be tested directly for the threshold rule (inclusive boundary, ties at the cut-off, empty input), because it is a pure function and its tests are cheap. This is also an existing seam.
- **Modules tested**: the command-line entry point and the ranking helper. The counting helper is not changed and needs no new tests beyond its existing ones.
- **Prior art**: `tests/test_cli.py` already tests the ranking helper (`format_counts`, ordering by count then word) and the entry point (`main`, with a temporary input file and output captured by `redirect_stdout`). New tests follow the same style, using `unittest`. For stderr capture and the exit code, use the same redirection pattern on the error stream and catch the `SystemExit` that the argument parser raises.
- **Required test cases**:
  - threshold filters out words below N and keeps words equal to N (boundary)
  - threshold of 1 produces the same output as no option
  - a word occurring exactly N times is kept
  - ties at the cut-off are ordered alphabetically
  - order of surviving words matches the unfiltered order
  - threshold above every count prints nothing and returns 0
  - empty file with the option prints nothing and returns 0
  - N of 0, a negative N, a non-integer N, and a missing value each exit with code 2, print the usage line on stderr, and print nothing on stdout
  - `--min-count=N` and option-after-file both work
  - repeated option uses the last value
  - help output contains the option
  - a missing input file still fails as it does today

## Out of Scope

- A maximum count option, or a range.
- Filtering by word length, stop words, or a regular expression.
- Changing the word definition (`[a-z']+` after lowercasing).
- Reading from standard input.
- Output formats other than `word count` lines.
- Changes to the test runner or packaging.

If any of these are wanted later, they are new feature requests and should get their own spec.

## Further Notes

Assumptions made because the user was unavailable. Each is stated here so the planner and implementer can see it and the user can overrule it:

1. **Non-integer values are rejected with exit code 2.** The design says N must be a positive integer and that N below 1 is an error. It does not say what happens to `abc` or `2.5`. This spec treats them the same way as an invalid N: usage on stderr, exit code 2.
2. **"Usage message" means the standard argument-parser usage block plus its error line.** The design does not give the exact text. This spec uses the parser's default format, which is the usage line followed by an error line naming the option.
3. **The option may appear before or after the file, and both `--min-count N` and `--min-count=N` are accepted.** This is the argument parser's default; the design did not rule these out.
4. **A repeated option uses the last value.** This is the argument parser's default.
5. **A threshold larger than every count is not an error.** It prints nothing and exits 0.
6. **The threshold applies to the same counts that are printed today.** Counting is case-insensitive and uses the existing word pattern, so "Cat" and "cat" count together before the threshold is applied.
7. **README update is in scope.** The README documents the command line, so the new option is added to its usage section with one example. This is a documentation change, not a behaviour change.
8. **No tracker is configured for this repo** (no `docs/agents/issue-tracker.md`, no `GLOSSARY.md`, no ADRs were found). The spec is published as a local file. No glossary terms were added; "word" and "count" are used as the code and README already use them.
9. **No tickets or plan are produced here.** This change is one slice that one agent can build in one sitting, so the spec goes straight to implementation once the user approves it.

Open decisions: none remain open in this spec. Each choice the user would otherwise have been asked about is recorded above as an assumption, to be revisited only if the user overrules it.
