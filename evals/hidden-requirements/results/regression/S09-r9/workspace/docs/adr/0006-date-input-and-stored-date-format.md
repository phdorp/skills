# 0006. Accepted date forms, and the ISO 8601 date format in the file

## Status

proposed

## Context

As found in the code, not yet decided by the architect: `pantry/dates.py:1,5,8-19` accepts `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd` and `+Nw`, relative to today, ignoring case and surrounding spaces. `pantry/model.py:12` and `:24` store and read dates as ISO 8601 strings. This serves R-1 (an item is added with an expiry date). It is a central decision under ADR-0001.

## Decision

The CLI accepts these five date forms. The file stores each date as an ISO 8601 `YYYY-MM-DD` string. Relative dates count days or weeks from today.

## Consequences

Existing pantry files depend on the stored format. Changing it needs a new ADR that supersedes this one, and a plan for existing files.
