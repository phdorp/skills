---
name: add-requirements
description: Use when the architect brings new requirements for a project that has an architecture (`docs/architecture/arc42.md`).
metadata:
  opencode/autoinvoke: false
---

# Add Requirements

The architect brings new requirements; you check each against the architecture, propose what
should happen to it, and apply only the outcomes the architect confirms. Requirement procedures
(the R-list format, ranking, quality goals) live in `quality-requirements`; ADRs live in
`domain-modeling`. Load both before you change any file.

## Precondition

Read `docs/architecture/arc42.md`. Without it, offer to run `setup-architecture` first and stop.

## 1. Check each requirement

Read the whole R-list (arc42 section 1), the quality goals, the stakeholders, the constraints
(section 2), and every accepted ADR in `docs/adr/`. Then, for each new requirement:

1. **Duplicate:** compare it with every R-list row, `deferred` and `rejected` rows included.
   Name the row it repeats.
2. **Consistency:** name each active requirement it conflicts with, by R-ID.
3. **Direction:** name each conflict with section 1's goals and stakeholders, a top quality
   goal, a section 2 constraint, or an accepted ADR, by its ID or number.
4. **Outcome:** propose one of four, with a one-line reason:

| outcome | when | what confirming it changes |
|---|---|---|
| system-level | it shapes the architecture | a new R-list row, `active` |
| feature-level | it fits inside an existing requirement | an issue citing that parent R-ID; no R-list row |
| deferred | the architect may want it later | a new R-list row, `deferred`, with their reason |
| rejected | it conflicts with the direction | a new R-list row, `rejected`, with their reason |

A duplicate gets no outcome of its own: propose "no new row" and name the row it repeats.

Done when every new requirement has its findings and a proposed outcome.

## 2. Ask the architect

Show one table (requirement, findings by ID, proposed outcome and reason) and ask the architect
to confirm or change each outcome. Offer a sharper wording where it helps, as a proposal.

This step changes no file: no R-list row, ADR, issue or code. It ends with the question. When
the architect's message already gives an outcome for every requirement, that is the
confirmation: go to step 3 with their outcomes, and name in your report any finding that
contradicts one of them.

## 3. Apply the confirmed outcomes

Existing R-list rows stay exactly as they are: ID, wording, rank, status and reason. A new
requirement that repeats a deferred or rejected row changes nothing in that row; say in your
report that it was asked for again.

- **System-level:** append a row with the next free R-ID (one past the highest, deferred and
  rejected rows included), the architect's wording, status `active`, and a rank proposed
  through `quality-requirements` › Rank. Then run
  `quality-requirements` › Goal impact.
- **Conflict with an accepted ADR:** draft a superseding ADR through `domain-modeling`. It is
  `proposed`, and the ADR it replaces stays `accepted`. Work that depends on the change waits
  for the architect's approval of the new ADR: change no code for it.
- **Feature-level:** file an issue in the tracker named in `docs/agents/issue-tracker.md`, or,
  without one, as `.scratch/requirements/issues/NN-<slug>.md`. It cites the parent R-ID; it
  continues through `triage`.
- **Deferred or rejected:** append a row with the next free R-ID, that status, and the
  architect's reason in one line.
- **Duplicate:** no new row.

Done when every confirmed outcome is applied and nothing else changed.

## 4. Report

List the rows you added, the issues you filed, the ADRs you drafted, and every question still
open for the architect: the proposed ranks to set, each goal-impact question, and each ADR
waiting for approval together with the work that waits for it ("<the change> waits until
you accept ADR-NNNN").

| Thought | Reality |
|---|---|
| "Requirement 4 fits the architecture, I'll build it while they decide the rest" | Step 2 ends with the question. Building is a later ticket, after triage. |
| "They confirmed the outcome, so the superseding ADR is accepted" | They confirmed a direction. The ADR is `proposed` until they approve its text, and the storage work waits for it. |
| "I'll note in R-4 that users asked again" | R-4's row stays as it is. The repeat goes in your report. |
| "Encryption is system-level, so it needs a security goal; I'll add one" | Goal impact proposes the goal as a question; the goal tables stay as they are. |
| "No rank was given, I'll leave it blank" | Propose a rank and ask the architect to set the order. |
