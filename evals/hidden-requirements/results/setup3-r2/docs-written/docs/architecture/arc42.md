# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check items out and back in; every check-out and check-in is recorded. | 1 | active | the core of the tool |
| R-2 | Anyone can see which coach holds each item and what is in the store. | 2 | active | the stated problem: nobody knows which coach has what |
| R-3 | A coach can check an item out or in without training. | 3 | active | the tool must be easy to use |
| R-4 | Check-out and check-in work without network and sync when the phone is back online. | 4 | active | the pitch has no signal |
| R-5 | Every Monday morning the overdue report is e-mailed to the kit manager. | 5 | active | the kit manager's weekly check |
| R-6 | Only the kit manager may edit or delete records. | 6 | active | coaches must not change records |
| R-7 | The treasurer can export the yearly inventory as CSV for the insurance audit. | 7 | active | the insurance audit |
| R-8 | A Python developer who did not build the tool can maintain it. | 8 | active | one volunteer maintains it; a successor must be able to take over |
| R-9 | Condition and repairs of kit are recorded. | – | deferred | the architect: can wait |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1, R-2 | QS-2 |
| QG-2 | Interaction capability: learnability | R-3 | QS-1 |
| QG-3 | Security: accountability | R-2, R-6 | QS-3 |
| QG-4 | Reliability: fault tolerance | R-4 | QS-4 |
| QG-5 | Security: integrity | R-6 | QS-5 |
| QG-6 | Maintainability: analysability | R-8 | open: measure not yet set |

Rows are in ID order; the architect has not yet set the order of the goals.

### Stakeholders

- **Kit manager:** the architect. Edits and deletes records, sees coaches' phone numbers, enters expiry dates, receives the Monday report.
- **Coaches:** about 40 volunteers, using their own phones at the pitch. Some are not tech-savvy and get no training.
- **Treasurer:** takes the yearly CSV export for the insurance audit.
- **Maintainer:** one volunteer who knows Python only; the successor takes over.

## 2. Constraints

- Runs on the club's existing Synology NAS, in Docker.
- Costs 0 EUR per month. No third-party cloud: the data stays on the club's own hardware.
- The Monday report goes through the club's existing mail account, at no extra cost.
- About 40 coaches and about 300 items. Performance is not a concern.
- Maintained by one volunteer who knows Python only; a successor must be able to take it over.
- Live for the start of the season on 1 March 2027.
- Coach names and phone numbers are personal data under GDPR.
- Lost-item history is kept for 2 years, for the insurance. Coach names are removed when the coach leaves; the history stays usable.

## 3. Context and scope

Out of scope: money. No deposits, fines or payments.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `../adr/`. The decisions made centrally are listed in the [Record architecture decisions](../adr/0001-record-architecture-decisions.md) ADR, which is `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a volunteer coach with no training and little experience of phones checks out a bag by scanning its QR code | at the pitch | the check-out is recorded under the coach's name | at most 3 taps and under 15 seconds, measured with first-time volunteers |
| QS-2 | QG-1 | the coach reports a wrong check-out to the kit manager | normal operation | the kit manager corrects the record; the history keeps the original and the correction | the correction takes at most 2 taps by the kit manager; the history is kept |
| QS-3 | QG-3 | a coach or the kit manager changes a record | normal operation | the change is stored with the name of the person who made it | 0 unattributed changes in the audit log in tests |
| QS-4 | QG-4 | a coach checks out or in with the phone in airplane mode | at the pitch, without network | the change is stored on the phone and reaches the NAS after reconnect | 100% of check-outs and check-ins succeed in airplane mode; records reach the NAS within 5 minutes of reconnect |
| QS-5 | QG-5 | a coach tries to edit or delete a record | normal operation | the change is refused | a non-manager edit or delete is refused in 100% of tests |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
