# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Each item's holder and location can be seen at any time, and each check-out or check-in is recorded with the coach's name and time. | 3 | active | The purpose of the tool: the club always knows where its kit is. |
| R-2 | Checking out an item takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. | 1 | active | Volunteers drop the tool if it is slow. In a conflict with R-1, R-2 is kept. |
| R-3 | Check-out and check-in work without a signal and sync when the phone is back online. | 2 | active | Offline check-out has to work at the pitch. In a conflict with R-1, R-3 is kept: a clash between two phones over the same item is flagged to the kit manager, not blocked. |
| R-4 | Only the equipment manager sees all coaches' data. | 4 | active | Coach names and phone numbers are personal data. |
| R-5 | The check-out history is never lost. | 5 | active | The history is kept 2 years for insurance. |
| R-6 | A successor who knows Python can understand and change the tool without the current maintainer. | 6 | active | The tool must outlive its first maintainer. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Security: accountability | R-1 | QS-2 |
| QG-3 | Interaction capability: operability | R-2 | QS-3 |
| QG-4 | Reliability: availability | R-3 | QS-4 |
| QG-5 | Security: confidentiality | R-4 | QS-5 |
| QG-6 | Reliability: recoverability | R-5 | QS-6 |
| QG-7 | Maintainability: analysability | R-6 | QS-7 |

### Stakeholders

- **Coaches** (about 40): check kit out and back in, on phones at the pitch.
- **Equipment manager** (the kit manager): runs the kit; the only one who sees all coaches' data; receives the Monday report and the first-aid expiry warnings.
- **Treasurer**: needs the yearly inventory CSV export.
- **Club committee**: needs nothing day to day from the tool; decides on budget and personal data.
- **Volunteer maintainer** (knows only Python) and their **successor**.

## 2. Constraints

- Runs on the club's existing Synology NAS, with Docker available.
- Budget: 0 EUR per month.
- Data stays on club hardware; no third-party cloud.
- Coach names and phone numbers are personal data under the GDPR and are kept on club hardware only.
- The history of lost items is kept for 2 years for insurance purposes, not deleted at season end.
- Must be live for the start of the season on 1 March 2027.
- Written in Python and kept simple, so that a successor can take it over.

## 3. Context and scope

Out of scope:

- No money handling: no deposits, fines or payments.
- No team or membership management.
- No scheduling of training or matches.
- No link to a member list.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`../adr/`](../adr/). The "Record architecture decisions" ADR is [0001](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks an item out or in during a training session | normal operation at the pitch | the record shows the item as held by that coach, or as in store; a clash between two phones is flagged | every clash is flagged; 0 unflagged mismatches between the records and a physical count after 10 sessions |
| QS-2 | QG-2 | a coach checks an item out | normal operation at the pitch | the record names that coach and the time | 0 check-outs without a named coach in 10 sessions |
| QS-3 | QG-3 | a coach scans the QR code on a kit bag and checks the item out | normal operation at the pitch | the check-out is saved | at most 3 taps and under 15 seconds from the scan to the saved check-out |
| QS-4 | QG-4 | a coach checks items out and in with no signal for 2 hours | offline at the pitch | the check-outs are kept and synced when the signal returns | 0 check-outs lost after 2 hours offline, synced within 10 minutes of signal returning |
| QS-5 | QG-5 | a coach account requests the data of all coaches | normal operation | the request is refused | 0 coach accounts can see another coach's data in an access test |
| QS-6 | QG-6 | the storage is restored from backup after a failure | normal operation | the check-out history is restored | after a restore from backup, 0 records lost |
| QS-7 | QG-7 | a new Python volunteer makes a small change | without the current maintainer | the change is made | a small change is made within one day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
