# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | It decides the storage and write strategy. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 2 | active | It limits dependencies to the standard library. |
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 3 | active | It defines the record that storage and export depend on. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | It is an external format that fixes the record fields; import and export formats are a central decision. |
| R-5 | It must be fast. | 5 | active | It shapes the storage choice; no measure yet, so no goal yet. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |

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

Architecture decisions are recorded in [`../adr/`](../adr/). Decisions the architect makes centrally are listed in [ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the laptop loses power, or the process is killed with SIGKILL, during `birdlog add` | normal operation | the sighting is either fully stored or absent; the store still opens with earlier sightings intact | 0 acknowledged sightings lost and 0 unreadable stores in 100 trials |
| QS-2 | QG-2 | a user installs birdlog on a fresh system with only Python and runs `add`, `list` and export | normal operation on Linux, macOS and Windows | all three commands work with no package beyond the standard library | 3 of 3 operating systems pass |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
