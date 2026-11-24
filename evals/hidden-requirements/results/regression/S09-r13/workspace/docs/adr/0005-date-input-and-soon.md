# 5. Date input formats and the meaning of "soon"

## Status

proposed

## Context

Found in the code: `pantry/dates.py` (`parse`, `RELATIVE`) and the `--soon` branch of
`pantry/cli.py`. It serves R-1 ("list what expires soon"). Whether expired items count as "soon"
is an open question to the architect (Q11, not answered).

## Decision

The CLI accepts `today`, `tomorrow`, `+Nd` and `+Nw` (days and weeks counted from today), and
`YYYY-MM-DD`. Input is trimmed and case-insensitive. Anything else is a user error (exit 1). `list
--soon DAYS` shows the items whose expiry date is on or before today plus DAYS, including items
already past their expiry date.

## Consequences

Users may enter dates in four relative forms and one absolute form. Expired items appear in
`--soon` output until the architect decides otherwise (arc42 section 11).
