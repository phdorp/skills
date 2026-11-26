# 5. Add a PostgreSQL backend

## Status

rejected 2026-11-21

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.

## Outcome

Rejected. We will not run a second storage engine, and a server database contradicts R-3
(installs on locked-down machines with only the standard library).
