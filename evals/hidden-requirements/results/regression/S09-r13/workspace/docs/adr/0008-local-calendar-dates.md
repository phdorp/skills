# 8. Expiry dates are local calendar dates

## Status

proposed

## Context

Found in the code: `pantry/model.py` (`Item.expires` is a `date`), `pantry/dates.py` (`date.today()`)
and the `--soon` branch of `pantry/cli.py` (`date.today()`). It serves R-1, and it is a crosscutting
convention on the list in ADR 0001.

## Decision

An expiry date is a calendar date with no time and no zone. It is stored and printed as
`YYYY-MM-DD`. "Today" is the local date of the machine at the time of the command.

## Consequences

Results of `list --soon` shift when the machine's date or zone changes. No time of day is recorded,
so an item cannot expire at a given hour.
