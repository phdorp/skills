# 2. Validate ISBNs locally

## Context

Books are often added offline, and a wrong ISBN makes `find` miss them later.

## Decision

ISBNs are checked locally with their check digit before a book is stored; no online lookup.

## Consequences

A correctly formed but unassigned ISBN is accepted.
