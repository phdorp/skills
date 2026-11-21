# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log and review sightings (species, place, time, count) from the command line. | 2 | active | Core function; fixes the input interface and the record shape. |
| R-2 | No sighting is lost, even if the laptop dies mid-write. | 1 | active | Core promise; decides how writes are made durable. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Sets the dependency rule: standard library only, no third-party packages. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Import/export data format; a central decision. |
| R-5 | Logging a sighting and listing sightings each complete within a measured limit (limit to be set). | 5 | active | Goal with no measure yet; see the open questions for QG-4 and QG-5. |

R-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1 and has no row here; it is filed as an issue.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Functional correctness | R-1 | QS-3 |

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

Decisions are recorded as ADRs in `docs/adr/` ([`../adr/`](../adr/)). The ADR that draws the line between central and local decisions is [Record architecture decisions](../adr/0001-record-architecture-decisions.md); it is written once the architect confirms the setup.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL, or power is lost) during `birdlog add` | normal operation | the sighting is either fully stored or absent; sightings stored before are intact and the store opens | 0 confirmed sightings lost and 0 unreadable stores in 100 kill-during-write trials |
| QS-2 | QG-2 | a person installs birdlog on a machine with only Python 3 | fresh Linux, macOS or Windows machine, offline | birdlog runs without any package beyond the standard library | 0 third-party packages; the test suite passes on all three OSes |
| QS-3 | QG-3 | a sighting is logged, then listed | normal operation | every field is stored as entered; `list` shows the latest sighting first | 0 mismatched fields and 0 wrong orderings in the round-trip test suite |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
