# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | Core purpose; fixes the sighting record that storage and export depend on. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Core promise; drives the storage and write strategy. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Limits runtime dependencies to the standard library. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Export format is on the central list. |
| R-5 | It must be fast. | 5 | active | Sets a performance goal; no measure yet, see open questions. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-1, R-4 | QS-3 |

Open question (no goal row until a measure is given): performance efficiency, time behaviour, from R-5. What would show R-5 is met: the time limit for `birdlog add` and `birdlog list`, and the number of stored sightings it must hold.

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

The architecture decisions are ADRs in [`../adr/`](../adr/). The decisions the architect makes centrally are listed in [Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed or power is lost during `birdlog add` | normal operation | the sighting is either fully stored or absent, and the store still opens | 0 acknowledged sightings lost and 0 unreadable stores in 1000 kill trials |
| QS-2 | QG-2 | a fresh machine with only Python installed runs add, list and export offline | normal operation on Linux, macOS and Windows | the commands run without installing anything | 3 of 3 OSes pass the acceptance script; 0 non-standard-library imports |
| QS-3 | QG-3 | a logged sighting is exported | normal operation | each exported row carries the logged values in the eBird layout | 100% of rows pass a check against the eBird column spec; 0 fields lost in a round trip |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
