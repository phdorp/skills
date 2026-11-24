# 4. Record shape and accepted date formats

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/model.py` writes an add as
`{"op": "add", "name", "expires"}` with `expires` in ISO format, and a removal as
`{"op": "remove", "name"}`. `pantry/dates.py` accepts `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`
and `+Nw`. It serves R-1.

## Decision

We will write records in the shape above, and we will accept the date formats above on input.

## Consequences

Changing either shape or the accepted formats changes stored data or the command line, so a
change needs its own ADR and a migration of existing files.
