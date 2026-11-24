# Kit Tracker: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Coaches check kit out and back in, so the club always knows where each item is. | 1 | active | Core of the product; shapes the data and the access model. |
| R-2 | Each checkout records which coach took or returned the item. | 3 | active | Answers "nobody knows which coach has what": accountability. |
| R-3 | The tool is easy to use, including for volunteers who are not tech-savvy. | 2 | active | Cross-cutting: shapes the screens and sign-in. Measured by QG-2. |
| R-4 | Checkout and check-in work offline and sync when the phone is back online. | 4 | active | Pitches often have no signal; shapes storage and sync. |
| R-5 | Coach personal data (names, phone numbers) is visible only to signed-in club coaches, and phones keep as little of it as possible. | 5 | active | Personal data under GDPR. Balanced against R-4 by the architect. |
| R-6 | The kit manager receives an e-mail every Monday morning listing overdue kit. The e-mail carries no coach phone numbers, and no data goes through a third-party cloud. | 6 | active | Outbound report; the data-location rule wins over the e-mail channel. |
| R-7 | Lost-item history is kept for 2 years, with the coach pseudonymised. | 7 | active | Retention rule that shapes the data model. |
| R-8 | A volunteer who knows Python can maintain the tool, and a successor can take it over. | 8 | active | Shapes code and documentation; backs QG-5. |

Feature-level requirements, filed as issues (no R-list row):
- Expiry warning 30 days before first-aid item expiry: under R-6, `.scratch/requirements/issues/01-expiry-warning.md`.
- Yearly inventory export as CSV for the treasurer's insurance audit: under R-1, `.scratch/requirements/issues/02-yearly-csv-export.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1, R-2 | QS-1 |
| QG-2 | Interaction capability: operability | R-3 | QS-2 |
| QG-3 | Reliability: availability | R-4 | QS-3 |
| QG-4 | Security: confidentiality | R-5, R-6, R-7 | QS-4 |
| QG-5 | Maintainability: modifiability | R-8 | QS-5 |

Ruled out by the architect: performance efficiency ("performance is not a concern"), so no goal.

### Stakeholders

- **Kit manager:** receives the Monday report; the architect of this document.
- **Coaches:** about 40, on their own phones; many are not tech-savvy.
- **Treasurer:** needs the yearly inventory export for the insurance audit.
- **Club committee:** no requirement of its own; kept as a stakeholder.
- **Maintainer:** one volunteer, who knows Python only.
- **Successor:** whoever takes over maintenance later; not yet named.

## 2. Constraints

- Runs on the club's existing Synology NAS with Docker, at 0 EUR per month.
- Personal data stays on the club's own hardware; no third-party cloud.
- Must be live for the start of the season on 1 March.
- Written in Python: the only maintainer knows only Python, and a successor must be able to take over.

## 3. Context and scope

About 40 coaches and about 300 items.

Out of scope:
- Money handling: no deposits, fines or payments.
- Player data, match results, and the club's membership system.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The "Record architecture decisions" ADR, [ADR 0001](../adr/0001-record-architecture-decisions.md), is `proposed` and awaits the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the club spot-checks items against their records | normal operation | the records match where the items are | at least 95% of spot-checked items match their record |
| QS-2 | QG-2 | a coach scans the QR code on a kit bag and checks it out | normal operation, on the coach's own phone | the checkout is recorded with the coach's identity | at most 3 taps and under 15 seconds from the scan |
| QS-3 | QG-3 | a coach checks an item out or in at the pitch with no signal | no mobile signal | the action is stored on the phone and synced when the phone is back online | every offline checkout appears after sync in test runs |
| QS-4 | QG-4 | someone without a sign-in asks for coach names or phone numbers | normal operation | the data is refused and nothing is shown | 0 coach records readable without sign-in |
| QS-5 | QG-5 | a maintainer who did not write a module makes a change in it | normal operation | the change is made with its tests passing | a tested change in one day |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
