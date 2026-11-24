# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 2 | active | The core function; the other requirements build on it |
| R-2 | A sighting that `add` reported as saved survives a crash or power loss at any moment during the write. | 1 | active | Losing data is the one failure the product cannot accept; conflicts with R-5 |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Limits every technology choice; the standard-library-only constraint follows from it |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Needed for eBird submission; the format is decided centrally |
| R-5 | It must be fast. | 5 | active | Quality goal with no measure yet; open question |

`birdlog list` shows the latest sighting first. This is feature-level under R-1 and is tracked in `.scratch/requirements/issues/01-list-latest-first.md`.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Flexibility: adaptability | R-3 | QS-1 |

### Stakeholders

- **Birder (user):** logs, lists and exports their sightings; one person on their own laptop.
- **Maintainer:** builds and maintains birdlog; one person, comfortable with Python.

## 2. Constraints

- Runs offline on Linux, macOS and Windows (R-3).
- Python 3.10 or newer is the only runtime; standard library only, no third-party packages (R-3).
- Export targets the current eBird import template (R-4).
- No hosting and no budget.
- Sighting data stays on the user's machine.

## 3. Context and scope

birdlog is a command-line tool with a local data file. Outside the system: the eBird web upload, which the user performs by hand with the exported file.

Out of scope:
- a server, syncing between machines, a graphical interface, an eBird API integration;
- editing and deleting sightings: these can wait, they are not part of the first version.

Figures:
- about 1,000 sightings a year, up to about 10,000 within five years;
- `list` must stay fast at 100,000 sightings (see the open question for R-5).

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in [`../adr/`](../adr/). The list of decisions made centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), which is `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the test suite is run on a clean machine | a clean Python 3.10+ install on Linux, macOS or Windows, offline | birdlog installs and the suite passes | the suite passes on all three operating systems |

Open questions (goals without a measure, not yet in the tables):
- **Reliability: recoverability** (R-2): what would show R-2 is met? For example, "0 lost sightings in 100 forced kills during `add`".
- **Performance efficiency: time behaviour** (R-5): what response time is fast enough for `add` and `list`, and at what log size?
- **Compatibility: interoperability** (R-4): which validation proves the export is correct, and for which eBird CSV version?

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
