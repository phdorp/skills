# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Core use; fixes the CLI interface and the expiry-date data every block uses. |
| R-2 | An item the store has confirmed as added stays listed after a crash at any point during a write. | 1 | active | A lost item cannot be recovered by the user. |
| R-3 | Runs with only the Python standard library. | 3 | active | Limits every dependency choice; the code already meets it. |
| R-4 | Adding a command changes only `cli.py` and at most one new module, tests excluded. | 4 | active | Matters for the next feature, not now. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

### Stakeholders

### Gap review

Asked at setup: security (confidentiality), performance efficiency (capacity), and interaction capability (user error protection). The architect answered that nothing is missing; no requirement was added.

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

Architecture decisions are recorded as ADRs in [`../adr/`](../adr/). [ADR 0001, Record architecture decisions](../adr/0001-record-architecture-decisions.md) lists the decisions made centrally; it is proposed until the architect accepts it.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | every item an earlier `add` confirmed is still listed, and the file reads without error | 0 lost confirmed items in 100 trials |
| QS-2 | QG-2 | `list --soon N` is run | normal operation | it lists exactly the items expiring on or before today+N, sorted by expiry | 0 wrong rows at the boundaries N−1, N and N+1 days |
| QS-3 | QG-3 | a developer adds a new command | normal operation | the change touches `cli.py` and at most one new module | at most 2 files changed per new command, tests excluded |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
