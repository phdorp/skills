# 0001. Record architecture decisions

Status: Proposed. The approval text was not found in the repository or the conversation, so this record is not yet marked Accepted.

## Context

Until now the architecture existed only in the code. The reasons behind choices such as the append-only event log, the standard-library-only constraint, and the one-module-per-command rule were not written down. `docs/architecture.md` describes the current structure. It does not record why each decision was made or what was considered and rejected.

## Decision

Architecture decisions are recorded as numbered Markdown files in `docs/adr/`, one decision per file, using this layout:

- **Status**: Proposed, Accepted, Superseded by NNNN, or Deprecated.
- **Context**: the forces and requirements that made the decision necessary.
- **Decision**: what was chosen, stated in the present tense.
- **Consequences**: what becomes easier or harder, including known gaps.

Once accepted, an ADR is not edited for substance. A changed decision gets a new ADR that supersedes the old one, and the old one's status is updated to point to it. Typo fixes and links are allowed.

`docs/architecture.md` describes the current system. It links to ADRs for the reasons behind it.

## Consequences

- Decisions have a dated, numbered record, so a reader can tell what was chosen and why.
- Each decision costs a short file. Small, reversible choices do not need one.
- Known gaps, such as the torn-write bug in `docs/architecture.md`, should be cross-referenced from the ADR for the decision they affect (append-only storage, ADR not yet written).
