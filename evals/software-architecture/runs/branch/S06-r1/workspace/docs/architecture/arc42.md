# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 1 | active | Defines the sighting record every other block uses. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 2 | active | Decides the storage approach: durable, atomic writes. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Constrains dependencies, storage and platform support. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | An export format is a central decision. |
| R-5 | It must be fast. | 5 | active | Shapes the design; no measure yet (open question). |

R-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1: an issue, not a row.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |

### Stakeholders

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

Decisions are ADRs in `docs/adr/`, linked as `../adr/` from this file. The ADR that draws the line between central and block-level decisions is [Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL, or power is lost, during a sighting write | normal operation | each sighting is either fully stored or absent; the store still opens | 0 acknowledged sightings lost in 100 kill-during-write trials |
| QS-2 | QG-2 | the test suite is run on Linux, macOS and Windows with only Python installed | offline, no packages beyond Python | all tests pass on each system without installing anything else | 0 failing tests on each of the three systems |
| QS-3 | QG-3 | a sightings file is exported to eBird CSV | normal operation | every sighting is in the file with the columns of the eBird import template | every fixture sighting exported with the template's columns, checked by a fixture test: 0 mismatches |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
