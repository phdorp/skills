# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | |
| R-3 | Runs with only the Python standard library. | 3 | active | |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |

Open, without a measure yet (not goals until the architect gives one):

- Flexibility: adaptability, from R-3. What would show it is met? On which Python versions and operating systems must it run?
- Functional suitability: functional correctness, from R-1. What would show it is met? Should `list --soon` include items already past their expiry date?

Ruled out by the architect, no reason given: Security: confidentiality; Performance efficiency: time behaviour.

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `../adr/`. The list of decisions made centrally is in
[0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL at a random point during `add` or `remove` | normal operation | every add or remove that reported success is in the store, and the store still opens | 0 acknowledged items lost in 100 kill trials |
| QS-2 | QG-2 | a new command is added | the existing code base | only `cli.py` and at most one new module change | 0 other files changed across the next 3 commands added |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
