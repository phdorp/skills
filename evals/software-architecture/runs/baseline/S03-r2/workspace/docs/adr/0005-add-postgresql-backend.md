# 5. Add a PostgreSQL backend

## Status

rejected 2026-11-21

We will not run a second storage engine. A server database contradicts R-3 (runs with only the
Python standard library, no installation). The search-speed request behind this ADR (R-1) is
still open; this rejection does not address it.

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
