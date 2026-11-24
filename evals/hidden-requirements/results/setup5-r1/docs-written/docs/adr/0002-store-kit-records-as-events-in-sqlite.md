# 2. Store kit records as events in SQLite

## Status

proposed

## Context

Decided centrally under "Record architecture decisions" (ADR 0001, accepted): where check-out and loss records are stored, and their data format. The forces are:

- check-out and check-in must work with no mobile signal and sync later (R-5, QG-3), and two offline events for one bag must both be kept (architect's answer to Q14);
- every event must trace to one coach (QG-5), and nothing recorded before a restart may be lost (QG-6);
- records older than 2 years are deleted while the item list is kept (R-9);
- the system runs on the club's Synology NAS in Docker, on Python, with a budget of 0 EUR and no third-party cloud (constraints, arc42 section 2);
- the size is about 300 items and 40 coaches, with a ceiling of 1,000 items and 60 coaches (arc42 section 3).

## Decision

We will store kit records in one SQLite database file on the NAS, in a Docker volume, using the Python standard-library `sqlite3` module.

Each check-out, check-in and loss is one row in an `events` table, appended and never edited. Each event holds the item, the coach, the kind of event, the time the coach acted and the time the server received it. The phone creates each event with its own ID, so an event sent twice is stored once.

The holder of an item is derived from its events, not stored separately. Item definitions (name, QR code, expiry date for first-aid items) sit in a separate `items` table.

## Consequences

Easier: no extra service to run, no new dependency, one file to back up with the NAS backups. Append-only events keep every offline event, so conflicts (Q14) are visible rather than overwritten, and every event names its coach (QG-5).

Harder: SQLite allows one writer at a time. That is enough for 60 coaches, but if writes ever become contended, this decision is reopened by a new ADR. The `events` table grows, so the R-9 deletion job must remove events older than 2 years and keep `items`.

Not decided here, and each needs its own ADR from the centrally decided list: the sync protocol between phone and server (interfaces), the CSV export format (R-7), and the versioning of the record format once the export depends on it.

Work that depends on this decision (the item catalogue and the coach trace, issues 01 and 02; the expiry warning, issue 03) waits until this ADR is accepted.
