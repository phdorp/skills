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

The command line and the catalog file (`~/.shelf.json`, or the path in `SHELF_FILE`) are described in [README › How it works](../../README.md#how-it-works).

## 4. Solution strategy

The catalog is one JSON file: [ADR 0001](../decisions/0001-store-books-in-one-json-file.md). ISBNs are checked locally: [ADR 0002](../decisions/0002-validate-isbn-locally.md).

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

The parts as they are today are described in [README › How it works](../../README.md#how-it-works).

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The decision records are in [docs/decisions/](../decisions/). The ADR "Record architecture decisions" is linked here once the architect confirms its proposal.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
