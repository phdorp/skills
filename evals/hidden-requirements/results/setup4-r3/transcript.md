## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the arc42 skeleton at `docs/architecture/arc42.md`. It is the only file this turn touched. The project has no code and no architecture documents, so there were no existing documents to link. Nothing is decided yet: below is my proposal for you to confirm or change.

## Triage

The R-list is empty, so only the outcome remains. I took the requirements from the README.

| Candidate | Checks | Proposed outcome and reason |
|---|---|---|
| **R-1:** Coaches check kit out to themselves and back in, so the club always knows which coach holds which item. | No duplicate, no conflicts. | **system-level.** It is the core of the idea and shapes the data model. |
| **R-2:** The tool is easy to use. | No duplicate, no conflicts. | **system-level.** It shapes the interface and scope. Sharper wording, as a proposal: *"A coach can check kit out or in without training or help."* |

The item types (balls, bibs, cones, first-aid bags) I would fold into R-1 as data, not give them a separate requirement or issue.

## Rank

1. R-1
2. R-2 (proposed)

No conflicts found. Tie-breaker: if only one of R-1 and R-2 can be fully met, which one?

## Quality goals

- **From R-1, Functional suitability: functional correctness.** Measure still open: what would show R-1 is met? For example, "after a week of use, no item is listed under a coach who does not hold it." Open question for you.
- **From R-2, Interaction capability: learnability.** Measure still open: how long, and for what share of coaches, does a first check-out take without help? Open question for you.

No goal without an R-ID behind it.

## Interview, round 1

❓ **Q1** - **Users**: Who uses the tool, how many of them, where, and on which devices, with what connectivity and skills?

➡️ Coaches, roughly 20–40, using their own phones at the pitch. Mobile data is often weak. Basic smartphone skills. The equipment manager is the admin.

❓ **Q2** - **Volume**: How many items and check-outs, now and in about three years?

➡️ A few hundred items and several dozen check-outs a week. Roughly double in three years.

❓ **Q3** - **First version**: What must the first version do, and what can wait?

➡️ First version: check out and check in by coach, and see who holds what. Later: reminders, reports, notifications.

❓ **Q4** - **Non-goals**: What must the tool never do?

➡️ No payments, no player or member database, no purchasing or stock ordering.

❓ **Q5** - **Hosting and cost**: Where may it run, and what may it cost?

➡️ A free or low-cost hosted service (under about €5 a month). No hardware purchase. No constraint on where the data is hosted beyond EU law.

❓ **Q6** - **Builders**: Who builds and maintains it, and with which skills?

➡️ One volunteer who is comfortable with spreadsheets but is not a developer, maintained by the equipment manager.

❓ **Q7** - **Data**: What data does it keep, whose is it, how long, and which law applies?

➡️ Coach names and item records. Personal data of coaches, so GDPR applies. Keep only what is needed, and delete a season's history after the season.

❓ **Q8** - **Deadline**: By when must it be live?

➡️ Before the next season starts. Please give the date.

❓ **Q9** - **Exchange**: Which systems or people does it exchange data with?

➡️ None at first. The committee may want a CSV export later.

❓ **Q10** - **Missing characteristics**: Did you leave out something like availability: must check-out work at the pitch with no signal?

➡️ Yes. A check-out made without signal should be recorded and synced later.

## Decisions made centrally (draft for "Record architecture decisions")

ADR `0001`, since there is no ADR directory yet. Its Context would cite R-1 and R-2 in words, since neither is confirmed. Draft list:

- **Decided centrally:** the storage engine and data format for item records and check-out history; the interfaces between building blocks and the dependency rule; crosscutting conventions (naming, units, error handling, logging, handling of coach personal data); third-party dependencies. Export format and its versioning join the list only if you want the CSV export (Q9).
- **Left to the building blocks:** internal helpers, screen layout, test layout.

## What I need from you

1. Confirm or change the triage outcomes, the wording of R-2, and the rank.
2. Say whether the two goal candidates are right, and give the measures I asked for.
3. Answer Q1–Q10 or change my recommendations.
4. Confirm or change the draft list for ADR 0001.

Once you have answered, I'll update the proposal and ask the next round. I write no requirement rows, goals or ADRs until you confirm them.

## ARCHITECT

1. Triage and rank: fine. Folding item types into R-1 as data is OK, but first-aid bag items need an expiry date, with a warning 30 days before. R-2 wording is OK if it includes a measure: check-out takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. Rank R-1 first, R-2 second. No preference on the tie-breaker.

2. Goals: both are right. R-1 measure: your example is fine. R-2 measure: at most 3 taps and under 15 seconds, for any volunteer, including the non-tech-savvy ones.

3. Several of the answers above are wrong:
- Q1: About 40 coaches on their own phones at the pitch, often with no mobile signal. Many are not tech-savvy. The kit manager is the admin.
- Q2: About 300 items and 40 coaches. Performance is not a concern.
- Q3: The first version must do offline check-out and check-in. I also want a Monday-morning overdue report by e-mail and an expiry warning 30 days ahead. A yearly inventory CSV export is needed too.
- Q4: Agreed on no payments. That includes no deposits or fines. No member database or purchasing is fine.
- Q5: Wrong. It must run on the club's existing Synology NAS (Docker is available). Budget is 0 EUR per month. No third-party cloud.
- Q6: Wrong. The only maintainer is one volunteer who knows Python only. A successor must be able to take it over.
- Q7: Stored data is coach names and phone numbers, which are personal data under GDPR. It must stay on the club's own hardware. History of lost items must be kept 2 years for insurance, so do not delete it after a season.
- Q8: It must be live by 1 March, the start of the season.
- Q9: The treasurer needs a yearly inventory export as CSV for the insurance audit. The overdue report goes out by e-mail every Monday.
- Q10: Yes. Check-out and check-in must work offline and sync when the phone is back online.

4. ADR 0001 list: fine. Add the CSV export format, since it is needed. For third-party dependencies, they must fit a Python-only maintainer.

## DESIGNER

I haven't written any files this turn, because your answers add new needs and corrections. The interview isn't finished. Below is the updated proposal. Your confirmed parts are marked as confirmed. Everything else is still a draft.

## Triage (new needs)

Q3 and the first-aid expiry both ask for the 30-day warning. That is one need, so it gets one row.

| Candidate | Checks | Proposed outcome and reason |
|---|---|---|
| **R-1** (confirmed, with items folded in): Coaches check kit out to themselves and back in, so the club always knows which coach holds which item. Items: balls, bibs, cones and first-aid bags. | none | system-level, confirmed |
| **R-2** (confirmed wording): Check-out takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. | none | system-level, confirmed |
| **R-3:** Check-out and check-in work offline and sync when the phone is back online. | Conflicts with R-1 (see below). | system-level. It shapes sync and local storage. |
| **R-4:** First-aid items carry an expiry date, and the club is warned 30 days before. | Repeats Q3's warning; one row. | system-level. It shares the e-mail channel with R-5. |
| **R-5:** The club gets an e-mail every Monday morning listing overdue kit. | none | system-level. It needs a scheduled job and an outgoing mail route. |
| **R-6:** The treasurer gets a yearly inventory export as CSV for the insurance audit. | none | system-level. It is an interface, so it goes on the ADR list. |
| **R-7:** A successor who knows only Python can take the tool over. | none | system-level. It limits dependencies and technology. |

Conflict: **R-1 vs R-3.** "Always knows which coach holds which item" fails while two offline devices disagree.

- **Tie-breaker:** if only one of R-1 and R-3 can be fully met, which?

## Rank

1. R-1 (set by you)
2. R-2 (set by you)
3. R-3 (proposed)
4. R-4 (proposed)
5. R-5 (proposed)
6. R-6 (proposed)
7. R-7 (proposed)

Proposed ranks are not yet set by you.

## Quality goals

- **QG-1, Functional suitability: functional correctness** (from R-1). Confirmed by you, scenario confirmed.
  - QS-1: a coach checks out or in an item; the list shows the holder at once. Measure: after a week of use, 0 items listed under a coach who does not hold them.
- **QG-2, Interaction capability: learnability** (from R-2). Confirmed by you, scenario confirmed.
  - QS-2: a volunteer, including one who is not tech-savvy, checks kit out by scanning the bag's QR code. Measure: at most 3 taps and under 15 seconds.
- **QG-3, Reliability: availability** (from R-3). Open question: what would show R-3 is met? My suggestion: a check-out made offline reaches the shared list within 5 minutes of reconnecting, and 0 of 100 offline check-outs are lost in trials.
- **QG-4, Compatibility: interoperability** (from R-6). Open question: what would show the export is complete? My suggestion: the CSV lists 100% of items and history rows, checked against the item list.
- **Maintainability: modifiability** (from R-7). Open question: what would show a successor can take over? My suggestion: a Python-only volunteer can read the setup and deploy on the NAS within a day.
- **Ruled out:** Performance efficiency (time behaviour, capacity, resource use). Your reason: about 300 items and 40 coaches.

## Constraints (section 2, proposed)

- Runs on the club's Synology NAS, in Docker.
- Budget 0 EUR per month.
- No third-party cloud service.
- Coach personal data stays on club hardware; GDPR applies.
- Loss history is kept for 2 years, for insurance.
- Live by 1 March, the start of the season.
- One maintainer, Python only; third-party dependencies must fit that.

## Out of scope (section 3, proposed)

- Payments, deposits and fines.
- A member or player database.
- Purchasing and stock ordering.

## Stakeholders (section 1, proposed)

Coaches (about 40, users); the kit manager (admin); the treasurer (yearly export, insurance audit); the single maintainer and their successor.

## Figures

About 300 items and 40 coaches. I had proposed several dozen check-outs a week; you didn't correct that, so please confirm it.

## ADR list (ADR 0001, updated)

- **Decided centrally:** storage and data format for items and history; sync protocol and the local data format on the phone (new, since offline sync crosses client and server); CSV export format, with its versioning; interfaces and the dependency rule; crosscutting conventions; third-party dependencies, which must fit a Python-only maintainer.
- **Left to the building blocks:** internal helpers, screen layout, test layout.

## Interview, round 2

❓ **Q11** - **Offline conflicts**: If two coaches check out the same item while offline, which record wins?

➡️ The first record to sync wins. The other is flagged for the kit manager to resolve.

❓ **Q12** - **Tie-breaker**: If only one of R-1 and R-3 can be fully met, which?

➡️ R-3 (offline). A coach at the pitch must be able to check out, even if the list is briefly out of date.

❓ **Q13** - **QR codes**: Is each individual item tagged, or only each bag?

➡️ Each bag. Items in a bag are checked out together.

❓ **Q14** - **App or web page**: Must coaches install an app from a store, or is a web page on the phone enough?

➡️ A web page the coach adds to the home screen. No store install.

❓ **Q15** - **Check-in measure**: Does the 3-tap, 15-second measure also cover check-in?

➡️ Yes, the same measure for check-in.

❓ **Q16** - **Overdue**: What counts as overdue?

➡️ Not checked in after 7 days.

❓ **Q17** - **Expiry warning**: Does the 30-day expiry warning go in the Monday e-mail, or separately?

➡️ In the Monday e-mail, as its own section.

❓ **Q18** - **Outgoing mail**: With no third-party cloud, is sending mail through the club's existing e-mail account acceptable?

➡️ Yes. It's already in use, so it is not a new cloud service.

❓ **Q19** - **Recipients**: Who receives the Monday report and the yearly export?

➡️ The kit manager gets the Monday report. The treasurer gets the export, with the kit manager in copy.

❓ **Q20** - **Personal data**: Who may see coach phone numbers?

➡️ Only the kit manager and treasurer. Coaches see item lists without phone numbers.

❓ **Q21** - **Recoverability**: Must the data survive a NAS disk failure?

➡️ Yes. Nightly copy to a second disk on the NAS, since the loss history is an insurance record.

❓ **Q22** - **Successor**: What would show a successor can take over?

➡️ A Python-only volunteer can read the setup notes and deploy on the NAS within a day.

❓ **Q23** - **Check-out volume**: Please confirm several dozen check-outs a week.

➡️ Yes, several dozen a week.

## What I need from you

1. Set the ranks of R-3 to R-7, or change the order.
2. Answer the tie-breaker (Q12) and the open goal measures (QG-3, QG-4, maintainability).
3. Answer Q11 and Q13 to Q23, or change my recommendations.
4. Say whether R-4 (expiry) and R-5 (Monday report) stay separate rows, as proposed.

Once you've answered, I'll update the proposal, and if nothing is missing I'll write the confirmed items.

## ARCHITECT

1. Ranks: fine, R-3 to R-7 in the order you proposed.

2. Tie-breaker: R-3 (offline) wins. A coach at the pitch must be able to check out. The measures for QG-3, QG-4 and maintainability are fine as you suggested.

3. Q11 and Q13-Q23: all fine as you wrote them. No preference on the technical points (web page on the home screen, mail route).

4. Yes, keep R-4 (expiry) and R-5 (Monday report) as separate rows.

## DESIGNER

The setup is written, except for one open item (the recoverability need, below). Everything you confirmed is in `docs/architecture/arc42.md`, and the decision record is drafted.

## Files written

- `docs/architecture/arc42.md`: the R-list (R-1 to R-7, with ranks 1 to 7), quality goals QG-1 to QG-5 with their scenarios QS-1 to QS-5, stakeholders, constraints, out-of-scope items, figures, the offline-conflict and Monday-report runtime notes, and the links in sections 9 and 12.
- `docs/adr/0001-record-architecture-decisions.md`: status `proposed`, with the list you approved, including the CSV export format and the third-party dependency rule.

No commit was made.

## Waiting for you

- **ADR 0001** needs your approval of its text before any of these can start: the storage and data format, the sync protocol and the phone's local data format, the CSV export format, the interfaces between blocks, the crosscutting conventions, and the third-party dependencies. Until it is accepted, none of that work begins.

## Open questions

- **Recoverability (Q21) has no row yet.** You confirmed "data survives a NAS disk failure, nightly copy to a second NAS disk". That is a system-level requirement I did not put to you as an R-row. Shall I propose it as R-8, with rank 8 and a goal of Reliability: recoverability, and ask you for its measure?
- **R-2's wording covers check-out only.** Q15 applies the same measure to check-in, which is in QS-2. Do you want the row to say "check-out or check-in", or keep your wording as it is?
- **Two confirmed answers are recorded as constraints, not rows.** Phone numbers visible only to the kit manager and treasurer (Q20) is in section 2. Offline conflict handling (Q11) is in section 6. Say if either should be a requirement.

## ARCHITECT

1. ADR 0001: Approved.

2. Recoverability: yes, propose it as R-8 with rank 8 and a Reliability: recoverability goal. Suggested measure: after a NAS disk failure, the data from the previous night can be restored. I have no preference on the technical details.

3. R-2: yes, change the wording to "check-out or check-in".

4. Phone-number visibility (Q20) and offline conflict handling (Q11): keeping them where they are is fine with me.

## DESIGNER

Setup is complete. The architecture is written and the decision record is accepted.

## Files changed

- `docs/adr/0001-record-architecture-decisions.md`: status is now `accepted 2026-11-24`.
- `docs/architecture/arc42.md`:
  - R-2 now reads "Check-out or check-in takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag."
  - R-8 added: "After a NAS disk failure, the data from the previous night can be restored." Rank 8, status `active`.
  - QG-6 added: Reliability: recoverability, from R-8.
  - QS-6 added, with your measure: after a NAS disk failure, the previous night's data can be restored.

Goal impact of R-8: it strengthens QG-6, which is new. I found no goal it strains.

Q11 (offline conflicts) and Q20 (phone-number visibility) stay as they are, in sections 6 and 2.

## Still open

Nothing is waiting on you. Two things follow from the approval:

- Work that depends on ADR 0001's list can now plan. Each listed decision (storage, sync, CSV export, dependencies, and the rest) still needs its own ADR, which I will draft as `proposed` when that work starts.
- No code has been written, and nothing is committed.

## ARCHITECT

Approved. Nothing further from me.