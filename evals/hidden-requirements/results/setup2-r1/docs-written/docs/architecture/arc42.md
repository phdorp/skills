# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches can check items out and return them, recording who holds each one. | 1 | active | The data every other requirement depends on. |
| R-4 | Check-out and check-in work offline and sync when the phone is back online. | 2 | active | There is often no signal at the pitch, where check-out happens. |
| R-3 | A new coach can check an item out without instructions. | 3 | active | Many volunteers are not tech-savvy; decides whether R-1 gets used. |
| R-2 | At any time the club can see which coach holds each item, or that it is in storage. | 4 | active | The purpose; useful once R-1 records the holders. |
| R-5 | An overdue report is e-mailed every Monday morning. | 5 | active | Chases items still out 7 days after check-out; carries the expiry warnings. |
| R-6 | A yearly inventory export as CSV. | 6 | active | The treasurer needs it for the insurance audit. |
| R-7 | Item history, including lost items, is kept for 2 years, with the minimum fields: item, date and coach name. | 7 | active | The insurer needs 2 years of history; GDPR limits the fields kept. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1, R-2 | QS-1 |
| QG-2 | Interaction capability: operability | R-3 | QS-2 |
| QG-3 | Reliability: recoverability | R-4 | QS-3 |
| QG-4 | Security: confidentiality | R-7; constraints on personal data and login (section 2) | QS-4 |
| QG-5 | Maintainability: analysability | constraint: a successor takes over (section 2) | QS-5 |

### Stakeholders

- **Coaches** (about 40): check items out and back in from their phones.
- **Kit manager** (also the architect): enters expiry dates, is the only one who sees phone numbers, and receives the Monday report.
- **Treasurer**: receives the yearly CSV for the insurance audit.
- **Insurer**: needs the 2-year item history.
- **Maintainer**: one volunteer who knows only Python; a successor must be able to take over.

## 2. Constraints

- **Hosting:** the club's Synology NAS, running Docker. Data stays on club hardware; no third-party cloud ([ADR-0002](../adr/0002-host-on-nas-with-docker-in-python.md)).
- **Budget:** 0 EUR per month.
- **Language:** Python ([ADR-0002](../adr/0002-host-on-nas-with-docker-in-python.md)).
- **Maintenance:** one volunteer who knows only Python maintains it; a successor must be able to take over.
- **Data protection:** GDPR applies to coach names and phone numbers.
- **Deadline:** live by 1 March, the start of the season.
- **Login:** each coach logs in with a club-issued code, and the phone stays logged in.
- **Backup:** nightly to a second club-owned disk, which stays on club hardware; restore tested once per season.
- **E-mail:** the club's existing mailbox, via SMTP.
- **Phones:** browsers can use the camera to scan QR codes; typing the code in is the fallback.

## 3. Context and scope

The tool is used by coaches in a phone browser. It sends e-mail through the club's mailbox to the kit manager (the Monday report) and to the treasurer (the yearly CSV). It runs on the club's NAS.

Out of scope:

- money handling: deposits, fines and payments;
- personal data beyond coach names and phone numbers;
- training schedules;
- low-stock alerts;
- performance tuning: not a concern at about 40 coaches and 300 items.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in `../adr/`. The list of decisions made centrally is in [Record architecture decisions](../adr/0001-record-architecture-decisions.md). Hosting and language are in [ADR-0002](../adr/0002-host-on-nas-with-docker-in-python.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the kit manager checks every item's recorded holder against the physical holder | normal operation, at the end of training | the recorded holder matches the physical one | at least 95% of items match |
| QS-2 | QG-2 | a coach with a logged-in phone scans the QR code on a kit bag and checks the item out | at the pitch, with no mobile signal | the check-out is recorded | at most 3 taps and under 15 seconds |
| QS-3 | QG-3 | the phone is closed or loses power during the sync of an offline check-out | at the pitch, offline, then back online | the check-out appears in the records after sync | 0 lost offline check-outs in 100 trials |
| QS-4 | QG-4 | a user without the kit manager role opens a coach's record | normal operation, logged in with a club-issued code | no phone number is shown | 0 phone numbers shown, tested with 3 accounts |
| QS-5 | QG-5 | a volunteer who knows only Python changes the Monday report, without help from the maintainer | the code base, as it stands | the change is made and tested | under 4 hours |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
