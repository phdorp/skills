# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out and back in, and the club can see at any time who holds each item. Item types (balls, bibs, cones, first-aid bags) are tracked. | 2 | active | Brief; confirmed as system-level (setup, Q11) |
| R-2 | Coaches can use the tool with little or no training: checking out an item takes at most 3 taps and under 15 seconds, by scanning the QR code on the kit bag. | 1 | active | Brief; confirmed as system-level and ranked first (setup, Q11) |
| R-3 | Check-out and check-in work without signal and sync when the phone is back online. No record may be lost. | 3 (proposed) | active | Setup, Q2 and Q3 |
| R-4 | The kit manager receives an overdue report by e-mail every Monday morning. | 4 (proposed) | active | Setup, Q3 and Q9 |
| R-5 | The treasurer can export a yearly inventory as CSV for the insurance audit. | 5 (proposed) | active | Setup, Q9 |
| R-6 | Loan and loss history is kept for 2 years, for the insurance. | 6 (proposed) | active | Setup, Q7 and Q10 |
| R-7 | A successor who knows only Python can take over maintaining the tool. | 7 (proposed) | active | Setup, Q6 |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Interaction capability: learnability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Reliability: recoverability | R-3 | QS-3 |
| QG-4 | Security: accountability | R-1, R-6 | QS-4 |
| QG-5 | Maintainability: analysability and modifiability | R-7 | QS-5 |

Performance efficiency is ruled out beyond the 15-second check-out measure in QS-1, by the architect's decision (setup, Q1 and Q10).

### Stakeholders

- **Coaches**: about 40 volunteers who check kit out and back in.
- **Kit manager**: runs the equipment and receives the Monday overdue report.
- **Treasurer**: exports the yearly inventory for the insurance audit.
- **Insurer**: audits the loan and loss history.
- **Successor maintainer**: a volunteer who knows only Python and takes over maintaining the tool.

## 2. Constraints

- The tool runs on the club's existing Synology NAS, in Docker.
- The tool is written in Python.
- The budget is 0 EUR per month.
- Personal data (coach names and phone numbers) is subject to GDPR. It stays on the club's own hardware, with no third-party cloud.
- The first version is live for the start of the season on 1 March 2027.

## 3. Context and scope

Out of scope: payments, deposits and fines; access for parents or players; GPS tracking of kit.

Figures: about 40 coaches; about 300 items.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The architecture decisions are in [docs/adr/](../adr/). The list of decisions made centrally is in the ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks out one item by scanning the QR code on its bag | normal use at the pitch | the check-out is recorded | at most 3 taps and under 15 seconds |
| QS-2 | QG-2 | a coach enters a check-out or check-in | normal operation | the stored record equals what was entered | 0 mismatches in 100 trials |
| QS-3 | QG-3 | the phone loses signal during a check-out or check-in, then reconnects | offline use | the record is kept on the phone and synced later, with no record lost | 0 records lost in 100 offline entries, each synced later |
| QS-4 | QG-4 | a loan or loss recorded two years earlier is looked up | normal operation | the loan record is still available, with the coach who made it | 0 loan records missing within the 2-year window in a retention test |
| QS-5 | QG-5 | a Python developer new to the project is asked to explain and change one screen | the repository and its documentation | the screen is explained and changed | within one day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
