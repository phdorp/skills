# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | Everything else assumes a stored sighting survives; drives atomic writes and flushing to disk. |
| R-2 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | The core function; defines the sighting record and the CLI surface. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Constrains storage and dependency choices: standard library only. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | The export format is a central data-format decision. |
| R-5 | It must be fast. | 5 | active | Not testable yet; its goal waits for a measure. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-2 | QS-3 |

Open, no measure yet (not goals until a measure is given):

- Performance efficiency: time behaviour, from R-5. What would show R-5 is met (response times, sighting count, reference machine)?
- Compatibility: interoperability, from R-4. Which eBird CSV template version does the export have to pass?

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

The ADRs are in [`../adr/`](../adr/). How decisions are recorded:
[0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | `birdlog add` is killed with SIGKILL mid-write (stands in for a power loss) | normal operation | the sighting is either fully stored or absent; every previously acknowledged sighting is still readable | 0 lost acknowledged sightings and 0 unreadable stores in 100 kill trials |
| QS-2 | QG-2 | a fresh Python 3 install on each OS runs `add` then `list` | Linux, macOS and Windows, offline | both work with the standard library only | 3 of 3 OSes pass; 0 third-party packages |
| QS-3 | QG-3 | 1,000 random sightings are logged, then listed | normal operation | every field reads back unchanged; the list is newest first | 100% of fields round-trip; 100% of list orders correct |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
