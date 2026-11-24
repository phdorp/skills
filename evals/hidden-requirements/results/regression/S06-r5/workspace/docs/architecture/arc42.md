# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No sighting is ever lost, even if the laptop dies mid-write. | 1 | active | A lost sighting cannot be recovered. |
| R-2 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | This is the core function. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Limits every later choice. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Needed, but it can follow the core. |
| R-5 | It must be fast. | 5 | active | No measure yet; see the open questions in the report. |

Feature-level requirement (no R-row): `birdlog list` shows the latest sighting first. It cites R-2 in the issue `.scratch/requirements/issues/01-list-latest-first.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |

### Stakeholders

- **Birder**: logs sightings from the command line and exports them to eBird.
- **Maintainer**: the one person who builds and maintains birdlog; comfortable with Python and the command line.

## 2. Constraints

- Python standard library only; no packages beyond Python itself (R-3).
- No network use: birdlog works offline (R-3).
- Sighting data stays on the user's machine and is never uploaded; no encryption in v1.
- No budget; open source under a permissive licence.
- One maintainer.

## 3. Context and scope

Out of scope for v1: editing or deleting sightings, uploading to eBird, photos.

Scale: one user per installation; a few thousand sightings a year; under 50,000 sightings in ten years.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

- **Time:** a sighting's time is when the bird was seen, stored with its UTC offset. "Latest" means the latest seen time, with ties broken by the order in which they were logged.

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The ADR that sets which decisions are made centrally is [Record architecture decisions](../adr/0001-record-architecture-decisions.md), status `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `birdlog add` | normal operation | each sighting is either fully stored or absent; every sighting whose add reported success is still there; the store still opens | 0 acknowledged sightings lost and 0 unreadable stores in 1000 SIGKILL trials |
| QS-2 | QG-2 | a clean Python 3 install on Linux, macOS or Windows, with no network | offline | the full test suite runs without installing any package | the suite passes on all three OSes |
| QS-3 | QG-3 | the user runs `birdlog export` and uploads the file to eBird | normal use | eBird's import accepts the file without edits | 0 import errors on the reference export file |

## 11. Risks and technical debt

## 12. Glossary

See [GLOSSARY.md](../../GLOSSARY.md).
