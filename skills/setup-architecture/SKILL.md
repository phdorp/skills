---
name: setup-architecture
description: Use when the architect sets up architecture documentation for a project: a fresh project, existing documentation, or code without documentation.
metadata:
  opencode/autoinvoke: false
---

# Setup Architecture

Setting up the architecture means writing down what the architect decides: their requirements,
their quality goals, and the line between decisions made centrally and decisions left to
building blocks. You prepare and propose; the architect decides. Code comes later, in ordinary
tickets, once the architecture is accepted.

Requirements and goals follow `quality-requirements` (the R-list and goal tables, Rank, Derive
goals, Gap question). ADRs follow `domain-modeling`. Load both before you write any file.

## 1. Find the situation

| what the project holds | situation |
|---|---|
| no source files and no architecture documentation | fresh |
| architecture documentation: an arc42 file, `docs/architecture/`, or an ADR directory | documented |
| source files without architecture documentation | undocumented |

A README that only describes the product idea is not architecture documentation. This version
handles fresh projects. For a documented or undocumented project, tell the architect which
situation you found and that this setup does not handle it yet, and stop.

## 2. Fresh project, first turn: skeleton and proposal

1. Write `docs/architecture/arc42.md` from [references/arc42-skeleton.md](references/arc42-skeleton.md):
   all twelve section headings, the empty tables of sections 1 and 10, and the links of sections
   9 and 12. This is the only file this turn writes.
2. Send the architect one message with your proposal:
   - **Triage:** for each requirement, its proposed outcome and a one-line reason, using the
     checks of [add-requirements](../add-requirements/SKILL.md) step 1 (against an empty
     R-list, only the outcome remains). Offer sharper wording as a proposal.
   - **Rank:** the system-level requirements in a proposed order (`quality-requirements` › Rank).
   - **Quality goals:** the candidates with their scenarios, and the open questions for any
     goal without a measure (`quality-requirements` › Derive goals).
   - **Gap questions** (`quality-requirements` › Gap question).
   - **Decisions made centrally:** the draft list for ADR-0001, from
     [references/made-centrally-adr.md](references/made-centrally-adr.md), adjusted to this
     product.
3. Ask the architect to confirm or change each part.

Done when the skeleton exists and your message ends with that question.

## 3. After the architect confirms

Write what they confirmed, in this order:

1. The R-list rows, `R-1` upwards in the confirmed order, and an issue for each feature-level
   requirement, as in [add-requirements](../add-requirements/SKILL.md) step 3.
2. The confirmed goals and scenarios as `QG-n` (section 1) and `QS-n` (section 10). A goal
   still without a measure stays an open question in your report.
3. `docs/adr/0001-record-architecture-decisions.md` from the template, status `proposed`, its
   Context citing the R- and QG-IDs it serves; section 9 links it.

Done when every confirmed item is written and nothing unconfirmed is.

## 4. Report

List the files written, the open questions (unmeasured goals, anything the architect left
unanswered), and ADR-0001 waiting for the architect's approval of its text, with what waits for
it: work on any decision on its list.

| Thought | Reality |
|---|---|
| "Set up the architecture means scaffold the code" | Setup writes the architecture documents. Code is ordinary work after ADR-0001 is accepted. |
| "The architect gave the requirements, so I'll write the R-list now" | The triage is a proposal until they confirm it. Turn one writes the skeleton only. |
| "I'll pick the storage engine now so the docs are complete" | Storage is a decision made centrally: it goes on ADR-0001's list and gets its own ADR later. |
| "They said 'confirmed', so ADR-0001 is accepted" | They confirmed your proposals. ADR-0001 is `proposed` until they approve its written text. |
