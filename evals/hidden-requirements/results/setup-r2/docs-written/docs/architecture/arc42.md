# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out to themselves and back in. | 1 | active | The core mechanism; R-2 depends on it. |
| R-2 | The club always knows where each item is and which coach holds it. | 3 | active | The problem the README states. |
| R-3 | Coaches can check kit out or in without a briefing. | 2 | active | Shapes the interface and platform. Wins over R-2 in a conflict (architect's tie-breaker). |
| R-4 | The treasurer can export a yearly kit inventory as CSV for the insurance audit. | 5 | active | Requested by the architect in the gap question on interoperability. |
| R-5 | Check-out and check-in work without a mobile signal and sync once the phone is back online. | 4 | active | The sideline often has no mobile signal. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Interaction capability: learnability and operability | R-3 | QS-1 |
| QG-2 | Performance efficiency: time behaviour | R-3 | QS-2 |
| QG-3 | Security: accountability | R-2 | QS-3 |
| QG-4 | Reliability: availability | R-5 | QS-4 |
| QG-5 | Compatibility: interoperability | R-4 | QS-5 |
| QG-6 | Functional suitability: functional correctness | R-2 | QS-6 |

### Stakeholders

- Coaches: check kit out and back in on the sideline.
- Treasurer: exports the yearly kit inventory for the insurance audit.
- Equipment manager: runs the club's kit and makes the architecture decisions.

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`docs/adr/`](../adr/). The ADR that lists the decisions made centrally is
[Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a first-time volunteer, with no help and no training, scans the QR code on the kit bag to check out an item | sideline; the phone may have no signal | the check-out is recorded | at most 3 taps |
| QS-2 | QG-2 | a coach scans the QR code on the kit bag to check out an item | sideline; no mobile signal | the check-out is recorded on the phone | under 15 seconds |
| QS-3 | QG-3 | a coach checks an item out or back in | normal use | the record names the coach; no login is needed | 100% of check-out and check-in records carry a coach name |
| QS-4 | QG-4 | the phone loses its signal during a check-out or check-in at the pitch | sideline; no mobile signal | the record is kept on the phone and syncs once the phone is back online | 100% of records made offline reach the shared record after reconnection |
| QS-5 | QG-5 | the treasurer exports the yearly kit inventory | end of the year, before the insurance audit | a CSV is produced with one row per item and its holder | 100% of items appear in the CSV, each with its holder |
| QS-6 | QG-6 | a full kit count compares each item with its record | normal use | the record shows the coach who actually holds the item | 0 items whose recorded holder differs from the holder found in the count |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
