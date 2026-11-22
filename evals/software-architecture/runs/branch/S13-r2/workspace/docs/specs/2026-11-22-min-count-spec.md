# `--min-count` Option Spec

Status: ready-for-agent
Source: Conversation with the architect. Approved design: "`tally --min-count N FILE` prints only the words counted at least N times; N is a positive integer; without the option every word is printed, as today; order unchanged; N below 1 is an error: usage message on stderr, exit code 2." The architect was unavailable for the open questions; their answers are stated as assumptions in Further Notes.

## Problem Statement

Someone counting words in a text file gets one line per distinct word, and in a long file most of those lines are words that appear once or twice. To find the words that actually recur, they must scroll or pipe the output through another tool to filter it. The frequent words are what they came for, and the rare ones are noise.

## Solution

`tally` gains an option, `--min-count N`. When it is given, the output lists only the words that occur at least N times in the file. Everything else about the output stays as it is today: one `word count` line per word, most frequent first, ties in alphabetical order. Without the option, the output is unchanged.

## User Stories

1. As a user of `tally`, I want to pass `--min-count 3` with a file, so that only the words appearing at least three times are printed.
2. As a user, I want a word that appears exactly N times to be printed, so that the threshold is inclusive and "at least N" means what it says.
3. As a user, I want a word that appears fewer than N times to be left out, so that the rare words do not clutter the result.
4. As a user, I want the remaining words to keep the usual order (most frequent first), so that the filtered output reads the same way as the unfiltered output.
5. As a user, I want ties at the same count to stay in alphabetical order, so that the output is predictable when several words share a count.
6. As a user, I want to run `tally` with no `--min-count` option exactly as before, so that existing scripts keep working.
7. As a user, I want `--min-count 1` to print the same output as no option at all, so that 1 is the no-op threshold: every word occurs at least once.
8. As a user, I want N larger than the count of every word to print nothing and exit successfully, so that "no word qualifies" is a normal result and not an error.
9. As a user, I want N = 0 to be rejected with the usage message on stderr and exit code 2, so that I learn the value is invalid and do not get silently unfiltered output.
10. As a user, I want a negative N to be rejected the same way as 0, so that every value below 1 gets one consistent answer.
11. As a user, I want a non-integer N (for example `abc` or `2.5`) to be rejected with the usage message and exit code 2, so that a typo is not silently accepted.
12. As a user, I want to write the option before or after the file name, and in either `--min-count 3` or `--min-count=3` form, so that the option behaves like other command-line options.
13. As a user, I want a rejected N to produce no words on stdout, so that a script never consumes partial or unfiltered output from a bad invocation.
14. As a user, I want a missing or unreadable file to fail as it does today, so that the new option does not change file errors.
15. As a user, I want an empty file, or a file with no words, to print nothing and exit successfully, with or without `--min-count`, so that empty input behaves as it does today.
16. As a user, I want the counting rules (case-insensitive, letters and apostrophes) to be unchanged by the option, so that a word counts the same whether or not I filter.
17. As a user reading the usage text, I want the `--min-count` option to appear in the help output with a short description, so that I can discover it without reading the source.

## Implementation Decisions

- **Interface change:** the command gains one optional option, `--min-count`, taking one value N. Nothing else in the command-line interface changes. The option name and the value placeholder are fixed by this spec.
- **Filtering rule:** after words are counted, a word is kept when its count is greater than or equal to N. Words below N are dropped. Filtering happens before the output is formatted, so the ranking and tie-break rules are applied to the kept words only and are not changed.
- **Output format:** unchanged. Each kept word is printed as `word count`, one per line, in the existing order.
- **Validation:** N must be a whole number of 1 or more. Any other value is a usage error: 0, negative numbers, and non-integers are all rejected by argument parsing, before the input file is opened. A usage error writes the usage message and the reason to stderr, writes nothing to stdout, and ends with exit code 2. Validation is done by the existing argument parser, which the project already uses, so the usage message follows the project's current style.
- **Exit codes:** a valid run that finds no qualifying words is not an error: it prints nothing and exits 0. A usage error exits 2. A missing or unreadable file keeps its current behaviour.
- **Counting:** the way words are found (lowercase, letters and apostrophes) does not change.
- **Documentation:** the command's help text describes the option. The README's usage section gains one example line showing the option.

## Testing Decisions

- **What makes a good test here:** the tests describe what a user sees: the printed lines, their order, and the exit code. They do not check internal data structures or how the filter is implemented.
- **Seam:** the existing entry point `main(argv)` in the CLI module. It is the highest existing seam and already has tests (the `Main` test class in `tests/test_cli.py`). Tests pass an argument list, capture stdout, and check the return value. For usage errors, the argument parser ends the call with `SystemExit`, so those tests assert that the exit code is 2 and read the message from stderr. The filter can also be tested through the existing `format_counts` / `count_words` tests, if the implementation keeps them as separate steps.
- **No new seam is proposed.** The option is a thin layer over an existing function, and `main(argv)` proves the behaviour end to end.
- **Behaviours to test through `main(argv)`:**
  - the threshold is inclusive (a word at exactly N is printed; N-1 is not);
  - kept words keep the most-frequent-first order and the alphabetical tie order;
  - N = 1 prints the same output as no option;
  - N above every count prints nothing and returns 0;
  - N = 0, a negative N, and a non-integer N each end with exit code 2, print nothing to stdout, and write the usage message to stderr;
  - the option works after the file name and in the `--min-count=N` form;
  - no option gives the same output as the current test `test_prints_every_word`, which must keep passing unchanged.
- **Prior art:** `tests/test_cli.py`, class `Main`, test `test_prints_every_word`, shows how to write a temp file, call `main`, and capture stdout. `CountWords.test_ranks_by_count_then_alphabetically` shows how ranking is tested.
- **Run with:** `python3 -m unittest`, as the README says.

## Quality Requirements

Not applicable. The project has no `docs/architecture/arc42.md`, so there are no R-, QS-, or ADR IDs to cite.

## Out of Scope

- A maximum count (`--max-count`) or a range of counts.
- Filtering by word pattern, length, or stop-word list.
- Changing how words are found or how case is handled.
- Changing the output format (for example, JSON or tab-separated output).
- Any change to how a missing or unreadable file is reported.
- Reading from stdin or accepting several files.

## Further Notes

The architect was unavailable to answer the open points. The following assumptions are made in their place and should be checked when they are next available. None of them contradicts the approved design; each one fills a gap the design does not cover.

- **A1, non-integer values:** the design covers N below 1 but not non-integer input. This spec treats any non-integer (`abc`, `2.5`, empty string) as a usage error with exit code 2, the same as N below 1.
- **A2, inclusive threshold:** "counted at least N times" is read as count >= N. A word that appears exactly N times is printed.
- **A3, no matches:** when no word reaches N, the output is empty and the exit code is 0. This is not treated as an error.
- **A4, order of checks:** a usage error from the option is reported before the file is opened. A bad N with a missing file therefore reports the usage error.
- **A5, seam:** the only test seam is the existing `main(argv)` entry point, as described in Testing Decisions. The architect was not asked to confirm this.
- **A6, documentation:** the README usage section and the command's help text are updated as part of this work. The design did not mention documentation.
- **A7, vocabulary:** the project has no `GLOSSARY.md` and no ADRs, so no terms were added or checked against one.
- **A8, option form:** both `--min-count N` and `--min-count=N` are accepted, because the standard argument parser accepts both.

If the architect rejects any of these, the spec should be updated before tickets or a plan are written.
