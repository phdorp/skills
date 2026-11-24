# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 1 | active | The purpose of the product. |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 2 | active | Storage must survive a crash mid-write. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Portability and no-network operation. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Sightings must reach eBird. |
| R-5 | It must be fast. | 5 | active | Speed of `add` and `list`; no measure yet. |

Feature-level, no R-ID: `birdlog list` shows the latest sighting first. Issue
`.scratch/requirements/issues/01-list-latest-first.md`, under R-1.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: adaptability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |
| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |

Not a goal: Security (confidentiality, integrity, authenticity). The product is single-user with
local data, and the operating system protects the file (architect's answer, Q9).

Open question (not a goal yet): R-5 (time behaviour). What measure shows it is met? Example:
"`add` and `list` each answer in under 0.5 s on a store with 20,000 sightings."

### Stakeholders

- Birder: logs and exports their own sightings. One birder per install.
- Maintainer: one person, comfortable in Python, who builds and maintains the tool.

## 2. Constraints

- Python 3.11 or newer.
- Standard library only: no third-party packages, no network at runtime (R-3).
- Export matches the current eBird import layout (Q7).
- No deadline. Free tools only.

## 3. Context and scope

Scope: `birdlog add` (R-1), `birdlog list` (R-1, R-6 feature), `birdlog export` to eBird CSV (R-4).

Out of scope:
- Editing and deleting sightings (v1; later).
- Sync across devices and sharing between users.
- Uploading to eBird directly; the export file is uploaded by hand.
- Security features, including encryption (see Quality goals).

Figures:
- Volume per user: about 20,000 sightings after five years; upper bound 100,000.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

- Time: stored as local time with its UTC offset (Q8).

## 9. Architecture decisions

The architecture decisions are recorded as ADRs in [../adr/](../adr/). The ADR "Record architecture decisions" ([`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md)) lists which decisions are made centrally. It is `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process or the laptop dies during `add` (SIGKILL in tests; a power cut in real use) | normal operation | every sighting reported as saved is present and readable afterwards; the store still opens | 0 lost sightings and 0 unreadable stores in 100 kill trials |
| QS-2 | QG-2 | a fresh Python install on each of Linux, macOS and Windows, without network, runs `add` and `list` | offline, Python only | both commands run and store a sighting | 3 of 3 OSes pass the smoke test |
| QS-3 | QG-3 | a 100-sighting export is imported into eBird | normal operation | eBird accepts every row | 0 rows rejected by eBird's import template check |
| QS-4 | QG-4 | a sighting is entered with `add` | normal operation | every field is stored as entered | 0 mismatches in 1,000 entries |

## 11. Risks and technical debt

- R-2 vs R-5: flushing each write to disk costs time. Rank order gives R-2 precedence; R-5 is
  at risk until its measure is set.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
