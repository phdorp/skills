# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | Core function; fixes the CLI surface and the record shape every block depends on. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Loss cannot be undone; storage and durability design rests on it. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Sets the dependency rule (standard library only) and forces cross-platform file handling. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Import/export format is a centrally decided item. |
| R-5 | It must be fast. | 5 | active | Shapes storage; no measure yet, so its goal stays open. |

Feature-level requirements (no R-row): `birdlog list` shows the latest sighting first. Parent R-1; filed as `.scratch/requirements/issues/01-list-latest-first.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability / adaptability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |
| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |

Open (no measure yet, not a row): Performance efficiency: time behaviour, from R-5.

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

Architecture decisions are recorded as ADRs in [`../adr/`](../adr/). The ADR that draws the line
between decisions made centrally and decisions left to the building blocks is
[0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md) (proposed).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed or power is lost during a write (`birdlog add`) | normal operation | the sighting is either fully stored or absent; the store still opens | 0 lost acknowledged sightings and 0 unreadable stores in 100 forced-kill trials |
| QS-2 | QG-2 | the test suite is run on a fresh Linux, macOS and Windows machine with only Python installed | normal operation | the suite passes on all three without extra packages | green on all three OSes in CI; 0 packages installed beyond the standard library |
| QS-3 | QG-3 | a file exported with the export command is imported into eBird | normal operation | eBird accepts every exported row | 100% of exported rows pass a check against the pinned eBird import template |
| QS-4 | QG-4 | a sighting is entered and then read back | normal operation | every field (species, place, time, count) comes back as entered | 0 field mismatches across every sighting in the round-trip test fixture set |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
