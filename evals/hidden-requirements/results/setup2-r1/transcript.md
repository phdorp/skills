## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

The skeleton is in place. This is the proposal for your review. Nothing else is written yet, and the ADR waits until you confirm.

**Starting point:** The project is fresh: no code and no architecture docs. The README describes the idea, not how the system is built, so there are no existing documents or legacy ADRs to map. The only file written is `docs/architecture/arc42.md`: twelve sections, empty tables in 1, 5 and 10, and links in 9 and 12. Section 9's link to `0001-record-architecture-decisions.md` will be broken until that ADR is written after your confirmation.

**Triage** (proposed outcomes; the R-list is empty, so only the outcome remains):

| requirement (from README) | proposed outcome | reason |
|---|---|---|
| Coaches check kit out and back in | system-level | defines the core flow and the data kept |
| Always know where everything is | system-level | defines the query the tool must answer |
| Easy to use | system-level | shapes the interface; needs a measure (see goals) |
| Item types: balls, bibs, cones, first-aid bags | feature-level, under the check-out requirement | a catalogue of item types, no architecture impact |
| "A small tool" | constraint (section 2), not a requirement | it limits scope rather than asking for a behaviour |

Sharper wording, as proposals only:
- R-1: "Coaches can check items out and return them, recording who holds each one."
- R-2: "At any time the club can see which coach holds each item, or that it is in storage."
- R-3: "A new coach can check an item out without instructions."

**Rank** (proposed):
1. R-1 check out and return: everything else depends on this data.
2. R-2 know where everything is: the purpose, but only useful once R-1 records the holders.
3. R-3 easy to use: decides whether R-1 gets used at all.

No conflicts found. Near-tie between R-2 and R-3. Tie-breaker: *"If only one of R-2 and R-3 can be fully met, which?"*

**Quality goals** (candidates):
- **QG-1 Functional suitability: functional correctness**, from R-1 and R-2. Proposed scenario: at a spot check of all items, the recorded holder matches the physical holder. Proposed measure: at least 95% match. Your number, please.
- **QG-2 Interaction capability: operability and learnability**, from R-3. **Open question:** what would show R-3 is met? For example: "a coach with no instructions checks out an item in under 30 seconds."

**Interview, round 1**

❓ **Q1** - **Who uses it**: Coaches only, or also the equipment manager? On phones at the pitch, or on a computer?

➡️ Coaches and the equipment manager, on phones, through a web page with nothing to install.

❓ **Q2** - **Connectivity**: Is there mobile signal at the pitch and in the storage room?

➡️ Not always. A check-out must still be recorded without signal and synced later.

❓ **Q3** - **First version**: What must it do, and what can wait?

➡️ First: check out, return, see where everything is. Later: history, reminders, low-stock alerts.

❓ **Q4** - **Non-goals**: What must it never do?

➡️ Store personal data about players, handle money or fees, or schedule training.

❓ **Q5** - **Where it runs and cost**: Hosted service or hardware the club owns? What may it cost per year?

➡️ A free-tier hosted service or a club-owned computer, with a budget near zero. Please give the number.

❓ **Q6** - **Builders**: Who builds and maintains it, and with which skills?

➡️ One volunteer comfortable with spreadsheets and basic web work; the equipment manager maintains it afterwards.

❓ **Q7** - **Data**: What does it keep, whose is it, how long, and which law applies?

➡️ Coach names and item records only, kept for one season and then deleted. GDPR if the club is in the EU. Please confirm the jurisdiction.

❓ **Q8** - **Date**: By when must it be live?

➡️ Before the next season starts.

❓ **Q9** - **Exchanges**: Does it exchange data with other systems or people, such as a membership list, a messenger group or spreadsheets?

➡️ Nothing in the first version. A CSV export later, if asked.

❓ **Q10** - **Missing characteristic**: Did you leave out something like Reliability: recoverability, meaning records survive a crash or a lost phone?

➡️ Yes. A check-out that is lost brings back the original problem, so records must survive crashes.

**Decisions made centrally** (draft list for the "Record architecture decisions" ADR, number 0001 because the project is fresh):
- storage engine and the format of stored records;
- export format (CSV), when it is added;
- interfaces between building blocks and the dependency rule between them;
- versioning of the export format and of any API other systems use;
- crosscutting conventions: naming, dates and time zones, error handling, logging;
- third-party dependencies, such as the framework and hosting service.

Left to the building blocks: internal helpers, structure inside one block, and test layout.

Please confirm or change each part, and answer Q1–Q10. Section 5 (building blocks) stays empty until the blocks are decided.

## ARCHITECT

**Triage, ranking, goals:** Fine with the triage and the ranking. Tie-breaker: R-3, ease of use, because many volunteers aren't tech-savvy.

- **QG-1:** 95% is fine.
- **QG-2:** Not 30 seconds. Checking out an item must take at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag.

**Q1.** Coaches use phones at the pitch. A web page with nothing to install is fine, with no preference on the technology.

**Q2.** There is often no mobile signal at the pitch. Check-out and check-in must work offline and sync when the phone is back online.

**Q3.** Not "later". These are needed:
- Check out and in, and seeing where everything is.
- An overdue report e-mailed every Monday morning.
- A warning 30 days before an expiry date on first-aid bag items.
- A yearly inventory export as CSV.
- History of lost items kept for 2 years.

There are no low-stock alerts on my list.

**Q4.**
- No money handling: no deposits, fines or payments.
- Coaches' names and phone numbers are stored, and that is personal data.
- Scale is tiny, about 40 coaches and 300 items, so performance is not a concern.
- No preference on training schedules.

**Q5.** Not a hosted service. It must run on the club's existing Synology NAS, which has Docker. The data must stay on club hardware with no third-party cloud. The budget is 0 EUR per month.

**Q6.** The only maintainer is one volunteer who knows Python only. A successor must be able to take it over. The equipment manager is not the maintainer.

**Q7.**
- It keeps coach names and phone numbers, plus item records.
- Item history, including lost items, is kept for 2 years for insurance, not one season.
- GDPR applies.
- The data stays on the club's own hardware.

**Q8.** It must be live for the start of the season on 1 March.

**Q9.** Yes, two exchanges:
- The Monday overdue report goes out by e-mail.
- The treasurer needs the yearly inventory CSV for the insurance audit.

Nothing else comes to mind.

**Q10.** Yes, agreed. Offline check-outs must not be lost either.

**Central decisions list:** Confirmed, with two notes:
- The CSV export is the yearly inventory export.
- Hosting is already decided: the Synology NAS, with Python as the language.

## DESIGNER

Thanks. Your answers open new needs, so this round is a proposal and writes no files yet. Once you confirm, I'll write the requirements, goals and constraints.

**Confirmed so far:**
- **Triage:** R-1 (check out and return), R-2 (know where everything is), R-3 (easy to use).
- **Ranking:** R-3 ranks above R-2 by your tie-breaker.
- **QG-1:** functional correctness, 95%.
- **QG-2:** operability. Check-out takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag.
- **Central decisions list:** confirmed, with the CSV export being the yearly inventory export and hosting and Python already decided.

**New needs from your answers**

| need | proposed outcome | reason |
|---|---|---|
| Check-out and check-in work offline and sync later | system-level, R-4 | changes how data is stored and synced between phone and server |
| Overdue report e-mailed every Monday | system-level, R-5 | an external e-mail interface and a scheduled job |
| 30-day expiry warning on first-aid items | feature-level, under R-5 | it can go in the Monday report; channel to confirm (Q13) |
| QR code on each kit bag | feature-level, under R-3 | the QG-2 measure depends on it |
| Yearly inventory CSV export | system-level, R-6 | an export format for the treasurer, versioned under the central list |
| History of lost items kept 2 years | system-level, R-7 | retention shapes storage and deletion; see the GDPR note below |
| Coach names and phone numbers | constraint (section 2) | personal data under GDPR; access rule in Q15 |
| No money, no training schedules, no low-stock alerts | out of scope (section 3) | you said no |

**Proposed rank:**
1. R-1 check out and return: everything depends on it.
2. R-4 offline: needed for R-1 at the pitch.
3. R-3 easy to use.
4. R-2 know where everything is.
5. R-5 Monday overdue report.
6. R-6 yearly CSV export.
7. R-7 two-year history.

**Conflicts:** R-7 (keeping history for 2 years) conflicts with GDPR data minimisation unless the history keeps only what the insurance needs.

**Tie-breakers to ask:**
- "If only one of R-3 and R-4 can be fully met, which?"
- "If only one of R-7 and data minimisation can be fully met, which?"

**Quality goal candidates** (QG-1 and QG-2 confirmed; the rest need your measures):
- **QG-3 Reliability: recoverability**, from R-4 and Q10. A check-out recorded offline must not be lost. **Open question:** what would show this is met? My proposal is 0 lost offline check-outs in 100 trials, including phones closed or losing power mid-sync. Your number?
- **QG-4 Security: confidentiality**, from the personal-data constraint. Coach phone numbers must be visible only to authorised people. **Open question:** what measure would show this? For example: "0 phone numbers shown to a coach without the equipment manager role, tested with 3 accounts."
- **QG-5 Maintainability: analysability**, from the successor constraint (Q6). **Open question:** what would show a successor can take it over? For example: "a Python-only volunteer changes the Monday report in under 4 hours, without the maintainer."

**Constraints and stakeholders** (for sections 1–3, pending your confirmation)
- Constraints: runs on the club's Synology NAS with Docker; data stays on club hardware with no third-party cloud; budget 0 EUR per month; Python; GDPR applies; live by 1 March; one volunteer maintains it, and a successor must be able to take over.
- Stakeholders: coaches (users), the equipment manager (user, not maintainer), the successor maintainer, the treasurer (receives the CSV for the insurance audit), the insurer (the 2-year history).

**ADR for hosting and language:** Hosting on the NAS with Docker and the choice of Python are decisions with lock-in. Should I record them as ADR-0002, proposed, for you to accept, or keep them as section 2 constraints only?

**Interview, round 2**

❓ **Q11** - **Mail**: Which mailbox sends the Monday report and the yearly CSV? Who receives the Monday report?

➡️ The club's existing mailbox, via SMTP. The Monday report goes to the equipment manager; the CSV goes to the treasurer.

❓ **Q12** - **Overdue**: How many days after check-out does an item count as overdue?

➡️ 7 days.

❓ **Q13** - **Expiry**: Who enters expiry dates, for which items, and does the 30-day warning go in the Monday report?

➡️ The equipment manager enters dates when restocking, for first-aid items only. The warning goes in the Monday report.

❓ **Q14** - **Offline conflicts**: Two coaches check out the same item offline. Which record wins when they sync?

➡️ Keep both and flag the conflict for the equipment manager.

❓ **Q15** - **Access**: Who logs in, and who may see coach phone numbers?

➡️ Each coach logs in with a club-issued code. Only the equipment manager sees phone numbers.

❓ **Q16** - **Leavers and history**: How long are a coach's name and phone number kept after they leave? What does the 2-year history store?

➡️ Phone numbers are deleted when a coach leaves. The history keeps the item, date and coach name, and deletes them after 2 years.

❓ **Q17** - **Backups**: Is the NAS backed up, and how?

➡️ A nightly backup to a second club-owned disk, with a restore test once per season.

❓ **Q18** - **Camera**: Can coaches' phone browsers use the camera to scan QR codes?

➡️ Yes, on current phones. Typing the code in is the fallback.

Please confirm or change the triage, the rank and tie-breakers, QG-3 to QG-5 and their measures, the constraints and out-of-scope list, and the ADR-0002 question, and answer Q11–Q18.

## ARCHITECT

**Confirmations**
- Triage: confirmed.
- Rank: confirmed.
- Tie-breaker R-3 vs R-4: R-4, offline. The pitch is where check-out happens, and there is often no signal there.
- Tie-breaker R-7 vs data minimisation: R-7. The insurance needs the 2-year history, but keep only the minimum fields.
- QG-3, QG-4, QG-5 and their measures: fine, as proposed.
- Constraints, stakeholders and out-of-scope list: confirmed. Please also list "performance is not a concern" as a non-goal (about 40 coaches, 300 items).
- ADR-0002 for hosting and language: yes, record it as an ADR.

**Q11.** No preference on the mailbox. The club's existing one is fine. The Monday report goes to me, the kit manager. The yearly CSV goes to the treasurer.

**Q12.** 7 days is fine.

**Q13.** Fine. I enter the expiry dates, for first-aid items only. The 30-day warning goes in the Monday report.

**Q14.** Fine. Keep both records and flag the conflict for me.

**Q15.** Fine. Each coach logs in with a club-issued code, and only I see phone numbers. The login must not push check-out past 3 taps or 15 seconds, so the phone should stay logged in.

**Q16.** Fine. Delete the phone number when a coach leaves. The history keeps the item, date and coach name for 2 years.

**Q17.** Fine. A nightly backup to a second club-owned disk, with a restore test once per season. The backup stays on club hardware too.

**Q18.** No preference. Typing the code in as a fallback is fine.

## DESIGNER

The architecture skeleton is filled in from your confirmations. Two ADRs are waiting for your approval of their text, and no open questions remain.

**Files written**
- `docs/architecture/arc42.md`:
  - **Section 1:** R-1 to R-7 with their confirmed ranks (R-1, R-4, R-3, R-2, R-5, R-6, R-7); QG-1 to QG-5; stakeholders.
  - **Section 2:** constraints (NAS with Docker, 0 EUR budget, Python, one Python-only maintainer, GDPR, live by 1 March, club-issued login with the phone kept logged in, nightly backup with a yearly restore test, club mailbox via SMTP, QR camera with typed fallback).
  - **Section 3:** context and out-of-scope list, including the performance non-goal.
  - **Section 9:** links to both ADRs.
  - **Section 10:** QS-1 to QS-5 with your measures.
- `docs/adr/0001-record-architecture-decisions.md`: the central-decisions list you confirmed, status `proposed`.
- `docs/adr/0002-host-on-nas-with-docker-in-python.md`: hosting on the NAS with Docker, in Python, status `proposed`.
- `.scratch/requirements/issues/01-item-types-catalogue.md`, `02-qr-code-check-out.md`, `03-expiry-warning.md`: the feature-level items under R-1, R-3 and R-5. There is no issue tracker configured, so they went to the fallback path. All three are `open`, to be triaged.

**Waiting for your approval**
- **ADR-0001** and **ADR-0002** are `proposed` until you approve their text. Work that depends on them waits: the storage engine, the export format, third-party libraries, and the implementation itself.

**Left empty on purpose**
- Section 4 (solution strategy) and section 5 (building blocks) need the ADRs accepted first. Sections 6, 7, 8 and 11 have nothing confirmed yet.

## ARCHITECT

Approved.