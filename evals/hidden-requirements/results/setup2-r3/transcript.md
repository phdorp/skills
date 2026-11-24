## ARCHITECT (opening prompt)

/sa:setup-architecture Set up the architecture for this project. The idea is in README.md.

## DESIGNER

I wrote the skeleton at `docs/architecture/arc42.md`. This is the only file changed so far. The R-list, goals, and ADRs wait for your confirmation.

## Triage (proposal)

The project is fresh, so these are the three needs in the README. Each gets an outcome only; there is no R-list yet.

| Need (from README) | Proposed outcome | Reason |
|---|---|---|
| Coaches check kit out and back in | system-level | Core behaviour; it shapes the data and the interface. |
| Always know where each item is and who has it | system-level | Core purpose; it depends on the check-out data. |
| Easy to use for volunteers | system-level | Shapes the interface and the training effort; it needs a measure (see goals). |

Sharper wording is up to you. For example, R-1 could read "A coach records check-out and check-in of any kit item in one step."

## Rank (proposal)

1. R-1 check-out and check-in: without it nothing else works.
2. R-2 known whereabouts: follows from R-1's data.
3. R-3 easy to use: it constrains how R-1 and R-2 are presented.

**Conflict:** R-1 (a full record of who, what, when) against R-3 (few taps). Tie-breaker: **if only one of R-1 and R-3 can be fully met, which?**

## Quality goals (candidates)

- **QG candidate, Functional suitability: correctness** (from R-1, R-2). The stimulus is a check-out or check-in; the response is that the record shows the correct holder and time. **Open question:** what would show that R-2 is met? For example, "a coach finds any item's holder in under a minute" or "0 wrong holders in 50 test check-outs"? You choose.
- **QG candidate, Usability: learnability** (from R-3). **Open question:** what would show R-3 is met? For example, "a first-time coach checks out an item in under 30 seconds without help"? Name your number.

The goals stay candidates until you confirm them and give measures.

## Interview, round 1

❓ **Q1** - **Users and devices**: Who uses the tool and on what? Coaches on their own phones, plus one shared device for the kit manager?

➡️ Yes: coaches use a phone browser; one shared tablet or laptop is for the kit manager.

❓ **Q2** - **Connectivity**: Is there a mobile signal at the pitch and in the store room?

➡️ Patchy. Check-out must still work without signal and sync later.

❓ **Q3** - **Access**: Can any coach check kit out, while only the kit manager adds items and sees the full history?

➡️ Yes.

❓ **Q4** - **First version**: Is check-out, check-in, and "where is item X and who has it" enough for v1?

➡️ Yes; everything else waits.

❓ **Q5** - **Non-goals**: Are purchasing, fitness or size tracking, payments, and links to the club's membership system out of scope?

➡️ Yes, all out of scope.

❓ **Q6** - **Hosting, budget and maintenance**: Must it run at zero cost, and can one volunteer with basic web skills maintain it?

➡️ Yes: free hosting, no paid licences, one volunteer maintains it.

❓ **Q7** - **Data**: The tool keeps coach names and check-out times. Is it deleted after one season, and does EU data protection (GDPR) apply?

➡️ Keep for one season, then delete. Yes, GDPR applies, if the club is in the EU. Please confirm where it is.

❓ **Q8** - **Date**: Must it be live by a fixed date, such as the start of next season?

➡️ Before the next season starts.

❓ **Q9** - **Other systems**: Must it exchange data with anything in v1, such as a club calendar or email?

➡️ No.

❓ **Q10** - **Missing characteristics**: Did you leave out something like security (only logged-in coaches change records), or reliability (a check-out is never lost)?

➡️ Yes to both: security for who may change records, reliability for check-outs that survive a dropped signal.

## Decisions made centrally (draft for the "Record architecture decisions" ADR)

This is ADR 0001, since the project has no ADRs yet. Its Context cites the requirements in words until you confirm their IDs.

Decided centrally (needs an ADR you accept):
- storage engine and on-disk data format for the kit records;
- import and export formats, if you want any;
- interfaces between building blocks, and the dependency rule between them;
- versioning of anything other systems depend on (none in v1, so probably nothing yet);
- crosscutting conventions: naming, units such as dates and time zones, error handling, logging;
- third-party dependencies.

Left to the building blocks (no ADR): internal helpers, screen layout, test layout.

## What I need from you

Please confirm or change:
1. The triage outcomes and the wording for R-1 to R-3.
2. The rank, and the tie-breaker answer for R-1 against R-3.
3. The two goal candidates, and the measures for R-2 and R-3.
4. The answers to Q1–Q10.
5. The central decision list for ADR 0001.

Once you confirm, I'll write the R-list, goals, scenarios, and ADR 0001. The ADR stays `proposed` until you approve its text. Section 9's link to it will resolve when that file is written.

## ARCHITECT

1. Triage and wording: fine, I accept R-1 to R-3 as you worded them.

2. Rank is fine. If only one of R-1 and R-3 can be fully met, ease of use wins. Checking out must take at most 3 taps and under 15 seconds, by scanning a QR code stuck on the kit bag.

3. Goals: both candidates are fine. For R-3, use the 3 taps / under 15 seconds measure instead of your 30-second example. For R-2, your "0 wrong holders in 50 test check-outs" is fine with me.

4. Q1-Q10:
- Q1: Yes. Coaches use their own phones, with the QR scan as above.
- Q2: Correct, but it's worse than patchy. There is often no signal at the pitch. Check-out and check-in must work offline and sync when the phone is back online.
- Q3: Yes.
- Q4: No, not enough. The v1 must also include:
  - an overdue report e-mailed every Monday morning;
  - a warning 30 days before an expiry date on first-aid bag items;
  - a yearly inventory export as CSV for the treasurer's insurance audit.
- Q5: Yes, all out of scope. Specifically, no money handling at all: no deposits, fines or payments.
- Q6: Not quite.
  - "Free hosting" is wrong. It must run on the club's existing Synology NAS (Docker is available), with a budget of 0 EUR per month.
  - The maintainer knows Python only, not general web skills. A successor must be able to take it over.
- Q7: Wrong on retention. History of lost items must be kept for 2 years for the insurance, not deleted after one season. GDPR applies: coach names and phone numbers are personal data, so data must stay on the club's own hardware, with no third-party cloud.
- Q8: It must be live for the start of the season on 1 March.
- Q9: Not quite. The e-mailed Monday report goes out, and there is the CSV export. Nothing else.
- Q10: Yes to both.

5. Central decision list: fine, go ahead with ADR 0001.

## DESIGNER

Thanks. You've answered Q1–Q10, and those answers add new needs and constraints, so the interview isn't finished. I haven't written any files this turn. Once the open questions close, I'll write everything you've confirmed.

## Two things to fix first

**Rank conflicts with the tie-breaker.** I proposed R-1, R-2, R-3, and you accepted it. But you said ease of use wins if only one of R-1 and R-3 can be fully met, which puts R-3 above R-1. Which order do you want? I'd recommend R-3, R-1, R-2, which matches the tie-breaker. Please set the order.

**Q2 was answered as "correct, but worse than patchy".** Offline check-out is a new need, so it's triaged below.

## Triage of the new needs

| ID | need (from your answers) | outcome | reason |
|---|---|---|---|
| R-4 | Check-out and check-in work offline and sync when the phone is back online (Q2) | system-level | Changes where data lives and how it syncs. |
| R-5 | Lost-item history kept for 2 years (Q7) | system-level | Shapes the data model and retention. |
| R-6 | Overdue report e-mailed every Monday morning (Q4, Q9) | system-level | Adds e-mail as an external system and a scheduled job. |
| R-7 | Warning 30 days before first-aid item expiry (Q4) | feature-level under R-6 | Reuses R-6's mail and scheduling; adds one date field. |
| R-8 | Yearly CSV inventory export for the treasurer (Q4) | system-level | An export format is a central decision and needs versioning. |
| R-9 | Any coach checks out; only the kit manager adds items and sees the full history (Q3) | system-level | Crosses the system: identity and access. |
| R-10 | A successor who knows Python can take it over (Q6) | system-level | Drives maintainability and the choice of structure. |

**Constraints for section 2 (proposed):** runs on the club's Synology NAS with Docker; 0 EUR per month; personal data stays on the club's hardware, with no third-party cloud; maintainer knows Python only; live for 1 March.

**Out of scope for section 3:** any money handling (no deposits, fines or payments).

**Stakeholders to add:** coaches (users), kit manager (admin), treasurer (CSV), insurer (lost-item history), maintainer, successor.

## Rank and conflicts (proposal)

Pending your order for R-1 to R-3, the new rows would be ranked after them: R-4, R-9, R-6, R-8, R-5, R-10. Ask your order. New conflicts:

- **R-2 against R-4:** offline, you can't see other coaches' check-outs. Tie-breaker: **if only one of R-2 and R-4 can be fully met, which?**
- **R-9 against R-3:** a login adds steps against the 3-tap limit. Tie-breaker: **if only one of R-3 and R-9 can be fully met, which?**

## Goals (candidates for the new needs)

- **C-3, Reliability: fault tolerance** (R-4, R-5). Stimulus: the signal drops during a check-out. Response: the check-out stays on the phone and syncs later. **Open question:** what would show R-4 is met? I suggest "0 lost check-outs in 50 offline trials."
- **C-4, Security: confidentiality** (R-9, personal-data constraint). Stimulus: a coach who is not kit manager asks for the full history. Response: it is refused. **Open question:** I suggest "0 unauthorised reads in 50 attempts."
- **C-5, Maintainability: analysability** (R-10). **Open question:** what would show R-10 is met? For example, "a Python developer finds and changes the CSV columns in under N hours." Please give N.

The goals keep their numbers QG-1 to QG-5 when written. QG-1 and QG-2 are already confirmed.

## Interview, round 2

❓ **Q11** - **Identity**: How does a coach identify themselves on the phone? Personal login, or a name picked once?

➡️ A personal login, remembered on the phone. Offline check-out works after one online login.

❓ **Q12** - **QR codes**: Does each physical unit get a code (every ball), or does each set (a bag of cones, a bag of bibs) get one?

➡️ Each ball and each first-aid bag gets its own code; each bag of cones or bibs gets one code.

❓ **Q13** - **Due times**: How long may kit be out before it's overdue? Per item type, or per check-out?

➡️ Per item type, set by the kit manager. Default: 7 days.

❓ **Q14** - **Report recipients**: Who gets the Monday report, and does it list only overdue items or all items?

➡️ The kit manager only, listing overdue items only.

❓ **Q15** - **Mail**: Which mail account sends the report and the warnings? Does the club's mail host offer SMTP?

➡️ The club's existing mail account, through its SMTP server, with credentials kept on the NAS.

❓ **Q16** - **Expiry warnings**: Who gets them, and who enters the expiry dates?

➡️ The kit manager gets them, and enters the date for each first-aid bag.

❓ **Q17** - **Lost items**: What counts as lost, and what events are kept for 2 years?

➡️ Lost means overdue and not returned after 30 days; the kit manager marks it. Kept: every check-out and check-in with coach and time.

❓ **Q18** - **Personal data**: Are phone numbers needed in the tool, or are names enough?

➡️ Names only. Phone numbers stay in the club's existing contacts. The purpose of the 2-year history is insurance.

❓ **Q19** - **NAS and backups**: Is Docker (Container Manager) enabled on the NAS, and is there a nightly backup?

➡️ Yes to both; the 2-year history is included in the backup.

❓ **Q20** - **Conflicts**: If two coaches check out the same bag while offline, whose check-out wins?

➡️ Both are recorded, and the second is flagged for the kit manager.

## What I need from you

1. The rank order of R-1 to R-3, given the tie-breaker.
2. The tie-breaker answers for R-2 against R-4, and R-3 against R-9.
3. The triage of R-4 to R-10 and the feature-level R-7 under R-6.
4. The constraints, out-of-scope items, and stakeholders above.
5. The measure values for C-3, C-4 and C-5, including N.
6. The answers to Q11–Q20.

ADR 0001's central list stays as drafted; it is written with the rest.

## ARCHITECT

1. Agreed: R-3, R-1, R-2.

2. R-2 against R-4: offline wins (R-4), because there is often no signal at the pitch. R-3 against R-9: ease of use wins (R-3). A check-out must take at most 3 taps and under 15 seconds.

3. Triage of R-4 to R-10, with R-7 under R-6: fine.

4. Constraints, out-of-scope items and stakeholders: fine.

5. Measures: C-3 and C-4 are fine as you suggested. For C-5, no preference on N. One working day sounds reasonable to me.

6. Q11-Q20:
- Q11: Fine, as long as the remembered login doesn't add taps beyond the 3.
- Q12: Fine.
- Q13: Fine.
- Q14: Fine.
- Q15: Fine, no preference.
- Q16: Fine.
- Q17: Fine.
- Q18: Not quite. Coaches' names and phone numbers are both personal data under GDPR. Whatever the tool holds must stay on the club's own hardware, with no third-party cloud.
- Q19: Yes to both, fine.
- Q20: Fine.

## DESIGNER

Thanks. Most of the round is settled, so I'll record what's confirmed and ask about the two points that remain open. I still haven't written any files, because the round isn't closed.

## Confirmed so far

- **Tie-breakers:** R-4 beats R-2 when only one can be fully met. R-3 beats R-9 when only one can be fully met.
- **Goals:** QG-1 (correctness, from R-1 and R-2) with "0 wrong holders in 50 test check-outs". QG-2 (learnability, from R-3) with "at most 3 taps and under 15 seconds". C-3 (fault tolerance, from R-4 and R-5) with "0 lost check-outs in 50 offline trials". C-4 (confidentiality, from R-9) with "0 unauthorised reads in 50 attempts". C-5 (analysability, from R-10) with "one working day" as N.
- **Q11:** the remembered login must add no taps beyond the 3. I'll write that into QS-2's measure.
- **Constraints, out-of-scope items, stakeholders, and the new triage:** as you accepted them.

## Still open

**Rank conflict.** You agreed the order R-3, R-1, R-2, but you also said offline (R-4) beats R-2 in a conflict. That means R-4 has to rank above R-2. The rest of the new rows also have no agreed order yet.

❓ **Q21** - **Rank of R-4 to R-10**: Where do R-4 and the rest go?

➡️ R-3, R-1, R-4, R-2, R-9, R-6, R-5, R-8, R-10. R-7 has no row of its own; it sits under R-6.

**Phone numbers.** Your Q18 answer says both names and phone numbers are personal data, but it doesn't say whether the tool holds phone numbers. Without that, I can't write the data constraint or the retention rule.

❓ **Q22** - **Phone numbers**: Does the tool hold phone numbers?

➡️ No. It holds names only. Phone numbers stay in the club's own contacts, outside the tool.

If you answer Q21 and Q22 as recommended, or change them, I'll close the round and write what you've confirmed: the R-list, QG-1 to QG-5 and their scenarios, the constraints, the out-of-scope items, the stakeholders, and ADR 0001 with status `proposed`.

## ARCHITECT

1. Q21: Agreed, the order is R-3, R-1, R-4, R-2, R-9, R-6, R-5, R-8, R-10, with R-7 under R-6.

2. Q22: Names only is fine with me. Names and phone numbers are both personal data under GDPR, so whatever the tool holds must stay on the club's NAS, with no third-party cloud.

Please go ahead and write the files.

## DESIGNER

The architecture documents are written. Nothing is committed.

**Files written**
- `docs/architecture/arc42.md`: the full arc42 file, with the R-list, quality goals, stakeholders, constraints, out-of-scope items, and quality scenarios you confirmed.
- `docs/adr/0001-record-architecture-decisions.md`: status `proposed`. It needs your approval of its text before any decision on its list is made.
- `.scratch/requirements/issues/01-expiry-warning.md`: the expiry warning, filed as feature-level under R-6. No issue tracker is configured in this repo, so it went here.

**Waiting for you**
- Approve the text of ADR 0001. Until you do, the work on each decision on its list waits, including the storage format, the CSV format, and the sync format.

**Things to check**
- **R-7 is skipped.** The expiry warning is feature-level, so it has no R-ID. I used the label R-7 for it during triage, so the R-list goes R-6 to R-8 with a gap. The note in section 1 says so.
- **QG-2 is labelled "learnability", but its measure tests operability** (3 taps and under 15 seconds). Should the label change to "operability"?
- **The 2-year history of coaches' names needs a stated purpose under GDPR.** The insurance purpose is not written down anywhere yet. I'd suggest we add it to the arc42 constraints once you've agreed on the wording.

## ARCHITECT

1. ADR 0001: Approved.

2. QG-2: yes, change the label to "operability". The point is 3 taps and under 15 seconds, scanning the QR code on the kit bag.

3. GDPR purpose: yes, add it. Coaches' names in the history are kept for 2 years for insurance, to show who had a lost item. The data stays on the club's NAS, with no third-party cloud.

4. R-7 gap: fine, as long as the note in section 1 explains it.

## DESIGNER

All four changes are in, and the setup is complete.

- **ADR 0001** is now `accepted 2026-11-23`. I used today's date from the environment.
- **QG-2** is now "Usability: operability". Its scenario (QS-2) already states the 3 taps, under 15 seconds, and the QR scan.
- **GDPR purpose** is added to section 2 of `docs/architecture/arc42.md`: coaches' names in the lost-item history are kept for 2 years to show who had a lost item, for the insurance, and the data stays on the club's NAS.
- **R-7 gap:** the note in section 1 already explains it, so I left it as it is.

The decisions on ADR 0001's list (storage, CSV format, sync format, interfaces, conventions, dependencies) are now open for their own ADRs. Nothing is committed.

## ARCHITECT

Approved.