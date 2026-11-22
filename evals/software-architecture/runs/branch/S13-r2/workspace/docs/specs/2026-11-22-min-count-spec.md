# `--min-count` Spec

Status: ready-for-agent
Source: conversation (approved design for a new `tally` option: "Here is the approved design for a new tally option. Write the spec.")

## Problem Statement

`tally` prints every word in a text file, one `word count` line each. On a long file most lines are words that occur once or twice, and the user has to scan past them to find the words that repeat. They want to see only the words that occur often enough to matter.

## Solution

`tally` gets a new option, `--min-count N`. With it, `tally --min-count N FILE` prints only the words that occur at least `N` times in `FILE`. Each printed line keeps today's `word count` format. Ordering does not change: most frequent first, ties in alphabetical order. Without the option, `tally FILE` behaves exactly as it does today.

## User Stories

1. As a user counting words in a file, I want `--min-count N` to print only words counted at least N times, so that I can see the recurring words without scanning past one-off words.
2. As a user, I want the printed lines to keep the `word count` format, so that output from `--min-count` can be read or piped exactly like today's output.
3. As a user, I want the most frequent words to still come first and ties to stay alphabetical, so that the filtered list reads in the same order as the full list.
4. As a user who does not pass `--min-count`, I want every word printed as before, so that existing scripts and habits keep working.
5. As a user passing `--min-count 1`, I want every word printed, since every word occurs at least once, so that the value 1 is a harmless no-op.
6. As a user whose `N` is larger than the count of every word, I want no lines printed and exit code 0, so that "nothing repeats that often" is reported as an empty result, not an error.
7. As a user whose file contains no words (empty file, or only punctuation and digits), I want no lines printed and exit code 0 with or without `--min-count`, so that an empty file is not an error.
8. As a user who passes `--min-count 0`, I want a usage message on stderr and exit code 2, so that I learn the value is invalid instead of getting a silently wrong result.
9. As a user who passes a negative `N`, such as `--min-count -3`, I want the same usage message on stderr and exit code 2 as for `0`.
10. As a user who passes a value that is not an integer, such as `--min-count abc` or `--min-count 2.5`, I want the same usage message on stderr and exit code 2, since the value is not a positive integer.
11. As a user who passes `--min-count` without a value, I want the standard argument error on stderr and exit code 2, so that a missing value is reported like any other bad argument.
12. As a user, I want to place `--min-count N` before or after the file name, so that both `tally --min-count 2 FILE` and `tally FILE --min-count 2` work.
13. As a user who passes an invalid `N`, I want nothing printed to stdout, so that a script never receives a partial or unfiltered list from a bad call.
14. As a user who passes a very large `N` (larger than any count), I want the same empty result as in story 6, so that there is no upper limit to document.
15. As a user with a missing or unreadable file, I want the behaviour unchanged from today, so that this feature does not alter file-error handling. (Out of scope to improve; see Out of Scope.)

## Implementation Decisions

- **Module changed:** `tally/cli.py` only. The filter is applied in the same place the existing ranking happens, after counting and before printing. Counting (`count_words`) and ordering (`format_counts`) keep their current behaviour and signatures.
- **Interface change:** `main(argv=None)` accepts one new optional argument, `--min-count` with a value. Its value is stored as an integer. Without the option, the value is absent and no filtering happens.
- **Validation:** a value is valid only if it is a base-10 integer of at least 1. Validation is done at argument-parse time, not after counting, so an invalid value fails before the file is read. Use argparse's own type-validation mechanism so the error path is the standard argparse one: a usage line and an error line on stderr, then exit status 2.
- **Error contract:** for any invalid value (zero, negative, non-integer, or missing), `main` ends with exit status 2 and writes the usage message to stderr. Nothing is written to stdout. Because argparse signals this by raising `SystemExit` with code 2, callers of `main` observe `SystemExit` with `code == 2`. This is the behaviour tests pin; `main` does not return 2 in this case.
- **Filter rule:** keep a word if and only if its count is greater than or equal to `N`. The comparison uses the same counts `count_words` produces (lowercased, same word pattern). No other rule (no stopword list, no length limit).
- **Output contract:** each kept word is printed as `word count` on its own line, using the existing format. Lines are sorted with the existing rule: descending count, then ascending alphabetical word. The filter does not change the sort key.
- **Return value:** a successful run, filtered or not, returns `0`, as today.
- **README:** the usage section gains one example of `--min-count` and one sentence describing it. This is documentation only.
- **Assumption (non-integer values):** the spec treats non-integer values such as `2.5` and `abc` as invalid in the same way as values below 1. The user did not state this; it is the natural reading of "N is a positive integer".
- **Assumption (position of the option):** the option may appear before or after the positional file argument. This is argparse's default and the spec does not restrict it.
- **Assumption (no upper bound):** there is no maximum for `N`. Any integer at least 1 is valid.

## Testing Decisions

- **What good tests look like here:** they call `main` with an argument list and check what is printed to stdout, the return value, and, for invalid input, the `SystemExit` code and stderr text. They do not check private helpers' internals or the argparse object.
- **Seam:** `tally.cli.main(argv)`. It is the highest seam that proves every behaviour in this spec, including the exit code and the stderr usage message. Existing tests already drive it this way, so no new seam is needed.
- **Modules tested:** `tally/cli.py` only, through `main`.
- **Prior art:** `tests/test_cli.py`, class `Main`, method `test_prints_every_word`. It writes a temporary file, redirects stdout with `contextlib.redirect_stdout`, calls `main([str(path)])`, and checks the output string. New tests follow this pattern. For stderr, use `redirect_stderr` in the same way.
- **Tests to add (each named by behaviour):**
  - prints only words with count at or above N, in the existing order (stories 1, 3);
  - keeps the `word count` line format (story 2);
  - without the option, prints every word, unchanged from the existing test (story 4);
  - `N = 1` prints every word (story 5);
  - `N` above every count prints nothing and returns 0 (stories 6, 14);
  - an empty file prints nothing and returns 0, with and without the option (story 7);
  - `N = 0`, `N = -3`, `N = abc`, and `N = 2.5` each raise `SystemExit` with code 2, print the usage line to stderr, and print nothing to stdout (stories 8–10, 13);
  - `--min-count` with no value raises `SystemExit` with code 2 (story 11);
  - the option works both before and after the file argument (story 12).
- **Not tested:** the exact wording of argparse's error text beyond the `usage:` prefix and the phrase `--min-count`. Those are argparse's responsibility.

## Out of Scope

- Changing how a missing or unreadable file is reported. Today it raises an uncaught exception; this feature leaves that as is.
- Other filters (maximum count, minimum word length, stopwords, top-N limits).
- Changing counting rules, the word pattern, or the sort order.
- Machine-readable output formats.
- Any change to the `format_counts` or `count_words` signatures.

## Further Notes

- **Assumptions made without the user:** the user was not available to answer questions. The assumptions are stated inline in Implementation Decisions. The main ones are: non-integer values are invalid like values below 1; the option works in either position; there is no upper bound on `N`; invalid values exit 2 through `SystemExit`, the standard argparse path.
- **Behaviour verified against the installed Python:** an argparse parser using a type function that raises `ArgumentTypeError` for values below 1 prints `usage: tally [-h] [--min-count MIN_COUNT] file` and `tally: error: argument --min-count: ...` to stderr and raises `SystemExit(2)` for `0`, `-3`, and `abc`; and accepts `--min-count 2` after the positional argument. The implementer should re-check this with the tests.
- **Open decisions:** none. Every decision the design left open has an assumption stated above.
