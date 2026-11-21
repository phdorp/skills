# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | Defines the record every other part stores, exports and lists. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Durability decides the storage mechanism. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Limits the dependencies and the storage options. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | An export format crosses a boundary, so it is decided centrally. |
| R-5 | It must be fast. | 5 | active | Shapes the storage and write path; no measure yet, see open questions. |

R-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1: it is an issue, not a row. See `.scratch/requirements/issues/01-list-latest-first.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |

Open questions (no measure yet, so no goal row): time behaviour (from R-5), and functional correctness of the eBird export (from R-4). What number would show R-5 is met, and how is an eBird import validated?

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

The ADRs are in [`../adr/`](../adr/). The decision on which decisions the architect makes centrally is the ADR "Record architecture decisions", proposed as [`../adr/0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md) and written once the architect confirms the setup proposal.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) or power is lost during a `log` call | normal operation | the sighting is either fully stored or absent, and the store still opens | 0 lost acknowledged sightings and 0 unreadable stores in 100 trials |
| QS-2 | QG-2 | the test suite runs on Linux, macOS and Windows with a stock Python | normal operation | the suite passes on all three platforms without platform-specific failures | 0 platform-specific failures |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
