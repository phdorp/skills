# 5. Date formats

## Status

proposed

## Context

Found in the code, not decided by the architect: `pantry/dates.py` accepts `today`, `tomorrow`, `+Nd`, `+Nw` and ISO `YYYY-MM-DD`; `pantry/model.py` writes and reads the expiry as an ISO date. This serves R-1 (QG-2) and is a date format under ADR-0001.

## Decision

Users type `today`, `tomorrow`, `+Nd`, `+Nw` or `YYYY-MM-DD`. The file stores `YYYY-MM-DD`. A relative date resolves against the current date when the command runs.

## Consequences

Stored expiry dates are absolute, so an item added as `+3d` keeps its resolved date afterwards. Changing the stored format changes the file format and needs its own ADR.
