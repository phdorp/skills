# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Volunteers check kit out to themselves and back in. | 2 | active | Core use. Ranks below R-2 (ease of use wins a conflict). |
| R-2 | Volunteers can use the tool without training. | 1 | active | Ease of use comes first; it wins a conflict with R-1 and R-4. |
| R-3 | Check-outs work without signal and sync when the phone is back online. | 5 | active | Offline use at the pitch; security (R-4) wins a conflict. |
| R-4 | Coach names and phone numbers are visible only to signed-in club volunteers, and phone numbers are never stored on a phone. | 3 | active | Security priority. Wins over R-3. |
| R-5 | No check-out or check-in is lost, and the tool is available on match days. | 4 | active | Reliability priority. |
| R-6 | A volunteer who knows only Python can maintain and change it. | 6 | active | A successor must be able to take over. |
| R-7 | Damage reports. | — | deferred | The architect said they can wait. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Interaction capability: operability | R-2 | QS-2 |
| QG-3 | Reliability: recoverability and availability | R-5 | QS-3 |
| QG-4 | Security: confidentiality | R-4 | QS-4 |
| QG-5 | Maintainability: modifiability | R-6 | QS-5 |

### Stakeholders

- **Kit manager** (the architect): receives the Monday overdue report and the 30-day expiry warnings; enters the expiry dates.
- **Coaches** (about 40): check kit out and back in.
- **Other volunteers**: check kit out and back in.
- **Treasurer**: receives the yearly CSV inventory export for the insurance audit.
- **Club's insurer**: audits the two-year history of lost items.
- **Maintainer**: one club volunteer who knows only Python.
- **Successor**: not yet named.

## 2. Constraints

- Runs on the club's Synology NAS, with Docker.
- Data stays on club hardware. No third-party cloud.
- Budget: 0 EUR per month.
- GDPR applies to coach data.
- Records are kept for 2 years, for insurance. Phone numbers are deleted when a coach leaves; coach names stay only on the history records for those 2 years.
- Coach names go out only through the club's own mail account, never through a third-party provider.
- The interface is in German.
- Python is required.
- Live by 1 March 2027, the start of the season.
- Scale: about 40 coaches and 300 items.

## 3. Context and scope

Out of scope: money handling (deposits, fines, payments); player or parent data; location tracking.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The architecture decisions are ADRs in [`../adr/`](../adr/). The list of decisions made centrally is in [Record architecture decisions](../adr/0001-record-architecture-decisions.md), which the architect accepted on 2026-11-23.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a volunteer checks an item out or back in, while other volunteers do the same and some are offline | normal operation, several volunteers | once synced, the record shows the true current holder of every item | 0 records with the wrong holder in a season |
| QS-2 | QG-2 | a volunteer who has never used the tool scans the QR code on a bag and checks it out | a phone, no training, no help | the check-out is recorded | at most 3 taps and under 15 seconds |
| QS-3 | QG-3 | the NAS fails, or a restore is needed, during a match | normal match-day operation | no check-out or check-in is lost, and the tool is back | 0 lost records in 100 restore trials; 99% availability during match hours |
| QS-4 | QG-4 | a request arrives without a valid sign-in | normal operation | no coach name or phone number is returned | 0 coach phone numbers returned in every trial |
| QS-5 | QG-5 | a Python-only volunteer is asked to make a small change | the written documents only, no help from the maintainer | the change is made and tested | under one day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
