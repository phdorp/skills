---
name: quality-requirements
description: Load before interviewing the architect for requirements, ranking requirements, deriving or changing quality goals or quality scenarios (ISO/IEC 25010), or checking how a new requirement affects them.
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
of them. A bare number in the `rank` column is the architect's order. Until they set it, a new row's
rank cell holds your proposal as `4 (proposed)`, and your report asks them to set the order.

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

## Interview

A brief holds the requirements the architect thought of; the architecture also has to serve
the ones they did not write down. Interview them in rounds until nothing about the
requirements is silently assumed.

1. Read what you were given (the brief, the README, existing documents). Ask nothing it
   already answers.
2. Ask the **frontier**: every open question whose prerequisites are settled. A question that
   depends on an answer you have not heard waits for a later round. The first round covers
   this territory, in the product's own terms:
   - who uses it, how many of them, where, and on what (devices, connectivity, skills);
   - how much it holds and handles (records, files, requests), now and in a few years;
   - what the first version must do, and what can wait;
   - what it must never do (non-goals);
   - where it runs and what it may cost (platform, hosting, budget, licences);
   - who builds and maintains it, and with which skills;
   - what data it keeps, whose, for how long, and which law or contract applies;
   - the date it must be live by;
   - the systems and people it exchanges data with;
   - each 25010 characteristic no requirement supports that the product could plausibly need:
     "did you leave out something like <characteristic, with a one-line example>?"
3. Format each question as below, numbered on across rounds, and word it so "yes" accepts your
   recommendation. The recommendation is a proposal the architect corrects; it becomes a
   requirement only when they confirm it. A "did you leave out" question carries no
   recommendation: whether the product needs that characteristic is the architect's call.

   ```
   ❓ **Q1** - **<title>**: <question>

   ➡️ <your recommended answer>
   ```

4. Sort each answer: a need is a new requirement and gets a triage outcome in your next
   message (`add-requirements` step 1); a constraint (platform, budget, date, mandated
   technology, law) is proposed for arc42 section 2; a non-goal for section 3 as out of scope;
   a person or role for the stakeholders in section 1; a figure (users, records, load) for the
   scenario it measures, or else section 3; a characteristic the architect rules out ("speed is
   no concern") as a line under the quality goals, with their reason.
5. Recompute the frontier from the answers and ask the next round.

Choosing technology (storage engine, framework, hosting product) is not part of the interview:
it is a decision made centrally, taken later in its own ADR. Ask about technology only as a
constraint the architect already has ("must it run on hardware the club owns?").

Done when the frontier is empty or the architect says nothing is missing: every territory item
asked about once, every answer sorted.

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
| "The brief lists the requirements, so I only need to triage them" | The brief lists what the architect thought of. Ask the interview territory once. |
| "They accepted my recommendations, so I'll recommend Flask and SQLite too" | Technology is decided centrally, later, in its own ADR. The interview asks only for constraints. |
