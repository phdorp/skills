# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | Data loss is irreversible; the storage format and write rule are expensive to change. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Defines the CLI surface and what is stored. |
| R-3 | Runs with only the Python standard library. | 3 | active | Third-party dependency decision. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Module-boundary rule; a cost of change rather than a user-visible result. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

Open, no measure yet: functional correctness for R-2 (what would show R-2 is met?). Not a goal until the architect gives a measure.

### Gap review

Asked at setup, for each ISO/IEC 25010 characteristic no requirement supports: the architect answered that nothing is missing. No requirement was added from this review.

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

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The list of decisions made centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), proposed and waiting for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` or `remove` | normal operation | every add or remove that returned is present afterwards, and the store still reads | 0 acknowledged items lost in 100 runs |
| QS-2 | QG-2 | the program and its tests are run on a fresh Python 3 interpreter with no packages installed | normal operation | the program runs and the tests pass | 0 non-stdlib imports; tests pass |
| QS-3 | QG-3 | a new CLI command is added | normal operation | the change touches only `pantry/cli.py` and at most one new module | at most 2 changed non-test files per new command |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
