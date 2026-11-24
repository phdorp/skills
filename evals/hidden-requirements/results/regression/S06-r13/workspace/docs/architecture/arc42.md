# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 1 | active | The product's purpose; it shapes the record model and the CLI. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 2 | active | The strongest correctness promise; it shapes the write path. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | A platform promise that limits dependencies and storage options. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | A self-contained export format. |
| R-5 | It must be fast. | 5 | active | Important, but it has no measure yet; see the open question for QG-3. |

`birdlog list` shows the latest sighting first. This is a feature-level requirement under R-1 and has no row here; it is tracked in `.scratch/requirements/issues/01-list-latest-first.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-4 | Compatibility: interoperability | R-4 | QS-3 |

QG-3 (Performance efficiency: time behaviour, from R-5) is reserved and open: no measure is given yet.

### Stakeholders

- **Birder**: the only user; logs sightings on their own laptop.
- **Maintainer**: builds and maintains birdlog; comfortable with Python.
- **eBird**: receives the exported CSV file, uploaded by the birder by hand.

## 2. Constraints

- Python 3.9 or newer; standard library only.
- Free and open-source licence.
- No hosting: everything runs on the user's machine.
- Sighting data is kept in one local file that the user owns and deletes; nothing is sent anywhere.
- The eBird export follows eBird's date and time format, to be verified against eBird's current CSV specification.
- No fixed delivery date.

## 3. Context and scope

- **System boundary:** the birdlog command-line tool and its local data file on the user's machine.
- **Outside the system:** the birder (the user) and eBird (receives the CSV file by manual upload; no API).
- **Out of scope:** editing and deleting sightings (these wait for a later version), sync between devices, a GUI, upload to eBird's API, and multi-user use.
- **Figures:** about 10,000 sightings now; about 100,000 in five years.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs live in `docs/adr/`. The "Record architecture decisions" ADR is [`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md), status `proposed`, awaiting the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL, or power is lost, during `birdlog add` | normal operation | the sighting is either fully stored or absent, and the store still opens | 0 unreadable stores and 0 partial records in 1000 kill trials |
| QS-2 | QG-2 | a clean machine with only Python installed, offline, on each of Linux, macOS and Windows, runs install and all commands | normal operation | all commands run with no extra package and no network | 0 extra installs needed across the three-OS test matrix |
| QS-3 | QG-4 | the user exports sightings and uploads the file to eBird | normal operation | every exported row follows the eBird CSV specification | 0 format violations in the export validation in the test suite |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
