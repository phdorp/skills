# Tally Min-Count Spec

Status: ready-for-agent
Source: the approved design given in the conversation that produced this spec (`tally --min-count N FILE`). The design owner was not available for questions; every point the design left open is recorded as an assumption under Further Notes.

### Problem Statement

`tally` prints every distinct word in a file. On a long text, most of the output is words that appear once or twice, and the words that recur are buried among them. A user who wants to see only the recurring words has to scroll through or post-process the whole list.

### Solution

`tally` accepts a `--min-count N` option. When it is given, `tally` prints only the words that occur at least N times in the file. Each line keeps the same `word count` format and the same order as today: most frequent first, ties in alphabetical order. When the option is omitted, the output is exactly as it is today. When N is zero or negative, `tally` refuses to run and reports a usage error.

### User Stories

1. As a user counting words in a file, I want to pass `--min-count N`, so that only the words counted at least N times are printed.
2. As a user, I want `tally FILE` without the option to print every word, exactly as it does today, so that existing scripts keep working.
3. As a user, I want the filtered list in the same order as the unfiltered list (most frequent first, ties alphabetical), so that I can read it the same way.
4. As a user, I want a word that occurs exactly N times to be included, so that the threshold is inclusive ("at least N").
5. As a user, I want `--min-count 1` to print every word, so that the option never hides a word unless I ask it to.
6. As a user, I want N larger than the most frequent word's count to produce no output and exit successfully, so that "no word repeats that often" is a normal answer and not an error.
7. As a user, I want an empty file to print nothing and exit successfully, with or without the option.
8. As a user, I want `--min-count 0` to fail with the usage message on stderr and exit code 2, so that a mistaken threshold cannot silently print nothing or everything.
9. As a user, I want a negative N (for example `--min-count -3`) to fail the same way as zero, so that the error is consistent.
10. As a user, I want a non-integer N (for example `abc`, `2.5`, or an empty string) to fail with the usage message on stderr and exit code 2, so that a typo is reported and not guessed at.
11. As a user, I want `--min-count` with no value to fail with the usage message on stderr and exit code 2.
12. As a user, I want to write the option before or after the file name, and as `--min-count=N` or `--min-count N`, so that it behaves like the other options of the standard argument parser.
13. As a user, I want nothing written to stdout when the option is rejected, so that a pipeline does not receive partial or misleading output.
14. As a user, I want a very large N (for example one billion) to be accepted and produce no output, so that I never hit an artificial upper limit.
15. As a user, I want the README to show the new option, so that I can find it without reading the source.

### Implementation Decisions

- **Counting is unchanged.** Words are still counted case-insensitively with the same word pattern. The option does not change any count; it only decides which counted words are printed.
- **Filtering happens after counting and before printing.** A word is printed if and only if its count is greater than or equal to N. Ranking (most frequent first, ties alphabetical) is applied to the kept words exactly as it is today.
- **Interface of the counting and formatting helpers.** The counting helper keeps its current contract. The formatting helper gains an optional minimum count that defaults to 1, so every existing caller and every existing test keeps its current behaviour.
- **The option is parsed by the existing argument parser.** The option takes one value. The value is validated as a positive integer at parse time. Any invalid value, whether below 1, non-integer, or missing, is reported through the parser's standard usage-error path: the usage line and a specific message on stderr, exit code 2, with nothing written to stdout. The exact wording of the specific message is not fixed by this spec.
- **No new module, no new file.** The change lives in the existing CLI module, with a one-sentence addition to the README's usage description.
- **Unchanged behaviour.** Missing file argument, unreadable file, and the program's exit code 0 on success are not changed by this feature.

### Testing Decisions

- **What makes a good test here.** Tests observe external behaviour: the lines printed to stdout, the text written to stderr, and the exit code. They do not inspect internal data structures or the order in which helpers are called.
- **Seam.** The existing `main(argv)` entry point in the CLI module is the seam. It already proves the behaviour end to end (argument parsing, counting, filtering, output), and the existing tests use it with captured stdout. No new seam is proposed.
- **Modules tested.** The CLI module only. One direct test of the formatting helper's minimum-count parameter is acceptable as a boundary check, but the main proof is through `main`.
- **Required cases through `main`:**
  - with `--min-count 2` on a file whose counts are 3, 2, 1: only the words with counts 3 and 2 are printed, in the existing order;
  - with `--min-count` equal to a word's count: that word is printed (inclusive boundary);
  - with `--min-count` greater than every count: nothing is printed and the exit code is 0;
  - with `--min-count 1`: the output equals the output without the option;
  - without the option: the output is byte-for-byte what `test_prints_every_word` already expects;
  - with `--min-count 0`, `--min-count -1`, `--min-count abc`, `--min-count 2.5`, and a missing value: `SystemExit` with code 2, the usage text on stderr, and nothing on stdout;
  - the option written after the file name and in the `--min-count=N` form: same output as the canonical form.
- **Prior art.** `tests/test_cli.py`: `Main.test_prints_every_word` shows how to call `main` with a temporary file and capture stdout. `CountWords.test_ranks_by_count_then_alphabetically` shows the expected ordering that filtered output must keep. Stderr capture and the `SystemExit` check have no prior art in this repo and are new.

### Out of Scope

- Changing the word pattern, case handling, or ordering.
- A maximum value for N, or any upper bound.
- Reading from standard input, or handling a missing or unreadable file more gracefully than today.
- Other output formats, such as JSON or CSV.
- A short option letter for `--min-count`.
- Any change to the exit code of a successful run.

### Further Notes

The design owner was not available to answer questions. The following points were open in the approved design or are implied by it. Each is recorded here as an assumption to confirm, with the reason for it. None is deferred.

- **A1. Non-integer values are rejected like values below 1.** The design names only "N below 1". N is specified as a positive integer, so `abc`, `2.5`, and an empty string are treated as the same kind of error: usage on stderr, exit code 2.
- **A2. A missing value is rejected the same way.** `--min-count` with no value after it is a usage error with exit code 2.
- **A3. Negative values are values, not options.** `--min-count -3` is read as the value -3 and then rejected under A1's rule for values below 1.
- **A4. Repeated option: the last value wins.** This is the standard behaviour of the argument parser, and the spec does not add a rejection for repeats.
- **A5. No upper bound on N.** A very large N is valid and produces no output.
- **A6. Usage errors exit with SystemExit(2).** The error is raised through the argument parser, so the code path is the same one that already handles unknown options. Callers of `main` that catch `SystemExit` see code 2. `__main__` passes the exit status through unchanged.
- **A7. The exact wording of the error message is not fixed.** Tests check that the usage text appears on stderr and that the exit code is 2. They do not compare the full message.
- **A8. Seam choice.** The seam is the existing `main(argv)` entry point, as described under Testing Decisions. The design did not name a seam, so this was chosen by the spec author.
- **A9. README.** The README's usage text gains one sentence describing the option. This is part of the change, not a separate task.
- **A10. Filtering is inclusive.** A word whose count equals N is printed. This follows from "at least N times" in the design.

Nothing in this list is deferred. Each item becomes final when the design owner reads this spec and either accepts it or asks for a change.
