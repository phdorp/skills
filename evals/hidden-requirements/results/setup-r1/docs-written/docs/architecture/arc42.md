# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out to themselves and back in. | 2 | active | creates the holder records the rest depends on |
| R-2 | The club can see, as of the last sync, which coach holds each item and where unheld items are. | 3 | active | the purpose of the tool |
| R-3 | A coach can check kit out or in without help or training. | 1 | active | decides the interface channel and the number of steps |
| R-4 | A coach identifies themselves at check-out without typing a password each time, within the limit of R-3. | 5 | active | no preference on how; must fit R-3's three taps and 15 seconds |
| R-5 | The history of check-outs and check-ins, with coach names, is kept for at least 2 years and survives failures. | 6 | active | the insurance needs two years of history of lost items |
| R-6 | The treasurer gets a yearly inventory export as CSV. | 7 | active | the insurance audit |
| R-7 | Check-out and check-in work offline and sync when the phone is back online. | 4 | active | phones at the pitch often have no mobile signal |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1, R-2, R-7 | QS-1 |
| QG-2 | Interaction capability: learnability | R-3 | QS-2 |
| QG-3 | Reliability: availability | R-7 | QS-3 |
| QG-4 | Reliability: recoverability | R-5 | QS-4 |
| QG-5 | Compatibility: interoperability | R-6 | QS-5 |

### Stakeholders

## 2. Constraints

- **Platform:** runs on the club's existing Synology NAS, with Docker.
- **Budget:** 0 EUR per month for software and hosting.
- **Personal data:** coach names and phone numbers are personal data (GDPR). All data stays on the
  club's own hardware; no third-party cloud service.
- **Language and handover:** Python only. The maintainer knows only Python, and a successor must be
  able to take over the code.
- **Size:** about 40 coaches and 300 items. Performance is not a concern.

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `docs/adr/`, linked from here as `../adr/`. The decisions the architect makes centrally
are listed in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md),
accepted 2026-11-23.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks an item out or in | normal operation | the recorded holder of the item matches who holds it | after every sync, the recorded holder is correct |
| QS-2 | QG-2 | a first-time coach scans the QR code on a kit bag and checks out one item | normal use at the pitch, on a phone | the check-out completes without help, in at most 3 taps and under 15 seconds | 9 of 10 first-time coaches succeed |
| QS-3 | QG-3 | a coach at the pitch with no mobile signal scans the QR code on a kit bag and checks out one item | offline, normal operation | the check-out is accepted on the phone and shows as held, in at most 3 taps and under 15 seconds | 100% of offline check-outs finish within 3 taps and 15 seconds |
| QS-4 | QG-4 | power is cut during a check-out or a sync | normal operation | every confirmed record is intact after restart, and the 2-year history is complete | 0 lost confirmed records in 10 power-cut trials |
| QS-5 | QG-5 | the treasurer exports the yearly inventory as CSV for the insurance audit | normal operation, once a year | the CSV is produced with the totals of the inventory | the CSV totals match the inventory on the day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
