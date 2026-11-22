# `--min-count` Option Spec

Status: ready-for-agent
Source: conversation, approved design: "`tally --min-count N FILE` prints only the words counted at least N times."

## Problem Statement

`tally` prints every word in a file, so on a long text the output is dominated by words that occur once or twice. A user who wants to see only the recurring words has to filter the output by hand (for example with `awk`), and has to know the output format to do it.

## Solution

A new option, `--min-count N`, limits the output to words whose count is at least N. Everything else stays as it is: the same input, the same `word count` line format, and the same order (most frequent first, ties in alphabetical order). Without the option, every word is printed, as today. An invalid N is rejected with a usage error.

## User Stories

1. As a `tally` user, I want to run `tally FILE` with no new options, so that I get exactly the output I get today.
2. As a `tally` user, I want to pass `--min-count N`, so that only words counted at least N times are printed.
3. As a `tally` user, I want the filtered output to keep the same order as the unfiltered output (most frequent first, ties in alphabetical order), so that I can read it the same way.
4. As a `tally` user, I want `--min-count 1` to print the same output as no option, so that 1 is a safe lower bound.
5. As a `tally` user, I want a threshold above the highest count in the file to print nothing and exit successfully, so that "no word qualifies" is not treated as a failure.
6. As a `tally` user, I want a threshold equal to a word's count to include that word, so that "at least N" means `>= N`, not `> N`.
7. As a `tally` user, I want the threshold to apply to case-folded counts, so that `The` and `the` are counted together before the threshold is checked, the same as the counting already does.
8. As a `tally` user, I want `--min-count` to work whether it comes before or after the file name, so that I can write the command in either order.
9. As a `tally` user, I want `--min-count=N` to work as well as `--min-count N`, so that I can use either form standard argument parsers accept.
10. As a `tally` user, I want `--min-count 0` to be rejected with a usage message on stderr and exit code 2, so that I learn the option needs a positive number.
11. As a `tally` user, I want a negative N (for example `--min-count -1`) to be rejected with the same usage error and exit code 2, so that negative thresholds do not silently print everything.
12. As a `tally` user, I want a non-integer N (for example `abc`, `2.5`, or an empty string) to be rejected with the same usage error and exit code 2, so that a typo does not silently change the output.
13. As a `tally` user, I want `--min-count` with no value to be rejected with the usage error and exit code 2, so that a forgotten number is caught.
14. As a `tally` user, I want the usage error to go to stderr and leave stdout empty, so that a pipeline does not receive error text as data.
15. As a `tally` user, I want an invalid N to be rejected before the file is read, so that the usage error is the reported problem even when the file is also missing.
16. As a `tally` user, I want a very large valid N (for example `1000000000`) to be accepted and print nothing, so that large inputs do not need special handling.
17. As a `tally` user, I want `tally --help` to show the new option with a one-line description, so that I can discover it.
18. As a `tally` user reading the README, I want the option documented with one example, so that I can use it without reading the code.
19. As a `tally` user, I want the file-not-found behaviour to stay unchanged by this feature, so that this change does not alter existing error handling.

## Implementation Decisions

- **Module changed: `tally.cli`.** It gains one command-line option and a threshold filter. No other module changes.
- **Threshold filter.** The filter is applied to the counts after counting and before ranking. It keeps a word when its count is greater than or equal to N. Ranking (count descending, then word ascending) is unchanged, so the filtered output is exactly the unfiltered output with the low-count lines removed.
- **Filter location.** The filter lives in the same step that formats counts for output, as an optional parameter that defaults to "no threshold". Existing callers keep their current behaviour without changes. (Decision recorded here; the plan does not revisit it.)
- **Option type.** `--min-count` takes one value. The value is parsed as an integer in base 10 using Python's `int()`. Values `int()` accepts are valid if they are at least 1 (for example `+3`, `03`, and `1_000` are valid, meaning 3, 3, and 1000). Values `int()` rejects are invalid (for example `abc`, `2.5`, empty string). Invalid values are rejected by the standard argument parser, which prints the usage line and an error line to stderr and exits with code 2. A value of 0 or below is rejected by the same mechanism, with a message naming the option.
- **Default.** When the option is absent, no threshold is applied and every word is printed.
- **Exit codes.** Success exits 0, including when nothing meets the threshold. Invalid N exits 2. Other behaviour (such as a missing file) is unchanged.
- **Ordering of checks.** The option value is validated during argument parsing, before the file is opened.
- **Output.** Only the `word count` lines that pass the threshold are printed to stdout, one per line, in the existing order. Nothing else is printed to stdout.
- **Interfaces.** `main(argv)` keeps its signature and return value (0 on success). The option is accepted wherever argparse accepts options, including `--min-count=N`.
- **Help text.** The option appears in `--help` with a short description saying it keeps words counted at least N times.
- **README.** The README gains one line describing the option and one example invocation, alongside the existing usage line.

## Testing Decisions

- **What makes a good test.** Tests check external behaviour through `main(argv)`: the lines written to stdout, the text written to stderr, and the return value or the exit code raised by the parser. Tests do not check internal data structures or call the filter with private helpers.
- **Seam.** One seam: `tally.cli.main(argv)`. It already exists and is the seam the current tests use, so no new seam is introduced. The threshold filter is exercised through `main`, which is the highest seam that can prove the behaviour.
- **Modules tested.** `tally.cli` only.
- **Cases the tests must cover.**
  - No option: output identical to today's output for a fixed input file.
  - `--min-count 2` on a fixed input: only words with count 2 or more appear, in the existing order.
  - Threshold equal to a word's count includes that word.
  - Threshold above the maximum count: empty stdout, return 0.
  - `--min-count 1`: same output as no option.
  - Case folding: `The` and `the` add up before the threshold is checked.
  - Option before and after the file name, and the `--min-count=N` form.
  - `0`, `-1`, `abc`, `2.5`, and a missing value: `SystemExit` with code 2, usage text on stderr, nothing on stdout.
  - Invalid N with a missing file: usage error reported, file not opened.
- **Prior art.** `tests/test_cli.py`. It uses `tempfile` for input files, `redirect_stdout` to capture output, and `main([...])` as the entry point. New tests follow the same pattern and add `redirect_stderr` for the error cases.
- **Run command.** `python3 -m unittest`, as in the README.

## Out of Scope

- Filtering by maximum count, or by a count range. Only a minimum is in scope.
- Changing how words are tokenised or how case is folded.
- Changing the output format, the sort order, or the default output.
- Changing error handling for missing or unreadable files.
- Reading from stdin or multiple input files.
- Any new tracker, ticket, or plan artifact. This is one slice, one sitting, one agent, so the spec goes straight to implementation.

## Further Notes

These points are assumptions. The author was not available to answer them, so each was decided here. Reviewers should confirm or overturn them before implementation.

1. **Non-integer values are errors.** Values that `int()` rejects (`abc`, `2.5`, `""`) are usage errors with exit code 2. Values `int()` accepts but a human might not expect (`+3`, `03`, `1_000`) are accepted as their integer value.
2. **Usage message content.** "The usage message on stderr" is taken to mean the standard argument-parser output: the usage line followed by an error line naming `--min-count`. The exact wording of the error line is not pinned by this spec.
3. **Option position.** The option is accepted before or after the file argument, and in `--min-count=N` form, because that is the standard parser behaviour and no restriction was asked for.
4. **Validation before file access.** An invalid N is reported before the file is opened, so the usage error wins over a file error.
5. **Negative numbers.** A negative value such as `-1` reaches the integer check as a value and is rejected there. It is not treated as an unknown option.
6. **README.** The README update is included because the README is the only user documentation and it documents the output contract.
