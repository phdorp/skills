# Min-Count Option Spec

Status: ready-for-agent
Source: conversation with the maintainer, which approved this design: `tally --min-count N FILE` prints only the words counted at least N times; N is a positive integer; without the option every word is printed as today; order unchanged (most frequent first, ties alphabetical); N below 1 is an error with the usage message on stderr and exit code 2.

### Problem Statement

When a text file is large, `tally` prints one line for every distinct word, including the many words that appear only once. The person reading the output has to scroll past or filter out those singletons by hand to see the words that actually recur. They want to ask for only the words that occur at least a given number of times.

### Solution

`tally` accepts a `--min-count N` option. When it is given, the output lists only the words that were counted at least N times, in the same order and format as today. When it is not given, the output is exactly what `tally` prints today.

### User Stories

1. As a writer reviewing a long draft, I want to run `tally --min-count 5 draft.txt`, so that I see only the words I repeat often and can spot overused vocabulary quickly.
2. As a writer, I want the output order to stay the same as without the option (most frequent first, ties alphabetical), so that I can compare filtered and unfiltered runs without relearning the layout.
3. As a writer, I want the output format to stay `word count` per line, so that scripts that already parse `tally` output keep working when they add the option.
4. As a user who runs `tally FILE` today, I want the output to be unchanged when I do not pass `--min-count`, so that my existing workflows are not affected.
5. As a user, I want `--min-count 1` to print the same output as no option at all, so that 1 is a safe lower bound that does not hide anything.
6. As a user, I want a count threshold equal to a word's count to include that word (the comparison is "at least N"), so that `--min-count 3` shows a word that appears exactly three times.
7. As a user, I want `--min-count` to be accepted before or after the file name, so that I can type the option in whichever position I remember.
8. As a user, I want `--min-count=N` (the single-argument form) to work the same as `--min-count N`, so that the option matches the convention of other command-line tools.
9. As a user, I want `--min-count 0` to fail with the usage message on stderr and exit code 2, so that a mistaken threshold is reported instead of silently printing everything.
10. As a user, I want a negative value (for example `--min-count -3`) to fail with the same usage error and exit code 2, so that every value below 1 is treated the same way.
11. As a user, I want a value that is not an integer (for example `abc` or `2.5`) to fail with the usage error and exit code 2, so that the option never accepts a threshold it cannot apply.
12. As a user, I want a usage error to print nothing on stdout and to leave the file unread, so that a failed run produces no partial output.
13. As a user, I want a threshold larger than every word's count (for example `--min-count 1000` on a short file) to print nothing and exit with code 0, so that an empty result is not reported as a failure.
14. As a user, I want an empty input file to print nothing with or without the option and exit with code 0, so that the empty case behaves as it does today.
15. As a user, I want a very large threshold to be accepted without special handling, so that I do not need to know the size of my file in advance.
16. As a user, I want a missing or unreadable file to fail exactly as it does today when `--min-count` is given, so that the new option does not change file-error behaviour.
17. As a user, I want `--help` to list the new option with a short description, so that I can discover it without reading this spec.

### Implementation Decisions

- **Counting is unchanged.** Words are counted exactly as today: case-insensitive, same word pattern, same counting step. The threshold is applied to the finished counts, not during counting.
- **Filter.** A word is kept when its count is greater than or equal to N. The filter runs after counting and before output. Without the option, no filter is applied, which is equivalent to N = 1.
- **Ordering and format.** Kept words are ordered by the existing rule (count descending, then word ascending) and printed in the existing `word count` format, one per line.
- **Option.** One long option, `--min-count`, takes one value. It is optional and its default is "no threshold". Its value is parsed as an integer and must be at least 1. Any other value (below 1, non-integer, missing value) is a usage error.
- **Usage error.** A usage error prints the standard argument-parser usage line and an error message on stderr, and exits with code 2. Nothing is written to stdout, and the input file is not opened. This is the behaviour the platform's argument parser already produces for invalid option values, so the implementation should rely on it rather than hand-write the message. Assumption: the "usage message" in the approved design means that standard usage line plus the error line.
- **Exit codes.** Successful runs exit with 0, including runs that print nothing because no word meets the threshold. Usage errors exit with 2. File errors keep their current behaviour.
- **Public interface.** The command-line interface gains `--min-count`. The `main` entry point keeps its existing signature and return behaviour; the option is added to the arguments it already parses. No other module's public behaviour changes.
- **No new dependencies.** The option uses the argument parsing and counting already in the project.

### Testing Decisions

- **What makes a good test.** Tests assert external behaviour through the command-line entry point: the output lines, their order, the exit code, what is written to stdout and stderr, and whether an error occurs. Tests do not assert on internal helper calls or on how the filter is structured.
- **Seam.** The `main(argv)` function in the CLI module is the seam. It is the highest existing seam that can prove every behaviour in this spec, including the usage error and exit code, so no new seam is needed. Assumption: no seam change is needed; the maintainer was not asked to confirm this.
- **Modules tested.** The CLI module only. Counting and formatting helpers are already covered by unit tests and are not changed in behaviour, so they need no new tests unless the implementation changes them.
- **Cases to cover through `main`:**
  - without the option, output is identical to the current output for a file with several words of different counts (regression);
  - `--min-count 2` keeps exactly the words with count 2 or more, with the same order as without the option;
  - a word whose count equals N is included;
  - `--min-count 1` gives the same output as no option;
  - `--min-count` before and after the file argument both work, and `--min-count=N` works;
  - a threshold above every count prints nothing and returns 0;
  - an empty file prints nothing and returns 0 with and without the option;
  - `0`, a negative value, and a non-integer each raise a system exit with code 2, print nothing to stdout, and print a usage line and an error message to stderr;
  - a missing file with the option behaves as it does without the option.
- **Prior art.** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`: it calls `main` with a temporary file, captures stdout with `redirect_stdout`, and checks the return code and output. New tests follow the same pattern and add `redirect_stderr` and an assertion on the raised `SystemExit` code for the error cases.
- **Test runner.** Tests run with `python3 -m unittest`, as the README states.

### Out of Scope

- Other filters, such as a maximum count, a top-N limit, or a minimum word length. These are not part of this design.
- Changes to what counts as a word, to case handling, or to the sort order.
- Changes to output format, for example CSV or JSON output.
- Changes to how missing or unreadable files are reported.
- A short option letter for `--min-count`.
- Documentation beyond the `--help` text and the existing README line. Updating the README's description of the output is left to the implementer as a single line if the maintainer wants it; this spec does not require it.

### Further Notes

Assumptions made because the maintainer was not available to answer. Each is recorded here so the planner and implementer can check them:

1. **Non-integer values are usage errors.** `abc`, `2.5`, and an empty string are rejected like values below 1, with exit code 2. The approved design only named values below 1; this extends it to all invalid integers.
2. **Inclusive threshold.** "Counted at least N times" is read as `count >= N`.
3. **Threshold above all counts.** The output is empty and the exit code is 0. It is not treated as an error.
4. **Usage error output.** Stdout is empty. Stderr has the standard usage line and the error line produced by the argument parser. The input file is not opened.
5. **Option position and syntax.** Both `--min-count N` and `--min-count=N` are accepted, before or after the file name. This is the argument parser's default behaviour.
6. **No upper bound.** Any positive integer is accepted. There is no maximum value.
7. **Default is no filter.** Omitting the option is the same as `--min-count 1`, so the existing output is preserved exactly.
8. **Seam.** The existing `main(argv)` entry point is the test seam. No new seam is introduced.

No decision in this spec is deferred. The open items above are assumptions for the maintainer to confirm or change after the fact; any change to them is a change to this spec, not a new design round.
