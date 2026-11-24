# 7. Expiry dates are local calendar dates

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/dates.py` (`parse`) and `pantry/model.py` (`Item.expires`). This decision is on the accepted list in ADR 0001 (date conventions). It serves R-1, which asks users to enter expiry dates.

## Decision

We will store expiry dates as local calendar dates without a time. Users may type `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd` (N days) or `+Nw` (N weeks). Relative forms are computed against the local date from `date.today()`.

## Consequences

Relative forms depend on the local date at the time of the command. Adding a time of day, or another input form, is a change to this convention and needs a new ADR.
