# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | Core function; fixes the data model and the CLI surface. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Losing a sighting defeats the purpose of the tool; decides the storage design. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Platform constraint every release must meet; implies standard library only. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Needed, but the last step of the workflow; fixes an export data format. |
| R-5 | It must be fast. | 5 | active | Matters once the other requirements hold. Conflicts with R-2 (crash-safe writes cost time). |

Feature-level, no row: `birdlog list` shows the latest sighting first. It fits inside R-1 and is
tracked as `.scratch/requirements/issues/01-list-latest-first.md`, citing R-1.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional completeness | R-1 | QS-2 |
| QG-3 | Flexibility: adaptability | R-3 | QS-3 |
| QG-4 | Compatibility: interoperability | R-4 | QS-4 |

Open question (no measure yet, so no goal row): Performance efficiency: time behaviour, from
R-5. What response time for `birdlog add` and `birdlog list`, at how many stored sightings?

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

The architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The central list
is [ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md),
which is `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL, or power is cut, during `birdlog add` | normal operation | each acknowledged sighting is fully stored and readable; the store still opens | 0 lost acknowledged sightings and 0 unreadable stores in 100 trials |
| QS-2 | QG-2 | `birdlog add` is run with species, place, time and count | normal operation | `birdlog list` shows the same four values | all four fields round-trip in 100% of test cases |
| QS-3 | QG-3 | the test suite runs on Linux, macOS and Windows | a machine with only Python installed, offline | all tests pass; the code imports nothing outside the standard library | passes on 3 of 3 operating systems; 0 non-standard-library imports |
| QS-4 | QG-4 | `birdlog export` writes the stored sightings as eBird CSV | normal operation | the file matches the eBird CSV template and imports without manual edits | 0 rows rejected by the fixture check against the eBird template |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
