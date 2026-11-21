# 5. Add a PostgreSQL backend

## Status

rejected 2026-11-21. A database server contradicts R-3 (standard library only).

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
