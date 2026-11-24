## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the skeleton at `docs/architecture/arc42.md`, and that is the only file this turn changes. Below is my proposal. Nothing in it becomes part of the architecture until you confirm it.

## Triage

The R-list is empty, so each candidate gets only its proposed outcome.

| candidate requirement (from README) | proposed outcome | reason |
|---|---|---|
| Coaches check kit out and back in, so the club always knows where each item is and which coach has it. | system-level | It decides the data model and the check-out and check-in flow. |
| Track balls, bibs, cones and first-aid bags. | feature-level, under R-1 | It lists the kinds of kit inside R-1. An issue is filed only after you confirm. |
| It should be easy to use. | system-level | It shapes the interface and how coaches work with the tool. It has no measure yet, so it stays open. |

## Rank (proposed)

1. **R-1**, the check-out record. It is the purpose of the tool.
2. **R-2**, ease of use. A record only helps if coaches use the tool.

Conflict: R-1 and R-2 may pull against each other, for example if an exact record needs an extra step. Tie-breaker: if only one of them can be fully met, which one? I recommend R-1. You set the order.

## Quality goals (candidates)

- **QG-1, Functional Suitability: functional correctness** (from R-1). Scenario: a coach checks an item out or back in during the season. Measure is still open. Candidate: "a spot check of 20 random items finds 0 with the wrong recorded holder." What would show R-1 is met?
- **QG-2, Interaction capability: operability and learnability** (from R-2). Scenario: a coach who has never used the tool checks out one item. Measure is still open. Candidate: "without help, in under 30 seconds, 9 times out of 10." Is that the right bar?

Neither goal is a confirmed row yet. Reliability and Security have no requirement behind them yet, so they are not candidates. Round 1 asks about them.

## Interview, round 1

❓ **Q1** - **Users and devices**: Who uses it, how many, on which devices, and how good is the signal at the pitch?

➡️ About 30–40 coaches on their own smartphones, often with weak signal at the pitch. You are the admin.

❓ **Q2** - **Scale**: How many items and how many check-outs per season?

➡️ About 300 items, 40 coaches, and about 5,000 check-out and check-in events per season.

❓ **Q3** - **First version**: What must it do, and what can wait?

➡️ Must: check out, check in, see who holds what, and list the items. Can wait: reminders for overdue kit, reports.

❓ **Q4** - **Non-goals**: What must it never do?

➡️ Track players, handle payments, or value or buy kit.

❓ **Q5** - **Platform, hosting, budget**: Where does it run, and what may it cost? Must it run on hardware the club owns?

➡️ Free or near-free hosting, reachable from a phone browser. Nothing that needs club-owned hardware.

❓ **Q6** - **Builders**: Who builds and maintains it, and with which skills?

➡️ One volunteer maintainer comfortable with basic web development, who hands it over to the next equipment manager.

❓ **Q7** - **Data**: What data does it keep, whose is it, how long, and which law applies?

➡️ Coach names and what they hold. No children's data. Delete the log after each season. GDPR applies if the club is in the EU.

❓ **Q8** - **Date**: What date must it be live by?

➡️ Before the next season starts.

❓ **Q9** - **Exchange**: Which systems or people does it exchange data with?

➡️ None in the first version. A CSV export for the committee.

❓ **Q10** - **Characteristics you may have left out**: Security: can any coach change or delete another coach's record? Reliability: what happens if the tool is down on match day?

➡️ Any coach may add a record. Only you may correct or delete one. A paper fallback on match day is fine, and records must survive a crash.

## Decisions made centrally (draft)

No ADR directory exists yet, so this would be `docs/adr/0001-record-architecture-decisions.md`, status `proposed`. It is written after you confirm the proposal. Draft list, adjusted to this product:

- Storage engine and the format of the check-out log.
- Import and export formats (the CSV export).
- Interfaces between building blocks and the dependency rule between them.
- Versioning of the export format and anything else others depend on.
- Crosscutting conventions: naming, units, error handling, logging.
- Third-party dependencies (framework, hosting service).

Left to the building blocks: internal helpers, structure inside a block, test layout.

## Stakeholders (proposed)

You as equipment manager and architect, the coaches, and the club committee, which receives the export. Confirm or change this list.

---

Please confirm or change each part above, including the rank and the two goal candidates, and answer round 1 (Q1–Q10). Once you have answered, I'll update the proposal and ask the next round.

## ARCHITECT

1. **Triage:** Fine, with two corrections. "Easy to use" is not open. Checking out an item must take at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag. Many volunteers are not tech-savvy.

2. **Rank:** R-1 first, R-2 second. Agreed.

3. **QG-1:** Your spot-check measure is fine with me.

4. **QG-2:** The 30 seconds is the wrong bar. Use at most 3 taps and under 15 seconds per check-out, via QR scan.

5. **Reliability and Security:** Both have requirements.
   - Check-out and check-in must work offline and sync when the phone is back online.
   - Coach names and phone numbers are GDPR personal data. Data must stay on the club's own hardware, with no third-party cloud.

**Round 1**

- **Q1:** About 40 coaches use their own phones at the pitch. There is often no mobile signal at all, not just a weak one. Check-out and check-in must work offline and sync later. The QR scan and 3-tap rule above applies.
- **Q2:** About 300 items and 40 coaches. I don't know the number of events, so I'm fine with your estimate. Performance is not a concern.
- **Q3:** Reminders and reports can't wait. I need these:
  - An overdue report e-mailed every Monday morning.
  - A warning 30 days before an expiry date on first-aid bag items.
  - A yearly inventory CSV export for the treasurer's insurance audit.
- **Q4:** No money handling at all: no deposits, fines or payments. The rest of your list is fine with me.
- **Q5:** This is wrong. It must run on the club's existing Synology NAS, where Docker is available. The budget is 0 EUR per month. Data must stay on club hardware, with no third-party cloud.
- **Q6:** The only maintainer is one volunteer who knows Python only, not web development in general. A successor must be able to take it over.
- **Q7:** It holds coach names and phone numbers, and GDPR applies. Do not delete the log each season. History of lost items must be kept for 2 years for the insurance.
- **Q8:** It must be live for the start of the season on 1 March.
- **Q9:** It sends the Monday overdue e-mail, and the treasurer gets the yearly inventory CSV. I know of nothing else.
- **Q10:** I have no preference on who may edit records, so your suggestion is fine. Records surviving a crash: yes. I have no preference on the paper fallback.

**Decisions made centrally:** The list is fine. Please keep the Python-only maintainer and the Synology NAS Docker setup in mind for dependencies.

**Stakeholders:** Add the treasurer, who receives the CSV. The kit manager is me, but the maintainer is a different volunteer. Otherwise fine.

## DESIGNER

Thanks. Your answers open new needs, so the frontier is not empty yet. I'm not writing any file this turn; after you confirm the parts below I'll write them.

## Triage (updated)

| candidate requirement | proposed outcome | reason |
|---|---|---|
| R-1: Coaches check kit out and back in, so the club always knows where each item is and which coach has it. | system-level | It decides the data model and the check-out flow. Confirmed as is. |
| R-2: Checking out an item takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. | system-level | It decides the interface. Your wording replaces "easy to use". |
| R-3: Check-out and check-in work offline and sync when the phone is back online. | system-level | It decides local storage and sync. |
| R-4: Coach names and phone numbers are protected as GDPR personal data. | system-level | It decides access control and storage. |
| R-5: Records survive a crash. | system-level | It decides the storage durability. |
| R-6: Any coach may add a record; only the kit manager may correct or delete one. | system-level | It decides the permission model. |
| R-7: An overdue report is e-mailed every Monday morning. | system-level | It adds a scheduler and outbound e-mail. |
| Expiry warning 30 days before a first-aid item expires. | feature-level, under R-7 | It uses the same notification mechanism. An issue is filed only after you confirm. |
| R-8: A yearly inventory CSV export for the insurance audit and the treasurer. | system-level | The export format is a decision made centrally and is versioned. |
| R-9: A volunteer who knows Python can understand, change and hand over the tool. | system-level | It limits the stack and the structure. |

Not requirements:
- Money handling (deposits, fines, payments): out of scope.
- Tracking players, buying or valuing kit: out of scope.
- Performance: ruled out by you ("not a concern").
- Paper fallback: no preference from you, so no requirement.

## Rank (proposed)

1. R-1 check-out record
2. R-2 3-tap QR check-out
3. R-3 offline check-out and sync
4. R-4 personal data protection
5. R-5 crash survival
6. R-6 edit permissions
7. R-7 Monday overdue e-mail
8. R-8 yearly CSV export
9. R-9 maintainable by a Python volunteer

Conflicts:
- **R-1 vs R-3:** while offline, a checkout is not visible to others until sync, so "always know where it is" can be stale. Tie-breaker: if only one of R-1 and R-3 can be fully met, which? I recommend R-1.
- **R-4 vs R-7:** an outbound mail service may count as third-party cloud. Question Q13 covers it.

You set the order.

## Quality goals (candidates)

- **QG-1, Functional Suitability: functional correctness** (R-1). Confirmed: a spot check of 20 random items finds 0 with the wrong recorded holder.
- **QG-2, Interaction capability: operability** (R-2). Confirmed: at most 3 taps and under 15 seconds per check-out, via QR scan.
- **QG-3, Reliability: fault tolerance** (R-3). Measure open. Candidate: 0 check-outs lost across 50 offline-then-sync cycles. What would show R-3 is met?
- **QG-4, Reliability: recoverability** (R-5). Measure open. Candidate: 0 lost confirmed check-outs in 100 kill-during-write trials.
- **QG-5, Security: confidentiality** (R-4). Measure open. It depends on Q14 (who may see phone numbers).
- Later candidates: **QG-6, Security: integrity** (R-6), **QG-7, Maintainability: analysability** (R-9), **QG-8, Interoperability** (R-8). Their measures are open too.

Proposed top 5 for you to rank: QG-1, QG-2, QG-3, QG-4, QG-5. QG-6 to QG-8 wait for the next round.

Ruled out: performance efficiency (time behaviour and capacity), because you said it is not a concern. The 15-second limit under QG-2 still applies. Do you confirm both sub-characteristics are ruled out?

## Constraints (section 2, proposed)

- Runs on the club's existing Synology NAS, in Docker.
- Running cost 0 EUR per month.
- No third-party cloud: data stays on club hardware.
- Maintained by one volunteer who knows Python only, and handed over to the next maintainer.
- Live by 1 March (start of the season).
- GDPR applies to coach names and phone numbers.
- Lost-item history is kept for 2 years (insurance).

## Out of scope (section 3, proposed)

- Money handling: deposits, fines, payments.
- Tracking players.
- Buying or valuing kit.

## Stakeholders (section 1, proposed)

- Kit manager: you, architect. You correct and delete records.
- Maintainer: a separate volunteer who knows Python.
- Coaches: about 40 users.
- Treasurer: receives the yearly CSV.
- The committee is dropped, since Q9 no longer names it.

## Decisions made centrally (ADR list, updated)

The list stands. Dependencies are added under third-party dependencies: Docker on the Synology NAS, and Python for the maintainer.

## Interview, round 2

❓ **Q11** - **Offline conflicts**: Two coaches check out the same item offline. What happens at sync?

➡️ Keep both events in time order and flag the item as conflicting, for the kit manager to resolve.

❓ **Q12** - **Overdue**: When is an item overdue?

➡️ Not checked in within 7 days of check-out. The window can change per item type later.

❓ **Q13** - **Monday e-mail**: Who receives it, and which mail service sends it?

➡️ The kit manager and the treasurer. It is sent through the club's existing mail account. Is a mail provider acceptable under "no third-party cloud", or should mail be sent only from the NAS?

❓ **Q14** - **Phone numbers**: Who may see a coach's phone number?

➡️ Only the kit manager. Coaches see names and the items each person holds.

❓ **Q15** - **Leavers**: When a coach leaves, do we delete their name and phone number, and keep the item history?

➡️ Delete the phone number when they leave. Keep the lost-item history for 2 years with the name pseudonymised. Insurance and GDPR both apply, so confirm this.

❓ **Q16** - **Backups and loss**: Does the NAS back up, and how much record loss is acceptable after a crash?

➡️ A nightly NAS backup. Losing the last few minutes of records is acceptable, but no check-out that was already synced may be lost.

❓ **Q17** - **Expiry and labels**: Which items have expiry dates, who prints the QR codes, and who receives the insurer's copy of the export?

➡️ Only first-aid bag items have expiry dates. You print and attach the QR codes. The treasurer sends the CSV to the insurer.

Please confirm or change the triage, the rank, the goal candidates and their measures, the constraints, the out-of-scope items and the stakeholders. Then answer Q11–Q17.

## ARCHITECT

1. **Triage:** Confirmed. The expiry warning under R-7 is fine.
2. **Rank:** Confirmed. If R-1 and R-3 conflict, R-1 wins.
3. **Goals:**
   - QG-3 and QG-4 measures are fine.
   - QG-5 follows my answer to Q14.
   - Performance is ruled out. Scale is tiny and not a concern.
   - Top 5 is fine.
4. **Constraints, out of scope, stakeholders:** Confirmed.

**Round 2**

- **Q11:** No preference, your proposal is fine.
- **Q12:** No preference, 7 days is fine.
- **Q13:**
  - Only I, the kit manager, get the Monday report. The treasurer only needs the yearly CSV.
  - The report names coaches, which is personal data. Data must stay on club hardware with no third-party cloud, so send it from the NAS if that is possible.
  - I can't judge whether the club's mail provider counts as a third party. Please flag that as a risk.
- **Q14:** No preference, only the kit manager sees phone numbers.
- **Q15:** Confirmed. Delete the phone number on leaving, and keep the lost-item history for 2 years.
- **Q16:** I don't know whether the NAS backs up. Your proposal is fine. No check-out that was already synced may be lost.
- **Q17:**
  - Only first-aid bag items have expiry dates.
  - Printing the QR codes myself is fine.
  - The treasurer needs the CSV for the insurance audit. Who sends it on is up to the treasurer.

## DESIGNER

The architecture skeleton is written with the confirmed requirements, goals, scenarios, constraints and risks. The "Record architecture decisions" ADR is written and waits for your approval.

**Files written** (in `/tmp/sa-bench/runs/setup4-r2/workspace`, uncommitted):
- `docs/architecture/arc42.md`: sections 1, 2, 3, 9, 10 and 11 filled from your answers; the rest stays as the skeleton.
  - R-1 to R-9 in your confirmed order, all `active`.
  - QG-1 to QG-5 with scenarios QS-1 to QS-5.
  - Performance is recorded as ruled out, with your reason.
- `docs/adr/0001-record-architecture-decisions.md`: status `proposed`, with your list of centrally decided items and the NAS and Python dependencies added.
- `.scratch/requirements/issues/01-track-kit-types.md`: feature-level issue under R-1. The repo has no `docs/agents/issue-tracker.md`, so I used the `.scratch` path.
- `.scratch/requirements/issues/02-expiry-warning.md`: feature-level issue under R-7.

**Legacy ADRs:** none, since this is a fresh project.

**Waiting for you:** approve the text of ADR 0001. Until you do, the storage, sync, interface, export, convention and dependency decisions on its list wait, so no code for them should be written.

**Open questions and risks** (recorded in section 11):
- **Monday report and "no third-party cloud":** you asked for the report to be sent from the NAS if possible. I don't know whether that is feasible, or whether the club's mail provider counts as third-party. The delivery path belongs in ADR 0001's third-party dependencies, and it needs a decision.
- **NAS backups:** their status is unknown. QG-4 depends on them.

## ARCHITECT

Approved. Please keep the Monday report sent from the NAS if that is possible. How it is sent is a technical choice, so I have no preference.