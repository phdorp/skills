# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out and back in, so the club always knows where each item is and which coach has it. | 1 | active | The purpose of the tool. Track balls, bibs, cones and first-aid bags (feature-level, issue `.scratch/requirements/issues/01-track-kit-types.md`). |
| R-2 | Checking out an item takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. | 2 | active | Many volunteers are not tech-savvy; the tool is only used if check-out is quick. |
| R-3 | Check-out and check-in work offline and sync when the phone is back online. | 3 | active | Many pitches have no mobile signal at all. Conflicts with R-1 while offline; R-1 wins. |
| R-4 | Coach names and phone numbers are protected as GDPR personal data. A phone number is deleted when the coach leaves. | 4 | active | GDPR applies; data stays on club hardware. Only the kit manager sees phone numbers. |
| R-5 | Records survive a crash, and no check-out that has already synced may be lost. | 5 | active | Kit records must not disappear. The NAS backup status is unknown (section 11). |
| R-6 | Any coach may add a record; only the kit manager may correct or delete one. | 6 | active | Protects the record from accidental or unauthorised edits. |
| R-7 | The kit manager gets an overdue report by e-mail every Monday morning. An item is overdue when it is not checked in within 7 days of check-out. Expiry warning 30 days before a first-aid item expires (feature-level, issue `.scratch/requirements/issues/02-expiry-warning.md`). | 7 | active | Makes overdue kit visible without anyone checking. |
| R-8 | A yearly inventory CSV export, for the treasurer and the insurance audit. | 8 | active | The insurer receives the CSV via the treasurer. |
| R-9 | A volunteer who knows Python can understand, change and hand over the tool. | 9 | active | One maintainer now; a successor must be able to take over. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional Suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Interaction capability: operability | R-2 | QS-2 |
| QG-3 | Reliability: fault tolerance | R-3 | QS-3 |
| QG-4 | Reliability: recoverability | R-5 | QS-4 |
| QG-5 | Security: confidentiality | R-4 | QS-5 |

Ruled out: Performance efficiency (time behaviour and capacity). Reason: the scale is small (about 300 items, 40 coaches), and the architect says performance is not a concern. The 15-second check-out limit under QG-2 still applies.

### Stakeholders

- **Kit manager** (the architect): sets the requirements, corrects and deletes records, and receives the Monday overdue report.
- **Maintainer**: one volunteer who knows Python, and the successor who takes over.
- **Coaches**: about 40 people who check kit out and back in with their own phones at the pitch.
- **Treasurer**: receives the yearly inventory CSV and passes it to the insurer.

## 2. Constraints

- The tool runs on the club's existing Synology NAS, in Docker.
- Running cost: 0 EUR per month.
- No third-party cloud: data stays on club hardware.
- One volunteer maintains it, and it must be handed over to the next maintainer. That volunteer knows Python only.
- It must be live by 1 March, the start of the season.
- GDPR applies to coach names and phone numbers.
- Lost-item history is kept for 2 years (insurance).

## 3. Context and scope

Inside the system: the check-out and check-in app on coaches' phones, the record store on the club's NAS, the Monday overdue report, and the yearly CSV export.

Outside the system:
- the printed QR codes on the kit bags (the kit manager prints them);
- the treasurer, who receives the CSV and passes it to the insurer;
- the club's mail provider, if the report is sent through it (see section 11).

Scale: about 300 items, about 40 coaches, and about 5,000 check-out and check-in events per season.

Out of scope:
- Money handling: deposits, fines, payments.
- Tracking players.
- Buying or valuing kit.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are ADRs in `../adr/`. The "Record architecture decisions" ADR, which lists the decisions made centrally, is [ADR 0001](../adr/0001-record-architecture-decisions.md) and is `proposed` until you approve its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks an item out or back in during the season | normal operation | the record names the item's holder and status correctly | 0 wrong holders in a spot check of 20 random items |
| QS-2 | QG-2 | a coach checks an item out by scanning its QR code | normal operation | the check-out is recorded | at most 3 taps and under 15 seconds per check-out |
| QS-3 | QG-3 | a coach checks an item out or in with no mobile signal, and the phone later reconnects | no mobile signal at the pitch | the event is kept on the phone and synced once online | 0 check-outs lost across 50 offline-then-sync cycles |
| QS-4 | QG-4 | the process is killed during a check-out write | normal operation | the record is either fully stored or absent, and the store still opens | 0 lost synced check-outs and 0 unreadable stores in 100 kill-during-write trials |
| QS-5 | QG-5 | a request for a coach's phone number comes from an account other than the kit manager's | normal operation | the number is not returned | 0 of 20 test requests by non-manager accounts return a phone number |

## 11. Risks and technical debt

- **The Monday report may leave club hardware.** If the club's mail provider counts as a third-party cloud, the report breaks "no third-party cloud" and the confidentiality goal (QG-5). Whether the NAS can send mail itself is not yet known. Threatens: R-4, QG-5, C "no third-party cloud".
- **The NAS backup status is unknown.** Records can be lost if the NAS fails. Threatens: R-5, QG-4.
- **Offline conflicts.** While a phone is offline, its check-outs are not visible to others until sync, and two offline check-outs of the same item conflict. Both events are kept and the item is flagged for the kit manager. Threatens: R-1 (stale holder until sync), R-3.
- **One maintainer.** The tool depends on a single volunteer. Threatens: R-9.
- **Hard date.** It must be live by 1 March. Threatens: the constraint on the date.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
