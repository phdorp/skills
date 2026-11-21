# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|

### Stakeholders

## 2. Constraints

## 3. Context and scope

The system boundary and the file it keeps outside itself are described in
[README › How it works](../../README.md#how-it-works).

## 4. Solution strategy

The catalog is one JSON file, written through a temporary file and renamed into place. See
[ADR 0001](../decisions/0001-store-books-in-one-json-file.md).

## 5. Building block view

The three parts (`cli`, `catalog`, `isbn`) are described in
[README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [docs/decisions/](../decisions/). The ADR
"Record architecture decisions" (proposed as 0003, not yet written) lists which decisions are
made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
