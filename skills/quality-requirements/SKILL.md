---
name: quality-requirements
description: Load before ranking requirements, deriving or changing quality goals or quality scenarios (ISO/IEC 25010), or checking how a new requirement affects them.
---

# Quality Requirements

The architect owns the requirements and the quality goals; you propose, they decide. Each
procedure below ends with a proposal and a question. A file changes only for what the
architect has confirmed in this conversation.

## Where they live

All three tables sit in `docs/architecture/arc42.md`. IDs never change meaning: a new entry
takes the next free number, and an entry the architect drops keeps its ID with a status.

| table | section | columns |
|---|---|---|
| Requirements overview (the R-list) | 1 | `ID \| requirement \| rank \| status \| reason` — status `active`, `deferred` or `rejected`; deferred and rejected rows stay, with the architect's reason |
| Quality goals | 1 | `ID \| goal (ISO/IEC 25010) \| from \| scenario` — `QG-n`, characteristic and sub-characteristic, the R-IDs it comes from, its `QS-n` |
| Quality scenarios | 10 | see [references/quality-scenario.md](references/quality-scenario.md) |

The R-list's wording is the architect's. Sharpening a requirement is a proposal you show
them, never an edit you make.

Deciding which new requirements enter the R-list (duplicate, consistency and direction checks,
the four outcomes) is the `add-requirements` triage; at setup the first requirements go
through the same triage.

## Rank

1. Propose an order of the active requirements, one line of reason each.
2. Name every conflict between two requirements by their IDs.
3. For each conflict or near-tie, ask a pairwise tie-breaker: "if only one of R-3 and R-7 can
   be fully met, which?"
4. Ask the architect to set the order. Use no scoring scheme (MoSCoW, weights) unless they ask.

Done when the architect has the proposed order, every conflict, and the tie-breakers in front
of them. The `rank` column changes only to the order they set; until then a new row's rank is
your proposal, marked as such in your report.

## Derive goals

1. For each ISO/IEC 25010 characteristic the active requirements imply, write a candidate goal:
   characteristic and sub-characteristic ([references/iso-25010.md](references/iso-25010.md)),
   citing the R-IDs it comes from. A characteristic with no R-ID behind it is not a candidate.
2. Give each candidate a scenario in the template of
   [references/quality-scenario.md](references/quality-scenario.md).
3. A candidate whose measure you cannot state is an **open question** to the architect ("what
   would show that R-2 is met?"), not a goal.
4. Ask the architect to confirm and rank the top 3–5.
5. Write only the confirmed goals and scenarios, as `QG-n` in section 1 and `QS-n` in
   section 10, in the architect's order.

Done when every implied characteristic is either a confirmed goal with a measured scenario or
an open question in your report.

## Gap question

For each 25010 characteristic that no requirement supports and that the product could
plausibly need, ask: "did you leave out something like <characteristic, with a one-line
example for this product>?" The answer is the architect's; a new requirement it produces goes
through `add-requirements`.

Done when each such characteristic has been asked about once, in one list.

## Goal impact

Run it after the architect confirms a new system-level requirement.

1. Name the quality goals the requirement strengthens and the ones it strains, by `QG-n`.
2. When no goal covers its characteristic, or a measure no longer fits, propose the new goal
   or changed measure with its scenario, as a question: "R-6 implies Security:
   confidentiality, which no goal covers. Add QG-4 with this scenario?" A missing measure is
   an open question, as in Derive goals.
3. Leave the quality-goal and scenario tables as they are; they change after the architect
   answers.

Done when your report lists, for the new requirement, the goals it touches and each proposed
goal or measure as an open question.

| Thought | Reality |
|---|---|
| "The new requirement obviously needs a security goal, I'll add QG-4" | Propose it with its scenario and ask. The goals are the architect's. |
| "No measure yet, I'll write 'fast' and fix it later" | A goal without a measure is an open question, never a row. |
| "The architect gave no rank, I'll append the row at the bottom as final" | Propose a rank, mark it proposed, and ask them to set the order. |
| "This requirement's wording is sloppy, I'll tidy it while I'm here" | Show the sharper wording as a proposal; the row stays as the architect wrote it. |
