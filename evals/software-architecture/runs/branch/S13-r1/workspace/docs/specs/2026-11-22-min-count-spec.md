# Minimum Count Option Spec

Status: ready-for-agent
Source: approved design in the conversation that produced this spec (`tally --min-count N FILE`). The user was unavailable for questions; every gap is resolved under Further Notes as a stated assumption.

## Problem Statement

`tally` prints every word in a text file, most frequent first. For a long file, the output is mostly words that appear once or twice, and the words that matter are buried among them. A person who wants to see only the recurring words has to scroll or pipe the output through another tool to filter it.

## Solution

`tally` accepts a `--min-count N` option. When it is given, `tally` prints only the words that occur at least N times in the file. Each printed line keeps its current form (`word count`), and the order does not change: most frequent first, ties in alphabetical order. Without the option, `tally` prints every word, as it does today.

## User Stories

1. As a person analysing a text file, I want to pass `--min-count N` to see only words counted at least N times, so that the recurring words stand out.
2. As a person analysing a text file, I want a word counted exactly N times to be printed, so that the threshold is inclusive and I do not lose words sitting on the boundary.
3. As a person analysing a text file, I want the printed words to keep the current order (most frequent first, ties alphabetical), so that filtered output reads the same way as unfiltered output.
4. As a person analysing a text file, I want `--min-count 1` to print the same output as running without the option, so that 1 is a neutral threshold.
5. As a person analysing a text file, I want to run `tally` without `--min-count` exactly as before, so that existing scripts and habits keep working.
6. As a person analysing a text file, I want `--min-count` to print nothing and exit successfully when no word reaches N, so that an empty result is distinguishable from an error.
7. As a person analysing an empty file, I want `--min-count N` to print nothing and exit successfully, so that an empty file behaves the same with or without the option.
8. As a person who mistypes the threshold, I want `--min-count 0` to be rejected with the usage message on stderr and exit code 2, so that I learn the input was wrong instead of getting silently empty or unfiltered output.
9. As a person who mistypes the threshold, I want a negative `--min-count` to be rejected with the usage message on stderr and exit code 2, so that a nonsensical threshold is never applied.
10. As a person who mistypes the threshold, I want a non-integer `--min-count` value (for example `abc` or `1.5`) to be rejected with the usage message on stderr and exit code 2, so that the option never has a meaning I did not intend.
11. As a person who forgets the value, I want `--min-count` given with no value to be rejected with the usage message on stderr and exit code 2, so that the option is never silently ignored.
12. As a person who writes the option before or after the file name, I want both `tally --min-count 2 FILE` and `tally FILE --min-count 2` to work, so that I do not have to remember an order.
13. As a person reading the help, I want `tally --help` to list `--min-count` with a short description, so that I can discover the option without reading the README.
14. As a person reading the README, I want a usage example of `--min-count`, so that the new option is documented where the existing usage is.

## Implementation Decisions

- **Module changed:** the command-line module (`tally/cli.py`). The counting step and the ordering step are not changed. The threshold filter is applied to the counts after counting and before the existing ordering and formatting.
- **Interface changed:** the command-line interface gains one option, `--min-count`, which takes one value. The value is parsed as an integer by the same argument parser that already parses the file argument. The file argument stays required and positional.
- **Parameter contract:** the public function `main(argv)` keeps its signature and its return value (`0` on success). It handles the new option and returns `0` after printing the filtered words.
- **Validation:** a value that is not an integer is rejected by the integer conversion. A value below 1 is not rejected by the conversion alone (it accepts `0` and negative numbers), so it needs an explicit check. Both failures go through the argument parser's usage-error path, which prints the usage message and an error line to stderr and exits with code 2. No other error path is added for this option.
- **Threshold rule:** a word is printed when its count is greater than or equal to N. Words below N are dropped before ordering.
- **Unchanged behaviour:** word splitting (letters and apostrophes, case-insensitive), the output line format, the sort order, and the exit code of a successful run.
- **Schema, API, and dependencies:** none. No new dependencies.
- **README:** the README's usage section gains one example that shows `--min-count`.

## Testing Decisions

- **What makes a good test:** these tests check what the command prints and what exit code it returns, given an argument list and a file. They do not check how the filter is written internally.
- **Seam:** the existing `main(argv)` entry point in `tally/cli.py`. It already takes an argument list, writes to stdout, and returns the exit code, so no new seam is introduced. Usage errors leave the function by raising `SystemExit`, so tests check the exit code of that exception.
- **Module tested:** `tally/cli.py`, through `main`. The existing `format_counts` and `count_words` tests keep covering ordering and counting; they are not changed.
- **Test cases to cover:**
  - threshold keeps words at exactly N and drops words below N (stories 1, 2)
  - order of the kept words matches the unfiltered order (story 3)
  - `--min-count 1` output equals the output without the option (story 4)
  - no option prints every word, as the existing test does (story 5)
  - a threshold above every count prints nothing and returns `0` (story 6)
  - an empty file with the option prints nothing and returns `0` (story 7)
  - `0`, a negative value, a non-integer value, and a missing value each raise `SystemExit` with code `2`, and the usage text appears on stderr (stories 8 to 11)
  - the option works before and after the file argument (story 12)
- **Prior art:** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temporary file, captures stdout with `redirect_stdout`, and asserts the output and the return value. The new tests follow that pattern. For the error cases, capture stderr in the same way with `redirect_stderr`.
- **Run command:** `python3 -m unittest`, as the README states.

## Out of Scope

- A maximum count option or a range option.
- Filtering by word length or by a word list.
- Changing what counts as a word.
- Changing how a missing or unreadable file is reported. That behaviour stays as it is today.
- Any change to the output format, such as a header line or totals.

## Further Notes

Assumptions made in place of questions to the user. Each one can be changed later by editing this spec.

1. **Non-integer values are rejected the same way as values below 1.** The design named only `N < 1`. Using an integer parser for the option makes `abc` and `1.5` fail with the same usage error and exit code 2. This is the assumption most likely to differ from what the user wants.
2. **Integer parsing is the parser's default.** Values such as `+3` and `03` are accepted, because that is what the integer conversion accepts. Values with a decimal point or an exponent are rejected (see assumption 1).
3. **The threshold is inclusive.** A word counted exactly N times is printed.
4. **No matching word is not an error.** When no word reaches N, the command prints nothing and returns exit code `0`.
5. **Repeating the option uses the last value**, which is the parser's default when an option is given twice.
6. **Error wording is not pinned.** The spec requires the usage message on stderr and exit code 2. The exact text of the error line is whatever the argument parser prints.
7. **The option name is `--min-count` only.** No short form is added.

No decision in this spec is left open for later.
