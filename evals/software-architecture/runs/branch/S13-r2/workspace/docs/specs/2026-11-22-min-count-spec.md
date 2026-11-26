# `--min-count` Option Spec

Status: ready-for-agent
Source: Approved design from the conversation: `tally --min-count N FILE` prints only the words counted at least N times.

## Problem Statement

`tally` prints every word in a file with its count. On a long text, most of the output is words that appear once or twice, and the words that matter (the frequent ones) are buried among them. A user who wants only the recurring vocabulary has to filter the output by hand.

## Solution

A user can pass `--min-count N` to print only the words that occur at least N times. Everything else stays as it is today: the same counting, the same ordering (most frequent first, ties in alphabetical order), and the same output format (`word count`, one per line). Without the option, every word is printed.

## User Stories

1. As a writer, I want to pass `--min-count N` to `tally`, so that I see only the words I used at least N times.
2. As a writer, I want the filtered output to keep the most-frequent-first order, so that I can read the top of the list first.
3. As a writer, I want ties broken alphabetically within the filtered output, so that the list is stable across runs.
4. As a writer, I want a word counted exactly N times to be included, so that `--min-count 3` means "three or more".
5. As a user, I want to run `tally` without the option and get every word, exactly as before, so that existing scripts keep working.
6. As a user, I want to place `--min-count` before or after the file name, so that I can write the command either way.
7. As a user, I want `--min-count` to accept a large N with no upper limit, so that I can ask for only the very frequent words.
8. As a user, I want a value of N that no word reaches to print nothing and exit successfully, so that "no matches" is not reported as a failure.
9. As a user, I want N of 0 to be rejected, so that I am told the option needs a positive number.
10. As a user, I want a negative N to be rejected, so that a typo does not silently print everything.
11. As a user, I want a non-integer N (for example `abc`, `2.5`, or an empty string) to be rejected, so that I am told the value must be a whole number.
12. As a user, I want a rejected N to print the usage message to stderr and exit with status 2, so that I can recognise a usage error the way I recognise other argument errors.
13. As a user, I want a rejected N to print nothing to stdout, so that a script does not mistake an error for an empty result.
14. As a user, I want the `--help` output to describe `--min-count` with its N value, so that I can discover the option.
15. As a user, I want the README to show how to use `--min-count`, so that the option is documented next to the basic usage.
16. As a user, I want a missing input file to behave as it does today, so that this change does not alter unrelated errors.

## Implementation Decisions

- **Option**: a single long option `--min-count` taking one integer value, shown in help with the metavar `N`. No short form.
- **Validation**: the value must be an integer and at least 1. Non-integers and values below 1 are rejected through the same argument-error path the command already uses for bad arguments. That path prints the usage line and an error message to stderr and exits with status 2. Nothing is printed to stdout in this case.
- **Filtering**: after counting and before formatting, keep only words whose count is greater than or equal to N. Filtering does not change counts.
- **Ordering**: unchanged. The existing ranking (descending count, then ascending word) applies to the filtered words.
- **Output format**: unchanged (`word count`, one line per word).
- **No matches**: when no word meets the threshold, nothing is printed and the exit status is 0.
- **Default**: when the option is absent, behaviour is identical to today.
- **Interfaces that change**: the command-line interface gains the option. The public counting and formatting functions keep their current behaviour when called without a threshold.
- **Documentation**: the README usage section shows the option with one example.

## Testing Decisions

What makes a good test here: the command's observable behaviour (stdout, stderr, exit status) for a given input file and argument list. Tests should not check how filtering is implemented.

Seam: the existing `main(argv)` entry point. It already accepts an argument list and a file path, and the current tests drive it and capture stdout. The new tests use the same seam. No new seam is needed. The existing `format_counts` seam is not used for these tests because the option lives in the command-line layer.

Behaviours to test through `main`:

- With `--min-count 2`, a file with words counted 3, 2, and 1 times prints only the 3 and the 2, in that order.
- A word counted exactly N times is included (boundary).
- Ties among retained words are alphabetical.
- With the option placed after the file name, the output is the same.
- Without the option, output is unchanged (the existing `test_prints_every_word` covers this; keep it passing).
- When no word reaches N, stdout is empty and the return value is 0.
- N = 0, N = -1, N = `abc`, and N = `2.5` each: stdout is empty, stderr contains the usage line, and the exit status is 2. Because the argument error path raises `SystemExit` with code 2 inside `main`, the test asserts that exception's code and the stderr text.

Prior art: `tests/test_cli.py`, class `Main`, with its use of `redirect_stdout` and temporary files. Extend that class, or add a sibling class in the same file.

## Out of Scope

- Changing the counting rules (what counts as a word, case handling).
- Changing the ordering rules.
- A maximum value for N or a separate upper-bound check.
- Other filters (maximum count, word length, stop words).
- Changing how a missing or unreadable input file is reported.
- Multiple input files.

## Further Notes

The approved design was given without follow-up questions, and the user was unavailable to answer the questions below. Each point is an assumption made by the spec author, recommended as stated. The user should confirm them before implementation; if the user changes one, update this spec first.

1. **Integer syntax.** Values are parsed by the standard integer conversion used for command-line arguments. Values such as `+3` or ` 3` are accepted as the integer they denote. Values such as `2.5`, `1e3`, or an empty string are rejected. Recommended: as stated.
2. **Threshold comparison.** The threshold is inclusive: a word is kept when its count is at least N. This follows the design's "counted at least N times". Recommended: as stated.
3. **Argument position.** The option may appear before or after the file argument, as usual for this kind of command-line parser. Recommended: as stated.
4. **Repeated option.** If `--min-count` appears more than once, the last value is used. This is the default behaviour of the argument parser. The alternative would be to reject repeats; recommended: last value wins, to keep the change small.
5. **No matches.** An empty result is a success (exit status 0) and prints nothing. The design does not specify this; treating it as an error would make `tally --min-count 1000 FILE` fail in scripts for a valid query. Recommended: as stated.
6. **Usage message.** "The usage message on stderr" is taken to mean the standard usage line followed by the error message, as the argument parser prints it. Recommended: as stated.
7. **Help text and README.** The option appears in `--help`, and the README gains one example. These are small documentation changes that go with the feature. Recommended: as stated.

Open decisions: none remain in the published spec beyond the assumptions above, which the user has not yet confirmed.
