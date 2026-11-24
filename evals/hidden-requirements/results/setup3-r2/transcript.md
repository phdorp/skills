## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the skeleton at `docs/architecture/arc42.md`, the only file this turn. Nothing else is written until you confirm.

## Proposal

**Situation:** fresh project. There is no source and no architecture documentation, only the idea in the README.

**Triage:** the README names four needs. The R-list is empty, so only the outcome applies.

| need from README | proposed outcome | reason |
|---|---|---|
| Coaches check kit out and back in, and each check-out is recorded | **R-1, system-level, active:** "Coaches check items out and back in; every check-out and check-in is recorded." | Shapes the core data and the interface. |
| Know which coach has what, and where everything is | **R-2, system-level, active:** "Anyone can see which coach holds each item and what is in the store." | Shapes the query side of the records. |
| It should be easy to use | **R-3, system-level, active:** "A coach can check an item out or in without training." | Drives the interface platform. The measure is still open (see below). |
| Balls, bibs, cones, first-aid bags | **feature-level** under R-1: item types, with an issue citing R-1 | Fits inside R-1; no R-row. |
| "A small tool" | **proposed constraint for section 2**, not an R-row: one club, a few hundred items, maintained by one volunteer | A limit on the solution, not a quality requirement. Confirm the numbers in Q3 and Q7. |

No duplicates or conflicts exist yet, since the R-list is empty.

**Rank (proposed):**
1. R-1 (check out and in): it is the core of the tool.
2. R-2 (who has what): it is the stated problem, and it depends on R-1's records.
3. R-3 (easy to use): it constrains how R-1 and R-2 are delivered.

Near-tie R-1 / R-2. Tie-breaker: **if only one of R-1 and R-2 can be fully met, which?**

**Quality goal candidates** (none is a goal yet: no measure is known):
- **Functional suitability: functional correctness** (from R-1). Scenario: a coach checks out three balls; the records show those three balls under that coach. *Open question:* what share of check-outs may be wrong per season, and what is acceptable?
- **Interaction capability: learnability** (from R-3). Scenario: a coach who has never used the tool checks an item out alone. *Open question:* how long, and how many steps or taps, count as "easy"?
- **Security: accountability** (from R-2). Scenario: every check-out is traceable to the coach who made it. *Open question:* must the record also show who made the change, or only who holds the item?

No reliability or security goal is proposed yet. Those depend on your answers to Q2 and Q11.

**Decisions made centrally** (draft for the "Record architecture decisions" ADR, `docs/adr/0001-record-architecture-decisions.md`, status `proposed`, not yet written):
- Decided centrally:
  - where the records live: storage engine and the format of check-out data;
  - import and export format for the item list, if one is planned;
  - interfaces between building blocks, and the dependency rule;
  - conventions: item identifiers and naming, units (counts), error handling, logging;
  - third-party dependencies that lock the project in.
- Left to building blocks: internal helpers, screen layout, test layout.
- Dropped for now: versioning, since no API or CLI is planned yet.

## Interview, round 1

❓ **Q1** - **Users and devices**: How many coaches use the tool, and on what: their own phones, a shared device, or a laptop at the clubhouse?

➡️ Their own phones, at the pitch.

❓ **Q2** - **Connectivity**: Is there mobile signal at the pitch and the clubhouse?

➡️ Often not at the pitch, so a check-out must still work there.

❓ **Q3** - **Volume**: How many items of each kind, and how many check-outs a week in season?

➡️ A few hundred items in total, tens of check-outs a week, slow growth.

❓ **Q4** - **First version**: What must v1 do, and what can wait?

➡️ v1: check out, check in, see who holds what and what is in the store. Later: overdue reminders, condition, repairs.

❓ **Q5** - **Non-goals**: What must the tool never do?

➡️ Hold player or parent data; handle money.

❓ **Q6** - **Platform and cost**: Where should it run, and what may it cost?

➡️ No hardware the club has to buy; free hosting tiers only.

❓ **Q7** - **Builders**: Who builds and maintains it, and with what skills?

➡️ You, with a volunteer helper. It must be simple enough for one person to maintain.

❓ **Q8** - **Data and law**: What does it keep (coach names, contacts), for how long, and which law applies?

➡️ Coach name only; delete it when the coach leaves the club; GDPR applies.

❓ **Q9** - **Deadline**: By when must it be live?

➡️ Before the start of next season.

❓ **Q10** - **Exchanges**: Does it exchange data with other systems (a membership list, a calendar)?

➡️ No.

❓ **Q11** - **Missing qualities**: Did you leave out reliability (no signal at the pitch), or security (who may change a record)?

➡️ Reliability: a check-out must not be lost without signal. Security: only the equipment manager may edit or delete records.

## What I need from you

1. Confirm or change the triage, the rank, the tie-breaker, and the constraint for section 2.
2. Confirm or change the goal candidates and give a measure for each open question.
3. Confirm or change the ADR draft list.
4. Answer Q1–Q11.

ADR 0001 is not written yet, so section 9 of arc42 names its path but has no link to it. The skeleton is the only file written.

## ARCHITECT

1. **Triage, rank, constraint:** Fine, with corrections. Rank R-1, then R-2, then R-3. If only one can be met, R-1. For section 2, the numbers are about 40 coaches and 300 items. Performance is not a concern. The only maintainer is one volunteer who knows Python only, and a successor must be able to take it over.

2. **Goals:**
   - **Learnability (R-3):** Checking out an item takes at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag.
   - **Correctness:** No preference on the error share. Wrong check-outs should be rare and correctable.
   - **Accountability:** Yes, record who made each change, not only who holds the item.
   - **Reliability:** Check-out and check-in must work offline at the pitch and sync when the phone is back online.

3. **ADR draft list:** Fine. The yearly inventory export as CSV for the treasurer's insurance audit belongs under the import/export format.

4. **Answers to Q1–Q11:**
   - **Q1:** Fine. Coaches use their own phones at the pitch.
   - **Q2:** Fine.
   - **Q3:** Correction: about 40 coaches and 300 items. No performance concern.
   - **Q4:** Correction: v1 also needs the overdue report e-mailed to the kit manager every Monday morning, and a warning 30 days before expiry dates on first-aid bag items. Condition and repairs can wait.
   - **Q5:** Correction: the only non-goal I have is no money handling: no deposits, fines or payments.
   - **Q6:** Correction: it must run on the club's existing Synology NAS (Docker is available). The budget is 0 EUR per month. No third-party cloud, because the data must stay on the club's own hardware.
   - **Q7:** Correction: the only maintainer is one volunteer who knows Python only. A successor must be able to take it over.
   - **Q8:** Correction: it keeps coaches' names and phone numbers, which is personal data under GDPR. History of lost items must be kept for 2 years for insurance.
   - **Q9:** Correction: it must be live for the start of the season on 1 March.
   - **Q10:** No.
   - **Q11:** Reliability: as in point 2. Security: only the equipment manager may edit or delete records. That's fine with me.

## DESIGNER

Thanks. Your corrections are in. I haven't written any files this turn, since the new needs still need triage and some questions are open. Here is the updated proposal.

## 1. Confirmed, and the new needs

**Constraints for arc42 section 2:**
- Runs on the club's existing Synology NAS, in Docker.
- Budget 0 EUR per month; no third-party cloud; data stays on club hardware.
- Scale: about 40 coaches and 300 items. No performance goal.
- Maintained by one volunteer who knows Python only. A successor must be able to take it over.
- Live by 1 March 2027, the start of the season.
- Lost-item history is kept for 2 years (insurance). Coach names and phone numbers are personal data under GDPR.

**Out of scope for arc42 section 3:** money (no deposits, fines or payments); condition and repairs (later); player or parent data.

**Stakeholders (section 1):** the kit manager, who edits and deletes records; the coaches, about 40; the treasurer, who takes the yearly export. I take the kit manager to be your role. Please confirm.

**New triage (proposed outcomes):**

| need | proposed outcome | reason |
|---|---|---|
| Check-out and check-in work offline at the pitch and sync later | **R-4, system-level, active:** "Check-out and check-in work without network and sync when the phone is back online." Rank 4 (proposed). | Shapes local storage and sync. Reliability goal. |
| Overdue report e-mailed to the kit manager every Monday morning | **R-5, system-level, active:** "Every Monday morning the overdue report is e-mailed to the kit manager." Rank 5 (proposed). | Outbound mail and a schedule cross a boundary. |
| Warning 30 days before expiry dates on first-aid items | **feature-level** under R-5: an issue citing R-5 | Same report mechanism. |
| Only the kit manager may edit or delete records | **R-6, system-level, active:** "Only the kit manager may edit or delete records." Rank 6 (proposed). | Authorisation shapes the architecture. |
| Yearly inventory export as CSV for the treasurer's insurance audit | **R-7, system-level, active:** "The treasurer can export the yearly inventory as CSV for the insurance audit." Rank 7 (proposed). | Export format is a central decision. |
| Successor can take over maintenance | **R-8, system-level, active:** "A Python developer who did not build the tool can maintain it." Rank 8 (proposed). | Drives maintainability goal. |

No duplicates. Conflicts:
- **R-3 vs accountability:** naming the coach on each change may add taps, which conflicts with 3 taps.
- **R-4 vs R-6:** an offline edit by a phone that is not the kit manager's must be refused after sync.

Rank: R-1, R-2, R-3 as you set; R-4 to R-8 proposed. Tie-breaker for the conflict: **if only one of "3 taps" and "every change names the coach" can be fully met, which?**

## 2. Quality goals (now with measures where given)

- **QG-1 Functional suitability: functional correctness** (R-1, R-2). Correctable. No error-share preference. *Open question:* what would show a wrong check-out is correctable? Proposed measure: the kit manager or the coach fixes a wrong record in at most 2 taps, and every correction stays in the history.
- **QG-2 Interaction capability: learnability** (R-3). Measure given. Draft scenario:
  - **QS-1:** a coach who has used the tool before checks out a bag by scanning its QR code. Response: recorded. Measure: at most 3 taps and at most 15 seconds.
- **QG-3 Security: accountability** (R-2, R-6). *Open question:* what measure? Proposed: every change record names a coach; 0 unattributed changes in the audit log in tests.
- **QG-4 Reliability: fault tolerance** (R-4). *Open question:* measures? Proposed: 100% of check-outs succeed in airplane mode; records reach the NAS within 5 minutes after reconnect.
- **QG-5 Security: integrity** (R-6). *Open question:* measure? Proposed: a non-manager edit or delete is refused in 100% of tests.
- **QG-6 Maintainability: analysability** (R-8). *Open question:* measure? Proposed: a Python developer who did not build the tool finds and fixes a seeded bug within a set number of hours.

## 3. Decisions made centrally (draft ADR 0001, still `proposed`)

- Storage: where records live, the check-out data format, and the phone-to-NAS sync protocol and conflict rules.
- Import and export formats, including the yearly CSV for the treasurer.
- Interfaces between building blocks and the dependency rule.
- Crosscutting conventions: identifiers, units, error handling, logging.
- Third-party dependencies and hosting on the NAS in Docker.
- Versioning: dropped for now.

## 4. Interview, round 2

❓ **Q12** - **Offline conflicts**: If two phones check out the same item while offline, which record wins?

➡️ Keep both records and let the kit manager resolve the clash.

❓ **Q13** - **Coach identity**: How does the phone know which coach is acting, without an extra tap per check-out?

➡️ Each phone is set up once with the coach's name; no login per check-out. Otherwise the 3-tap goal fails.

❓ **Q14** - **Personal data**: Who may see coaches' phone numbers?

➡️ Only the kit manager. Coaches see only the holder's name on an item.

❓ **Q15** - **Correction measure**: Is "a wrong record is fixed in at most 2 taps by the kit manager or the coach, with history kept" the measure you want for correctability?

➡️ Yes.

❓ **Q16** - **Offline measures**: Is "100% of check-outs work in airplane mode; records reach the NAS within 5 minutes of reconnect" the measure you want?

➡️ Yes.

❓ **Q17** - **Monday e-mail**: Does the club have a mail account the tool may send through, or is that a third-party service?

➡️ The club's existing mail account; no new paid service.

❓ **Q18** - **Retention**: How long are records of coaches who have left kept? The loss history is kept 2 years.

➡️ Coach names are removed when they leave; the item history stays 2 years.

❓ **Q19** - **Expiry dates**: Which items carry expiry dates, and who enters them?

➡️ First-aid bag items only, entered by the kit manager.

❓ **Q20** - **Maintenance**: What must a successor find in place?

➡️ A README and automated tests that run with Python, so a new maintainer can check changes.

## What I need from you

1. Confirm R-4 to R-8 and their ranks, and the conflict tie-breaker.
2. Confirm the constraints and out-of-scope items above.
3. Confirm or change the measures for QG-3 to QG-6, and the draft QS-1.
4. Answer Q12–Q20.

Once these are answered, I write the confirmed rows, goals and ADR 0001 to the files.

## ARCHITECT

1. **R-4 to R-8 and ranks:** Confirmed, ranks fine. Tie-breaker: 3 taps wins. The phone is set up once with the coach's name, so naming the coach should not add taps. I am the kit manager, so the stakeholder entry is right.

2. **Constraints and out-of-scope:** Confirmed. Condition and repairs can wait. Money stays out.

3. **Measures:**
   - **QG-3, QG-4, QG-5, QG-6:** Approved as proposed. For the seeded bug in QG-6, I have no preference on the number of hours.
   - **QS-1:** One correction. Many of our volunteers are not tech-savvy, so the 3 taps and 15 seconds must hold for them too, with no training. It should not only cover coaches who have used the tool before.

4. **Answers:**
   - **Q12:** Fine. Keep both records and I resolve the clash.
   - **Q13:** Fine.
   - **Q14:** Fine. Only I see the phone numbers.
   - **Q15:** Correction. Only I, the kit manager, may edit or delete records, so coaches cannot fix records themselves. The 2-tap fix and the kept history are fine for me.
   - **Q16:** Yes.
   - **Q17:** Fine, as long as it costs nothing extra (0 EUR per month).
   - **Q18:** The loss history must be kept for 2 years for the insurance. I have no preference on how coach names are removed beyond that, as long as the history stays usable.
   - **Q19:** Yes. Only first-aid bag items carry expiry dates, and I enter them.
   - **Q20:** Fine. A README and automated tests that run with Python.

## DESIGNER

The architecture skeleton is written and the confirmed items are in it. One goal is still open, and the ADR that governs the rest awaits your approval.

## Files written

- **`docs/architecture/arc42.md`**
  - **Section 1:** the R-list (R-1 to R-8 active, ranked 1 to 8; R-9 deferred), goals QG-1 to QG-6, and stakeholders.
  - **Section 2:** constraints (NAS in Docker, 0 EUR, no third-party cloud, mail via the club account, scale, GDPR, 2-year history, 1 March 2027 deadline, maintainer knows Python only).
  - **Section 3:** out of scope, money only.
  - **Section 9:** a link to ADR 0001.
  - **Section 10:** QS-1 to QS-5.
- **`docs/adr/0001-record-architecture-decisions.md`**: status `proposed`. The decided-centrally list is the one you approved, with the yearly CSV export under import and export formats.
- **`.scratch/requirements/issues/01-item-types.md`** (feature under R-1) and **`02-expiry-warning.md`** (feature under R-5). There is no tracker config in the repo, so the `.scratch` fallback applies.

## Choices I made

- **R-9 "Condition and repairs" is recorded as deferred**, from your answer that it can wait. You didn't say it was a row, so tell me if you'd rather it not be there.
- **Player and parent data is not in out of scope.** Your correction to Q5 said money was the only non-goal, so I dropped the player and parent data item I had proposed.
- **QS-1 covers first-time volunteers** with no training, as you corrected.
- **Section 5 is empty.** Building blocks wait for the storage decisions.

## Open for you

1. **QG-6 has no measure.** You approved the goal, but you have no preference on the hours. Its row says "open" and it has no QS row. Pick a number for the seeded-bug test, or accept an example such as 4 hours, and I'll write QS-6.
2. **Goal order.** The goal table is in ID order. Tell me how you rank the goals, and I'll reorder it.
3. **ADR 0001** stays `proposed` until you approve its text. Until then the work on storage, sync, the CSV export and hosting waits, as the ADR says.
4. **Coach names after they leave.** You want the history kept usable without the names. That is a design question for the storage ADR, not a decision now.

## ARCHITECT

1. **QG-6:** 4 hours is fine. Write QS-6 with that.
2. **Goal order:** No preference. Keep ID order.
3. **ADR 0001:** Approved.
4. **Coach names after they leave:** Fine, leave it for the storage ADR. The 2-year loss history must stay usable.

Keeping R-9 as deferred is fine too.