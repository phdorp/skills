# 0007. Dates are ISO 8601 calendar dates

## Status

proposed

## Context

Found in `model.py` (`isoformat` and `fromisoformat`), `dates.py` and the output of `cli.py`.
Serves R-1 and QG-2.

## Decision

We will store and print dates as ISO 8601 calendar dates (`YYYY-MM-DD`). Users may type an ISO
date, `today`, `tomorrow`, `+Nd` or `+Nw`. Relative forms resolve to an absolute date when the
command runs.

## Consequences

A stored date keeps its meaning on any later day. Times of day are not supported. Relative
dates resolve against the local date of the machine at the time of the command.
