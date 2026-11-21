# 3. Records are JSON objects with op, name and expires

## Status

proposed

## Context

Found in the code, not decided: `pantry/model.py` (`Item.to_record`, `removal`, `replay`). Serves R-1 (QG-4).

## Decision

We will record an add as `{"op": "add", "name": NAME, "expires": ISO-DATE}` and a remove as `{"op": "remove", "name": NAME}`. Replay applies them in file order, so a later add of the same name replaces the earlier one.

## Consequences

A new op or key changes the file format and needs a new ADR. Replay raises an error on a record that lacks a key (arc42 section 11, risk 3).

Question for the architect: keep this record format?
