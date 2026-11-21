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
| architecture documentation in any form: an arc42 file, `docs/architecture/`, an ADR directory, or a README, wiki or design-doc section that describes the parts of the system or why it is built the way it is | documented |
| source files without architecture documentation | undocumented |

A README that only describes the product idea or how to run it is not architecture
documentation; a README section on how the system is built is. In an undocumented project,
the architecture is recovered from the code once the architect has approved the list of
decisions made centrally, because that list decides which findings become ADRs.

## 2. First turn: skeleton and proposal

1. Write `docs/architecture/arc42.md` from [references/arc42-skeleton.md](references/arc42-skeleton.md):
   all twelve section headings, the empty tables of sections 1, 5 and 10, and the links of
   sections 9 and 12. In a documented project, each section whose content already lives in
   another document links to it (references/arc42-skeleton.md › Existing documents). This is
   the only file this turn writes: existing documents and ADRs stay as they are.
2. Send the architect one message with your proposal:
   - **Triage:** for each requirement, its proposed outcome and a one-line reason, using the
     checks of [add-requirements](../add-requirements/SKILL.md) step 1 (against an empty
     R-list, only the outcome remains). Offer sharper wording as a proposal.
   - **Rank:** the system-level requirements in a proposed order, a one-line reason for each
     (`quality-requirements` › Rank).
   - **Quality goals:** the candidates the system-level requirements imply, with their
     scenarios, and the open questions for any goal without a measure
     (`quality-requirements` › Derive goals). A feature-level requirement gets no R-ID and
     no goal.
   - **Gap questions** (`quality-requirements` › Gap question).
   - **Where your documents map** (documented project): each existing document, the arc42
     section that links to it, and the statement that the document stays where and as it is.
   - **Legacy ADRs** (documented project): the ADRs without a Status, offered for upgrade in
     one batch as `domain-modeling` describes, each with the IDs its Context would cite. Their
     decisions stay as they are.
   - **Decisions made centrally:** the draft list for the "Record architecture decisions" ADR,
     from [references/made-centrally-adr.md](references/made-centrally-adr.md), adjusted to
     this product, and its number: the next free one in the project's ADR directory. In an
     undocumented project, say that recovering the architecture from the code waits for the
     architect's approval of this ADR.
3. Ask the architect to confirm or change each part.

Done when the skeleton exists and your message ends with that question.

## 3. After the architect confirms

Write what they confirmed, in this order:

1. The R-list rows, `R-1` upwards in the confirmed order, and an issue for each feature-level
   requirement, as in [add-requirements](../add-requirements/SKILL.md) step 3.
2. The confirmed goals and scenarios as `QG-n` (section 1) and `QS-n` (section 10). A goal
   still without a measure stays an open question in your report.
3. The legacy ADRs, upgraded as `domain-modeling` describes, when the architect confirmed the
   batch.
4. The "Record architecture decisions" ADR from the template, as the next free number in the
   project's ADR directory (`0001-record-architecture-decisions.md` in a fresh project), status
   `proposed`, its Context citing the R- and QG-IDs it serves; section 9 links it.

Done when every confirmed item is written and nothing unconfirmed is.

In an undocumented project, end this turn by asking the architect to approve the written text
of the "Record architecture decisions" ADR, and leave sections 2–8 and 11 empty until they do.
After the approval, recover the architecture as [references/recovery.md](references/recovery.md)
says; its report replaces section 4.

## 4. Report

List the files written, the legacy ADRs upgraded (still `accepted (legacy)`), the open
questions (unmeasured goals, anything the architect left unanswered), and the "Record
architecture decisions" ADR, by its number, waiting for the architect's approval of its text,
with what waits for it: work on any decision on its list.

| Thought | Reality |
|---|---|
| "Set up the architecture means scaffold the code" | Setup writes the architecture documents. Code is ordinary work after the "Record architecture decisions" ADR is accepted. |
| "The architect gave the requirements, so I'll write the R-list now" | The triage is a proposal until they confirm it. Turn one writes the skeleton only. |
| "The README's architecture section belongs in arc42, I'll move it over" | Link it from the arc42 section. The README stays as it is. |
| "I'll pick the storage engine now so the docs are complete" | Storage is a decision made centrally: it goes on the "Record architecture decisions" list and gets its own ADR later. |
| "They said 'confirmed', so the new ADR is accepted" | They confirmed your proposals. The ADR is `proposed` until they approve its written text. |
| "The architect approved ADR-0001, so the recovered ADRs are approved too" | The approval covers ADR-0001's text. Each recovered ADR is `proposed` until the architect approves it. |
| "The code clearly decided this, so I'll mark it accepted" | Found is not decided. Recovered content carries *as found, unconfirmed* and recovered ADRs stay `proposed`. |
