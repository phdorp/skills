# Min Count Option Spec

Status: ready-for-agent
Source: the approved design in the conversation that produced this spec (`tally --min-count N FILE`). Where that design was silent, the assumptions in Further Notes apply; the author was unavailable to confirm them.

### Problem Statement

Someone who counts word frequencies in a long text gets every word in the output, including the many words that appear once. To see only the words that matter, they must scan or filter the whole list by hand. Even a simple cut-off, such as "only words used at least three times", is not available today.

### Solution

`tally` accepts a `--min-count N` option. With it, the output lists only the words counted at least N times, in the same order as today: most frequent first, ties in alphabetical order. Without the option, the output is unchanged: every word is printed.

### User Stories

1. As a writer, I want to pass `--min-count 3` to tally, so that I see only the words I use three or more times.
2. As a writer, I want to put `--min-count` before or after the file name, so that I can type the option where it reads most naturally.
3. As a writer, I want the filtered list to keep the same order as the unfiltered list, so that I can compare the two outputs directly.
4. As a writer, I want ties at the same count to stay in alphabetical order, so that the output is predictable across runs.
5. As a writer, I want a word whose count equals N to be included, so that "at least N" means what it says.
6. As a writer, I want a word whose count is one below N to be excluded, so that the cut-off is exact.
7. As a user who does not pass the option, I want the output to stay exactly as it is today, so that existing scripts keep working.
8. As a user, I want N = 1 to print every word, so that 1 is the lowest valid value and means "no filtering".
9. As a user whose text has no word that reaches N, I want tally to print nothing and exit successfully, so that "no matches" is not reported as an error.
10. As a user whose text is empty, I want tally to print nothing and exit successfully, so that an empty file behaves as it does today.
11. As a user who passes N below 1 (0, -3), I want tally to print the usage message to stderr and exit with code 2, so that I learn the value is wrong and scripts can detect the failure.
12. As a user who passes a value that is not an integer (`abc`, `2.5`, an empty string), I want tally to print the usage message to stderr and exit with code 2, so that a typo is not silently ignored.
13. As a user who omits the value (`tally --min-count FILE`), I want tally to print the usage message to stderr and exit with code 2, so that the option is never silently misread.
14. As a user who passes a very large N with no word reaching it, I want tally to print nothing and exit successfully, so that large values are valid.
15. As a user who passes `--min-count` twice, I want the last value to win, so that the behaviour follows the standard convention of the argument parser.
16. As a user reading the help text, I want `--min-count N` to be listed with a short description, so that I can discover the option without reading the source.
17. As a user reading the README, I want the usage example to show the option, so that I can learn it from the documentation.
18. As a user, I want the word rules to stay the same (case-insensitive, same word definition), so that the counts shown are the counts I expect.

### Implementation Decisions

- **Module changed:** `tally/cli.py`. The `main(argv)` function gains the option. No other module changes behaviour.
- **Option contract:** `--min-count` takes one required value, `N`. It is parsed as an integer. A value that is not an integer, or is less than 1, is a usage error.
- **Usage error mechanism:** Use the argument parser's own error path (the same path that already handles unknown options and missing file names). That path prints the usage line and an error line to stderr and exits with status 2. Inside the process, `main(argv)` therefore raises `SystemExit` with code 2 rather than returning 2. `python3 -m tally` exits with status 2 as a result.
- **Filter placement:** The filter runs after counting and before ranking. Words with a count below N are dropped. The count comparison is inclusive: a count equal to N is kept.
- **Unchanged:** `count_words` (case folding, word pattern), the ranking rule in `format_counts` (count descending, then word ascending), and the output line format (`word count`).
- **Default:** When the option is absent, no filter is applied, and the output is identical to today's.
- **Interface change:** The command line gains `--min-count N`. The Python signature of `main(argv=None)` is unchanged.
- **Documentation:** The README usage section mentions the option with one example line.

### Testing Decisions

- **What makes a good test:** The observable behaviour of the command: what is printed to stdout, what is printed to stderr, and the exit status. Tests do not inspect internal counters or intermediate lists.
- **Seam:** `main(argv)` in `tally/cli.py`. This is the existing seam, and it is the highest point that can prove the behaviour, since the filter, the ordering, and the error path are all reached through it. No new seam is introduced.
- **Modules tested:** `tally/cli.py`, through `main`. The existing `count_words` and `format_counts` tests stay as they are.
- **Cases to cover through `main`:**
  - the option absent: output identical to today's (existing test covers this; keep it passing)
  - a word with count exactly N is printed; a word with count N-1 is not
  - ties at or above N keep alphabetical order
  - the option placed before and after the file name give the same output
  - no word reaches N: empty stdout, return value 0
  - N = 1: all words printed
  - N = 0, N = -3: `SystemExit` with code 2; usage text on stderr; nothing on stdout
  - N = `abc` and a missing value: `SystemExit` with code 2; usage text on stderr
  - repeated `--min-count`: the last value applies
- **Prior art:** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temp file, calls `main([...])` with `redirect_stdout`, and asserts the output. New tests follow the same pattern and add `redirect_stderr` for the error cases.
- **Test runner:** `python3 -m unittest`, as in the README.

### Out of Scope

- Filtering by a maximum count, or by a range. Only a minimum is in scope.
- Reading from standard input, or accepting several files.
- A short option alias such as `-m`.
- Changing what counts as a word (punctuation, digits, Unicode letters). The current word pattern stays.
- Changing the behaviour for an unreadable or missing file. It stays as it is today.
- Any change to the output format or sort order beyond the filter.

### Further Notes

Assumptions made in place of questions, since the author was unavailable. Each one is a decision the spec has closed; a reviewer can overturn one before the plan is written.

1. **Non-integer values** (`abc`, `2.5`, empty string) are usage errors with exit code 2, the same as N below 1. The design only named N below 1; treating other non-integers differently would be surprising.
2. **Inclusive threshold:** a word is kept when its count is greater than or equal to N.
3. **No upper bound on N.** A value larger than every count prints nothing and exits 0.
4. **Empty result is not an error:** nothing is printed to stdout and the exit status is 0.
5. **Repeated option:** the last occurrence wins, following the argument parser's default behaviour.
6. **Option form:** `--min-count N` and `--min-count=N` are both accepted, following the argument parser's default behaviour. There is no short alias.
7. **Usage error:** the message goes to stderr through the argument parser, and the exit status is 2. Inside the process, `main` raises `SystemExit(2)`.
8. **README:** updating the usage section is part of this change. It is a single example line, not a rewrite.

No questions remain open. Confirming these eight assumptions is the only follow-up needed before the plan is written.
