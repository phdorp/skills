# 5. Crosscutting conventions: errors and dates

## Status

proposed

## Context

Found in the code: `pantry/cli.py:1` documents the exit codes; `pantry/cli.py:27-29` and `:33`
print user errors to stderr with the `pantry:` prefix; `pantry/cli.py:23` maps argparse errors to
exit code 2; `pantry/model.py:12` and `pantry/store.py:15` write dates as ISO 8601. Serves R-1 (the
add and list commands report errors and show dates the user can read).

## Decision

We will report user errors on stderr with the prefix `pantry:` and exit with code 1. We will exit
with code 2 on bad command-line usage. We will store and show dates as ISO 8601 `YYYY-MM-DD`.

## Consequences

Any new command follows these conventions, which keeps its errors and exit codes the same as the
existing ones.
