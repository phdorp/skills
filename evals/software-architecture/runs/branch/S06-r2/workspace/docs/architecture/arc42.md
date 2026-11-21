# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | Defines the core interface and the data every other requirement touches. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Shapes the storage and write path; needs an ADR. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Limits dependencies to the standard library and rules out a server. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Import and export formats are a central decision. |
| R-5 | It must be fast. | 5 | active | Shapes storage; not testable as written, so its goal stays open. |

R-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1 and has no row here; see the issue in `.scratch/requirements/issues/`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-1 | QS-3 |
| QG-4 | Compatibility: interoperability | R-4 | QS-4 |

Open question (no measure yet, so no goal row): Performance efficiency: time behaviour, from R-5.
What would show R-5 is met?

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in `docs/adr/`. The ADR that defines which decisions are made
centrally is [Record architecture decisions](../adr/0001-record-architecture-decisions.md)
(written once the architect confirms the proposal).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed during `birdlog add` | normal operation | the sighting is either fully stored or absent, and the store opens on the next run | 0 unreadable stores and 0 acknowledged sightings lost in 100 kill trials |
| QS-2 | QG-2 | the test suite runs on a clean Python install on each OS, with no packages beyond the standard library | normal operation | all tests pass | 3 of 3 OSes pass; 0 third-party imports |
| QS-3 | QG-3 | a user logs a sighting, then lists and exports it | normal operation | the species, place, time and count match what was entered | 0 mismatches in a 1,000-entry round-trip test |
| QS-4 | QG-4 | a user exports the log to eBird CSV | normal operation | the file has the eBird columns and values | 0 format errors on the fixture set |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
