# 2. Validate ISBNs locally

## Status

Accepted

## Context

Books are often added offline, and a wrong ISBN makes `find` miss them later.

## Decision

ISBNs are checked locally with their check digit before a book is stored; no online lookup.
The check lives in `isbn.valid` and is applied by `cli.add`.

## Consequences

- A correctly formed but unassigned ISBN is accepted.
- Enforcement is in `cli.add` only. `catalog.add` stores any string, so the decision is not yet
  enforced for other callers (see [architecture gaps](../architecture.md#known-gaps)).
- ISBN lookup compares strings exactly today, so the check digit is verified but formatting is not
  normalised on search.
