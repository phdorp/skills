# 6. Date input and date convention

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/dates.py` and `pantry/cli.py` (`list --soon`). Serves R-1 (QG-1). Accepted date forms: `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`. Relative dates count from `date.today()`.

## Decision

We will accept the date forms above as the input for expiry dates. We will treat every date as a calendar date without time, counted from the local date.

## Consequences

Users can type the forms directly. Relative dates depend on the machine's clock and time zone, so the same input can mean a different date on another day.

Question for the architect: keep these input forms and the local calendar-date convention?
