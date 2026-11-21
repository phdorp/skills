# 2. Validate ISBNs locally

## Status

accepted (legacy)

## Context

Books are often added offline, and a wrong ISBN makes `find` miss them later (R-1, R-4).

## Decision

ISBNs are checked locally with their check digit before a book is stored; no online lookup.

## Consequences

A correctly formed but unassigned ISBN is accepted. The check applies only when an ISBN is given;
whether an ISBN is required is still open for the architect (see the report).
