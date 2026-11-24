# 5. Accepted date forms

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/dates.py`. Serves R-1 (QG-4): the expiry date is the input to the expiry listing.

## Decision

We will accept these forms for an expiry date, case-insensitively: `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd` (N days from today), and `+Nw` (N weeks from today). Relative forms are resolved against the local date when the command runs.

## Consequences

Users' scripts and habits depend on these forms. Adding a form is a compatible change; removing or changing one needs a new ADR. The local date means that the same input can resolve to different dates on different days.
