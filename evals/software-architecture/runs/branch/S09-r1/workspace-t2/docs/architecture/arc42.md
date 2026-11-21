# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | The product's core function; it fixes what the store holds. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | Shapes the storage format and write path. |
| R-3 | Runs with only the Python standard library. | 3 | active | A third-party-dependency decision; the central list covers it. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Constrains module boundaries and how features are added. |

Gap check: the architect left out Security: confidentiality and Interaction capability: user
error protection. No requirement was added.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-4 | QS-1 |

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

No ADR is accepted yet. The ADRs live in [`../adr/`](../adr/). The decision list that says which
decisions the architect makes centrally is the ADR
[0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md), status
`proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a new command is added | normal development | the change touches cli.py and at most one new module; store.py and model.py are unchanged | at most 2 files changed; 0 changes to store.py or model.py |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
