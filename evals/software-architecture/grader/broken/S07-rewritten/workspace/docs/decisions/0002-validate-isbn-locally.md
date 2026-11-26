# 2. Validate ISBNs locally

## Status

accepted (legacy)

## Context

Books are often added offline, and a wrong ISBN makes `find` miss them later (R-4).

## Decision

ISBNs are validated by an online lookup before a book is stored.

## Consequences

A correctly formed but unassigned ISBN is accepted.
