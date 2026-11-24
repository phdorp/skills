# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out and back in | 1 | active | The core action; nothing else works without it. |
| R-2 | The current holder of each item is visible at any time | 4 | active | The club cannot tell who has what, which is the problem. |
| R-3 | A check-out takes at most 3 taps and under 15 seconds, by scanning the QR code on the bag | 2 | active | Many volunteers are not tech-savvy; it governs how R-1 is delivered. |
| R-4 | Scheduled e-mails: a Monday-morning overdue report and a warning 30 days before first-aid expiry dates | 7 | active | A new outbound channel with credentials, running unattended on the NAS. |
| R-5 | A yearly CSV inventory export for the treasurer's insurance audit | 6 | active | Required by the insurance audit. |
| R-6 | Check-out and lost-item history kept for 2 years | 5 | active | Required by the insurance; GDPR limits how long personal data is kept. |
| R-7 | Check-out and check-in work offline and sync when the phone is back online | 3 | active | The pitch often has no mobile signal. |
| R-8 | A successor can take over the tool | 8 | active | One volunteer maintainer, who knows only Python. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional completeness | R-1, R-2, R-4, R-5 | QS-1 |
| QG-2 | Interaction capability: operability | R-3 | QS-2 |
| QG-3 | Reliability: recoverability | R-7 | QS-3 |
| QG-4 | Security: accountability | R-1 | QS-4 |
| QG-5 | Maintainability: analysability | R-8 | QS-5 |

### Stakeholders

| role | expectation |
|---|---|
| Coaches (about 40) | Check kit out and in with at most 3 taps at the pitch, even without signal. |
| Kit manager | See who holds each item; declare items lost; enter expiry dates; the only one who sees coaches' phone numbers, and only for overdue or lost items. |
| Treasurer | A yearly CSV inventory export for the insurance audit. |
| Maintainer (volunteer) | Keep the tool running; hand it to a successor who knows only Python. |

## 2. Constraints

- **C-1:** Runs on the club's existing Synology NAS, in Docker.
- **C-2:** Budget 0 EUR per month. No free hosting and no third-party cloud.
- **C-3:** Coaches' names and phone numbers stay on the club's own hardware. GDPR applies.
- **C-4:** Live for the start of the season on 1 March.
- **C-5:** Python is the implementation language, because the maintainer and any successor know only Python.

## 3. Context and scope

Out of scope:

- Money handling: no deposits, fines or payments.
- Purchasing.
- Membership or player records.
- Integration with other systems in v1; none are known.

Outside the system: the treasurer receives the CSV export; the insurer receives it only through the treasurer.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in [`docs/adr/`](../adr/). The list of decisions made centrally
is in the ADR "Record architecture decisions" ([`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md)),
proposed and waiting for the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks an item out or in | a trial season of normal operation | every check-out and check-in is recorded and appears in the inventory | 0 unrecorded check-outs in a trial season |
| QS-2 | QG-2 | a volunteer who is not tech-savvy scans a bag's QR code and checks it out | 5 volunteers, 3 check-outs each (15 trials), at the pitch | the check-out is recorded | 15 of 15 check-outs within 3 taps and under 15 seconds |
| QS-3 | QG-3 | a check-out and a check-in are made with no signal, then the phone reconnects | 100 offline check-outs, each followed by a sync | each is kept and synced; a conflicting second check-out is flagged for the kit manager | 0 lost check-outs in 100 |
| QS-4 | QG-4 | any check-out | normal operation | the record names the coach | 100% of check-outs carry the coach's name |
| QS-5 | QG-5 | a successor who did not write the code reads the docs and makes one change | the documented codebase | the change is made and tested | done within 2 hours of reading the docs |

## 11. Risks and technical debt

- **No coach login (accountability):** a check-out names the coach chosen once per phone, not an
  authenticated person. A coach could check out an item in another coach's name. Threatens QG-4.
- **Offline view (R-2):** while offline, the holder shown may be out of date; the view shows the
  last synced time. Threatens R-2.
- **Single maintainer (R-8):** one volunteer, Python only. Threatens QG-5.
- **E-mail sender (R-4):** the club's e-mail account is not yet confirmed. Threatens R-4 and C-2.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
