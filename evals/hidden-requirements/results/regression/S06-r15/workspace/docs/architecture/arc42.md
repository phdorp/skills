# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 3 | active | Core function; shapes the input model and storage. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Data loss is irreversible and hardest to retrofit. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 4 | active | Platform reach and the no-dependency rule shape the build. |
| R-4 | Sightings export to the eBird CSV format. | 2 | active | Fixes an external format, so it is a central decision. |
| R-5 | It must be fast. | 5 | active | Can be tuned later, once a measure exists. |

The requirement "`birdlog list` shows the latest sighting first" is feature-level under R-1; it is
filed as an issue and has no row here (`.scratch/requirements/issues/01-list-latest-first.md`).

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability and adaptability | R-3 | QS-2 |

Open, without a measure yet (not goals until the architect gives one):

- Compatibility: interoperability (R-4): the measure needs the target eBird CSV template and a sample file.
- Performance efficiency: time behaviour (R-5): the measure is open; for example, "`add` returns in under 100 ms with 10,000 stored sightings" is a candidate figure.

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

ADRs live in [`../adr/`](../adr/). The decision on which decisions the architect makes centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (proposed).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | The process is killed during `add`. | normal operation | The sighting is either fully stored or absent, and the store still opens. | 0 acknowledged sightings lost and 0 unreadable stores in 100 kill-during-write trials |
| QS-2 | QG-2 | Install and run the full test suite on a clean machine with only Python, offline. | Linux, macOS and Windows | The suite passes with nothing installed beyond Python. | The suite passes on 3 of 3 operating systems. |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
