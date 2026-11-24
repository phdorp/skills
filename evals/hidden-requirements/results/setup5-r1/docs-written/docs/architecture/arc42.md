# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches record when they check equipment out and back in, and who has it. | 1 | active | Core: nothing else works without it. |
| R-2 | Anyone can see at any time which coach holds each item. | 4 | active | The purpose of the tool. |
| R-3 | A coach can check equipment out or in without training or help. | 3 | active | Easy to use wins over R-4 (architect's decision). |
| R-4 | Only club members can see the data. Each coach has a personal login, which takes one step after the first time. | 5 | active | Club data stays with club members. |
| R-5 | Check-out and check-in work with no mobile signal and sync when the phone is back online. | 2 | active | Coaches often have no signal at the pitch. Wins over R-2 if they conflict. |
| R-6 | The equipment manager receives an e-mail of overdue items every Monday morning. An item is overdue 7 days after check-out. | 6 | active | Overdue equipment must be followed up. |
| R-7 | The treasurer receives a yearly inventory export as CSV. | 7 | active | Treasurer's yearly stock count. |
| R-8 | A Python-only successor can change and deploy the tool in under 2 hours, using written setup steps. | 8 | active | One volunteer maintains it; a successor must be able to take over. |
| R-9 | Check-out and loss records older than 2 years are deleted; the item list is kept. | 9 | active | Insurance needs 2 years of loss history; GDPR limits personal data. |

### Quality goals

Performance efficiency (time behaviour, resource use, capacity) is not a goal: ruled out by the architect, as performance is no concern at this size (up to 1,000 items and 60 coaches).

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1, R-2 | QS-1 |
| QG-2 | Interaction capability: operability | R-3 | QS-2 |
| QG-3 | Reliability: availability | R-5 | QS-3 |
| QG-4 | Security: confidentiality | R-4 | QS-4 |
| QG-5 | Security: accountability | R-2 (issue 02) | QS-5 |
| QG-6 | Reliability: recoverability | R-2 | QS-6 |
| QG-7 | Maintainability: modifiability | R-8 | QS-7 |

### Stakeholders

- Coaches: about 40 volunteers, on their own phones at the pitch, often with no signal.
- Equipment manager (the architect): keeps the coach list and receives the overdue report and expiry warnings.
- Maintainer: one volunteer who knows only Python; a successor takes over.
- Treasurer: receives the yearly inventory CSV.
- Insurer: needs the loss history in the format item, date, coach, note.

## 2. Constraints

- Runs on the club's existing Synology NAS, in Docker.
- Budget 0 EUR a month.
- No third-party cloud.
- Implemented in Python; the maintainer and any successor know only Python.
- Personal data stays on the club's own hardware; GDPR applies.
- Live for the start of the season on 1 March 2027.

## 3. Context and scope

Non-goals (out of scope):

- No money of any kind: no deposits, fines or payments.
- No tracking of players.

Sizing: about 40 coaches and about 300 items now. Ceiling for design: 1,000 items and 60 coaches.

Outside the system:

- Coaches' phones, which reach the NAS when they have signal. Open: whether phones can reach the NAS from outside the club (not yet confirmed).
- The club's existing e-mail account, which sends the overdue report and the expiry warning. Open: confirm that it can send them.
- The treasurer, who receives the CSV export.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The list of decisions made centrally is in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks out or in 200 items in a test run | normal operation | the overview shows the correct holder for every item | 0 items shown with the wrong holder |
| QS-2 | QG-2 | a coach with no training scans the QR code on a kit bag to check out one item | at the pitch, normal operation | the item is checked out | at most 3 taps and under 15 seconds |
| QS-3 | QG-3 | a coach checks out or in with no mobile signal, and the signal returns | at the pitch, no signal | the action completes on the phone and syncs | 100% of offline actions complete; sync within 5 minutes of signal |
| QS-4 | QG-4 | a non-member asks for the data | normal operation | access is denied | 0 of 10 test attempts show any record |
| QS-5 | QG-5 | 200 check-out events in a test run | normal operation | every event names the coach | 100% of events name a coach |
| QS-6 | QG-6 | the app is restarted 100 times during use | normal operation | recorded check-outs remain | 0 recorded check-outs lost in 100 restarts |
| QS-7 | QG-7 | a Python-only successor makes a change and deploys it, using the written setup steps | normal operation | the change is deployed | under 2 hours |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
