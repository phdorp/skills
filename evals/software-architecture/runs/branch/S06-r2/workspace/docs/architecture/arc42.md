# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Decides the storage design and is expensive to change later. |
| R-2 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 2 | active | Constrains dependencies and storage, and must hold on all three OSes. |
| R-3 | Birders log a sighting (species, place, time, count) from the command line. | 3 | active | Defines the product's main interface. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | The export format is an external data format, decided centrally. |
| R-5 | It must be fast. | 5 | active | Real requirement; "fast" has no measure yet, so the goal stays open. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Flexibility: adaptability | R-2 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |

Open question (no measure yet, so no goal row): Functional correctness (from R-3), and
Performance efficiency: time behaviour (from R-5).

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

The architecture decisions are recorded as ADRs in [`../adr/`](../adr/). The ADR
[Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `proposed` and
waits for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed or the power fails during `birdlog add` | normal operation | the sighting is either fully stored or absent; the store still opens and lists | 0 lost saved sightings and 0 unreadable stores in 1,000 forced kills per OS |
| QS-2 | QG-2 | the test suite is run on a clean install of Linux, macOS and Windows | a clean install with Python and no third-party packages | the suite passes on each OS without extra packages | 0 third-party packages installed; suite passes on all three OSes |
| QS-3 | QG-3 | an exported eBird CSV file is imported into eBird | normal operation | all rows are accepted | 0 rejected rows |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
