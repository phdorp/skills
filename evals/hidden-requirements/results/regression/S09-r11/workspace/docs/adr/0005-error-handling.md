# 5. Error handling

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/cli.py` and `pantry/store.py`: user errors are printed
to stderr with a `pantry:` prefix, and lines of the pantry file that are not JSON are skipped
without a report. Serves R-1 (QG-1) and R-2.

## Decision

We will print user errors to stderr with a `pantry:` prefix. We will skip unreadable lines of the
pantry file without reporting them.

## Consequences

Skipping unreadable lines without a report can hide lost items, so arc42 section 11 records it as
a risk. Changing how unreadable lines are reported is a new ADR.
