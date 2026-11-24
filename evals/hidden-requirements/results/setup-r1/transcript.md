## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

The skeleton is written. Here is my proposal for you to confirm or change. Nothing else is written yet.

**Triage** (the R-list is empty, so only the outcome is open). These are candidates taken from the README; the wording is my proposal.

| candidate requirement | findings | proposed outcome | reason |
|---|---|---|---|
| Coaches check kit out to themselves and back in | none (first row) | system-level | It creates the holder records the rest depends on, so it shapes the data model. |
| The club can see at any time which coach holds each item, and where unheld items are | conflicts with nothing yet | system-level | It is the purpose of the tool; the record it needs shapes storage and the data format. |
| A coach can check kit out or in without help or training | conflicts with the first row: every extra field or step at check-out works against it | system-level | It decides the interface channel (phone or laptop at the pitch) and how many steps a check-out takes. |
| Item types: balls, bibs, cones, first-aid bags | none | feature-level, parent R-1 | It is catalogue content inside check-out; no architecture impact by itself. |
| "A small tool" | none | not an R-row; a section 2 constraint question | It needs a number (users, items, devices) before it can be a constraint. |

**Rank (proposed, you set the order):** 1 (proposed) R-1, 2 (proposed) R-2, 3 (proposed) R-3, because R-1 produces the records that R-2 reports on.
Conflict: R-1 vs R-3. Tie-breaker: "if only one of R-1 and R-3 can be fully met, which?"

**Quality goals** (candidates, not yet written):
- Functional suitability: functional completeness, from R-1 and R-2. Open question: "what would show R-2 is met?" (for example, "after every check-out or check-in the recorded holder is correct"). I have no number, so this stays open.
- Interaction capability: operability and learnability, from R-3. Candidate scenario:
  - source: a coach who has not used the tool before
  - stimulus: checks out one item
  - environment: normal use at the pitch, on a phone
  - response: completes it without asking for help
  - measure: [N] of [M] first-time coaches succeed unaided, and each takes under [S] seconds. Please give N, M and S.

**Gap questions** (one list, each asked once):
- Security, authenticity: can a coach check out for someone else, or does each coach log in?
- Security, accountability: does the club need to know who recorded a check-out, for disputes?
- Recoverability: if the records are lost, is it acceptable to start again, or must history survive?
- Compatibility, interoperability: must it import an existing kit list or export to a spreadsheet?
- Adaptability: which devices will coaches use, phone only or also a laptop?

**Where your documents map:** none. The project has no existing architecture documents, and there are no legacy ADRs.

**Decisions made centrally** (draft list for the "Record architecture decisions" ADR, which will be `docs/adr/0001-record-architecture-decisions.md`):
- storage engine and data format for holder and location records;
- interfaces between building blocks, and the dependency rule between them;
- third-party dependencies (framework, hosting);
- import and export formats, if any are confirmed;
- crosscutting conventions: naming, dates and time zone (units), error handling.

Left to building blocks: UI layout, internal helpers, test layout.

**What I wrote:** only `docs/architecture/arc42.md`, with the twelve sections and the empty tables. Sections 9 and 12 hold plain text for now, since the ADR and `GLOSSARY.md` don't exist yet.

Please confirm or change:
1. Are the three candidate requirements right, and is "small tool" a constraint rather than a row?
2. Is the rank order right, and what is your answer to the R-1 vs R-3 tie-breaker?
3. Which quality goals should be written, and what are the numbers for the interaction scenario and the R-2 measure?
4. Answers to the gap questions.
5. Is the draft decision list for the ADR right?

## ARCHITECT

1. Yes, the three are right. "Small tool" is a constraint: about 40 coaches and 300 items. Performance is not a concern.

2. The rank order is fine. The tie-breaker is R-3. Many volunteers aren't tech-savvy, so checking out must take at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag.

3. Write both goals. For the interaction scenario I'd use N = 9 of M = 10 first-time coaches, and S = 15 seconds with at most 3 taps. Your R-2 measure ("after every check-out or check-in the recorded holder is correct") is fine.

4. Gap answers:
   - **Authenticity:** no preference. A coach only checks out kit to themselves.
   - **Accountability:** yes. We must keep the history of lost items for 2 years for the insurance.
   - **Recoverability:** history must survive, at least those 2 years.
   - **Interoperability:** the treasurer needs a yearly inventory export as CSV for the insurance audit. No preference on import.
   - **Devices:** coaches use phones at the pitch, where there is often no mobile signal. Check-out and check-in must work offline and sync when the phone is back online.

5. The decision list is right. For third-party dependencies and hosting:
   - It must run on our existing Synology NAS, which has Docker.
   - The budget is 0 EUR per month.
   - Coaches' names and phone numbers are personal data (GDPR), so data must stay on the club's own hardware, with no third-party cloud.
   - The only maintainer knows Python only, and a successor must be able to take it over.

## DESIGNER

The confirmed parts are written. Your gap answers also raise new requirements, and those need your outcome before I write them. One ranking point also needs a decision from you.

## Written

- **`docs/architecture/arc42.md`**
  - Section 1: R-1, R-2 and R-3 as active system-level rows, ranked 1, 2 and 3. QG-1 (functional correctness, from R-1 and R-2) and QG-2 (learnability, from R-3).
  - Section 2: the constraints from your answers: Synology NAS with Docker, 0 EUR per month, all personal data on club hardware, Python only with a successor able to take over, and the size (about 40 coaches, 300 items).
  - Section 9: a link to the ADR below.
  - Section 10: QS-1 (the recorded holder is correct after every check-out or check-in) and QS-2 (9 of 10 first-time coaches check out unaided in at most 3 taps and under 15 seconds).
- **`docs/adr/0001-record-architecture-decisions.md`**: status `proposed`. The decision list is adjusted to your answers: storage and data format, CSV export, interfaces, dependencies (including Docker on the NAS and Python), and naming, dates and error handling. It waits for your approval of its text.
- **`.scratch/requirements/issues/01-item-types.md`**: a feature-level issue for the four item types (balls, bibs, cones, first-aid bags), citing R-1. There is no tracker config in the repo, so it went to `.scratch/`.

Stakeholders in section 1 stay empty because you didn't answer about them. Section 5 and section 11 are empty as well.

## Needs your decision

**Rank conflict.** You confirmed the order 1 R-1, 2 R-2, 3 R-3, but you named R-3 as the winner of the R-1 vs R-3 tie-breaker. Those two answers point in opposite directions. Which one holds?

**New requirements from your gap answers.** These go through triage, so I haven't written any of them. My proposed outcomes:

| candidate | findings | proposed outcome |
|---|---|---|
| A coach checks out only to themselves | repeats R-1 | no new row |
| How a coach identifies themselves at check-out | not covered; needed for A | question: how do coaches identify themselves? A QR scan identifies the bag, not the coach. |
| Check-out and check-in history kept 2 years and survives failures | your accountability and recoverability answers describe one history | one system-level row. Coach names kept for 2 years also raise a GDPR storage-limit question. |
| Yearly CSV inventory export for the treasurer | none; export format is on the central decision list | system-level |
| Check-out and check-in work offline and sync when back online | conflicts with R-2's "at any time" | system-level, and R-2's wording needs your sharpening |

Please confirm or change each outcome, and answer the identification question. Once you confirm the system-level rows, I'll run goal impact. Expected: offline strains QG-1 while unsynced, and no goal covers availability or recoverability yet, so I'll propose goals with scenarios for those.

Nothing is committed.

## ARCHITECT

1. **Rank:** the tie-breaker holds. R-3 (check-out without help) wins over R-1. Please rank R-3 first, then R-1, then R-2.

2. **New requirements:**
   - "Coach checks out only to themselves": no new row, agreed.
   - **Identification:** no preference on how. It must fit inside the 3 taps and 15 seconds, so nothing that makes volunteers type a password every time.
   - **2-year history:** yes, one system-level row. Keeping coach names for the 2 years is fine, since that is what the insurance needs.
   - **Yearly CSV export:** yes, system-level.
   - **Offline check-out and check-in with sync:** yes, system-level. For R-2, "at any time" can mean "as of the last sync". Sharpen the wording that way.

3. Goal impact: go ahead and propose the goals with scenarios for availability and recoverability.

4. The ADR text is approved.

## DESIGNER

The ranks and new rows are written, and the ADR is accepted. Goal impact is proposed below, and nothing in the goal tables has changed.

## Written

- **R-list** in `docs/architecture/arc42.md`:
  - Ranks are now R-3 = 1, R-1 = 2, R-2 = 3, as you ordered.
  - R-2 now reads "as of the last sync", as you asked.
  - New active rows: R-4 (identification, no password per check-out), R-5 (2-year history with coach names, surviving failures), R-6 (yearly CSV export for the treasurer), R-7 (offline check-out and sync).
  - R-4 to R-7 have proposed ranks, 4 to 7, which you still need to set.
- **Section 9** now says the ADR is accepted 2026-11-23.
- **ADR 0001** Status is `accepted 2026-11-23`. Its text is unchanged.

Stakeholders are still empty, and I didn't write any goal rows.

## Goal impact (proposed, not written)

- **R-7 offline strains QG-1.** The QS-1 measure, "after every check-out or check-in the recorded holder is correct", can't hold while a phone is unsynced. Proposed measure: "after every sync, the recorded holder is correct". Do you accept it?
- **Availability (no goal covers it).** Proposed QG-3, Reliability: availability.
  - Source: a coach at the pitch with no signal.
  - Stimulus: checks out one item.
  - Environment: offline, normal operation.
  - Response: the check-out is accepted on the phone and shows as held.
  - Measure: every offline check-out completes within the QS-2 limit of 3 taps and 15 seconds. Is that 100%, or what share?
- **Recoverability (no goal covers it).** Proposed QG-4, Reliability: recoverability.
  - Source: a power cut, or a restart of the NAS.
  - Stimulus: power is lost during a check-out or a sync.
  - Environment: normal operation.
  - Response: every confirmed record is intact after restart, and the 2-year history is complete.
  - Measure: zero lost confirmed records in N power-cut trials. What is N?

## Open questions

- **Authenticity (R-4):** no goal covers it. Should there be one, and what would show that a coach's identity is proven?
- **Accountability (R-5, with coach names):** should the history have its own goal?
- **Export (R-6):** what would show the CSV is right for the audit? For example, its totals match the inventory on the day.
- **Ranks for R-4 to R-7:** please set their order.

## ARCHITECT

1. **R-7 measure for QS-1:** accepted. "After every sync, the recorded holder is correct" is fine.

2. **QG-3 availability:** yes, 100%. Every offline check-out should finish within 3 taps and 15 seconds.

3. **QG-4 recoverability:** no preference on N. Your call, 10 trials is fine with me.

4. **Authenticity (R-4):** no separate goal. It is enough that identification fits inside the 3 taps and 15 seconds.

5. **Accountability (R-5):** no separate goal. Keeping the 2-year history under QG-4 is enough.

6. **Export (R-6):** yes. The CSV is right if its totals match the inventory on the day.

7. **Ranks:** R-7 = 4, R-4 = 5, R-5 = 6, R-6 = 7. Offline use and identification matter most for the volunteers at the pitch. The export is only needed once a year.

## DESIGNER

Everything you confirmed is written in `docs/architecture/arc42.md`. No code, commits or other files were touched.

**Ranks (sections 1):** R-3 = 1, R-1 = 2, R-2 = 3, R-7 = 4, R-4 = 5, R-5 = 6, R-6 = 7. The "(proposed)" markers are gone.

**Quality goals and scenarios:**
- QG-1 (functional correctness) now comes from R-1, R-2 and R-7. QS-1 measure: "after every sync, the recorded holder is correct".
- QG-2 (learnability, QS-2) is unchanged.
- QG-3 (availability, from R-7), QS-3: offline check-outs with no signal, 100% within 3 taps and 15 seconds.
- QG-4 (recoverability, from R-5), QS-4: power cut during a check-out or sync, 0 lost confirmed records in 10 trials.

**Not written as goals:** authenticity (R-4) and accountability (R-5) get no separate goal. Your answers cover them through QS-2 and QS-4.

**Open:** the export measure (R-6: the CSV is right if its totals match the inventory on the day) has no goal to live under. Should I add an interoperability goal and scenario for it, or does it stay as a note for now?

## ARCHITECT

Yes, add it as a goal with a scenario. The measure stays as I said: the CSV is right if its totals match the inventory on the day. It's needed once a year for the insurance audit, so a low rank is fine.

## DESIGNER

I added the export as goal QG-5 with its scenario QS-5, in `docs/architecture/arc42.md`.

- **QG-5** (Compatibility: interoperability), from R-6. ISO 25010 puts the exchange of information with other systems under interoperability, which is how I classified it. Tell me if you'd rather file it elsewhere.
- **QS-5:** the treasurer exports the yearly inventory as CSV for the insurance audit. Measure: the CSV totals match the inventory on the day.
- R-6 keeps rank 7.

Nothing else changed.

## ARCHITECT

Filing it under interoperability is fine with me. Approved.