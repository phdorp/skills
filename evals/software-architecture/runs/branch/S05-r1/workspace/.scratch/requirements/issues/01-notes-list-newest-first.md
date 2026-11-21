# `notes list` shows the newest notes first

Parent requirement: R-1 (Users add, list and search notes from the command line.)

Requirement (from user interviews this week): `notes list` shows the newest notes first.

Triage: feature-level, fits inside R-1. No R-list row.

Open: ordering depends on each note's creation time. The `Note` value has a `created` field, but
it is a `str` with no format specified, so ordering by it needs a defined timestamp format.
Confirm that this still holds if ADR-0004 is accepted.
