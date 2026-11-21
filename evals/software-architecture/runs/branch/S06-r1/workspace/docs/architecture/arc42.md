# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | A sighting the tool has acknowledged is never lost or left half-written after a crash or power loss during a write. | 1 | active | It decides the storage engine and write path, which are expensive to change. |
| R-2 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | It defines the data model every other part depends on. |
| R-3 | Runs offline on Linux, macOS and Windows with only Python installed (no third-party packages, no network). | 3 | active | It limits the storage and dependency choices. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | It is an import/export data format, so it needs an ADR. |
| R-5 | Logging and listing are fast. | 5 | active | A quality requirement with no measure yet; its goal stays open. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-2 | QS-2 |
| QG-3 | Interoperability | R-4 | QS-3 |
| QG-4 | Flexibility: adaptability | R-3 | QS-4 |

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in `docs/adr/`. See [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (or power is cut) during `birdlog add` | normal operation | the sighting is either fully stored or absent; earlier acknowledged sightings remain; the store still opens | 0 acknowledged sightings lost and 0 unreadable stores in 100 kill-during-write trials |
| QS-2 | QG-2 | a sighting is logged and then listed | normal operation | the listed sighting matches the logged fields | 0 field mismatches in 1,000 logged sightings |
| QS-3 | QG-3 | an exported file is imported into eBird | normal operation | eBird accepts the file | 0 import errors across the sample exports (sample set to be agreed) |
| QS-4 | QG-4 | the test suite runs on each of Linux, macOS and Windows | Python installed, nothing else | all tests pass on each OS | the suite passes on all three OSes in CI |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
