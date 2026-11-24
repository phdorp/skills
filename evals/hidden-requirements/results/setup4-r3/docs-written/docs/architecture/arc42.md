# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out to themselves and back in, so the club always knows which coach holds which item. Items: balls, bibs, cones and first-aid bags. | 1 | active | Where R-1 and R-3 conflict, R-3 wins (architect's tie-breaker). |
| R-2 | Check-out or check-in takes at most 3 taps and under 15 seconds, by scanning a QR code on the kit bag. | 2 | active | |
| R-3 | Check-out and check-in work offline and sync when the phone is back online. | 3 | active | |
| R-4 | First-aid items carry an expiry date, and the club is warned 30 days before. | 4 | active | |
| R-5 | The club gets an e-mail every Monday morning listing overdue kit. | 5 | active | |
| R-6 | The treasurer gets a yearly inventory export as CSV for the insurance audit. | 6 | active | |
| R-7 | A successor who knows only Python can take the tool over. | 7 | active | |
| R-8 | After a NAS disk failure, the data from the previous night can be restored. | 8 | active | |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Interaction capability: learnability | R-2 | QS-2 |
| QG-3 | Reliability: availability | R-3 | QS-3 |
| QG-4 | Compatibility: interoperability | R-6 | QS-4 |
| QG-5 | Maintainability: modifiability | R-7 | QS-5 |
| QG-6 | Reliability: recoverability | R-8 | QS-6 |

Ruled out: performance efficiency (time behaviour, resource utilisation, capacity). Reason from the architect: about 300 items and 40 coaches; performance is not a concern.

### Stakeholders

- Coaches: about 40 volunteers, the users, on their own phones at the pitch, often without mobile signal; many not tech-savvy.
- Kit manager: the admin; receives the Monday report.
- Treasurer: receives the yearly CSV export for the insurance audit; copied on the Monday report.
- Maintainer: one volunteer who knows only Python; the successor takes over from them.

## 2. Constraints

- Runs on the club's existing Synology NAS, in Docker.
- Budget: 0 EUR per month.
- No third-party cloud service, except the club's existing e-mail account for outgoing mail.
- Coaches use a web page on their phone, added to the home screen; no app install from a store.
- Coach personal data (names and phone numbers) is personal data under GDPR and stays on club hardware. Phone numbers are visible only to the kit manager and the treasurer.
- The history of lost items is kept for 2 years, for insurance; it is not deleted after a season.
- Must be live by 1 March, the start of the season.
- One maintainer, who knows only Python; third-party dependencies must fit that.

## 3. Context and scope

Out of scope:

- Payments, deposits and fines.
- A member or player database.
- Purchasing and stock ordering.

Figures: about 300 items; about 40 coaches; several dozen check-outs a week.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

- **Offline conflict:** two coaches check out the same item while offline. The first record to sync wins; the other is flagged for the kit manager to resolve.
- **Monday report:** every Monday, an overdue item is one not checked in after 7 days. The e-mail to the kit manager, with the treasurer in copy, lists overdue items and a section for first-aid items expiring within 30 days.

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The list of architecture decisions made centrally is in [ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), status `proposed`, until the architect approves it.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a coach checks an item out or in | normal operation | the list shows the holder at once | after a week of use, 0 items listed under a coach who does not hold them |
| QS-2 | QG-2 | a volunteer, including one who is not tech-savvy, checks kit out or in by scanning the bag's QR code | at the pitch | the check-out or check-in completes | at most 3 taps and under 15 seconds |
| QS-3 | QG-3 | a coach checks kit out with no mobile signal, and the phone reconnects later | offline, then back online | the check-out syncs to the shared list | a check-out made offline reaches the shared list within 5 minutes of reconnecting; 0 of 100 offline check-outs lost in trials |
| QS-4 | QG-4 | the treasurer requests the yearly inventory export | normal operation | the CSV lists every item and history row | 100% of items and history rows present, checked against the item list |
| QS-5 | QG-5 | a Python-only volunteer takes over from the maintainer | handover | the successor reads the setup notes and deploys on the NAS | within one day |
| QS-6 | QG-6 | the NAS disk fails | normal operation with the nightly copy in place | the previous night's data is restored | after a NAS disk failure, the previous night's data can be restored |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
