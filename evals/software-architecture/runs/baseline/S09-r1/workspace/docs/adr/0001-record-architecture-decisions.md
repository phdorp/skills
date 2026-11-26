# 1. Record architecture decisions

**Status:** Proposed. This is a draft, not the approved text. The approved
version of this ADR was not in the repository, so the content below is taken
from the Decisions section of `ARCHITECTURE.md`. Replace it with the approved
text before relying on it.

## Context

Pantry's design rests on a few choices that are not obvious from the code:
an append-only event log, replay on every read, an fsync on every write, and a
standard-library-only constraint. Without a record, a later change could undo
one of them without knowing why it was made.

## Decision

Record significant architecture decisions as numbered ADRs in `docs/adr/`.
Each ADR states its context, the decision, and its consequences. Architecture
decisions are described in `ARCHITECTURE.md`; each ADR states the reason for
one decision.

## Consequences

- Decisions have a stable place to be reviewed and superseded.
- Changes that reverse a recorded decision must add a new ADR that supersedes
  the old one, rather than editing history.
