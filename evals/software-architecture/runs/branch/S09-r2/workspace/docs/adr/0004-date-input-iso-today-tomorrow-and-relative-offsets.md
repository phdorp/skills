# 4. Date input: ISO, today, tomorrow, and +Nd or +Nw

## Status

proposed

## Context

Found in the code, not decided: `pantry/dates.py` (`parse`). Serves R-1 (QG-4).

## Decision

We will accept an expiry date as an ISO date, `today`, `tomorrow`, `+Nd` or `+Nw`, resolved against the local date when the item is added.

## Consequences

The stored date is absolute, so later changes of the clock do not move it. Adding another input form is a change to the user interface and needs a new ADR (ADR 0005).

Question for the architect: keep these input forms?
