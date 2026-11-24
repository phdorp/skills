# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | System-level: it decides the storage design, the costliest part to change later. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | System-level: it fixes the command-line interface and the expiry-date model. |
| R-3 | A new command touches only cli.py and at most one new module. | 3 | active | System-level: it sets the dependency rule between the building blocks. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-1 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-2 | QS-2 |
| QG-3 | Maintainability: modifiability | R-3 | QS-3 |

Not a goal: Security (confidentiality). The architect's answer to the "did you leave out" question: nothing is missing.

Open, without a measure, so no goal yet: Portability (adaptability), from the standard-library constraint in section 2. Which Python versions and operating systems must it run on with no install step?

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library, with no third-party dependencies. Stated by the architect as a requirement; it bounds the solution, so it is a constraint and has no R-row.

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in `../adr/`. The ADR [0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md) lists which decisions are made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the machine crashes or the process is killed while `add` or `remove` writes | normal operation | every item whose command returned success is still listed, and the pantry file still reads | 0 lost items and 0 unreadable files in 100 kill-during-write trials |
| QS-2 | QG-2 | the user runs `list --soon N` | normal operation | exactly the items expiring by today plus N days are listed, earliest first | 0 mismatches against a reference list over 1,000 random item sets |
| QS-3 | QG-3 | a developer adds one read-only command | the current code | only cli.py and at most one new module change | at most 2 files changed in a reference change |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
