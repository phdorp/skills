# `--min-count` Spec

Status: ready-for-agent
Source: approved design in the conversation of 2026-11-22 (`tally --min-count N FILE` prints only the words counted at least N times). The user was unavailable during spec writing; every point where a question would have been asked is stated as an assumption in Further Notes.

### Problem Statement

`tally` prints every word in a text file. On a long text most of the output is rare words, so a user who wants the frequent words has to scan past the whole list to find them.

### Solution

`tally` accepts a `--min-count N` option. When given, it prints only the words that occur at least N times in the file. Each printed line keeps today's format (`word count`), and the order stays most frequent first, ties in alphabetical order. Without the option, every word is printed, as today. N must be a positive integer; anything below 1 is a usage error.

### User Stories

1. As a writer reviewing a draft, I want to run `tally --min-count 3 draft.txt`, so that I see only the words I used three or more times.
2. As a writer, I want a word used exactly N times to be included, so that the threshold is "at least N", not "more than N".
3. As a writer, I want the kept words in the same order as the full output (most frequent first, ties alphabetical), so that I can read the two outputs side by side.
4. As a user who runs `tally FILE` without the option, I want the output to be unchanged, so that existing scripts keep working.
5. As a user who passes `--min-count 1`, I want the same output as when I omit the option, so that 1 is a no-op threshold.
6. As a user whose N is larger than every word's count, I want no output and exit code 0, so that "nothing matched" is not treated as an error.
7. As a user who passes `--min-count 0`, I want a usage message on stderr and exit code 2, with nothing printed to stdout, so that I learn the value is invalid.
8. As a user who passes a negative N, I want the same usage error as for 0.
9. As a user who passes a non-integer N (`abc`, `1.5`) or omits the value, I want a usage error with exit code 2.
10. As a user who types the option after the file name (`tally FILE --min-count 3`), I want it to work the same as before the file name.
11. As a user whose N is invalid and whose file does not exist, I want the usage error, so that I learn about the option before the file is opened.
12. As a user of an empty file with `--min-count 2`, I want no output and exit code 0.
13. As a user who runs `tally --help`, I want the option listed with a short description, so that I can discover it.
14. As a user who passes a valid N and a file that does not exist, I want the same error as today, so that this change does not alter existing failure behaviour.

### Implementation Decisions

- **Interface change**: one new long-form option, `--min-count`, with an integer value. No short form. The value is required when the option is given.
- **Validation at parse time**: values below 1 are rejected by the argument parser, so the error takes the same path as any other usage error: usage text and error line on stderr, exit code 2. Validation runs before the input file is opened.
- **Filtering**: the filter is applied to the word counts after counting and before formatting. It compares each word's total occurrences in the file against N and keeps words where the total is at least N. Ordering and output format are unchanged, so the ranking rule stays in one place.
- **Counting is unchanged**: words are still case-insensitive, and N is compared against the total number of occurrences, not the number of distinct words.
- **Entry point**: `main(argv)` keeps its signature and its return value (0 on success). `count_words` and `format_counts` keep their current behaviour; the filter may be applied inside `main` or in a helper, which is the implementer's choice.
- **Documentation**: the README's usage section gains the option, one line.

### Testing Decisions

- **Seam**: `main(argv)` in `tally/cli.py`. It is the highest existing seam and already covers the CLI contract. Tests pass an argument list, capture stdout and stderr, and check the return value or `SystemExit` code. No new seam is needed.
- **Module under test**: `tally/cli.py`, through `main` only. Do not assert on internal helper names.
- **What makes a good test here**: each test runs one command line against a temporary file and checks what a user would see: printed lines, stderr content, and exit code.
- **Prior art**: `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temp file, calls `main([...])` inside `redirect_stdout`, and checks the output string. New tests follow that pattern and add stderr capture with `redirect_stderr`.
- **Required tests** (new cases in `tests/test_cli.py`):
  - threshold keeps words with count >= N, and drops the rest
  - a word with count exactly N is kept
  - kept words keep the most-frequent-first, alphabetical-tie order
  - N = 1 produces the same output as omitting the option
  - N above every count prints nothing and returns 0
  - N = 0, a negative N, and a non-integer N each raise `SystemExit` with code 2, print usage to stderr, and print nothing to stdout
  - the option with no value raises `SystemExit` with code 2
  - the option after the file name works
  - an invalid N with a non-existent file raises `SystemExit` with code 2, not `FileNotFoundError`
  - an empty file with a valid N prints nothing and returns 0

### Out of Scope

- A maximum-count option or a range filter.
- A short flag such as `-m`.
- Any change to tokenising, case handling, or ranking.
- Output formats other than `word count` lines (JSON, CSV).
- Changes to the glossary: the repo has no `GLOSSARY.md`, and this spec adds no new domain terms.

### Further Notes

Assumptions made because the user was unavailable. Each is the reading I would have asked about. The user should confirm or correct them on review.

1. **Non-integer values** (`abc`, `1.5`, empty string) are rejected with the same usage error and exit code 2 as N below 1. This follows from "N is a positive integer".
2. **Negative values** are errors, the same as 0, because the design says "N below 1 is an error".
3. **Threshold is inclusive**: a word is kept when its total count is at least N.
4. **No matching words is not an error**: the output is empty and the exit code is 0.
5. **Error text**: stderr contains the standard argparse usage line and an error line. The exact wording of the error line is not pinned; tests check for the usage line and exit code 2.
6. **Option position**: the option may appear before or after `FILE`, as argparse allows by default.
7. **Validation before file access**: an invalid N is reported before the file is opened.
8. **No upper bound** on N. Very large integers are accepted and simply match no words.
9. **README** gets a one-line mention of the option. This is a small documentation change inside the same work, not a new deliverable.
