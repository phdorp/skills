## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the skeleton at `docs/architecture/arc42.md`. Nothing else is written yet. Here is my proposal for your confirmation.

## Skeleton

`docs/architecture/arc42.md` has all twelve sections and the empty tables for sections 1, 5 and 10. Section 9 points to `../adr/`, which does not exist yet. Section 12 has the "GLOSSARY.md is created with the first resolved term" line. I did not link the "Record architecture decisions" ADR because it is not written yet.

## Triage (against an empty R-list)

| Req | Requirement (draft wording) | Findings | Proposed outcome | Reason |
|---|---|---|---|---|
| A | Coaches check kit out and back in, so the club always knows where each item is. | none | system-level | Core of the product; shapes the data and the access model. |
| B | Each checkout records which coach took or returned the item. | conflicts with D (see below) | system-level | "Nobody knows which coach has what" is its own need: accountability. Could be folded into A if you prefer. |
| C | Balls, bibs, cones and first-aid bags are tracked as kit items. | none | feature-level, under A | A kind of item inside A, not architecture-shaping. Would be an issue citing A once A is confirmed. |
| D | Easy to use. | none | system-level | Cross-cutting: shapes the screens and the sign-in. Has no measure yet (see goals). |

Duplicates: none. Direction checks: no goals or ADRs exist yet.

## Rank (proposed)

1. R-1 check in/out: the core need.
2. R-2 attribution per coach.
3. R-3 easy to use.

**Conflict:** R-2 and D (easy to use) can pull against each other, because identifying each coach adds sign-in friction.
**Tie-breaker:** if only one of R-2 and R-3 can be fully met, which?

The order above is a proposal; you set it.

## Quality goal candidates

- **QG-1, Functional suitability: functional correctness** (from R-1, R-2): the records match where the kit actually is. *Open question:* what would show this is met? For example, the share of items found where the records say, at a spot check.
- **QG-2, Interaction capability: operability and learnability** (from R-3): *Open question:* what would show that R-3 is met? For example, the time until a new coach checks an item out unaided.

No goal is written until you give a measure. Security and performance have no requirement behind them yet, so they are not candidates. The interview may change that.

## Decisions made centrally (draft ADR "Record architecture decisions", number 0001, `proposed`)

No ADR directory exists, so the number is 0001. Its draft list:

- Where the kit records are stored and their data format, including how a phone without signal syncs later.
- Export format for the kit list, if the committee needs one (drop it if Q9 says no).
- Interfaces between the parts (screens, records, access rules) and the dependency rule between them.
- Versioning: only if an export or API is decided; otherwise drop it.
- Crosscutting conventions: naming, dates and units, error handling, logging.
- Third-party dependencies: framework and hosting product.

Left to the building blocks: internal helpers, screen layout, test layout.

## Stakeholders (draft)

- The equipment manager (the person who wrote the README).
- Coaches, who use the tool.
- The club committee, who may read the records.

## Interview, round 1

❓ **Q1** - **Users and devices**: How many coaches will use it, on which devices, and with what technical skill?

➡️ About 20–30 coaches on their own phones, with basic phone skills.

❓ **Q2** - **Connectivity**: Do coaches have a mobile signal at the pitch and at the equipment store?

➡️ Often not reliably. Checkouts must still be recorded when offline and reach the club later. (This may become a new system-level requirement.)

❓ **Q3** - **Volume**: How many items and checkouts per week, now and in three years?

➡️ About 150 items and about 40 checkouts per week, doubling within three years.

❓ **Q4** - **First version**: What must the first version do, and what can wait?

➡️ Check out, check in, and see where each item is. Reminders, reports and history beyond the season wait.

❓ **Q5** - **Non-goals**: What must it never do?

➡️ It does not track players, payments or results, and it does not replace the club's membership system.

❓ **Q6** - **Personal data and law**: Which personal data is kept, for how long, and under which data-protection rules? Where is the club based?

➡️ Only coach names, no contact details or player data, deleted at the end of each season. Assuming the club is in the EU, GDPR applies.

❓ **Q7** - **Hosting and budget**: Where may it run, and what may it cost?

➡️ Free or near-free hosting, no paid servers, no budget beyond the club's own accounts.

❓ **Q8** - **Maintenance**: Who maintains it after launch, and with which skills?

➡️ One volunteer with basic web skills, who must be able to change it without a developer.

❓ **Q9** - **Integrations**: Does it exchange data with other systems or people?

➡️ Not in the first version. The committee reads the records on screen or as a printout.

❓ **Q10** - **Access**: Should only club coaches be able to change records, and should anyone be able to see where items are? (Checking for a characteristic you may have left out: Security: confidentiality.)

➡️ Only signed-in club coaches change records. Any coach may view where items are.

## Your confirmation

Please confirm or change:

1. The triage outcomes for A to D, and the rank order with the R-2/R-3 tie-breaker.
2. The quality goal candidates, and what measures they should have (QG-1, QG-2).
3. The draft ADR list and the stakeholders.
4. Your answers to Q1–Q10.

Which of these do you confirm, and what do you change?

## ARCHITECT

1. **Triage and rank:** Fine with A to D and the order. On the tie-breaker, I'd say easy to use wins. Checking out must take at most 3 taps and under 15 seconds by scanning a QR code on the kit bag, so identifying the coach has to fit inside that.

2. **Quality goals:** Yes to both.
   - QG-2: a checkout takes at most 3 taps and under 15 seconds, starting from a QR scan.
   - QG-1: your spot check is fine. Checkouts and check-ins must also work offline and sync later.
   - Security is a requirement, not an open question. Coaches' names and phone numbers are personal data under GDPR (see Q6).
   - Performance is not a concern.

3. **ADR list and stakeholders:**
   - The ADR list is fine, but don't drop the export. The treasurer needs a yearly inventory export as CSV for the insurance audit.
   - Add the treasurer and the single volunteer maintainer (and their successor) to the stakeholders.

4. **Answers to Q1 to Q10:**
   - **Q1:** Wrong numbers. There are about 40 coaches, on their own phones. Many volunteers are not tech-savvy.
   - **Q2:** Confirmed. There is often no signal at the pitch, so checkout and check-in must work offline and sync when the phone is back online.
   - **Q3:** Wrong. There are about 300 items and 40 coaches. Performance is not a concern, so I have no checkout numbers and no growth forecast.
   - **Q4:** Wrong. These can't wait:
     - an overdue report e-mailed every Monday morning
     - a warning 30 days before an expiry date on first-aid bag items
     - lost-item history kept for 2 years

     It must be live for the start of the season on 1 March.
   - **Q5:** Right that there is no money handling: no deposits, fines or payments. The rest is fine with me.
   - **Q6:** Wrong. Coach names and phone numbers are kept, not only names. Data must stay on the club's own hardware, with no third-party cloud. Deleting at the end of each season clashes with keeping lost-item history for 2 years.
   - **Q7:** Wrong. It must run on the club's existing Synology NAS (Docker is available), at 0 EUR per month.
   - **Q8:** Wrong. The only maintainer is one volunteer who knows Python only. A successor must be able to take it over.
   - **Q9:** Not right. The Monday overdue e-mail and the yearly CSV export are both needed. Committee access on screen or as a printout is fine, I have no view on that.
   - **Q10:** Fine, I accept that.

## DESIGNER

No files are written this turn. The updated proposal follows, and `docs/architecture/arc42.md` still holds only the skeleton.

## What changed

- **Order:** with the tie-breaker "easy to use wins", the order is R-1, R-3, R-2.
- **QG-2:** the measure is "at most 3 taps and under 15 seconds, from a QR scan".
- **QG-1:** the spot check is confirmed as the method. It still needs a threshold, see Q15.
- **Security** is a requirement (R-5 below).
- **Performance** is dropped as a concern.
- **Export:** kept on the ADR list. The yearly CSV inventory is needed for the treasurer's insurance audit.
- **Stakeholders:** treasurer, maintainer and successor added. The committee stays as well.
- **Figures:** about 40 coaches and 300 items. No checkout volumes or growth forecast, so these go to section 3.

## New needs (triage, `add-requirements` step 1)

Proposed IDs are R-4 to R-8 in the order listed. IDs are assigned on confirmation.

| Label | Need (draft wording) | Findings | Proposed outcome | Reason |
|---|---|---|---|---|
| E (R-4) | Checkout and check-in work offline and sync when the phone is back online. | conflicts with F: offline identity needs cached data on the phone | system-level | Shapes storage and sync; the ADR list's first item. |
| F (R-5) | Coach personal data (names, phone numbers) is visible only to signed-in club coaches. | conflicts with R-3 (sign-in step) and E (cached sign-in) | system-level | Personal data under GDPR (Q6). |
| G (R-6) | The club gets an e-mail every Monday morning listing overdue kit. | conflicts with F and with "data stays on club hardware": the mail names who has what | system-level | Outbound e-mail is a new interface. |
| H | A warning 30 days before first-aid item expiry. | none | feature-level, under G | A notification inside G. |
| I (R-7) | Lost-item history is kept for 2 years. | conflicts with the season-end deletion of coach data (Q6) and with F | system-level | A retention rule that shapes the data model. |
| J | The treasurer exports a yearly inventory as CSV for the insurance audit. | none | feature-level, under R-1 | An export of the record; its format is on the ADR list. |
| K (R-8) | A volunteer who knows Python can maintain it, and a successor can take it over. | none | system-level | Shapes code and documentation; backs a maintainability goal. |

**Constraints (section 2, once confirmed):**
- Runs on the club's existing Synology NAS with Docker, at 0 EUR per month.
- Personal data stays on the club's hardware, with no third-party cloud.
- Must be live for the start of the season, 1 March.
- The maintainer knows Python only (see Q14).

**Non-goals (section 3):** no money handling (deposits, fines, payments). Also no player data, results or membership system.

## Rank (proposed, you set it)

1. R-1 check in/out
2. R-3 easy to use
3. R-2 attribution per coach
4. R-4 offline
5. R-5 confidentiality
6. R-6 Monday e-mail
7. R-7 lost-item history
8. R-8 maintainability

**Conflicts and tie-breakers:**
- R-4 vs R-5: if only one can be fully met, which?
- R-5 vs R-6: if only one can be fully met, which?
- R-7 vs season-end deletion: if only one can be fully met, which?
- R-2 vs QG-2 (3 taps): you settled it in favour of R-3. How a coach is identified within 3 taps is open (Q11).

## Quality goal candidates

- **QG-1, Functional suitability: functional correctness** (R-1, R-2). Measure: spot check. The threshold is open (Q15).
- **QG-2, Interaction capability: operability** (R-3). Scenario: a coach scans the bag's QR code and checks it out, in normal operation. Measure: at most 3 taps and under 15 seconds from the scan.
- **QG-3, Reliability: availability** (R-4). Scenario: a coach checks out at the pitch with no signal. Measure: open (Q15).
- **QG-4, Security: confidentiality** (R-5). Scenario: someone without a sign-in asks for coach names or phone numbers. Response: denied, nothing shown. Proposed measure: 0 coach records readable without sign-in. Open until you confirm it (Q15).
- **QG-5, Maintainability: modifiability** (R-8). Measure: open (Q15).

**Goal impact:**
- R-4 strengthens QG-3 and strains QG-4 (cached data on the phone).
- R-5 strengthens QG-4 and strains QG-2 (a sign-in step inside the 3 taps).
- R-6 and R-7 strain QG-4 (personal data in e-mail and in two-year history).
- R-8 strengthens QG-5.

## Interview, round 2

❓ **Q11** - **Identity in 3 taps**: How does a coach get identified within the 3 taps, with no signal?

➡️ Each coach signs in once on their own phone; checkouts then use that identity, so there is no extra step.

❓ **Q12** - **Retention clash**: Lost-item history is kept 2 years, but coach names and phone numbers are deleted at season end. Which wins?

➡️ Both: at season end, delete coach names and phone numbers, and keep lost-item history for 2 years with the coach replaced by a pseudonym.

❓ **Q13** - **Monday e-mail**: Who receives it, and may it name the coach who has an overdue item? It has to leave the NAS through a mail provider.

➡️ The equipment manager receives it. It names the item and the coach's first name, sent from the club's existing mail account. Sending it means personal data leaves the club's hardware, so this conflicts with the constraint. Please decide whether to accept that.

❓ **Q14** - **Python**: Must the system be written in Python, or is Python only a fact about the maintainer?

➡️ Yes, Python is a constraint for section 2.

❓ **Q15** - **Measures**: What number would show each goal is met?

➡️ Recommended, for you to change:
- QG-1: at least 95% of spot-checked items where the record says.
- QG-3: every offline checkout appears after sync, in test runs.
- QG-4: 0 coach records readable without sign-in, as proposed.
- QG-5: a maintainer who did not write a module can make a tested change in it within one day.

❓ **Q16** - **Overdue**: After how many days out is an item overdue?

➡️ Not checked in within 7 days.

## Your turn

Please:
1. Set the rank, or confirm the proposed one and the three tie-breakers (R-4/R-5, R-5/R-6, R-7/season deletion).
2. Confirm or change the new triage outcomes (E to K) and the constraints.
3. Answer Q11 to Q16.

## ARCHITECT

1. **Rank and tie-breakers:** The proposed rank is fine.
   - **R-4 / R-5:** Both matter. Offline must work, but keep as little personal data on the phone as possible.
   - **R-5 / R-6:** Data staying on the club's own hardware wins. No coach phone numbers in the e-mail, and nothing may go through a third-party cloud. I want the Monday report, but it has to respect that.
   - **R-7 / season deletion:** I never asked for deletion at season end. Coach names and phone numbers are kept, and lost-item history is kept for 2 years.

2. **Triage and constraints:** E to K and the constraints are fine. The constraint "Runs on the Synology NAS with Docker, at 0 EUR per month" is right. I'd add that the kit manager receives the Monday report.

3. **Q11 to Q16:**
   - **Q11:** Signing in once per phone is fine, as long as a checkout stays within 3 taps from the QR scan.
   - **Q12:** See point 1. If you pseudonymise the coach in the lost-item history, that's fine with me.
   - **Q13:** The kit manager receives it. It must not send data to a third-party cloud (see point 1). The technical way to send it is up to you. I have no preference on whether it shows first names.
   - **Q14:** Yes, Python. The only maintainer knows only Python.
   - **Q15:** The measures are fine. Also keep the 3 taps and 15 seconds for QG-2.
   - **Q16:** 7 days is fine.

## DESIGNER

The architecture is written, pending your approval of ADR 0001. Nothing is committed.

## Files written

- **`docs/architecture/arc42.md`**
  - Section 1: the R-list (R-1 to R-8, ranked as you set it), QG-1 to QG-5, and the stakeholders.
  - Section 2: the four constraints.
  - Section 3: the figures (about 40 coaches, about 300 items) and the non-goals.
  - Section 9: links to ADR 0001.
  - Section 10: QS-1 to QS-5, with the measures you confirmed.
  - Sections 4–8, 11 and 12 are still empty, and sections 5, 6 and 7 wait for building blocks.
- **`docs/adr/0001-record-architecture-decisions.md`**: status `proposed`. Its decided-centrally list is storage and sync, the CSV export, the Monday report channel, interfaces, crosscutting conventions and third-party dependencies. Work on any of these waits for your approval.
- **`.scratch/requirements/issues/01-expiry-warning.md`**: a feature-level issue under R-6. There is no issue tracker in the repo, so this is the fallback location.
- **`.scratch/requirements/issues/02-yearly-csv-export.md`**: a feature-level issue under R-1.

## Choices I made

- **Your rank:** R-1, R-3, R-2, R-4, R-5, R-6, R-7, R-8. It is recorded as bare numbers, as you set them.
- **Q12 and the season-end deletion:** I wrote no deletion rule, since you said you never asked for one. Coach names and phone numbers have no retention period yet (see open questions).
- **R-6 wording:** I added "the kit manager receives it", as you asked. I also added the no-phone-numbers and no-third-party-cloud rules.
- **R-5 wording:** I added "phones keep as little personal data as possible", as the tie-breaker answer.
- **Issue location:** I used `.scratch/` because `docs/agents/issue-tracker.md` does not exist.

## Open questions

1. **Retention for coach names and phone numbers.** No period is set, which GDPR normally requires. Please give one, or say that none applies.
2. **Monday report channel.** R-6 says no third-party cloud, but e-mail usually goes through a mail provider. The channel is an open decision for ADR 0001.
3. **R-4 against R-5 on the phone.** You said both matter, and I recorded that in the R-5 wording. It is not resolved by the rank, so the storage and sync decisions in ADR 0001 must settle it.
4. **Risks (section 11)** are not written, because you did not confirm any. The R-4 against R-5 conflict is the obvious first entry if you want it.

## Waiting for you

- **Approve or reject ADR 0001.** Its text is `proposed` until you approve it. Storage, sync, the CSV export format and the Monday report channel all wait for that approval.

## ARCHITECT

1. **Retention of coach names and phone numbers:** Keep them while someone is an active coach, and delete them when they leave the club. The pseudonymised lost-item history stays for 2 years. If you recommend a different period, that's fine with me.
2. **Monday report channel:** The technical way is up to you. It must not go through a third-party cloud, it must cost nothing, and it must run from the NAS. The kit manager receives it, and no phone numbers go in it.
3. **R-4 against R-5 on the phone:** Fine, settle it in the storage and sync decisions.
4. **Risks:** Yes, add the R-4/R-5 conflict as the first entry.
5. **ADR 0001:** Approved.