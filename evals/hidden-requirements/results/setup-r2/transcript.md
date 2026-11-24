## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the skeleton at `docs/architecture/arc42.md`. It is the only file this turn touched. Below is my proposal. Nothing in the R-list or the goal tables is written until you confirm it.

**Triage** (the R-list is empty, so each requirement gets only an outcome)

| Proposed ID | Requirement (proposed wording) | Outcome | Reason |
|---|---|---|---|
| R-1 | A coach checks kit out to themselves and back in. | system-level | This is the core mechanism of the tool. |
| R-2 | The club always knows where each item is and which coach holds it. | system-level | This is the problem the README states. |
| R-3 | A coach can check kit out or in without a briefing. Sharper wording needed: "easy to use" has no measure yet. | system-level | It shapes the interface and platform. |
| (issue) | Kit categories: balls, bibs, cones, first-aid bags. | feature-level | It fits inside R-1 and R-2, so it gets an issue, not a row. |

**Rank (proposed, for you to set):** 1 R-1, 2 R-2, 3 R-3. R-1 is the mechanism R-2 depends on.

**Conflict:** R-3 may conflict with R-1 and R-2 if every check-out asks for many details. Tie-breaker: if only one of R-2 and R-3 can be fully met, which one?

**Quality goal candidates** (each needs a measure before it becomes a goal)
- Functional correctness (from R-2): the recorded holder matches reality. Open question: what share of items must match?
- Accountability, under Security (from R-2): every check-out traces to a coach. Open question: must it be identified by login, or is a name enough?
- Operability, under Interaction capability (from R-3): a coach checks out kit without help. Open question: how many seconds, and after how much training?

**Gap questions** (each asked once)
- Time behaviour: must a check-out work quickly on the sideline during a match?
- Interoperability: should the kit list or history be exported for the club?

**Where the documents map:** none. This is a fresh project.

**Legacy ADRs:** none.

**Decisions made centrally**, the draft for ADR 0001 "Record architecture decisions" in `docs/adr/`, status `proposed`:
- Centrally decided: storage engine and record format for kit and check-out history; export format, if you want export; interfaces between building blocks and the dependency rule; versioning of the data format once other tools read it; crosscutting conventions (naming, dates and times, error handling, logging); third-party dependencies.
- Left to the building blocks: internal helpers, code structure within one block, test layout.

Section 9 of the skeleton links to ADR 0001, which will exist once you confirm. The link stays dangling until then.

**Please confirm or change:** the R-IDs and outcomes, the rank, the tie-breaker answer, the goal candidates and their measures, the two gap questions, and the ADR 0001 draft list.

## ARCHITECT

1. IDs and outcomes: confirmed, including the categories as an issue.
2. Rank: R-1, R-2, R-3 is fine.
3. Tie-breaker: R-3 wins. If it's hard to use, volunteers won't do it, and then the records are wrong anyway.
4. Goal measures:
   - Correctness: no preference on the share.
   - Accountability: a name is enough, no login needed from my side.
   - Operability: checking out an item takes at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag. Many volunteers aren't tech-savvy, so no training should be needed.
5. Time behaviour: yes, it matters on the sideline. Coaches use phones at the pitch, where there is often no mobile signal. Check-out and check-in must work offline and sync once the phone is back online. Speed is the 15 seconds above. Otherwise performance isn't a concern.
6. Interoperability: yes. The treasurer needs a yearly inventory export as CSV for the insurance audit.
7. ADR 0001 draft list: confirmed.

## DESIGNER

The architecture skeleton is written and your confirmed answers are recorded. Two things need your decision before the architecture is settled: the tie-breaker contradicts the rank, and two goals still have no measure.

**Files written**
- `docs/architecture/arc42.md`: R-list rows R-1 to R-5, goals QG-1 to QG-3, scenarios QS-1 to QS-3.
- `.scratch/requirements/issues/01-kit-categories.md`: the kit-categories issue, citing R-1 and R-2. There is no `docs/agents/issue-tracker.md`, so I used the fallback path.
- `docs/adr/0001-record-architecture-decisions.md`: status `proposed`, with the ADR list you confirmed.

**Decision for you: rank vs. tie-breaker.** You set the order R-1, R-2, R-3, which puts R-3 last. You also said R-3 wins a conflict with R-2. Those contradict each other, so I recorded both as you gave them. Should R-3 move above R-2?

**New requirements from your answers.** I took the answers to the time-behaviour and interoperability questions as new system-level requirements and gave them active rows. The ranks 4 and 5 are my proposals. Please set the order.
- R-4: the treasurer exports a yearly CSV inventory.
- R-5: check-out and check-in work offline and sync later.

**Wording I wrote from your answers, please check**
- QS-3's measure, "100% of records carry a coach name", is my reading of "a name is enough".
- The R-4 and R-5 wording is mine.

**Goal impact (proposed as questions, no goal rows written)**
- R-5 implies availability, which no goal covers. Add QG-4 with this scenario: a phone loses signal during check-out at the pitch; the record is kept and reaches the shared record after reconnection. Measure: 100% of check-outs complete without signal. Open: what is the longest acceptable delay before a queued record syncs?
- R-4 implies interoperability, which no goal covers. Add QG-5 with this scenario: the treasurer exports the yearly inventory; the CSV lists every item and its holder. Open: what number or observation shows the export is complete?

**Open questions (goals without a measure)**
- Functional correctness (from R-2): you gave no preference on the share, so it still needs a measure. What observation would show a holder record is correct?
- Learnability: "no training" under R-3 has no measure. What would show a first-time volunteer can check out without help?

**Still open**
- Stakeholders are empty. The README names coaches, the treasurer, and the equipment manager; confirm them and I will write them.
- ADR 0001 waits for your approval of its text. Until then, work on the centrally decided items waits too: the storage engine and record format, the CSV export format, and the interfaces between building blocks.

## ARCHITECT

1. Yes, move R-3 above R-2. The order is R-1, R-3, R-2.
2. Offline matters more than the export, so R-5 goes ahead of R-4. The full order is R-1, R-3, R-2, R-5, R-4.
3. The QS-3 wording "100% of records carry a coach name" is fine. Your R-4 and R-5 wording is fine too.
4. QG-4 and QG-5: yes, add both.
   - QG-4: I have no preference on the sync delay. Once the phone is back online, it just needs to sync.
   - QG-5: the CSV lists every item and its holder. That's enough for me.
5. Correctness: no preference, your call on how to measure it.
6. Learnability: a first-time volunteer checks out an item by scanning the QR code in at most 3 taps and under 15 seconds, with no help and no training.
7. Stakeholders: confirmed. They are the coaches, the treasurer, and the equipment manager, which is me.
8. ADR 0001: Approved.

## DESIGNER

The architecture is set up. The R-list, goals, scenarios, stakeholders and ADR 0001 now match what you confirmed.

**Files**
- `docs/architecture/arc42.md`
  - R-list in the order R-1, R-3, R-2, R-5, R-4, with R-3 above R-2 as you asked.
  - Six goals, QG-1 to QG-6, each with its scenario QS-1 to QS-6.
  - Stakeholders: coaches, treasurer, equipment manager.
- `docs/adr/0001-record-architecture-decisions.md`: status `accepted 2026-11-23`, with the ADR list you confirmed.
- `.scratch/requirements/issues/01-kit-categories.md`: the kit-categories issue, citing R-1 and R-2.

**Choices I made, for you to check**
- **QG-6, functional correctness:** you left the measure to me. I used "in a full kit count, 0 items whose recorded holder differs from the holder found in the count." Tell me if you want a different measure.
- **QG-1 is learnability and operability together:** QS-1 carries the first-time-volunteer, no-help, at-most-3-taps measure, so the learnability requirement sits in one goal rather than a separate one.

Nothing is left open in the architecture. The next step is the building-block view in section 5. It stays empty until the centrally decided items are built, and they now are approved to build against. I have not committed these changes.

## ARCHITECT

1. QG-6 measure: fine, approved.
2. QG-1 covering learnability and operability together: fine, approved.

Approved.