# 7. Dates and date input

## Status

proposed

## Context

Users type dates (R-2, QG-2), and units are a central crosscutting convention (ADR 0001). Found in `pantry/dates.py`, `pantry/model.py` and `pantry/cli.py`.

## Decision

Dates are calendar days, with no time and no zone. Input is `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd` or `+Nw`, in any letter case. Relative dates resolve against the local date from `date.today()`. Dates are stored as ISO strings.

## Consequences

The result of `list --soon` depends on the clock of the machine running it. A change of grammar or of time zone handling changes what users' inputs mean, so it needs a new ADR that supersedes this one.
