# 8. Error reporting on stderr, naming the input

## Status

proposed

## Context

Found in the code, not decided: `pantry/cli.py` prints user errors to stderr with the offending input (`not a date`, `no such item`). Serves R-1 (QG-4).

## Decision

We will report user errors on stderr as `pantry: <message>`, naming the input that caused them.

## Consequences

Output on stdout stays the list of items, so scripts reading it are unaffected. Exit codes are governed by ADR 0005.

Question for the architect: keep this error format?
