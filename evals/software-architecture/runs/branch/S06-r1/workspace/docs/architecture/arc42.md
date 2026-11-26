# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Our one property not to trade away; the other requirements build on it. |
| R-2 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | The core use; nothing works without it. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Sets the dependency rule (standard library only) and rules out some storage options. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Uses the stored data and is needed for use with eBird. |
| R-5 | It must be fast. | 5 | active | Judged against the others once it has a measure (open). |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-1 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |
| QG-4 | Functional suitability: functional completeness | R-2 | QS-4 |

### Stakeholders

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

The ADRs live in [`docs/adr/`](../adr/). The "Record architecture decisions" ADR is
[`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md); it is
proposed and gets written once the architect confirms the setup proposal.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL, or power is cut, during `birdlog add` | normal operation | the sighting is either fully stored or absent, and the store still opens | 0 unreadable stores and 0 acknowledged sightings lost in 100 kill trials |
| QS-2 | QG-2 | a user installs and runs every command on a fresh machine | Linux, macOS and Windows with Python 3 only, no network | every command works | the test suite passes on all three systems with no third-party packages |
| QS-3 | QG-3 | a user exports sightings to eBird CSV | normal operation | the file matches the eBird column specification | every export of a 1,000-sighting fixture matches, with 0 mismatches |
| QS-4 | QG-4 | a user logs a sighting with all four fields and lists it | normal operation | the four fields read back unchanged | 100% of test records round-trip |

Time behaviour (R-5) has no measure yet and is an open question, so it has no goal row.

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
