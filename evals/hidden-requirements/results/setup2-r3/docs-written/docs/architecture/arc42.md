# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out and back in. | 2 | active | Core purpose: kit disappears because nobody knows who has what. |
| R-2 | Always know where each item is and who has it. | 4 | active | Core purpose; depends on the check-out data of R-1. |
| R-3 | Easy to use for volunteers. | 1 | active | Ease of use wins over R-1 and R-9 when only one can be fully met. |
| R-4 | Check-out and check-in work offline and sync when the phone is back online. | 3 | active | Often no signal at the pitch; wins over R-2 when only one can be fully met. |
| R-5 | Lost-item history is kept for 2 years. | 7 | active | Insurance requirement. |
| R-6 | An overdue report is e-mailed every Monday morning. | 6 | active | The kit manager's weekly control. |
| R-8 | A yearly inventory export as CSV for the treasurer's insurance audit. | 8 | active | Insurance audit. |
| R-9 | Any coach checks out; only the kit manager adds items and sees the full history. | 5 | active | Access control; loses to R-3 when only one can be fully met. |
| R-10 | A successor who knows Python can take over and maintain the tool. | 9 | active | Continuity: the maintainer is a volunteer. |

R-7 is not used. The expiry warning for first-aid items is feature-level under R-6 and gets an
issue, not an R-ID.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: correctness | R-1, R-2 | QS-1 |
| QG-2 | Usability: operability | R-3 | QS-2 |
| QG-3 | Reliability: fault tolerance | R-4, R-5 | QS-3 |
| QG-4 | Security: confidentiality | R-9 | QS-4 |
| QG-5 | Maintainability: analysability | R-10 | QS-5 |

### Stakeholders

| stakeholder | role | concern |
|---|---|---|
| Coaches | use the tool at training and matches | check kit out in one scan, also without signal |
| Kit manager | runs the equipment; the only administrator | full history, reports, adds items |
| Treasurer | keeps the club's books | yearly CSV export for the audit |
| Insurer | audits lost items (external) | 2-year history of lost items |
| Maintainer | volunteer who builds and runs the tool, knows Python only | a codebase that stays maintainable |
| Successor | takes over maintenance | can learn the codebase in Python |

## 2. Constraints

- The tool runs on the club's Synology NAS with Docker (Container Manager). Budget: 0 EUR per month.
- Personal data (coaches' names; no phone numbers are held) stays on the club's NAS, with no
  third-party cloud. GDPR applies.
- Purpose of the personal data: coaches' names in the lost-item history are kept for 2 years,
  to show who had a lost item, for the insurance.
- The tool is written in Python; the maintainer knows Python only.
- E-mail is sent through the club's existing mail account, via its SMTP server.
- The tool is live for the start of the season on 1 March.

## 3. Context and scope

Out of scope:

- any money handling: no deposits, fines or payments;
- purchasing and tracking of fitness or size;
- links to the club's membership system;
- any e-mail or calendar integration beyond the Monday report and the expiry warnings;
- storing phone numbers.

External parties: the coaches' phones (clients), the club's NAS (host), the club's mail account
(SMTP), the treasurer (CSV export), the insurer (audit).

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in [`../adr/`](../adr/). The line between decisions made centrally
and decisions left to the building blocks is set by
[ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks out or checks in an item | normal operation | the record shows the correct holder and time | 0 wrong holders in 50 test check-outs |
| QS-2 | QG-2 | a coach scans the QR code on a kit bag to check it out | phone with a remembered login; the login adds no taps | the check-out is recorded | at most 3 taps and under 15 seconds |
| QS-3 | QG-3 | the phone loses signal during a check-out or check-in | phone offline | the event is kept on the phone and synced when the phone is back online | 0 lost check-outs in 50 offline trials |
| QS-4 | QG-4 | a coach who is not the kit manager asks for the full history | normal operation | the request is refused and no history is shown | 0 unauthorised reads in 50 attempts |
| QS-5 | QG-5 | a Python developer changes the columns of the CSV export | normal operation | the change is made and the tests pass | done in under one working day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
