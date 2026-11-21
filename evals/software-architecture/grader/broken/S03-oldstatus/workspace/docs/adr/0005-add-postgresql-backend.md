# 5. Add a PostgreSQL backend

## Status

rejected 2026-11-21: we will not run a second storage engine; a server database contradicts R-3.

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
